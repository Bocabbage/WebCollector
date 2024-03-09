import os
import loguru

# [todo] replace the hard-code
MAIN_LOGGER = loguru.logger
MAIN_LOGGER.add(
    "./logs/mainLog.log",
    format="{time}|{level}|{message}",
    level="INFO",
)
