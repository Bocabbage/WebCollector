from src.utils import get_url_by_name, get_magnet, download_obj


def test_get_url_by_name():
    test_name_lists = [
        '葬送的芙莉莲'
    ]
    for name in test_name_lists:
        url_route = get_url_by_name(name)
        print(f"url route for {name}: {url_route}")


def test_get_magnet():
    magnet = get_magnet('/Home/Bangumi/3141')
    print(f"magnet: {magnet}")


def test_download_obj():
    magnet = get_magnet('/Home/Bangumi/3141')
    download_obj(magnet, './')


if __name__ == '__main__':
    # test_get_url_by_name()
    # test_get_magnet()
    test_download_obj()
