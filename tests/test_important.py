"""
Test important object marking.
"""

from unittest import TestCase

from chromalog.important import Important

from .common import repeat_for_values


class ImportantTests(TestCase):
    @repeat_for_values()
    def test_string_rendering_of_important(self, _, value):
        self.assertEqual('{}'.format(value), '{}'.format(Important(value)))

    @repeat_for_values()
    def test_unicode_rendering_of_important(self, _, value):
        self.assertEqual(u'{}'.format(value), u'{}'.format(Important(value)))

    @repeat_for_values()
    def test_important_objects_dont_compare_to_their_value_as(self, _, value):
        self.assertNotEqual(value, Important(value))

    @repeat_for_values()
    def test_important_objects_have_a_color_tag_attribute_for(self, _, value):
        self.assertTrue(hasattr(Important(value), 'color_tag'))
        self.assertTrue(
            hasattr(Important(value, color_tag='info'), 'color_tag'),
        )

    @repeat_for_values()
    def test_important_objects_can_be_nested_for(self, _, value):
        obj = Important(Important(value, 'b'), 'a')
        self.assertEqual(['a', 'b'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Important(Important(value, ['b', 'c']), 'a')
        self.assertEqual(['a', 'b', 'c'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Important(Important(value, 'c'), ['a', 'b'])
        self.assertEqual(['a', 'b', 'c'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Important(Important(value, ['c', 'd']), ['a', 'b'])
        self.assertEqual(['a', 'b', 'c', 'd'], obj.color_tag)
        self.assertEqual(value, obj.obj)
