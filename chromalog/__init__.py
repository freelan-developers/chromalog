"""
Enhance Python logging with colors.
"""

import logging

from .log import (
    ColorizingFormatter,
    ColorizingStreamHandler,
)


def basicConfig(
    format=None,
    datefmt=None,
    level=None,
    stream=None,
    colorizer=None,
):
    """
    Does basic configuration for the logging system by creating a
    :class:`chromalog.log.ColorizingStreamHandler` with a default
    :class:`chromalog.log.ColorizingFormatter` and adding it to the root
    logger.

    This function does nothing if the root logger already has handlers
    configured for it.

    :param format: The format to be passed to the formatter.
    :param datefmt: The date format to be passed to the formatter.
    :param level: Set the root logger to the specified level.
    :param stream: Use the specified stream to initialize the stream handler.
    :param colorizer: Set the colorizer to be passed to the stream handler.
    """
    logger = logging.getLogger()

    if not logger.handlers:
        if format is None:
            format = '%(levelname)s:%(name)s:%(message)s'

        formatter = ColorizingFormatter(fmt=format, datefmt=datefmt)
        handler = ColorizingStreamHandler(stream=stream, colorizer=colorizer)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if level:
            logger.setLevel(level)
