import json
import asyncio
from typing import List
import traceback
import aio_pika
from configs import RabbitmqConfig
from job import RSSJob
from logger import LOGGER

class MikanamiAnimeSubWorker:
    r'''
        Anime subscription worker:
        (1) Listen rabbitmq sqs task
        (2) Request & parse rss subscription xmls
        (3) Collect all need-to-download torrents and send to Qbittorrent service
    '''
    def __init__(self):
        self.job_obj = RSSJob()
 
    async def _sqs_consume_callback(self, message: aio_pika.IncomingMessage):
        # Parse task read from sqs
        msg_dict_list: List[dict] = json.loads(message.body)
        for entry in msg_dict_list:
            uid = entry.get("uid")
            tlist: List[str] = list()
            if uid:
                try:
                    # Get & parse rss xml to gather torrents for each anime
                    tlist = self.job_obj.get_torrent_urls(entry)
                except Exception as e:
                    LOGGER.error(f"[get_torrent_urls][uid: {uid}]Error: exception-{e}, {traceback.format_exc()}")
                    # await message.reject()
                    continue
            # await message.ack()

            # Send task to qbittorrent service
            self.job_obj.send_task_to_qbit({ "uid": uid, "tlist": tlist })
    
            
    async def sqs_async_run(self):
        try:
            sqs_user = RabbitmqConfig["user"]
            sqs_pwd = RabbitmqConfig["pwd"]
            sqs_server = RabbitmqConfig["host"]
            sqs_port = RabbitmqConfig["port"]
            queue_name = RabbitmqConfig["queue"]
            
            connection_url = f"amqp://{sqs_user}:{sqs_pwd}@{sqs_server}:{sqs_port}/"
            connection = await aio_pika.connect(connection_url)        
            channel = await connection.channel()
    
            queue = await channel.get_queue(queue_name)
            await queue.consume(self._sqs_consume_callback, no_ack=True)

            LOGGER.info("Start rabbitmq serve: press Ctrl+c to stop.")
            await asyncio.Future()

        except asyncio.CancelledError:
            LOGGER.info("sqs_async_func() has been cancelled.")
            await channel.close()
            await connection.close()
            LOGGER.info("rabbitmq channel/conn closed.")
            # raise
