import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the straight-line distance between
    two geographical coordinates in kilometres.
    """

    earth_radius = 6371.0

    lat1 = math.radians(float(lat1))
    lon1 = math.radians(float(lon1))
    lat2 = math.radians(float(lat2))
    lon2 = math.radians(float(lon2))

    difference_latitude = lat2 - lat1
    difference_longitude = lon2 - lon1

    a = (
        math.sin(difference_latitude / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(difference_longitude / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c

    return round(distance, 2)