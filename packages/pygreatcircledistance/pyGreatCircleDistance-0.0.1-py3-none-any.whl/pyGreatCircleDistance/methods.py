import math
from .utils import coords_to_radians


def spherical_law_of_cosines_formula(from_coords, to_coords):
    from_radians = coords_to_radians(from_coords)
    to_radians = coords_to_radians(to_coords)

    cos_latitudes = [math.cos(from_radians[0]), math.cos(to_radians[0])]
    sin_latitudes = [math.sin(from_radians[0]), math.sin(to_radians[0])]
    delta_longitudes = to_radians[1] - from_radians[1]

    angle_degrees = math.acos(
        sin_latitudes[0] * sin_latitudes[1] +
        cos_latitudes[0] * cos_latitudes[1] * math.cos(delta_longitudes)
    )

    return angle_degrees


def haversine_formula(from_coords, to_coords):
    from_radians = coords_to_radians(from_coords)
    to_radians = coords_to_radians(to_coords)

    delta_longitudes = to_radians[1] - from_radians[1]

    angle_degrees = 2 * math.asin(
        math.sqrt(
            math.pow(math.sin((to_radians[0] - from_radians[0])/2), 2) +
            math.cos(from_radians[0]) * math.cos(to_radians[0]) * math.pow(math.sin(delta_longitudes/2), 2)
        )
    )

    return angle_degrees


def vincenty_formula(from_coords, to_coords):
    from_radians = coords_to_radians(from_coords)
    to_radians = coords_to_radians(to_coords)

    cos_latitudes = [math.cos(from_radians[0]), math.cos(to_radians[0])]
    sin_latitudes = [math.sin(from_radians[0]), math.sin(to_radians[0])]
    delta_longitudes = to_radians[1] - from_radians[1]

    numerator = math.sqrt(
        math.pow(cos_latitudes[1] * math.sin(delta_longitudes), 2) +
        math.pow(
            cos_latitudes[0] * sin_latitudes[1] -
            sin_latitudes[0] * cos_latitudes[1] * math.cos(delta_longitudes),
        2))
    denominator = sin_latitudes[0] * sin_latitudes[1] + \
                  cos_latitudes[0] * cos_latitudes[1] * math.cos(delta_longitudes)

    angle_degrees = math.atan2(numerator, denominator)

    return angle_degrees
