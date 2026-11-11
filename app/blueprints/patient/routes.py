from flask import render_template
from flask_login import login_required, current_user

from app.blueprints.patient import patient_bp


@patient_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role == "admin":
        from flask import redirect, url_for
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "main/dashboard.html",
        user=current_user
    )


@patient_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "patient/profile.html",
        user=current_user
    )