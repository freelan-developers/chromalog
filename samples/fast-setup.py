import logging
import chromalog

chromalog.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
