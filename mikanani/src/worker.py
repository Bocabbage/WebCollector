import os
import aio_pika
import traceback
from .configs import RabbitmqConfig
from .job import RSSJob
from .logger import LOGGER

class MikanamiAnimeSubWorker:
    def __init__(self):
        config_path = f"{os.path.dirname(os.path.abspath(__file__))}/../config/media"
        self.job_obj: RSSJob = RSSJob(config_path)
    
    def run(self):
        try:
            tlist = self.job_obj.get_torrent_urls()
            LOGGER.info("get_torrent_urls success.")
        except Exception as e:
            LOGGER.error(f"get_torrent_urls error: exception-{e}, {traceback.format_exc()}")
        
        try:
            expected_sources = self.job_obj.send_task_to_qbit(tlist)
            LOGGER.info(f"send_task_to_qbit success, new files number: {len(expected_sources)}.")
        except Exception as e:
            LOGGER.error(f"send_task_to_qbit error: exception-{e}, {traceback.format_exc()}")
    
    async def _sqs_consume_callback(message: aio_pika.IncomingMessage):
        pass
    
    async def _sqs_consume(self):
        sqs_user = RabbitmqConfig["user"]
        sqs_pwd = RabbitmqConfig["pwd"]
        sqs_server = RabbitmqConfig["host"]
        sqs_port = RabbitmqConfig["port"]
        queue_name = RabbitmqConfig["queue"]
        
        connection_url = f"amqp:{sqs_user}:{sqs_pwd}@{sqs_server}:{sqs_port}/"
        connection = await aio_pika.connect_robust(connection_url)        
        channel = await connection.channel()
 
        queue = await channel.get_queue(queue_name)
        # set callback
        await queue.consume(self._sqs_consume_callback)
            
    async def sqs_async_run(self):
        await self._sqs_consume()
        
