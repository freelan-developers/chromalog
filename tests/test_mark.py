"""
Test object marking.
"""

from unittest import TestCase
from six import (
    PY2,
    PY3,
)

from chromalog.mark import Mark

from .common import (
    repeat_for_values,
    repeat_for_integral_values,
)


class MarkTests(TestCase):
    @repeat_for_values()
    def test_string_rendering_of_marked(self, _, value):
        # Python2 non-unicode string want to use the 'ascii' encoding for this
        # conversion, which cannot work.
        if PY2 and isinstance(value, unicode):
            return

        self.assertEqual('{0}'.format(value), '{0}'.format(Mark(value, 'a')))

    @repeat_for_values()
    def test_unicode_rendering_of_marked(self, _, value):
        self.assertEqual(u'{0}'.format(value), u'{0}'.format(Mark(value, 'a')))

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

    @repeat_for_values({
        'simple_name': 'alpha',
        'underscore_name': 'alpha_beta',
    })
    def test_simple_helpers_with(self, _, name):
        import chromalog.mark.helpers.simple as helpers
        helper = getattr(helpers, name)
        self.assertEqual([name], helper(42).color_tag)

    @repeat_for_values({
        'simple_name': 'alpha_or_beta',
        'underscore_name': 'alpha_beta_or_gamma_delta',
    })
    def test_conditional_helpers_with(self, _, name):
        import chromalog.mark.helpers.conditional as helpers
        helper = getattr(helpers, name)
        true_color_tag, false_color_tag = name.split('_or_')
        self.assertEqual([true_color_tag], helper(42, True).color_tag)
        self.assertEqual([false_color_tag], helper(42, False).color_tag)
        self.assertEqual([true_color_tag], helper(True).color_tag)
        self.assertEqual([false_color_tag], helper(False).color_tag)

    def test_explicit_unicode_in_python3(self):
        if PY3:
            self.assertEqual(
                u'test',
                Mark(u'test', 'foo').__unicode__(),
            )
