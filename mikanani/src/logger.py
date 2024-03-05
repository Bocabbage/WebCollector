import os
import loguru
from configs import LogConfig

os.makedirs(LogConfig['log_dir'], exist_ok=True)
LOGGER = loguru.logger
LOGGER.add(
    os.path.join(LogConfig['log_dir'], "mikanani.log"),
    format="{time}|{level}|{message}",
    level=LogConfig['log_level'],
)
