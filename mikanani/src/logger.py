import loguru
from configs import LOG_FILE

LOGGER = loguru.logger
LOGGER.add(
    LOG_FILE,
    format="{time}|{level}|{message}",
    level="INFO",
)
