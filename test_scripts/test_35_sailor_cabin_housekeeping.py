__author__ = 'Saloni.pattnaik'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.INTEGRATION
@pytest.mark.SAILOR_HOUSEKEEPING
@pytest.mark.run(order=37)
class TestSailorHousekeeping:
    """
    Test Suite to check integration of cabin services and house keeping
    """

    @pytestrail.case(26112488)
    def test_01_login(self, config, test_data, guest_data, rest_ship):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        test_data['housekeepingGuest'] = dict()
        test_data['sailorHousekeeping'] = dict()
        test_data['sailorHousekeeping']['guest'] = dict()
        test_data['sailorHousekeeping']['user'] = 'd01796e7-2c4f-428e-b6a1-3ab996ab327c'
        guest = guest_data[0]
        _shore = config.ship.url
        url = urljoin(_shore, "user-account-service/signin/email")
        body = {
            "userName": guest['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

    @pytestrail.case(662299)
    def test_02_start_up(self, config, rest_ship):
        """
        Guest start up
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/housekeeping/startup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('configurations', _content)

    @pytestrail.case(26116396)
    def test_03_list_of_cabin_services(self, config, test_data, rest_ship):
        """
        Get Lists for all Services
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {
            "device": "app",
            "cabinNumber": test_data['cabinNumber'],
            "shipcode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), 'housekeeping/landing')
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        assert _content['serviceLabel'] == "Cabin Services", "Cabin Services Label is not Correct !!"
        assert _content['maintenanceText'] == "Maintenance", "Maintenance service is not available !!"
        assert _content[
                   'header'] == "Hey Sailor, tell us how we can help you.", "header is not matching in service tab!!"
        for buttons_title in _content['serviceButtons']:
            if buttons_title['requestName'] not in ['freshTowels', 'cabinClean', 'waterRefill', 'bed', 'ice',
                                                    'laundry']:
                raise Exception(f"{buttons_title['requestName']} is not exist in response")

        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), 'housekeeping/waterRefill/confirmation')
        params = {
            "device": "app",
            "isActive": "false"
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for response in _content['requestButtons']:
            if response['requestName'] not in ['stillWater', 'sparklingWater', 'stillAndSparklingWater']:
                raise Exception(f"{response['requestName']} is not exist in response")

    @pytestrail.case(1125002)
    def test_04_guest_create_request(self, config, test_data, rest_ship, guest_data):
        """
        Guest raising request
        :param guest_data:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:

        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), 'housekeeping/createRequest/')
        _body = {
            "requestName": "cabinClean",
            "cabinNumber": test_data['cabinNumber'],
            "reservationGuestId": guest_data[0]['reservationGuestId'],
            "reservationId": guest_data[0]['reservationId'],
            "userId": test_data['sailorHousekeeping']['user']
        }
        params = {'device': 'app'}
        _content = rest_ship.send_request(method="POST", url=_url, json=_body, params=params, auth="user").content
        is_key_there_in_dict('requestId', _content)
        test_data['sailorHousekeeping']['requestId'] = _content['requestId']
        assert _content['status'] == "pending", "Wrong status displaying,it should be pending!"

    @pytestrail.case(26155048)
    def test_05_schedule_search(self, config, test_data, rest_ship):
        """
        Get the schedule search
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/search")
        data = {
            "teamMemberIds": [test_data['sailorHousekeeping']['user']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=data, auth="crew").content
        hour = datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + test_data['aci']['shipOffSet']).hour
        if 8 <= hour < 22:
            test_data['sailorHousekeeping']['dayPeriod'] = 'day'
        else:
            test_data['sailorHousekeeping']['dayPeriod'] = 'night'
        for _schedule in _content:
            is_key_there_in_dict('date', _schedule)
            is_key_there_in_dict('dayPeriod', _schedule)
            is_key_there_in_dict('teamMemberId', _schedule)
            is_key_there_in_dict('teamMemberRole', _schedule)
            is_key_there_in_dict('placeSectionIds', _schedule)
            is_key_there_in_dict('placeDeckIds', _schedule)

            assert test_data['sailorHousekeeping']['user'] == _schedule['teamMemberId'], "teamMemberId mismatch !!"

    @pytestrail.case(26112489)
    def test_06_login(self, config, rest_ship):
        """
        Crew Login as Deck Manager
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, 'user-account-service/signin/username')
        body = {
            "userName": "SDUBE01",
            "password": "Test@1234"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.crewToken = f"{str(_content['tokenType']).capitalize()} {_content['accessToken']}"

    @pytestrail.case(26155536)
    def test_07_get_venue(self, config, test_data, rest_ship):
        """
        Get Venue place id
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, 'locationconstruct-service/venues')
        params = {
            'name': test_data['cabinNumber'],
            'offset': 0,
            'limit': 100,
            'simId': 1
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for _venue in _content:
            is_key_there_in_dict('id', _venue['venue'])
            test_data['sailorHousekeeping']['placeId'] = _venue['venue']['id']
            test_data['sailorHousekeeping']['placeDeckIds'] = _venue['venue']['sectorId']
            for _tags in _venue['tags']:
                if 'Section' in _tags['name']:
                    test_data['sailorHousekeeping']['placeSectionId'] = _tags['id']
                    break

    @pytestrail.case(26155537)
    def test_08_team_members_on_my_team(self, config, test_data, rest_ship):
        """
        My team page
        :param config
        :param test_data
        :param rest_ship
        """
        url = urljoin(config.ship.url, 'locationconstruct-service/sections')
        params = {
            'shipcode': test_data['shipCode'],
            'size': 1000
        }
        body = {
            "simId": 1,
            "ids": "7,2,3,4,5,1,15,16,17,18,19,20,21,22,106,23,24,25"
        }
        sections = []
        _content = rest_ship.send_request(method="GET", url=url, params=params, json=body, auth="crew").content
        for _sector in _content['sectors']:
            if 'sections' in _sector:
                if len(_sector['sections']) > 0:
                    for _section in _sector['sections']:
                        sections.append(_section['id'])
        test_data['sailorHousekeeping']['placeSectionIds'] = list(set(sections))

    @pytestrail.case(26133576)
    def test_09_assign_deck_to_crew(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/search")
        body = {
            "from": str(datetime.today().date()),
            "to": str(datetime.today().date()),
            "teamMemberIds": [
                test_data['sailorHousekeeping']['user']
            ]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
            body = [
                _content[0]['publicId']
            ]
            _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{
            "placeDeckIds": [test_data['sailorHousekeeping']['placeDeckIds']],
            "placeSectionIds": test_data['sailorHousekeeping']['placeSectionIds'],
            "dayPeriod": test_data['sailorHousekeeping']['dayPeriod'],
            "teamMemberId": test_data['sailorHousekeeping']['user'],
            "teamMemberRole": "RN",
            "date": str(
                datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + test_data['aci']['shipOffSet']).date())
        }]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _team_member in _content:
            is_key_there_in_dict('placeDeckIds', _team_member)
            is_key_there_in_dict('placeSectionIds', _team_member)
            is_key_there_in_dict('dayPeriod', _team_member)
            is_key_there_in_dict('teamMemberId', _team_member)
            is_key_there_in_dict('teamMemberRole', _team_member)
            is_key_there_in_dict('date', _team_member)
            is_key_there_in_dict('publicId', _team_member)
            test_data['sailorHousekeeping']['runnerPublicId'] = _team_member['publicId']
            assert [test_data['sailorHousekeeping']['placeDeckIds']] == _team_member[
                'placeDeckIds'], "placeDeckId Mismatch!"

    @pytestrail.case(26122245)
    def test_10_login_as_runner(self, config, test_data, rest_ship):
        """
        Crew Login as runner
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, 'user-account-service/signin/username')
        body = {
            "userName": "PSALONI01",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        test_data['sailorHousekeeping']['crewToken'] = rest_ship.crewToken
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(1575693)
    def test_11_request_on_details_page(self, config, test_data, rest_ship):
        """
        Get requests on Details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 4,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['sailorHousekeeping']['user']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            test_data['No_request_sailor_cabin_runner'] = False
            for request in _content:
                if request['publicId'] == test_data['sailorHousekeeping']['requestId']:
                    break
            else:
                random_request = random.choice(_content)
                test_data['sailorHousekeeping']['requestId'] = random_request['publicId']
                test_data['sailorHousekeeping']['guest']['reservationId'] = random_request['reservationId']
                test_data['sailorHousekeeping']['guest']['reservationGuestId'] = random_request['reservationGuestId']
                test_data['sailorHousekeeping']['guest']['guestId'] = random_request['guestId']

            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                          f"/requests/{test_data['sailorHousekeeping']['requestId']}"
                          f"/assign/{test_data['sailorHousekeeping']['user']}")
            body = {
                "userId": test_data['sailorHousekeeping']['user']
            }
            try:
                rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
            except Exception as exp:
                if "400" and 'No free slots' in exp.args[0]:
                    test_data['sailorHousekeeping']['Slots_availability'] = False
                    pytest.skip("No free slots to assign new request")
                else:
                    raise Exception(exp)
            test_data['sailorHousekeeping']['Slots_availability'] = True
            _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
            body = {
                "limit": 4,
                "status": "pending",
                "sortBy": "assignedAt",
                "assignId": test_data['sailorHousekeeping']['user']
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
            for _request in _content:
                if _request['publicId'] == test_data['sailorHousekeeping']['requestId']:
                    break
            for _request in _content:
                is_key_there_in_dict('status', _request)
                is_key_there_in_dict('reservationGuestId', _request)
                is_key_there_in_dict('reservationId', _request)
                is_key_there_in_dict('publicId', _request)
                is_key_there_in_dict('priority', _request)
                assert 'pending' == _request['status'], "Request Mismatched !! "
        else:
            test_data['No_request_sailor_cabin_runner'] = True
            raise Exception("Newly created request doesn't get assigned to runner")

    @pytestrail.case(26156025)
    def test_12_cabin_request_on_cabin_services_in_housekeeping(self, config, test_data, rest_ship):
        """
        Get request on cabin services page of housekeeping
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_sailor_cabin_runner']:
            pytest.skip(msg="No request available on dashboard")
        elif not test_data['sailorHousekeeping']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), f"/requests/{test_data['sailorHousekeeping']['requestId']}")
        _content = rest_ship.send_request(method="GET", url=_url, auth="crew").content

        assert test_data['sailorHousekeeping']['requestId'] == _content['publicId'], "publicId mismatch !!"
        assert "pending" == _content['status'], "status is not pending"

    @pytestrail.case(10770753)
    def test_13_cancel_request_services_to_housekeeping(self, config, test_data, rest_ship):
        """
        Cancel requests from sailor app
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), 'housekeeping/updateRequest')
        _body = {
            "requestId": test_data['sailorHousekeeping']['requestId'],
            "cabinNumber": test_data['cabinNumber'],
            "status": "cancel"
        }
        _content = rest_ship.send_request(method="PUT", url=_url, json=_body, auth="user").content
        assert "cancelled" == _content['status'], "request is not cancelled !!"

    @pytestrail.case(26130070)
    def test_14_request_on_details_page(self, config, test_data, rest_ship):
        """
        Check requests on Details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_sailor_cabin_runner']:
            pytest.skip(msg="No request available on dashboard")
        elif not test_data['sailorHousekeeping']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 4,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['sailorHousekeeping']['user']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _request in _content:
            if _request['publicId'] == test_data['sailorHousekeeping']['requestId']:
                raise Exception('request is not getting cancelled !!')

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(681480)
    def test_15_guest_create_request_maintenance(self, config, guest_data, test_data, rest_ship):
        """
        Guest Create Housekeeping Maintenance Request
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _cabin = test_data['cabinNumber']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.cabinbff'), "/housekeeping/maintenance")
        _body = {
            "reservationGuestId": guest_data[0]['reservationGuestId'],
            "incidentCategoryCode": "CABS",
            "stateroom": test_data['cabinNumber']
        }
        params = {
            "device": 'app',
            "shipcode": config.ship.code
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=_body, params=params, auth="crew").content
        test_data['housekeepingGuest']['incidentId'] = _content['incidentId']
        test_data['housekeepingGuest']['incidentCategoryCode'] = _content['incidentCategoryCode']

    @pytestrail.case(26156026)
    def test_16_un_assign_deck_to_crew_member(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [
            test_data['sailorHousekeeping']['runnerPublicId']
        ]
        _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

    @pytestrail.case(26151270)
    def test_17_check_splash_screen(self, config, test_data, guest_data, rest_ship):
        """
        To check splash screen call for ship eats and cabin services
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        services = ['cabin', 'eats']
        for service in services:
            url = urljoin(getattr(config.ship.contPath, "url.path.guestbff"),
                                                                        f'/discover/splashscreenCheck/{service}')
            params = {
                    "reservation-guest-id": guest_data[0]['reservationGuestId'],
                    "reservation-number": test_data['reservationNumber']
                    }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            is_key_there_in_dict('showSplashScreen', _content)
            assert not _content['showSplashScreen'], f"Show splash screen returning True for {service} service"

