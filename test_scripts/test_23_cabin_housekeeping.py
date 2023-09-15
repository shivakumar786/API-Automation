__author__ = 'sarvesh.singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.CABIN_HOUSE_KEEPING
@pytest.mark.run(order=24)
class TestCabinHousekeeping:
    """
    Test Suite to Test Cabin Housekeeping App
    """

    @pytestrail.case(1575696)
    def test_01_get_role_hierarchy(self, config, test_data, rest_ship, guest_data):
        """
        Get Role hierarchy
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['housekeepingCrew'] = dict()
        test_data['housekeepingCrew']['applicationId'] = '9bdfde22-8b71-11e9-ace7-0a1a4261e962'
        test_data['housekeepingCrew']['user'] = 'd01796e7-2c4f-428e-b6a1-3ab996ab327c'
        test_data['housekeepingCrew']['guest'] = guest_data[0]
        role_id = []
        test_data['housekeepingCrew']['roleId'] = []
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "/rolehierarchy")
        params = {
            'applicationId': test_data['housekeepingCrew']['applicationId']
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for _roles in _content:
            is_key_there_in_dict('roleId', _roles)
            is_key_there_in_dict('appRoleName', _roles)
            is_key_there_in_dict('appRoleCode', _roles)
        for roleId in role_id:
            if roleId not in test_data['housekeepingCrew']['roleId']:
                test_data['housekeepingCrew']['roleId'].append(roleId)

    @pytestrail.case(8365312)
    def test_02_get_user_roles(self, config, test_data, rest_ship):
        """
        Get User Roles
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "/userroles")
        params = {
            'applicationID': test_data['housekeepingCrew']['applicationId']
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for _roles in _content['applicationFeatures']:
            is_key_there_in_dict('applicationFeatureId', _roles)
            is_key_there_in_dict('name', _roles)
            is_key_there_in_dict('code', _roles)

    @pytestrail.case(8365313)
    def test_03_user_status(self, config, test_data, rest_ship):
        """
        Get the user status
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "/userstatuses/search")
        body = {
            "personIds": [test_data['housekeepingCrew']['user']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _user in _content['content']:
            is_key_there_in_dict('userId', _user)
            is_key_there_in_dict('userStatusId', _user)
            is_key_there_in_dict('applicationId', _user)
            assert test_data['housekeepingCrew']['user'] == _user['personId'], "personId mismatch !!"

    @pytestrail.case(8365314)
    def test_04_schedule_search(self, config, test_data, rest_ship):
        """
        Get the schedule search
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['housekeepingCrew']['deckId'] = []
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/search")
        data = {
            "teamMemberIds": [test_data['housekeepingCrew']['user']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=data, auth="crew").content
        hour = datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + test_data['aci']['shipOffSet']).hour
        if 8 <= hour < 22:
            test_data['housekeepingCrew']['dayPeriod'] = 'day'
        else:
            test_data['housekeepingCrew']['dayPeriod'] = 'night'
        for _schedule in _content:
            is_key_there_in_dict('date', _schedule)
            is_key_there_in_dict('dayPeriod', _schedule)
            is_key_there_in_dict('teamMemberId', _schedule)
            is_key_there_in_dict('teamMemberRole', _schedule)
            is_key_there_in_dict('placeSectionIds', _schedule)
            is_key_there_in_dict('placeDeckIds', _schedule)
            test_data['housekeepingCrew']['deckId'].append(_schedule['placeDeckIds'][0])

            assert test_data['housekeepingCrew']['user'] == _schedule['teamMemberId'], "teamMemberId mismatch !!"

    @pytestrail.case(8365316)
    def test_05_requests_count_before(self, config, test_data, rest_ship):
        """
        Get Requests count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), '/requests/count')
        body = {
            "status": "completed",
            "assignId": test_data['housekeepingCrew']['user']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['housekeepingCrew']['previousCount'] = _content

    @pytestrail.case(26112979)
    def test_06_login(self, config, rest_ship):
        """
        Crew Login
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "BKAN01",
            "password": "Test@1234"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"{str(_content['tokenType']).capitalize()} {_content['accessToken']}"

    @pytestrail.case(760024)
    def test_07_requests_search(self, config, test_data, rest_ship):
        """
        Get Requests search
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 1,
            "status": "started",
            "sortBy": "assignedAt",
            "assignId": test_data['housekeepingCrew']['user']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(760025)
    def test_08_requests_types(self, config, test_data, rest_ship):
        """
        Get Requests types
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requestTypes")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        for _types in _content:
            is_key_there_in_dict('name', _types)
            is_key_there_in_dict('priority', _types)
            is_key_there_in_dict('categoryId', _types)
            is_key_there_in_dict('isCleaning', _types)
            is_key_there_in_dict('atRiskDuration', _types)
            is_key_there_in_dict('slaDuration', _types)
            is_key_there_in_dict('requestDuration', _types)
        for _request in _content:
            test_data['housekeepingCrew']['categoryId'] = _request['categoryId']
            test_data['housekeepingCrew']['priority'] = _request['priority']
            break

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(8365318)
    def test_09_get_venue(self, config, test_data, rest_ship):
        """
        Get Venue place id
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.locationconstruct"), "/venues")
        params = {
            'name': test_data['cabinNumber'],
            'offset': 0,
            'limit': 100,
            'simId': 1
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for _venue in _content:
            is_key_there_in_dict('id', _venue['venue'])
            test_data['housekeepingCrew']['placeId'] = _venue['venue']['id']
            test_data['housekeepingCrew']['placeDeckIds'] = _venue['venue']['sectorId']
            for _tags in _venue['tags']:
                if 'Section' in _tags['name']:
                    test_data['housekeepingCrew']['placeSectionId'] = _tags['id']
                    break

    @pytestrail.case(26124637)
    def test_10_team_member_search(self, config, test_data, rest_ship):
        """
        Search the team member
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.reporting"), "/housekeeping/teammembers/search")
        params = {
            'shipcode': config.ship.code,
            'size': 1000
        }
        body = {
            "applicationId": test_data['housekeepingCrew']['applicationId'],
            "personIds": [test_data['housekeepingCrew']['user']]
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _teammemeber in _content:
            is_key_there_in_dict('personId', _teammemeber)
            is_key_there_in_dict('applicationId', _teammemeber)
            is_key_there_in_dict('userId', _teammemeber)
            assert test_data['housekeepingCrew']['user'] == _teammemeber['personId'], "personId mismatch !!"
            assert test_data['housekeepingCrew']['applicationId'] == _teammemeber[
                'applicationId'], "applicationId mismatch !!"

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(1575697)
    def test_11_team_members_on_my_team(self, config, test_data, rest_ship):
        """
        My team page
        :param config
        :param test_data
        :param rest_ship
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.locationconstruct"), "/sections")
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
        test_data['housekeepingCrew']['placeSectionIds'] = list(set(sections))

    @pytestrail.case(1575687)
    def test_12_assigned_team_on_my_team_page(self, config, test_data, rest_ship):
        """
        Get the assigned team on my Team Page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/search")
        body = {
            "teamMemberIds": [test_data['housekeepingCrew']['user']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _schedule in _content:
            is_key_there_in_dict('date', _schedule)
            is_key_there_in_dict('dayPeriod', _schedule)
            is_key_there_in_dict('teamMemberId', _schedule)
            is_key_there_in_dict('teamMemberRole', _schedule)
            is_key_there_in_dict('placeSectionIds', _schedule)
            is_key_there_in_dict('placeDeckIds', _schedule)
            assert test_data['housekeepingCrew']['user'] == _schedule['teamMemberId'], "teamMemberId mismatch !!"

    @pytestrail.case(11248897)
    def test_13_assign_deck_to_runner(self, config, test_data, rest_ship):
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
                "d01796e7-2c4f-428e-b6a1-3ab996ab327c"
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
            "placeDeckIds": [test_data['housekeepingCrew']['placeDeckIds']],
            "placeSectionIds": test_data['housekeepingCrew']['placeSectionIds'],
            "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
            "teamMemberId": 'd01796e7-2c4f-428e-b6a1-3ab996ab327c',
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
            test_data['housekeepingCrew']['runnerPublicId'] = _team_member['publicId']
            assert [test_data['housekeepingCrew']['placeDeckIds']] == _team_member[
                'placeDeckIds'], "placeDeckId Mismatch!"

    @pytestrail.case(27084951)
    def test_14_assign_deck_for_next_day(self, config, test_data, rest_ship):
        """
        Assign deck to runner for next day
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        next_day = datetime.today().date() + timedelta(days=1)
        test_data['housekeepingCrew']['shift'] = ['am', 'pm', 'night']
        assigned_shift = random.choice(test_data['housekeepingCrew']['shift'])
        body = [{
            "placeDeckIds": [test_data['housekeepingCrew']['placeDeckIds']],
            "placeSectionIds": test_data['housekeepingCrew']['placeSectionIds'],
            "dayPeriod": assigned_shift,
            "teamMemberId": '6f53086f-5ab1-427a-b0ef-8948ee9f5f7f',
            "teamMemberRole": "RN",
            "date": f"{next_day}"
        }]
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            for _teammemeber in _content:
                is_key_there_in_dict('placeDeckIds', _teammemeber)
                is_key_there_in_dict('placeSectionIds', _teammemeber)
                is_key_there_in_dict('dayPeriod', _teammemeber)
                is_key_there_in_dict('teamMemberId', _teammemeber)
                is_key_there_in_dict('teamMemberRole', _teammemeber)
                is_key_there_in_dict('date', _teammemeber)
                is_key_there_in_dict('publicId', _teammemeber)
                test_data['housekeepingCrew']['publicIdDeckAssigned'] = _teammemeber['publicId']
                assert [test_data['housekeepingCrew']['placeDeckIds']] == _teammemeber[
                    'placeDeckIds'], "placeDeckId Mismatch!"

            _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
            body = [
                test_data['housekeepingCrew']['publicIdDeckAssigned']
            ]
            _content = rest_ship.send_request(method="DELETE", url=_url, json=body, auth="crew").content
        except Exception:
            pytest.skip(msg="skipped, schedule already exists for next day")

    @pytestrail.case(26122243)
    def test_15_login_runner(self, config, test_data, rest_ship):
        """
        Log in with runner
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "PSALONI01",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        test_data['housekeepingCrew']['crewToken'] = rest_ship.crewToken
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @pytestrail.case(24930245)
    def test_16_assignment_queue_on_runner(self, config, test_data, rest_ship):
        """
        verify Assignment queue ON
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "userstatuses/updatestatus")
        body = {
            "applicationId": test_data['housekeepingCrew']['applicationId'],
            "personId": "d01796e7-2c4f-428e-b6a1-3ab996ab327c",
            "personTypeCode": "C",
            "status": "ON_LINE",
            "statusTypeCode": "USR_AVAIL",
            "statusChangedDate": test_data['aci']['validationStatusDate']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if "ACCEPTED" not in _content:
            raise Exception('Assignment queue not updated')

    @pytestrail.case(786607)
    def test_17_create_request_by_runner(self, config, test_data, rest_ship, guest_data):
        """
        Create Request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests")
        body = {
            "priority": test_data['housekeepingCrew']['priority'],
            "requestType": test_data['housekeepingCrew']['categoryId'],
            "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
            "placeSectionId": test_data['housekeepingCrew']['placeSectionId'],
            "placeId": test_data['housekeepingCrew']['placeId'],
            "guestId": test_data['housekeepingCrew']['guest']['guestId'],
            "reservationGuestId": test_data['housekeepingCrew']['guest']['reservationGuestId'],
            "reservationId": test_data['housekeepingCrew']['guest']['reservationId'],
            "userId": test_data['housekeepingCrew']['user']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('guestId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('placeId', _content)
        assert test_data['housekeepingCrew']['guest']['guestId'] == _content['guestId'], "guestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationGuestId'] == _content[
            'reservationGuestId'], "reservationGuestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationId'] == _content[
            'reservationId'], "reservationId mismatch !!"
        test_data['housekeepingCrew']['requestId'] = _content['publicId']

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(26129603)
    def test_18_request_on_details_page(self, config, guest_data, test_data, rest_ship):
        """
        Get requests on Details page
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 4,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['housekeepingCrew']['user']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            test_data['No_request_runner'] = False
            for request in _content:
                if request['publicId'] == test_data['housekeepingCrew']['requestId']:
                    test_data['Request_with_reservationGuestId'] = True
                    break
            else:
                for request in _content:
                    if request['reservationGuestId'] is not None:
                        test_data['housekeepingCrew']['requestId'] = request['publicId']
                        test_data['housekeepingCrew']['guest']['reservationId'] = request['reservationId']
                        test_data['housekeepingCrew']['guest']['reservationGuestId'] = request['reservationGuestId']
                        test_data['housekeepingCrew']['guest']['guestId'] = request['guestId']
                        test_data['Request_with_reservationGuestId'] = True
                        break
                else:
                    test_data['Request_with_reservationGuestId'] = False
                    pytest.skip("No request found with reservationGuestId")
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                          f"/requests/{test_data['housekeepingCrew']['requestId']}"
                          f"/assign/{test_data['housekeepingCrew']['user']}")
            body = {
                "userId": test_data['housekeepingCrew']['user']
            }
            try:
                rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
            except Exception as exp:
                if "400" and 'No free slots' in exp.args[0]:
                    test_data['housekeepingCrew']['Slots_availability_runner'] = False
                    pytest.skip("No free slots to assign new request")
                else:
                    raise Exception(exp)
            test_data['housekeepingCrew']['Slots_availability_runner'] = True
            _url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
            body = {
                "limit": 4,
                "status": "pending",
                "sortBy": "assignedAt",
                "assignId": test_data['housekeepingCrew']['user']
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
            for _request in _content:
                if _request['publicId'] == test_data['housekeepingCrew']['requestId']:
                    break
            for _request in _content:
                is_key_there_in_dict('status', _request)
                is_key_there_in_dict('reservationGuestId', _request)
                is_key_there_in_dict('reservationId', _request)
                is_key_there_in_dict('publicId', _request)
                is_key_there_in_dict('priority', _request)
                assert 'pending' == _request['status'], "Request Mismatched !! "
        else:
            test_data['No_request_runner'] = True
            raise Exception("Newly created request doesn't get assigned to runner")

    @pytestrail.case(871417)
    def test_19_start_request_runner(self, config, test_data, rest_ship):
        """
        Start request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_runner']:
            pytest.skip(msg="No request available on dashboard")
        elif not test_data['Request_with_reservationGuestId']:
            pytest.skip("No request found with reservationGuestId")
        elif not test_data['housekeepingCrew']['Slots_availability_runner']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['requestId']}/start")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        assert 'started' == _content['status'], "Request is not getting started !!"

    @pytestrail.case(871418)
    def test_20_complete_request(self, config, test_data, rest_ship):
        """
        Complete the request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_runner']:
            pytest.skip(msg="No request available on dashboard")
        elif not test_data['Request_with_reservationGuestId']:
            pytest.skip("No request found with reservationGuestId")
        elif not test_data['housekeepingCrew']['Slots_availability_runner']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['requestId']}/complete")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        test_data['housekeepingCrew']['status'] = _content['status']
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        assert 'completed' == _content['status'], "Request is not getting started !!"

    @pytestrail.case(8365324)
    def test_21_cabin_status_runner(self, config, test_data, rest_ship):
        """
        Get cabin status
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/cabinStatuses/search")
        body = {
            "placeIds": [test_data['housekeepingCrew']['placeId']],
            "shipCode": test_data['shipCode']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(8365325)
    def test_22_get_created_request(self, config, test_data, rest_ship):
        """
        Get created request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_runner']:
            pytest.skip(msg="No request available on dashboard")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['requestId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('guestId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        assert test_data['housekeepingCrew']['guest']['guestId'] == _content['guestId'], "guestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationGuestId'] == _content[
            'reservationGuestId'], "reservationGuestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationId'] == _content[
            'reservationId'], "reservationId mismatch !!"

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(26129604)
    def test_23_request_on_details_page(self, config, test_data, rest_ship):
        """
        Get requests on Details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if test_data['No_request_runner']:
            pytest.skip(msg="No request available on dashboard")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 4,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['housekeepingCrew']['user']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _request in _content:
            is_key_there_in_dict('status', _request)
            is_key_there_in_dict('reservationGuestId', _request)
            is_key_there_in_dict('reservationId', _request)
            is_key_there_in_dict('publicId', _request)
            is_key_there_in_dict('priority', _request)
            assert 'pending' == _request['status'], "Request Mismatched !! "

    @pytestrail.case(1575691)
    def test_24_set_cabin_preferences_runner(self, config, test_data, rest_ship):
        """
        Set cabin preferences by crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), '/guestpreferences')
        body = {
            "additionalPreference": 'Its Mandatory',
            "guestId": test_data['housekeepingCrew']['guest']['guestId'],
            "reservationGuestId": test_data['housekeepingCrew']['guest']['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('additionalPreference', _content)
        is_key_there_in_dict('guestId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('isDeleted', _content)
        is_key_there_in_dict('modifiedByUser', _content)
        is_key_there_in_dict('guestPreferenceId', _content)
        test_data['housekeepingCrew']['additionalPreference'] = _content['additionalPreference']
        test_data['housekeepingCrew']['guestPreferenceId'] = _content['guestPreferenceId']
        assert 'Its Mandatory' == test_data['housekeepingCrew'][
            'additionalPreference'], "additionalPreference Mismatched !!"

    @pytestrail.case(1575695)
    def test_25_delete_cabin_preferences_runner(self, config, test_data, rest_ship):
        """
        Delete cabin preferences by crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"),
                      f"guestpreferences/{test_data['housekeepingCrew']['guestPreferenceId']}")
        _content = rest_ship.send_request(method="DELETE", url=url, auth="crew").content

    @pytestrail.case(1575689)
    def test_26_un_assign_deck_to_runner(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [
            test_data['housekeepingCrew']['runnerPublicId']
        ]
        _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

    @pytestrail.case(32464051)
    def test_27_assign_deck_to_deck_manager(self, config, test_data, rest_ship):
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
                'd088e358-aa4d-4027-b7c1-30762fe1334e'
            ]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
            body = [
                _content[0]['publicId']
            ]
            _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

        place_deck_id = [test_data['housekeepingCrew']['placeDeckIds']]
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{
            "placeDeckIds": place_deck_id,
            "placeSectionIds": test_data['housekeepingCrew']['placeSectionIds'],
            "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
            "teamMemberId": 'd088e358-aa4d-4027-b7c1-30762fe1334e',
            "teamMemberRole": "DM",
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
            test_data['housekeepingCrew']['deck_managerpublicId'] = _team_member['publicId']
            assert place_deck_id == _team_member['placeDeckIds'], "placeDeckId Mismatch!"

    @pytestrail.case(32464880)
    def test_28_login_deck_manager(self, config, test_data, rest_ship):
        """
        Log in with deck manager
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "KKUMAR01",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content)
        is_key_there_in_dict('tokenType', _content)
        test_data['housekeepingCrew']['crewToken'] = rest_ship.crewToken
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @pytestrail.case(32464881)
    def test_29_assignment_queue_on_for_deck_manager(self, config, test_data, rest_ship):
        """
        verify Assignment queue ON
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "userstatuses/updatestatus")
        test_data['housekeepingCrew']['UserDeckManager'] = "d088e358-aa4d-4027-b7c1-30762fe1334e"
        body = {
            "applicationId": test_data['housekeepingCrew']['applicationId'],
            "personId": test_data['housekeepingCrew']['UserDeckManager'],
            "personTypeCode": "C",
            "status": "ON_LINE",
            "statusTypeCode": "USR_AVAIL",
            "statusChangedDate": test_data['aci']['validationStatusDate']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if "ACCEPTED" not in _content:
            raise Exception("Assignment queue not updated")

    @pytestrail.case(27173013)
    def test_30_create_custom_request(self, config, test_data, rest_ship):
        """
        Create custom Request by deck manager
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requestTypes")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        for _types in _content:
            is_key_there_in_dict("name", _types)
            is_key_there_in_dict("id", _types)
            is_key_there_in_dict("priority", _types)
            if _types['name'] == "Other":
                test_data['housekeepingCrew']['customId'] = _types['id']
                test_data['housekeepingCrew']['custom_priority'] = _types['priority']
                break
        else:
            raise Exception("custom request option not available")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests")
        body = {
            "priority": test_data['housekeepingCrew']['custom_priority'], "description": "Medical assistance",
            "requestType": test_data['housekeepingCrew']['customId'],
            "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
            "placeSectionId": test_data['housekeepingCrew']['placeSectionId'],
            "placeId": test_data['housekeepingCrew']['placeId'],
            "guestId": test_data['housekeepingCrew']['guest']['guestId'],
            "reservationGuestId": test_data['housekeepingCrew']['guest']['reservationGuestId'],
            "reservationId": test_data['housekeepingCrew']['guest']['reservationId'],
            "userId": test_data['housekeepingCrew']['UserDeckManager']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('guestId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('placeId', _content)
        assert test_data['housekeepingCrew']['guest']['guestId'] == _content['guestId'], "guestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationGuestId'] == _content[
            'reservationGuestId'], "reservationGuestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationId'] == _content[
            'reservationId'], "reservationId mismatch !!"
        test_data['housekeepingCrew']['requestId'] = _content['publicId']

    @pytestrail.case(32275801)
    def test_31_assign_to_me_for_deck_manager(self, config, test_data, rest_ship):
        """
        To assign to me cta for unassigned requests
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"/requests/{test_data['housekeepingCrew']['requestId']}"
                      f"/assign/{test_data['housekeepingCrew']['UserDeckManager']}")
        body = {
            "userId": test_data['housekeepingCrew']['UserDeckManager']
        }
        try:
            response = rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
            _content = response.content
        except Exception as exp:
            if "400" and 'no free slots' in exp.args[0].lower():
                test_data['housekeepingCrew']['Slots_availability'] = False
                pytest.skip("No free slots to assign new request")
            else:
                raise Exception(exp)
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('publicId', _content)
        test_data['housekeepingCrew']['AssignToMePublicId'] = _content['publicId']
        assert 'pending' == _content['status'], "Status Mismatched !!"
        test_data['housekeepingCrew']['Slots_availability'] = True

    @pytestrail.case(32320432)
    def test_32_start_request(self, config, test_data, rest_ship):
        """
        Start request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['requestId']}/start")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        assert 'started' == _content['status'], "Request is not getting started !!"

    @retry_when_fails(retries=60, interval=5)
    @pytestrail.case(32320433)
    def test_33_complete_request(self, config, test_data, rest_ship):
        """
        Complete the request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['requestId']}/complete")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        test_data['housekeepingCrew']['status'] = _content['status']
        test_data['housekeepingCrew']['publicId'] = _content['publicId']
        assert 'completed' == _content['status'], "Request is not getting started !!"

    @pytestrail.case(32274160)
    def test_34_get_team_assignments_page(self, config, test_data, rest_ship):
        """
        To Verify Team Assignments Page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        team = []
        test_data['housekeepingCrew']['teamMemberRoleId'] = []
        url = urljoin(getattr(config.ship.contPath, "url.path.reporting"), "housekeeping/teammembers/search")
        params = {"shipcode": config.ship.code, "size": 1000}
        body = {"applicationId": test_data['housekeepingCrew']['applicationId'],
                 "userRoleIds": test_data['housekeepingCrew']['roleId'],
                 "isCheckedOutCrewNeeded": False}
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for team_members in _content:
            is_key_there_in_dict('personId', team_members)
            is_key_there_in_dict('teamMemberRoleId', team_members)
            team.append(team_members['teamMemberRoleId'])
        for teamMemberRoleId in team:
            if teamMemberRoleId not in test_data['housekeepingCrew']['teamMemberRoleId']:
                test_data['housekeepingCrew']['teamMemberRoleId'].append(teamMemberRoleId)

    @pytestrail.case(1575692)
    def test_35_reassignment_request_report(self, config, test_data, rest_ship):
        """
        To verify Reassignment request reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        current_date = f"{test_data['crew_framework']['currentDate'][:10]}"
        today_date = datetime.today()
        one_month_ago = str(today_date - relativedelta(months=3)).split()[0]
        test_data['housekeepingCrew']['from_date'] = f"{one_month_ago[:10]}T18:30:00Z"
        test_data['housekeepingCrew']['to_date'] = f"{current_date}T23:59:59Z"
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "reports/requests-reassignments")
        params = {
            "from": test_data['housekeepingCrew']['from_date'],
            "to": test_data['housekeepingCrew']['to_date'],
            "teamMemberIds": [test_data['housekeepingCrew']['UserDeckManager']]
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for report in _content:
                is_key_there_in_dict('teamMemberId', report)
        else:
            raise Exception('No Reassignment request reports found')

    @pytestrail.case(1575690)
    def test_36_average_cleaning_reports(self, config, test_data, rest_ship):
        """
        To verify Average Cleaning Reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "reports/average-cleaning-time")
        params = {
            "from": test_data['housekeepingCrew']['from_date'],
            "to": test_data['housekeepingCrew']['to_date'],
            "teamMemberIds": '9518e6d7-2ec5-42d1-99cf-b6dd68f44d90',
            "deckIds": test_data['housekeepingCrew']['deckId'],
            "fromDateOffset": 330
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for report in _content:
                is_key_there_in_dict('teamMemberId', report)
        else:
            raise Exception('No Average Cleaning Reports found')

    @pytestrail.case(32464882)
    def test_37_un_assign_deck_to_deck_manager(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [
            test_data['housekeepingCrew']['deck_managerpublicId']
        ]
        _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

    @pytestrail.case(26133575)
    def test_38_assign_deck_to_cabin_host_first(self, config, test_data, rest_ship):
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
                '6e45350e-43fe-476e-81c0-e3a8066fe7ac'
            ]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
            body = [
                _content[0]['publicId']
            ]
            _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content
        place_deck_id = [test_data['housekeepingCrew']['placeDeckIds']]
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{
            "placeDeckIds": place_deck_id,
            "placeSectionIds": test_data['housekeepingCrew']['placeSectionIds'],
            "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
            "teamMemberId": '6e45350e-43fe-476e-81c0-e3a8066fe7ac',
            "teamMemberRole": "CH",
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
            test_data['housekeepingCrew']['CabinHostFirst'] = _team_member['publicId']
            assert place_deck_id == _team_member['placeDeckIds'], "placeDeckId Mismatch!"

    @pytestrail.case(32464883)
    def test_39_assign_deck_to_cabin_host_second(self, config, test_data, rest_ship):
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
                '0361bc8e-f017-45b5-9241-485259d6fdd7'
            ]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        if len(_content) > 0:
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
            body = [
                _content[0]['publicId']
            ]
            _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content
        place_deck_id = [test_data['housekeepingCrew']['placeDeckIds']]
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{
            "placeDeckIds": place_deck_id,
            "placeSectionIds": test_data['housekeepingCrew']['placeSectionIds'],
            "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
            "teamMemberId": '0361bc8e-f017-45b5-9241-485259d6fdd7',
            "teamMemberRole": "CH",
            "date": str(
                datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + test_data['aci']['shipOffSet']).date())
        }]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _teammemeber in _content:
            is_key_there_in_dict('placeDeckIds', _teammemeber)
            is_key_there_in_dict('placeSectionIds', _teammemeber)
            is_key_there_in_dict('dayPeriod', _teammemeber)
            is_key_there_in_dict('teamMemberId', _teammemeber)
            is_key_there_in_dict('teamMemberRole', _teammemeber)
            is_key_there_in_dict('date', _teammemeber)
            is_key_there_in_dict('publicId', _teammemeber)
            test_data['housekeepingCrew']['CabinHostSecond'] = _teammemeber['publicId']
            assert place_deck_id == _teammemeber['placeDeckIds'], "placeDeckId Mismatch!"

    @pytestrail.case(26122244)
    def test_40_login_cabin_host_first(self, config, test_data, rest_ship):
        """
        Log in with runner
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "PSHARMA01",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content)
        is_key_there_in_dict('tokenType', _content)
        test_data['housekeepingCrew']['crewToken'] = rest_ship.crewToken
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @pytestrail.case(26133577)
    def test_41_assignment_queue_on_for_cabin_host_first(self, config, test_data, rest_ship):
        """
        verify Assignment queue ON
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "userstatuses/updatestatus")
        test_data['housekeepingCrew']['UserCabinHostFirst'] = "6e45350e-43fe-476e-81c0-e3a8066fe7ac"
        body = {
            "applicationId": test_data['housekeepingCrew']['applicationId'],
            "personId": test_data['housekeepingCrew']['UserCabinHostFirst'],
            "personTypeCode": "C",
            "status": "ON_LINE",
            "statusTypeCode": "USR_AVAIL",
            "statusChangedDate": test_data['aci']['validationStatusDate']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if "ACCEPTED" not in _content:
            raise Exception("Assignment queue not updated")

    @pytestrail.case(27202216)
    def test_42_create_request_by_cabin_host_first(self, config, test_data, rest_ship):
        """
        Create Request by cabin host on behalf of sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests")
        body = {
            "priority": test_data['housekeepingCrew']['priority'],
            "requestType": test_data['housekeepingCrew']['categoryId'],
            "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
            "placeSectionId": test_data['housekeepingCrew']['placeSectionId'],
            "placeId": test_data['housekeepingCrew']['placeId'],
            "guestId": test_data['housekeepingCrew']['guest']['guestId'],
            "reservationGuestId": test_data['housekeepingCrew']['guest']['reservationGuestId'],
            "reservationId": test_data['housekeepingCrew']['guest']['reservationId'],
            "userId": test_data['housekeepingCrew']['UserCabinHostFirst']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('guestId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('placeId', _content)
        assert test_data['housekeepingCrew']['guest']['guestId'] == _content['guestId'], "guestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationGuestId'] == _content[
            'reservationGuestId'], "reservationGuestId mismatch !!"
        assert test_data['housekeepingCrew']['guest']['reservationId'] == _content[
            'reservationId'], "reservationId mismatch !!"
        test_data['housekeepingCrew']['CabinHostRequestId'] = _content['publicId']

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(24935886)
    def test_43_request_on_details_page_first(self, config, test_data, rest_ship):
        """
        Get requests on Details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "requests/search")
        body = {
            "limit": 2,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['housekeepingCrew']['UserCabinHostFirst']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) <= 1:
            for _request in _content:
                is_key_there_in_dict('status', _request)
                is_key_there_in_dict('reservationGuestId', _request)
                is_key_there_in_dict('reservationId', _request)
                is_key_there_in_dict('publicId', _request)
                is_key_there_in_dict('priority', _request)
                assert 'pending' == _request['status'], "Request Mismatched !! "
        else:
            pytest.skip(msg="more than two pending request on dashboard")

    @pytestrail.case(32464884)
    def test_44_login_cabin_host_second(self, config, test_data, rest_ship):
        """
        Log in with runner
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "BernardP",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content)
        is_key_there_in_dict('tokenType', _content)
        test_data['housekeepingCrew']['crewToken'] = rest_ship.crewToken
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @pytestrail.case(32464885)
    def test_45_assignment_queue_on_for_cabin_host_second(self, config, test_data, rest_ship):
        """
        verify Assignment queue ON
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.identityaccessmanagement"), "userstatuses/updatestatus")
        test_data['housekeepingCrew']['UserCabinHostSecond'] = "0361bc8e-f017-45b5-9241-485259d6fdd7"
        body = {
            "applicationId": test_data['housekeepingCrew']['applicationId'],
            "personId": test_data['housekeepingCrew']['UserCabinHostSecond'],
            "personTypeCode": "C",
            "status": "ON_LINE",
            "statusTypeCode": "USR_AVAIL",
            "statusChangedDate": test_data['aci']['validationStatusDate']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if "ACCEPTED" not in _content:
            raise Exception("Assignment queue not updated")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(32464886)
    def test_46_request_on_details_page_second(self, config, test_data, rest_ship):
        """
        Get requests on Details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests/search")
        body = {
            "limit": 2,
            "status": "pending",
            "sortBy": "assignedAt",
            "assignId": test_data['housekeepingCrew']['UserCabinHostSecond']
        }
        _content = _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['requestReadyToStart'] = False
        if len(_content) == 0:
            url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                          f"/requests/{test_data['housekeepingCrew']['CabinHostRequestId']}"
                          f"/assign/{test_data['housekeepingCrew']['UserCabinHostSecond']}")
            body = {
                "userId": test_data['housekeepingCrew']['UserCabinHostSecond']
            }
            rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
            test_data['requestReadyToStart'] = True
        else:
            _content = _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            for _request in _content:
                is_key_there_in_dict('status', _request)
                is_key_there_in_dict('reservationGuestId', _request)
                is_key_there_in_dict('reservationId', _request)
                is_key_there_in_dict('publicId', _request)
                is_key_there_in_dict('priority', _request)
                assert 'pending' == _request['status'], "Request Mismatched !! "
                if _request['publicId'] == test_data['housekeepingCrew']['requestId']:
                    test_data['requestReadyToStart'] = True
                    break

    @pytestrail.case(32465715)
    def test_47_assign_to_me_cta(self, config, test_data, rest_ship):
        """
        To assign to me cta for unassigned requests
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['requestReadyToStart']:
            pytest.skip(msg="Skipping, as the Runner is already having more than 2 request to work upon !!")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"/requests/{test_data['housekeepingCrew']['CabinHostRequestId']}"
                      f"/assign/{test_data['housekeepingCrew']['UserCabinHostSecond']}")
        body = {
            "userId": test_data['housekeepingCrew']['UserCabinHostSecond']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('publicId', _content)
        test_data['housekeepingCrew']['assign_publicId'] = _content['publicId']
        assert 'pending' == _content['status'], "Status matched !!"

    @pytestrail.case(32419828)
    def test_48_start_request_cabin_host_second(self, config, test_data, rest_ship):
        """
        Start request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['requestReadyToStart']:
            pytest.skip(msg="Skipping, as the Runner is already having more than 2 request to work upon !!")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['CabinHostRequestId']}/start")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        assert 'started' == _content['status'], "Request is not getting started !!"

    @pytestrail.case(32420455)
    def test_49_complete_request_cabin_host_second(self, config, test_data, rest_ship):
        """
        Complete the request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['requestReadyToStart']:
            pytest.skip(msg="Skipping, as the Runner is already having more than 2 request to work upon !!")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['CabinHostRequestId']}/complete")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('priority', _content)
        test_data['housekeepingCrew']['status'] = _content['status']
        assert 'completed' == _content['status'], "Request is not getting started !!"

    @pytestrail.case(32465716)
    def test_50_un_assign_deck_to_cabin_host_first(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [test_data['housekeepingCrew']['CabinHostFirst']]
        _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

    @pytestrail.case(32465717)
    def test_51_un_assign_deck_to_cabin_host_second(self, config, test_data, rest_ship):
        """
        Assign deck to crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [test_data['housekeepingCrew']['CabinHostSecond']]
        _content = rest_ship.send_request(method="DELETE", url=url, json=body, auth="crew").content

    @pytestrail.case(68321435)
    def test_52_login_angel_role(self, config, test_data, rest_ship):
        """
        Log in with Angel Role
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/username")
        body = {
            "userName": "Astar01",
            "password": "Test@1234",
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content)
        is_key_there_in_dict('tokenType', _content)
        test_data['housekeepingCrew']['angel_userId'] = _content['userId']

    @pytestrail.case(68321436)
    def test_53_pending_request_list(self, config, test_data, rest_ship):
        """
        To verify that Pending Requests are displayed after login through Angel Role
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "requests/search")
        body = {"limit": 200, "notCreatedBy": "auto", "status": "pending", "sortBy": "createdDesc",
                "voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for request in _content:
            if not request['status'] == 'pending':
                raise Exception("Incorrect Pending List")

    @pytestrail.case(68321437)
    def test_54_done_request_list(self, config, test_data, rest_ship):
        """
        To verify that Completed Requests are displayed after login through Angel Role
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "requests/search")
        body = {"limit": 200, "notCreatedBy": "auto", "status": "completed", "sortBy": "createdDesc",
                "voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for request in _content:
            if not request['status'] == 'completed':
                raise Exception("Incorrect Done List")

    @pytestrail.case(68321438)
    def test_55_create_request_angel_role(self, config, test_data, rest_ship):
        """
        To verify that New Request can be created by Angel Role
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests")
        body = {"priority": test_data['housekeepingCrew']['priority'],
                "requestType": test_data['housekeepingCrew']['categoryId'],
                "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
                "placeSectionId": test_data['housekeepingCrew']['placeSectionId'],
                "placeId": test_data['housekeepingCrew']['placeId'],
                "userId": test_data['housekeepingCrew']['angel_userId']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['housekeepingCrew']['angel_publicId'] = _content['publicId']
        assert _content['status'] == 'pending', "Request not created successfully"

    @pytestrail.case(1125005)
    def test_56_reassign_own_request(self, config, test_data, rest_ship):
        """
        To verify Crew can Reassign own Request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['angel_publicId']}/assign/"
                      f"{test_data['housekeepingCrew']['UserDeckManager']}")
        body = {"userId": test_data['housekeepingCrew']['UserDeckManager']}
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        except Exception as exp:
            if "No free slots to assign new request" in exp.args[0]:
                test_data['assign_request'] = False
                pytest.skip("Skipping this TC as no free slots available to assign new request")
            else:
                raise Exception(exp)
        assert _content['assignId'] == test_data['housekeepingCrew']['UserDeckManager'], \
            'Request not Assigned to the Deck Manager'
        test_data['assign_request'] = True
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['angel_publicId']}/forceAssign/"
                      f"{test_data['housekeepingCrew']['UserDeckManager']}")
        body = {"userId": test_data['housekeepingCrew']['UserDeckManager']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['assignId'] == test_data['housekeepingCrew']['UserDeckManager'], \
            'Request not Re-assigned to the Deck Manager'

    @pytestrail.case(760023)
    def test_57_start_reassign_request(self, config, test_data, rest_ship):
        """
        To verify Crew can Start Reassign Request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['assign_request']:
            pytest.skip("Skipping this TC as no free slots available to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['angel_publicId']}/start")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        assert _content['status'] == 'started', 'Request not Started'

    @pytestrail.case(1125006)
    def test_58_complete_reassign_request(self, config, test_data, rest_ship):
        """
        To verify that after reassignment deck manager/executive manager will be able to complete it
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['angel_publicId']}/complete")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        assert _content['status'] == 'completed', 'Request not Completed'

    @pytestrail.case(1080196)
    def test_59_assign_come_back_later_status(self, config, test_data, rest_ship):
        """
        To verify that crew can set the cabin status as come back later
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        slot_date = test_data['crew_framework']['currentDate']
        start_time = f"{slot_date[:10]} 00:00:00"
        end_time = f"{slot_date[:10]} 11:59:59"
        test_data['housekeepingCrew']['from_date'] = int(change_epoch_of_datetime(start_time) / 1000)
        test_data['housekeepingCrew']['to_date'] = int(change_epoch_of_datetime(end_time) / 1000)
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['housekeepingCrew']['comeBackLater'] = _content['comeBackLater']
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['AssignToMePublicId']}/comeBackLater")
        body = {"delay": 3600, "userId": test_data['housekeepingCrew']['UserDeckManager']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        assert test_data['housekeepingCrew']['comeBackLater'] < _content['comeBackLater'], \
            'Not assigned as Come Back later'

    @pytestrail.case(959404)
    def test_60_mark_dnd_status(self, config, test_data, rest_ship):
        """
        To verify that crew can change the cabin status as DND
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['housekeepingCrew']['dnd'] = _content['dnd']
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "cabinStatuses")
        body = {"placeIds": [test_data['housekeepingCrew']['placeId']], "status": "dnd", "shipCode": config.ship.code,
                "expiresAt": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        assert test_data['housekeepingCrew']['dnd'] < _content['dnd'], \
            'Not marked as DND'

    @pytestrail.case(937694)
    def test_61_un_mark_dnd_status(self, config, test_data, rest_ship):
        """
        To Verify that crew can remove the DND cabin status
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['housekeepingCrew']['dnd'] = _content['dnd']
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "cabinStatuses")
        body = {"placeIds": [test_data['housekeepingCrew']['placeId']], "status": None, "shipCode": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_date'], "to": test_data['housekeepingCrew']['to_date']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        assert test_data['housekeepingCrew']['dnd'] > _content['dnd'], \
            'DND cabin status not removed'

    @pytestrail.case(959406)
    def test_62_mark_please_service(self, config, test_data, rest_ship):
        """
        To verify that crew can change the cabin status as Please service
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "cabinStatuses")
        body = {"placeIds": [test_data['housekeepingCrew']['placeId']], "status": "please-service",
                "shipCode": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for request in _content:
            if not request['status'] == 'please-service':
                raise Exception("Please-Service not marked successfully")

    @pytestrail.case(959407)
    def test_63_un_mark_please_service(self, config, test_data, rest_ship):
        """
        To Verify that crew can remove the please service cabin status
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['housekeepingCrew']['Slots_availability']:
            pytest.skip("No free slots to assign new request")
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['AssignToMePublicId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        assert _content['cabinStatus'] == 'please-service', "Cabin Status already in non Please-Service State"
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "cabinStatuses")
        body = {"placeIds": [test_data['housekeepingCrew']['placeId']], "status": None, "shipCode": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['AssignToMePublicId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        assert _content['cabinStatus'] == None, "Please Service cabin status not removed"

    @pytestrail.case(1125007)
    def test_64_refill_mini_bar(self, config, test_data, rest_ship):
        """
        To Refill Mini Bar Request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "requests/record")
        body = {"recordType": "MiniBarRefill", "createdBy": test_data['housekeepingCrew']['UserDeckManager'],
                "placeId": test_data['housekeepingCrew']['placeId'],
                "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
                "placeSectionId": test_data['housekeepingCrew']['placeSectionId']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(68853169)
    def test_65_cabins_not_cleaned_report(self, config, test_data, rest_ship):
        """
        To verify Cabins-Not-Cleaned reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "reports/cabins-not-cleaned-in-24h")
        params = {"placeDeckIds": test_data['housekeepingCrew']['placeDeckIds']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for report in _content:
                is_key_there_in_dict('teamMemberId', report)
        else:
            raise Exception('Cabins-Not-Cleaned reports not found')

    @pytestrail.case(722442)
    def test_66_get_housekeeping_dashboard(self, config, test_data, rest_ship):
        """
        To Verify that dashboard call is working fine
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        from_datetime = f"{test_data['crew_framework']['currentDate'][:11]}00:00:00"
        to_datetime = f"{test_data['debarkDate'][:10]} 05:59:59"
        test_data['housekeepingCrew']['from_epochtime'] = int(change_epoch_of_datetime(from_datetime)/1000)
        test_data['housekeepingCrew']['to_epochtime'] = int(change_epoch_of_datetime(to_datetime)/1000)
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "dashboard")
        params = {"deckIds": test_data['housekeepingCrew']['placeDeckIds'],
                  "from": test_data['housekeepingCrew']['from_epochtime'],
                  "to": test_data['housekeepingCrew']['to_epochtime']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content != 0:
            is_key_there_in_dict('occupiedCabins', _content)
            is_key_there_in_dict('overdue', _content)
            is_key_there_in_dict('atRisk', _content)
            is_key_there_in_dict('comeBackLater', _content)
            is_key_there_in_dict('dnd', _content)
        else:
            raise Exception('Dashboard call is not working')

    @pytestrail.case(68853170)
    def test_67_non_productive_time_reports(self, config, test_data, rest_ship):
        """
        To verify Non-Productive Time Reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        current_date = f"{test_data['crew_framework']['currentDate'][:10]}"
        today_date = datetime.today()
        one_month_ago = str(today_date - relativedelta(months=3)).split()[0]
        test_data['housekeepingCrew']['from_date'] = f"{one_month_ago[:10]}T18:30:00Z"
        test_data['housekeepingCrew']['to_date'] = f"{current_date}T18:29:59Z"
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "reports/non-productive-time")
        body = {
            "placeDeckIds": [test_data['housekeepingCrew']['placeDeckIds']],
            "teamMemberIds": [test_data['housekeepingCrew']['UserDeckManager']],
            "from": test_data['housekeepingCrew']['from_date'],
            "to": test_data['housekeepingCrew']['to_date']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for report in _content:
                is_key_there_in_dict('teamMemberId', report)
        else:
            raise Exception('Non-Productive Time Reports not found')

    @pytestrail.case(68853171)
    def test_68_queue_turned_off_reports(self, config, test_data, rest_ship):
        """
        To verify Queue-Turned-Off Reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "reports/queue-turned-off/custom")
        params = {
            "roleIds": [test_data['housekeepingCrew']['roleId']],
            "from": test_data['housekeepingCrew']['from_date'],
            "to": test_data['housekeepingCrew']['to_date']
            }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for report in _content:
                is_key_there_in_dict('teamMemberId', report)
        else:
            raise Exception('Queue-Turned-Off Reports not found')

    @pytestrail.case(26112978)
    def test_69_deck_assignment_multiple_deck_manager(self, config, test_data, rest_ship):
        """
        To verify that multiple deck managers should not be assigned to a single deck at a time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [{"placeSectionIds": [], "placeDeckIds": [test_data['housekeepingCrew']['placeDeckIds']],
                 "teamMemberId": test_data['housekeepingCrew']['UserDeckManager'],
                 "teamMemberRole": "DM", "date": test_data['crew_framework']['currentDate'][:10],
                 "dayPeriod": test_data['housekeepingCrew']['dayPeriod']}]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "teamMember/schedule/bulk")
        body = [{"placeSectionIds": [], "placeDeckIds": _content[0]['placeDeckIds'],
                 "teamMemberId": "a24c61f8-d981-402c-93a4-705564cb706d",
                 "teamMemberRole": "DM", "date": _content[0]['date'],
                 "dayPeriod": _content[0]['dayPeriod']}]
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            raise Exception('Multiple deck managers assigned to a single deck')
        except Exception as exp:
            if "Schedule already exists" in exp.args[0]:
                logger.info("Same deck not assigned to multiple deck managers")
                return

    @pytestrail.case(1125008)
    def test_70_custom_request_not_assigned_directly(self, config, test_data, rest_ship):
        """
        To verify that custom request created should not get assigned directly
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{"placeSectionIds": [test_data['housekeepingCrew']['placeDeckIds']],
                 "date": test_data['crew_framework']['currentDate'][:10],
                 "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
                 "teamMemberId": test_data['housekeepingCrew']['UserDeckManager'], "teamMemberRole":"DM",
                 "publicId": test_data['housekeepingCrew']['deck_managerpublicId'], "dxpPlaceDeckIds":[],
                 "placeDeckIds":[test_data['housekeepingCrew']['placeDeckIds']]}]
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        assert _content[0]['teamMemberId'] == test_data['housekeepingCrew']['UserDeckManager'], \
            'Deck is not assigned to Deck Manager'
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/teamMember/schedule/bulk")
        body = [{"placeSectionIds": [test_data['housekeepingCrew']['placeDeckIds']],
                 "date": test_data['crew_framework']['currentDate'][:10],
                 "dayPeriod": test_data['housekeepingCrew']['dayPeriod'],
                 "teamMemberId": test_data['housekeepingCrew']['UserCabinHostFirst'], "teamMemberRole": "CH",
                 "publicId": test_data['housekeepingCrew']['deck_managerpublicId'], "dxpPlaceDeckIds": [],
                 "placeDeckIds": [test_data['housekeepingCrew']['placeDeckIds']]}]
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        assert _content[0]['teamMemberId'] == test_data['housekeepingCrew']['UserCabinHostFirst'], \
            'Deck is not assigned to Runner Host'
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"), "/requests")
        body = {
            "priority": test_data['housekeepingCrew']['custom_priority'], "description": "Medical Testing",
            "requestType": test_data['housekeepingCrew']['customId'],
            "placeDeckId": test_data['housekeepingCrew']['placeDeckIds'],
            "placeSectionId": test_data['housekeepingCrew']['placeSectionId'],
            "placeId": test_data['housekeepingCrew']['placeId'],
            "guestId": test_data['housekeepingCrew']['guest']['guestId'],
            "reservationGuestId": test_data['housekeepingCrew']['guest']['reservationGuestId'],
            "reservationId": test_data['housekeepingCrew']['guest']['reservationId'],
            "userId": test_data['housekeepingCrew']['UserCabinHostFirst']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['housekeepingCrew']['custom_publicId'] = _content['publicId']
        assert _content['assignId'] == None, 'Custom Request Assigned Directly'

    @pytestrail.case(1125009)
    def test_71_deck_manager_send_custom_request_to_queue(self, config, test_data, rest_ship):
        """
        To verify that deck manager should be able to send custom request to queue
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.housekeeping"),
                      f"requests/{test_data['housekeepingCrew']['custom_publicId']}/resume")
        _content = rest_ship.send_request(method="POST", url=url, auth="crew").content
        assert _content['publicId'] == test_data['housekeepingCrew']['custom_publicId'], \
            'Deck Manager is not able to send custom request to queue'