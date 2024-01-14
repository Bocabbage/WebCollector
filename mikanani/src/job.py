import os
import re
import xmltodict
import traceback
import requests
import yaml
import qbittorrent
import base64
from typing import Optional, List
from .configs import ProxyConfig, QbitConfig
from .logger import LOGGER
from .errors import NoRSSYamlError, RSSRuleFileError, RSSRuleFileErrCode
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
        
    def _get_torrent_urls(self, rss_rules: dict) -> List[str]:
        result_list = list()
        try:
            name: str = rss_rules['name']
            rss_url: str = rss_rules['rss_url']
            rule_version: str = rss_rules['rule_version']
            rule_regex: str = r"{}".format(rss_rules['rule_regex'])
        except KeyError as e:
            not_found_key = e.args[0]
            raise RSSRuleFileError(
                message=f"{RSSRuleFileErrCode.YAML_FORMAT_ERROR.name}, miss key: {not_found_key}",
                error_code=RSSRuleFileErrCode.YAML_FORMAT_ERROR.value
            )
        
        # Get rss-xml
        rss_xml_dict = dict()
        response = requests.get(rss_url, proxies=self.proxies)
        if response.status_code != 200:
            raise RSSRuleFileError(
                message=f"{RSSRuleFileErrCode.RSS_XML_REQUEST_ERROR.name}: request error code={response.status_code}",
                error_code=RSSRuleFileErrCode.RSS_XML_REQUEST_ERROR.value
            )
        rss_xml_dict = xmltodict.parse(response.text)
        regex_pattern = re.compile(rule_regex)
        if rule_version == 'latest':
            try:
                target_items: list = rss_xml_dict['rss']['channel']['item']
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
                    result_list.append(latest_url)
            except Exception as e:
                raise RSSRuleFileError(
                    message=f"{RSSRuleFileErrCode.XML_PARSE_ERROR.name}: {traceback.format_exc()}",
                    error_code=RSSRuleFileErrCode.XML_PARSE_ERROR.value
                )
        elif rule_version == 'all':
            try:
                target_items: list = rss_xml_dict['rss']['channel']['item']
                latest_number: int = -1
                latest_url: Optional[str] = None
                
                for item in target_items.items():
                    title = item['title']
                    if match_obj := regex_pattern.match(title):
                        latest_url = item["enclosure"]["@url"]
                        result_list.append(latest_url)
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
            
    
    def get_torrent_urls(self, input_configs: Optional[dict] = None) -> Optional[List[str]]:
        result: List[str] = list()
        
        if input_configs is None: # direct mode
            for rootdir, _, files in os.walk(self.config_dir):
                for file in files:
                    if file == 'example.yaml':
                        continue
                    with open(os.path.join(rootdir, file), 'r', encoding='utf-8') as ifile:
                        rss_rules = yaml.safe_load(ifile)
                        if torrents := self._get_torrent_urls(rss_rules):
                            result.extend(torrents)
        else:
            for rss_rules in input_configs:
                if torrents := self._get_torrent_urls(rss_rules):
                    result.extend(torrents)
        return result
    
    def send_task_to_qbit(self, torrent_url_lists: List[str]) -> List[str]:
        qbit_dir = QbitConfig['torrent_file_dir']
        os.makedirs(qbit_dir, exist_ok=True)
        
        expected_source = list()
        for t_url in torrent_url_lists:
            t_name = os.path.basename(t_url)
            file_path = os.path.join(qbit_dir, t_name)
            if os.path.exists(file_path):
            # filter out exist objs
                continue
            response = requests.get(t_url, proxies=self.proxies)
            if response.status_code != 200:
                LOGGER.warning(f"torrent-file download failed: {t_url}")
                continue
            with open(file_path, 'wb') as ofile:
                ofile.write(response.content)
            expected_source.append(file_path)

        # [todo] clean failed-torrents
        if expected_source:
            torrent_list = [open(f, 'rb') for f in expected_source]
            media_path = QbitConfig['media_file_dir']
            qb_cli = qbittorrent.Client(QbitConfig['qbit_addr'])
            res = qb_cli.login(username=QbitConfig['username'], password=QbitConfig['password'])
            LOGGER.debug(f"login status: {res}")
            qb_cli.download_from_file(torrent_list, savepath=media_path)
        else:
            LOGGER.warning(f"No new media file to download.")
            
        return expected_source

# [todo] implement
class CleanJob:
    pass

# [deprecated]
# class JobBase:
#     def __init__(
#         self,
#         target_animes: dict[Optional[list]],
#         save_path: str,
#     ):
#         r'''
#             target_animes:
#             {
#                 "anime_name1": ["source1", "source2", ...],
#                 "anime_name1": None (Find the default one)
#             }
#         '''
#         self.target_animes = target_animes
#         self.save_path = save_path

#     def run(self):
#         for anime_name, source_list in self.target_animes.items():
#             try:
#                 url_route = get_url_by_name(anime_name)
#                 magnet = get_magnet(url_route, source_list)
#                 save_path = os.path.join(self.save_path, anime_name)

#                 if not download_obj(magnet, save_path):
#                     LOGGER.error(f"[{anime_name}] send task to qbittorent failed.")
#             except Exception as e:
#                 LOGGER.error(f"[{anime_name}] download failed, exception: {e}")