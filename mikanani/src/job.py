import os
import re
import glob
import xmltodict
import traceback
import requests
import qbittorrentapi
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
# import base64
from typing import Optional, List, Set
from configs import ProxyConfig, QbitConfig
from logger import LOGGER
from errors import NoRSSYamlError, RSSRuleFileError, RSSRuleFileErrCode
from schema import AnimeDocMapping # , AnimeMetaMapping
import db_helper
from utils import bitmap2numset
# from utils import get_url_by_name, get_magnet, download_obj


class RSSJob:
    r'''
        1. Load config.yamls
        2. Request RSS files and parse the url
        3. Return the torrent-url-list
    '''
    def __init__(self, config_dir: Optional[str]):
        if config_dir is None:
            raise NoRSSYamlError
        self.config_dir: str = config_dir
        self.proxies = None
        if ProxyConfig['proxy_enable']:
            self.proxies = {
                'http': f"http://{ProxyConfig['proxy_addr']}:{ProxyConfig['proxy_port']}",
                'https': f"http://{ProxyConfig['proxy_addr']}:{ProxyConfig['proxy_port']}",
            }

    
    @classmethod
    def _clean_dir(cls, dir: str) -> None:
        pattern = os.path.join(dir, '*')
        files = glob.glob(pattern)
        for filename in files:
            os.remove(filename)


    def _get_torrent_urls(self, rss_rules: dict) -> List[tuple]:
        result_list = list()
        try:
            # name: str = rss_rules[AnimeMetaMapping.name]
            rss_url: str = rss_rules[AnimeDocMapping.rssUrl]
            rule_version: str = rss_rules[AnimeDocMapping.rule]
            rule_regex: str = r"{}".format(rss_rules[AnimeDocMapping.regex])
        except KeyError as e:
            not_found_key = e.args[0]
            raise RSSRuleFileError(
                message=f"{RSSRuleFileErrCode.YAML_FORMAT_ERROR.name}, miss key: {not_found_key}",
                error_code=RSSRuleFileErrCode.YAML_FORMAT_ERROR.value
            )
        
        # Get rss-xml
        rss_xml_dict = dict()
        try:
            rss_session = Session()

            retries = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[502, 503, 504],
                allowed_methods={'GET'},
            )
            rss_session.mount("https://", HTTPAdapter(max_retries=retries))

            response = rss_session.get(rss_url, proxies=self.proxies, timeout=60)
            if response.status_code != 200:
                raise RSSRuleFileError(
                    message=f"{RSSRuleFileErrCode.RSS_XML_REQUEST_ERROR.name}: request error code={response.status_code}",
                    error_code=RSSRuleFileErrCode.RSS_XML_REQUEST_ERROR.value
                )
        except Exception as e:
            LOGGER.error(f"request error for rss_url: {rss_url}, proxies={self.proxies}")
            raise
        rss_xml_dict = xmltodict.parse(response.text)
        regex_pattern = re.compile(rule_regex)
        if rule_version == 'latest':
            try:
                target_items: list = rss_xml_dict['rss']['channel']['item']
                # Robust enhance
                if isinstance(target_items, dict):
                    target_items = [target_items]
                
                latest_number: int = -1
                latest_url: Optional[str] = None
                
                for item in target_items:
                    title = item['title']
                    if match_obj := regex_pattern.match(title):
                        number = int(match_obj.groups(1)[0])
                        if number > latest_number:
                            latest_number = number
                            latest_url = item["enclosure"]["@url"]
                if latest_url is not None:
                    result_list.append((latest_number, latest_url))
            except Exception as e:
                raise RSSRuleFileError(
                    message=f"{RSSRuleFileErrCode.XML_PARSE_ERROR.name}: {traceback.format_exc()}",
                    error_code=RSSRuleFileErrCode.XML_PARSE_ERROR.value
                )
        elif rule_version == 'all':
            try:
                target_items: list = rss_xml_dict['rss']['channel']['item']
                # Robust enhance
                if isinstance(target_items, dict):
                    target_items = [target_items]
                
                for item in target_items:
                    title = item['title']
                    if match_obj := regex_pattern.match(title):
                        number = int(match_obj.groups(1)[0])
                        url = item["enclosure"]["@url"]
                        result_list.append((number, url))
            except Exception as e:
                raise RSSRuleFileError(
                    message=f"{RSSRuleFileErrCode.XML_PARSE_ERROR.name}: {traceback.format_exc()}",
                    error_code=RSSRuleFileErrCode.XML_PARSE_ERROR.value
                )
        else:
            raise RSSRuleFileError(
                message=f"{RSSRuleFileErrCode.RULE_VERSION_ERROR.name}: {rule_version}",
                error_code=RSSRuleFileErrCode.RULE_VERSION_ERROR.value
            )
            
        return result_list
            
    
    def get_torrent_urls(self, input_config: dict = None) -> Optional[List[str]]:
        result: List[str] = list()
        if torrents := self._get_torrent_urls(input_config):
            result.extend(torrents)
        return result

    
    def send_task_to_qbit(self, torrent_url_infos: dict) -> None:
        r'''
            torrent_url_infos: {
                uid: str
                tlist: List[(int, str)] -- pair of (episode, torrent_url)
            }
        '''
        qbit_dir = QbitConfig['torrent_file_dir']
        os.makedirs(qbit_dir, exist_ok=True)
        
        uid: str = torrent_url_infos.get("uid")
        tlist: list = torrent_url_infos.get("tlist")
        
        # Get downloaded list from mysql
        qsql = (f"SELECT download_bitmap FROM `mikanani`.`anime_meta` WHERE uid = {uid};")
        conn = db_helper.get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute(qsql)
        result = cursor.fetchall()
        
        if not result:
            LOGGER.warning(f"uid[{uid}] not exist in db but sent from job. Ignored")
            return
        downloaded_episodes = bitmap2numset(result[0][0])
        
        expected_source = list()
        for episode, t_url in tlist:
            # Ignore downloaded item(s)
            if episode in downloaded_episodes:
                continue

            t_name = os.path.basename(t_url)
            file_path = os.path.join(qbit_dir, t_name)
            response = requests.get(t_url, proxies=self.proxies)
            if response.status_code != 200:
                LOGGER.error(f"torrent-file download failed:[uid: {uid}, episode: {episode}, url: {t_url}]")
                continue
            with open(file_path, 'wb') as ofile:
                ofile.write(response.content)
            expected_source.append(file_path)

        if expected_source:
            torrent_list = [open(f, 'rb') for f in expected_source]
            conn_info = dict(
                host=QbitConfig['qbit_addr'],
                port=int(QbitConfig['qbit_port']),
                username=QbitConfig['username'],
                password=QbitConfig['password'],
            )
            try:
                # Call Qbittorrent API for downloading
                with qbittorrentapi.Client(**conn_info) as qbt_client:
                    if qbt_client.torrents_add(
                        torrent_files=torrent_list, 
                        save_path=os.path.join(QbitConfig['media_file_dir'], f"medias/{uid}/")
                    ) == "Ok.":
                        LOGGER.info(f"[daily-send][SUCCESS][uid: {uid}, counts: {len(expected_source)}]")
                    else:
                        LOGGER.error(f"[daily-send][FAILED][uid: {uid}, task: {torrent_list}] Qbittorrent API return not OK.")
                # Finish download, clean torrent files.
                self._clean_dir(qbit_dir)
            except Exception as e:
                LOGGER.error(f"[daily-send][FAILED][uid: {uid}, task: {torrent_list}] Exception: {e}, traceback: {traceback.format_exc()}")
        else:
            LOGGER.debug(f"[daily-send][IGNORED]No new media file to download for uid:{uid}.")
