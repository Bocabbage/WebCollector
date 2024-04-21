import re
import os
import time
import traceback
from bson.int64 import Int64
from db_helper import get_mongo_client, get_mysql_conn
from configs import QbitConfig, MongoDBConfig
from logger import LOGGER
from utils import numset2bitmap

class MikanamiAnimeSync:
    def sync(self) -> None:
        # Get expected-list in mongodb
        anime_infos = dict()
        
        conn = get_mysql_conn()
        sql = f"SELECT uid, download_bitmap FROM `mikanani`.`anime_meta` WHERE is_active IS TRUE;"
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            return

        for uid, download_bitmap in result:
            anime_infos.setdefault(uid, {'download_bitmap': download_bitmap})
        
        to_update_animes = dict()
        # TODO: enhance, a little tricky
        regex_pattern = re.compile(r"\b\d{2}\b")
        current_time = time.time()
        for uid, info in anime_infos.items():
            target_dir = os.path.join(QbitConfig["nfs_media_file_dir"], f"medias/{uid}")
            num_dict = dict()
            
            files = os.listdir(target_dir)
            files = [entry for entry in files 
                     if (
                         os.path.isfile(os.path.join(target_dir, entry)) and 
                         os.path.getmtime(os.path.join(target_dir, entry)) < current_time - 30 * 60
                        )
                    ]
            for file in files:
                if match_obj := regex_pattern.search(file):
                    num_dict.setdefault(int(match_obj.group(0)), file)
            curr_bitmap = numset2bitmap(set(num_dict.keys()))
            if curr_bitmap != info.get("download_bitmap") or len(num_dict) > 0:
                to_update_animes[uid] = {
                    "curr_bitmap": curr_bitmap,
                    "num_dict": num_dict,
                }
        
        if to_update_animes:
            LOGGER.info(f"[Sync]need to update bitmap today count: {len(to_update_animes)}")
            try:
                conn = get_mysql_conn(set(num_dict.keys()))
                for uid, val in to_update_animes.items():
                    # Update mysql record
                    bitmap = val.get("curr_bitmap")
                    usql = ("UPDATE `mikanani`.`anime_meta` "
                            f"SET download_bitmap = {bitmap} "
                            f"WHERE uid = {uid};")
                    cursor = conn.cursor()
                    cursor.execute(usql)
                    conn.commit()
                    LOGGER.info(f"[Sync][UpdateMySQL][SUCCESS]uid:{uid} bitmap to {bitmap}.")
                    # Rename the record
                    for episode, old_filename in num_dict.items():
                        os.rename(
                            os.path.join(target_dir, old_filename),
                            os.path.join(target_dir, f"{episode}.mp4")
                        ) 
                    LOGGER.info(f"[Sync][RenameFile][SUCCESS]: uid:{uid}.")
            except Exception as e:
                LOGGER.error(f"[Sync][FAILED] Exception {e}: {traceback.format_exc()}")
