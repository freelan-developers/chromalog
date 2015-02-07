"""
Test important object marking.
"""

from unittest import TestCase

from chromalog.important import (
    Important,
    hl,
)


class ImportantTests(TestCase):
    def test_important_integers_can_render_as_strings(self):
        value = 42
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_floats_can_render_as_strings(self):
        value = 3.14
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_strings_can_render_as_strings(self):
        value = "Hello you"
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_unicode_strings_can_render_as_strings(self):
        value = u"Hello you"
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_booleans_can_render_as_strings(self):
        value = True
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_none_can_render_as_strings(self):
        value = None
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    def test_important_integers_can_render_as_unicode_strings(self):
        value = 42
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_important_floats_can_render_as_unicode_strings(self):
        value = 3.14
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_important_strings_can_render_as_unicode_strings(self):
        value = "Hello you"
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_important_unicode_strings_can_render_as_unicode_strings(self):
        value = u"Hello you"
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_important_booleans_can_render_as_unicode_strings(self):
        value = True
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_important_none_can_render_as_unicode_strings(self):
        value = None
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    def test_hl_returns_important_objects(self):
        value = "Hello you"
        self.assertEqual(Important(value), hl(value))

    def test_important_objects_do_not_compare_to_their_value(self):
        value = "Hello you"
        self.assertNotEqual(value, Important(value))
