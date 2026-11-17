import time

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from flask_login import login_user, logout_user, login_required

from app.blueprints.auth import auth_bp
from app.models.user import User
from extensions import db
from app.services.otp_service import create_and_send_otp


def start_otp_verification(user, purpose):
    """Store pending verification details and send an OTP."""

    if not create_and_send_otp(user, purpose):
        flash("Unable to send OTP. Please check your email configuration and try again.", "danger")
        return False

    session["pending_user_id"] = user.id
    session["pending_otp_purpose"] = purpose
    session["otp_attempts"] = 0
    session["otp_last_sent_at"] = time.time()

    return True


def dashboard_redirect(user):
    """Redirect user according to their role."""

    if user.role == "admin":
        return redirect(url_for("admin.dashboard"))

    return redirect(url_for("main.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            # First verify the email if it has not been verified before.
            purpose = "login" if user.is_email_verified else "register"

            if start_otp_verification(user, purpose):
                flash("A verification OTP has been sent to your email.", "info")
                return redirect(url_for("auth.verify_otp"))

            return redirect(url_for("auth.login"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not all([name, email, phone, password]):
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered. Please login instead.", "danger")
            return redirect(url_for("auth.login"))

        new_user = User(
            name=name,
            email=email,
            phone=phone,
            role="patient"
        )

        new_user.set_password(password)
        new_user.is_email_verified = False

        db.session.add(new_user)
        db.session.commit()

        if start_otp_verification(new_user, "register"):
            flash("Registration successful! Verify your email using the OTP.", "success")
            return redirect(url_for("auth.verify_otp"))

        # Remove the pending account if the verification email could not be sent.
        db.session.delete(new_user)
        db.session.commit()

        return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    user_id = session.get("pending_user_id")
    purpose = session.get("pending_otp_purpose")

    if not user_id or not purpose:
        flash("Please login or register first.", "warning")
        return redirect(url_for("auth.login"))

    user = db.session.get(User, user_id)

    if not user:
        session.pop("pending_user_id", None)
        session.pop("pending_otp_purpose", None)
        flash("User account not found. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        otp = request.form.get("otp", "").strip()

        if not otp.isdigit() or len(otp) != 6:
            flash("Please enter a valid 6-digit OTP.", "danger")
            return redirect(url_for("auth.verify_otp"))

        attempts = session.get("otp_attempts", 0)

        if attempts >= 5:
            user.clear_otp()
            db.session.commit()

            session.pop("pending_user_id", None)
            session.pop("pending_otp_purpose", None)
            session.pop("otp_attempts", None)

            flash("Too many incorrect attempts. Please login again.", "danger")
            return redirect(url_for("auth.login"))

        if user.otp_purpose != purpose or not user.verify_otp(otp):
            session["otp_attempts"] = attempts + 1
            flash("Incorrect or expired OTP. Please try again.", "danger")
            return redirect(url_for("auth.verify_otp"))

        # OTP verified successfully.
        if purpose == "register":
            user.is_email_verified = True

        user.clear_otp()
        db.session.commit()

        session.pop("pending_user_id", None)
        session.pop("pending_otp_purpose", None)
        session.pop("otp_attempts", None)
        session.pop("otp_last_sent_at", None)

        login_user(user)

        flash("Email verified successfully! Welcome to MediRescue.", "success")
        return dashboard_redirect(user)

    return render_template("auth/verify_otp.html")


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():

    user_id = session.get("pending_user_id")
    purpose = session.get("pending_otp_purpose")

    if not user_id or not purpose:
        flash("Please login or register first.", "warning")
        return redirect(url_for("auth.login"))

    last_sent = session.get("otp_last_sent_at", 0)

    if time.time() - last_sent < 60:
        flash("Please wait 60 seconds before requesting another OTP.", "warning")
        return redirect(url_for("auth.verify_otp"))

    user = db.session.get(User, user_id)

    if not user:
        flash("User account not found.", "danger")
        return redirect(url_for("auth.login"))

    if create_and_send_otp(user, purpose):
        session["otp_last_sent_at"] = time.time()
        session["otp_attempts"] = 0
        flash("A new OTP has been sent to your email.", "success")
    else:
        flash("Unable to send OTP. Please try again later.", "danger")

    return redirect(url_for("auth.verify_otp"))


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    session.pop("pending_user_id", None)
    session.pop("pending_otp_purpose", None)
    session.pop("otp_attempts", None)
    session.pop("otp_last_sent_at", None)

    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Send a password-reset OTP to the registered email."""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not email:
            flash("Please enter your registered email address.", "danger")
            return redirect(url_for("auth.forgot_password"))

        user = User.query.filter_by(email=email).first()

        # Use a generic response to avoid revealing whether an account exists.
        if user and user.is_email_verified:
            if create_and_send_otp(user, "reset_password"):
                session["pending_reset_user_id"] = user.id
                flash(
                    "If your account is registered, a password-reset OTP "
                    "has been sent to your email.",
                    "info"
                )
                return redirect(url_for("auth.reset_password"))

        flash(
            "If your account is registered, a password-reset OTP "
            "has been sent to your email.",
            "info"
        )
        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html")



@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Verify reset OTP and allow the user to set a new password."""

    user_id = session.get("pending_reset_user_id")

    if not user_id:
        flash("Please request a password-reset OTP first.", "warning")
        return redirect(url_for("auth.forgot_password"))

    user = db.session.get(User, user_id)

    if not user or user.otp_purpose != "reset_password":
        session.pop("pending_reset_user_id", None)
        flash("Invalid or expired password-reset request.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        otp = request.form.get("otp", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not otp.isdigit() or len(otp) != 6:
            flash("Please enter a valid 6-digit OTP.", "danger")
            return redirect(url_for("auth.reset_password"))

        if not user.verify_otp(otp):
            flash("Incorrect or expired OTP. Please try again.", "danger")
            return redirect(url_for("auth.reset_password"))

        if user.otp_purpose != "reset_password":
            flash("Invalid OTP purpose.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("auth.reset_password"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.reset_password"))

        # Update password and clear OTP
        user.set_password(password)
        user.clear_otp()

        db.session.commit()

        session.pop("pending_reset_user_id", None)

        flash(
            "Your password has been reset successfully. Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")