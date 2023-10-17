from configs import PROXY_ADDR, SEARCH_ROUTE, BASE_URL
from typing import Optional
from logger import LOGGER
from bs4 import BeautifulSoup
from urllib.parse import quote
from qbittorrent import Client
import requests

proxies = {
    'http': 'http://' + PROXY_ADDR,
    'https': 'http://' + PROXY_ADDR,
}


def _get_url_by_name(anime_name: str) -> Optional[str]:
    search_url = BASE_URL + SEARCH_ROUTE + quote(anime_name)
    try:
        response = requests.get(
            search_url,
            proxies=proxies
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all(name='ul', class_='an-ul')
        if links:
            link = links[0].find('a')
            print(f"link: {link}")
            url_route = link.get('href')
            LOGGER.info(f"{anime_name} url route found: {url_route}")
            return url_route
        else:
            LOGGER.debug(f"{anime_name} url route not found.")
            return None
    except Exception as e:
        LOGGER.error(f'get url by name failed of {anime_name}: exception: {e}')
        return None


def _get_magnet(
        detail_url_route: str,
        target_sources: list = ['ANi']
) -> Optional[str]:
    try:
        # print(f"BASE_URL + detail_url_route: {BASE_URL + detail_url_route}")
        response = requests.get(
            BASE_URL + detail_url_route,
            proxies=proxies
        )
    except Exception as e:
        LOGGER.debug(f'get html file failed for detail_url {detail_url_route}: exception {e}')
        return None

    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    magnet = None
    target_group = None
    for source in target_sources:
        target_groups = soup.find_all('a', text=source, target='_blank')

        if target_groups:
            target_group = target_groups[0]
            target_group = target_group.find_parent('div')
            break
    if target_group:
        try:
            target_table = target_group.find_next('table')

            magnet = target_table.find('tbody').find('tr').find('td').find_all('a')[1].get('data-clipboard-text')
            LOGGER.info(f"magnet found: {magnet}")
        except Exception as e:
            LOGGER.debug(f"get magnet failed for: {detail_url_route} in finding table-entry.")
    else:
        LOGGER.debug(f"get magnet failed for: {detail_url_route} in source-list: {target_sources}")

    return magnet


def _download_obj(magnet: str, savepath: str) -> bool:
    qb = Client('http://127.0.0.1:8080/', verify=False)
    try:
        # Todo: Add retry
        qb.download_from_link(magnet, savepath=savepath)
        return True
    except Exception as e:
        LOGGER.debug(f"download obj {magnet} failed: exception {e}")
    return False
