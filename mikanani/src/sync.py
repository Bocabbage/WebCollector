import re
import os
import time
import traceback
from datetime import datetime, timedelta
import redis
from db_helper import get_mysql_conn
from configs import QbitConfig, RedisConfig
from logger import LOGGER
from utils import numset2bitmap

class MikanamiAnimeSync:
    def sync(self) -> None:
        # Get expected-list in mongodb
        anime_infos = dict()
        
        conn = get_mysql_conn()
        sql = "SELECT uid, name, download_bitmap FROM `mikanani`.`anime_meta` WHERE is_active IS TRUE;"
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            return

        for uid, name, download_bitmap in result:
            anime_infos.setdefault(uid, {'name': name, 'download_bitmap': download_bitmap})
        
        to_update_animes = dict()
        # For finding un-rename files
        regex_pattern = re.compile(r"\b\d{2}\b")
        renamed_pattern = re.compile(r"\d+")
        current_time = time.time()
        for uid, info in anime_infos.items():
            target_dir = os.path.join(QbitConfig["nfs_media_file_dir"], f"medias/{uid}")
            num_set = set()
            
            files = os.listdir(target_dir)
            files = [entry for entry in files 
                     if (
                         os.path.isfile(os.path.join(target_dir, entry)) and 
                         os.path.getmtime(os.path.join(target_dir, entry)) < current_time - 30 * 60
                        )
                    ]
            for file in files:
                if match_obj := regex_pattern.search(file):
                    # un-rename files
                    episode = int(match_obj.group(0))
                    os.rename(
                        os.path.join(target_dir, file),
                        os.path.join(target_dir, f"{episode}.mp4")
                    )
                    num_set.add(int(match_obj.group(0)))
                elif renames := renamed_pattern.findall(file):
                    num_set.add(int(renames[0]))
            curr_bitmap = numset2bitmap(num_set)
            if curr_bitmap != info.get("download_bitmap"):
                to_update_animes[uid] = curr_bitmap
        
        if to_update_animes:
            LOGGER.info(f"[Sync]need to update bitmap today count: {len(to_update_animes)}")
            redis_update = dict()
            timestamp = str(int((datetime.now() + timedelta(days=3)).timestamp()))
            try:
                conn = get_mysql_conn()
                for uid, bitmap in to_update_animes.items():
                    # Update mysql record
                    usql = ("UPDATE `mikanani`.`anime_meta` "
                            f"SET download_bitmap = {bitmap} "
                            f"WHERE uid = {uid};")
                    cursor = conn.cursor()
                    cursor.execute(usql)
                    conn.commit()
                    LOGGER.info(f"[Sync][UpdateMySQL][SUCCESS]uid:{uid} bitmap to {bitmap}.")
                    redis_update[f"{uid}"] = timestamp

                # Update redis
                host: str = RedisConfig['host']
                port: int = int(RedisConfig['port'])
                pwd: str = RedisConfig['password']
                key = "mikananistate:recentupdate"
                rds_cli = redis.StrictRedis(host, port, 0, pwd)
                res = rds_cli.hset(key, mapping=redis_update)
                rds_cli.expire(key, timedelta(days=3))
                LOGGER.info(f"[Sync][UpdateRedis]result: {res}")

            except Exception as e:
                LOGGER.error(f"[Sync][FAILED] Exception {e}: {traceback.format_exc()}")
