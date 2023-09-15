__author__ = 'HT'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.INTEGRATION
@pytest.mark.SAILOR_ARS_ADMIN
@pytest.mark.run(order=39)
class TestArsSailorArsAdmin:
    """
    Test Suite to check integration between sailor application and ARS Admin
    """

    @pytestrail.case(26112985)
    def test_01_login(self, config, test_data, guest_data, rest_ship, creds):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        test_data['booking_details'] = dict()
        guest = guest_data[0]
        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": guest['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

        _url = urljoin(config.ship.url, '/user-account-service/signin/username')
        body = {
            "userName": creds.verticalqa.username, "password": creds.verticalqa.password,
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body).content
        rest_ship.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

    @pytestrail.case(26151262)
    def test_02_list_activities(self, config, test_data, rest_ship, guest_data):
        """
        List all Activities
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        test_data['excursionAvailableShipIntegration'] = True
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/activities")
        guest_count = test_data['guests']
        current_date = str(datetime.utcfromtimestamp(test_data['aci']['shipEpochTime'] + 19800)).replace(' ', 'T')
        body = {
            "voyageNumber": test_data['voyageId'],
            "reservationNumber": test_data['reservationNumber'],
            "reservationGuestId": guest['reservationGuestId'],
            "categoryCode": "PA", "guestCount": guest_count
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        pages = _content['page']['totalPages']
        for counts, _pages in enumerate(range(pages), start=1):
            _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/activities")
            params = {"page": counts}
            _content = rest_ship.send_request(method="POST", url=_url, json=body, params=params, auth="user").content
            is_key_there_in_dict('filterCategories', _content)
            is_key_there_in_dict('activities', _content)
            is_key_there_in_dict('preCruise', _content)
            is_key_there_in_dict('page', _content)
            for count, _activity in enumerate(_content['activities']):
                if len(_content['activities'][count]['activitySlots']) > 0:
                    for _activitySlots in _activity['activitySlots']:
                        if not _activitySlots['isBookingClosed']:
                            if _activitySlots['startDate'] > current_date and _activitySlots['isEnabled']:
                                test_data['booking_details']['activityCodeShip'] = _activity['activityCode']
                                test_data['booking_details']['activitySlotCode'] = _activitySlots['activitySlotCode']
                                if len(_activitySlots['activitySellingPrices']) == 0:
                                    test_data['booking_details']['amount'] = 0
                                else:
                                    test_data['booking_details']['amount'] = _activitySlots['activitySellingPrices'][0][
                                        'amount']
                                test_data['booking_details']['startTime'] = _activitySlots['startDate']
                                test_data['booking_details']['endTime'] = _activitySlots['endDate']
                                return

    @pytestrail.case(10565611)
    def test_03_book_activities(self, config, test_data, guest_data, rest_ship):
        """
        Book activity from sailor application
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if 'activityCodeShip' not in test_data['booking_details']:
            test_data['excursionAvailableShipIntegration'] = False
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        guest = guest_data[0]
        guest_two = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['booking_details']['activityCodeShip'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId']
            },
                {
                    "personId": guest_two['reservationGuestId'],
                    "reservationNumber": test_data['reservationNumber'],
                    "guestId": guest_two['guestId']
                }],
            "activitySlotCode": test_data['booking_details']['activitySlotCode'],
            "accessories": [],
            "totalAmount": test_data['booking_details']['amount'],
            "operationType": None,
            "currencyCode": "USD"
        }
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        except Exception as exp:
            if "Missing or wrong parameter {charge_id}" in exp.args[0]:
                test_data["activity_book_sailor_app"] = False
                pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
            else:
                raise Exception(exp)
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not Fully Paid even after paying completely")
        test_data["activity_book_sailor_app"] = True
        test_data['booking_details']['appointmentId'] = _content['appointmentId']
        test_data['booking_details']['appointmentLinkId'] = _content['appointmentLinkId']

    @pytestrail.case(26156027)
    def test_04_find_active_voyage(self, config, test_data, rest_ship):
        """
        Get Active Voyage in ARS admin website
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        test_data['voyage_details'] = dict()
        _shipCode = config.ship.code
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            test_data['voyage_details']['active_voyage'] = voyage['number']
            test_data['voyage_details']['embark'] = voyage['embarkDate']
            test_data['voyage_details']['debark'] = voyage['debarkDate']
            break
        else:
            raise Exception('Voyage data does not exist')

    @pytestrail.case(26156030)
    def test_05_booking_search(self, config, test_data, rest_ship):
        """
        Search for an activity in ARS that is booked from sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        params = {
            "size": 1500
        }
        body = {"activityCodes": [test_data['booking_details']['activityCodeShip']],
                "activitySlotCode": [test_data['booking_details']['activitySlotCode']],
                "personDetails": [], "activityDetailRequired": True, "waiverStatus": None, "status": "CONFIRMED",
                "checkInStatus": None, "voyageNumber": test_data['voyageNumber'], "isBookingLocationRequired": True,
                "embarkDate": test_data['voyage_details']['embark']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('bookings', _content)
        if not any(
                d['bookingLinkId'] == test_data['booking_details']['appointmentLinkId'] for d in _content['bookings']):
            raise Exception(f'Booking not reflected in ARS web application')

    @pytestrail.case(26156029)
    def test_06_delete_activities(self, config, test_data, rest_ship, guest_data):
        """
        Delete the booked activity from sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        guest = guest_data[0]
        second_guest = guest_data[1]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "appointmentLinkId": test_data['booking_details']['appointmentLinkId'],
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

    @pytestrail.case(10565605)
    def test_07_search_cancelled_activity(self, config, test_data, rest_ship):
        """
        Verify the cancelled activity from sailor app is removed from ARS booked activity list
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        params = {
            "size": 1500
        }
        body = {"activityCodes": [test_data['booking_details']['activityCodeShip']],
                "activitySlotCode": [test_data['booking_details']['activitySlotCode']],
                "personDetails": [], "activityDetailRequired": True, "waiverStatus": None, "status": "CONFIRMED",
                "checkInStatus": None, "voyageNumber": test_data['voyageNumber'], "isBookingLocationRequired": True,
                "embarkDate": test_data['voyage_details']['embark']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('bookings', _content)
        if any(d['bookingLinkId'] == test_data['booking_details']['appointmentLinkId'] for d in _content['bookings']):
            raise Exception(f'not removed from ARS website')

    @pytestrail.case(26151266)
    def test_08_book_activities(self, config, test_data, guest_data, rest_ship):
        """
        re-book an activity from sailor application
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        test_data['new_booking_details'] = dict()
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/ars/v2/book")
        body = {
            "activityCode": test_data['booking_details']['activityCodeShip'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": test_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": test_data['reservationNumber'],
                "guestId": guest['guestId']
            }],
            "activitySlotCode": test_data['booking_details']['activitySlotCode'],
            "accessories": [],
            "totalAmount": test_data['booking_details']['amount'],
            "operationType": None,
            "currencyCode": "USD"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="user").content
        if "FULLY_PAID" != _content['paymentStatus']:
            raise Exception("Payment status is not Fully Paid even after paying completely")
        test_data['new_booking_details']['appointmentId'] = _content['appointmentId']
        test_data['new_booking_details']['appointmentLinkId'] = _content['appointmentLinkId']

    @pytestrail.case(10565603)
    def test_09_search_booked_activity(self, config, test_data, rest_ship):
        """
        Get Activity Search in ARS admin application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        params = {
            "size": 1500
        }
        body = {"activityCodes": [test_data['booking_details']['activityCodeShip']],
                "activitySlotCode": [test_data['booking_details']['activitySlotCode']],
                "personDetails": [], "activityDetailRequired": True, "waiverStatus": None, "status": "CONFIRMED",
                "checkInStatus": None, "voyageNumber": test_data['voyageNumber'], "isBookingLocationRequired": True,
                "embarkDate": test_data['voyage_details']['embark']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('bookings', _content)
        if not any(d['bookingLinkId'] == test_data['new_booking_details']['appointmentLinkId'] for d in
                   _content['bookings']):
            raise Exception(f'Booking not shown here')

    @pytestrail.case(26156961)
    def test_10_cancel_booking(self, config, test_data, rest_ship):
        """
        Cancel the booking from ARS admin application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/batchcancelbookings")
        body = {
            "cancellationReasonId": "68e822ae-f250-11e9-81b4-2a2ae2dbcce4", "cancellationReasonText": "cancelled",
            "cancelledByPersonId": test_data['personId'], "cancelledByPersonTypeCode": "C",
            "refundAmount": 0, "activityBookingIds": [test_data['new_booking_details']['appointmentId']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for booking in _content:
            if booking['status'] != 'CANCELLED':
                raise Exception('Booking has not been cancelled successfully')

    @pytestrail.case(10565609)
    def test_11_verify_cancelled_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify activity in sailor app that is deleted from ARS application
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        guest = guest_data[0]
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            if any(_booking['appointmentLinkId'] == test_data['new_booking_details']['appointmentLinkId'] for
                   _booking in _content):
                raise Exception(f'Booking does not cancelled from sailor application')

    @pytestrail.case(11365175)
    def test_12_cancelled_notification(self, config, test_data, rest_ship):
        """
        Verify the activity cancelled notification in sailor app
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), '/getAllReadNotification')
        params = {
            "PageNo": 0
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            pass
        else:
            raise Exception("Notification not received")

    @pytestrail.case(26156963)
    def test_13_get_activity_type(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "activitytypes/findall")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content['activityTypes']) != 0:
            for activityType in _content['activityTypes']:
                is_key_there_in_dict('activityTypeId', activityType)
            test_data['activityTypeId'] = _content['activityTypes'][0]['activityTypeId']
            test_data['activityCode'] = _content['activityTypes'][0]['code']
            test_data['activityDescription'] = _content['activityTypes'][0]['description']
            test_data['activityName'] = _content['activityTypes'][0]['name']
        else:
            raise Exception('activity type data does not exist')

    @pytestrail.case(26156964)
    def test_14_get_activity_group(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activitygroups")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for activityGroup in _content:
                is_key_there_in_dict('activityGroupId', activityGroup)
                is_key_there_in_dict('groupCode', activityGroup)
                is_key_there_in_dict('isDeleted', activityGroup)
                is_key_there_in_dict('subActivityGroups', activityGroup)
                if activityGroup['groupCode'] == 'PA':
                    test_data['activityGroupId'] = activityGroup['activityGroupId']
                    break
        else:
            raise Exception('Activity Group data does not exist')

    @pytestrail.case(10565614)
    def test_15_booking_conflict(self, config, test_data, rest_ship, guest_data):
        """
        Get Booking Conflict
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_sailor_app"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        guest = guest_data[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/conflicts")
        body = {
            "activityCode": test_data['booking_details']['activityCodeShip'],
            "activityGroupCode": "PA",
            "endDateTime": test_data['booking_details']['endTime'], "isActivityPaid": True,
            "personDetails": [{
                "personId": guest['reservationGuestId'], "personTypeCode": "G",
                "reservationNumber": test_data['reservationNumber']
            }],
            "startDateTime": test_data['booking_details']['startTime']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['activityConflictDetails'] is not None:
            pass
        else:
            raise Exception("User already has booking for this time")

    @pytestrail.case(26156965)
    def test_16_activity_booking(self, config, request, test_data, rest_ship, guest_data):
        """
        Book an activity from ARS admin website
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        guest = guest_data[0]
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings")
        body = {
            "activityCode": test_data['booking_details']['activityCodeShip'], "activityGroupCode": "PA",
            "activitySlotCode": test_data['booking_details']['activitySlotCode'], "additionalNotes": "",
            "bookedByPersonId": guest['guestId'], "bookedByPersonTypeCode": "C", "discountAmount": 0,
            "discountReasonId": "", "discountUnit": "AMOUNT", "isCheckedIn": "",
            "payeePersonId": guest['reservationGuestId'], "payeePersonTypeCode": "G", "personDetails": [{
                "personId": guest['reservationGuestId'], "personTypeCode": "G"
            }]
        }
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        except Exception as exp:
            if "Missing or wrong parameter {charge_id}" in exp.args[0]:
                test_data["activity_book_ars_admin"] = False
                pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
            else:
                raise Exception(exp)
        if _content['bookingLinkId'] is None:
            raise Exception("Booking is not successful")
        test_data['activity_booking_id'] = _content['bookings'][0]['activityBookingId']
        test_data["activity_book_ars_admin"] = True
        for booking in _content['bookings']:
            for _key in _ship_data:
                is_key_there_in_dict(_key, booking)
            for activityPersonBooking in booking['activityPersonBookings']:
                for _key in _ship_data['activityPersonBookings']:
                    is_key_there_in_dict(_key, activityPersonBooking)

    @pytestrail.case(10565607)
    def test_17_verify_booked_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify booked activity from sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        guest = guest_data[0]
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            pass
        else:
            raise Exception("Booking from ARS not reflected on Sailor application")

    @pytestrail.case(11365173)
    def test_18_booking_notification(self, config, test_data, rest_ship):
        """
        To raise a request to sailor service(support-queue) from sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), '/getAllReadNotification')
        params = {
            "PageNo": 0
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            pass
        else:
            raise Exception("Notification not received")

    @pytestrail.case(10565612)
    def test_19_modify_booking(self, config, request, test_data, rest_ship):
        """
        Get Cancel booking from ARS web application
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/cancelled_booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings",
                      f"/{test_data['activity_booking_id']}")

        body = {"notes": "", "addtionalNotes": "",
                "refundReasonId": "f2ed986e-1d8c-11ea-978f-2e728ce88125", "refundAmount": "100",
                "refundAmountUnit": "PERCENT", "activityPersonBookings": [{"isCheckedIn": True}]
                }
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        if _content['activityPersonBookings'][0]['isCheckedIn']:
            pass
        else:
            raise Exception('Booking has not been modified successfully')

    @pytestrail.case(26156962)
    def test_20_cancel_booking(self, config, request, test_data, rest_ship):
        """
        Get Cancel booking from ARS web application
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/cancelled_booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/batchcancelbookings")
        body = {
            "cancellationReasonId": "68e822ae-f250-11e9-81b4-2a2ae2dbcce4", "cancellationReasonText": "cancelled",
            "cancelledByPersonId": test_data['personId'], "cancelledByPersonTypeCode": "C",
            "refundAmount": 0, "activityBookingIds": [test_data['activity_booking_id']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for booking in _content:
            for _key in _ship_data:
                is_key_there_in_dict(_key, booking)
            for activityPersonBooking in booking['activityPersonBookings']:
                for _key in _ship_data['activityPersonBookings']:
                    is_key_there_in_dict(_key, activityPersonBooking)
            if booking['status'] != 'CANCELLED':
                raise Exception('Booking has not been cancelled successfully')

    @pytestrail.case(26156966)
    def test_21_verify_cancelled_activities(self, config, test_data, rest_ship, guest_data):
        """
        Verify cancelled Activities in sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        guest = guest_data[0]
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.guestbff'), "/myvoyages/guestItineraries")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) == 0:
            pass
        else:
            for count in range(0, len(_content)):
                appointment_id = _content[count]['appointmentLinkId']
                assert appointment_id != test_data['appointmentLinkIdUpdated'], "booked activity dit not get deleted"

    @pytestrail.case(11365174)
    def test_22_modified_notification(self, config, test_data, rest_ship):
        """
        To verify the modified notification in sailor application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['excursionAvailableShipIntegration']:
            pytest.skip(msg='Skipping, as No future excursion is available to Book for active voyage')
        elif not test_data["activity_book_ars_admin"]:
            pytest.skip("Skipping this TC as not able to book activity due to charge id issue")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), '/getAllReadNotification')
        params = {
            "PageNo": 0
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            pass
        else:
            raise Exception("Notification not received")
