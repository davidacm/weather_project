#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from app import conversions
from unitTests.data_tests.conversions_data import cardinal_tests, wind_scale_tests, cloud_scale_tests


class _TestConversionFunction(unittest.TestCase):
    """This is a general class to test those functions that returns a string according to the value received.
    you must setUp the common test cases (self.test_cases )
    and if exist, exception cases (self.exception_cases ).
    for thest cases, each item is a tuple with two elements: the decired values to try and the value expected for those values.
    for exception test cases, just set a list of values to test.
    the self.function is the function to be tested.
    """

    def function_test(self, value):
        raise NotImplementedError("please set the function to test")

    def exception_test(self, exception: Exception, values: list):
        """test if the function throws the given exception with the specified values.

        Args:
            exception (Exception): the exception to test.
            values (list): a list of values to test.
        """
        with self.assertRaises(exception):
            for k in values:
                self.function_test(k)

    def value_test(self, value, expected_value):
        """test if the given value is correct according to the expected value.

        Args:
            value: the input value.
            expected_value: the expected result.
        """
        with self.subTest(value=value, expected=expected_value):
            self.assertEqual(self.function_test(value,), expected_value)

    def cases_tests(self, tests: list[tuple[tuple, object]]):
        """test a list of values that are related with a specific result, for each item in the given list.

        Args:
            tests (list[tuple[tuple, object]]): the tests cases.
        """
        for values, result in tests:
            for value in values:
                self.value_test(value, result)


class TestCardinals(_TestConversionFunction):
    def setUp(self) -> None:
        self.function_test = conversions.degrees_to_cardinal

    def test_range_exceptions(self):
        self.exception_test(conversions.DegreesOutOfRangeError, [-1, 361])

    def test_degrees_to_cardinal_data(self):
        self.cases_tests(cardinal_tests)


class TestWindScale(_TestConversionFunction):
    def setUp(self) -> None:
        self.function_test = conversions.wind_velocity_to_description

    def test_negative_exception(self):
        self.exception_test(ValueError, [-1])

    def test_wind_scale(self):
        self.cases_tests(wind_scale_tests)


class TestCloudScale(_TestConversionFunction):
    def setUp(self) -> None:
        self.function_test = conversions.cloudiness_percent_to_description

    def test_out_range_exception(self):
        self.exception_test(ValueError, [-1, 101])

    def test_cloud_scale(self):
        self.cases_tests(cloud_scale_tests)
