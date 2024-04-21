import os
import json
import asyncio
import aio_pika
import traceback
import grpc
import grpc_service
import mikanani_grpc_pb2_grpc
from typing import Optional, List
from configs import RabbitmqConfig, gRPCServerConfig
from job import RSSJob
from logger import LOGGER

class MikanamiAnimeSubWorker:
    def __init__(self):
        config_path = f"{os.path.dirname(os.path.abspath(__file__))}/../config/media"
        self.job_obj: RSSJob = RSSJob(config_path)
 
    async def _sqs_consume_callback(self, message: aio_pika.IncomingMessage):
        msg_dict_list: List[dict] = json.loads(message.body)
        for entry in msg_dict_list:
            tlist: List[str] = list()
            try:
                uid = entry.get("uid")
                if uid:
                    tlist = self.job_obj.get_torrent_urls(entry)
                    LOGGER.info(f"get_torrent_urls success, tlist: {tlist}.")
                else:
                    LOGGER.warning(f"empty uid for {entry}, ignored.")
                    continue
            except Exception as e:
                LOGGER.error(f"get_torrent_urls error: exception-{e}, {traceback.format_exc()}")
                # await message.reject()
                continue
            # await message.ack()
            
            try:
                self.job_obj.send_task_to_qbit({
                    "uid": uid, "tlist": tlist
                })
                LOGGER.info(f"send_task_to_qbit success.")
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

            
class MiakananigRPCSvcWorker:
    def __init__(self):
        self.listen_addr = gRPCServerConfig["listenAddr"]

    async def grpc_server(self):
        try:
            server = grpc.aio.server()
            mikanani_grpc_pb2_grpc.add_MikananiServiceServicer_to_server(
                grpc_service.MikananiSvcServicer(),
                server,
            )
            server.add_insecure_port(self.listen_addr)
            LOGGER.info(f"mikanani grpc server: start serve at {self.listen_addr}")
            await server.start()
            await server.wait_for_termination()
        except Exception:
            # TODO: enhance graceful cancel
            LOGGER.info("mikanani grpc server has been cancelled.")
            await server.stop(None)