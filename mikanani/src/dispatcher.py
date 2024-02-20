import pika
import json
from pymongo import MongoClient
from .configs import RabbitmqConfig, MongoDBConfig

class MikanamiAnimeDispatcher:
    def sqs_dispatch(self):
        # Get expected-list in mongodb
        mongo_client = MongoClient(MongoDBConfig['host'])
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        mongo_col = mongo_db[MongoDBConfig['mikancollection']]

        query = { "isActive": True }

        data_to_send = [
            # {
            #     "name": "sousou_no_frieren",
            #     "rss_url": 'https://mikanani.me/RSS/Bangumi?bangumiId=3141&subgroupid=583',
            #     "rule_version": "latest",
            #     "rule_regex": '\[ANi\]\s+.*?\s+/\s+葬送的芙莉莲\s+-\s+(\d+)\s+\[1080P\]\[Baha\].*',
            # },
            # {
            #     "name": "dungeon_meshi",
            #     "rss_url": "https://mikanani.me/RSS/Bangumi?bangumiId=3240&subgroupid=382",
            #     "rule_version": "latest",
            #     "rule_regex": '【喵萌奶茶屋】★01月新番★\[迷宫饭 / Dungeon Meshi / Delicious in Dungeon\]\[(\d+)\]\[1080p\]\[简日双语\].*',
            # }
            x for x in mongo_col.find(query, {"_id": 0})
        ]

        credentials = pika.PlainCredentials(username=RabbitmqConfig['user'], password=RabbitmqConfig['pwd'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RabbitmqConfig['host'],
                port=RabbitmqConfig['port'],
                credentials=credentials
            )
        )

        channel = connection.channel()

        json_message = json.dumps(data_to_send, ensure_ascii=False)
        channel.basic_publish(exchange="mikanani-direct-ex",
                            routing_key="mikanani-subanime-download",
                            body=json_message)

        print(f" [x] Sent JSON message: {json_message}")


        connection.close()