"""
Test colorized logging structures.
"""
import sys

from unittest import TestCase
from logging import (
    LogRecord,
    DEBUG,
)
from mock import (
    MagicMock,
    patch,
)

from chromalog.colorizer import GenericColorizer
from chromalog.important import Important as hl
from chromalog.log import (
    ColorizingFormatter,
    ColorizingStreamHandler,
)


class LogTests(TestCase):
    def create_colorizer_stream_handler(self, format):
        result = MagicMock(spec=ColorizingStreamHandler)
        result.active_colorizer = MagicMock(spec=GenericColorizer)
        result.active_colorizer.colorize = MagicMock(
            side_effect=lambda x: format % x,
        )
        return result

    def test_colorizing_formatter_without_a_colorizer(self):
        formatter = ColorizingFormatter(fmt='%(message)s')
        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%d + %d gives %d',
            args=(4, 5, 4 + 5,),
            exc_info=None,
        )
        self.assertEqual('4 + 5 gives 9', formatter.format(record))

    def test_colorizing_formatter_with_a_colorizer(self):
        formatter = ColorizingFormatter(fmt='%(message)s')
        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, 4 + 5,),
            exc_info=None,
        )
        setattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
            self.create_colorizer_stream_handler(format='[%s]'),
        )

        self.assertEqual('[4] + [5] gives [9]', formatter.format(record))

        handler = getattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        )
        handler.active_colorizer.colorize.assert_any_call(4)
        handler.active_colorizer.colorize.assert_any_call(5)
        handler.active_colorizer.colorize.assert_any_call(9)

    def test_csh_color_support_with_color_stream(self):
        color_stream = MagicMock(spec=object)
        color_stream.isatty = lambda: True
        self.assertTrue(ColorizingStreamHandler.stream_has_color_support(
            color_stream
        ))

    def test_csh_color_support_with_no_color_stream(self):
        no_color_stream = MagicMock(spec=object)
        no_color_stream.isatty = lambda: False
        self.assertFalse(
            ColorizingStreamHandler.stream_has_color_support(no_color_stream),
        )

    def test_csh_color_support_with_simple_stream(self):
        simple_stream = MagicMock(spec=object)
        self.assertFalse(
            ColorizingStreamHandler.stream_has_color_support(simple_stream),
        )

    @patch('sys.stderr', spec=sys.stderr)
    def test_csh_uses_stderr_as_default(self, stream):
        stream.isatty = lambda: False
        handler = ColorizingStreamHandler()
        self.assertEqual(stream, handler.stream)

    @patch('colorama.ansitowin32.StreamWrapper')
    def test_csh_uses_streamwrapper(
        self,
        proxy,
    ):
        ColorizingStreamHandler()
        proxy.assert_called_once()

    @patch('colorama.ansitowin32.StreamWrapper')
    def test_csh_dont_uses_streamwrapper_if_no_color(
        self,
        proxy,
    ):
        ColorizingStreamHandler(stream=MagicMock(spec=object))
        self.assertFalse(proxy.called)

    def test_csh_format(self):
        colorizer = GenericColorizer(color_map={
            'bracket': ('[', ']'),
        })
        highlighter = GenericColorizer(color_map={
            'bracket': ('<', '>'),
        })
        formatter = ColorizingFormatter(fmt='%(message)s')
        color_stream = MagicMock()
        color_stream.isatty = lambda: True
        handler = ColorizingStreamHandler(
            stream=color_stream,
            colorizer=colorizer,
            highlighter=highlighter,
        )
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, hl(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives [9]', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))

    def test_csh_format_no_color_support(self):
        colorizer = GenericColorizer(color_map={
            'bracket': ('[', ']'),
        })
        highlighter = GenericColorizer(color_map={
            'bracket': ('<', '>'),
        })
        formatter = ColorizingFormatter(fmt='%(message)s')
        no_color_stream = MagicMock()
        no_color_stream.isatty = lambda: False
        handler = ColorizingStreamHandler(
            stream=no_color_stream,
            colorizer=colorizer,
            highlighter=highlighter,
        )
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, hl(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives <9>', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))

    def test_csh_format_no_highlighter(self):
        colorizer = GenericColorizer(color_map={
            'bracket': ('[', ']'),
        })
        formatter = ColorizingFormatter(fmt='%(message)s')
        color_stream = MagicMock()
        color_stream.isatty = lambda: True
        handler = ColorizingStreamHandler(
            stream=color_stream,
            colorizer=colorizer,
        )
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, hl(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives [9]', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))

    def test_csh_format_no_highlighter_no_color_support(self):
        colorizer = GenericColorizer(color_map={
            'bracket': ('[', ']'),
        })
        formatter = ColorizingFormatter(fmt='%(message)s')
        color_stream = MagicMock()
        color_stream.isatty = lambda: False
        handler = ColorizingStreamHandler(
            stream=color_stream,
            colorizer=colorizer,
        )
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, hl(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives 9', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))
