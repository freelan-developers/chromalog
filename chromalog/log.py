"""
Log-related functions and structures.
"""
from builtins import map

import sys
import logging

from colorama import AnsiToWin32
from functools import partial
from contextlib import contextmanager

from .colorizer import Colorizer
from .mark.objects import Mark
from .stream import stream_has_color_support


class ColorizingFormatter(logging.Formatter):
    """
    A formatter that colorize its output.
    """

    @contextmanager
    def _patch_record(self, record, colorizer, message_color_tag):
        save_dict = record.__dict__.copy()

        if colorizer:
            record.args = tuple(map(
                partial(
                    colorizer.colorize,
                    context_color_tag=message_color_tag,
                ),
                record.args,
            ))
            record.filename = colorizer.colorize(record.filename)
            record.funcName = colorizer.colorize(record.funcName)
            record.levelname = colorizer.colorize(record.levelname)
            record.module = colorizer.colorize(record.module)
            record.name = colorizer.colorize(record.name)
            record.pathname = colorizer.colorize(record.pathname)
            record.processName = colorizer.colorize(record.processName)
            record.threadName = colorizer.colorize(record.threadName)

            if message_color_tag:
                message = colorizer.colorize(Mark(
                    record.getMessage(),
                    color_tag=message_color_tag,
                ))
                record.getMessage = lambda: message

        try:
            yield
        finally:
            record.__dict__ = save_dict

    def format(self, record):
        """
        Colorize the arguments of a record.

        :record: A `LogRecord` instance.
        :returns: The colorized formatted string.

        .. note:: The `record` object must have a `colorizer` attribute to be
            use for colorizing the formatted string. If no such attribute is
            found, the default non-colorized behaviour is used instead.
        """
        colorizer = getattr(record, 'colorizer', None)
        message_color_tag = getattr(record, 'message_color_tag', None)

        with self._patch_record(record, colorizer, message_color_tag):
            return super(ColorizingFormatter, self).format(record)


class ColorizingStreamHandler(logging.StreamHandler):
    """
    A stream handler that colorize its output.
    """

    _RECORD_ATTRIBUTE_NAME = 'colorizer'
    default_attributes_map = {
        'name': 'important',
        'levelname': lambda record: str(record.levelname).lower(),
        'message': lambda record: str(record.levelname).lower(),
    }

    def __init__(
        self,
        stream=None,
        colorizer=None,
        highlighter=None,
        attributes_map=None,
    ):
        """
        Initializes a colorizing stream handler.

        :param stream: The stream to use for output.
        :param colorizer: The colorizer to use for colorizing the output. If
            not specified, a :class:`chromalog.colorizer.Colorizer` is
            instantiated.
        :param highlighter: The colorizer to use for highlighting the output
            when color is not supported.
        :param attributes_map: A map of LogRecord attributes/color tags.
        """
        if not stream:
            stream = sys.stderr

        self.has_color_support = stream_has_color_support(stream)
        self.color_disabled = False
        self.attributes_map = attributes_map or self.default_attributes_map

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
        setattr(record, self._RECORD_ATTRIBUTE_NAME, self.active_colorizer)

        try:
            yield
        finally:
            delattr(record, self._RECORD_ATTRIBUTE_NAME)

    def _color_tag_from_record(self, color_tag, record):
        if hasattr(color_tag, '__call__'):
            return color_tag(record)
        else:
            return color_tag.format(**record.__dict__)

    def format(self, record):
        """
        Format a `LogRecord` and prints it to the associated stream.
        """
        with self.__bind_to_record(record):
            for attribute, color_tag in self.attributes_map.items():
                if attribute == 'message':
                    record.message_color_tag = self._color_tag_from_record(
                        color_tag,
                        record,
                    )
                else:
                    setattr(record, attribute, Mark(
                        getattr(record, attribute),
                        color_tag=self._color_tag_from_record(
                            color_tag,
                            record,
                        ),
                    ))

            return super(ColorizingStreamHandler, self).format(record)
