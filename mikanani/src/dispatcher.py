import pika
import json
from pymongo import MongoClient
from configs import RabbitmqConfig, MongoDBConfig

class MikanamiAnimeDispatcher:
    def sqs_dispatch(self):
        # Get expected-list in mongodb
        mongo_client = MongoClient(MongoDBConfig['host'])
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        mongo_col = mongo_db[MongoDBConfig['mikancollection']]

        query = { "isActive": True }

        data_to_send = [
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