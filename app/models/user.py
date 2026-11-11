from datetime import datetime, timezone, timedelta

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="patient"
    )

    # Email verification status
    is_email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc)
    )
    
    #OTP storage
    otp_hash = db.Column(
        db.String(256),
        nullable=True
    )
    
    otp_expires_at = db.Column(
        db.DateTime,
        nullable=True
    )
    
    otp_purpose = db.Column(
        db.String(20),
        nullable=True
    )
    
    #Password methods
    def set_password(self, password):
        """Store a securely hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the entered password."""
        return check_password_hash(
            self.password_hash,
            password
        )
        
    #OTP methods
    def set_otp(self, otp, purpose):
        self.otp_hash = generate_password_hash(otp)
        self.otp_expires_at = (datetime.now(timezone.utc) + timedelta(minutes=5))
        self.otp_purpose = purpose

    def verify_otp(self, otp):
        if not self.otp_hash or not self.otp_expires_at:
            return False
        expiry = self.otp_expires_at
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expiry:
            return False
        return check_password_hash(
            self.otp_hash,
            otp
        )

    def clear_otp(self):
        self.otp_hash = None
        self.otp_expires_at = None
        self.otp_purpose = None    

    def __repr__(self):
        return f"<User {self.email}>"