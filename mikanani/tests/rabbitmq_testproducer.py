import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(dirname(abspath(__file__)),'../'))

import pika
import json
from src.configs import RabbitmqConfig

credentials = pika.PlainCredentials(username=RabbitmqConfig['user'], password=RabbitmqConfig['pwd'])
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RabbitmqConfig['host'],
        port=RabbitmqConfig['port'],
        credentials=credentials
    )
)

channel = connection.channel()

data_to_send = [
    {
        "name": "kusuriya_no_hitorigoto",
        "rss_url": "https://mikanani.me/RSS/Bangumi?bangumiId=3203&subgroupid=370",
        "rule_version": "latest",
        "rule_regex": '\[喵萌奶茶屋\&LoliHouse\].*?Kusuriya no Hitorigoto - (\d+).*',
    },
    {
        "name": "16bit_no_kanto",
        "rss_url": "https://mikanani.me/RSS/Bangumi?bangumiId=3178&subgroupid=583",
        "rule_version": "latest",
        "rule_regex": '\[ANi\].*?(\d+) \[1080P\]\[Baha.*',
        
    },
    {
        "name": "hoshikuzu_telepath",
        "rss_url": "https://mikanani.me/RSS/Bangumi?bangumiId=3144&subgroupid=370",
        "rule_version": "latest",
        "rule_regex": '\[喵萌奶茶屋&LoliHouse\].*?(\d+) \[WebRip.*',
    }
]
json_message = json.dumps(data_to_send)


channel.basic_publish(exchange="mikanani-direct-ex",
                      routing_key="mikanani-subanime-download",
                      body=json_message)

print(f" [x] Sent JSON message: {json_message}")


connection.close()