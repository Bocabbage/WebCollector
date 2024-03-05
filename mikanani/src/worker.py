import os
import json
import asyncio
import aio_pika
import traceback
import grpc
import mongodb_crud
from grpc_utils import mongodb_crud_pb2_grpc
from typing import Optional, List
from configs import RabbitmqConfig, gRPCServerConfig
from job import RSSJob
from logger import LOGGER

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
    
    async def _sqs_consume_callback(self, message: aio_pika.IncomingMessage):
        tlist: List[str] = list()
        try:
            msg_dict: Optional[dict] = json.loads(message.body)
            # LOGGER.debug(f"msg_dict: {msg_dict}")
            tlist = self.job_obj.get_torrent_urls(msg_dict)
            LOGGER.info("get_torrent_urls success.")
        except Exception as e:
            LOGGER.error(f"get_torrent_urls error: exception-{e}, {traceback.format_exc()}")
            # await message.reject()
            tlist = list()
            
        # await message.ack()
        
        try:
            expected_sources = self.job_obj.send_task_to_qbit(tlist)
            LOGGER.info(f"send_task_to_qbit success, new files number: {len(expected_sources)}.")
        except Exception as e:
            LOGGER.error(f"send_task_to_qbit error: exception-{e}, {traceback.format_exc()}")
    
            
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


class MongoDBOpsWorker:
    def __init__(self):
        self.listen_addr = gRPCServerConfig["listenAddr"]

    async def grpc_server(self):
        try:
            server = grpc.aio.server()
            mongodb_crud_pb2_grpc.add_MikananiMongoCrudServicer_to_server(
                mongodb_crud.MikananiMongoDBCrud(),
                server,
            )
            server.add_insecure_port(self.listen_addr)
            LOGGER.info(f"mongodb grpc server: start serve at {self.listen_addr}")
            await server.start()
            await server.wait_for_termination()
        except Exception:
            # TODO: enhance graceful cancel
            LOGGER.info("mongodb grpc server has been cancelled.")
            await server.stop(None)