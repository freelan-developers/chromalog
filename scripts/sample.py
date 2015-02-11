"""
A sample using chromalog.
"""

import logging

from chromalog.log import (
    ColorizingStreamHandler,
    ColorizingFormatter,
)

from chromalog.mark import (
    important,
    success,
    error,
)

formatter = ColorizingFormatter('[%(levelname)s] %(message)s')

handler = ColorizingStreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info("This is a regular info log message.")
logger.info(
    "Trying to read user information from %s using a json parser.",
    important(r'/usr/local/mylib/user-info.json'),
)
logger.warning(
    "Unable to read the file at %s ! Something is wrong.",
    important(r'/usr/local/mylib/user-info.json'),
)
logger.error("Something went really wrong !")
logger.info(
    "This is a %s and this is an %s.",
    success("success"),
    error("error"),
)
logger.info(
    "You can combine %s and %s to get an %s !",
    success("success"),
    important("important"),
    important(success("important-success")),
)
