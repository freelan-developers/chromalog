"""
Test colorizers.
"""

from unittest import TestCase

from chromalog.colorizer import (
    Colorizer,
    ColorizableMixin,
)
from chromalog.important import Important as hl

from .common import repeat_for_values


class ColorizerTests(TestCase):
    @repeat_for_values()
    def test_colorizer_doesnt_change_unknown_types(self, _, value):
        colorizer = Colorizer()
        self.assertEqual(value, colorizer.colorize(value))

    @repeat_for_values()
    def test_colorizer_changes_colorizable_types(self, _, value):
        colorizer = Colorizer()
        self.assertNotEqual(value, colorizer.colorize(hl(value)))

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
        result = colorizer.colorize(hl('hello', color_tag='my_tag'))
        self.assertEqual('START_MARKhelloSTOP_MARK', result)

    def test_colorizer_colorizes_with_known_color_tag_and_default(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
                'default': ('START_DEFAULT_MARK', 'STOP_DEFAULT_MARK')
            },
            default_color_tag='default',
        )
        result = colorizer.colorize(hl('hello', color_tag='my_tag'))
        self.assertEqual('START_MARKhelloSTOP_MARK', result)

    def test_colorizer_doesnt_colorize_with_unknown_color_tag(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
            },
        )
        result = colorizer.colorize(hl('hello', color_tag='my_unknown_tag'))
        self.assertEqual('hello', str(result))

    def test_colorizer_colorizes_with_unknown_color_tag_and_default(self):
        colorizer = Colorizer(
            color_map={
                'my_tag': ('START_MARK', 'STOP_MARK'),
                'default': ('START_DEFAULT_MARK', 'STOP_DEFAULT_MARK')
            },
            default_color_tag='default',
        )
        result = colorizer.colorize(hl('hello', color_tag='my_unknown_tag'))
        self.assertEqual('START_DEFAULT_MARKhelloSTOP_DEFAULT_MARK', result)
