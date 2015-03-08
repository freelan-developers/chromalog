"""
Test colorizers.
"""
from builtins import str  # noqa

from unittest import TestCase
from six import PY3

from chromalog.colorizer import (
    ColorizedObject,
    Colorizer,
    ColorizableMixin,
)
from chromalog.mark import Mark

from .common import repeat_for_values


class ColorizerTests(TestCase):
    def test_colorizer_get_color_pair_not_found(self):
        colorizer = Colorizer({})
        self.assertEqual(('', ''), colorizer.get_color_pair(color_tag=['a']))

    def test_colorizer_get_color_pair_found(self):
        colorizer = Colorizer({
            'a': ('[', ']'),
        })
        self.assertEqual(('[', ']'), colorizer.get_color_pair(color_tag=['a']))

    def test_colorizer_get_color_pair_found_double(self):
        colorizer = Colorizer({
            'a': ('[', ']'),
            'b': ('<', '>'),
        })
        self.assertEqual(
            ('[<', '>]'),
            colorizer.get_color_pair(color_tag=['a', 'b']),
        )

    def test_colorizer_get_color_pair_not_found_with_default(self):
        colorizer = Colorizer(
            {
                'a': ('[', ']'),
                'b': ('<', '>'),
            },
            default_color_tag='b',
        )
        self.assertEqual(('<', '>'), colorizer.get_color_pair(color_tag=['c']))

    def test_colorizer_get_color_pair_not_found_with_disabled_default(self):
        colorizer = Colorizer(
            {
                'a': ('[', ']'),
                'b': ('<', '>'),
            },
            default_color_tag='b',
        )
        self.assertEqual(
            ('', ''),
            colorizer.get_color_pair(color_tag=['c'], use_default=False),
        )

    def test_colorizer_get_color_pair_found_with_context(self):
        colorizer = Colorizer(
            {
                'a': ('[', ']'),
                'b': ('<', '>'),
            },
        )
        self.assertEqual(
            ('><[', ']><'),
            colorizer.get_color_pair(color_tag=['a'], context_color_tag='b'),
        )

    def test_colorizer_get_color_pair_found_with_list_context(self):
        colorizer = Colorizer(
            {
                'a': ('[', ']'),
                'b': ('<', '>'),
                'c': ('(', ')'),
            },
        )
        self.assertEqual(
            (')><([', '])><('),
            colorizer.get_color_pair(
                color_tag=['a'],
                context_color_tag=['b', 'c'],
            ),
        )

    @repeat_for_values()
    def test_colorizer_converts_unknown_types(self, _, value):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('<', '>'),
        })
        self.assertEqual(ColorizedObject(value), colorizer.colorize(value))

    @repeat_for_values()
    def test_colorizer_changes_colorizable_types(self, _, value):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
        })
        self.assertEqual(
            ColorizedObject(Mark(value, 'a'), ('[', ']')),
            colorizer.colorize(Mark(value, 'a')),
        )

    @repeat_for_values()
    def test_colorizer_changes_colorizable_types_with_tags(self, _, value):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('<', '>'),
        })
        self.assertEqual(
            ColorizedObject(Mark(value, ['a', 'b']), ('[<', '>]')),
            colorizer.colorize(Mark(value, ['a', 'b'])),
        )

    @repeat_for_values()
    def test_colorizer_changes_colorizable_types_with_context(self, _, value):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('<', '>'),
        })
        self.assertEqual(
            ColorizedObject(Mark(value, 'a'), ('><[', ']><')),
            colorizer.colorize(Mark(value, 'a'), context_color_tag='b'),
        )

    @repeat_for_values()
    def test_colorizer_changes_colorizable_types_with_tags_and_context(
        self,
        _,
        value,
    ):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('(', ')'),
            'c': ('<', '>'),
        })
        self.assertEqual(
            ColorizedObject(Mark(value, ['a', 'b']), ('><[(', ')]><')),
            colorizer.colorize(Mark(value, ['a', 'b']), context_color_tag='c'),
        )

    @repeat_for_values({
        "default_colorizable": ColorizableMixin(),
        "specific_colorizable": ColorizableMixin(color_tag='info'),
    })
    def test_colorizable_mixin_has_a_color_tag_attribute_for(self, _, value):
        self.assertTrue(hasattr(value, 'color_tag'))

    def test_colorizer_colorizes_with_known_color_tag(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
            },
        )
        result = colorizer.colorize(Mark('hello', color_tag='my_tag'))
        self.assertEqual(
            ColorizedObject(
                Mark(
                    'hello',
                    'my_tag',
                ),
                (
                    'START_MARK',
                    'STOP_MARK',
                ),
            ),
            result,
        )

    def test_colorizer_colorizes_with_known_color_tag_and_default(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
                'default': ('START_DEFAULT_MARK', 'STOP_DEFAULT_MARK')
            },
            default_color_tag='default',
        )
        result = colorizer.colorize(Mark('hello', color_tag='my_tag'))
        self.assertEqual(
            ColorizedObject(
                Mark(
                    'hello',
                    'my_tag',
                ),
                (
                    'START_MARK',
                    'STOP_MARK',
                ),
            ),
            result,
        )

    def test_colorizer_doesnt_colorize_with_unknown_color_tag(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
            },
        )
        result = colorizer.colorize(Mark('hello', color_tag='my_unknown_tag'))
        self.assertEqual(
            ColorizedObject(Mark('hello', 'my_unknown_tag'), ('', '')),
            result,
        )

    def test_colorizer_colorizes_with_unknown_color_tag_and_default(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
                'default': ('START_DEFAULT_MARK', 'STOP_DEFAULT_MARK')
            },
            default_color_tag='default',
        )
        result = colorizer.colorize(Mark('hello', color_tag='my_unknown_tag'))
        self.assertEqual(
            ColorizedObject(
                Mark(
                    'hello',
                    'my_unknown_tag',
                ),
                (
                    'START_DEFAULT_MARK',
                    'STOP_DEFAULT_MARK',
                ),
            ),
            result,
        )

    def test_colorize_message(self):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('(', ')'),
        })
        message = '{}-{}_{a}~{b}'
        args = [42, Mark(42, ['a', 'b'])]
        kwargs = {
            'a': 0,
            'b': Mark(0, ['b', 'a']),
        }
        self.assertEqual(
            '42-[(42)]_0~([0])',
            colorizer.colorize_message(message, *args, **kwargs),
        )

    def test_colorize_message_with_context(self):
        colorizer = Colorizer(color_map={
            'a': ('[', ']'),
            'b': ('(', ')'),
            'c': ('<', '>'),
        })
        message = Mark('{}-{}_{a}~{b}', 'c')
        args = [42, Mark(42, ['a', 'b'])]
        kwargs = {
            'a': 0,
            'b': Mark(0, ['b', 'a']),
        }
        self.assertEqual(
            '<42-><[(42)]><_0~><([0])><>',
            colorizer.colorize_message(message, *args, **kwargs),
        )

    @repeat_for_values()
    def test_colorized_object_conversion(self, _, value):
        self.assertEqual(
            u'{}'.format(value),
            u'{}'.format(ColorizedObject(value)),
        )

    @repeat_for_values()
    def test_colorized_object_conversion_with_color_pair(self, _, value):
        self.assertEqual(
            u'<{}>'.format(value),
            u'{}'.format(ColorizedObject(value, color_pair=('<', '>'))),
        )

    @repeat_for_values()
    def test_colorized_object_representation(self, _, value):
        self.assertEqual(
            repr(value),
            repr(ColorizedObject(value)),
        )

    @repeat_for_values()
    def test_colorized_object_representation_with_color_pair(self, _, value):
        self.assertEqual(
            u'<{!r}>'.format(value),
            repr(ColorizedObject(value, color_pair=('<', '>'))),
        )

    @repeat_for_values({
        "integer": int,
        "float": float,
        "boolean": bool,
    })
    def test_colorized_object_cast(self, _, type_):
        self.assertEqual(
            type_(),
            type_(ColorizedObject(type_())),
        )

    @repeat_for_values({
        "integer": int,
        "float": float,
        "boolean": bool,
    })
    def test_colorized_object_cast_with_color_pair(self, _, type_):
        self.assertEqual(
            type_(),
            type_(ColorizedObject(type_(), color_pair=('<', '>'))),
        )

    def test_explicit_unicode_in_python3(self):
        if PY3:
            self.assertEqual(
                u'test',
                ColorizedObject(u'test').__unicode__(),
            )
            self.assertEqual(
                u'<test>',
                ColorizedObject(u'test', color_pair=('<', '>')).__unicode__(),
            )
