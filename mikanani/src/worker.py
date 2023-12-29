import os
import traceback
from job import RSSJob
from logger import LOGGER

class MikanamiAnimeSubWorker:
    def __init__(self):
        config_path = f"{os.path.abspath(__file__)}/../config"
        self.job_obj: RSSJob = RSSJob(config_path)
    
    def run(self):
        try:
            tlist = self.job_obj.get_torrent_urls()
            LOGGER.info("get_torrent_urls success.")
        except Exception as e:
            LOGGER.error(f"get_torrent_urls error: exception-{e}, {traceback.format_exc()}")
        
        try:
            self.job_obj.send_task_to_qbit(tlist)
            LOGGER.info(f"send_task_to_qbit success: {tlist}.")
        except Exception as e:
            LOGGER.error(f"send_task_to_qbit error: exception-{e}, {traceback.format_exc()}")
