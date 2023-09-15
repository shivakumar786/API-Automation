__author__ = 'Sarvesh.Singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.SAILOR_APP_SHIP
@pytest.mark.run(order=33)
class TestSailorApp:
    """
    Test Suite to Test Sailor App
    """

    @pytestrail.case(26137880)
    def test_01_start_up(self, config, test_data, rest_ship):
        """
        Get Links for all Services
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "user-account-service/startup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="Basic").content
        test_data.update(_content)

    @pytestrail.case(26112980)
    def test_02_login(self, config, test_data, guest_data, rest_ship):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        test_data['sailorApp'] = dict()
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

    @pytestrail.case(23750433)
    def test_03_update_reset_email(self, config, test_data, guest_data, rest_ship):
        """
        Update the email id and reset it in On-cruise mode
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        # updating email id
        guest = guest_data[0]
        original_email_id = guest['email']
        updated_email_id = generate_email_id(first_name=guest_data[0]['FirstName'], last_name=guest_data[0]['LastName'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/account/username")
        body = {
                "oldUserName": original_email_id,
                "newUserName": updated_email_id
                }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        test_data['sailorApp']['updated_email_ship'] = updated_email_id
        test_data['sailorApp']['original_email_ship'] = original_email_id
        guest_data[0]['email'] = updated_email_id

        # login with updated email
        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": test_data['sailorApp']['updated_email_ship'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        is_key_there_in_dict('accessToken', _content)
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

        # resetting the emailId to original one
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/account/username")
        body = {
            "oldUserName": test_data['sailorApp']['updated_email_ship'],
            "newUserName": test_data['sailorApp']['original_email_ship']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        test_data['sailorApp']['updated_email_ship'] = body["newUserName"]
        guest_data[0]['email'] = body["newUserName"]

        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": guest_data[0]['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

    @pytestrail.case(28231253)
    def test_04_access_to_cabin_mates_contacts(self, config, guest_data, rest_ship):
        """
        Deny / Allow cabin mate to see what you are attending
        :param config:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.guestbff"), "/messaging/contact/preferences")
        body_deny = {
            "personId": guest_data[0]['reservationGuestId'],
            "connectionPersonId": guest_data[1]['reservationGuestId'],
            "isEventVisibleCabinMates": False
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body_deny, auth="user").content
        body_allow = {
            "personId": guest_data[0]['reservationGuestId'],
            "connectionPersonId": guest_data[1]['reservationGuestId'],
            "isEventVisibleCabinMates": True
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body_allow, auth="user").content

    @pytestrail.case(26137881)
    def test_05_user_account_service(self, config, rest_ship):
        """
        Get Links for all Services
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "user-account-service/userprofile")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content

    @pytestrail.case(26137882)
    def test_06_get_wearable(self, config, request, rest_ship, guest_data):
        """
        Check if User is able to get wearable notification after log in
        :param config:
        :param request:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/sailorapp_wearable.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/wearable/delivery")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(26137883)
    def test_07_check_days_left_cabin(self, config, test_data, rest_ship, guest_data):
        """
        Check if User is able to get wearable notification after log in
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(12150706)
    def test_08_check_homecoming_guide_on_homepage(self, config, test_data, rest_ship, guest_data):
        """
        Check if User is able to get homecoming guide after log in
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if test_data['embarkDate'] == test_data['aci']['currentDate'].split("T")[0]:
            pytest.skip("Skipping as today is embarkation day")
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict("disembarkationHomecoming", _content)

    @pytestrail.case(26138349)
    def test_09_discovery_start_up(self, config, test_data, rest_ship):
        """
        Start Discovery
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/startup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('configurations', _content)
        test_data['configurations'] = _content['configurations']

    @pytestrail.case(26138837)
    def test_10_discover_landing(self, config, rest_ship, guest_data):
        """
        Discovery Landing
        :param config:
        :param rest_ship:
        :return:
        """
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), f"/discover/discover/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('discoverItems', _content)
        if "Lineup" != _content['discoverItems'][0]['title'] and "Ship" != _content['discoverItems'][1][
            'title'] and "Ports" != \
                _content['discoverItems'][2]['title'] and "Guides" != _content['discoverItems'][3]['title']:
            raise Exception("Not able to see the mandatory contents on discover landing page")

    @pytestrail.case(26139325)
    def test_11_discover_lineup_landing(self, config, rest_ship, guest_data):
        """
        Discovery Lineup Landing
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discover/lineup/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(26139326)
    def test_12_discover_ship_landing(self, config, rest_ship, guest_data):
        """
        Discovery Ship Landing
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discover/ship/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(26139327)
    def test_13_discover_guides_landing(self, config, request, rest_ship, guest_data):
        """
        Discovery Guides Landing
        :param config:
        :param request:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/discovery_guides.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discover/guides/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(26139328)
    def test_14_services_splash_screen(self, config, request, rest_ship, guest_data):
        """
        Check if the splash screen in services is getting displayed
        :param config:
        :param request:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/services_splash_screens.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        guest = guest_data[0]
        _res_id = guest['reservationId']
        _res_guest_id = guest['reservationGuestId']
        params = {
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "reservation-id": guest_data[0]['reservationId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/splashscreens/eats")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(26139329)
    def test_15_activity_reservation_resources(self, config, test_data, rest_ship):
        """
        Activity Reservation
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/resources")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['assets'] = _content['assets']

    @pytestrail.case(26140304)
    def test_16_get_port_code(self, config, test_data, rest_ship):
        """
        Get Port Code
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"reservation-number": test_data['reservationNumber']}
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/reservation/summary/")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="user").content

    @pytestrail.case(26140792)
    def test_17_ports_landing(self, config, rest_ship, guest_data, test_data):
        """
        Get Port Code
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discover/ports/landing")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="user").content
        for _port_code in _content['destinationCardCarousel']:
            is_key_there_in_dict('portCode', _port_code)
        test_data['sailorApp']['ship_port_details'] = dict()
        random_port = _content['destinationCardCarousel'][-1]
        test_data['sailorApp']['ship_port_details'] = random_port

    @pytestrail.case(26140793)
    def test_18_help_support_resource(self, config, test_data, rest_ship):
        """
        Help and support resource
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/help-support/resources")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['configurations'].update(_content['assets'])

    @pytestrail.case(26140794)
    def test_19_messaging_resource(self, config, test_data, rest_ship):
        """
        Message Resource
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/messaging/resources")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['configurations'].update(_content['assets'])

    @pytestrail.case(26140795)
    def test_20_my_voyage_dashboard(self, config, test_data, rest_ship, guest_data):
        """
        My Voyage Dash-Board
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/dashboard")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('stateroom', _content)
        is_key_there_in_dict('bookingStartDate', _content)
        is_key_there_in_dict('timeSlots', _content)
        is_key_there_in_dict('categories', _content)
        is_key_there_in_dict('shipCode', _content)
        test_data['configurations'].update(_content)

    @pytestrail.case(26140796)
    def test_21_user_account_service_user_profile(self, config, test_data, rest_ship):
        """
        User account Service and User Profile
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        _url = urljoin(_ship, "user-account-service/userprofile")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('firstName', _content)
        is_key_there_in_dict('bookingInfo', _content)
        is_key_there_in_dict('birthDate', _content)
        is_key_there_in_dict('email', _content)
        is_key_there_in_dict('isPasswordExist', _content)
        is_key_there_in_dict('personId', _content)
        is_key_there_in_dict('personTypeCode', _content)
        test_data['configurations'].update(_content)

    @pytestrail.case(26140797)
    def test_22_voyage_account_settings_lookup(self, config, test_data, rest_ship):
        """
        Voyage account settings lookup
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/lookup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('referenceData', _content)
        test_data['configurations'].update(_content)

    @pytestrail.case(26140798)
    def test_23_my_voyage_accounts_settings(self, config, request, test_data, rest_ship, guest_data):
        """
        My Voyage account settings
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :param request:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath,
                             'test_data/verification_data/my_voyage_accounts_setting.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "reservation-id": guest_data[0]['reservationId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(26150286)
    def test_24_voyage_account_setting_personal_info(self, config, test_data, rest_ship, guest_data):
        """
        Check if the first and last name is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _ship = config.ship.url
        _num = test_data['reservationNumber']
        _id = guest['reservationGuestId']
        _res_id = guest['reservationId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/personal")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if _content['firstName'] != guest['FirstName'] and _content['lastName'] != guest['LastName']:
            raise Exception("First and Last name is not matching under the personal information of Sailor App")

    @pytestrail.case(1065281)
    def test_25_user_logout(self, config, rest_ship):
        """
        Log out Sailor app
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(config.ship.url, "user-account-service/logout")
        _content = rest_ship.send_request(method="POST", url=_url, auth="user").content

    @pytestrail.case(26111999)
    def test_26_sign_up_connect_booking(self, config, test_data, rest_ship, guest_data):
        """
        Register a User
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        first_name = generate_first_name(from_saved=True)
        last_name = generate_last_name(from_saved=True)
        test_data['usernameConnect'] = generate_email_id(first_name=first_name, last_name=last_name)
        url = urljoin(config.ship.url, "user-account-service/signup")
        body = {
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "birthDate": guest['birthDate'],
            "email": test_data['usernameConnect'],
            "firstName": first_name,
            "userType": "guest",
            "lastName": last_name,
            "password": "Voyages@9876"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content['authenticationDetails'])
        rest_ship.userToken = test_data['userToken']

    @pytestrail.case(507101)
    def test_27_connect_booking(self, config, test_data, rest_ship, guest_data):
        """
        Connect a booking
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _ship = config.ship.url
        _res_num = test_data['reservationNumber']
        _res_guest_id = guest['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/booking/connect")
        body = {
            "surname": guest['LastName'],
            "dateOfBirth": guest['birthDate'],
            "reservationId": _res_num,
            "guestId": "",
            "reservationGuestId": ""
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        name = f"{guest['FirstName']} {guest['LastName']}"
        if _content['guestName'] != name:
            raise Exception("User is not able to connect booking with the account")

    @pytestrail.case(26112981)
    def test_28_guest_login(self, config, test_data, rest_ship, guest_data):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(_ship, "user-account-service/signin/email")
        body = {
                "userName": guest_data[0]['email'],
                "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(12150733)
    def test_29_verify_folio_transaction_details(self, config, rest_ship, guest_data):
        """
        Verify the folio transaction details
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        body = {
            "reservationGuestId": guest['reservationGuestId']
        }

        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/folio/transactiondetails")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(12150700)
    def test_30_verify_discover_search_ship(self, config, test_data, rest_ship):
        """
        Verify the Discover search landing page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {
            "iscoaching": "true"
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discoversearch/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        assert _content['suggestionsHeader'] == "Suggestions", "Search Suggestion is not matching !!"
        is_key_there_in_dict('closeBtnImgUrl', _content)
        is_key_there_in_dict('searchIconUrl', _content)
        is_key_there_in_dict('searchDefaultValue', _content)
        is_key_there_in_dict('clearSearchBtnLabel', _content)
        test_data['suggestionList'] = _content['suggestionList']
        is_key_there_in_dict('suggestionList', _content)
        if len(_content['suggestionList']) == 0:
            raise Exception("suggestionList length is Zero!!")

    @pytestrail.case(12150704)
    def test_31_verify_discover_search_functionality_ship(self, config, test_data, rest_ship, guest_data):
        """
        Verify the Discover search functionality
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        params = {
            "reservation-guest-id": guest['reservationGuestId'],
            "reservation-id": guest['reservationId'],
            "voyagenumber": test_data['voyageId'],
            "shipCode": config.ship.code
        }

        for suggestion in test_data['suggestionList']:
            body = {
                "searchTerm": suggestion
            }
            _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/discoversearch/search")
            _content = rest_ship.send_request(method="POST", url=_url, params=params, json=body, auth="user").content
            is_key_there_in_dict('closeBtnImgUrl', _content)
            is_key_there_in_dict('continueBtnImgUrl', _content)
            if 'noItemFound' in _content:
                logger.warn(_content['noItemFound']['headlineText'])
            else:
                if len(_content['resultContents']) > 0:
                    is_key_there_in_dict('relatedLabel', _content)
                    for results in _content['resultContents']:
                        if results['searchGroup'] == 'Events':
                            for resultEntryTypes in results['resultEntryTypes']:
                                check_assertions(
                                    ['id', 'name', 'category', 'sub_category', 'thumbnail_image_url', 'itemType'],
                                    resultEntryTypes)
                        elif results['searchGroup'] == 'Shops':
                            for resultEntryTypes in results['resultEntryTypes']:
                                check_assertions(
                                    ['actionURL', 'id', 'name', 'category', 'sub_category', 'thumbnail_image_url',
                                     'itemType'],
                                    resultEntryTypes)
                        elif results['searchGroup'] == 'Eateries':
                            for resultEntryTypes in results['resultEntryTypes']:
                                check_assertions(
                                    ['actionURL', 'id', 'name', 'category', 'deck', 'sub_category',
                                     'thumbnail_image_url',
                                     'itemType'],
                                    resultEntryTypes)
                        elif results['searchGroup'] == 'Shore Things':
                            for resultEntryTypes in results['resultEntryTypes']:
                                check_assertions(
                                    ['id', 'name', 'category', 'sub_category', 'thumbnail_image_url', 'itemType'],
                                    resultEntryTypes)
                else:
                    logger.warn(f"resultContents is Zero for {suggestion}")

                if len(_content['resultContents']) > 0:
                    if 'relatedGuides' in _content:
                        for relatedGuides in _content['relatedGuides']:
                            check_assertions(
                                ['header', 'body', 'landscapeThumbnailUrl', 'portraitThumbnailUrl', 'actionURL'],
                                relatedGuides)
                    else:
                        logger.warn('relatedGuides is not coming in discoversearch')

    @pytestrail.case(23748122)
    def test_32_update_personal_info_ship(self, config, rest_ship, guest_data):
        """
        Verify the update personal info at Ship
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        body = {
            "firstName": guest['FirstName'],
            "lastName": guest['LastName'],
            "middleName": "shipmidname",
            "preferredName": "shipprename"
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/personal")
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content

        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        assert _content['firstName'] == guest['FirstName'], "First Name is not matching !!"
        assert _content['lastName'] == guest['LastName'], "Last Name is not matching !!"
        assert _content['preferredName'] == "shipprename", "preferred Name is not matching !!"
        assert _content['middleName'] == "shipmidname", "middle name is not matching !!"

    @pytestrail.case(8365311)
    def test_33_update_contact_info_ship(self, config, test_data, rest_ship, guest_data):
        """
        Update Guest Contact info
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/contact")
        _content = rest_ship.send_request(method="GET", url=url, auth="user").content
        if 'addresses' in _content:
            test_data['ship_user_address'] = _content['addresses'][0]
            body = {
                "email": guest['email'],
                "phoneCountryCode": "US",
                "phoneNumber": str(generate_phone_number(10)),
                "addresses": [{
                    "countryCode": _content['addresses'][0]['countryCode'],
                    "city": _content['addresses'][0]['city'],
                    "line1": _content['addresses'][0]['line1'],
                    "zip": _content['addresses'][0]['zip'],
                    "stateCode": _content['addresses'][0]['stateCode']
                }]
            }
        else:
            body = {
                "email": guest['email'],
                "phoneCountryCode": "US",
                "phoneNumber": str(generate_phone_number(10)),
                "addresses": [{
                    "countryCode": "US",
                    "city": "Orlando",
                    "line1": "Baker Street",
                    "line2": "345",
                    "zip": "30987",
                    "stateCode": "FL"
                }]
            }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content
        _content = rest_ship.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('addresses', _content)
        for addresses in _content['addresses']:
            assert guest['email'] == _content['email'], "ERROR: Email not matching !!"
            assert _content['addresses'][0]['countryCode'] == addresses[
                'countryCode'], "ERROR: countryCode not matching !!"
            assert _content['addresses'][0]['city'] == addresses['city'], "ERROR: city not matching !!"
            assert _content['addresses'][0]['line1'] == addresses['line1'], "ERROR: lineOne not matching !!"
            assert _content['addresses'][0]['zip'] == addresses['zip'], "ERROR: zipCode not matching !!"
            assert _content['addresses'][0]['stateCode'] == addresses['stateCode'], "ERROR: stateCode not matching !!"

    @pytestrail.case(12150712)
    def test_34_help_and_support_ship(self, config, rest_ship):
        """
        Verify help and support response in on cruise mode
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/help-support/helps")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('categories', _content)

        for help_categories in _content['categories']:
            is_key_there_in_dict('cta', help_categories)
            is_key_there_in_dict('articles', help_categories)
            is_key_there_in_dict('name', help_categories)
            if help_categories['cta'] not in ['Before You Sail', 'The Days at Sea', 'Back on Dry Land']:
                raise Exception(f"{help_categories['cta']} is not exist in response")
            if len(help_categories['articles']) == 0:
                raise Exception(f"{help_categories['cta']} sub-sections are not present under articles")

    @pytestrail.case(30224872)
    def test_35_myvoyage_addons_ship(self, config, rest_ship, test_data, guest_data):
        """
        Verify the My voyage addons API
        :param config:
        :param rest_ship:
        :param test_data:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        params = {
            "guestId": guest['guestId'],
            "reservationNumber": test_data['reservationNumber'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/addons")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(30226097)
    def test_36_check_join_help_desk_vq(self, config, rest_ship, test_data, guest_data):
        """
        Verify the Join Help Desk Queue
        :param config:
        :param rest_ship:
        :param test_data:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/virtualqueuedefinitions")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        for definition_id in _content:
            is_key_there_in_dict('virtualQueueDefinitionId', definition_id)
            is_key_there_in_dict('virtualQueueDefinitionName', definition_id)
            is_key_there_in_dict('virtualQueueSettings', definition_id)
            if definition_id['virtualQueueDefinitionName'] == 'Help Desk':
                test_data['definition_id'] = definition_id['virtualQueueDefinitionId']
            for setting_id in definition_id['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', setting_id)
                is_key_there_in_dict('key', setting_id)
                is_key_there_in_dict('value', setting_id)

        body = {
            "personId": guest['reservationGuestId'],
            "personTypeCode": 'RG',
            "origin": 'SA-FAQ-PG',
            "virtualQueueDefinitionId": test_data['definition_id'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/virtualqueue")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content

        body = {
            "personIds": [guest['reservationGuestId']],
            "personTypeCode": 'RG',
            "virtualQueueDefinitionId": test_data['definition_id'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/virtualqueue/search")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        is_key_there_in_dict('virtualQueuePersons', _content['_embedded'])
        for vq_process in _content['_embedded']['virtualQueuePersons']:
            test_data['personTypeCode'] = vq_process['personTypeCode']
            test_data['origin'] = vq_process['origin']

    @pytestrail.case(30312159)
    def test_37_leave_help_desk_vq(self, config, rest_ship, test_data, guest_data):
        """
        Verify the Leave Help Desk Queue
        :param config:
        :param rest_ship:
        :param test_data:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        body = {
            "personId": guest['reservationGuestId'],
            "personTypeCode": 'RG',
            "status": 'R',
            "virtualQueueDefinitionId": test_data['definition_id'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/virtualqueue")
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content

        body = {
            "personIds": [guest['reservationGuestId']],
            "personTypeCode": 'RG',
            "virtualQueueDefinitionId": test_data['definition_id'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/virtualqueue/search")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if '_embedded' in _content:
            raise Exception("Guest does not leave from Help desk VQ")
        else:
            logger.info("Guest leave from Help desk VQ")

    @pytestrail.case(28231255)
    def test_38_on_boarded(self, config, test_data, rest_ship):
        """
        check guest is on boarded
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"reservation-number": test_data['reservationNumber'],
                  "reservation-guest-id": test_data['reservation_guest_ids']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), f"/guest-dashboard/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        assert _content['isGuestOnBoard'] == True, "Guest is not on-boarded"

    @pytestrail.case(28231254)
    def test_39_card_details(self, config, test_data, guest_data, rest_ship):
        """
        check card details of on boarded sailor
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "reservation-id": guest_data[0]['reservationId'],
            "path": "/Sailor-App/Guides/Ports/Portsmouth",
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/carddetail")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(28317710)
    def test_40_voyage_account_setting_personal_info(self, config, rest_ship, guest_data):
        """
        Check if the first and last name is matching with the reservation booked
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/personal")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if _content['firstName'] != guest['FirstName'] and _content['lastName'] != guest['LastName']:
            raise Exception("First and Last name is not matching under the personal information of Sailor App!")

    @pytestrail.case(31069447)
    def test_41_add_social_connection(self, config, rest_ship, guest_data):
        """
        Add Social Connection
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        json = {
            "personId": guest['reservationGuestId'],
            "personTypeCode": "RG",
            "connectionState": [
                "CF"
            ],
            "isIncludeSameStateroomGuests": True
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "connections/search")
        _content = rest_ship.send_request(method="POST", url=_url, json=json, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('connectionDetailsResponses', _content['_embedded'])
        assert len(_content['_embedded']['connectionDetailsResponses']) > 0, 'No social connections created !!'
        for _connection in _content['_embedded']['connectionDetailsResponses']:
            assert _connection['connectionState'] == 'CF', 'Connection status is not confirmed after adding !!'

    @pytestrail.case(32788747)
    def test_42_voyage_account_setting_reservation(self, config, test_data, rest_ship):
        """
        Check if the reservation guestId and guestId is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/reservations")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict("guestBookings", _content)
        is_key_there_in_dict("pageDetails", _content)
        assert len(test_data['shipside_guests']) != 0, 'No guest available on ship side'
        if test_data['shipside_guests'][0]['reservationid'] != _content['guestBookings'][0]['reservationId']:
            raise Exception('Same ReservationId is not available in Voyage Setting reservation')
        if test_data['shipside_guests'][0]['reservationguestid'] != _content['guestBookings'][0]['reservationGuestId']:
            raise Exception('Same ReservationId is not available in Voyage Setting reservation')

    @pytestrail.case(32788748)
    def test_43_voyage_account_setting_communication_preferences(self, config, rest_ship):
        """
        Check if the essentialsPreference is coming in communication_preferences
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/user/communicationpreferences")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        assert len(_content) != 0, 'communication preference is not coming'
        is_key_there_in_dict("pageDetails", _content)
        is_key_there_in_dict("userNotifications", _content)

    @pytestrail.case(32788749)
    def test_44_voyage_account_setting_wearable_content(self, config, rest_ship):
        """
        Check if the contents are coming for wearble
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/wearable/content")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        assert len(_content) != 0, 'Band and Pin change option is not available'
        is_key_there_in_dict("statusLocked", _content)
        is_key_there_in_dict("successPinChangedBody", _content)

    @pytestrail.case(32788750)
    def test_45_travel_documents_in_setting(self, config, test_data, rest_ship, guest_data):
        """
        Verification of Travel Document in Setting
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "reservation-id": guest_data[0]['reservationId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/sailingdocuments/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        assert len(_content) != 0, 'Sailing document not Syncing'
        is_key_there_in_dict('travelDocuments', _content['sailingDocuments'])
        is_key_there_in_dict('contracts', _content['sailingDocuments'])
        is_key_there_in_dict('voyageContract', _content['sailingDocuments'])
        is_key_there_in_dict('embarkationHealthCheck', _content['sailingDocuments'])
        params = {
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/traveldocuments")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        assert len(_content) != 0, 'Travel document page content is not Syncing'
        is_key_there_in_dict('passport', _content)
        is_key_there_in_dict('visas', _content)
        is_key_there_in_dict('arc', _content)
        is_key_there_in_dict('esta', _content)
        is_key_there_in_dict('postCruiseInfo', _content)

    @pytestrail.case(32788751)
    def test_46_voyage_account_setting_login(self, config, rest_ship):
        """
        Check if the change email and password is enabled or not
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "voyage-account-settings/login/landing")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict("labels", _content)
        is_key_there_in_dict("loginDetails", _content)
        is_key_there_in_dict("changeEmail", _content['loginDetails'])
        is_key_there_in_dict("isEnable", _content['loginDetails']['changePassword'])
        assert _content['loginDetails']['changeEmail']['isEnable'] == True, 'change email option is in disable mode'
        assert _content['loginDetails']['changePassword'][
                   'isEnable'] == True, 'change password option is in disable mode'

    @pytestrail.case(32788753)
    def test_47_menu_indicator_ship_eats(self, config, rest_ship):
        """
        Get ship eats menu indicator
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/configuration/menuindicators')
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if type(_content) == str:
            _content = json.loads(_content)
        assert len(_content) != 0, 'No menuindicator available for shipeats'
        is_key_there_in_dict('Vegetarian', _content)
        is_key_there_in_dict('GlutenFreeOption', _content)

    @pytestrail.case(32788754)
    def test_48_notification_hub_ship_eats(self, config, rest_ship):
        """
        Get ship eats notification hub
        :param config:
        :param rest_ship:
        :return:
        """
        params = {
            "negotiateVersion": "1"
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), 'notificationHub/negotiate')
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        assert len(_content['availableTransports']) != 0, 'no transport available'
        is_key_there_in_dict('connectionId', _content)
        is_key_there_in_dict('connectionToken', _content)

    @pytestrail.case(32788755)
    def test_49_voyage_account_setting_startup(self, config, rest_ship):
        """
        Check if the essentials feedback request is coming in voyage setting
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/voyage-account-settings/startup")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('configurations', _content)
        is_key_there_in_dict('notificationPrefValues', _content['configurations'])
        is_key_there_in_dict('reminder', _content['configurations']['notificationPrefValues'])
        is_key_there_in_dict('sailChat', _content['configurations']['notificationPrefValues'])
        is_key_there_in_dict('recommendations', _content['configurations']['notificationPrefValues'])
        is_key_there_in_dict('feedbackRequest', _content['configurations']['notificationPrefValues'])
        is_key_there_in_dict('privacy', _content['configurations']['notificationPrefValues'])
        for content in _content['configurations']['notificationPrefValues']:
            assert len(
                content) != 0, f"content not available {_content['configurations']['notificationPrefValues'][content]} "

    @pytestrail.case(50434675)
    def test_50_stateroom_muster_landing(self, config, rest_ship, test_data, guest_data):
        """
        To verify muster data landing
        param: config
        param: rest_ship
        param: guest_data
        param: test_data
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.cabinbff"), "/stateroom/muster/landing")

        params = {
            "shipcode": config.ship.code,
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "language": "esp",
            "device": "app"
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('musterData', _content)
        is_key_there_in_dict('assemblyStationData', _content)

    @pytestrail.case(32788752)
    def test_51_dashboard_port_details(self, config, test_data, guest_data, rest_ship):
        """
        To verify port details should available on dashboard ship side
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/content/ports")
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "voyage-number": test_data['voyageNumber'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "reservation-number": test_data['reservationNumber'],
            "sailing-package": test_data['sailingPackageCode']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('ports', _content)
        for port in _content['ports']:
            is_key_there_in_dict('portCode', port)
            is_key_there_in_dict('itineraryDay', port)
            is_key_there_in_dict('isSeaDay', port)

    @pytestrail.case(67651956)
    def test_52_verify_dashboard_quick_links(self, config, test_data, guest_data, rest_ship):
        """
        To verify quick links are available on dashboard ship side
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/guest-dashboard/quicklinks")
        params = {
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            'reservation-id': guest_data[0]['reservationId'],
            'reservation-number': test_data['reservationNumber'],
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('taskLinkDetails', _content)
        is_key_there_in_dict('exprienceLinkDetails', _content)
        is_key_there_in_dict('taskLinks', _content['taskLinkDetails'])
        is_key_there_in_dict('exprienceLinks', _content['exprienceLinkDetails'])

        task_links_list = ['addContact', 'viewShipVenue', 'viewAgenda', "viewWallet", "cabinServices",
                           'shipEatsDelivery']
        experience_links_list = ['restaurant', 'shoreThing', 'event', 'treatment', 'mnvv']
        for link in _content['taskLinkDetails']['taskLinks']:
            is_key_there_in_dict('taskName', link)
            assert link['taskName'] in task_links_list, f"Quick link not displayed on dashboard for {link['title']}"

        for link in _content['exprienceLinkDetails']['exprienceLinks']:
            is_key_there_in_dict('exprienceName', link)
            assert link['exprienceName'] in experience_links_list, f"Quick link not displayed on dashboard for {link['title']}"

@pytest.mark.SAILOR_APP_SHIP
@pytest.mark.run(order=34)
class TestActivitiesShip:
    """
        Test Suite For ShoreEx, dining, Lineup at Ship side
    """

    @pytestrail.case(26152205)
    def test_01_check_shake_for_champagne_get_data(self, config, rest_ship):
        """
        Get the static data for Champagne
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "resources/shakeforchampagne")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content

        is_key_there_in_dict('landing', _content)
        is_key_there_in_dict('landingPushButton', _content)
        is_key_there_in_dict('landingBottlesPanel', _content)
        is_key_there_in_dict('confirmation', _content)
        is_key_there_in_dict('confirmationCancel', _content)
        is_key_there_in_dict('error', _content)

    @pytestrail.case(26152206)
    def test_02_champagne_order_details(self, config, test_data, rest_ship):
        """
        Get the Champagne order venue and menu item details
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "v1/menuitems/champagne")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content

        is_key_there_in_dict('OrderTypeId', _content)
        is_key_there_in_dict('OrderOriginId', _content)
        is_key_there_in_dict('MaximumBottlesAllowed', _content)

        test_data['menuItemID'] = _content['MenuItemDetails']['MenuItemId']
        test_data['menuItemNumber'] = _content['MenuItemDetails']['MenuItemNumber']
        for menuitem in _content['MenuItemDetails']['MenuItemPrices']:
            test_data['unitId'] = menuitem['UnitId']
            test_data['price'] = menuitem['Price']
        test_data['venueId'] = _content['VenueDetails']['VenueId']
        test_data['orderTypeId'] = _content['OrderTypeId']
        test_data['orderOriginId'] = _content['OrderOriginId']

    @pytestrail.case(12150716)
    def test_03_make_champagne_order(self, config, test_data, rest_ship, guest_data):
        """
        Order the champagne for guest
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        test_data['taxAmount'] = 14
        body = {
            "OrderTypeId": test_data['orderTypeId'],
            "OrderOriginId": test_data['orderOriginId'],
            "VenueId": test_data['venueId'],
            "GuestId": guest['reservationGuestId'],
            "AddedBy": guest['reservationGuestId'],
            "TaxAmount": test_data['taxAmount'],
            "Amount": test_data['taxAmount'] + int(test_data['price']),
            "OrderDetails": [{
                "OrderQuantity": 1,
                "MenuItemId": test_data['menuItemID'],
                "UnitPrice": int(test_data['price']),
                "UnitId": test_data['unitId'],
                "TaxAmount": test_data['taxAmount'],
                "Amount": int(test_data['price'])
            }]
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "v1/orders")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if 'ReturnCode' and 'Message' in _content:
            if _content['Message'] == 'NotAvailableOnLocation':
                test_data['champagne_order'] = False
                pytest.skip("Simulator not enabled")
        test_data['champagne'] = _content
        assert 1 == _content['Status'], "Status of order is not booked"
        is_key_there_in_dict('OrderId', _content)
        test_data['champagne_order'] = True

    @pytestrail.case(12150717)
    def test_04_cancel_champagne_order(self, config, test_data, rest_ship, guest_data):
        """
        Cancel the champagne for guest
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['champagne_order']:
            pytest.skip("Simulator not enabled")
        guest = guest_data[0]
        body = {
            "OrderId": test_data['champagne']['OrderId'],
            "VenueId": test_data['champagne']['VenueId'],
            "OrderCancellations": [{
                "OrderId": test_data['champagne']['OrderId'],
                "CancellationRequestedBy": guest['reservationGuestId'],
                "CancellationReason": "I have changed my mind",
                "AddedBy": guest['reservationGuestId']
            }]
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"v1/orders/{test_data['champagne']['OrderId']}/cancel")
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content

        assert "OrderSuccessfullyCancelled" == _content['Message'], "Champagne Order is not cancelled !!"
        assert guest['reservationGuestId'] == _content['GuestId'], "Guest Id is not matching for order is cancelled!!"
        assert test_data['orderOriginId'] == _content[
            'OrderOriginId'], "Order Origin Id is not matching for cancel order"
        assert test_data['orderTypeId'] == _content['OrderTypeId'], "Order Type Id is not matching for cancel order"

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(11777711)
    def test_05_check_availability_of_lineup(self, config, test_data, rest_ship, guest_data):
        """
        List all Lineup Activities
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['chosenActivity'] = dict()
        current_date = str(datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + 19800)).replace(' ', 'T')
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        body = {
            "voyageNumber": test_data['voyageId'],
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": guest['reservationGuestId'],
            "categoryCode": "ET",
        }
        params = {
            "page": 1,
            "size": 9999999
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, params=params, auth="user").content
        if len(_content['activities']) == 0:
            test_data['lineupAvailableShip'] = False
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        is_key_there_in_dict('activities', _content)
        is_key_there_in_dict('filterCategories', _content)
        is_key_there_in_dict('preCruise', _content)
        is_key_there_in_dict('page', _content)
        test_data['lineupAvailableShip'] = False

        for activity in _content['activities']:
            if activity['isBookingEnabled'] and len(activity['activitySlots']) > 0:
                for slot in activity['activitySlots']:
                    if not slot['isBookingClosed']:
                        if len(slot['activitySellingPrices']) != 0:
                            break
                        if slot['isEnabled'] and slot['startDate'] > current_date and slot['inventoryCount'] > 0:
                            test_data['chosenActivity']['startDate'] = slot['startDate']
                            test_data['chosenActivity']['endDate'] = slot['endDate']
                            test_data['chosenActivity']['activitySlotCode'] = slot['activitySlotCode']
                            test_data['chosenActivity']['activityCode'] = activity['activityCode']
                            test_data['chosenActivity']['currencyCode'] = activity['currencyCode']
                            test_data['chosenActivity']['categoryCode'] = activity['categoryCode']
                            test_data['chosenActivity']['amount'] = 0
                            test_data['lineupAvailableShip'] = True
                            return
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup with 0 selling price available to Book for active voyage")

    @pytestrail.case(11777708)
    def test_06_book_lineup(self, config, test_data, guest_data, rest_ship):
        """
        Book Lineup
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'], "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId']
            }],
            "activitySlotCode": test_data['chosenActivity']['activitySlotCode'],
            "accessories": [],
            "operationType": None,
            "currencyCode": test_data['chosenActivity']['currencyCode'],
            "shipCode": config.ship.code,
            "categoryCode": test_data['chosenActivity']['categoryCode']
        }
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        except Exception as exp:
            if "Booking already exists for following person, for the selected date and time" in exp.args[0]:
                test_data['lineup_booked'] = False
                pytest.skip("Skipping this TC as lineup booking is already there for selected activity")
            else:
                raise Exception(exp)
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not Fully Paid even after paying completely")
        test_data['shipLineupBookingId'] = _content
        test_data['lineup_booked'] = True

    @pytestrail.case(11777712)
    def test_07_verify_lineup_under_guest_itineraries(self, config, test_data, rest_ship, guest_data):
        """
        Verify that lineup under guestItineraries after book
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        elif not test_data['lineup_booked']:
            pytest.skip("Skipping this TC as lineup booking is already there for selected activity")
        guest = guest_data[0]
        params = {"reservationGuestId": guest['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['appointmentLinkId'] == test_data['shipLineupBookingId']['appointmentLinkId'] and \
                    activity['appointmentId'] == test_data['shipLineupBookingId']['appointmentId']:
                break
        else:
            raise Exception("Cannot find activityCode and appointmentId for booked lineup !!")

    @pytestrail.case(11777709)
    def test_08_edit_lineup(self, config, test_data, rest_ship, guest_data):
        """
        Add the new guest in Lineup
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        elif not test_data['lineup_booked']:
            pytest.skip("Skipping this TC as lineup booking is already there for selected activity")
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "isPayWithSavedCard": False,
            "activityCode": test_data['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [
                {
                    "personId": guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": guest['guestId'],
                    "status": "CONFIRMED"
                },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId']
                }
            ],
            "activitySlotCode": test_data['chosenActivity']['activitySlotCode'],
            "accessories": [],
            "totalAmount": test_data['chosenActivity']['amount'],
            "currencyCode": test_data['chosenActivity']['currencyCode'],
            "appointmentLinkId": test_data['shipLineupBookingId']['appointmentLinkId'],
            "operationType": "EDIT",
            "categoryCode": test_data['chosenActivity']['categoryCode'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "startDate": test_data['chosenActivity']['startDate'],
            "endDate": test_data['chosenActivity']['endDate']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['shipLineupBookingId'] = _content

    @pytestrail.case(11777713)
    def test_09_verify_edit_lineup_under_guest_itineraries(self, config, test_data, rest_ship, guest_data):
        """
        Verify that lineup in guestItineraries after edit
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        elif not test_data['lineup_booked']:
            pytest.skip("Skipping this TC as lineup booking is already there for selected activity")
        guest = guest_data[0]
        params = {"reservationGuestId": guest['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['appointmentLinkId'] == test_data['shipLineupBookingId']['appointmentLinkId'] and \
                    activity['categoryCode'] == test_data['chosenActivity']['categoryCode']:
                break
        else:
            raise Exception("Cannot find activityCode and appointmentId for booked lineup !!")

    @pytestrail.case(11777710)
    def test_10_cancel_lineup(self, config, test_data, rest_ship, guest_data):
        """
        cancel lineup
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        elif not test_data['lineup_booked']:
            pytest.skip("Skipping this TC as lineup booking is already there for selected activity")
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['shipLineupBookingId']['appointmentLinkId'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CANCELLED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId'],
                    "status": "CANCELLED"
                }
            ]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('paymentStatus', _content)
        test_data['lineupCancelledBookingId'] = _content

    @pytestrail.case(11777714)
    def test_11_verify_cancel_lineup(self, config, test_data, rest_ship, guest_data):
        """
        Verify cancelled lineup
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        elif not test_data['lineup_booked']:
            pytest.skip("Skipping this TC as lineup booking is already there for selected activity")

        guest = guest_data[0]
        params = {"reservationGuestId": guest['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) == 0:
            return
        elif len(_content) > 0:
            for activity in _content:
                if activity['appointmentLinkId'] == test_data['lineupCancelledBookingId']['appointmentLinkId'] and \
                        activity['categoryCode'] == test_data['chosenActivity']['categoryCode']:
                    raise Exception("Booked lineup did not got cancelled")
            else:
                return

    @pytestrail.case(12768802)
    def test_12_verify_current_activities(self, config, rest_ship, guest_data):
        """
        Verify Deleted Activities
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _shore = config.ship.url
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            logger.info(f"Fresh Sailor already have {len(_content)} linked activities")

    @pytestrail.case(26150774)
    def test_13_list_activities(self, config, test_data, rest_ship, guest_data):
        """
        List all Activities
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        current_date = str(datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + 19800)).replace(' ', 'T')
        body = {
            "voyageNumber": test_data['voyageId'],
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": guest['reservationGuestId'],
            "categoryCode": "PA", "guestCount": guest_count
        }
        params = {
            "page": 1,
            "size": 9999999
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, params=params, auth="user").content
        if len(_content['activities']) == 0:
            test_data['excursionAvailableShip'] = False
            pytest.skip(msg="Skipping, as No Excursion is available to Book for active voyage")
        is_key_there_in_dict('filterCategories', _content)
        is_key_there_in_dict('activities', _content)
        is_key_there_in_dict('preCruise', _content)
        is_key_there_in_dict('page', _content)
        test_data['excursionAvailableShip'] = False

        for activity in _content['activities']:
            if activity['isBookingEnabled'] and len(activity['activitySlots']) > 0:
                for slot in activity['activitySlots']:
                    if not slot['isBookingClosed']:
                        if len(slot['activitySellingPrices']) != 0:
                            break
                        if slot['startDate'] > current_date and slot['isEnabled'] and slot['inventoryCount'] > 0:
                            test_data['activityCodeShip'] = activity['activityCode']
                            test_data['activitySlotCode'] = slot['activitySlotCode']
                            test_data['startTime'] = slot['startDate']
                            test_data['endTime'] = slot['endDate']
                            test_data['amount'] = 0
                            test_data['excursionAvailableShip'] = True
                            return
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg="Skipping, as No Excursion with 0 selling price available to Book for active voyage")

    @pytestrail.case(12150705)
    def test_14_validate_excursion_filter(self, config, test_data, rest_ship, guest_data):
        """
        Validate all filters in excursion
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        start_time = {'morning': "06:00:00", 'afternoon': "12:00:00", 'night': "18:00:00"}
        end_time = {'morning': "11:59:59", 'afternoon': "17:59:59", "night": "23:59:59"}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        for duration in start_time.keys():
            body = {
                "categoryCode": "PA",
                "reservationNumber": test_data['reservationNumber'],
                "reservationGuestId": guest['reservationGuestId'],
                "voyageNumber": test_data['voyageId'],
                "portCode": test_data['sailorApp']['ship_port_details']['portCode'],
                "guestCount": guest_count,
                "startDate": test_data['sailorApp']['ship_port_details']['arrivalTime'],
                "startTime": start_time[duration],
                "endDate": "",
                "endTime": end_time[duration],
                "subTypeId": ""
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
            is_key_there_in_dict('filterCategories', _content)
            is_key_there_in_dict('activities', _content)
            is_key_there_in_dict('strings', _content)
            is_key_there_in_dict('preCruise', _content)

    @pytestrail.case(26151264)
    def test_15_add_excursion_to_love_list(self, config, test_data, guest_data, rest_ship):
        """
        Add excursion to love list
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')

        guest = guest_data[0]
        _num = test_data['reservationNumber']
        _id = guest['reservationGuestId']
        _res_id = guest['reservationId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/favourites")
        body = {
            "reservationGuestId": _id,
            "categoryCode": "PA",
            "activityCode": test_data['activityCodeShip'],
            "isFavourite": True
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="user").content

        params = {
            "reservationNumber": _num,
            "reservationGuestId": _id,
            "categoryCodes": "PA",
            "size": 10
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/favourites")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="user").content
        for favourite in _content['favourites']:
            if favourite['activityCode'] == test_data['activityCodeShip']:
                break
        else:
            raise Exception(f"{test_data['activityCodeExcursion']} Excursion Not Added to the love list in Sailor App")

    @pytestrail.case(26151265)
    def test_16_book_activities(self, config, test_data, guest_data, rest_ship):
        """
        Book activities
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        time.sleep(5)
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['activityCodeShip'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId']
            }],
            "activitySlotCode": test_data['activitySlotCode'],
            "accessories": [],
            "totalAmount": test_data['amount'],
            "operationType": None,
            "currencyCode": "USD"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not Fully Paid even after paying completely")
        test_data['appointmentId'] = _content['appointmentId']
        test_data['appointmentLinkId'] = _content['appointmentLinkId']

    @pytestrail.case(26151267)
    def test_17_verify_guest_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')

        guest = guest_data[0]
        _res_num = test_data['reservationNumber']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/guestactivities")
        body = {
            "activityCode": test_data['activityCodeShip'],
            "reservationGuestId": guest_data[0]['reservationGuestId'],
            "startTime": test_data['startTime'],
            "endTime": test_data['endTime'],
            "includeConflicts": False
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        for _guests in _content['guests']:
            if guest['guestId'] == _guests['guestId']:
                break
        else:
            raise Exception("The activities did not got booked for the correct User")

    @pytestrail.case(26151268)
    def test_18_verify_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')

        params = {"reservationGuestId": guest_data[0]['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), f"/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for booked_activity in _content:
            if booked_activity['productSlotCode'] == test_data['activitySlotCode']:
                assert test_data['activityCodeShip'] == booked_activity[
                                'productCode'], "activityCode != productCode !!"
                assert test_data['appointmentId'] == booked_activity[
                                    'appointmentId'], "appointmentId mismatch !!"
                assert test_data['appointmentLinkId'] == booked_activity[
                                'appointmentLinkId'], "appointmentLinkId mismatch !!"

    @pytestrail.case(12758866)
    def test_19_update_activities(self, config, test_data, rest_ship, guest_data):
        """
        Update activities that has been purchased
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['activityCodeShip'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CONFIRMED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId']
                }],
            "activitySlotCode": test_data['activitySlotCode'],
            "accessories": [],
            "currencyCode": "USD",
            "appointmentLinkId": test_data['appointmentLinkId'],
            "operationType": "EDIT"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        test_data['appointmentLinkIdUpdated'] = _content['appointmentLinkId']
        test_data['appointmentIdUpdated'] = _content['appointmentId']
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not fully paid after updating excursion")

    @pytestrail.case(26151269)
    def test_20_verify_update_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify activities has been updated
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')

        params = {
            "reservationGuestId": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for slot in _content:
            if slot['productSlotCode'] == test_data['activitySlotCode']:
                if test_data['appointmentLinkIdUpdated'] == slot['appointmentLinkId'] and test_data[
                    'appointmentIdUpdated'] != slot['appointmentId']:
                    break
        else:
            raise Exception(f"Booked activity is not updated with new Time Slot !!")

    @pytestrail.case(12758867)
    def test_21_delete_activities(self, config, test_data, rest_ship, guest_data):
        """
        Delete Activity
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['appointmentLinkIdUpdated'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CANCELLED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId'],
                    "status": "CANCELLED"
                }
            ]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content

    @pytestrail.case(12768801)
    def test_22_verify_deleted_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify Deleted Activities
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShip']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')

        guest = guest_data[0]
        _shore = config.ship.url
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for booked_activity in _content:
            if booked_activity['productSlotCode'] == test_data['activitySlotCode']:
                raise Exception("Booked excursion did not got cancelled")

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(4825991)
    def test_23_list_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Verify list of eateries available
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _num = test_data['reservationNumber']
        _id = guest['reservationGuestId']
        _res_id = guest['reservationId']
        params = {
            "reservation-guest-id": guest['reservationGuestId'],
            "reservation-id": _res_id,
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/spacetype/Eateries/landing")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

        if len(_content['spaces']['bookingRequired']) == 0:
            test_data['eateriesAvailableShip'] = False
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')

        activities = _content['spaces']['bookingRequired']
        activities_copy = activities[:]
        for activity in activities_copy:
            activity_copy = activity
            if 'avaliableSlots' in activity and 'activityCode' in activity:
                if len(activity['avaliableSlots']) > 0:
                    slots_copy = activity_copy['avaliableSlots'][:]
                    for slot in slots_copy:
                        if slot['isActive']:
                            if 'slotCode' not in slot:
                                activity['avaliableSlots'].remove(slot)
                        else:
                            activity['avaliableSlots'].remove(slot)
                            
                    if len(activity['avaliableSlots']) == 0:
                        activities.remove(activity)
                else:
                    activities.remove(activity)
            else:
                activities.remove(activity)
        test_data['sailorApp']['eateries'] = activities

        if len(test_data['sailorApp']['eateries']) == 0:
            test_data['eateriesAvailableShip'] = False
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')
        else:
            test_data['eateriesAvailableShip'] = True

    @pytestrail.case(4825993)
    def test_24_book_eateries(self, config, test_data, guest_data, rest_ship):
        """
        Book eateries
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        params = {"reservationGuestId": guest['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

        test_data['eateriesBookedShip'] = False
        for activity in test_data['sailorApp']['eateries']:
            if not test_data['eateriesBookedShip']:
                for slot in activity['avaliableSlots']:
                    if len(_content) != 0:
                        if _content[0]['productSlotCode'] == slot["slotCode"]:
                            break
                    slot_start_date = str(datetime.fromtimestamp(slot['startDateTime']/1000)).split(" ")[0]
                    body = {
                        "activityCode": activity['activityCode'],
                        "loggedInReservationGuestId": guest['reservationGuestId'],
                        "reservationNumber": test_data['reservationNumber'],
                        "isGift": False,
                        "personDetails": [{
                            "personId": guest['reservationGuestId'],
                            "reservationNumber": test_data['reservationNumber'],
                            "guestId": guest['guestId']
                        }],
                        "activitySlotCode": slot["slotCode"],
                        "accessories": [],
                        "operationType": None,
                        "currencyCode": "USD",
                        "categoryCode": "RT",
                        "shipCode": config.ship.code,
                        'voyageNumber': test_data['voyageNumber'],
                        'startDate': slot_start_date
                    }
                    try:
                        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
                        is_key_there_in_dict('paymentStatus', _content)
                        is_key_there_in_dict('appointmentLinkId', _content)
                        is_key_there_in_dict('appointmentId', _content)
                        if "FULLY_PAID" != _content['paymentStatus']:
                            raise Exception("Payment status is not fully paid after booking eateries")
                        test_data['eateries_appointmentLinkId'] = _content['appointmentLinkId']
                        test_data['eateries_appointmentId'] = _content['appointmentId']
                        test_data['sailorApp']['chosenEateries'] = activity
                        test_data['sailorApp']['chosenEateries']['eateriesSlots'] = slot
                        test_data['eateries_activitycode'] = activity['activityCode']
                        test_data['eateries_activityslotcode'] = slot['slotCode']
                        test_data['eateriesBookedShip'] = True
                        break
                    except Exception as exp:
                        if "409" and "booking already exists" in exp.args[0].lower():
                            logger.info(exp)
                            continue
                        elif "400" and "no inventory available on this slot" in exp.args[0].lower():
                            logger.info(exp)
                            continue
                        else:
                            raise Exception(exp)
            else:
                break
        if not test_data['eateriesBookedShip']:
            pytest.skip("Not able to book any slot for any of the eatries.")

    @pytestrail.case(4825995)
    def test_25_verify_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Verify that eateries has been purchased
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')

        params = {"reservationGuestId": guest_data[0]['reservationGuestId']}
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for booked_activity in _content:
            if booked_activity['productSlotCode'] == test_data['eateries_activityslotcode']:
                assert test_data['eateries_activitycode'] == booked_activity['productCode'], "activityCode != productCode !!"
                assert test_data['eateries_appointmentId'] == booked_activity['appointmentId'], "appointmentId mismatch !!"
                assert test_data['eateries_appointmentLinkId'] == booked_activity['appointmentLinkId'], "appointmentLinkId mismatch !!"

    @pytestrail.case(4825997)
    def test_26_update_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Update eateries that has been purchased
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['eateries_activitycode'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CONFIRMED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId']
                }],
            "activitySlotCode": test_data['eateries_activityslotcode'],
            "accessories": [],
            "currencyCode": "USD",
            "appointmentLinkId": test_data['eateries_appointmentLinkId'],
            "operationType": "EDIT",
            "categoryCode": "RT",
            "shipCode": config.ship.code
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        test_data['eateries_appointmentLinkIdUpdated'] = _content['appointmentLinkId']
        test_data['eateries_appointmentIdUpdated'] = _content['appointmentId']
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not fully paid after updating eateries")

    @pytestrail.case(4825999)
    def test_27_verify_update_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Verify eateries has been updated
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')

        params = {
            "reservationGuestId": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _activity in _content:
            if _activity['productSlotCode'] == test_data['eateries_activityslotcode']:
                if test_data['eateries_appointmentIdUpdated'] == _activity['appointmentId']:
                    raise Exception('appointmentId is same even after updating eateries')

    @pytestrail.case(4826000)
    def test_28_delete_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Delete eateries
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')
        time.sleep(5)
        guest = guest_data[0]
        second_guest = guest_data[1]
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['eateries_appointmentLinkIdUpdated'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "categoryCode": "RT",
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CANCELLED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId'],
                    "status": "CANCELLED"
                }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content

    @pytestrail.case(4826003)
    def test_29_verify_deleted_eateries(self, config, test_data, rest_ship, guest_data):
        """
        Verify Deleted eateries
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShip']:
            pytest.skip(msg='Skipping, as No eateries available to Book for active voyage')

        guest = guest_data[0]
        _ship = config.ship.url
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for booked_activity in _content:
            if booked_activity['productSlotCode'] == test_data['eateries_activityslotcode']:
                raise Exception("Booked eateries did not got cancelled")

    @pytestrail.case(17527574)
    def test_30_check_in_detail(self, config, test_data, rest_ship, guest_data):
        """
        Get Guest Check in detail
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['sailorApp']['shipEats'] = dict()
        guest = guest_data[0]
        params = {
            "reservation-guest-id": guest['reservationGuestId'],
            'parts': 'reservationInfo'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/checkin/guest/detail-info')
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content['_embedded']) == 0:
            raise Exception('Check in details are not there for the Guest')
        for _check_in in _content['_embedded']['eCheckinGuestDetailsList']:
            is_key_there_in_dict('reservationGuestId', _check_in)
            is_key_there_in_dict('guestId', _check_in)
            is_key_there_in_dict('reservationId', _check_in)
            is_key_there_in_dict('reservationInfo', _check_in)

    @pytestrail.case(17532225)
    def test_31_get_ship_time_fnb(self, config, rest_ship):
        """
        Get Ship time from fnb service
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/ship/shiptime')
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('ShipTimeOffset', _content)
        is_key_there_in_dict('ShipTime', _content)
        is_key_there_in_dict('ShipTimeUiFormat', _content)

    @pytestrail.case(17543851)
    def test_32_get_muster_drill_status(self, config, rest_ship):
        """
        Get Muster drill status
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/ships/musterdrillstatus')
        params = {
            'shipcode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(24938097)
    def test_33_configurations_ship_eats(self, config, rest_ship, test_data):
        """
        Get ship eats configurations
        :param config:
        :param rest_ship:
        :param test_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/configuration/shipeats')
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        check_assertions([
            'ShipEatsBreakfastType', 'ShipEatsOrderHistoryPollingInterval', 'ShipEatsOrderOriginId',
            'ShipEatsEatNowOrderTypeId', 'ShipEatsPreOrderTypeId',
            'ShipEatsDefaultResponseTimeout', 'ActivityCodeDeliveredNotification',
            'ActivityCodeDeliveredPreOrderNotification', 'ActivityCodeGuestNotFoundNotification',
            'ActivityCodeCancelledOrderNotification', 'ActivityCodeCancelledByGuestNotification',
            'IsErrorMode'], _content)
        test_data['sailorApp']['shipEats']['shipEatsEatNowOrderTypeId'] = _content['ShipEatsEatNowOrderTypeId']
        test_data['sailorApp']['shipEats']['ShipEatsOrderOriginId'] = _content['ShipEatsOrderOriginId']

    @pytestrail.case(17543853)
    def test_34_ship_eats_resources(self, config, rest_ship):
        """
        Get ship eats resources
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/resources/shipEats/shared')
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        check_assertions([
            'gotYourOrderIllo', 'pickUpPlatesText', 'vegetarianOptionText', 'weGotOrderUpdate', 'orderCancelIllo',
            'minusImage', 'breakFastSelectTimeSlotText',
            'confirmationBodyText', 'notAvailableText', 'orderUpdateIllo', 'noRecentOrderText',
            'guestNotFoundNotificationBgColor', 'yesText',
            'preOrderNotAvailText', 'yourBasketText', 'glutenFreeOptionText'], _content)

    @pytestrail.case(26151271)
    def test_35_get_venues(self, config, test_data, rest_ship, guest_data):
        """
        Get venues
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"/v1/venues/detection/{guest['reservationGuestId']}")
        params = {
            'onlyLocationRequired': False
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        check_assertions([
            'Venue', 'Location', 'PreOrderBreakfastVenueId', 'CabinNumber', 'LocationId', 'ReturnCode'], _content)
        test_data['sailorApp']['shipEats']['venue'] = _content

    @pytestrail.case(26151272)
    def test_36_get_allergens(self, config, rest_ship, test_data):
        """
        Get Allergens
        :param config:
        :param rest_ship:
        :param test_data:
        :return:
        """
        test_data['sailorApp']['shipEats']['allergens'] = dict()
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/allergens")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        for _data in _content:
            check_assertions([
                'AllergyId', 'AllergenName'], _data)
        for _data in _content:
            test_data['sailorApp']['shipEats']['allergens']['id'] = _data['AllergyId']
            break

    @pytestrail.case(17612299)
    def test_37_get_meal_periods(self, config, test_data, rest_ship):
        """
        Get Meal periods
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/menuitems/mealperiods")
        current_date = str(datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + 19800).date())
        params = {
            'venueId': test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId'],
            'startDate': current_date
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _data in _content:
            check_assertions([
                'MealPeriodId', 'MealPeriodType', 'Name', 'MealPeriodEffectiveWindows'], _data)

    @pytestrail.case(26152203)
    def test_38_get_menu_items(self, config, test_data, rest_ship):
        """
        Get Menu Items
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/menuItems")
        epoch_time = test_data['aci']['shipEpochTime'] + 19800
        test_data['sailorApp']['shipEats']['startDate'] = str(datetime.utcfromtimestamp(epoch_time).date())
        epoch_time = test_data['aci']['shipEpochTime'] + 19800 + 86400
        test_data['sailorApp']['shipEats']['endDate'] = str(datetime.utcfromtimestamp(epoch_time).date())
        params = {
            'venueId': test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId'],
            'startDate': test_data['sailorApp']['shipEats']['startDate'],
            'endDate': test_data['sailorApp']['shipEats']['endDate']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) == 0:
            raise Exception('There is no menu item available to book')
        for _data in _content:
            check_assertions([
                'Name', 'MenuItemId', 'MenuItemNumber', 'VenueId', 'MenuItemType', 'MenuItemIngredients',
                'MenuItemPrices', 'CustomizationGroupMenuItems', 'MealPeriodMenuItems', 'MenuItemAllergies',
                'MenuItemCustomizationGroups', 'MenuItemExceptionWindows', 'MenuItemLifestyles', 'MenuItemNutritions',
                'MenuItemFilters', 'MenuItemOptions'], _data)
        for _data in _content:
            if len(_data['MenuItemPrices']) > 0 and len(_data['MealPeriodMenuItems']) > 0:
                test_data['sailorApp']['shipEats']['menuItem'] = _data
                break

    @pytestrail.case(17644851)
    def test_39_get_time_slots(self, config, test_data, rest_ship):
        """
        Get time slots
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/PreOrders/timeslots")
        params = {
            'venueId': test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId'],
            'startDate': test_data['sailorApp']['shipEats']['startDate'],
            'endDate': test_data['sailorApp']['shipEats']['endDate']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        for _data in _content:
            check_assertions([
                'VenueId', 'PreOrderSlotDetailId', 'PreOrderSlotDate', 'StartTime', 'EndTime', 'EditCutOffTime',
                'IsPreOrderAvailable', 'PreOrderSlots'], _data)

    @pytestrail.case(26152204)
    def test_40_get_order_wait_time(self, config, test_data, rest_ship):
        """
        Get ordered wait time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"v1/venues/{test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId']}/orderwaittimes")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if len(_content) == 0:
            raise Exception('There is no OrderTypeId available for the chosen value')
        for _data in _content:
            check_assertions([
                'VenueId', 'OrderWaitTimeId', 'OrderTypeId', 'MinWaitTime', 'MaxWaitTime', 'IsDeleted', 'WaitTimeId'],
                _data)
        test_data['sailorApp']['shipEats']['venue']['OrderTypeId'] = _content[0]['OrderTypeId']

    @pytestrail.case(12150708)
    def test_41_create_order(self, config, test_data, rest_ship, guest_data):
        """
        Create order
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders')
        body = {
            "GuestId": guest['reservationGuestId'],
            "AddedBy": guest['reservationGuestId'],
            "VenueId": test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId'],
            "OrderTypeId": test_data['sailorApp']['shipEats']['shipEatsEatNowOrderTypeId'],
            "OrderOriginId": test_data['sailorApp']['shipEats']['ShipEatsOrderOriginId'],
            "OrderDetails": [{
                "OrderQuantity": 1,
                "MenuItemId": test_data['sailorApp']['shipEats']['menuItem']['MenuItemId'],
                "UnitPrice": int(test_data['sailorApp']['shipEats']['menuItem']['MenuItemPrices'][0]['Price']),
                "UnitId": test_data['sailorApp']['shipEats']['menuItem']['MenuItemPrices'][0]['UnitId'],
                "Amount": int(test_data['sailorApp']['shipEats']['menuItem']['MenuItemPrices'][0]['Price']),
                "MenuItemOptionIds": [],
                "MenuItemOptionNames": [],
                "OrderAllergies": [{"AllergyId": test_data['sailorApp']['shipEats']['allergens']['id']}]
            }],
            "IsDeliveryChargeApplied": True,
            "Location": test_data['cabinNumber']                      
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if 'ReturnCode' and 'Message' in _content:
            if _content['Message'] == 'No account provided/found(check_id)':
                test_data['shipEats_order'] = False
                pytest.skip("Not able to create order due to charge id issue")
        check_assertions([
            'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'Location', 'OrderDate',
            'Status', 'GuestId', 'OrderNumber', 'AddedBy', 'Amount', 'OrderDetails', 'OrderAllergies'], _content)
        test_data['sailorApp']['shipEats']['orderResponse'] = _content
        test_data['shipEats_order'] = True
        assert 1 == _content['Status'], "Ship Eats order did not get Booked"

    @pytestrail.case(12150709)
    def test_42_verify_order_created(self, config, test_data, rest_ship, guest_data):
        """
        Verify that order got created
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['shipEats_order']:
            pytest.skip("Skipping as the order is not created.")
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders/search')
        body = {
            "StatusIds": "1,2,3,4",
            "GuestId": guest['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if not any(d['OrderId'] == test_data['sailorApp']['shipEats']['orderResponse']['OrderId'] for d in _content):
            raise Exception('Ship Eats order is not showing in recent orders for Sailor')

    @pytestrail.case(12150710)
    def test_43_cancel_order(self, config, test_data, rest_ship, guest_data):
        """
        cancel order
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['shipEats_order']:
            pytest.skip("Skipping as the order is not created.")
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"/v1/orders/{test_data['sailorApp']['shipEats']['orderResponse']['OrderId']}/cancel")
        body = {
            "OrderId": test_data['sailorApp']['shipEats']['orderResponse']['OrderId'],
            "VenueId": test_data['sailorApp']['shipEats']['venue']['Venue']['VenueId'],
            "OrderCancellations": [{
                "OrderId": test_data['sailorApp']['shipEats']['orderResponse']['OrderId'],
                "CancellationRequestedBy": guest['reservationGuestId'],
                "AddedBy": guest['reservationGuestId'],
                "CancellationReason": "Canceled by sailor"
            }]
        }
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content
        check_assertions(['ReturnCode', 'Message', 'OrderNumber', 'GuestId', 'OrderOriginId', 'OrderTypeId'], _content)
        assert 1003 == _content['ReturnCode'], "ReturnCode Mismatch!!"
        assert 'OrderSuccessfullyCancelled' == _content['Message'], "Message Mismatch!!"

    @pytestrail.case(12150707)
    def test_44_verify_order_cancelled(self, config, test_data, rest_ship, guest_data):
        """
        Verify that order got cancelled
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['shipEats_order']:
            pytest.skip("Skipping as the order is not created.")
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders/search')
        body = {
            "StatusIds": "1,2,3,4",
            "GuestId": guest['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if any(d['OrderId'] == test_data['sailorApp']['shipEats']['orderResponse']['OrderId'] for d in _content):
            raise Exception('Ship Eats order did not get cancelled for Sailor')

    @pytestrail.case(12150713)
    def test_45_search_in_help_support(self, config, rest_ship):
        """
        Verify search functionality in help and support
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), '/help-support/search')
        body = {
            "timeout": "60s",
            "searchTerm": "Sailor services",
            "isOnboard": True,
            "sort": [{"_score": {"order": "desc"}}]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth='user').content
        is_key_there_in_dict('took', _content)
        is_key_there_in_dict('_shards', _content)
        is_key_there_in_dict('hits', _content)

    @pytestrail.case(12150722)
    def test_46_toggle_reminders_in_notification(self, config, rest_ship, guest_data, test_data):
        """
        Turn off and on reminders toggle button in Notifications for oncruise
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                                                        '/guestpreferences/search/findbyreservationguestids')
        body = {
                "reservationGuestIds": [guest['reservationGuestId']]
                }
        _content = rest_ship.send_request(method='POST', url=url, json=body, auth="user").content
        is_key_there_in_dict('guestPreferences', _content['_embedded'])
        is_key_there_in_dict('guestPreferenceId', _content['_embedded']['guestPreferences'][0])
        test_data['guestPreferenceId'] = _content['_embedded']['guestPreferences'][0]['guestPreferenceId']

        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                                                        f"/guestpreferences/{test_data['guestPreferenceId']}")
        states = ["IS_OPT_IN_REMINDER_NO", "IS_OPT_IN_REMINDER_YES"]
        for state in states:
            body = {
                    "guestPreferenceId": test_data['guestPreferenceId'],
                    "reservationGuestId": guest['reservationGuestId'],
                    "preferenceCode": 'IS_OPT_IN_REMINDER',
                    "preferenceValueCode": state
                    }
            _content = rest_ship.send_request(method='PUT', url=url, json=body, auth="user").content
            is_key_there_in_dict('guestPreferenceId', _content)
            is_key_there_in_dict('preferenceValueCode', _content)
            assert _content['preferenceValueCode'] == body[
                                            "preferenceValueCode"], "Reminder toggle button not turned off and on"

    @pytestrail.case(67651960)
    def test_47_beauty_and_body_landing(self, config, rest_ship, guest_data, test_data):
        """
        To verify landing on beauty & body for ship side
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/discover/spacetype/Beauty---Body/landing")
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code,
            "path": "/Beauty---Body",
            "reservationNumber": test_data['reservationNumber'],
             }
        _content = rest_ship.send_request(method='GET', url=url, params=params, auth="user").content
        is_key_there_in_dict('spaces', _content)
        is_key_there_in_dict('header', _content)
        if len(_content['spaces']) > 0:
            for space in _content['spaces']:
                is_key_there_in_dict('name', space)
                is_key_there_in_dict('label', space)
                is_key_there_in_dict('externalId', space)
        else:
            raise Exception("No activity found on beauty and body page")
