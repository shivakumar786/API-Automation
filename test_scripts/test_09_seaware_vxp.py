__author__ = 'sarvesh.singh'

from virgin_utils import *


@pytest.mark.skip(reason='DCP-109856')
@pytest.mark.INTEGRATION
@pytest.mark.SEAWARE_VXP
@pytest.mark.run(order=10)
class TestSeawareVXP:
    """
    Test Suite to check Seaware and VXP Integration
    """

    @pytestrail.case(26903303)
    def test_01_sign_up(self, config, test_data, rest_shore, guest_data):
        """
        Register a User
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        # Save Guest we are signing up and use this one for all E2E
        test_data['seawareVxp'] = dict()
        test_data['seawareVxp']['signupGuest'] = dict()
        test_data['seawareVxp']['signupGuest']['addresses'] = guest_data[0]['Addresses']
        test_data['seawareVxp']['signupGuest']['email'] = generate_email_id(from_saved=True,
                                                                            first_name=guest_data[0]['FirstName'],
                                                                            last_name=guest_data[0]['LastName'])
        test_data['seawareVxp']['signupGuest']['password'] = 'Voyages@9876'
        test_data['seawareVxp']['signupGuest']['appId'] = str(generate_guid()).upper()
        test_data['seawareVxp']['signupGuest']['userType'] = 'guest'
        test_data['seawareVxp']['signupGuest']['enableEmailNewsOffer'] = False
        test_data['seawareVxp']['signupGuest']['deviceId'] = str(
            generate_random_alpha_numeric_string(length=32)).lower()
        url = urljoin(config.shore.url, "user-account-service/signup")
        body = {
            "birthDate": guest_data[0]['BirthDate'],
            "email": test_data['seawareVxp']['signupGuest']['email'],
            "firstName": guest_data[0]['FirstName'],
            "userType": test_data['seawareVxp']['signupGuest']['userType'],
            "preferredName": guest_data[0]['FirstName'],
            "lastName": guest_data[0]['LastName'],
            "password": test_data['seawareVxp']['signupGuest']['password'],
            "enableEmailNewsOffer": test_data['seawareVxp']['signupGuest']['enableEmailNewsOffer']
        }
        test_data['seawareVxp']['signupGuest'].update(body)
        # rest_shore.basicToken = "Basic NmM3ZjE1ZWUtMWRlYy00NzRmLWFhMmEtZjI1MjY4ODg2ZTdjOkJkNHh4NzVUSFUzdzg3Zmg="
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        # _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('authenticationDetails', _content)
        token = _content['authenticationDetails']
        is_key_there_in_dict('accessToken', token)
        is_key_there_in_dict('tokenType', token)
        test_data['seawareVxp']['signupGuest']['accessToken'] = f"{token['tokenType']} {token['accessToken']}"
        rest_shore.userToken = test_data['seawareVxp']['signupGuest']['accessToken']

    @pytestrail.case(26945986)
    def test_02_check_available_sailing(self, config, rest_shore, test_data):
        """
        Check the available sailing
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        if config.startDate is None:
            start_date = datetime.now(tz=pytz.utc).date()
        else:
            date_use = config.startDate
            start_date = datetime.strptime(date_use, "%Y-%m-%d")
        url = urljoin(config.shore.url, 'bookvoyage-bff/voyages')
        body = {
            "searchQualifier": {
                "sailingDateRange": [{"start": str(start_date), "end": str(start_date + timedelta(days=40))}],
                "cabins": [{"guestCounts": [{"ageCategory": "Adult", "count": test_data['guests']}]}],
                "currencyCode": "USD",
                "accessible": False
            }
        }
        # Get available voyages
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('sailings', _content)
        is_key_there_in_dict('packages', _content)
        test_data['seawareVxp']['voyages'] = sorted(_content['sailings'], key=lambda i: i['startDate'])
        voyages = sorted(_content['sailings'], key=lambda i: i['startDate'])
        if len(voyages) == 0:
            raise Exception("Zero Voyages Returned !!")
        for _voyage in voyages:
            if _voyage['startDate'] > str(start_date):
                test_data['seawareVxp']['voyage'] = _voyage
                break

    @pytestrail.case(26946522)
    def test_03_get_cabin_category(self, config, test_data, rest_shore):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'cabincategories/search')
        body = {
            "voyageId": test_data['seawareVxp']['voyage']['id'],
            "searchQualifier": {
                "sailingDateRange": [{
                    "start": test_data['seawareVxp']['voyage']['startDate'],
                    "end": test_data['seawareVxp']['voyage']['endDate']}],
                "cabins": [{"guestCounts": [{"ageCategory": "Adult", "count": test_data['guests']}]}]
            }
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        cabins = _content['cabins']
        if cabins is None or len(cabins) == 0:
            raise Exception(f"No Cabin(s) Returned !!")

        for cabin in cabins:
            for category in cabin['categoryOptions']:
                if category['maxOccupancy'] >= test_data['guests']:
                    is_key_there_in_dict('categoryCode', category)
                    is_key_there_in_dict('genericCategoryCode', category)
                    test_data['seawareVxp']['cabin'] = category
                    return
        else:
            raise Exception(f"Cannot Find Cabin with {test_data['guests']} Guests !!")

    @pytestrail.case(26946523)
    def test_04_cabin_search(self, config, test_data, rest_shore):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'cabins/search')
        body = {
            "voyageId": test_data['seawareVxp']['voyage']['id'],
            "cabins": [{
                "categoryCode": test_data['seawareVxp']['cabin']['categoryCode'],
                "guestCounts": [{"count": test_data['guests']}]
            }]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if 'cabinOptions' not in _content and len(_content['cabinOptions']) == 0:
            raise Exception(f"No Cabins Returned !!")

        # Choose a Random Cabin
        test_data['seawareVxp']['cabin'].update(random.choice(_content['cabinOptions']))

    @pytestrail.case(22855411)
    def test_05_book_reservation_seaware(self, config, rest_shore, test_data, guest_data, xml_data, creds):
        """
        Book reservation from seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :param xml_data:
        :param creds:
        :return:
        """
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.login_seaware.format(creds.seaware.username, creds.seaware.password)
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        test_data['seawareSessionId'] = _content_json['Login_OUT']['MsgHeader']['SessionGUID']

        guest = guest_data[0]
        date_of_birth = datetime.strptime((guest['BirthDate']), "%Y-%m-%d")
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        url = urljoin(config.shore.ota, 'OTA_CruiseBookRQ')

        xml = xml_data.book_rq_seaware.format(
            test_data['seawareVxp']['voyage']['id'],
            config.ship.code,
            test_data['seawareVxp']['cabin']['categoryCode'],
            test_data['seawareVxp']['cabin']['categoryCode'],
            test_data['seawareVxp']['cabin']['cabinNumber'], age,
            guest['CitizenshipCountryCode'],
            guest['BirthDate'], guest['GenderCode'], guest['BirthDate'],
            guest['FirstName'], guest['LastName'],
            test_data['seawareVxp']['signupGuest']['email'], age,
            guest['CitizenshipCountryCode'],
            guest['BirthDate'], guest['GenderCode'], guest['BirthDate'],
            guest['FirstName'], guest['LastName'],
            test_data['seawareVxp']['signupGuest']['email'])
        rest_shore.session.headers.update({'Content-Type': 'application/xml'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('vx:OTA_CruiseBookRS', _content_json)
        is_key_there_in_dict('vx:ReservationID', _content_json['vx:OTA_CruiseBookRS'])
        is_key_there_in_dict('@ID', _content_json['vx:OTA_CruiseBookRS']['vx:ReservationID'])
        test_data['seawareVxp']['seawareReservationNumber'] = _content_json['vx:OTA_CruiseBookRS']['vx:ReservationID'][
            '@ID']
        is_key_there_in_dict('vx:BookingPayment', _content_json['vx:OTA_CruiseBookRS'])
        is_key_there_in_dict('vx:PaymentSchedule', _content_json['vx:OTA_CruiseBookRS']['vx:BookingPayment'])
        _payment_schedule = _content_json['vx:OTA_CruiseBookRS']['vx:BookingPayment']['vx:PaymentSchedule']
        is_key_there_in_dict('vx:Payment', _payment_schedule)
        is_key_there_in_dict('@Amount', _payment_schedule['vx:Payment'])
        test_data['seawareVxp']['seawareReservationAmount'] = _payment_schedule['vx:Payment']['@Amount']

    @pytestrail.case(26952618)
    def test_06_check_guest_details_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the guest details in seaware after booking reservation
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        try:
            url = urljoin(config.shore.ota, 'OTA_ReadRQ')
            xml = xml_data.read_rq_seaware.format(test_data['seawareVxp']['seawareReservationNumber'])
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('vx:OTA_ResRetrieveRS', _content_json)
            is_key_there_in_dict('vx:ReservationsList', _content_json['vx:OTA_ResRetrieveRS'])
            is_key_there_in_dict('vx:CruiseReservation', _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList'])
            is_key_there_in_dict('vx:ReservationInfo',
                                 _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation'])
            _reservation_info = _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation'][
                'vx:ReservationInfo']
            is_key_there_in_dict('vx:GuestDetails', _reservation_info)
            assert len(_reservation_info['vx:GuestDetails']) == 1, 'Guest Count is not matching in seaware !!'
            is_key_there_in_dict('vx:GuestDetail', _reservation_info['vx:GuestDetails'])
            if len(_reservation_info['vx:GuestDetails']['vx:GuestDetail']) < 2:
                raise Exception('Reservation is not created for 2 guests !!')
            for _guest in _reservation_info['vx:GuestDetails']['vx:GuestDetail']:
                is_key_there_in_dict('vx:ContactInfo', _guest)
                is_key_there_in_dict('@LoyaltyMembershipID', _guest['vx:ContactInfo'])
                test_data['seawareVxp']['loyaltyMemberShipId'] = _guest['vx:ContactInfo']['@LoyaltyMembershipID']
                break
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(26951012)
    def test_07_check_reservation_booking_website(self, config, test_data, rest_shore):
        """
        Check if reservation got synced to booking website
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """

        url = urljoin(config.shore.url, 'bookvoyage-bff/userprofile')
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('userBookings', _content)
        if len(_content['userBookings']) == 0:
            raise Exception('Booked reservation from seaware is not showing on Booking Website !!')
        test_data['seawareVxp']['guestId'] = []
        for _booking in _content['userBookings']:
            is_key_there_in_dict('guestId', _booking)
            test_data['seawareVxp']['guestId'].append(_booking['guestId'])
            assert _booking['reservationNumber'] == test_data['seawareVxp'][
                'seawareReservationNumber'], 'Reservation Number mismatch !!'

    @pytestrail.case(22855413)
    def test_08_pay_reservation_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Pay for booked reservation from seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        try:
            tx_id = generate_guid()
            url = urljoin(config.shore.ota, 'OTA_CruisePaymentRQ')
            xml = xml_data.pay_rq_seaware.format(
                test_data['seawareVxp']['loyaltyMemberShipId'],
                test_data['seawareVxp']['seawareReservationNumber'],
                tx_id, tx_id, test_data['seawareVxp']['seawareReservationAmount']
            )
            rest_shore.session.headers.update({'Content-Type': 'application/xml'})
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(26961183)
    def test_09_check_reservation_pay_booking_website(self, config, test_data, rest_shore):
        """
        Check if reservation payment got synced to booking website
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """

        url = urljoin(config.shore.url, 'bookvoyage-bff/voyagedashboard')
        params = {
            'reservationNumber': test_data['seawareVxp']['seawareReservationNumber']
        }
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        if len(_content) == 0:
            raise Exception('Booked reservation from seaware is not shown in booking website !!')
        for _res in _content:
            is_key_there_in_dict('sailorDetails', _res)
            for _sailor in _res['sailorDetails']:
                if _sailor['id'] in test_data['seawareVxp']['guestId']:
                    continue
                else:
                    test_data['seawareVxp']['guestId'].append(_sailor['id'])
            is_key_there_in_dict('paymentDetails', _res)
            if len(_res['paymentDetails']) == 0:
                raise Exception('Booked reservation payment done from seaware is not showing on Booking Website !!')
            for _payment in _res['paymentDetails']:
                assert _payment['dueAmount'] == 0, 'Due Amount is not 0 even after full payment from seaware !!'

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(27109329)
    def test_10_guest_service_guests(self, config, rest_shore, test_data):
        """
        Get Reservation guest id from guest id
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """

        test_data['seawareVxp']['reservationGuestId'] = []
        for count, _guest in enumerate(test_data['seawareVxp']['guestId']):
            url = urljoin(config.shore.url, "dxpcore/reservationguests/search/findbyguestids")
            body = {"guestIds": [_guest]}
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="User").content
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('reservationGuests', _content['_embedded'])
            if len(_content['_embedded']['reservationGuests']) == 0:
                raise Exception('No guest found for booked reservation !!')
            for res_guest in _content['_embedded']['reservationGuests']:
                if _guest == res_guest['guestId']:
                    if res_guest['reservationGuestId'] == '' or res_guest['reservationGuestId'] is None:
                        logger.info("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                        raise Exception("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                    test_data['seawareVxp']['reservationGuestId'].append(res_guest['reservationGuestId'])
                    test_data['seawareVxp']['reservationId'] = res_guest['reservationId']
                    break
            else:
                raise Exception("reservationGuestId Not Found !!")

    @pytestrail.case(27105048)
    def test_11_list_activities(self, config, test_data, rest_shore):
        """
        List all Activities
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """

        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        body = {
            "voyageNumber": test_data['seawareVxp']['voyage']['id'],
            "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
            "reservationGuestId": test_data['seawareVxp']['reservationGuestId'][0],
            "categoryCode": "PA",
            "guestCount": guest_count
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content

        test_data['seawareVxp']['excursionAvailableShore'] = True
        if 'activities' not in _content:
            test_data['seawareVxp']['excursionAvailableShore'] = False
            pytest.skip(msg="Activities is not found in content")

        if len(_content['activities']) == 0:
            test_data['seawareVxp']['excursionAvailableShore'] = False
            pytest.skip(
                msg=f"Skipping, as No excursion is available to Book for {test_data['seawareVxp']['voyage']['startDate']}")

        is_key_there_in_dict('filterCategories', _content)
        is_key_there_in_dict('preCruise', _content)
        is_key_there_in_dict('page', _content)

        # Filter out activities which are available and have more than 1 activity slots
        test_data['seawareVxp']['activities'] = [x for x in _content['activities'] if
                                                 len(x['activitySlots']) > 0 and x['isAvailable']]
        if len(test_data['seawareVxp']['activities']) == 0:
            test_data['seawareVxp']['excursionAvailableShore'] = False
            pytest.skip(
                msg=f"Skipping, as No excursion is available to Book for {test_data['seawareVxp']['voyage']['startDate']}")

        test_data['seawareVxp']['chosenActivity'] = random.choice(test_data['seawareVxp']['activities'])
        slots = [x for x in test_data['seawareVxp']['chosenActivity']['activitySlots'] if
                 x['isEnabled'] and x['isInventoryAvailable'] and x['inventoryCount'] > 1]

        # Choose Two Slots for Activities
        first_slot = random.choice(slots)
        test_data['seawareVxp']['chosenActivity']['activitySlots'] = first_slot

    @pytestrail.case(27132335)
    def test_12_lock_reservation_seaware(self, config, rest_shore, test_data, xml_data):
        """
        lock reservation created from seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['seawareVxp']['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.lock_booking_in_seaware.format(test_data['seawareSessionId'],
                                                      test_data['seawareVxp']['seawareReservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('LoadBooking_OUT', _content_json)
        is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
        is_key_there_in_dict('ResHeader', _content_json['LoadBooking_OUT']['ResShell'])
        test_data['seawareVxp']['ResHeader'] = _content_json['LoadBooking_OUT']['ResShell']['ResHeader']
        is_key_there_in_dict('ResGuests', _content_json['LoadBooking_OUT']['ResShell'])
        test_data['seawareVxp']['ResGuests'] = _content_json['LoadBooking_OUT']['ResShell']['ResGuests']
        is_key_there_in_dict('ResPackages', _content_json['LoadBooking_OUT']['ResShell'])
        is_key_there_in_dict('ResPackage', _content_json['LoadBooking_OUT']['ResShell']['ResPackages'])
        test_data['seawareVxp']['ResPackage'] = _content_json['LoadBooking_OUT']['ResShell']['ResPackages'][
            'ResPackage']

    @pytestrail.case(27174622)
    def test_13_book_excursion_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Book excursion from seaware and check in sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['seawareVxp']['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        try:
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/UpdateBooking_IN')
            xml = xml_data.book_shorex_seaware.format(test_data['seawareSessionId'],
                                                      test_data['seawareVxp']['seawareReservationNumber'],
                                                      dict2xml(test_data['seawareVxp']['ResGuests']),
                                                      dict2xml(test_data['seawareVxp']['ResPackage']),
                                                      test_data['seawareVxp']['chosenActivity']['activitySlots'][
                                                          'activitySlotCode'],
                                                      test_data['seawareVxp']['chosenActivity']['activityCode'])
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('UpdateBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['UpdateBooking_OUT'])
            is_key_there_in_dict('ResPackages', _content_json['UpdateBooking_OUT']['ResShell'])
            is_key_there_in_dict('ResPackage', _content_json['UpdateBooking_OUT']['ResShell']['ResPackages'])
            _res_package = _content_json['UpdateBooking_OUT']['ResShell']['ResPackages']['ResPackage']
            if len(_res_package) < 2:
                raise Exception('Shore did not get Booked from Seaware !!')
            for _package in _res_package:
                if _package['PackageClass'] == 'SHOREX':
                    assert _package['PackageCode'] == test_data['seawareVxp']['chosenActivity']['activitySlots'][
                        'activitySlotCode'], 'activitySlotCode Mismatch !!'
                    assert _package['PackageType'] == test_data['seawareVxp']['chosenActivity'][
                        'activityCode'], 'activityCode Mismatch !!'
                    test_data['seawareVxp']['chosenActivity']['packageCode'] = _package['PackageCode']
                    test_data['seawareVxp']['chosenActivity']['PackageType'] = _package['PackageType']
                    assert _package['Status'] == 'CONFIRMED', 'Status is not CONFIRMED !!'
                    break
            else:
                raise Exception('Shore did not get Booked from Seaware !!')
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/StoreBooking_IN')
            xml = xml_data.store_book_shorex_seaware.format(test_data['seawareSessionId'],
                                                            test_data['seawareVxp']['seawareReservationNumber'])
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('StoreBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['StoreBooking_OUT'])
            is_key_there_in_dict('ResInvoice', _content_json['StoreBooking_OUT']['ResShell'])
            is_key_there_in_dict('ResInvoiceItem', _content_json['StoreBooking_OUT']['ResShell']['ResInvoice'])
            _invoice = _content_json['StoreBooking_OUT']['ResShell']['ResInvoice']['ResInvoiceItem']
            for invoice in _invoice:
                if invoice['Type'] == 'SHORE THINGS':
                    test_data['seawareVxp']['seawareArsAmount'] = invoice['Amount']
                    break
            else:
                raise Exception('There are no due payment for Shorex !!')
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(27195804)
    def test_14_pay_shorex_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Pay for booked shorex from seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['seawareVxp']['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")
        try:
            tx_id = generate_guid()
            url = urljoin(config.shore.ota, 'OTA_CruisePaymentRQ')
            xml = xml_data.pay_rq_seaware.format(test_data['seawareVxp']['loyaltyMemberShipId'],
                                                 test_data['seawareVxp']['seawareReservationNumber'],
                                                 tx_id, tx_id, test_data['seawareVxp']['seawareArsAmount'])
            rest_shore.session.headers.update({'Content-Type': 'application/xml'})
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(22855417)
    def test_15_verify_excursion_sailor(self, config, rest_shore, test_data):
        """
        verify booked excursion from seaware in sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        if not test_data['seawareVxp']['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        params = {"reservationGuestId": test_data['seawareVxp']['reservationGuestId'][0]}
        chosen = test_data['seawareVxp']['chosenActivity']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        for activity in _content:
            if activity['productSlotCode'] == chosen['packageCode'] and activity['productCode'] == chosen[
                'PackageType']:
                test_data['seawareVxp']['chosenActivity']['appointmentLinkId'] = activity['appointmentLinkId']
                test_data['seawareVxp']['chosenActivity']['appointmentId'] = activity['appointmentId']
                break
        else:
            raise Exception(f"Cannot find productSlotCode and productCode for booked excursion !!")

    @pytestrail.case(22855421)
    def test_16_edit_excursion_sailor_app(self, config, rest_shore, test_data):
        """
        edit excursion from sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        if not test_data['seawareVxp']['excursionAvailableShore']:
            pytest.skip(msg=f"Skipping, as No excursion is available to Book for {test_data['voyage']['startDate']}")

        chosen = test_data['seawareVxp']['chosenActivity']
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": chosen['activityCode'],
            "loggedInReservationGuestId": test_data['seawareVxp']['reservationGuestId'][0],
            "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'], "isGift": False,
            "personDetails": [{
                "personId": test_data['seawareVxp']['reservationGuestId'][0],
                "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
                "guestId": test_data['seawareVxp']['guestId'][0],
                "status": "CONFIRMED"
            },
                {
                    "personId": test_data['seawareVxp']['reservationGuestId'][1],
                    "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
                    "guestId": test_data['seawareVxp']['guestId'][1]
                }
            ],
            "activitySlotCode": chosen['packageCode'],
            "accessories": [], "currencyCode": "USD",
            "appointmentLinkId": chosen['appointmentLinkId'], "operationType": "EDIT",
            "shipCode": config.ship.code,
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

        params = {"reservationGuestId": test_data['seawareVxp']['reservationGuestId'][0]}
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        for slot in _content:
            if chosen['appointmentLinkId'] == slot['appointmentLinkId'] and chosen['appointmentId'] == slot[
                'appointmentId']:
                break
        else:
            raise Exception(f"Booked activity is not updated with new Time Slot !!")

    @pytestrail.case(22855425)
    def test_17_get_available_excursion_seaware(self, config, rest_shore, test_data, xml_data):
        """
        check all excursion from seaware are in sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        body = {
            "voyageNumber": test_data['seawareVxp']['voyage']['id'],
            "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
            "reservationGuestId": test_data['seawareVxp']['reservationGuestId'][0],
            "categoryCode": "PA",
            "guestCount": test_data['guests']
        }
        sailor_content = rest_shore.send_request(method="POST", url=_url, json=body, auth="user").content

        is_key_there_in_dict('activities', sailor_content)
        is_key_there_in_dict('filterCategories', sailor_content)
        is_key_there_in_dict('preCruise', sailor_content)
        is_key_there_in_dict('page', sailor_content)
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/GetAvailShorex_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        xml = xml_data.avail_shorex_in_seaware.format(test_data['seawareSessionId'],
                                                      test_data['voyage']['startDate'],
                                                      test_data['voyage']['endDate'],
                                                      test_data['voyage']['startDate'],
                                                      test_data['voyage']['endDate'],
                                                      )
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('AvailPackage', _content_json['GetAvailShorex_OUT']['AvailPackages'])
        assert len(_content_json['GetAvailShorex_OUT']['AvailPackages']['AvailPackage']) != len(
            sailor_content['activities']), 'Activities are not available in seaware and sailor app for booking'

    @pytestrail.case(22855424)
    def test_18_get_available_dining_seaware(self, config, rest_shore, test_data, xml_data):
        """
        check all dining from seaware are in sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/GetAvailDinings_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        xml = xml_data.avail_dining_in_seaware.format(test_data['seawareSessionId'],
                                                      config.ship.code,
                                                      test_data['seawareVxp']['voyage']['startDate'],
                                                      test_data['voyage']['endDate'],
                                                      test_data['seawareVxp']['seawareReservationNumber']
                                                      )
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        test_data['seawareVxp']['eateriesAvailableShore'] = _content_json
        params = {
            "reservation-id": test_data['seawareVxp']['reservationId'],
            "reservation-guest-id": test_data['seawareVxp']['reservationGuestId'][0],
            "shipCode": config.ship.code
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/discover/spacetype/Eateries/landing")
        sailor_content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        test_data['seawareVxp']['eateriesAvailableShore'] = _content_json
        is_key_there_in_dict('GetAvailDinings_OUT', _content_json)
        is_key_there_in_dict('AvailDinings', _content_json['GetAvailDinings_OUT'])
        is_key_there_in_dict('spaces', sailor_content)
        is_key_there_in_dict('bookingRequired', sailor_content['spaces'])
        assert len(sailor_content['spaces']['bookingRequired']) != 0 and len(_content_json['GetAvailDinings_OUT'][
                                                                                 'AvailDinings']) != 0, 'No eateries available for Booking in seaware and sailorapp'

    @pytestrail.case(22855416)
    def test_19_book_dining_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Book dining from seaware and check in sailor app
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        if not test_data['seawareVxp']['eateriesAvailableShore']:
            pytest.skip(
                msg=f"Skipping, as No dining is available to Book for {test_data['seawareVxp']['eateriesAvailableShore']}")
        try:
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/GetAvailDinings_IN')
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            xml = xml_data.avail_dining_in_seaware.format(test_data['seawareSessionId'],
                                                          config.ship.code,
                                                          test_data['seawareVxp']['voyage']['startDate'],
                                                          test_data['voyage']['endDate'],
                                                          test_data['seawareVxp']['seawareReservationNumber']
                                                          )
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            xml = xml_data.load_dining_booking_in_seaware.format(test_data['seawareSessionId'], "Y",
                                                                 test_data['seawareVxp']['seawareReservationNumber'])
            load_content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            load_content_json = xmltodict.parse(load_content)
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/UpdateBooking_IN')
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            load_cont = load_content_json['LoadBooking_OUT']['ResShell']
            xml = xml_data.update_dining_in_seaware.format(test_data['seawareSessionId'],
                                                           dict2xml(load_cont['ResHeader']),
                                                           dict2xml(load_cont['ResGuests']),
                                                           dict2xml(load_cont['ResPackages']),
                                                           _content_json['GetAvailDinings_OUT']['AvailDinings'][
                                                               'AvailDining'][0]['Restaurant'],
                                                           test_data['seawareVxp']['voyage']['startDate']
                                                           )
            update_dining = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            update_dining_json = xmltodict.parse(update_dining)
            test_data['seawareVxp']['resDining'] = update_dining_json['UpdateBooking_OUT']['ResShell']['ResDining'][
                'DiningRequest']
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/StoreBooking_IN')
            rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
            xml = xml_data.store_dining_booking_in_seaware.format(test_data['seawareSessionId'],
                                                                  test_data['seawareVxp']['seawareReservationNumber'])
            rest_shore.send_request(method="POST", url=url, data=xml, auth=None)
            url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
            xml = xml_data.load_dining_booking_in_seaware.format(test_data['seawareSessionId'], "N",
                                                                 test_data['seawareVxp']['seawareReservationNumber'])
            rest_shore.send_request(method="POST", url=url, data=xml, auth=None)
            params = {"reservationGuestId": test_data['seawareVxp']['reservationGuestId'][0]}
            _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
            sailor_content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
            test_data['seawareVxp']['eateries'] = sailor_content
            is_key_there_in_dict('appointmentId', sailor_content[0])
            is_key_there_in_dict('categoryCode', sailor_content[0])
            assert len(sailor_content) != 0, 'GuestItineraries do not have booked itineries'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(22855426)
    def test_20_check_eateries_edit_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the edited eateries in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "isPayWithSavedCard": False,
            "activityCode": test_data['seawareVxp']['eateries'][0]['productCode'],
            "loggedInReservationGuestId": test_data['seawareVxp']['reservationGuestId'][0],
            "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": test_data['seawareVxp']['reservationGuestId'][0],
                "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
                "guestId": test_data['seawareVxp']['guestId'][0],
                "status": "CONFIRMED"
            },
                {
                    "personId": test_data['seawareVxp']['reservationGuestId'][1],
                    "reservationNumber": test_data['seawareVxp']['seawareReservationNumber'],
                    "guestId": test_data['seawareVxp']['guestId'][1]
                }],
            "activitySlotCode": test_data['seawareVxp']['eateries'][0]['productSlotCode'],
            "accessories": [],
            "currencyCode": "USD",
            "appointmentLinkId": test_data['seawareVxp']['eateries'][0]['appointmentId'],
            "operationType": "EDIT",
            "categoryCode": "RT",
            "shipCode": config.ship.code,
            "voyageNumber": test_data['seawareVxp']['voyage']['id']
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        test_data['eateries_appointmentIdUpdated'] = _content['appointmentId']
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_dining_booking_in_seaware.format(test_data['seawareSessionId'], "N",
                                                             test_data['seawareVxp']['seawareReservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        try:
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('LoadBooking_OUT', _content_json)
            is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
            is_key_there_in_dict('ResDining', _content_json['LoadBooking_OUT']['ResShell'])
            is_key_there_in_dict('PartySize',
                                 _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'])
            assert len(_content_json['LoadBooking_OUT']['ResShell'][
                           'ResDining']) == '1', 'Eateries edited in sailor app is not showing in Seaware !!'
            assert _content_json['LoadBooking_OUT']['ResShell']['ResDining']['DiningRequest'][
                       'PartySize'] == '2', '2 Guest is not added in edited eateries !!'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(41753632)
    def test_21_check_cancel_eateries_notification_sailor_app(self, config, rest_shore, test_data, xml_data):
        """
        Check the edited eateries in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/GetAvailDinings_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        xml = xml_data.avail_dining_in_seaware.format(test_data['seawareSessionId'],
                                                      config.ship.code,
                                                      test_data['seawareVxp']['voyage']['startDate'],
                                                      test_data['voyage']['endDate'],
                                                      test_data['seawareVxp']['seawareReservationNumber']
                                                      )
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        xml = xml_data.load_dining_booking_in_seaware.format(test_data['seawareSessionId'], "Y",
                                                             test_data['seawareVxp']['seawareReservationNumber'])
        load_content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        load_content_json = xmltodict.parse(load_content)
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/UpdateBooking_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        load_cont = load_content_json['LoadBooking_OUT']['ResShell']
        xml = xml_data.cancel_dining_in_seaware.format(test_data['seawareSessionId'],
                                                       dict2xml(load_cont['ResHeader']),
                                                       dict2xml(load_cont['ResGuests']),
                                                       dict2xml(load_cont['ResPackages']),
                                                       _content_json['GetAvailDinings_OUT']['AvailDinings'][
                                                           'AvailDining'][0]['Restaurant'],
                                                       test_data['seawareVxp']['voyage']['startDate']
                                                       )
        restaurant = _content_json['GetAvailDinings_OUT']['AvailDinings']['AvailDining'][0]['Restaurant']
        update_dining = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        update_dining_json = xmltodict.parse(update_dining)
        test_data['seawareVxp']['resDining'] = update_dining_json['UpdateBooking_OUT']['ResShell']['ResDining'][
            'DiningRequest']
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/StoreBooking_IN')
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        xml = xml_data.store_dining_booking_in_seaware.format(test_data['seawareSessionId'],
                                                              test_data['seawareVxp']['seawareReservationNumber'])
        rest_shore.send_request(method="POST", url=url, data=xml, auth=None)
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_dining_booking_in_seaware.format(test_data['seawareSessionId'], "N",
                                                             test_data['seawareVxp']['seawareReservationNumber'])
        rest_shore.send_request(method="POST", url=url, data=xml, auth=None)
        _url = urljoin(config.shore.url, "messaging-service/getAllReadNotification?PageNo=0&EventType=Notifications,"
                                         "URLNotifications,StatusBanners&Size=10")
        messages = rest_shore.send_request(method="GET", url=_url, auth="user").content
        if messages['Length'] != 0:
            assert messages['readNotification'][0][
                       'Notification_Body'] == "We’re so sorry, we just had too many bookings on our plate.", "Dining order not cancelled"
