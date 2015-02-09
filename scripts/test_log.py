"""
Test logging.
"""

import logging

from chromalog import basicConfig
from chromalog.mark import (
    Mark,
    success,
    error,
)

if __name__ == '__main__':
    basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    for level in [
            'debug',
            'info',
            'warning',
            'error',
            'critical',
    ]:
        getattr(logger, level)('This is a log of level %s !', Mark(level, 'important'))
        getattr(logger, level)('This is a %s and a %s !', success('success'), error('error'))
