"""
Test colorizers.
"""
from builtins import str

from unittest import TestCase

from chromalog.colorizer import (
    ColorizedObject,
    Colorizer,
    ColorizableMixin,
)
from chromalog.mark import Mark

from .common import repeat_for_values


class ColorizerTests(TestCase):
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
            colorizer.colorize(Mark(value, 'a'), 'b'),
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
            colorizer.colorize(Mark(value, ['a', 'b']), 'c'),
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
