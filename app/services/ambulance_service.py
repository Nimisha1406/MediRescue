from extensions import db
from app.models.ambulance import Ambulance
from app.services.allocation_service import find_nearest_ambulance


def get_available_ambulances():
    """Return all available ambulances."""

    return Ambulance.query.filter_by(
        status="available"
    ).all()


def assign_ambulance(latitude, longitude):
    """
    Find and assign the nearest available ambulance.
    """

    ambulance = find_nearest_ambulance(
        float(latitude),
        float(longitude)
    )

    if ambulance is None:
        return None

    ambulance.status = "booked"
    db.session.commit()

    return ambulance


def release_ambulance(ambulance_id):
    """Make an ambulance available again after a trip."""

    ambulance = db.session.get(Ambulance, ambulance_id)

    if ambulance is None:
        return False

    ambulance.status = "available"
    db.session.commit()

    return True


def update_ambulance_status(ambulance_id, status):
    """Update the status of an ambulance."""

    allowed_statuses = ["available", "booked", "maintenance"]

    if status not in allowed_statuses:
        return False

    ambulance = db.session.get(Ambulance, ambulance_id)

    if ambulance is None:
        return False

    ambulance.status = status
    db.session.commit()

    return True