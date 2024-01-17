"""Constants & Definitions."""
import logging

BASE_URL = "https://bridge.simplefin.org/simplefin"
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
