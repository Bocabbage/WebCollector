import pika
import pika
import json
from .configs import RabbitmqConfig

class MikanamiAnimeDispatcher:
    def sqs_dispatch(self):
        # [todo] enhancement: use mongodb to replace hard-coding
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
                "name": "sousou_no_frieren",
                "rss_url": 'https://mikanani.me/RSS/Bangumi?bangumiId=3141&subgroupid=583',
                "rule_version": "latest",
                "rule_regex": '\[ANi\]\s+.*?\s+/\s+葬送的芙莉莲\s+-\s+(\d+)\s+\[1080P\]\[Baha\].*',
            },
            {
                "name": "dungeon_meshi",
                "rss_url": "https://mikanani.me/RSS/Bangumi?bangumiId=3240&subgroupid=382",
                "rule_version": "latest",
                "rule_regex": '【喵萌奶茶屋】★01月新番★\[迷宫饭 / Dungeon Meshi / Delicious in Dungeon\]\[(\d+)\]\[1080p\]\[简日双语\].*',
            }
        ]
        json_message = json.dumps(data_to_send)
        channel.basic_publish(exchange="mikanani-direct-ex",
                            routing_key="mikanani-subanime-download",
                            body=json_message)

        print(f" [x] Sent JSON message: {json_message}")


        connection.close()