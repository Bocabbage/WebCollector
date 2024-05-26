import os
import re
import glob
import traceback
from typing import Optional, List
import xmltodict
import requests
import qbittorrentapi
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
# import base64
from configs import ProxyConfig, QbitConfig
from logger import LOGGER
from errors import RSSRuleFileError, RSSRuleFileErrCode
from schema import AnimeDocMapping
import db_helper
from utils import bitmap2numset


class RSSJob:
    r'''
        1. Request RSS files and parse the url
        2. Return the torrent-url-list
    '''
    def __init__(self):
        self.proxies = None
        if ProxyConfig['proxy_enable']:
            self.proxies = {
                'http': f"http://{ProxyConfig['proxy_addr']}:{ProxyConfig['proxy_port']}",
                'https': f"http://{ProxyConfig['proxy_addr']}:{ProxyConfig['proxy_port']}",
            }

    
    @classmethod
    def _clean_dir(cls, to_clean_dir: str) -> None:
        pattern = os.path.join(to_clean_dir, '*')
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
            LOGGER.error(f"[get_torrent_urls]Key error for: {not_found_key}")
            raise
        
        # Get rss-xml by requesting mikanani url
        rss_xml_dict = dict()
        try:
            # Retry options setting
            rss_session = Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], allowed_methods={'GET'})
            rss_session.mount("https://", HTTPAdapter(max_retries=retries))

            # Get 
            response = rss_session.get(rss_url, proxies=self.proxies, timeout=180)
            if response.status_code != 200:
                raise RSSRuleFileError(
                    message=f"[requests][failed][status code: {response.status_code}]",
                    error_code=RSSRuleFileErrCode.RSS_XML_REQUEST_ERROR.value
                )
        except Exception as e:
            LOGGER.error(f"[_get_torrent_urls][url:{rss_url}][proxies={self.proxies}]Error: {e}")
            raise

        # XML file parsing
        rss_xml_dict = xmltodict.parse(response.text)
        regex_pattern = re.compile(rule_regex)
        if rule_version == 'latest':
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

        elif rule_version == 'all':
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
        else:
            raise RSSRuleFileError(
                message=f"{RSSRuleFileErrCode.RULE_VERSION_ERROR.name}: {rule_version}",
                error_code=RSSRuleFileErrCode.RULE_VERSION_ERROR.value
            )
            
        return result_list
            
    
    def get_torrent_urls(self, input_config: dict = None) -> Optional[List[str]]:
        r'''
        Params:
        @input_config: dict -- Format follows [AnimeDocMapping]
        '''
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
        qsql = f"SELECT download_bitmap FROM `mikanani`.`anime_meta` WHERE uid = {uid};"
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
            response = requests.get(t_url, proxies=self.proxies, timeout=180)
            if response.status_code != 200:
                LOGGER.error(f"[send_task_to_qbit][uid: {uid}, episode: {episode}, url: {t_url}]torrent-file download failed")
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
                        LOGGER.info(f"[send_task_to_qbit][SUCCESS][uid: {uid}, counts: {len(expected_source)}]")
                    else:
                        LOGGER.error(f"[send_task_to_qbit][FAILED][uid: {uid}, task: {torrent_list}] Qbittorrent API return not OK.")
            except Exception as e:
                LOGGER.error(f"[send_task_to_qbit][FAILED][uid: {uid}, task: {torrent_list}] Exception: {e}, traceback: {traceback.format_exc()}")
        else:
            LOGGER.debug(f"[send_task_to_qbit][IGNORED][uid: {uid}].")

        # Clean the workspace        
        self._clean_dir(qbit_dir)
