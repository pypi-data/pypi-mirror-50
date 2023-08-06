from typing import Union, List, Tuple
from enum import Enum, unique
from .methods import haversine_formula, spherical_law_of_cosines_formula, vincenty_formula


EARTH_RADIUS = 6372795  # meters

@unique
class CalcMethod(Enum):
    SPHERICAL_LAW_OF_COSINES = 0
    HAVERSINE = 1
    VINCENTY = 2


def calc_distance(from_coords: Union[List[float], Tuple[float, float]],
                  to_coords: Union[List[float], Tuple[float, float]],
                  method: CalcMethod = CalcMethod.VINCENTY) -> float:
    """
    Calculate the distance between two GPS coordinates in meters

    *Example:*

    ```python
    >>> from_coords = (77.1539, -120.398)
    >>> to_coords = (77.1804, 129.55)
    >>> dist = calc_distance(from_coords, to_coords)
    >>> print(dist)
    2332668.5392066096
    ```
    """
    methods = {
        CalcMethod.SPHERICAL_LAW_OF_COSINES: spherical_law_of_cosines_formula,
        CalcMethod.HAVERSINE: haversine_formula,
        CalcMethod.VINCENTY: vincenty_formula
    }

    angle_degrees = methods[method](from_coords, to_coords)

    return angle_degrees * EARTH_RADIUS
