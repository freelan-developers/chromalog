import logging
import chromalog

from chromalog.mark import success, error, important

chromalog.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger()

filename = r'/var/lib/status'

logger.info("Booting up system: %s", success("OK"))
logger.info("Booting up network: %s", error("FAIL"))
logger.info("Reading file at %s: %s", important(filename), success("OK"))
