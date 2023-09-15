__author__ = 'sarvesh.singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.TRACKABLE_SHP
@pytest.mark.run(order=21)
class TestShipTrackable:
    """
    Verify Trackable Ship Side
    """

    @pytestrail.case(4351197)
    def test_01_validate_hydration_iam_token(self, config, rest_ship):
        """
        Test IAM Token is Generated with Hydration IAM Token
        :param config:
        :param rest_ship:
        :return:
        """
        headers = {"Authorization": f"Basic {config.hydration}"}
        params = {"grant_type": "client_credentials"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'), 'oauth/token')
        _content = rest_ship.send_request(method='POST', url=url, params=params, headers=headers, auth=None).content
        is_key_there_in_dict('access_token', _content)
        is_key_there_in_dict('token_type', _content)
        is_key_there_in_dict('tokenType', _content)
        is_key_there_in_dict('scope', _content)
        is_key_there_in_dict('expires_in', _content)

    @pytestrail.case(720228)
    def test_02_trackable_lookup(self, config, rest_ship):
        """
        Check Trackable is available on Ship
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "lookup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
        is_key_there_in_dict('filters', _content)
        is_key_there_in_dict('decks', _content['filters'])
        is_key_there_in_dict('loyaltyLevels', _content['filters'])
        is_key_there_in_dict('cabinTypes', _content['filters'])
        is_key_there_in_dict('cabinRange', _content['filters'])

    @pytestrail.case(507104)
    def test_03_get_embark_debark_dates_for_trackables(self, config, test_data, rest_ship):
        """
        Fetch Embark and Debark Date for Trackables on active voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['trackable'] = dict()
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "voyages")
        _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
        is_key_there_in_dict('voyages', _content)
        for _voyage in _content['voyages']:
            if _voyage['isActive'] is True:
                test_data['trackable']['activeVoyage'] = _voyage
                test_data['trackable']['activeVoyage']['embarkdate'] = _voyage['embarkDate']
                test_data['trackable']['activeVoyage']['debarkdate'] = _voyage['debarkDate']
                break
        else:
            raise Exception('There is no active voyage in the system !!')

    @pytestrail.case(125)
    def test_04_check_basic_search(self, config, test_data, rest_ship):
        """
        Check the basic search functionality
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "/guests/search/basic")
        params = {
            'embarkDate': test_data['trackable']['activeVoyage']['embarkdate'],
            'debarkDate': test_data['trackable']['activeVoyage']['debarkdate'],
            'query': test_data['cabinNumber']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="bearer").content
        is_key_there_in_dict('guests', _content)
        for _guests in _content['guests']:
            is_key_there_in_dict('name', _guests)
            is_key_there_in_dict('cabinNumber', _guests)
            is_key_there_in_dict('reservationGuestId', _guests)

    @pytestrail.case(720229)
    def test_05_get_unassigned_not_printed_trackables_from_active_voyage(self, config, test_data, rest_ship,
                                                                         guest_data):
        """
        searching the active Voyage Guest details is available or not
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "pending/printing/search")
        body = {
            "embarkDate": test_data['trackable']['activeVoyage']['embarkdate'],
            "debarkDate": test_data['trackable']['activeVoyage']['debarkdate']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="bearer").content
        test_data['trackable']['trackable'] = []
        for _guest in guest_data:
            name = f"{_guest['FirstName']} {_guest['LastName']}"
            cabin_number = test_data['cabinNumber']
            res_id = _guest['reservationGuestId']
            test_data['trackable']['trackable'].append(
                {"name": name, 'cabinNumber': cabin_number, 'reservationGuestId': res_id})

    @pytestrail.case(725649)
    def test_06_print_trackable(self, config, test_data, rest_ship):
        """
        Print Trackable for guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "print")
        for trackable in test_data['trackable']['trackable']:
            body = {
                "reservationGuestIds": trackable['reservationGuestId'],
                "embarkDate": test_data['trackable']['activeVoyage']['embarkdate'],
                "debarkDate": test_data['trackable']['activeVoyage']['debarkdate']
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="bearer").content

    @pytestrail.case(22812176)
    def test_07_get_unique_rf_id_not_assigned_to_any_guest(self, config, test_data, rest_ship, guest_data):
        """
        Get RFID that is not assigned to any guest
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.hydration'), "trackablehosts")
        test_data['trackable']['beacons'] = []
        for _guests in guest_data:
            rf_id = str(generate_random_number(low=0, high=99999999, include_all=True))
            while True:
                params = {"trackableId": rf_id, "trackableIdType": "rfId"}
                try:
                    _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
                    rf_id = str(generate_random_number(low=0, high=99999999, include_all=True))
                except (Exception, ValueError):
                    logger.debug(f"RF-ID {rf_id} is free to be assigned ...")
                    break

            major = generate_random_number(low=0, high=99, include_all=True)
            minor = generate_random_number(low=0, high=99, include_all=True)
            uu_id = generate_guid()
            beacon_id = f"{uu_id}:{major}:{minor}"
            test_data['trackable']['beacons'].append({
                "major": major, "minor": minor, "rf_id": rf_id, "uu_id": uu_id, "beacon_id": beacon_id,
                "host_id": _guests['reservationGuestId']
            })

    @pytestrail.case(725650)
    def test_08_assign_trackable_to_guest(self, config, test_data, rest_ship, guest_data):
        """
        Assign Trackable To Guest
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "assign")
        for count in range(0, len(guest_data)):
            rf_id = str(generate_random_number(low=0, high=99999999, include_all=True))
            while True:
                params = {"trackableId": rf_id, "trackableIdType": "rfId"}
                try:
                    _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
                    rf_id = str(generate_random_number(low=0, high=99999999, include_all=True))
                except (Exception, ValueError):
                    logger.debug(f"RF-ID {rf_id} is free to be assigned ...")
                    break

            _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "assign")
            beacon = test_data['trackable']['beacons'][count]
            body = {"reservationGuestId": beacon['host_id'], "rfId": rf_id}
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="bearer").content

    @pytestrail.case(507105)
    def test_09_ship_guest_data(self, config, test_data, rest_ship):
        """
        Get Trackable details To Search Shore Side Using reservationGuestId
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "guest")
        found = False
        for beacon in test_data['trackable']['beacons']:
            params = {"reservationGuestId": beacon['host_id']}
            _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="bearer").content
            is_key_there_in_dict('guest', _content)
            assert _content['guest']['reservationGuestId'] == beacon['host_id'], "Reservation ID Mismatch !!"
            assert _content['guest']['isTrackableAssigned'] is True, "Trackable not assigned !!"
            is_key_there_in_dict('partyMembers', _content)
            for member in _content['partyMembers']:
                if not member['isMinor']:
                    if member['isTrackableAssigned']:
                        found = True
        if found is False:
            raise Exception('Trackable did not get assigned !!')

    @pytestrail.case(507107)
    def test_10_un_assign_trackable_printing(self, config, test_data, rest_ship):
        """
        Ship Print New Trackable
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "print")
        for beacon in test_data['trackable']['beacons']:
            body = {
                "reservationGuestId": beacon['host_id'],
                "embarkDate": test_data['embarkDate'],
                "debarkDate": test_data['debarkDate']
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="bearer").content

    @pytestrail.case(507106)
    def test_11_ship_guest_un_assign_trackable(self, config, test_data, rest_ship):
        """
        Un-Assign Trackable
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        for beacon in test_data['trackable']['beacons']:
            host_id = beacon['host_id']
            _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'),
                           f"guest/{host_id}/trackable")
            _content = rest_ship.send_request(method="DELETE", url=_url, auth="bearer").content

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(507108)
    def test_12_assign_new_trackable_to_guest_when_damaged(self, config, test_data, rest_ship):
        """
        Assign New Trackable to Guest when Damaged
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['virginUuid'] = get_all_trackables(config, rest_ship)
        for count, beacon in enumerate(test_data['trackable']['beacons']):
            rf_id = str(generate_random_number(low=0, high=99999999, include_all=True))
            major = generate_random_number(low=0, high=99, include_all=True)
            minor = generate_random_number(low=0, high=99, include_all=True)
            uu_id = test_data['virginUuid']
            _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "trackables")
            body = {
                "isDamaged": True, "isLost": False, "isDeleted": False, "rfId": rf_id, "major": major, "minor": minor,
                "uuid": uu_id
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
            test_data['trackable']['beacons'][count]['beacon_id'] = _content['beaconId']
            test_data['trackable']['beacons'][count]['rf_id'] = _content['rfId']
            test_data['trackable']['beacons'][count]['uu_id'] = _content['uuid']
            test_data['trackable']['beacons'][count]['trackableId'] = _content['trackableId']

            _url = urljoin(getattr(config.ship.contPath, 'url.path.trackablemanagementbff'), "assign")
            body = {"reservationGuestId": beacon['host_id'], "rfId": _content['rfId']}
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content

    @pytestrail.case(32174392)
    def test_13_get_printing_templates(self, config, test_data, rest_ship):
        """
        Get Printing Templates
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "/fcstask-service/templates")
        _content = rest_ship.send_request(method="GET", url=_url, auth=None).content
        if len(_content) != 0:
            test_data['fcsTaskService'] = dict()
            for template in _content:
                is_key_there_in_dict('id', template)
                is_key_there_in_dict('name', template)
                is_key_there_in_dict('type', template)
                if template['type'] == 'tray':
                    test_data['fcsTaskService']['tray'] = template['name']
                if template['type'] == 'trackable':
                    test_data['fcsTaskService']['template'] = template['name']
        else:
            raise Exception("No print template Found!!")

    @pytestrail.case(32174393)
    def test_14_print_trackable(self, config, test_data, rest_ship):
        """
        Print Trackable
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "/fcstask-service/print/queue/")
        _body = {
            "template": test_data['fcsTaskService']['template'], "tray": test_data['fcsTaskService']['tray'],
            "items": [
                {
                    "orderId": generate_guid(),
                    "items": [
                        {
                            "hostId": test_data['shipside_guests'][0]['reservationguestid'],
                            "text": {
                                "caption7": "A3",
                                "caption6": "1(866)234-7350",
                                "caption1": "Rosemarie",
                                "caption5": "BLISS",
                                "caption4": "01/12/2019",
                                "caption3": "Mphfnlcpiq"
                            }
                        }
                    ]
                }
            ],
            "space": "0"
        }
        rest_ship.send_request(method="POST", url=_url, json=_body, auth=None)

    @pytest.mark.skip(reason='DCP-89688')
    @pytestrail.case(32174394)
    def test_15_verify_printed_trackable(self, config, test_data, rest_ship):
        """
        Verify Printed Trackable
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "/fcstask-service/print/queue/")
        _content = rest_ship.send_request(method="GET", url=_url, auth=None).content
        if len(_content) != 0:
            _status = False
            for template in _content:
                is_key_there_in_dict('id', template)
                is_key_there_in_dict('hostIds', template)
                is_key_there_in_dict('status', template)
                for host in template['hostIds']:
                    if host == test_data['shipside_guests'][0]['reservationguestid']:
                        _status = True
            assert _status, "Trackable not printed successfully!!"
        else:
            raise Exception("No Printed Trackable Found!!")
