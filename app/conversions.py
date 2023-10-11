#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


class DegreesOutOfRangeError(Exception):
    def __init__(self, degrees):
        self.degrees = degrees
        super().__init__(f"The degrees {degrees} are out of range (0 to 360).")


# Quadrants list. The last is repeated, for those cases when (deg > 348.75) due to the way the index is calculated.
QUADRANTS = ("North", "North-Northeast", "Northeast", "East-Northeast",
             "East", "East-Southeast", "Southeast", "South-Southeast",
             "South", "South-Southwest", "Southwest", "West-Southwest",
             "West", "West-Northwest", "Northwest", "North-Northwest",
             "North",)

_quadrant_size = 360 / (len(QUADRANTS) - 1)
_deg_rotate = _quadrant_size / 2 - 0.01


def degrees_to_cardinal(deg: float) -> str:
    """converts degrees to quadrants, (360 degrees / 16 quadrants). 0 and 360 degrees are equivalent.

    Args:
        deg (float): the degrees to convert.

    Raises:
        DegreesOutOfRangeError: if deg is not between 0 and 360.

    Returns:
        str: the corresponding cardinal name associated with the specified deg.
    """
    if 0 <= deg <= 360:
        # convert quadrant to index, from 0 to 16.
        # rotate deg to the right, in order to center the quadrants. If not, the  index calc won't work.
        index = math.floor((deg + _deg_rotate) / _quadrant_size)
        return QUADRANTS[index]
    raise DegreesOutOfRangeError(deg)


# wind velocity squale (in m/s) for descriptions, according to Beaufort Wind Scale from:
# http://gyre.umeoce.maine.edu/data/gomoos/buoy/php/variable_description.php?variable=wind_2_speed
# https://en.wikipedia.org/wiki/Beaufort_scale

# this list must always be sorted.
WIND_SCALE_DESCRIPTIONS = [
    (0, "Calm"),
    (0.5, "Light air"),
    (1.6, "Light breeze"),
    (3.4, "Gentle breeze"),
    (5.5, "Moderate breeze"),
    (8, "Fresh breeze"),
    (10.8, "Strong breeze"),
    (13.9, "Moderate gale"),
    (17.2, "Fresh gale"),
    (20.8, "Strong gale"),
    (24.5, "Whole gale"),
    (28.5, "Storm"),
    (32.7, "Hurricane"),
]


def _value_to_description(value: str, ranges: list[tuple[int, str]]) -> str:
    """converts a value to a more human understandable form, according to the specified range descriptions.

    the function will return the description related with the range in this way: prev_value <= value < next_value.
    if value is greater than the last item of ranges, the last description will be returned.

    Args:
        value (str): the value to get teh association.

        ranges (list[tuple[int, str]]): a sorted non-empty list of ranges of the descriptions.
        in tuples of (value, description).
        Value is the minimum range to relate with the description.
        E.G. [(0, 'value 1'), (1, 'value 2')]

    Returns:
        string: a string with the associated wind scale

    exceptions:
        valueError: if the value is less than the lowest value in the list of ranges.
    """
    if value < ranges[0][0]:
        raise ValueError("The value is less than the lowest possible number", value)

    description = ""
    for v,d in ranges:
        if value >= v:
            description = d
        else:
            break
    return description


def wind_velocity_to_description(velocity: str) -> str:
    """converts wind speed to a more human understandable form, according to Beaufort Wind Scale.

    Args:
        velocity (str): the wind velocity.

    Returns:
        string: a string with the associated wind scale
    """
    return _value_to_description(velocity, WIND_SCALE_DESCRIPTIONS)


# cloudiness scale according to:
# https://openweathermap.org/weather-conditions
CLOUDINESS_SCALE = [
    (0, "clear sky"),
    (11, "few clouds"),
    (25, "scattered clouds"),
    (51, "broken clouds"),
    (85, "overcast clouds"),
]


def cloudiness_percent_to_description(cloud_percent: float) -> str:
    """Converts cloud percentage to a human description.

    Args:
        cloud_percent (float): cloudiness in percent. Range from 0 to 100.

    Raises:
        ValueError: if the cloud_percent is out of range.

    Returns:
        str: _description_
    """
    if 0 <= cloud_percent <= 360:
        return _value_to_description(cloud_percent, CLOUDINESS_SCALE)
    raise ValueError("The cloud percent must be between 0 and 100", cloud_percent)


def celsius_to_fahrenheit(celsius: float) -> float:
    """a simple celsius to fahrenheit formula.

    this function won't be tested for now, as the code was obtained from an external source.

    Args:
        celsius (float): the temperature in celsius

    Returns:
        float: temperature in fahrenheit
    """
    return round((celsius * 1.8) + 32, 2)
