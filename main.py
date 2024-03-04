import sys
import signal
import asyncio
import argparse
from typing import List
from mikanani.src import configs
from mikanani.src.worker import MikanamiAnimeSubWorker, MongoDBOpsWorker
from mikanani.src.dispatcher import MikanamiAnimeDispatcher
from common.logger import MAIN_LOGGER as mlogger

def signal_handler(tasks: List[asyncio.Task], sig, frame):
    # [Attention] 
    # Don't use the try-catch KeyboardInterrupt method to cancel the task
    # because the inner logic of aio_pika will probably catch it
    # and then cause problem-crash.
    mlogger.info(f"Received signal {sig}, cancel tasks")
    for task in tasks:
        task.cancel()
        mlogger.info(f"task {task} cancelled.")
    mlogger.info("all tasks cancelled.")

async def _mikanani_async_main():
    try:
        tasks = [
            # [debug] temporarily shutdown sqs_worker
            # MikanamiAnimeSubWorker().sqs_async_run(), # mikanani-parse-and-send worker
            MongoDBOpsWorker().grpc_server(),         # mongodb-crud grpc server
        ]
        tasks = [ asyncio.create_task(x) for x in tasks ]

        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(tasks, sig, frame))
        mlogger.info("mikanani sqs_async_run: start")
        await asyncio.gather(*tasks)
    except Exception as e:
        mlogger.info(f"Exception {e} happened.")
    finally:
        mlogger.debug(f"Mikanani worker: stopped.")


def mikanani_main(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="direct")
    args = parser.parse_args(args)
    
    if args.mode == "direct":
        MikanamiAnimeSubWorker().run()
    elif args.mode == "sqs-worker":
        asyncio.run(_mikanani_async_main())
    elif args.mode == "sqs-dispatch":
        MikanamiAnimeDispatcher().sqs_dispatch()


if __name__ == '__main__':
    mlogger.info(f"mikanani env load test: test-env-log={configs.TestConfig}")
    args = sys.argv[1:]
    if args[0] == 'mikanani':
        mikanani_main(args[1:])
