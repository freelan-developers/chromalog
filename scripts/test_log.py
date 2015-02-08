"""
Test logging.
"""

import logging

from chromalog import basicConfig
from chromalog.important import Important as hl

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
        getattr(logger, level)('This is a %s !', hl(level))
