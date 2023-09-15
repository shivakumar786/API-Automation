__author__ = 'Sarvesh.Singh'

from virgin_utils import *

@pytest.mark.SHORE
@pytest.mark.SAILOR_APP_SHORE
@pytest.mark.run(order=5)
class TestSailorAppShoreSide:
    """
    Test Suite to Test Sailor App
    """

    @pytestrail.case(186245)
    def test_01_start_up(self, config, test_data, rest_shore):
        """
        Get Links for all Services
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['sailorApp'] = dict()
        _url = urljoin(config.shore.url, "user-account-service/startup")
        _content = rest_shore.send_request(method="GET", url=_url, auth="Basic").content
        test_data['sailorApp'].update(_content)

    @pytestrail.case(186249)
    def test_02_user_account_service(self, test_data, rest_shore):
        """
        Get Links for all Services
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['sailorApp']['userProfileUrl']
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        for match in ['firstName', 'lastName', 'email']:
            assert test_data['signupGuest'][match].upper() == _content[match].upper(), f"ERROR: {match} not matching !!"

    @pytestrail.case(1064151)
    def test_03_get_wearable(self, config, request, test_data, rest_shore):
        """
        Check if User is able to get wearable notification after log in
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/sailorapp_wearable.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "guest-dashboard/wearable/delivery")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(1064152)
    def test_04_verify_cabin_number(self, config, test_data, rest_shore):
        """
        Check if User is able to get wearable notification after log in
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/guest-dashboard/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if test_data['cabin']['cabinNumber'] != "GTY":
            deck = _content['voyageTicket']['deck']
            number = _content['voyageTicket']['cabinNumber']
            side = _content['voyageTicket']['cabinSide']
            assert f"{deck}{number}{side}" == test_data['cabin']['cabinNumber'], f"Cabin Number Mismatch !!"

    @pytestrail.case(186246)
    def test_05_discovery_start_up(self, config, test_data, rest_shore):
        """
        Start Discovery
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "discover/startup")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('configurations', _content)
        test_data['sailorApp'].update(_content)

    @pytestrail.case(186220)
    def test_06_discover_landing(self, config, test_data, rest_shore):
        """
        Discovery Landing
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('discoverItems', _content)
        sequence = ['Lineup', 'Ship', 'Ports', 'Guides']
        items = _content['discoverItems']
        for count, item in enumerate(items):
            if items[count]['title'] != sequence[count]:
                raise Exception(f"{sequence[count]} not found at index {count} !!")

    @pytestrail.case(1064154)
    def test_07_discover_lineup_landing(self, config, test_data, rest_shore):
        """
        Discovery Lineup Landing
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/lineup/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(1064155)
    def test_08_discover_ship_landing(self, config, test_data, rest_shore):
        """
        Discovery Ship Landing
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/ship/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(1064156)
    def test_09_discover_guides_landing(self, config, request, test_data, rest_shore):
        """
        Discovery Guides Landing
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/discovery_guides.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/guides/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(186208)
    def test_10_dashboard_settings(self, config, rest_shore):
        """
        Verify settings call on dashboard
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, "url.path.guestbff"), "/ars/settings")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('timeSlotsFilter', _content)
        is_key_there_in_dict('activityLevelMapping', _content)
        is_key_there_in_dict('activitySubTypes', _content)
        is_key_there_in_dict('cardTypes', _content)

    @pytestrail.case(1064157)
    def test_11_services_splash_screen(self, config, request, test_data, rest_shore):
        """
        Check if the splash screen in services is getting displayed
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/services_splash_screens.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/splashscreens/eats")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

    @pytestrail.case(186247)
    def test_12_activity_reservation_resources(self, config, test_data, rest_shore):
        """
        Activity Reservation
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/resources")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['sailorApp']['assets'] = _content['assets']

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(370)
    def test_13_get_port_code(self, config, test_data, rest_shore):
        """
        Get Port Code
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {"reservation-number": test_data['reservationNumber']}
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/reservation/summary/")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('voyageDetails', _content)
        is_key_there_in_dict('reservationId', _content)
        is_key_there_in_dict('reservationNumber', _content)
        is_key_there_in_dict('paymentStatusCode', _content)
        is_key_there_in_dict('guestCount', _content)
        is_key_there_in_dict('guestsSummary', _content)
        is_key_there_in_dict('_links', _content)
        test_data['startDateTime'] = _content['voyageDetails']['startDateTime']
        test_data['endDateTime'] = _content['voyageDetails']['endDateTime']

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(186221)
    def test_14_ports_landing(self, config, test_data, rest_shore):
        """
        Get Port Code
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/ports/landing")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        for _port_code in _content['destinationCardCarousel']:
            is_key_there_in_dict('portCode', _port_code)
        test_data['sailorApp']['port_details'] = dict()
        random_port = random.choice(_content['destinationCardCarousel'][1:-1])
        test_data['sailorApp']['port_details'] = random_port

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(7292053)
    def test_15_set_pin(self, config, test_data, rest_shore):
        """
        Set the Pin in sailor application and verification of supportive API's
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/guest-dashboard/wearable/country/list")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        if _content is '' and len(_content) == 0:
            raise Exception("countries not available in response !!")

        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/account/setpin")
        body = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "pin": generate_phone_number(4)
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user")

        params = {
            "parts": test_data['voyage']['id']
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/reservationguests/search")
        body = {"userReservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        for guests in _content['_embedded']['reservationGuestDetailsResponses']:
            for resdetails in guests['reservationDetails']:
                if resdetails['reservationGuestId'] == test_data['signupGuest']['reservationGuestId']:
                    if resdetails['isPinAvailable']:
                        return
        else:
            raise Exception("Pin is not set for the Guest !!")

    @pytestrail.case(12768800)
    def test_16_verify_current_activities(self, config, test_data, rest_shore):
        """
        Verify Deleted Activities
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            logger.warn('Fresh Sailor already have a linked activity')

    @pytestrail.case(186225)
    def test_17_help_support_resource(self, config, test_data, rest_shore):
        """
        Help and support resource
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/help-support/resources")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['sailorApp']['configurations'].update(_content['assets'])

    @pytestrail.case(186226)
    def test_18_messaging_resource(self, config, test_data, rest_shore):
        """
        Message Resource
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/messaging/resources")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('assets', _content)
        test_data['sailorApp']['configurations'].update(_content['assets'])

    @pytestrail.case(186227)
    def test_19_my_voyage_dashboard(self, config, test_data, rest_shore, guest_data):
        """
        My Voyage Dash-Board
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": guest_data[0]['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/dashboard")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('stateroom', _content)
        is_key_there_in_dict('bookingStartDate', _content)
        is_key_there_in_dict('timeSlots', _content)
        is_key_there_in_dict('categories', _content)
        is_key_there_in_dict('shipCode', _content)
        test_data['sailorApp']['configurations'].update(_content)

    @pytestrail.case(398)
    def test_20_user_account_service_user_profile(self, config, test_data, rest_shore):
        """
        User account Service and User Profile
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(config.shore.url, "user-account-service/userprofile")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('lastName', _content)
        is_key_there_in_dict('firstName', _content)
        is_key_there_in_dict('bookingInfo', _content)
        is_key_there_in_dict('birthDate', _content)
        is_key_there_in_dict('email', _content)
        is_key_there_in_dict('isPasswordExist', _content)
        is_key_there_in_dict('personId', _content)
        is_key_there_in_dict('personTypeCode', _content)
        test_data['sailorApp']['configurations'].update(_content)
        test_data['guestId'] = _content['personId']

    @pytestrail.case(186250)
    def test_21_voyage_account_settings_lookup(self, config, test_data, rest_shore):
        """
        Voyage account settings lookup
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/lookup")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('referenceData', _content)
        test_data['sailorApp']['configurations'].update(_content)

    @pytestrail.case(186229)
    def test_22_my_voyage_accounts_settings(self, config, request, test_data, rest_shore):
        """
        My Voyage account settings
        :param config:
        :param test_data:
        :param rest_shore:
        :param request:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath,
                             'test_data/verification_data/my_voyage_accounts_setting.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)

    @pytestrail.case(1065280)
    def test_23_voyage_account_setting_personal_info(self, config, test_data, rest_shore):
        """
        Check if the first and last name is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _num = test_data['reservationNumber']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/personal")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content

        if _content['firstName'] != test_data['signupGuest']['firstName']:
            raise Exception("First is not matching under the personal information of Sailor App !!")

        if _content['lastName'] != test_data['signupGuest']['lastName']:
            raise Exception("Last name is not matching under the personal information of Sailor App !!")

    @pytestrail.case(186210)
    def test_24_verify_my_voyage_dashboard(self, config, test_data, rest_shore):
        """
        Check dashboard API work fine so Guest app Dashboard should display proper
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/dashboard")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if test_data['cabin']['cabinNumber'] != "GTY":
            assert test_data['cabin']['cabinNumber'] == _content['stateroom'], f"Cabin Number Mismatch !!"
        is_key_there_in_dict('imageUrl', _content)
        is_key_there_in_dict('profileImageUrl', _content)
        is_key_there_in_dict('myWalletUrl', _content)
        is_key_there_in_dict('timeSlots', _content)
        is_key_there_in_dict('bigCardCategoryCodes', _content)
        is_key_there_in_dict('categories', _content)

    @pytestrail.case(12150696)
    def test_25_verify_pre_cruise_ship_eats(self, config, test_data, rest_shore):
        """
        Check the Ship Eats page content on Pre cruise mode
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "spacename": ""
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/splashscreens/eats")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        ship_dict = {
            "title": "Ship Eats Delivery",
            'shipEatsDelivery': "ShipEats Delivery",
            "description": "Our spin on room service-and-beyond. You'll be able to:",
            "number_one": "1",
            "header_one": "Order the best bites and bevs",
            "number_two": "2",
            "header_two": "Delivered right to you",
            "number_three": "3",
            "header_three": "Breakfast in bed, but also…"
        }
        assert _content['title'] == ship_dict["title"], "Title is not matching on Ship Eats page !!"
        assert _content['shipEatsDelivery'] == ship_dict[
            "shipEatsDelivery"], "shipEatsDelivery is not matching on Ship Eats page !!"
        assert _content['description'] == ship_dict["description"], "Ship Eats page description is not matching  !!"
        for shipEats in _content['shipEats']:
            if shipEats['numberLabel'] == ship_dict["number_one"]:
                assert shipEats[
                           'header'] == "Order the best bites and bevs", "Header 1 is not Mismatch on Ship Eats page !!"
            if shipEats['numberLabel'] == ship_dict["number_two"]:
                assert shipEats['header'] == ship_dict["header_two"], "Header 2 is not Mismatch on Ship Eats page !!"
            if shipEats['numberLabel'] == ship_dict["number_three"]:
                assert shipEats['header'] == ship_dict["header_three"], "Header 2 is not Mismatch on Ship Eats page !!"
        is_key_there_in_dict('recentOrdersIconImageURL', _content)
        is_key_there_in_dict('portholeImage', _content)
        is_key_there_in_dict('backActionURL', _content)

    @pytestrail.case(12150697)
    def test_26_verify_pre_cruise_cabin_service(self, config, test_data, rest_shore):
        """
        Check the Cabin Service page content on Pre cruise mode
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "spacename": ""
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/splashscreens/cabin")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        splash_dict = {
            "title": "Making your cabin... ",
            "description": "Once you're on board, come back here for all your cabin wants and needs.",
        }
        assert _content['title'] == splash_dict["title"], "Title is not matching on Cabin page !!"
        assert _content['description'] == splash_dict["description"], "Ship Eats page description is not matching!!"
        is_key_there_in_dict('backButtonIconImageURL', _content)
        is_key_there_in_dict('portholeImage', _content)
        is_key_there_in_dict('backActionURL', _content)

    @pytestrail.case(16851387)
    def test_27_verify_discover_search(self, config, test_data, rest_shore):
        """
        Verify the Discover search landing page
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "iscoaching": "true"
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discoversearch/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        assert _content['suggestionsHeader'] == "Suggestions", "Search Suggestion is not matching !!"
        is_key_there_in_dict('closeBtnImgUrl', _content)
        is_key_there_in_dict('searchIconUrl', _content)
        is_key_there_in_dict('searchDefaultValue', _content)
        is_key_there_in_dict('clearSearchBtnLabel', _content)
        test_data['suggestionList'] = _content['suggestionList']
        is_key_there_in_dict('suggestionList', _content)
        if len(_content['suggestionList']) == 0:
            raise Exception("suggestionList length is Zero!!")

    @pytestrail.case(15833646)
    def test_28_verify_discover_search_functionality(self, config, test_data, rest_shore):
        """
        Verify the Discover search functionality
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "voyagenumber": test_data['voyage']['id'],
            "shipCode": config.ship.code
        }

        for suggestion in test_data['suggestionList']:
            body = {
                "searchTerm": suggestion
            }
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discoversearch/search")
            try:
                _content = rest_shore.send_request(method="POST", url=_url, params=params, json=body, auth="user").content
            except Exception as e:
                logger.info(f"Not able to search {suggestion} in Discover search.")
                raise Exception(e)
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

    @pytestrail.case(12150720)
    def test_29_my_wallet_pre_cruise(self, config, test_data, rest_shore):
        """
        Verify the Wallet call in Pre Cruise mode
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/mywallet")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('myWalletkey', _content)
        is_key_there_in_dict('additionalInformation', _content)

    @pytestrail.case(24862302)
    def test_30_travel_documents_in_setting(self, config, test_data, rest_shore):
        """
        Verification of Travel Document in Setting
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/sailingdocuments/landing")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

        is_key_there_in_dict('travelDocuments', _content['sailingDocuments'])
        is_key_there_in_dict('contracts', _content['sailingDocuments'])
        is_key_there_in_dict('voyageContract', _content['sailingDocuments'])
        is_key_there_in_dict('embarkationHealthCheck', _content['sailingDocuments'])

        params = {
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/traveldocuments")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

        is_key_there_in_dict('passport', _content)
        is_key_there_in_dict('visas', _content)
        is_key_there_in_dict('arc', _content)
        is_key_there_in_dict('esta', _content)
        is_key_there_in_dict('postCruiseInfo', _content)

    @pytestrail.case(24862303)
    def test_31_voyage_contract_in_setting(self, config, test_data, rest_shore):
        """
        Verification of Voyage Contract in Setting
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-number": test_data['reservationNumber'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/contracts/voyagecontract")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

        is_key_there_in_dict('voyageContractPage', _content)
        is_key_there_in_dict('signedContractInformation', _content)

    @pytestrail.case(12150699)
    def test_32_help_and_support(self, config, rest_shore):
        """
        Verify help and support response in pre cruise mode
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/help-support/helps")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('categories', _content)

        for help_categories in _content['categories']:
            is_key_there_in_dict('cta', help_categories)
            is_key_there_in_dict('articles', help_categories)
            is_key_there_in_dict('name', help_categories)
            if help_categories['cta'] not in ['Before You Sail', 'The Days at Sea', 'Back on Dry Land']:
                raise Exception(f"{help_categories['cta']} is not exist in response")
            if len(help_categories['articles']) == 0:
                raise Exception(f"{help_categories['cta']} sub-sections are not present under articles")

    @pytestrail.case(29946976)
    def test_33_myvoyage_addons(self, config, rest_shore, test_data):
        """
        Verify the My voyage addons API
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        params = {
            "guestId": test_data['guestId'],
            "reservationNumber": test_data['reservationNumber'],
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/addons")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('addons', _content)

    @pytestrail.case(29967425)
    def test_34_fill_voyage_well_form(self, config, rest_shore, test_data):
        """
        Verify the voyage well form filling
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        params = {
            "reservationguestid": test_data['signupGuest']['reservationGuestId'],
        }
        body = {
            "signedBy": f"{test_data['signupGuest']['firstName']} {test_data['signupGuest']['lastName']}",
            "signedId": test_data['signupGuest']['reservationGuestId'],
            "signedByEmail": test_data['signupGuest']['email'],
            "signedDate": f"{str(datetime.now(tz=pytz.utc).date())}T10:09:47",
            "isSigned": 'true'
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "guests/contract/cruisewell/")
        _content = rest_shore.send_request(method="POST", url=_url, json=body, params=params, auth="user").content

        _content = rest_shore.send_request(method="GET", url=_url, json=body, params=params, auth="user").content
        assert _content[
                   'signedBy'] == f"{test_data['signupGuest']['firstName']} {test_data['signupGuest']['lastName']}", "Signed by not matching!!"
        assert _content['signedByEmail'] == test_data['signupGuest']['email'], "Signed by Email is not matching!!"

    @pytestrail.case(30406676)
    def test_35_modify_email_address_voyage_well(self, config, rest_shore, guest_data, test_data):
        """
        To modify the email address in the voyage well acknowledgement form
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "guests/contract/cruisewell/")
        params = {
            "reservationguestid": guest_data[0]["reservationGuestId"]
        }
        body = {
            "isSigned": True,
            "signedBy": f"{guest_data[0]['FirstName']} {guest_data[0]['LastName']}",
            "signedDate": f"{str(datetime.now(tz=pytz.utc).date())}T10:10:50",
            "signedByEmail": "vertical-qa@decurtis.com",
        }
        rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        test_data['voyageWellDetails'] = _content
        assert test_data['voyageWellDetails']['isSigned'], "Voyage well contract did not get sign."
        assert test_data['voyageWellDetails'][
                   'signedByEmail'] == 'vertical-qa@decurtis.com', "Email address entered while completing voyage well acknowledgement form is not matching."

    @pytestrail.case(32788756)
    def test_36_voyage_account_setting_reservation(self, config, test_data, rest_shore):
        """
        Check if the reservation guestId and guestId is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/user/reservations")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        assert len(_content['guestBookings']) != 0, 'Guest Booking not available in reservation'
        is_key_there_in_dict("guestBookings", _content)
        is_key_there_in_dict("pageDetails", _content)
        is_key_there_in_dict("reservationGuestId", _content['guestBookings'][0])
        assert test_data['signupGuest']['reservationId'] == _content['guestBookings'][0][
            'reservationId'], 'Same ReservationId is not available in Voyage Setting'
        assert test_data['signupGuest']['reservationGuestId'] == _content['guestBookings'][0][
            'reservationGuestId'], 'Same ReservationId is not available in Voyage Setting'

    @pytestrail.case(32788757)
    def test_37_voyage_account_setting_communication_preferences(self, config, rest_shore):
        """
        Check if the essentialsPreference is coming in communication_preferences
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'),
                       "/voyage-account-settings/user/communicationpreferences")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        assert len(_content) != 0, 'communication preference is not coming'
        is_key_there_in_dict("pageDetails", _content)
        is_key_there_in_dict("userNotifications", _content)

    @pytestrail.case(32788758)
    def test_38_voyage_account_setting_wearable_content(self, config, rest_shore):
        """
        Check if the contents are coming for wearble
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/wearable/content")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        assert len(_content) != 0, 'The Band and Pin Page is coming blank'
        is_key_there_in_dict("statusLocked", _content)
        is_key_there_in_dict("successPinChangedBody", _content)

    @pytestrail.case(32788759)
    def test_39_voyage_account_setting_legals(self, config, rest_shore):
        """
        Check if the contents are coming in terms and condition
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/content/legal")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        assert len(_content['general']['content']) != 0, "no genral content"
        assert len(_content['mobile']['content']) != 0, "no content in mobile"
        assert len(_content['privacy']['content']) != 0, "no content in privacy"
        assert len(_content['cookie']['content']) != 0, "no content in cookie"
        is_key_there_in_dict("heading", _content)
        is_key_there_in_dict("general", _content)
        is_key_there_in_dict("mobile", _content)
        is_key_there_in_dict("privacy", _content)
        is_key_there_in_dict("cookie", _content)

    @pytestrail.case(32788760)
    def test_40_voyage_account_setting_login(self, config, rest_shore):
        """
        Check if the change email and password is enabled or not
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/login/landing")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict("labels", _content)
        is_key_there_in_dict("loginDetails", _content)
        is_key_there_in_dict("changeEmail", _content['loginDetails'])
        is_key_there_in_dict("changePassword", _content['loginDetails'])
        is_key_there_in_dict("isEnable", _content['loginDetails']['changeEmail'])
        assert _content['loginDetails']['changeEmail']['isEnable'] == True, 'change email option is in disable mode'
        assert _content['loginDetails']['changePassword'][
                   'isEnable'] == True, 'change password option is in disable mode'

    @pytestrail.case(32788763)
    def test_41_verify_message_dash_board_landing(self, config, test_data, rest_shore):
        """
        Check if User is able to get all pre-cruise message content on dashboard
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservationNumber": test_data['reservationNumber']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/messaging/dashboard")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('isPreCruise', _content)
        if not _content['isPreCruise']:
            raise Exception('Default precruise should be true')

    @pytestrail.case(32788762)
    def test_42_verify_contact_in_message(self, config, test_data, rest_shore):
        """
        Check if User is able to get all cabin mates names on dashboard
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservationId": test_data['signupGuest']['reservationId'],
            "personId": test_data['signupGuest']['reservationGuestId'],
            "personTypeCode": "RG"
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/messaging/contacts")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        assert len(_content) != 0, 'contact details page should contain sailormate and cabinmate name'
        is_key_there_in_dict('cabinMates', _content)
        is_key_there_in_dict('sailorMates', _content)

    @pytestrail.case(186209)
    def test_43_access_to_cabin_mates_contacts(self, config, guest_data, rest_shore):
        """
        Deny / Allow cabin mate to see what you are attending
        :param config:
        :param guest_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, "url.path.guestbff"), "/messaging/contact/preferences")
        body_deny = {
                "personId": guest_data[0]['reservationGuestId'],
                "connectionPersonId": guest_data[1]['reservationGuestId'],
                "isEventVisibleCabinMates": False
                }
        _content = rest_shore.send_request(method="POST", url=_url, json=body_deny, auth="user").content
        body_allow = {
            "personId": guest_data[0]['reservationGuestId'],
            "connectionPersonId": guest_data[1]['reservationGuestId'],
            "isEventVisibleCabinMates": True
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body_allow, auth="user").content

    @pytestrail.case(33219476)
    def test_44_voyage_account_setting_update_gender(self, config, rest_shore):
        """
        Update Gender of primary user
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/user/personal")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('pageDetails', _content)
        is_key_there_in_dict('genderCode', _content)
        if _content['genderCode'] == "M":
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/user/personal")
            body = {
                "firstName": _content['firstName'],
                "lastName": _content['lastName'],
                "birthDate": _content['birthDate'],
                "genderCode": "F",
                "preferredName": _content['preferredName']
            }
            _content = rest_shore.send_request(method="PUT", url=_url, json=body, auth="user").content
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/user/personal")
            _content_update = rest_shore.send_request(method="GET", url=_url, auth="user").content
            is_key_there_in_dict('genderCode', _content_update)
            assert _content_update['genderCode'] != "M", 'Gender code is not updated'
        elif _content['genderCode'] == "F":
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/user/personal")
            body = {
                "firstName": _content['firstName'],
                "lastName": _content['lastName'],
                "birthDate": _content['birthDate'],
                "genderCode": "M",
                "preferredName": _content['preferredName']
            }
            _content = rest_shore.send_request(method="PUT", url=_url, json=body, auth="user").content
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "voyage-account-settings/user/personal")
            _content_update = rest_shore.send_request(method="GET", url=_url, auth="user").content
            is_key_there_in_dict('genderCode', _content_update)
            assert _content_update['genderCode'] != "F", 'Gender code is not updated'

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(42804011)
    def test_45_add_card(self, config, test_data, rest_shore):
        """
        Add Card
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/payment")
        method = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('savedCards', method)

        transaction_Id = generate_guid()
        body = {
            "clientTransactionId": transaction_Id,
            "signedFields": "clientTransactionId,currencyCode,clientReferenceNumber,transactionType,signedFields",
            "currencyCode": "USD",
            "clientReferenceNumber": test_data['reservationNumber'],
            "transactionType": "create_payment_token",
            "amount": "0"
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/signature")
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth='user').content
        is_key_there_in_dict('signedFields', _content)
        is_key_there_in_dict('signedTimeStamp', _content)
        is_key_there_in_dict('signature', _content)
        signed_fields = _content['signedFields']
        signed_time_stamp = _content['signedTimeStamp']
        signature = _content['signature']

        url = urljoin(config.shore.url, "user-account-service/userprofile")
        _content = rest_shore.send_request(method="GET", url=url, json=body, auth='user').content
        is_key_there_in_dict('userNotifications', _content)
        is_key_there_in_dict('userId', _content['userNotifications'][0])
        userId = _content['userNotifications'][0]['userId']

        url = urljoin(config.shore.url, "payment-bff/initiatepayment")
        body = {
            "billToCountryCode": "USA",
            "lastName": test_data['signupGuest']['lastName'],
            "signedTimeStamp": signed_time_stamp,
            "signature": signature,
            "billToState": test_data['signupGuest']['addresses'][0]['stateCode'],
            "clientTransactionId": transaction_Id,
            "signedFields": signed_fields,
            "clientReferenceNumber": test_data['reservationNumber'],
            "billToCity": test_data['signupGuest']['addresses'][0]['city'],
            "shipToCity": test_data['signupGuest']['addresses'][0]['city'],
            "billToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
            "shipToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
            "shipToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
            "requestData": "dummy",
            "shipToState": test_data['signupGuest']['addresses'][0]['stateCode'],
            "shipToLastName": test_data['signupGuest']['lastName'],
            "amount": "0",
            "billToLine2": test_data['signupGuest']['addresses'][0]['lineOne'],
            "shipToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
            "billToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
            "shipToFirstName": test_data['signupGuest']['firstName'],
            "consumerId": userId,
            "clientUserIP": "103.93.185.99",
            "transactionType": "create_payment_token",
            "firstName": test_data['signupGuest']['firstName'],
            "consumerType": "DXPUserId",
            "shipToCountryCode": "AT",
            "currencyCode": "USD",
            "locale": "en-US",
            "targetUrl": "https://localhost:8443"
        }
        _initial = rest_shore.send_request(method="POST", url=url, json=body, auth='user').content
        is_key_there_in_dict('sessionKey', _initial)
        is_key_there_in_dict('transactionId', _initial)

        url = 'https://demohpp.fmsapps.com/hpp/authorization'
        if config.envMasked == 'STAGE':
            url = url.replace('demohpp', 'hppstaging')
        body = {
            "bluefin_token": "",
            "payment_token": _initial['sessionKey'],
            "txn_amount": "0.0",
            "txn_currency": "USD",
            "credit_card": {
                "payment_method_type": "new_card",
                "card_number": "4111111111111111",
                "card_scheme": "visa",
                "holder_full_name": f"{test_data['signupGuest']['firstName']} {test_data['signupGuest']['lastName']}",
                "card_expiry_month": "06",
                "card_expiry_year": "2033",
                "card_cvc": "123"
            },
            "payment_type": "ACCOUNT_STATUS",
            "origin": {},
            "bill_to_details": {
                "first_name": test_data['signupGuest']['firstName'],
                "last_name": test_data['signupGuest']['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": test_data['signupGuest']['addresses'][0]['city'],
                "stateId": "6557",
                "postal_code": test_data['signupGuest']['addresses'][0]['zipCode'],
                "country": test_data['signupGuest']['addresses'][0]['countryCode']
            },
            "ship_as_bill_details": "true",
            "ship_to_details": {
                "first_name": test_data['signupGuest']['firstName'],
                "last_name": test_data['signupGuest']['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": test_data['signupGuest']['addresses'][0]['city'],
                "postal_code": test_data['signupGuest']['addresses'][0]['zipCode'],
                "country": test_data['signupGuest']['addresses'][0]['countryCode']
            }
        }
        _auth = rest_shore.send_request(method="POST", url=url, json=body, auth=None).content
        is_key_there_in_dict('payment_token', _auth)
        is_key_there_in_dict('status', _auth)
        is_key_there_in_dict('status_code', _auth)
        is_key_there_in_dict('response_message', _auth)
        is_key_there_in_dict('card_token', _auth)
        is_key_there_in_dict('expiry_date', _auth['card_token'])
        is_key_there_in_dict('card_scheme', _auth['card_token'])
        is_key_there_in_dict('receipt_reference', _auth['card_token'])
        is_key_there_in_dict('masked_pan', _auth['card_token'])
        is_key_there_in_dict('token_provider', _auth['card_token'])
        assert _auth['status'] == 'SUCCESS', f"ERROR: Payment Status !!"
        assert _auth['response_message'] == 'Success', f"ERROR: Payment Response Message !!"
        test_data['paymentDetails'] = _auth

        url = _initial['_links']['transactionUrl']['href']
        body = {
            "transactionId": _initial['transactionId'],
            "billToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
            "billToLine2": test_data['signupGuest']['addresses'][0]['lineOne'],
            "billToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
            "billToCity": test_data['signupGuest']['addresses'][0]['city'],
            "billToState": test_data['signupGuest']['addresses'][0]['stateCode'],
            "billToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
            "cardUsername": f"{test_data['signupGuest']['firstName']} {test_data['signupGuest']['lastName']}",
            "cvvNumber": 123,
            "cardExpiryMonth": _auth['card_token']['expiry_date'][2::],
            "cardExpiryYear": _auth['card_token']['expiry_date'][0:2],
            "paymentToken": _auth['payment_token'],
            "gatewayPaymentToken": _auth['payment_token'],
            "isSaveCard": True,
            "cardScheme": _auth['card_token']['card_scheme'],
            "receiptReference": _auth['card_token']['receipt_reference'],
            "maskedPan": _auth['card_token']['masked_pan'],
            "tokenProvider": _auth['card_token']['token_provider'],
            "shipToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
            "shipToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
            "shipToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
            "shipToCity": test_data['signupGuest']['addresses'][0]['city'],
            "shipToState": test_data['signupGuest']['addresses'][0]['stateCode'],
            "shipToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
            "paymentMode": 'CARD',
            "status": _auth['status'],
            "statusCode": _auth['status_code'],
            "utcOffset": -330
        }
        _transaction = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/payment")
        method = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('savedCards', method)
        test_data['cardId'] = method['savedCards'][0]['paymentToken']
        assert len(method['savedCards']) != 0, "Card not saved successfully!!"

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(42804012)
    def test_46_remove_card(self, config, test_data, rest_shore):
        """
        Remove Card
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'),
                       f"/voyage-account-settings/user/cards/{test_data['cardId']}")
        rest_shore.send_request(method="DELETE", url=_url, auth="user")
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/payment")
        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('savedCards', _content)
        assert len(_content['savedCards']) == 0, "Card not removed successfully!!"

    @pytestrail.case(32788761)
    def test_47_dashboard_port_details(self, config, test_data, guest_data, rest_shore):
        """
        To verify port details should available on dashboard shore side
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/guest-dashboard/content/ports")
        params = {
                "reservation-id": guest_data[0]['reservationId'],
                "voyage-number": test_data['voyage']['id'],
                "reservation-guest-id": guest_data[0]['reservationGuestId'],
                "reservation-number": test_data['reservationNumber'],
                "sailing-package": test_data['voyage']['packageCode']
                  }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('ports', _content)
        for port in _content['ports']:
            is_key_there_in_dict('portCode', port)
            is_key_there_in_dict('isSeaDay', port)
            is_key_there_in_dict('itineraryDay', port)

    @pytestrail.case(67651957)
    def test_48_verify_dashboard_quick_links(self, config, test_data, guest_data, rest_shore):
        """
        To verify quick links are available on dashboard shore side
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/guest-dashboard/quicklinks")
        params = {
                  "reservation-guest-id": guest_data[0]['reservationGuestId'],
                  'reservation-id': guest_data[0]['reservationId'],
                  'reservation-number': test_data['reservationNumber'],
                  'shipCode': config.ship.code
                  }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('taskLinkDetails', _content)
        is_key_there_in_dict('exprienceLinkDetails', _content)
        is_key_there_in_dict('taskLinks', _content['taskLinkDetails'])
        is_key_there_in_dict('exprienceLinks', _content['exprienceLinkDetails'])

        task_links_list = ['addContact', 'viewShipVenue', 'viewAgenda', 'viewWallet', 'cabinServices', 'shipEatsDelivery']
        experience_links_list = ['restaurant', 'shoreThing', 'event', 'treatment', 'bartabAddon']
        for link in _content['taskLinkDetails']['taskLinks']:
            is_key_there_in_dict('taskName', link)
            assert link['taskName'] in task_links_list, f"Quick link not displayed on dashboard for {link['title']}"

        for link in _content['exprienceLinkDetails']['exprienceLinks']:
            is_key_there_in_dict('exprienceName', link)
            assert link['exprienceName'] in experience_links_list, f"Quick link not displayed on dashboard for {link['title']}"

