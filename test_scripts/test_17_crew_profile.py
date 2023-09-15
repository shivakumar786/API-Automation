__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.CREW_PROFILE
@pytest.mark.run(order=18)
class TestCrewProfile:
    """
    Test Suite to test Crew Profile

    """

    @pytestrail.case(253)
    def test_01_get_profile_settings(self, config, rest_ship):
        """
        Get Crew Profile Settings
        :param config:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-profile/settings")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('multimediaUrl', _content)
        is_key_there_in_dict('socialSettings', _content)
        is_key_there_in_dict('allergiesMaxLength', _content)
        is_key_there_in_dict('nickNameMaxLength', _content)
        is_key_there_in_dict('likesMaxLength', _content)
        is_key_there_in_dict('interestsMaxLength', _content)

    @pytestrail.case(254)
    def test_02_get_profile_lookup(self, config, rest_ship):
        """
        Get Crew Profile Lookup
        :param config:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-profile/lookup")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('astroSigns', _content)
        is_key_there_in_dict('maritalstatuses', _content)
        for astro_sign in _content['astroSigns']:
            is_key_there_in_dict('name', astro_sign)
        for marital_status in _content['maritalstatuses']:
            is_key_there_in_dict('name', marital_status)

    @pytestrail.case(255)
    def test_03_get_personal_items(self, config, rest_ship):
        """
        Get Crew Personal Items
        :param config:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-profile/personalitems")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        for personal_item in _content:
            is_key_there_in_dict('teamMemberPersonalItemId', personal_item)
            is_key_there_in_dict('name', personal_item)
            is_key_there_in_dict('isDeleted', personal_item)

    @pytestrail.case(256)
    def test_04_add_personal_item(self, config, test_data, rest_ship):
        """
        Add Personal Item
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-profile/personalitems")
        test_data['crewProfile'] = dict()
        test_data['crewProfile']['serialNumber'] = generate_random_alpha_numeric_string()
        test_data['crewProfile']['personId'] = test_data['personId']
        body = {
            "teamMemberId": test_data['crewProfile']['personId'],
            "imageMediaItemId": "", "name": "Apple", "description": "Iphone X", "approvalStatus": "PENDING",
            "serialNumber": test_data['crewProfile']['serialNumber'], "isDeleted": False
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            personal_items = [x for x in _content if x['serialNumber'] == test_data['crewProfile']['serialNumber']]
            for item in personal_items:
                is_key_there_in_dict('teamMemberPersonalItemId', item)
                is_key_there_in_dict('name', item)
                is_key_there_in_dict('isDeleted', item)

                if item['isDeleted'] is True:
                    raise Exception(
                        f"ERROR: Item {test_data['crewProfile']['serialNumber']} is not added successfully !!")
                test_data['crewProfile']['teamMemberPersonalItemId'] = item['teamMemberPersonalItemId']
        else:
            raise Exception("Personal Item is not added successfully")

    @pytestrail.case(257)
    def test_05_delete_personal_items(self, config, test_data, rest_ship):
        """
        Delete Personal Item
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"itemId": test_data['crewProfile']['teamMemberPersonalItemId']}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-profile/personalitems")
        _content = rest_ship.send_request(method="DELETE", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            personal_items = [x for x in _content if x['serialNumber'] == test_data['crewProfile']['serialNumber']]
            for item in personal_items:
                is_key_there_in_dict('teamMemberPersonalItemId', item)
                is_key_there_in_dict('name', item)
                is_key_there_in_dict('isDeleted', item)

                if item['isDeleted'] is False:
                    raise Exception(f"ERROR: {test_data['crewProfile']['serialNumber']} Failed to Delete !!")
        else:
            raise Exception("No Personal item is there for deletion")
