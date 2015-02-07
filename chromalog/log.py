"""
Log-related functions and structures.
"""

import sys
import logging

from colorama import AnsiToWin32
from contextlib import contextmanager

from .colorizer import Colorizer


class ColorizingFormatter(logging.Formatter):
    """
    A formatter that colorize its output.
    """

    def format(self, record):
        """
        Colorize the arguments of a record.

        :record: A `LogRecord` instance.
        :returns: The colorized formatted string.

        .. note:: The `record` object must have a `colorizer` attribute to be
        use for colorizing the formatted string. If no such attribute is found,
        the default non-colorized behaviour is used instead.
        """
        colorized_stream_handler = getattr(
            record,
            ColorizingStreamHandler._RECORD_ATTRIBUTE_NAME,
            None,
        )

        if colorized_stream_handler:
            colorizer = colorized_stream_handler.active_colorizer

            if colorizer:
                record.args = tuple(map(colorizer.colorize, record.args))

        return super(ColorizingFormatter, self).format(record)


class ColorizingStreamHandler(logging.StreamHandler):
    """
    A stream handler that colorize its output.
    """

    _RECORD_ATTRIBUTE_NAME = 'colorized_stream_handler'

    @staticmethod
    def stream_has_color_support(stream):
        """
        Check if a stream has color support.

        :param stream: The stream to check.
        :returns: True if stream has color support.
        """
        return getattr(stream, 'isatty', lambda: False)()

    def __init__(self, stream=None, colorizer=None, highlighter=None):
        """
        Initializes a colorizing stream handler.

        :param stream: The stream to use for output.
        :param colorizer: The colorizer to use for colorizing the output. If
            not specified, a :class:`chromalog.colorizer.Colorizer` is
            instantiated.
        :param highlighter: The colorizer to use for highlighting the output
            when color is not supported.
        """
        if not stream:
            stream = sys.stderr

        self.has_color_support = self.stream_has_color_support(stream)
        self.color_disabled = False

        if self.has_color_support:
            stream = AnsiToWin32(stream).stream

        super(ColorizingStreamHandler, self).__init__(
            stream=stream
        )
        self.colorizer = colorizer or Colorizer()
        self.highlighter = highlighter
        self.setFormatter(ColorizingFormatter())

    @property
    def active_colorizer(self):
        """
        The active colorizer or highlighter depending on whether color is
        supported.
        """
        if (
                self.has_color_support and
                not self.color_disabled and
                self.colorizer
        ):
            return self.colorizer

        return self.highlighter

    @contextmanager
    def __bind_to_record(self, record):
        setattr(record, self._RECORD_ATTRIBUTE_NAME, self)

        try:
            yield
        finally:
            delattr(record, self._RECORD_ATTRIBUTE_NAME)

    def format(self, record):
        """
        Format a `LogRecord` and prints it to the associated stream.
        """
        with self.__bind_to_record(record):
            return super(ColorizingStreamHandler, self).format(record)
