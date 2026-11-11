from datetime import datetime

from extensions import db


class Ambulance(db.Model):

    __tablename__ = "ambulances"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vehicle_no = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    driver_name = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="available"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def is_available(self):
        return self.status == "available"

    def update_location(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __repr__(self):
        return f"<Ambulance {self.vehicle_no}>"