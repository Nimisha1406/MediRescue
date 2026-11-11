import secrets

from flask import current_app
from flask_mail import Message

from extensions import db, mail


def generate_otp():
    """Generate a secure 6-digit OTP."""
    return str(secrets.randbelow(900000) + 100000)


def send_otp_email(user, otp, purpose):
    """Send OTP to the user's registered email."""

    if purpose == "register":
        subject = "MediRescue - Email Verification"
        heading = "Verify Your Email Address"
    else:
        subject = "MediRescue - Login Verification"
        heading = "Login Verification"

    expiry = current_app.config.get(
        "OTP_EXPIRY_MINUTES", 5
    )

    message = Message(
        subject=subject,
        recipients=[user.email]
    )

    message.body = f"""
Hello {user.name},

Your MediRescue verification OTP is:

{otp}

This OTP is valid for {expiry} minutes.

Please do not share this OTP with anyone.

If you did not request this verification,
please ignore this email.

Regards,
MediRescue Team
"""

    message.html = f"""
    <div style="font-family: Arial; padding: 20px;">
        <h2 style="color: #0d6efd;">MediRescue</h2>
        <h3>{heading}</h3>

        <p>Hello {user.name},</p>

        <p>Your verification OTP is:</p>

        <h1 style="letter-spacing: 8px; color: #0d6efd;">
            {otp}
        </h1>

        <p>This OTP is valid for {expiry} minutes.</p>

        <p>Please do not share this OTP with anyone.</p>

        <p>Regards,<br>MediRescue Team</p>
    </div>
    """

    mail.send(message)


def create_and_send_otp(user, purpose):
    """Generate, store and email an OTP."""

    otp = generate_otp()

    user.set_otp(otp, purpose)

    db.session.commit()

    try:
        send_otp_email(user, otp, purpose)

    except Exception:
        current_app.logger.exception(
            "Failed to send verification email."
        )

        user.clear_otp()
        db.session.commit()

        return False

    return True