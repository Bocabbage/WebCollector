import pika
import json
from bson.int64 import Int64
from db_helper import get_mongo_client, get_mysql_conn
from configs import RabbitmqConfig, MongoDBConfig
from logger import LOGGER

class MikanamiAnimeDispatcher:
    def sqs_dispatch(self):
        # Get expected-list in mongodb
        uid_list = list()
        conn = get_mysql_conn()
        sql = f"SELECT uid FROM `mikanani`.`anime_meta` WHERE is_active IS TRUE;"
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            uid_list = [x[0] for x in result]
            uid_list = [Int64(uid) for uid in uid_list]
        LOGGER.info(f"get uid list from meta-db: {uid_list}")
        
        mongo_client = get_mongo_client()
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        mongo_col = mongo_db[MongoDBConfig['mikancollection']]

        query = { "uid": {"$in": uid_list} }

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