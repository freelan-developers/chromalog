# coding=utf-8

"""
Common functions for tests.
"""

from nose_parameterized import parameterized


def repeat_for_values(values=None):
    if not values:
        values = {
            "integers": 42,
            "floats": 3.14,
            "strings": "Hello you",
            "unicode_strings": u"éléphant is the french for elephant",
            "booleans": True,
            "none": None,
        }

    return parameterized.expand(list(values.items()))


def repeat_for_integral_values(values=None):
    if not values:
        values = {
            "integers": 42,
            "floats": 3.14,
            "booleans": True,
        }

    return parameterized.expand(list(values.items()))
