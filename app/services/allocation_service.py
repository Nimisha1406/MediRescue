from app.models.ambulance import Ambulance
from app.utils.distance import haversine_distance


def find_nearest_ambulance(latitude, longitude):
    """
    Find the nearest available ambulance
    using the patient's pickup coordinates.
    """

    available_ambulances = Ambulance.query.filter_by(
        status="available"
    ).all()

    if not available_ambulances:
        return None

    nearest_ambulance = None
    shortest_distance = float("inf")

    for ambulance in available_ambulances:

        distance = haversine_distance(
            latitude,
            longitude,
            ambulance.latitude,
            ambulance.longitude
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_ambulance = ambulance

    return nearest_ambulance