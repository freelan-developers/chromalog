"""
Stream tests.
"""

from unittest import TestCase

from mock import MagicMock

from chromalog.stream import stream_has_color_support


class StreamTests(TestCase):
    def test_csh_color_support_with_color_stream(self):
        color_stream = MagicMock(spec=object)
        color_stream.isatty = lambda: True
        self.assertTrue(stream_has_color_support(
            color_stream
        ))

    def test_csh_color_support_with_no_color_stream(self):
        no_color_stream = MagicMock(spec=object)
        no_color_stream.isatty = lambda: False
        self.assertFalse(
            stream_has_color_support(no_color_stream),
        )

    def test_csh_color_support_with_simple_stream(self):
        simple_stream = MagicMock(spec=object)
        self.assertFalse(
            stream_has_color_support(simple_stream),
        )
