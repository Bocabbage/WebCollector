import sys
import asyncio
import argparse
from typing import List
from mikanani.src.worker import MikanamiAnimeSubWorker
from .common.logger import MAIN_LOGGER as mlogger


def mikanani_main(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="direct")
    args = parser.parse_args(args)
    
    if args.mode == "direct":
        MikanamiAnimeSubWorker().run()
    elif args.mode == "sqs":
        mlogger.info("mikanani sqs_async_run: start")
        asyncio.run(MikanamiAnimeSubWorker().sqs_async_run())


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'mikanani':
        mikanani_main(args[1:])
