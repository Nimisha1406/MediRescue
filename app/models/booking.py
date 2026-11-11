from datetime import datetime

from extensions import db


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    ambulance_id = db.Column(
        db.Integer,
        db.ForeignKey("ambulances.id"),
        nullable=True
    )

    pickup_location = db.Column(
        db.String(250),
        nullable=False
    )

    destination = db.Column(
        db.String(250),
        nullable=False
    )

    pickup_latitude = db.Column(
        db.Float,
        nullable=False
    )

    pickup_longitude = db.Column(
        db.Float,
        nullable=False
    )

    destination_latitude = db.Column(
        db.Float,
        nullable=True
    )

    destination_longitude = db.Column(
        db.Float,
        nullable=True
    )

    emergency_type = db.Column(
        db.String(50),
        default="General"
    )

    distance = db.Column(
        db.Float,
        nullable=True
    )

    estimated_time = db.Column(
        db.Float,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    patient = db.relationship(
        "User",
        backref=db.backref("bookings", lazy=True)
    )

    ambulance = db.relationship(
        "Ambulance",
        backref=db.backref("bookings", lazy=True)
    )

    def __repr__(self):
        return f"<Booking {self.id}>"