from src.utils import _get_url_by_name, _get_magnet, _download_obj


def test_get_url_by_name():
    test_name_lists = [
        '葬送的芙莉莲'
    ]
    for name in test_name_lists:
        url_route = _get_url_by_name(name)
        print(f"url route for {name}: {url_route}")


def test_get_magnet():
    magnet = _get_magnet('/Home/Bangumi/3141')
    print(f"magnet: {magnet}")


def test_download_obj():
    magnet = _get_magnet('/Home/Bangumi/3141')
    _download_obj(magnet, './C:/Users/37806/OneDrive/Utils')


if __name__ == '__main__':
    # test_get_url_by_name()
    # test_get_magnet()
    test_download_obj()
