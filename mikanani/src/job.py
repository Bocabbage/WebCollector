import os
from typing import Optional
from logger import LOGGER
from utils import get_url_by_name, get_magnet, download_obj


class JobBase:
    def __init__(
        self,
        target_animes: dict[Optional[list]],
        save_path: str,
    ):
        r'''
            target_animes:
            {
                "anime_name1": ["source1", "source2", ...],
                "anime_name1": None (Find the default one)
            }
        '''
        self.target_animes = target_animes
        self.save_path = save_path

    def run(self):
        for anime_name, source_list in self.target_animes.items():
            try:
                url_route = get_url_by_name(anime_name)
                magnet = get_magnet(url_route, source_list)
                save_path = os.path.join(self.save_path, anime_name)

                if not download_obj(magnet, save_path):
                    LOGGER.error(f"[{anime_name}] send task to qbittorent failed.")
            except Exception as e:
                LOGGER.error(f"[{anime_name}] download failed, exception: {e}")