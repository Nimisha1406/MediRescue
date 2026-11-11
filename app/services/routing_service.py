import json
from urllib.request import urlopen
from urllib.parse import quote
from app.utils.distance import haversine_distance


def calculate_route(
    pickup_latitude,
    pickup_longitude,
    destination_latitude,
    destination_longitude
):
    """
    Calculate road distance, travel time and route geometry
    using the OSRM routing API.
    """

    try:
        coordinates = (
            f"{pickup_longitude},{pickup_latitude};"
            f"{destination_longitude},{destination_latitude}"
        )

        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            + quote(coordinates, safe=",;")
            + "?overview=full&geometries=geojson"
        )

        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("code") != "Ok" or not data.get("routes"):
            return None

        route = data["routes"][0]

        return {
            "distance_km": round(route["distance"] / 1000, 2),
            "duration_minutes": round(route["duration"] / 60, 2),
            "geometry": route["geometry"]
        }

    except Exception:
        # Fallback if the routing service is unavailable.
        straight_distance = haversine_distance(
            pickup_latitude,
            pickup_longitude,
            destination_latitude,
            destination_longitude
        )

        return {
            "distance_km": round(straight_distance, 2),
            "duration_minutes": None,
            "geometry": None
        }