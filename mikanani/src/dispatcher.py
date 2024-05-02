import json
import pika
from bson.int64 import Int64
from db_helper import get_mongo_client, get_mysql_conn
from configs import RabbitmqConfig, MongoDBConfig
from logger import LOGGER

class MikanamiAnimeDispatcher:
    r'''
        Cronjob dispatch to query active-anime subscribes
        and tell worker to check-and-download
    '''
    def sqs_dispatch(self):
        # Get active-anime uid list from MySQL
        uid_list = list()
        conn = get_mysql_conn()
        sql = "SELECT uid FROM `mikanani`.`anime_meta` WHERE is_active IS TRUE;"
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            uid_list = [x[0] for x in result]
            uid_list = [Int64(uid) for uid in uid_list]
        # LOGGER.info(f"[UID-list]: {uid_list}")
        
        # Get related doc from Mongo
        mongo_client = get_mongo_client()
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        mongo_col = mongo_db[MongoDBConfig['mikancollection']]

        query = { "uid": {"$in": uid_list} }

        data_to_send = [
            x for x in mongo_col.find(query, {"_id": 0})
        ]

        # Rabbitmq client init
        credentials = pika.PlainCredentials(username=RabbitmqConfig['user'], password=RabbitmqConfig['pwd'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RabbitmqConfig['host'],
                port=RabbitmqConfig['port'],
                credentials=credentials
            )
        )

        # Send task to queue
        channel = connection.channel()
        # If not exist, create queue/exchange/router-key
        # Queue def
        channel.queue_declare(queue="mikanani_dispatch", durable=True)
        # Exchange def
        channel.exchange_declare("mikanani-direct-ex", "direct", durable=True)
        # Exchange-Queue bind
        routing_key = "mikanani-subanime-download"
        channel.queue_bind(queue="mikanani_dispatch", exchange="mikanani-direct-ex", routing_key=routing_key)

        json_message = json.dumps(data_to_send, ensure_ascii=False)
        channel.basic_publish(
            exchange="mikanani-direct-ex",
            routing_key="mikanani-subanime-download",
            body=json_message
        )

        LOGGER.info(f" [x] Sent JSON message: {json_message}")
        connection.close()
