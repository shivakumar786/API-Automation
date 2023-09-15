__author__ = 'Sarvesh.Singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.CABIN_CONTROL
@pytest.mark.run(order=20)
class TestCabinControl:
    """
    Test Suite to Test Cabin Control App
    """

    @pytestrail.case(186534)
    def test_01_start_up(self, config, rest_ship):
        """
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),
                      "/oauth/token?grant_type=client_credentials")
        _content = rest_ship.send_request(method="POST", url=url, auth="basic").content
        rest_ship.userToken = "bearer " + _content['access_token']

    @pytestrail.case(186535)
    def test_02_get_state_room_controls(self, config, test_data, rest_ship):
        """
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/stateroom/stateroomcontrols/5326Z")
        _content = rest_ship.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('id', _content['lightZones'][0])
        is_key_there_in_dict('brightness', _content['lightZones'][0])
        is_key_there_in_dict('scaleCurrentValue', _content['temperature'])
        test_data['temperatureValue'] = _content['temperature']['scaleCurrentValue']
        test_data['lightBrightness'] = _content['lightZones'][0]['brightness']

    @pytestrail.case(186536)
    def test_03_update_light_zones(self, config, test_data, rest_ship):
        """
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'),
                      "/stateroom/stateroomcontrols/5326Z/lightzones")
        if test_data['lightBrightness'] >= 70:
            brightness = test_data['lightBrightness'] - 10
        else:
            brightness = test_data['lightBrightness'] + 10
        body = {
            "lightZones": [
                {
                    "id": "ceiling",
                    "brightness": brightness
                }
            ]

        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        is_key_there_in_dict('message', _content)
        if "ACCEPTED" != _content['message']:
            raise Exception("Message status is not Accepted after updating light zones")

    @pytestrail.case(186537)
    def test_04_update_temperature(self, config, test_data, rest_ship):
        """
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'),
                      "/stateroom/stateroomcontrols/5326Z/temperature")
        temperature_list = [0, 1, 2, 3]
        temperature_choose = random.choice(temperature_list)
        if temperature_choose == test_data['temperatureValue']:
            temperature_list.remove(temperature_choose)
            temperature_choose = random.choice(temperature_list)
        body = {"scaleCurrentValue": temperature_choose}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        is_key_there_in_dict('message', _content)
        if "ACCEPTED" != _content['message']:
            raise Exception("Message status is not Accepted after updating temperature")

    @pytestrail.case(186538)
    def test_05_put_drape(self, config, test_data, rest_ship):
        """
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/stateroom/stateroomcontrols/5326Z/drape")
        if test_data['drapeState'] == "close":
            body = {"status": "open"}
        else:
            body = {"status": "close"}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        is_key_there_in_dict('message', _content)
        if "ACCEPTED" != _content['message']:
            raise Exception("Message status is not Accepted")

    @pytestrail.case(186539)
    def test_06_verify_changes(self, config, test_data, rest_ship):
        """
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/stateroom/stateroomcontrols/5326Z")
        _content = rest_ship.send_request(method="GET", url=url, auth="user").content
        if test_data['lightBrightness'] == _content['lightZones'][0]['brightness']:
            raise Exception("The light zones did not got updated")
        if test_data['temperatureValue'] == _content['temperature']['scaleCurrentValue']:
            raise Exception("The temperature did not got updated")
