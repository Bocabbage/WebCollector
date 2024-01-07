import os
from typing import Dict, Optional

LogConfig: Dict[str, Optional[str]] = {
    'log_dir': os.getenv('LOG_DIR', './logs'),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
}

RSSConfig: Dict[str, str] = {
    'config_dir': os.getenv('CONFIG_DIR'),
}

QbitConfig: Dict[str, str] = {
    'qbit_addr': os.getenv('QBIT_ADDR'),
    'torrent_file_dir': os.getenv('TORRENT_FILE_DIR', './'),
    'media_file_dir': os.getenv('MEDIA_FILE_DIR', './'),
    'username': os.getenv('QBIT_USER'),
    'password': os.getenv('QBIT_PWD'),
}

ProxyConfig: dict = {
    'proxy_enable': False if os.getenv('PROXY_ENABLE', "False") == "False" else True,
    'proxy_addr': os.getenv('PROXY_ADDR'),
}

RabbitmqConfig: dict = {
    'host': os.getenv('RABBITMQ_HOST_MKANI'),
    'port': os.getenv('RABBITMQ_PORT_MKANI'),
    'user': os.getenv('RABBITMQ_USER_MKANI'),
    'pwd': os.getenv('RABBITMQ_PWD_MKANI'),
    'queue': os.getenv('RABBITMQ_QUEUENAME_MKANI')
}