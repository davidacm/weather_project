#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.conversions import QUADRANTS

# Test data for cardinals degrees boundaries.
# 3 test per quadrant. boundaries and center, with max two decimals.
cardinal_tests = [
    # nort
    ((348.76, 0, 11.25), QUADRANTS[0]),
    # North-Northeast
    ((11.26, 22.5, 33.75), QUADRANTS[1]),
    # Northeast
    ((33.76, 45, 56.25), QUADRANTS[2]),
    # East-Northeast
    ((56.26, 67.5, 78.75), QUADRANTS[3]),
    # East
    ((78.76, 90, 101.25), QUADRANTS[4]),
    # East-Southeast
    ((101.26, 112.5, 123.75), QUADRANTS[5]),
    # Southeast
    ((123.76, 135, 146.25), QUADRANTS[6]),
    # South-Southeast
    ((146.26, 157.5, 168.75), QUADRANTS[7]),
    # South
    ((168.76, 180, 191.25), QUADRANTS[8]),
    # South-Southwest
    ((191.26, 202.5, 213.75), QUADRANTS[9]),
    # Southwest
    ((213.76, 225, 236.25), QUADRANTS[10]),
    # West-Southwest
    ((236.26, 247.5, 258.75), QUADRANTS[11]),
    # West
    ((258.76, 270, 281.25), QUADRANTS[12]),
    # West-Northwest
    ((281.26, 292.5, 303.75), QUADRANTS[13]),
    # Northwest
    ((303.76, 315, 326.25), QUADRANTS[14]),
    # North-Northwest
    ((326.26, 337.5, 348.75), QUADRANTS[15]),
]


wind_scale_tests = [
    ((0, 0.4), "Calm"),
    ((0.5, 1.5), "Light air"),
    ((1.6, 3.3), "Light breeze"),
    ((3.4, 5.4), "Gentle breeze"),
    ((5.5, 7.9), "Moderate breeze"),
    ((8, 10.7), "Fresh breeze"),
    ((10.8, 13.8), "Strong breeze"),
    ((13.9, 17.1), "Moderate gale"),
    ((17.2, 20.7), "Fresh gale"),
    ((20.8, 24.4), "Strong gale"),
    ((24.5, 28.4), "Whole gale"),
    ((28.5, 32.6), "Storm"),
    ((32.7, 40, 50), "Hurricane"),
]


cloud_scale_tests = [
    ((0, 10), "clear sky"),
    ((11, 24), "few clouds"),
    ((25, 50), "scattered clouds"),
    ((51, 84), "broken clouds"),
    ((85, 100), "overcast clouds"),
]
