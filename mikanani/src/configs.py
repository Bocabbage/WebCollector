import os
from typing import Dict, Optional

TestConfig: str = os.getenv('TESTCONFIG')

LogConfig: Dict[str, Optional[str]] = {
    'log_dir': os.getenv('LOG_DIR', './logs'),
    'log_level': os.getenv('LOG_LEVEL', 'DEBUG'),
}

RSSConfig: Dict[str, str] = {
    'config_dir': os.getenv('CONFIG_DIR'),
}

QbitConfig: Dict[str, str] = {
    'qbit_addr': os.getenv('QBIT_ADDR'),
    'qbit_port': os.getenv('QBIT_PORT', 8080),
    'torrent_file_dir': os.getenv('TORRENT_FILE_DIR', './'),
    'media_file_dir': os.getenv('MEDIA_FILE_DIR', './'),
    'nfs_media_file_dir': os.getenv('NFS_MEDIA_FILE_DIR'),
    'username': os.getenv('QBIT_USER'),
    'password': os.getenv('QBIT_PWD'),
}

ProxyConfig: dict = {
    'proxy_enable': False if os.getenv('PROXY_ENABLE', "False") == "False" else True,
    'proxy_addr': os.getenv('PROXY_ADDR'),
    'proxy_port': os.getenv('PROXY_PORT'),
}

RabbitmqConfig: dict = {
    'host': os.getenv('KAPIBARA_RABBITMQ_SVC_SERVICE_HOST', os.getenv('RABBITMQ_HOST_MKANI')),
    'port': os.getenv('KAPIBARA_RABBITMQ_SVC_SERVICE_PORT', os.getenv('RABBITMQ_PORT_MKANI')),
    'user': os.getenv('RABBITMQ_USER_MKANI'),
    'pwd': os.getenv('RABBITMQ_PWD_MKANI'),
    'queue': os.getenv('RABBITMQ_QUEUENAME_MKANI'),
    'routing_key': os.getenv('RABBITMQ_ROUTING_KEY'),
}

MongoDBConfig: dict = {
    'host': os.getenv('KAPIBARA_MONGODB_SVC_URL'),
    'mikandb': os.getenv('KAPIBARA_MONGODB_MIKANDB'),
    'mikancollection': os.getenv('KAPIBARA_MONGODB_MIKANCOLLECTION'),
}

MySQLConfig: dict = {
    'host': os.getenv('MIKANANI_MYSQL_HOST'),
    'user': os.getenv('MIKANANI_MYSQL_USER'),
    'password': os.getenv('MIKANANI_MYSQL_PWD'),
    'database': 'mikanani',
}

gRPCServerConfig: dict = {
    'listenAddr': '[::]:50051',
}