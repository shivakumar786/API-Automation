__author__ = 'Sarvesh.Singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.CABIN_TV
@pytest.mark.run(order=25)
class TestCabinTv:
    """
    Test Suite to Test Cabin TV App
    """

    @pytestrail.case(915060)
    def test_01_startup(self, config, rest_ship):
        """
        Get Startup
        :param config:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/entertainment/startup")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content

    @pytestrail.case(720222)
    def test_02_get_entertainment_content(self, config, rest_ship, guest_data, test_data):
        """
        Get video content
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": guest_data[0]['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/entertainment/content/")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if len(_content['contents']) == 0:
            raise Exception("There is no video content for entertainment")
        is_key_there_in_dict('videoUrl', _content['contents'][0])
