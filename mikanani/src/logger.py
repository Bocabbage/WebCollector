import os
import loguru
from configs import LogConfig

os.makedirs(LogConfig['log_dir'], exist_ok=True)
LOGGER = loguru.logger
LOGGER.add(
    LogConfig['log_dir'],
    format="{time}|{level}|{message}",
    level=LogConfig['log_dir'],
)
