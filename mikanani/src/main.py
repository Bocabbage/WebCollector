import sys
import signal
import asyncio
import argparse
from typing import List
from worker import MikanamiAnimeSubWorker, MiakananigRPCSvcWorker
from dispatcher import MikanamiAnimeDispatcher
from logger import LOGGER

def signal_handler(tasks: List[asyncio.Task], sig, frame):
    # [Attention] 
    # Don't use the try-catch KeyboardInterrupt method to cancel the task
    # because the inner logic of aio_pika will probably catch it
    # and then cause problem-crash.
    LOGGER.info(f"Received signal {sig}, cancel tasks")
    for task in tasks:
        task.cancel()
        LOGGER.info(f"task {task} cancelled.")
    LOGGER.info("all tasks cancelled.")

async def _mikanani_async_main():
    try:
        tasks = [
            MikanamiAnimeSubWorker().sqs_async_run(), # mikanani-parse-and-send worker
            MiakananigRPCSvcWorker().grpc_server(),         # mongodb-crud grpc server
        ]
        tasks = [ asyncio.create_task(x) for x in tasks ]

        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(tasks, sig, frame))
        LOGGER.info("mikanani sqs_async_run: start")
        await asyncio.gather(*tasks)
    except Exception as e:
        LOGGER.info(f"Exception {e} happened.")
    finally:
        LOGGER.debug(f"Mikanani worker: stopped.")


def mikanani_main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="direct")
    args = parser.parse_args(args)
    
    if args.mode == "sqs-worker":
        asyncio.run(_mikanani_async_main())
    elif args.mode == "sqs-dispatch":
        MikanamiAnimeDispatcher().sqs_dispatch()
