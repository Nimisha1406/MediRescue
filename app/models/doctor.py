from datetime import datetime

from extensions import db


class Doctor(db.Model):

    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    specialty = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True
    )

    consultation_fee = db.Column(
        db.Float,
        nullable=False,
        default=500
    )

    experience = db.Column(
        db.Integer,
        default=0
    )

    availability = db.Column(
        db.String(100),
        default="Available"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Doctor {self.name}>"