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
            "unicode_strings": "Hello you",
            "booleans": True,
            "none": None,
        }

    return parameterized.expand(list(values.items()))
