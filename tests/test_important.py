"""
Test important object marking.
"""

from unittest import TestCase
from nose_parameterized import parameterized

from chromalog.important import (
    Important,
    hl,
)


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

    return parameterized.expand(values.items())


class ImportantTests(TestCase):
    @repeat_for_values()
    def test_string_rendering_of_important(self, _, value):
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    @repeat_for_values()
    def test_unicode_rendering_of_important(self, _, value):
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    @repeat_for_values()
    def test_hl_returns_important_objects_for(self, _, value):
        self.assertEqual(Important(value), hl(value))

    @repeat_for_values()
    def test_important_objects_do_not_compare_to_their_value_as(self, _, value):
        self.assertNotEqual(value, Important(value))
