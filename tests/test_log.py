"""
Test colorized logging structures.
"""
import sys
import logging

from unittest import TestCase
from logging import (
    LogRecord,
    DEBUG,
)
from mock import (
    MagicMock,
    patch,
)
from six import StringIO

from chromalog import basicConfig
from chromalog.colorizer import GenericColorizer
from chromalog.mark import Mark
from chromalog.log import (
    ColorizingFormatter,
    ColorizingStreamHandler,
)


class LogTests(TestCase):
    def create_colorizer(self, format):
        def colorize(obj, context_color_tag=None):
            return format % obj

        result = MagicMock(spec=GenericColorizer)
        result.colorize = MagicMock(side_effect=colorize)

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

    def test_colorizing_formatter_without_a_colorizer_mapping(self):
        formatter = ColorizingFormatter(fmt='%(message)s')
        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%(summand1)d + %(summand2)d gives %(sum)d',
            args=({'summand1': 4, 'summand2': 5, 'sum': 4 + 5},),
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
            self.create_colorizer(format='[%s]'),
        )

        self.assertEqual('[4] + [5] gives [9]', formatter.format(record))

        colorizer = getattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        )
        colorizer.colorize.assert_any_call(4, context_color_tag=None)
        colorizer.colorize.assert_any_call(5, context_color_tag=None)
        colorizer.colorize.assert_any_call(9, context_color_tag=None)

    def test_colorizing_formatter_with_a_colorizer_mapping(self):
        formatter = ColorizingFormatter(fmt='%(message)s')
        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%(summand1)s + %(summand2)s gives %(sum)s',
            args=({'summand1': 4, 'summand2': 5, 'sum': 4 + 5},),
            exc_info=None,
        )
        setattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
            self.create_colorizer(format='[%s]'),
        )

        self.assertEqual('[4] + [5] gives [9]', formatter.format(record))

        colorizer = getattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        )
        colorizer.colorize.assert_any_call(4, context_color_tag=None)
        colorizer.colorize.assert_any_call(5, context_color_tag=None)
        colorizer.colorize.assert_any_call(9, context_color_tag=None)

    @patch('sys.stderr', spec=sys.stderr)
    def test_csh_uses_stderr_as_default(self, stream):
        stream.isatty = lambda: False
        handler = ColorizingStreamHandler()
        self.assertEqual(stream, handler.stream)

    def test_csh_uses_streamwrapper(self):
        stream = StringIO()

        with patch(
            'chromalog.log.stream_has_color_support',
            return_value=True,
        ):
            handler = ColorizingStreamHandler(stream=stream)

        self.assertIsNot(handler.stream, stream)

    def test_csh_dont_uses_streamwrapper_if_no_color(self):
        stream = StringIO()
        handler = ColorizingStreamHandler(stream=stream)
        self.assertIs(handler.stream, stream)

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
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives [9]', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))

    def test_csh_format_with_context(self):
        colorizer = GenericColorizer(color_map={
            'bracket': ('[', ']'),
            'context': ('{', '}'),
        })
        highlighter = GenericColorizer(color_map={
            'bracket': ('<', '>'),
            'context': ('(', ')'),
        })
        formatter = ColorizingFormatter(fmt='%(levelname)s %(message)s')
        color_stream = MagicMock()
        color_stream.isatty = lambda: True
        handler = ColorizingStreamHandler(
            stream=color_stream,
            colorizer=colorizer,
            highlighter=highlighter,
            attributes_map={
                'message': 'context',
                'levelname': 'bracket',
            },
        )
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual(
            '[DEBUG] {4 + 5 gives }{[9]}{}',
            handler.format(record),
        )

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
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
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
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
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
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives 9', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(record, 'colorizer'))

    def test_csh_format_disabled_color_support(self):
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
        handler.color_disabled = True
        handler.setFormatter(formatter)

        record = LogRecord(
            name='my_record',
            level=DEBUG,
            pathname='my_path',
            lineno=42,
            msg='%s + %s gives %s',
            args=(4, 5, Mark(4 + 5, color_tag='bracket'),),
            exc_info=None,
        )

        self.assertEqual('4 + 5 gives <9>', handler.format(record))

        # Make sure that the colorizer attribute was removed after processing.
        self.assertFalse(hasattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
        ))

    def test_basic_config_add_a_stream_handler(self):
        logger = logging.Logger('test')

        self.assertEqual([], logger.handlers)

        with patch('logging.getLogger', new=lambda: logger):
            basicConfig()
            self.assertEqual(1, len(logger.handlers))

    def test_basic_config_sets_level(self):
        logger = logging.Logger('test')

        with patch('logging.getLogger', new=lambda: logger):
            basicConfig(level=logging.DEBUG)
            self.assertEqual(logging.DEBUG, logger.level)

    def test_basic_config_sets_format(self):
        logger = logging.Logger('test')

        with patch('logging.getLogger', new=lambda: logger):
            basicConfig(format='my format')
            self.assertEqual('my format', logger.handlers[0].formatter._fmt)
