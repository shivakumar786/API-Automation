__author__ = 'sarvesh.singh'

from virgin_utils import *
from datetime import timezone

@pytest.mark.SHIP
@pytest.mark.TABLE_MANAGEMENT
@pytest.mark.run(order=30)
class TestTableManagement:
    """
    Test Suite to Test Table Management module in Crew App
    """

    @pytestrail.case(729671)
    def test_01_login(self, config, rest_ship, guest_data, test_data):
        """
        To login to the App
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": guest_data[0]['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content

    @pytestrail.case(786608)
    def test_02_search_venues(self, config, test_data, rest_ship):
        """
        To search all available venues and retrieve venue details.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/sims/1/venues")
        response = rest_ship.send_request(method='GET', url=url, auth="crew").content
        name = "The Test Kitchen"
        for count in response:
            is_key_there_in_dict('name', count)
            is_key_there_in_dict('simId', count)
            is_key_there_in_dict('publicId', count)

            if count['name'] == name:
                test_data['tables'] = dict()
                test_data['tables']['venue'] = dict()
                test_data['tables']['venue']['venueId'] = count['venueId']
                test_data['tables']['venue']['venue_publicId'] = count['publicId']

    @pytestrail.case(911089)
    def test_03_validate_ship_time(self, config, test_data, rest_ship):
        """
        Get ship time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {
            'shipcode': config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-embarkation/shiptime")
        _content = rest_ship.send_request(method='GET', url=url, params=params, auth="crew").content
        test_data['tables'].update({'offset': _content['shipOffset'] * 60})
        epoch_time = int(datetime.now(tz=timezone.utc).timestamp())
        test_data['tables'].update({'epocTimestamp': epoch_time})
        test_data['tables'].update(
            {'current_date': str(
                datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + test_data['aci']['shipOffSet']).date())})

    @pytestrail.case(1575698)
    def test_04_check_current_sailing_availability(self, config, test_data, rest_ship):
        """
        To check the availability of Current sailing date
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['tables']['venue']['venue_publicId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"/deprecated/venues/{venue_id}/sailings/current")
        _response = rest_ship.send_request(method="GET", url=_url, auth="crew").content
        if _response[0]['sailing']['status'] == "current":
            print("current date available")
        else:
            raise Exception("ERROR: Current sailing date not available")
        test_data['tables'].update({'sailingId': _response[0]['sailing']['publicId']})
        test_data['tables'].update({'dateStart': _response[0]['sailing']['dateStart']})
        test_data['tables'].update({'dateEnd': _response[0]['sailing']['dateEnd']})
        test_data['tables'].update({'voyageNumber': _response[0]['sailing']['voyageNumber']})
        for count, guest in enumerate(_response[0]['settings']):
            if guest['date'] == test_data['tables']['current_date']:
                test_data['tables'].update({'publicId': guest['publicId']})
                break

    @pytestrail.case(28017793)
    def test_05_check_venues_available_for_booking(self, config, test_data, rest_ship):
        """
        To check the availability of venues for Current sailing date
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        test_data['tables']['virtualQueue'] = dict()
        test_data['tables']['available_bookings'] = False
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/sims/1/venues")
        response = rest_ship.send_request(method='GET', url=url, auth="crew").content
        name = ['Gunbae', 'Razzle Dazzle', 'The Wake', 'Extra Virgin', 'Pink Agave', 'The Test Kitchen']
        for venues in response:
            if venues['name'] in name:
                test_data['tables']['virtualQueue']['venueId'] = venues['publicId']
                vq_venue_id = venues['publicId']
                _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                               f'/deprecated/venues/{vq_venue_id}/sailings/current')
                _response = rest_ship.send_request(method="GET", url=_url, auth="crew").content
                is_key_there_in_dict("sailing", _response[0])
                is_key_there_in_dict('status', _response[0]['sailing'])
                test_data['tables']['virtualQueue']['sailing'] = _response[0]['sailing']
                if _response[0]['sailing']['status'] == "current":
                    for settings in _response[0]['settings']:
                        if not settings['sailorBookingAllowed']:
                            is_key_there_in_dict("publicId", settings)
                            is_key_there_in_dict("venueId", settings)
                            is_key_there_in_dict("sailingId", settings)
                            is_key_there_in_dict("isReady", settings)
                            is_key_there_in_dict("date", settings)
                            is_key_there_in_dict("newPresetId", settings)
                            is_key_there_in_dict("newPresetDayId", settings)
                            is_key_there_in_dict("data", settings)
                            test_data['tables']['virtualQueue']['publicIdForVq'] = settings['publicId']
                            test_data['tables']['virtualQueue']['venueId'] = settings['venueId']
                            test_data['tables']['virtualQueue']['sailingId'] = settings['sailingId']
                            test_data['tables']['virtualQueue']['isReady'] = settings['isReady']
                            test_data['tables']['virtualQueue']['date'] = settings['date']
                            test_data['tables']['virtualQueue']['newPresetId'] = settings['newPresetId']
                            test_data['tables']['virtualQueue']['newPresetDayId'] = settings['newPresetDayId']
                            test_data['tables']['virtualQueue']['basicData'] = settings['data']['basicData']
                            test_data['tables']['virtualQueue']['sessions'] = settings['data']['sessions']
                            test_data['tables']['virtualQueue']['mealTimes'] = settings['data']['mealTimes']
                            test_data['tables']['virtualQueue']['settingsTables'] = settings['data']['settingsTables']
                            test_data['tables']['virtualQueue']['seatingsAdvanced'] = settings['data'][
                                'seatingsAdvanced']
                            test_data['tables']['virtualQueue']['stations'] = settings['data']['stations']
                            test_data['tables']['available_bookings'] = True
                            return
        else:
            pytest.skip(msg="skipped, venues are not available for turning on virtual queue")

    @pytestrail.case(28143035)
    def test_06_enable_virtual_queue(self, config, test_data, rest_ship):
        """
        To verify enabling of virtual queue
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['available_bookings']:
            pytest.skip(msg="skipped, venues are not available for turning on virtual queue")
        vq_venue_id = test_data['tables']['virtualQueue']['publicIdForVq']
        test_data['tables']['virtualQueue']['sessions'][0]['name'] = 'Dinner'
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), f"deprecated/settings/{vq_venue_id}")
        body = {
            "publicId": test_data['tables']['virtualQueue']['publicIdForVq'],
            "venueId": test_data['tables']['virtualQueue']['venueId'],
            "sailingId": test_data['tables']['virtualQueue']['sailingId'],
            "isReady": test_data['tables']['virtualQueue']['isReady'],
            "date": test_data['tables']['virtualQueue']['date'],
            "sailorBookingAllowed": True,
            "newPresetId": test_data['tables']['virtualQueue']['newPresetId'],
            "newPresetDayId": test_data['tables']['virtualQueue']['newPresetDayId'],
            "basicData": test_data['tables']['virtualQueue']['basicData'],
            "sessions": test_data['tables']['virtualQueue']['sessions'],
            "mealTimes": test_data['tables']['virtualQueue']['mealTimes'],
            "settingsTables": test_data['tables']['virtualQueue']['settingsTables'],
            "seatingsAdvanced": test_data['tables']['virtualQueue']['seatingsAdvanced'],
            "stations": test_data['tables']['virtualQueue']['stations'],
            "sailing": test_data['tables']['virtualQueue']['sailing']
        }
        _content = rest_ship.send_request(method='PUT', url=_url, json=body, auth='crew')

    @pytestrail.case(28143036)
    def test_07_disable_virtual_queue(self, config, test_data, rest_ship):
        """
        To verify disabling of virtual queue
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['available_bookings']:
            pytest.skip(msg="skipped, venues are not available for turning on virtual queue")
        vq_venue_id = test_data['tables']['virtualQueue']['publicIdForVq']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), f"deprecated/settings/{vq_venue_id}")
        body = {
            "publicId": test_data['tables']['virtualQueue']['publicIdForVq'],
            "venueId": test_data['tables']['virtualQueue']['venueId'],
            "sailingId": test_data['tables']['virtualQueue']['sailingId'],
            "isReady": test_data['tables']['virtualQueue']['isReady'],
            "date": test_data['tables']['virtualQueue']['date'],
            "sailorBookingAllowed": False,
            "newPresetId": test_data['tables']['virtualQueue']['newPresetId'],
            "newPresetDayId": test_data['tables']['virtualQueue']['newPresetDayId'],
            "basicData": test_data['tables']['virtualQueue']['basicData'],
            "sessions": test_data['tables']['virtualQueue']['sessions'],
            "mealTimes": test_data['tables']['virtualQueue']['mealTimes'],
            "settingsTables": test_data['tables']['virtualQueue']['settingsTables'],
            "seatingsAdvanced": test_data['tables']['virtualQueue']['seatingsAdvanced'],
            "stations": test_data['tables']['virtualQueue']['stations'],
            "sailing": test_data['tables']['virtualQueue']['sailing']
        }
        _content = rest_ship.send_request(method='PUT', url=_url, json=body, auth='crew')

    @pytestrail.case(26137876)
    def test_08_get_available_reservation_times(self, config, test_data, rest_ship, guest_data):
        """
        To get the available timings for reservation
        :param test_data:
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/reservations/check")
        test_data['tables']['timeslots_length'] = False
        ship_date = test_data['aci']['shipTimeDate'].split('T')[0]
        test_data["ship_date"] = ship_date
        test_data['tables']['to'] = f"{ship_date}T23:59:59".replace('T', ' ')
        test_data['tables']['from'] = f"{ship_date}T00:00:00".replace('T', ' ')
        _data = {
            "check": {
                "sailingId": test_data['tables']['sailingId'],
                "from": test_data['tables']['from'],
                "to": test_data['tables']['to'],
                "reservationDetails": {
                    "highChair": False,
                    "wheelChair": False,
                    "status": "reservation",
                    "guestList": [
                        guest_data[0]['guestId']
                    ],
                    "reservationType": 0,
                    "partySize": 1
                }
            }
        }
        _response = rest_ship.send_request(method="POST", json=_data, url=_url, auth="crew").content
        if len(_response) > 0:
            is_key_there_in_dict('timeslots', _response[0])
            test_data['tables']['timeslots'] = _response[0]['timeslots']
            if len(test_data['tables']['timeslots']) <= 1:
                pytest.skip(msg='No another slot is available as it is the last slot of the day')
            for slot in reversed(range(len(test_data['tables']['timeslots']))):
                if test_data['tables']['timeslots'][slot]['timestamp'] > test_data['aci']['currentDate']:
                    if test_data['tables']['timeslots'][slot - 1]['timestamp'] > test_data['aci']['currentDate']:
                        test_data['tables']['epocTimestamp'] = test_data['tables']['timeslots'][slot]['timestamp']
                        test_data['tables']['edit_epocTimestamp'] = test_data['tables']['timeslots'][slot - 1][
                            'timestamp'].replace('T', ' ')
                        test_data['tables']['timeslots_length'] = True
                        break
            else:
                pytest.skip("No 2 slots are having future time stamp.")
        else:
            pytest.skip(msg="no slots are available at this time for reservation")

    @pytestrail.case(729672)
    def test_09_add_reservations(self, config, test_data, rest_ship, guest_data):
        """
        To Add reservations of guests for the venue
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="no slots available to add reservation")
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/reservations")
        body = {
            "venueId": test_data['tables']['venue']['venue_publicId'],
            "sailingId": test_data['tables']['sailingId'],
            "mainGuestId": guest_data[0]['reservationGuestId'],
            "guestList": [], "anonymosGuests": 0, "reservationType": 0,
            "timestamp": test_data['tables']['epocTimestamp'],
            "requests": [], "preferences": [], "allergies": [], "wheelChair": False, "highChair": False,
            "tableIds": [],
            "status": "reservation",
            "guestsDetails": [{"id": guest_data[0]['reservationGuestId'], "preferences": []}],
            "waitList": False,
            "waitlistDelay": None
        }
        _content = rest_ship.send_request(method='POST', url=url, json=body, auth="crew").content
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('tableId', _content)
        is_key_there_in_dict('externalId', _content)
        is_key_there_in_dict('tableIds', _content)
        test_data['tables']['reservation_publicID'] = _content['publicId']
        test_data['tables']['tableId'] = _content['tableId']
        test_data['tables']['externalId'] = _content['externalId']
        test_data['tables']['tableIds'] = _content['externalId']

    @pytestrail.case(786609)
    def test_10_search_guest_reservation(self, config, test_data, rest_ship, guest_data):
        """
        Search the Guest for reservation created
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="no slots available to add reservation")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/reservations/search")
        _body = {
            "sailingId": test_data['tables']['sailingId'],
            "from": f"{test_data['ship_date']}T00:00:00",
            "to": f"{test_data['ship_date']}T23:59:59",
            "guestIds": [guest_data[0]['reservationGuestId']]
        }
        _content = rest_ship.send_request(method='POST', url=_url, json=_body, auth="crew").content
        if len(_content) == 0:
            raise Exception("Reservation did not got booked in Table Management")

    @pytestrail.case(10355319)
    def test_11_edit_reservation(self, config, test_data, rest_ship, guest_data):
        """
        To Edit booked reservation
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                      f"deprecated/reservations/{test_data['tables']['reservation_publicID']}")
        body = {
            "venueId": test_data['tables']['venue']['venue_publicId'],
            "sailingId": test_data['tables']['sailingId'],
            "mainGuestId": guest_data[0]['reservationGuestId'],
            "guestList": [],
            "tableMinPartySize": 0,
            "tableSize": 0,
            "tables": [],
            "waitList": False,
            "waitlistDelay": None,
            "externalId": test_data['tables']['externalId'],
            "anonymosGuests": 0,
            "reservationType": 0,
            "timestamp": test_data['tables']['edit_epocTimestamp'],
            "requests": [], "preferences": [], "allergies": [], "wheelChair": False, "highChair": False,
            "tableId": None,
            "status": "upcoming",
            "autoAssigned": False, "draftId": None, "lastNotificationTime": None,
            "guestsDetails": [{"id": guest_data[0]['reservationGuestId'], "preferences": []}],
            "created": test_data['tables']['epocTimestamp'],
            "publicId": test_data['tables']['reservation_publicID'],
            "seated": None,
            "seatedGuests": [],
            "tableIds": [],
            "tableMaxPartySize": 0,
            "bookedByType": "crew",
            "bookedBy": "2498b407-9ba0-4b4a-8e09-368e4f3b0a18",
            "createdBy": "dcfe0bd8-64ff-11e9-bc39-0a1a4261e962",
            "modifiedBy": "dcfe0bd8-64ff-11e9-bc39-0a1a4261e962"
        }
        _content = rest_ship.send_request(method='PUT', url=url, json=body, auth="crew").content
        is_key_there_in_dict('tableIds', _content)
        test_data['tables']['tableIds'] = _content['tableIds']
        assert test_data['tables']['tableId'] == _content['tableId'], "tableId Mismatched !!"
        assert "upcoming" == _content['status'], "Status is not upcoming even after editing the Reservation"

    @pytestrail.case(26137878)
    def test_12_delete_reservation(self, config, test_data, rest_ship):
        """
        Delete the booked reservation
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="due to non availability of slots no booking done so skipped this tc")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"/deprecated/reservations/{test_data['tables']['reservation_publicID']}/cancel")
        _content = rest_ship.send_request(method='POST', url=_url, auth="crew").content
        if _content['status'] != 'cancelled':
            raise Exception("Reservation booked for table management did not got deleted")

    @pytestrail.case(786610)
    def test_13_search_table(self, config, test_data, rest_ship):
        """
        Search the Table reservation details created for the Guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"deprecated/v2/reservations/searchWithTables")
        _body = {
            "sailingId": test_data['tables']['sailingId'],
            "venueId": test_data['tables']['venue']['venue_publicId'],
            "from": f"{test_data['aci']['shipDate']}T00:00:00",
            "to": f"{test_data['aci']['shipDate']}T23:59:59",
            "guestIds": [],
            "tableId": test_data['tables']['tableId'],
            "statusIds": ["upcoming", "waitlist"],
            "type": "open"
        }
        _content = rest_ship.send_request(method='POST', url=_url, json=_body, auth="crew").content

    @pytestrail.case(10355320)
    def test_14_add_walk_in(self, config, test_data, rest_ship, guest_data):
        """
        To add walk-in
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/reservations")
        body = {
            "mainGuestId": guest_data[0]['reservationGuestId'],
            "guestList": [],
            "anonymosGuests": 0,
            "reservationType": 0,
            "timestamp": None,
            "requests": [],
            "preferences": [],
            "allergies": [],
            "wheelChair": False,
            "highChair": False,
            "tableIds": [],
            "sailingId": test_data['tables']['sailingId'],
            "venueId": test_data['tables']['venue']['venue_publicId'],
            "status": "waitlist",
            "guestsDetails": [{"id": guest_data[0]['reservationGuestId'], "preferences": []}],
            "waitlistDelay": 30,
            "waitList": True
        }
        _content = rest_ship.send_request(method='POST', url=url, json=body, auth="crew").content
        is_key_there_in_dict('publicId', _content)
        test_data['tables']['walkInPublicId'] = _content['publicId']
        assert "waitlist" == _content['status'], "Waitlist Mismatched !!"

    @pytestrail.case(25457259)
    def test_15_delete_walk_in(self, config, test_data, rest_ship):
        """
        Delete the walk in
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"/deprecated/reservations/{test_data['tables']['walkInPublicId']}/cancel")
        _content = rest_ship.send_request(method='POST', url=_url, auth="crew").content
        if _content['status'] != 'cancelled':
            raise Exception("Walk in did not got deleted")

    @pytestrail.case(25230864)
    def test_16_operational_hours(self, config, test_data, rest_ship):
        """
        Get operational hours
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"deprecated/venues/{test_data['tables']['venue']['venue_publicId']}/sailings/current/operation-hours")
        _content = rest_ship.send_request(method='GET', url=_url, auth="crew").content
        for _schedule in _content:
            is_key_there_in_dict("status", _schedule)
            is_key_there_in_dict("dateStart", _schedule)
            is_key_there_in_dict("dateEnd", _schedule)
            test_data['tables']['dateStart'] = _schedule['dateStart']
            test_data['tables']['dateEnd'] = _schedule['dateEnd']

    @pytestrail.case(26137877)
    def test_17_check_next_voyage_sailing_availability(self, config, test_data, rest_ship):
        """
        To check the availability of Current sailing date
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        venue_id = test_data['tables']['venue']['venue_publicId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"/deprecated/venues/{venue_id}/sailings")
        _content = rest_ship.send_request(method="GET", url=_url, auth="crew").content
        saillings_sorted = sorted(_content, key=lambda i: i['sailing']['dateStart'])
        for _sailing in saillings_sorted:
            if _sailing['sailing']['dateStart'] >= test_data['debarkDate']:
                is_key_there_in_dict('publicId', _sailing['sailing'])
                is_key_there_in_dict('dateStart', _sailing['sailing'])
                is_key_there_in_dict('dateEnd', _sailing['sailing'])
                is_key_there_in_dict('voyageNumber', _sailing['sailing'])
                is_key_there_in_dict('name', _sailing['sailing'])
                test_data['tables']['upcoming_publicId'] = _sailing['sailing']['publicId']
                test_data['tables']['upcoming_sailingId'] = _sailing['settings'][0]['sailingId']
                test_data['tables']['upcoming_venueId'] = _sailing['settings'][0]['venueId']
                test_data['tables']['upcoming_dateStart'] = _sailing['sailing']['dateStart']
                test_data['tables']['upcoming_dateEnd'] = _sailing['sailing']['dateEnd']
                test_data['tables']['upcoming_voyageNumber'] = _sailing['sailing']['voyageNumber']
                test_data['tables']['upcoming_name'] = _sailing['sailing']['name']
                test_data['tables']['PublicId_sailing_Id'] = _sailing['settings'][0]['publicId']
                break
            if _sailing['settings'][1]["newPresetId"] == 0:
                raise Exception("No preset is applied to upcoming voyage")

    @pytestrail.case(729670)
    def test_18_table_layout(self, config, test_data, rest_ship):
        """
        To create the Layout for table settings
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        _name = f"Dazzle {generate_random_alpha_numeric_string(length=3)}"
        test_data['tables'].update({'layout_name': _name})
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"/deprecated/settings/{test_data['tables']['PublicId_sailing_Id']}/layouts")
        _data = {
            "name": "script_automation",
            "isDefault": False
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=_data, auth="crew").content
        is_key_there_in_dict('publicId', _content)
        test_data['tables'].update({'layoutId': _content['publicId']})

    @pytestrail.case(786611)
    def test_19_add_tables(self, config, test_data, rest_ship):
        """
        To add table in layout
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        layout_id = test_data['tables']['layoutId']
        x = generate_random_number(low=0, high=999, include_all=True)
        y = generate_random_number(low=0, high=999, include_all=True)
        table_number = generate_random_number(low=1, high=20, include_all=True)
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"deprecated/settings/{test_data['tables']['PublicId_sailing_Id']}/layouts/{layout_id}/tables")
        _data = {
            "shapeId": "rect",
            "tableSize": 4,
            "x": x,
            "y": y,
            "layoutId": layout_id,
            "name": f"{table_number}",
            "reservationType": 0,
            "isMultiparty": False,
            "isAccessible": False,
            "isBlocked": False,
            "angle": 0,
            "type": "base",
            "rating": 1,
            "highChair": False,
            "newTable": True
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=_data, auth="crew").content
        is_key_there_in_dict('publicId', _content)
        test_data['tables'].update({'tableId': _content['publicId']})

    @pytestrail.case(26137879)
    def test_20_delete_layout(self, config, test_data, rest_ship):
        """
        To add table in layout
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="skipped this tc because we got less than two slots")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'),
                       f"deprecated/settings/{test_data['tables']['PublicId_sailing_Id']}/layouts/{test_data['tables']['layoutId']}")
        _content = rest_ship.send_request(method="DELETE", url=_url, auth="crew").content

    @pytestrail.case(41704354)
    def test_21_guest_preferences(self, config, test_data, rest_ship):
        """
        To get guest preferences
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "deprecated/guest-preferences")
        _body = ["ALLERGEN", "DISABILITY", "DIETARY"]
        _content = rest_ship.send_request(method="POST", json=_body, url=_url, auth="crew").content
        if len(_content) != 0:
            for preferences in _content:
                is_key_there_in_dict('type', preferences)
                is_key_there_in_dict('value', preferences)
                is_key_there_in_dict('code', preferences)
                if preferences['type'] == "ALLERGEN":
                    test_data['tables']["allergen"] = preferences
                elif preferences['type'] == "DISABILITY":
                    test_data['tables']["disability"] = preferences
                elif preferences['type'] == "DIETARY":
                    test_data['tables']["dietary"] = preferences
                else:
                    raise Exception("preference nto matching with given type!!")
        else:
            raise Exception("No preference data found!!")
        is_key_there_in_dict('allergen', test_data['tables'])
        is_key_there_in_dict('disability', test_data['tables'])
        is_key_there_in_dict('dietary', test_data['tables'])

    @pytestrail.case(41704355)
    def test_22_add_reservations_with_preferences(self, config, test_data, rest_ship, guest_data):
        """
        To Add reservations with preferences
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['tables']['timeslots_length']:
            pytest.skip(msg="no slots available to add reservation")
        url = urljoin(getattr(config.ship.contPath, 'url.path.tablemanagement'), "/deprecated/reservations")
        body = {
            "venueId": test_data['tables']['venue']['venue_publicId'],
            "sailingId": test_data['tables']['sailingId'],
            "mainGuestId": guest_data[0]['reservationGuestId'],
            "guestList": [], "anonymosGuests": 0, "reservationType": 0,
            "timestamp": test_data['tables']['epocTimestamp'],
            "requests": [], "preferences": [], "allergies": [], "wheelChair": True, "highChair": False,
            "tableIds": [],
            "status": "reservation",
            "guestsDetails": [{"id": guest_data[0]['reservationGuestId'], "preferences": [
                test_data['tables']["allergen"], test_data['tables']["dietary"]],
                               "specialNeeds": [{"code": test_data['tables']["disability"]["code"]}]}],
            "waitList": False,
            "waitlistDelay": None
        }
        _content = rest_ship.send_request(method='POST', url=url, json=body, auth="crew").content
        is_key_there_in_dict('publicId', _content)
        is_key_there_in_dict('tableId', _content)
        is_key_there_in_dict('externalId', _content)
        is_key_there_in_dict('tableIds', _content)
        is_key_there_in_dict('guestsDetails', _content)
        assert len(_content['guestsDetails']) != 0, "No guest data found!!"
        for guestsDetails in _content['guestsDetails']:
            is_key_there_in_dict('id', guestsDetails)
            is_key_there_in_dict('preferences', guestsDetails)
            is_key_there_in_dict('specialNeeds', guestsDetails)
            assert len(guestsDetails['preferences']) != 0, "No preferences data found!!"
            assert len(guestsDetails['specialNeeds']) != 0, "No special needs data found!!"