@pytest.mark.skip(reason='DCP-124726')
@pytest.mark.SHORE
@pytest.mark.SAILOR_APP_SHORE
@pytest.mark.run(order=6)
class TestActivities:
    """
        Test Suite For ShoreEx, dining, Lineup
    """

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(186222)
    def test_01_list_activities(self, config, test_data, rest_shore):
        """
        List all Activities
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-id": test_data['signupGuest']['reservationId'],
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "shipCode": config.ship.code
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/discover/ports/landing")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('destinationCardCarousel', _content)
        start_date = _content['destinationCardCarousel'][1]['arrivalTime']
        end_date = _content['destinationCardCarousel'][1]['departureTime']
        port_code = _content['destinationCardCarousel'][1]['portCode']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        body = {
            "voyageNumber": test_data['voyage']['id'],
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "categoryCode": "PA",
            "guestCount": guest_count,
            "portCode": port_code,
            "startDate": start_date,
            "startTime": "",
            "endDate": end_date,
            "endTime": "",
            "subTypeId": ""
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content
        is_key_there_in_dict('activities', _content)
        if len(_content['activities']) == 0:
            test_data['excursionAvailableShore'] = False
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        test_data['excursionAvailableShore'] = True
        is_key_there_in_dict('filterCategories', _content)
        is_key_there_in_dict('preCruise', _content)
        is_key_there_in_dict('page', _content)

        # Filter out activities which are available and have more than 1 activity slots
        test_data['sailorApp']['activities'] = [x for x in _content['activities'] if
                                                len(x['activitySlots']) > 0 and x['isAvailable']]
        if len(test_data['sailorApp']['activities']) == 0:
            test_data['excursionAvailableShore'] = False
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

    @pytestrail.case(5313656)
    def test_02_validate_activities_data(self, test_data):
        """
        Validate Activities Data, so that anyone of these can be picked and booked
        :param test_data:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        fields = [
            'displayName', 'shortDescription', 'longDescription', 'imageUrl', 'amount', 'startTime',
            'currencyCode', 'activityCode', 'activitySlots', 'portCode', 'isBookingEnabled', 'isAvailable',
            'isFavourite', 'isNotifyEnabled', 'isSubscribed', 'guestDetails', 'mobileHighlightImageUrl',
            'tabletHighlightImageUrl', 'highlightDetails', 'introduction', 'instructionDetails', 'confirmationImage',
            'isMultipleBookingAllowed', 'disclaimers', 'info', 'appointments', 'waiverOpeningDuration', 'waiverCode',
            'categoryCode', 'primaryCategory', 'editorialBlocks', 'isSignature', 'bookingCloseDuration'
        ]
        for activity in test_data['sailorApp']['activities']:
            for field in fields:
                is_key_there_in_dict(field, activity)

    @pytestrail.case(12150701)
    def test_03_validate_excursion_filter(self, config, test_data, rest_shore):
        """
        Validate all filters in excursion
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        start_time = {'morning': "06:00:00", 'afternoon': "12:00:00", 'night': "18:00:00"}
        end_time = {'morning': "11:59:59", 'afternoon': "17:59:59", "night": "23:59:59"}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        for duration in start_time.keys():
            body = {
                    "categoryCode": "PA",
                    "reservationNumber": test_data['reservationNumber'],
                    "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
                    "voyageNumber": test_data['voyage']['id'],
                    "portCode": test_data['sailorApp']['port_details']['portCode'],
                    "guestCount": guest_count,
                    "startDate": test_data['sailorApp']['port_details']['arrivalTime'],
                    "startTime": start_time[duration],
                    "endDate": test_data['sailorApp']['port_details']['departureTime'],
                    "endTime": end_time[duration],
                    "subTypeId": ""
                    }
            _content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content
            is_key_there_in_dict('filterCategories', _content)
            is_key_there_in_dict('activities', _content)
            is_key_there_in_dict('strings', _content)
            is_key_there_in_dict('preCruise', _content)

    @pytestrail.case(1065279)
    def test_04_add_excursion_to_love_list(self, config, test_data, rest_shore):
        """
        Add excursion to love list
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/favourites")
        test_data['sailorApp']['chosenActivity'] = random.choice(test_data['sailorApp']['activities'])
        slots = [x for x in test_data['sailorApp']['chosenActivity']['activitySlots'] if
                 x['isEnabled'] and x['isInventoryAvailable'] and x['inventoryCount'] > 1]

        # Choose Two Slots for Activities
        first_slot = random.choice(slots)

        test_data['sailorApp']['chosenActivity']['activitySlots'] = first_slot

        activity_code = test_data['sailorApp']['chosenActivity']['activityCode']
        body = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "categoryCode": test_data['sailorApp']['chosenActivity']['categoryCode'],
            "activityCode": activity_code,
            "isFavourite": True
        }
        _content = rest_shore.send_request(method="PUT", url=url, json=body, auth="user").content

        params = {
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "categoryCodes": test_data['sailorApp']['chosenActivity']['categoryCode'],
            "size": 10
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/favourites")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        for favourite in _content['favourites']:
            if favourite['activityCode'] == activity_code:
                break
        else:
            raise Exception(f"{activity_code} Excursion Not Added to the love list in Sailor App")

    @pytestrail.case(186224)
    def test_05_book_activities(self, config, test_data, guest_data, rest_shore):
        """
        Book activities
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['sailorApp']['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'], "isGift": False,
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'], "guestId": test_data['signupGuest']['guestId']
            }],
            "activitySlotCode": test_data['sailorApp']['chosenActivity']['activitySlots']['activitySlotCode'],
            "accessories": [], "totalAmount": test_data['sailorApp']['chosenActivity']['amount'], "operationType": None,
            "currencyCode": test_data['sailorApp']['chosenActivity']['currencyCode']
        }
        try:
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        except Exception as exp:
            if "Booking already exists for following person" in exp.args[0]:
                test_data['excursion_already_booked'] = True
                pytest.skip("Skipping this TC as booking already exist")
            else:
                raise Exception(exp)
        is_key_there_in_dict('paymentDetails', _content)
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        test_data['sailorApp']['chosenActivity'].update(_content)
        test_data['excursion_already_booked'] = False
        # Verify Payment is in Pending State
        assert "PENDING" == _content['paymentStatus'], f"Payment status Error !!"

        amount = _content['paymentDetails']['amount'].split('.')[0]
        rest_shore.userToken = _content['paymentDetails']['clientToken']
        retries = 5
        for count in range(retries):
            try:
                content_transaction = payment_virgin(
                    config, test_data, guest_data, rest_shore, amount,
                    signature=_content['paymentDetails']['signature'],
                    signed_time_stamp=_content['paymentDetails']['signedTimeStamp'],
                    consumer_id=_content['paymentDetails']['consumerId'],
                    signed_fields=_content['paymentDetails']['signedFields'],
                    client_ref_num=_content['paymentDetails']['clientReferenceNumber']
                )
                break
            except Exception as exp:
                excpt = exp.args[0]
                continue
        else:
            raise Exception(excpt)
        rest_shore.userToken = test_data['signupGuest']['accessToken']

        # Make the Payment
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/pay")
        body = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "appointmentLinkId": test_data['sailorApp']['chosenActivity']['appointmentLinkId'],
            "paymentDetails": {
                "transactionId": content_transaction['transactionId'], "consumerId": content_transaction['consumerId'],
                "consumerType": "DXPUserId", "cardMaskedNo": "411111******1111", "cardType": "001",
                "cardExpiryMonth": "06", "cardExpiryYear": "33", "paymentToken": content_transaction['paymentToken'],
                "signedFields": content_transaction['signedFields'], "signature": content_transaction['signature'],
                "status": "ACCEPT", "statusCode": 100, "statusMessage": "Request successfully processed",
                "signedTimeStamp": content_transaction['signedTimeStamp'],
                "clientTransactionId": content_transaction['clientTransactionId'],
                "clientReferenceNumber": content_transaction['clientReferenceNumber'],
                "amount": content_transaction['amount'], "currencyCode": "USD",
                "firstName": test_data['signupGuest']['firstName'], "lastName": test_data['signupGuest']['lastName'],
                "billToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
                "billToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
                "billToCity": test_data['signupGuest']['addresses'][0]['city'],
                "billToState": test_data['signupGuest']['addresses'][0]['stateCode'],
                "billToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
                "billToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
                "shipToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
                "shipToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
                "shipToCity": test_data['signupGuest']['addresses'][0]['city'],
                "shipToState": test_data['signupGuest']['addresses'][0]['stateCode'],
                "shipToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
                "shipToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'], "paymentMode": "card"
            }
        }

        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['sailorApp']['chosenActivity'].update(_content)
        if "FULLY_PAID" != _content['status']:
            raise Exception("Payment status is not Fully Paid even after paying completely")

    @pytestrail.case(186248)
    def test_06_verify_guest_activities(self, config, test_data, rest_shore):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/guestactivities")
        body = {
            "activityCode": test_data['sailorApp']['chosenActivity']['activityCode'],
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "startTime": test_data['sailorApp']['chosenActivity']['activitySlots']['startDate'],
            "endTime": test_data['sailorApp']['chosenActivity']['activitySlots']['endDate'],
            "categoryCode": "RT",
            "isActivityPaid": False
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content
        for _guests in _content['guests']:
            if test_data['signupGuest']['guestId'] == _guests['guestId']:
                break
        else:
            raise Exception("The activities did not got booked for the correct User")

    @pytestrail.case(507102)
    def test_07_verify_activities(self, config, test_data, rest_shore):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        chosen = test_data['sailorApp']['chosenActivity']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['appointmentLinkId'] == chosen['appointmentLinkId'] and \
                    activity['appointmentId'] == chosen['appointmentId']:
                break
        else:
            raise Exception(f"Cannot find activityCode and appointmentId for booked excursion !!")

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(22855419)
    def test_08_check_activities_seaware(self, config, rest_shore, test_data, xml_data, creds):
        """
        Check the created shorex in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')

        xml = xml_data.login_seaware.format(creds.seaware.username, creds.seaware.password)
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('Login_OUT', _content_json)
        is_key_there_in_dict('MsgHeader', _content_json['Login_OUT'])
        is_key_there_in_dict('SessionGUID', _content_json['Login_OUT']['MsgHeader'])
        test_data['seawareSessionId'] = _content_json['Login_OUT']['MsgHeader']['SessionGUID']
        xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
        try:
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('LoadBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
            is_key_there_in_dict('ResPackages', _content_json['LoadBooking_OUT']['ResShell'])
            is_key_there_in_dict('ResPackage', _content_json['LoadBooking_OUT']['ResShell']['ResPackages'])
            assert len(_content_json['LoadBooking_OUT']['ResShell']['ResPackages'][
                           'ResPackage']) == 2, 'Shorex booked in sailor app is not showing in Seaware !!'
            for _res_package in _content_json['LoadBooking_OUT']['ResShell']['ResPackages']['ResPackage']:
                if _res_package['PackageClass'] == 'SHOREX':
                    assert _res_package['PackageType'] == test_data['sailorApp']['chosenActivity'][
                        'activityCode'], 'Activity code for Shorex is not matching !!'
                    assert _res_package['Status'] == 'CONFIRMED', 'Shorex booked is not confirmed !!'
                    assert _res_package['PackageCode'] == test_data['sailorApp']['chosenActivity']['activitySlots'][
                        'activitySlotCode'], 'Activity Slot code for Shorex is not matching !!'
                    break
            else:
                raise Exception('Booked Shorex from Sailor app is not showing in Seaware !!')
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(12758857)
    def test_09_change_booked_activity_slot(self, config, test_data, rest_shore, guest_data):
        """
        Change Booked Activity Slot
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        time.sleep(5)
        second_guest = guest_data[1]
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['sailorApp']['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'], "isGift": False,
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId'],
                "status": "CONFIRMED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": second_guest['guestId']
                }
            ],
            "activitySlotCode": test_data['sailorApp']['chosenActivity']['activitySlots']['activitySlotCode'],
            "accessories": [], "currencyCode": "USD",
            "appointmentLinkId": test_data['sailorApp']['chosenActivity']['appointmentLinkId'], "operationType": "EDIT"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['sailorApp']['chosenActivity'].update(_content)

    @pytestrail.case(474328)
    def test_10_verify_update_activities(self, config, test_data, rest_shore):
        """
        Verify activities has been updated
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        for slot in _content:
            if test_data['sailorApp']['chosenActivity']['appointmentLinkId'] == slot['appointmentLinkId'] and \
                    test_data['sailorApp']['chosenActivity']['appointmentId'] != slot['appointmentId']:
                break
        else:
            raise Exception(f"Booked activity is not updated with new Time Slot !!")
        test_data['sailorApp']['chosenActivity']['appointmentId'] = _content[0]['appointmentId']

    @pytestrail.case(26881151)
    def test_11_check_activities_edit_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the edited shorex in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        try:
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('LoadBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
            is_key_there_in_dict('ResPackages', _content_json['LoadBooking_OUT']['ResShell'])
            is_key_there_in_dict('ResPackage', _content_json['LoadBooking_OUT']['ResShell']['ResPackages'])
            rest_shore.session.headers.update({'Content-Type': 'application/json'})
            assert len(_content_json['LoadBooking_OUT']['ResShell']['ResPackages'][
                           'ResPackage']) == 3, 'Shorex Edited in sailor app is not showing in Seaware !!'
            for _res_package in _content_json['LoadBooking_OUT']['ResShell']['ResPackages']['ResPackage']:
                if _res_package['PackageClass'] == 'SHOREX':
                    assert _res_package['PackageType'] == test_data['sailorApp']['chosenActivity'][
                        'activityCode'], 'Activity code for Shorex is not matching !!'
                    assert _res_package['Status'] == 'CONFIRMED', 'Shorex booked is not confirmed !!'
                    assert _res_package['PackageCode'] == test_data['sailorApp']['chosenActivity']['activitySlots'][
                        'activitySlotCode'], 'Activity Slot code for Shorex is not matching !!'
                    break
            else:
                raise Exception('Booked Shorex from Sailor app is not showing in Seaware !!')
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(12758858)
    def test_12_delete_activities(self, config, test_data, rest_shore, guest_data):
        """
        Delete Activity
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        time.sleep(5)
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        second_guest = guest_data[1]
        body = {
            "appointmentLinkId": test_data['sailorApp']['chosenActivity']['appointmentLinkId'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId'],
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
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('paymentStatus', _content)
        test_data['sailorApp']['chosenActivity'].update(_content)

    @pytestrail.case(12768799)
    def test_13_verify_deleted_activities(self, config, test_data, rest_shore):
        """
        Verify Deleted Activities
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        elif test_data['excursion_already_booked']:
            pytest.skip("Skipping this TC as booking already exist")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            raise Exception("Booked activity did not got cancelled")

    @pytestrail.case(26881152)
    def test_14_check_activities_delete_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the deleted shorex in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        try:
            if not test_data['excursionAvailableShore']:
                pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
            elif test_data['excursion_already_booked']:
                pytest.skip("Skipping this TC as booking already exist")
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
            xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('LoadBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
            is_key_there_in_dict('ResPackages', _content_json['LoadBooking_OUT']['ResShell'])
            is_key_there_in_dict('ResPackage', _content_json['LoadBooking_OUT']['ResShell']['ResPackages'])
            rest_shore.session.headers.update({'Content-Type': 'application/json'})
            assert len(_content_json['LoadBooking_OUT']['ResShell'][
                           'ResPackages']) == 1, 'Shorex Deleted in sailor app is not deleted from Seaware !!'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(4825990)
    def test_15_list_eateries(self, config, test_data, rest_shore):
        """
        Verify list of eateries available
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['sailorApp']['eateries'] = dict()
        params = {
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId'],
            "shipCode": config.ship.code
        }

        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/spacetype/Eateries/landing")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

        test_data['eateriesAvailableShore'] = True
        if len(_content['spaces']['bookingRequired']) == 0:
            test_data['eateriesAvailableShore'] = False
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")

        test_data['sailorApp']['eateries'] = [x for x in _content['spaces']['bookingRequired'] if
                                              'avaliableSlots' in x and len(x['avaliableSlots']) > 0]

        if len(test_data['sailorApp']['eateries']) == 0:
            test_data['eateriesAvailableShore'] = False
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")

        test_data['sailorApp']['chosenEateries'] = random.choice(test_data['sailorApp']['eateries'])
        slots = [x for x in test_data['sailorApp']['chosenEateries']['avaliableSlots']]

        # Choose One Slots for Activities
        for activeSlot in slots:
            if activeSlot['isActive']:
                test_data['sailorApp']['chosenEateries']['eateriesSlots'] = activeSlot
        test_data['eateries_activitycode'] = test_data['sailorApp']['chosenEateries']['activityCode']
        test_data['eateries_activityslotcode'] = test_data['sailorApp']['chosenEateries']['eateriesSlots']['slotCode']

    @pytestrail.case(4825992)
    def test_16_book_eateries(self, config, test_data, rest_shore):
        """
        Book eateries
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
        time.sleep(5)
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['eateries_activitycode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId']
            }],
            "activitySlotCode": test_data['eateries_activityslotcode'],
            "accessories": [],
            "operationType": None,
            "currencyCode": "USD",
            "categoryCode": "RT",
            "shipCode": config.ship.code
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        test_data['eateries_appointmentLinkId'] = _content['appointmentLinkId']
        test_data['eateries_appointmentId'] = _content['appointmentId']
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not fully paid after booking eateries")

    @pytestrail.case(4825994)
    def test_17_verify_eateries(self, config, test_data, rest_shore):
        """
        Verify that eateries has been purchased
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")

        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for _eateries in _content:
            assert test_data['eateries_activitycode'] == _eateries['productCode'], "activityCode != productCode !!"
            assert test_data['eateries_appointmentId'] == _eateries['appointmentId'], "appointmentId mismatch !!"
            assert test_data['eateries_appointmentLinkId'] == _eateries[
                'appointmentLinkId'], "appointmentLinkId mismatch !!"

    @pytestrail.case(22855418)
    def test_18_check_eateries_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the created eateries in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('LoadBooking_OUT', _content_json)
        is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
        is_key_there_in_dict('ResDining', _content_json['LoadBooking_OUT']['ResShell'])
        is_key_there_in_dict('DiningRequest', _content_json['LoadBooking_OUT']['ResShell']['ResDining'])
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        assert len(_content_json['LoadBooking_OUT']['ResShell'][
                       'ResDining']) == 1, 'Eateries booked in sailor app is not showing in Seaware !!'
        assert _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'][
                   'GuestRefs'] == '1', 'Guest is not added in booked eateries !!'
        assert _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'][
                   'GuestRefs'] == '1', 'Guest is not added in booked eateries !!'

    @pytestrail.case(4825996)
    def test_19_update_eateries(self, config, test_data, rest_shore, guest_data):
        """
        Update eateries that has been purchased
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
        time.sleep(5)
        second_guest = guest_data[1]
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['eateries_activitycode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId'],
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
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['eateries_appointmentIdUpdated'] = _content['appointmentId']
        test_data['eateries_appointmentLinkId'] = _content['appointmentLinkId']

    @pytestrail.case(4825998)
    def test_20_verify_update_eateries(self, config, test_data, rest_shore):
        """
        Verify eateries has been updated
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")

        params = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for _eateries in _content:
            if test_data['eateries_appointmentIdUpdated'] == _eateries['appointmentId']:
                raise Exception('appointmentId is same even after updating eateries')

    @pytestrail.case(26882223)
    def test_21_check_eateries_edit_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the edited eateries in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('LoadBooking_OUT', _content_json)
        is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
        is_key_there_in_dict('ResDining', _content_json['LoadBooking_OUT']['ResShell'])
        is_key_there_in_dict('DiningRequest', _content_json['LoadBooking_OUT']['ResShell']['ResDining'])
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        assert len(_content_json['LoadBooking_OUT']['ResShell'][
                       'ResDining']) == 1, 'Eateries edited in sailor app is not showing in Seaware !!'
        assert _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'][
                   'GuestRefs'] == '1 2', '2 Guest is not added in edited eateries !!'
        assert _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'][
                   'PartySize'] == '2', '2 Guest is not added in edited eateries !!'

    @pytestrail.case(4826001)
    def test_22_delete_eateries(self, config, test_data, rest_shore, guest_data):
        """
        Delete eateries
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
        time.sleep(5)
        second_guest = guest_data[1]
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['eateries_appointmentLinkId'],
            "isRefund": True,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "categoryCode": "RT",
            "personDetails": [
                {
                    "personId": test_data['signupGuest']['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": test_data['signupGuest']['guestId'],
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
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

    @pytestrail.case(4826002)
    def test_23_verify_deleted_eateries(self, config, test_data, rest_shore):
        """
        Verify Deleted eateries
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['eateriesAvailableShore']:
            pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")

        params = {
            "reservationGuestId": test_data['signupGuest']['reservationGuestId']
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            raise Exception("Booked eateries did not got cancelled !!")


    @pytestrail.case(26882230)
    def test_24_check_eateries_delete_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the deleted eateries in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        try:
            if not test_data['eateriesAvailableShore']:
                pytest.skip(msg=f"Skipping, as No eateries is available to Book for {test_data['voyage']['startDate']}")
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
            xml = xml_data.load_booking_in_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            rest_shore.session.headers.update({'Content-Type': 'application/json'})
            is_key_there_in_dict('LoadBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
            if 'ResDining' in _content_json['LoadBooking_OUT']['ResShell']:
                raise Exception('Booked eateries did not got cancelled from Seaware !!')
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(11248896)
    def test_25_check_availability_of_lineup(self, config, test_data, rest_shore):
        """
        List all Lineup Activities
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['chosenActivity'] = dict()
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        body = {
            "voyageNumber": test_data['voyage']['id'],
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "categoryCode": "ET",
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content

        test_data['lineupAvailableShip'] = False
        if len(_content['activities']) == 0:
            test_data['lineupAvailableShip'] = False
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")

        is_key_there_in_dict('activities', _content)
        is_key_there_in_dict('filterCategories', _content)
        is_key_there_in_dict('preCruise', _content)
        is_key_there_in_dict('page', _content)

        # Filter out lineup which are available and have more than 1 activity slots
        for activity in _content['activities']:
            test_data['chosenActivity']['activityCode'] = activity['activityCode']
            test_data['chosenActivity']['currencyCode'] = activity['currencyCode']
            test_data['chosenActivity']['categoryCode'] = activity['categoryCode']
            # test_data['chosenActivity']['amount'] = activity['amount']
            if activity['isBookingEnabled']:
                for slots in activity['activitySlots']:
                    test_data['chosenActivity']['startDate'] = slots['startDate']
                    test_data['chosenActivity']['endDate'] = slots['endDate']
                    if not slots['isBookingClosed'] and slots['inventoryCount'] > 1 and slots['isEnabled']:
                        test_data['chosenActivity']['activitySlotCode'] = slots['activitySlotCode']
                        test_data['lineupAvailableShip'] = True
                        return
        if not test_data['sailorApp']['shipLineup']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")

    @pytestrail.case(11248893)
    def test_26_book_lineup(self, config, test_data, rest_shore):
        """
        Book Lineup
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId']
            }],
            "activitySlotCode": test_data['chosenActivity']['activitySlotCode'],
            "accessories": [],
            "operationType": None,
            "currencyCode": test_data['chosenActivity']['currencyCode'],
            "shipCode": config.ship.code,
            "categoryCode": test_data['chosenActivity']['categoryCode'],
            "startDate": test_data['chosenActivity']['startDate'],
            "endDate": test_data['chosenActivity']['endDate'],
            "isPayWithSavedCard": False
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('paymentStatus', _content)
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('appointmentId', _content)
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not Fully Paid even after paying completely")
        test_data['lineupBookingId'] = _content

    @pytestrail.case(11365154)
    def test_27_verify_lineup_under_guest_itineraries(self, config, test_data, rest_shore):
        """
        Verify that lineup under guestItineraries after book
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['appointmentLinkId'] == test_data['lineupBookingId']['appointmentLinkId'] and \
                    activity['appointmentId'] == test_data['lineupBookingId']['appointmentId'] and \
                    activity['categoryCode'] == test_data['chosenActivity']['categoryCode']:
                break
        else:
            raise Exception("Cannot find activityCode and appointmentId for booked lineup !!")

    @pytestrail.case(11248894)
    def test_28_edit_lineup(self, config, test_data, rest_shore, guest_data):
        """
        Add the new guest in Lineup
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        time.sleep(5)
        second_guest = guest_data[1]
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "isPayWithSavedCard": False,
            "activityCode": test_data['chosenActivity']['activityCode'],
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [
                {
                    "personId": test_data['signupGuest']['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": test_data['signupGuest']['guestId'],
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
            "currencyCode": test_data['chosenActivity']['currencyCode'],
            "appointmentLinkId": test_data['lineupBookingId']['appointmentLinkId'],
            "operationType": "EDIT",
            "categoryCode": test_data['chosenActivity']['categoryCode'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "startDate": test_data['chosenActivity']['startDate'],
            "endDate": test_data['chosenActivity']['endDate']
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['lineupBookingId'] = _content

    @pytestrail.case(11365155)
    def test_29_verify_edit_lineup_under_guest_itineraries(self, config, test_data, rest_shore):
        """
        Verify that lineup in guestItineraries after edit
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['appointmentLinkId'] == test_data['lineupBookingId']['appointmentLinkId'] and \
                    activity['categoryCode'] == test_data['chosenActivity']['categoryCode']:
                break
        else:
            raise Exception("Cannot find activityCode and appointmentId for booked lineup !!")

    @pytestrail.case(11248895)
    def test_30_cancel_lineup(self, config, test_data, rest_shore, guest_data):
        """
        cancel lineup
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        time.sleep(5)
        second_guest = guest_data[1]
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['lineupBookingId']['appointmentLinkId'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": test_data['signupGuest']['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "personDetails": [{
                "personId": test_data['signupGuest']['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": test_data['signupGuest']['guestId'],
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
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('appointmentLinkId', _content)
        is_key_there_in_dict('paymentStatus', _content)
        test_data['lineupCancelledBookingId'] = _content

    @pytestrail.case(11365156)
    def test_31_verify_cancel_lineup(self, config, test_data, rest_shore):
        """
        Verify cancelled lineup
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data['lineupAvailableShip']:
            pytest.skip(msg="Skipping, as No lineup is available to Book for active voyage")
        params = {"reservationGuestId": test_data['signupGuest']['reservationGuestId']}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) == 0:
            return
        elif len(_content) > 0:
            for activity in _content:
                if activity['appointmentLinkId'] == test_data['lineupCancelledBookingId']['appointmentLinkId'] and \
                        activity['categoryCode'] == test_data['chosenActivity']['categoryCode']:
                    raise Exception("Booked lineup did not got cancelled")
            else:
                return

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(30406677)
    def test_32_check_voyage_well_response_sync(self, config, test_data, rest_ship, guest_data):
        """
        To check voyage well response syncing from Sailor application to ACI.
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        # add retry
        test_data['sailorApp']['voyage_well'] = {}
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, f"/GuestStatus::{_res_id}")
            _content = rest_ship.send_request(method="GET", url=_url).content
            test_data['sailorApp']['voyage_well'][count] = _content

        assert test_data['sailorApp']['voyage_well'][0]["CruisewellContractSignedByEmail"] == \
               test_data['voyageWellDetails'][
                   'signedByEmail'], "Voyage well acknowledgement form details did not get sync from Sailor application shore side to ACI."
        assert test_data['sailorApp']['voyage_well'][0][
            "IsCruisewellContractSigned"], "Voyage well acknowledgement form status is not appearing as complete."

    @pytestrail.case(12150721)
    def test_33_toggle_reminders_in_notification(self, config, rest_shore, guest_data, test_data):
        """
        Turn off and on reminders toggle button in Notifications for precruise
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'),
                                            'guestpreferences/search/findbyreservationguestids')
        body = {
            "reservationGuestIds": [guest['reservationGuestId']]
        }
        _content = rest_shore.send_request(method='POST', url=url, json=body, auth="user").content
        is_key_there_in_dict('guestPreferences', _content['_embedded'])
        is_key_there_in_dict('guestPreferenceId', _content['_embedded']['guestPreferences'][0])
        test_data['guestPreferenceId_shore'] = _content['_embedded']['guestPreferences'][0]['guestPreferenceId']

        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'),
                                            f"guestpreferences/{test_data['guestPreferenceId_shore']}")
        states = ["IS_OPT_IN_REMINDER_NO", "IS_OPT_IN_REMINDER_YES"]
        for state in states:
            body = {
                "guestPreferenceId": test_data['guestPreferenceId_shore'],
                "reservationGuestId": guest['reservationGuestId'],
                "preferenceCode": 'IS_OPT_IN_REMINDER',
                "preferenceValueCode": state
            }
            _content = rest_shore.send_request(method='PUT', url=url, json=body, auth="user").content
            is_key_there_in_dict('guestPreferenceId', _content)
            is_key_there_in_dict('preferenceValueCode', _content)
            assert _content['preferenceValueCode'] == body[
                                                "preferenceValueCode"], "Reminder toggle button not turned off and on"

    @pytestrail.case(67651959)
    def test_34_beauty_and_body_landing(self, config, rest_shore, guest_data, test_data):
        """
        To verify landing on beauty & body for shore side
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/spacetype/Beauty---Body/landing")
        params = {
            "reservation-id": guest_data[0]['reservationId'],
            "reservation-guest-id": guest_data[0]['reservationGuestId'],
            "shipCode": config.ship.code,
            "path": "/Beauty---Body",
            "reservationNumber": test_data['reservationNumber'],
             }
        _content = rest_shore.send_request(method='GET', url=url, params=params, auth="user").content
        is_key_there_in_dict('spaces', _content)
        is_key_there_in_dict('header', _content)
        if len(_content['spaces']) > 0:
            for space in _content['spaces']:
                is_key_there_in_dict('name', space)
                is_key_there_in_dict('label', space)
                is_key_there_in_dict('externalId', space)
        else:
            raise Exception("No activity found on beauty and body page.")