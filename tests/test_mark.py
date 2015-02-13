"""
Test object marking.
"""

from unittest import TestCase

from chromalog.mark import Mark

from .common import (
    repeat_for_values,
    repeat_for_integral_values,
)


class MarkTests(TestCase):
    @repeat_for_values()
    def test_string_rendering_of_marked(self, _, value):
        self.assertEqual('{}'.format(value), '{}'.format(Mark(value, 'a')))

    @repeat_for_values()
    def test_unicode_rendering_of_marked(self, _, value):
        self.assertEqual(u'{}'.format(value), u'{}'.format(Mark(value, 'a')))

    @repeat_for_integral_values()
    def test_int_rendering_of_marked(self, _, value):
        self.assertEqual('%d' % value, '%d' % Mark(value, 'a'))

    @repeat_for_integral_values()
    def test_hexadecimal_int_rendering_of_marked(self, _, value):
        self.assertEqual('%x' % value, '%x' % Mark(value, 'a'))

    @repeat_for_integral_values()
    def test_float_rendering_of_marked(self, _, value):
        self.assertEqual('%f' % value, '%f' % Mark(value, 'a'))

    @repeat_for_values()
    def test_marked_objects_dont_compare_to_their_value_as(self, _, value):
        self.assertNotEqual(value, Mark(value, 'a'))

    @repeat_for_values()
    def test_marked_objects_have_a_color_tag_attribute_for(self, _, value):
        self.assertTrue(hasattr(Mark(value, 'a'), 'color_tag'))
        self.assertTrue(
            hasattr(Mark(value, color_tag='info'), 'color_tag'),
        )

    @repeat_for_values()
    def test_marked_objects_can_be_nested_for(self, _, value):
        obj = Mark(Mark(value, 'b'), 'a')
        self.assertEqual(['a', 'b'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Mark(Mark(value, ['b', 'c']), 'a')
        self.assertEqual(['a', 'b', 'c'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Mark(Mark(value, 'c'), ['a', 'b'])
        self.assertEqual(['a', 'b', 'c'], obj.color_tag)
        self.assertEqual(value, obj.obj)

        obj = Mark(Mark(value, ['c', 'd']), ['a', 'b'])
        self.assertEqual(['a', 'b', 'c', 'd'], obj.color_tag)
        self.assertEqual(value, obj.obj)
