__author__ = 'anshuman.goyal'
__maintainer__ = 'piyush.kumar'

import json
from virgin_utils import *


@pytest.mark.CHECKIN_ONBORD
@pytest.mark.SHIP
@pytest.mark.CREW_FRAMEWORK
@pytest.mark.run(order=11)
class TestCrewFramework:
    """
    Test Suite to test Crew Framework

    """

    @pytestrail.case(12758859)
    def test_01_prepare_ship_side_data(self, test_data, guest_data):
        """
        Prepare Test Bed for ship side
        :param test_data:
        :param guest_data:
        :return:
        """

        with open('guest_data_shore.json', 'w') as _fp:
            _fp.write(json.dumps(guest_data, default=lambda o: o.__dict__, indent=2, sort_keys=True))
        with open('test_data_shore.json', 'w') as _fp:
            _fp.write(json.dumps(test_data, default=lambda o: o.__dict__, indent=2, sort_keys=True))
        del guest_data
        for items in ['signupGuest', 'voyages', 'voyage', 'cabin', 'paymentDetails']:
            if items in test_data:
                del test_data[items]

    @pytestrail.case(26111998)
    def test_02_crew_sign_up(self, config, test_data, rest_shore, guest_data, rest_ship, creds):
        """
        Register a User
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        first_name = generate_first_name(from_saved=True)
        last_name = generate_last_name(from_saved=True)
        test_data['username'] = generate_email_id(first_name=first_name, last_name=last_name)
        test_data['password'] = "Voyages@9876"
        test_data['appId'] = str(generate_guid()).upper()
        test_data['deviceId'] = str(generate_random_alpha_numeric_string(length=32)).lower()
        url = urljoin(config.ship.url, "user-account-service/signup")
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        body = {
            "birthDate": guest_data[0]['BirthDate'],
            "email": test_data['username'],
            "firstName": guest_data[0]['FirstName'],
            "userType": "guest",
            "preferredName": guest_data[0]['FirstName'],
            "lastName": guest_data[0]['LastName'],
            "password": test_data['password'],
            "enableEmailNewsOffer": False
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('authenticationDetails', _content)
        _token = _content['authenticationDetails']['accessToken']
        rest_shore.userToken = f"bearer {_token}"
        is_key_there_in_dict('accessToken', _content['authenticationDetails'])
        test_data['userToken'] = rest_shore.userToken
        test_data['guest_details'] = body

        _url = urljoin(config.ship.url, '/user-account-service/signin/username')
        body = {
            "userName": creds.verticalqa.username, "password": creds.verticalqa.password,
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body).content
        rest_shore.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

        url = urljoin(config.shore.url, "identityaccessmanagement-service/oauth/token")
        params = {"grant_type": "client_credentials"}
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="basic").content
        rest_ship.bearerToken = f"{_content['token_type']} {_content['access_token']}"

    @pytestrail.case(12758860)
    def test_03_get_data_shipboard(self, config, test_data, rest_shore, db_core):
        """
        Checking and fetching the guest details to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param db_core:
        :return:
        """
        # To get the voyage Id for our active voyage
        _ship = config.ship.url
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            if voyage['isActive']:
                test_data['embarkDate'] = voyage['embarkDate'].split('T')[0]
                test_data['debarkDate'] = voyage['debarkDate'].split('T')[0]
                test_data['voyageId'] = voyage['voyageId']
                test_data['voyageNumber'] = voyage['number']
                test_data['shipCode'] = voyage['shipCode']
                test_data['sailingPackageCode'] = voyage['sailingPackageCode']
                break
        else:
            raise Exception("There's no active voyage in system !!")

        test_data['shipside_guests'] = []
        _query = f"with cte as (SELECT reservationguestid, reservationid, guestid, isprimary, row_number() " \
                 f"over(partition by reservationid) AS rownum FROM public.reservationguest where embarkdate = " \
                 f"'{test_data['embarkDate']}' and debarkdate ='{test_data['debarkDate']}' and reservationstatuscode = '" \
                 f"RS' and stateroom!= 'GTY') select reservationguestid, reservationid, guestid, isprimary from cte " \
                 f"where reservationid in (select reservationid  from cte where rownum > 1);"
        _data = db_core.ship.run_and_fetch_data(query=_query)
        for _guests in _data:
            test_data['shipside_guests'].append({
                "reservationguestid": _guests['reservationguestid'],
                "reservationid": _guests['reservationid'],
                "isprimary": _guests['isprimary'],
                "guestid": _guests['guestid']
            })
        if len(test_data['shipside_guests']) == 0:
            raise Exception('No guest available on ship side for running E2E Ship Side')
        else:
            random.shuffle(test_data['shipside_guests'])

    @pytestrail.case(12758861)
    def test_04_get_guest_details_ship_side(self, config, test_data, rest_shore):
        """
        Fetching the guest details from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _ship = config.ship.url
        for guest in test_data['shipside_guests']:
            params = {"personid": guest['guestid']}
            _url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),
                           "/userprofiles/getuserdetails")
            _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="crew").content
            if len(_content) != 0 and True is guest['isprimary']:
                url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                              f"/guests/search/findbyreservationguests/{guest['reservationguestid']}")
                _content_findbyreservationguests = rest_shore.send_request(method="GET", url=url, auth="user").content
                if '@mailinator.com' in _content_findbyreservationguests['email']:
                    test_data['shipside_guests'].clear()
                    test_data['iam_user_id'] = _content['userId']
                    test_data['shipside_guests'].append(guest)
                    test_data['shipside_guests'][0]['email'] = _content_findbyreservationguests['email']
                    break

    @pytestrail.case(12758862)
    def test_05_get_guest_guest_id_ship_side(self, config, test_data, rest_shore, guest_data, db_iam):
        """
        Fetching the guest guestid from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param db_iam:
        :return:
        """
        guest = 0
        first_name = guest_data[guest]['FirstName']
        last_name = guest_data[guest]['LastName']
        gender_code = guest_data[guest]['GenderCode']
        birth_date = guest_data[guest]['BirthDate']
        citizenship = guest_data[guest]['CitizenshipCountryCode']

        guest_data.clear()

        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/reservationguests/search/findbyguestids")
        body = {"guestIds": [test_data['shipside_guests'][0]['guestid']]}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        _query = f"select * from public.userprofile where personid  = '{_content['_embedded']['reservationGuests'][0]['guestId']}';"
        _data = db_iam.ship.run_and_fetch_data(query=_query)
        guest_data.append({
            "reservationId": _content['_embedded']['reservationGuests'][0]['reservationId'],
            "reservationGuestId": _content['_embedded']['reservationGuests'][0][
                'reservationGuestId'],
            "guestId": _content['_embedded']['reservationGuests'][0]['guestId'],
            "email": _data[0]['email'],
            "FirstName": first_name,
            "LastName": last_name,
            "GenderCode": gender_code,
            "birthDate": birth_date,
            "CitizenshipCountryCode": citizenship
        })
        test_data['reservation_guest_ids'] = guest_data[0]['reservationGuestId']
        test_data['cabinNumber'] = _content['_embedded']['reservationGuests'][0]['stateroom']

    @pytestrail.case(12758863)
    def test_06_get_guest_reservation_ship_side(self, config, test_data, rest_shore, guest_data):
        """
        Fetching the guest reservation number from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"/reservations/{guest_data[0]['reservationId']}")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        test_data['reservationNumber'] = _content['reservationNumber']
        test_data['voyageId'] = _content['voyageNumber']

    @pytestrail.case(12758864)
    def test_07_get_user_profile(self, config, test_data, rest_shore):
        """
        Get User Profile
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/userprofile")
        _content = rest_shore.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('personId', _content)
        test_data['personId'] = _content['personId']

    @pytestrail.case(12758865)
    def test_08_get_guest_first_name(self, config, rest_shore, guest_data):
        """
        Get Guest First and last name
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f"/guests/{guest['guestId']}")
        _content = rest_shore.send_request(method="GET", url=url, auth="crew").content
        guest['FirstName'] = _content['firstName']
        guest['LastName'] = _content['lastName']
        guest['birthDate'] = _content['birthDate']

    @pytestrail.case(26112487)
    def test_09_get_secondary_guest(self, config, test_data, rest_shore, guest_data):
        """
        Get secondary guest
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      "/reservationevents/search/getguestsdetailbyreservationnumber")
        params = {
            "reservationnumber": test_data['reservationNumber']
        }
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['guestDetails']) == 0:
            raise Exception(f"0 guests returned for reservation number {test_data['reservationNumber']} !!")

        for _guest in _content['guestDetails']:
            if _guest['guestId'] != guest_data[0]['guestId']:
                guest_data.append({
                    "reservationId": guest_data[0]['reservationId'],
                    "reservationGuestId": _guest['reservationGuestId'],
                    "guestId": _guest['guestId'],
                    "email": _guest['email'],
                    "FirstName": _guest['firstName'],
                    "LastName": _guest['lastName'],
                    "birthDate": _guest['birthDate'],
                })

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(198)
    def test_10_crew_app_dashboard(self, config, rest_ship, test_data):
        """
        Get Crew App Dashboard Items
        :param config:
        :param rest_ship:
        :return:
        """
        test_data['crew_framework'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-dashboard/dashboard")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('profileImageUrl', _content)
        is_key_there_in_dict('isOnDuty', _content)
        is_key_there_in_dict('isDutyManager', _content)
        is_key_there_in_dict('voyageDetails', _content)
        is_key_there_in_dict('shiftDetails', _content)
        is_key_there_in_dict('currentDate', _content)
        test_data['crew_framework']['currentDate'] = _content['currentDate']
        current_date = change_epoch_time(datetime.today().date())
        for count, voyageItineraries in enumerate(_content['voyageDetails']['voyageItineraries']):
            if not voyageItineraries['isSeaDay']:
                try:
                    current_ship_date = change_epoch_time(voyageItineraries['arrivalTime'][:10])
                except Exception:
                    current_ship_date = change_epoch_time(voyageItineraries['departureTime'][:10])
                if current_date == current_ship_date:
                    test_data['crew_framework']['portCode'] = voyageItineraries['portCode']
                    test_data['crew_framework']['portName'] = voyageItineraries['portName']
                    break
            else:
                test_data['crew_framework']['portCode'] = ""
                test_data['crew_framework']['portName'] = "At Sea"
                break

    @pytestrail.case(247)
    def test_11_get_duty_statuses(self, config, rest_ship):
        """
        Get Duty Statuses
        :param config:
        :param rest_ship:
        :return:
        """
        # Get Manager on Duty
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-dashboard/dutystatus")
        params = {
            "isOnDuty": 'True',
            "isDutyManager": 'True'
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        # Check BFF Dashboard
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-dashboard/dashboard")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if not _content['isOnDuty']:
            raise Exception("Duty not updated successfully")
        if not _content['isDutyManager']:
            raise Exception("Duty Manager not updated successfully")

    @pytestrail.case(248)
    def test_12_get_inquiries_faqs(self, config, rest_ship):
        """
        Get Inquiries & FAQs
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-dashboard/inquiries/faq")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        for inquiry in _content:
            is_key_there_in_dict('name', inquiry)
            is_key_there_in_dict('sailorFaqs', inquiry)

    @pytestrail.case(41570495)
    def test_13_get_help_center_categories(self, config, rest_ship):
        """
        Get help center categories from crew dashboard
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.contentmanagement'), "/faqs/crew/categories")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        assert len(_content) != 0, "no data present for help center"

    @pytestrail.case(725646)
    def test_14_get_venue_and_operational_hours(self, config, test_data, rest_shore):
        """
        Get Venue and Operational Hours
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-dashboard/v1/venues')
        _content = rest_shore.send_request(method="GET", url=url, auth="crew").content
        for venueCategory in _content['categories']:
            is_key_there_in_dict('id', venueCategory)
            is_key_there_in_dict('name', venueCategory)
            is_key_there_in_dict('instanceName', venueCategory)
        for venue in _content['venues']:
            is_key_there_in_dict('globalVenueId', venue)
            is_key_there_in_dict('venueName', venue)
            is_key_there_in_dict('id', venue)
            is_key_there_in_dict('isVenueClosedToday', venue)
            is_key_there_in_dict('imageUrl', venue)
            is_key_there_in_dict('categoryId', venue)
            is_key_there_in_dict('venueId', venue)
            if 'operatingHours' in venue:
                for operationHour in venue['operatingHours']:
                    is_key_there_in_dict('weekday', operationHour)
                    is_key_there_in_dict('timesheet', operationHour)
                    for timeSheet in operationHour['timesheet']:
                        is_key_there_in_dict('from', timeSheet)
                        is_key_there_in_dict('to', timeSheet)
                        is_key_there_in_dict('isClosed', timeSheet)
        test_data['venueTypeId'] = _content['categories'][0]['id']
        test_data['venueId'] = _content['venues'][0]['venueId']

    @pytestrail.case(250)
    def test_15_get_venue_details(self, config, test_data, rest_shore):
        """
        Get Venue Details
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _venueTypeId = test_data['venueTypeId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-dashboard/venuedetails')
        params = {
            "venueTypeId": _venueTypeId
        }
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="crew").content
        for venueName in _content:
            is_key_there_in_dict('venueName', venueName)
            is_key_there_in_dict('isOpen', venueName)
            is_key_there_in_dict('deckNumber', venueName)

    @pytestrail.case(251)
    def test_16_get_lineup_info(self, config, test_data, rest_shore):
        """
        Get Lineup Info
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _voyageNo = test_data['voyageNumber']
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-dashboard/lineupinfo')
        body = {
            "startDate": test_data['embarkDate'],
            "endDate": test_data['debarkDate'],
            "voyageNumber": _voyageNo
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="crew")

    @pytestrail.case(1853)
    def test_17_user_account_startup(self, request, config, rest_shore):
        """
        Get user account startup details
        :param request:
        :param config:
        :param rest_shore:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath,
                             'test_data/verification_data/crew_framework_user_accounts.json')
        with open(_file, 'r') as _fp:
            _data = json.load(_fp)

        url = urljoin(config.ship.url, 'user-account-service/startup')
        _response = rest_shore.send_request(method="GET", url=url, auth="basic").content
        for _key in _data:
            is_key_there_in_dict(_key, _response)

    @pytestrail.case(26112977)
    def test_18_login(self, config, rest_shore, guest_data, test_data):
        """
        Guest Login
        :param config:
        :param rest_shore:
        :param guest_data:
        :param test_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/signin/email")
        body = {
            "userName": guest_data[0]['email'],
            "password": "Voyages@9876"
        }
        try:
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="Basic")
            test_data['guestPassword'] = 'Voyages@9876'
        except Exception as exp:
            if 'Bad credentials' in exp.args[0]:
                body['password'] = 'Voyages@9899'
                _content = rest_shore.send_request(method="POST", url=url, json=body, auth="Basic")
                test_data['guestPassword'] = 'Voyages@9899'
            else:
                raise Exception(exp.args[0])