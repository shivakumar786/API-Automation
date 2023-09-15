__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.BOOKING_MANAGEMENT
@pytest.mark.run(order=23)
class TestBookingManagement:
    """
    Test Suite to test Booking Management
    """

    @pytestrail.case(687189)
    def test_01_find_active_voyage(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['activities'] = dict()
        test_data['portCodes'] = []
        test_data['activities']['currentTime'] = change_epoch_of_datetime(test_data['crew_framework']['currentDate'])
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            test_data['active_voyage'] = voyage['number']
            test_data['embark'] = voyage['embarkDate']
            test_data['debark'] = voyage['debarkDate']
            for itenary in voyage['voyageItineraries']:
                if 'portCode' in itenary:
                    test_data['portCodes'].append(itenary['portCode'])
            break
        else:
            raise Exception('Voyage data does not exist')

    @pytestrail.case(700725)
    def test_02_get_activity_type(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
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

    @pytestrail.case(700726)
    def test_03_get_activity_group(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
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
                    test_data['activityGroupCode'] = activityGroup['groupCode']
                    break
        else:
            raise Exception('Activity Group data does not exist')

    @pytestrail.case(67372987)
    def test_04_add_new_slot_to_activity(self, config, test_data, rest_ship):
        """
        To verify new slot added to activity
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        slot_date = test_data['crew_framework']['currentDate']
        epoch_date = int(change_epoch_of_datetime(slot_date))
        test_data['start_time'] = int(epoch_date+int(60*60*1000))
        test_data['end_time'] = int(test_data['start_time']+int(60*60*1000))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?parts=sellingPrices&page=1")
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": f"{test_data['embarkDate']}T00:00:00",
                "activityName": None, "includeCancelledSlots": True, "includeActivityGroupName": True,
                "includeSellingPrices": True, "includeVendorDetail": False, "page": 1,
                "endDate": f"{test_data['debarkDate']}T23:59", "canFilterByPort": True,
                "fetchActivityNameFromCMS": True, "statuses": [],
                "activityGroupCode": test_data['activityGroupCode'],
                "disableDbSearch": False, "portCodes": test_data['portCodes']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content['activities']) != 0, "empty activity list"
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['portCode'] = activity['portCode']
            test_data['activityCode'] = activity['code']
            test_data['activitySlotCode'] = f"{test_data['activityCode']}-{test_data['start_time']}-" \
                                            f"{test_data['end_time']}"
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"activityId": test_data['activityGroupId'],
                 "code": test_data['activityCode'],
                 "activityGroupCode": test_data['activityGroupCode'],
                 "activitySlots":
                     [{"isDeleted": False, "activityId": test_data['activityGroupId'],
                       "activityCode": test_data['activityCode'],
                       "code": test_data['activitySlotCode'],
                       "status": "OPEN",
                       "activityLocation":
                         {"isDeleted": False, "setupDuration": 480, "activityDuration": 122, "deckCode": None,
                          "sectionCode": None, "directionCode": None, "venueId": test_data['portCode'],
                          "locationType": "PORT", "arsVenueId": None
                          },
                       "capacity":
                         {"isDeleted": False, "holdCapacity": 50, "maximumWaitlistCount": 0, "minimumSelling": 0,
                          "totalCapacity": 99999
                          },
                       "voyageNumber": test_data['voyageNumber'],
                       "sellingPrices":
                         [{"isDeleted": False, "personType": "C", "levelType": "ALL", "levelValue": "ALL",
                             "price": 0, "tax": 0
                           }],
                         "meetingLocations":
                         [{"isDeleted": False, "endTime": 61, "startTime": 3055, "deckCode": None, "sectionCode": None,
                             "directionCode": None, "locationType": "SHORE",
                             "arsVenueId": test_data['venueId']
                           }],
                         "cancellationCharges":
                         [{"isDeleted": False, "chargeUnit": "PERCENT", "chargeValue": 0, "maxDuration": 1440,
                             "isNoShow": False
                           }],
                         "isBookingStopped": False, "isCancelled": False,
                         "isWaitListEnable": False, "cancelBookings": False, "moveBookings": False,
                         "shipCode": config.ship.code, "checkedInCount": 0,
                         "startDateTime": test_data['start_time'],
                         "endDateTime": test_data['end_time'], "availableInventory": 0
                       }]
                 }]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content['failedActivityCodes']) == 0, "slot not added successfully"
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'],
                "activitySlotCode": test_data['activitySlotCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PRIVATE", "PUBLIC"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['holdCapacity'] = activity['capacity']['holdCapacity']
            test_data['totalCapacity'] = activity['capacity']['totalCapacity']
            test_data['activitySlotId'] = activity['activitySlots'][0]['activitySlotId']
            test_data['capacityId'] = activity['capacity']['capacityId']
            test_data['activityId'] = activity['activityId']
            assert activity['activitySlots'][0]['code'] == test_data['activitySlotCode'], "slot code not matched"

    @pytestrail.case(67646386)
    def test_05_child_to_parent_details_edit(self, config, test_data, rest_ship):
        """
        To verify child slot details should not reflect in the parent details
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        Total_Capacity = random.randint(500, 2000)
        Hold_Capacity = random.randint(10, 70)
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"activityGroupCode": test_data['activityGroupCode'], "activityId": test_data['activityId'],
                 "code": test_data['activityCode'],
                 "activitySlots":
                     [{"activitySlotId": test_data['activitySlotId'],
                       "code": test_data['activitySlotCode'],
                       "capacity":
                           {"capacityId": test_data['capacityId'], "totalCapacity": Total_Capacity,
                            "holdCapacity": Hold_Capacity, "minimumSelling": 0, "maximumWaitlistCount": 0}}]}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PRIVATE", "PUBLIC"], "voyageNumber": test_data['voyageNumber'],
                "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            if not Total_Capacity != activity['capacity']['totalCapacity'] and \
                    Hold_Capacity != activity['capacity']['holdCapacity']:
                raise Exception('changes in child details reflected in parent details')

    @pytestrail.case(67646106)
    def test_06_parent_to_child_slot_details_edit(self, config, test_data, rest_ship):
        """
        To verify parent details should not reflect in the child details for existing slots
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        Total_Capacity = random.randint(500, 2000)
        Hold_Capacity = random.randint(10, 70)
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/{test_data['activityCode']}")
        body = {"activityGroupCode": test_data['activityGroupCode'], "activityId": test_data['activityId'],
                "code": test_data['activityCode'], "inheritParentToChild": False,
                "sendSlotTimeUpdateNotification": True, "isMoveSlotEnabled": True, "activitySlots": [],
                "capacity":
                    {"capacityId": test_data['capacityId'], "totalCapacity": Total_Capacity,
                     "holdCapacity": Hold_Capacity, "minimumSelling": 0, "maximumWaitlistCount": 0}}
        rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "activitySlotCode": test_data['activitySlotCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PRIVATE", "PUBLIC"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            if not Total_Capacity != activity['capacity']['holdCapacity'] and \
                   Hold_Capacity != activity['capacity']['totalCapacity']:
                raise Exception('changes in parent details reflected in existing child details')

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(671708)
    def test_07_activity_slots_search(self, config, test_data, rest_ship):
        """
        Get Activity Slot Search
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'),
                      "/activities/slots/search?sort=activityCode&sort=status,desc")
        params = {
            "size": 99999
        }
        body = {
            "includeArrivalCount": True,
            "startDate": f"{test_data['embarkDate']}T06:00:00",
            "endDate": f"{test_data['debarkDate']}T23:59",
            "activityGroupCodes": [
                "PA"
            ]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content['data']) == 0:
            raise Exception('activity created slot not available')
        for count in range(0, len(_content['data'])):
            if _content['data'][count]['activityCode'] == test_data['activityCode']:
                test_data['endDateTime'] = _content['data'][count]['endDateTime']
                test_data['startDateTime'] = _content['data'][count]['startDateTime']
                is_key_there_in_dict('access', _content['data'][count])
                is_key_there_in_dict('activityCode', _content['data'][count])
                is_key_there_in_dict('activityName', _content['data'][count])
                is_key_there_in_dict('activitySlotCode', _content['data'][count])
                is_key_there_in_dict('capacity', _content['data'][count])
                is_key_there_in_dict('checkedIn', _content['data'][count])
                is_key_there_in_dict('endDateTime', _content['data'][count])
                is_key_there_in_dict('groupCode', _content['data'][count])
                is_key_there_in_dict('startDateTime', _content['data'][count])
                is_key_there_in_dict('status', _content['data'][count])
                break
        else:
            raise Exception("created slot available in inventory list")

    @pytestrail.case(681484)
    def test_08_booking_conflict(self, config, test_data, rest_ship, guest_data):
        """
        Get Booking Conflict
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/conflicts")
        body = {
            "activityCode": test_data['activityCode'],
            "activityGroupCode": test_data['activityGroupCode'],
            "endDateTime": test_data['endDateTime'], "isActivityPaid": True,
            "personDetails": [{
                "personId": guest['reservationGuestId'], "personTypeCode": "G",
                "reservationNumber": test_data['reservationNumber']
            }],
            "startDateTime": test_data['startDateTime']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(671709)
    def test_09_activity_booking(self, config, request, test_data, rest_ship, guest_data):
        """
        Get Activity Booking
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings")
        body = {
            "activityCode": test_data['activityCode'], "activityGroupCode": test_data['activityGroupCode'],
            "activitySlotCode": test_data['activitySlotCode'], "additionalNotes": "",
            "bookedByPersonId": guest['guestId'], "bookedByPersonTypeCode": "C", "discountAmount": 0,
            "discountReasonId": "", "discountUnit": "AMOUNT", "isCheckedIn": True,
            "payeePersonId": guest['reservationGuestId'], "payeePersonTypeCode": "G", "personDetails": [{
                "personId": guest['reservationGuestId'], "personTypeCode": "G"
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['bookingLinkId'] is None:
            raise Exception("Booking is not successful")
        test_data['activity_booking_id'] = _content['bookings'][0]['activityBookingId']
        for booking in _content['bookings']:
            for _key in _ship_data:
                is_key_there_in_dict(_key, booking)
            for activityPersonBooking in booking['activityPersonBookings']:
                for _key in _ship_data['activityPersonBookings']:
                    is_key_there_in_dict(_key, activityPersonBooking)

    @pytestrail.case(26999705)
    def test_10_edit_booking(self, config, test_data, rest_ship):
        """
        Edit the booking done for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, "url.path.ars"), "/bookings",
                       f"/{test_data['activity_booking_id']}")
        body = {
            "notes": "test_automation", "addtionalNotes": "", "refundReasonId": "f2ed986e-1d8c-11ea-978f-2e728ce88125",
            "refundAmount": "10", "refundAmountUnit": "PERCENT", "activityPersonBookings": [{"isCheckedIn": True}]
        }
        _content = rest_ship.send_request(method="PATCH", json=body, url=_url, auth="crew")
        if len(_content) != 0:
            pass
        else:
            raise Exception("Failed to edit the booking")

    @pytestrail.case(671710)
    def test_11_activity_search(self, config, test_data, rest_ship):
        """
        Get Activity Search
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'),
                      "/activities/search")
        params = {
            "size": 9999, "parts": "activityAccounts,sellingPrices,activitySlots.capacity,costPrices"
        }
        body = {
            "startDate": f"{test_data['embarkDate']}T06:00:00",
            "endDate": f"{test_data['debarkDate']}T23:59",
            "requiredNoSlot": False,
            "includeSellingPrices": True,
            "includeCancelledSlots": True,
            "includeActivityGroupName": True,
            "voyageNumber": test_data['active_voyage'],
            "includeVendorDetail": False,
            "page": 1,
            "sortField": "",
            "type": "",
            "statuses": [],
            "access": [],
            "port": "",
            "activityName": "",
            "activityGroupCodes": [
                "PA"
            ],
            "fetchActivityNameFromCMS": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        for count in range(0, len(_content['activities'])):
            if _content['activities'][count]['code'] == test_data['activityCode']:
                break
        else:
            raise Exception("created activity does not exists in inventory list")

    @pytestrail.case(667948)
    def test_12_booking_search(self, config, request, test_data, rest_ship):
        """
        Get Booking Search
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        body = {"activityCodes": [test_data['activityCode']], "activitySlotCode": [test_data['activitySlotCode']]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            reservation_guest_ids = []
            for booking in _content['bookings']:
                for _key in _ship_data:
                    is_key_there_in_dict(_key, booking)
                for activityPersonBooking in booking['activityPersonBookings']:
                    for _key in _ship_data['activityPersonBookings']:
                        is_key_there_in_dict(_key, activityPersonBooking)
                    reservation_guest_ids.append(activityPersonBooking['personId'])
            test_data['reservation_guest_ids'] = reservation_guest_ids
        else:
            raise Exception('booking does not exist')

    @pytestrail.case(687190)
    def test_13_reservation_guest_search(self, config, request, test_data, rest_ship):
        """
        Get Reservation Guest Search
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath,
                             'test_data/verification_data/reservationGuestDetail_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/reservationguests/search")
        body = {"reservationGuestIds": test_data['reservation_guest_ids']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for reservationGuestDetail in _content['_embedded']['reservationGuestDetailsResponses']:
                for _key in _ship_data:
                    is_key_there_in_dict(_key, reservationGuestDetail)
                for _key in _ship_data['personalDetails']:
                    is_key_there_in_dict(_key, reservationGuestDetail['personalDetails'])
                for reservationDetail in reservationGuestDetail['reservationDetails']:
                    for _key in _ship_data['reservationDetails']:
                        is_key_there_in_dict(_key, reservationDetail)
        else:
            raise Exception('reservation guest data not available')

    @pytestrail.case(681479)
    def test_14_cancel_booking(self, config, request, test_data, rest_shore):
        """
        Get Cancel booking
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :return:
        """
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
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="crew").content
        for booking in _content:
            for _key in _ship_data:
                is_key_there_in_dict(_key, booking)
            for activityPersonBooking in booking['activityPersonBookings']:
                for _key in _ship_data['activityPersonBookings']:
                    is_key_there_in_dict(_key, activityPersonBooking)
            if booking['status'] != 'CANCELLED':
                raise Exception('Booking has not been cancelled successfully')

    @pytestrail.case(1126673)
    def test_15_mark_arrived(self, config, test_data, rest_ship, guest_data):
        """
        Mark Arrived
        :param test_data:
        :param rest_ship:
        :param config:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings")
        body = {
            "activityCode": test_data['activityCode'],
            "activityGroupCode": test_data['activityGroupCode'],
            "activitySlotCode": test_data['activitySlotCode'], "additionalNotes": "",
            "bookedByPersonId": test_data['personId'], "bookedByPersonTypeCode": "C", "discountAmount": 0,
            "discountReasonId": "", "discountUnit": "AMOUNT", "isCheckedIn": True,
            "payeePersonId": guest['reservationGuestId'], "payeePersonTypeCode": "G",
            "personDetails": [{
                "personId": guest['reservationGuestId'], "personTypeCode": "G"
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['bookingLinkId'] is None:
            raise Exception("Booking is not successful")
        test_data['activity_booking_id'] = _content['bookings'][0]['activityBookingId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/batchupdate")
        body = {"activityBookingIds": [test_data['activity_booking_id']], "isCheckedIn": True}
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        params = {
            'size': '300'
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        body = {"activityCodes": [test_data['activityCode']], "activitySlotCode": [test_data['activitySlotCode']]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _person_id = False
            _booking_id = False
            for booking in _content['bookings']:
                if booking['activityBookingId'] == test_data['activity_booking_id']:
                    _booking_id = True
                    for activityPersonBooking in booking['activityPersonBookings']:
                        if activityPersonBooking['personId'] == guest['reservationGuestId']:
                            _person_id = True
                            if not activityPersonBooking['isCheckedIn']:
                                raise Exception('Guest has not been marked arrived successfully!')
                    if not _person_id:
                        raise Exception('Guest data does not exist in created booking response!')
            if not _booking_id:
                raise Exception('created booking does not exist in total bookings response!')
        else:
            raise Exception('Getting no booking data in response!')

    @pytestrail.case(1126674)
    def test_16_include_arrival_count(self, config, test_data, rest_ship):
        """
        Include Arrival Count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'),
                      "/activities/slots/search?sort=activityCode&sort=status,desc&size=300&")
        body = {"voyageNumber": test_data['voyageNumber'], "includeArrivalCount": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for activity in _content['data']:
                if activity['activityCode'] == test_data['activityCode']:
                    if activity['checkedIn'] == 0:
                        raise Exception('checked in count is not correct!')
        else:
            raise Exception('activity slot not available')
        body = {"voyageNumber": test_data['voyageNumber'], "includeArrivalCount": False}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for activity in _content['data']:
                if activity['activityCode'] == test_data['activityCode']:
                    if activity['checkedIn'] != 0:
                        raise Exception('checked in count is not correct!')
        else:
            raise Exception('activity slot not available')

    @pytestrail.case(1267274)
    def test_17_update_waiver_status(self, config, request, test_data, rest_ship):
        """
        Update Waiver Status
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/booking_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/", test_data['activity_booking_id'])
        body = {"waiverStatus": "SIGNED", "waiverVersion": "V1", "waiverCode": "WR"}
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)
        for activityPersonBooking in _content['activityPersonBookings']:
            for _key in _ship_data['activityPersonBookings']:
                is_key_there_in_dict(_key, activityPersonBooking)
        if _content['waiverStatus'] != 'SIGNED' or _content['waiverVersion'] != 'V1' or _content['waiverCode'] != 'WR':
            raise Exception('Waiver not updated successfully!')

    @pytestrail.case(1267273)
    def test_18_search_activity_group(self, config, test_data, rest_ship):
        """
        Get Active Voyage
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activitygroups/search")
        body = {"groupCode": test_data['activityGroupCode'], "includeChilds": False, "includeNestedChilds": False}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('activityGroupId', _content)
            is_key_there_in_dict('description', _content)
            is_key_there_in_dict('groupCode', _content)
            is_key_there_in_dict('name', _content)
            if _content['activityGroupId'] != test_data['activityGroupId']:
                raise Exception('Activity Group id is not matching!')
        else:
            raise Exception('Activity Group data does not exist')

    @pytestrail.case(1126675)
    def test_19_cancel_activity_slot(self, config, test_data, rest_ship, rest_shore):
        """
        Cancel Activity Slot
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities", test_data['activityCode'])
        body = {
            "cancellationReasonId": "f2ed986e-1d8c-11ea-978f-2e728ce88125",
            "cancellationReasonText": "",
            "cancelledByPersonId": test_data['personId'],
            "cancelledByPersonTypeCode": "C",
            "refundAmount": 100,
            "refundAmountUnit": "PERCENT",
            "activitySlots": [{
                "code": test_data['activitySlotCode'],
                "cancelBookings": True, "isCancelled": True

            }]
        }
        rest_shore.send_request(method="PATCH", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'),
                      "/activities/slots/search?page=1&parts=activityAccounts,activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "activitySlotCode": test_data['activitySlotCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'],
                "includeVendorDetail": True, "fetchActivityNameFromCMS": True, "disableDbSearch": False,
                "access": ["PRIVATE", "PUBLIC"], "slotAccessTypes": ["PRIVATE", "PUBLIC"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for slots in _content['data']:
            test_data['activitySlotId'] = slots['cancellationCharges'][0]['activitySlotId']
            assert slots['isCancelled'] == True, "slots not cancelled successfully"

    @pytestrail.case(1126676)
    def test_20_booking_status_after_slot_cancellation(self, config, test_data, rest_ship):
        """
        Verify Booking Status After Slot Cancellation
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/search")
        body = {"activityCodes": [test_data['activityCode']], "activitySlotCode": [test_data['activitySlotCode']]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for booking in _content['bookings']:
                if booking['status'] != 'CANCELLED':
                    raise Exception('Booking has not been cancelled after activity slot cancellation!')
        else:
            raise Exception('booking does not exist')

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(32275802)
    def test_21_update_slot_sailor_selling_price(self, config, test_data, rest_ship):
        """
        update sailor selling price for any activity slot and verify the same reflected in booking management
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/filter")
        body = {
                "voyageNumber": test_data['voyageNumber'],
                "startDateTime": f"{test_data['embarkDate']}T00:00:00",
                "endDateTime": f"{test_data['debarkDate']}T23:59",
                "excludeActivityGroups": ["HET", "SET"]
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('Activities', _content)
        is_key_there_in_dict('PortData', _content)
        portCodes = []
        for port in _content['PortData']:
            if port['code'] not in portCodes:
                portCodes.append(port['code'])
        current_time = int(test_data['activities']['currentTime'])
        test_data['activities']['slotTime'] = int(change_epoch_of_datetime(test_data['crew_framework']['currentDate']))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {'size': 99999, "parts": "activityAccounts,sellingPrices,activitySlots.capacity,costPrices"}
        body = {"activityGroupCodes": ["PA"], "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "includeCancelledSlots": True, "includeActivityGroupName": True, "includeSellingPrices": True,
                "activityName": "", "includeVendorDetail": False, "fetchActivityNameFromCMS": True,
                "port": "", "statuses": [], "access": [], "portCodes": portCodes
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        assert len(_content) != 0, "empty activity list"
        is_key_there_in_dict('activities', _content)
        for activities in _content['activities']:
            if activities['code'] != "MIABKE00001VS" and activities['name'] != 'Script Automation':
                test_data['activities']['activityGroupId'] = activities['activityGroupId']
                test_data['activities']['cmsId'] = activities['cmsId']
                test_data['activities']['modifiedByUser'] = activities['modifiedByUser']
                test_data['activities']['createdByUser'] = activities['createdByUser']
                test_data['activities']['portCode'] = activities['portCode']
                is_key_there_in_dict('activitySlots', activities)
                is_key_there_in_dict('activityTypes', activities)
                for slots in activities['activitySlots']:
                    if slots['startDateTime'] > current_time:
                        test_data['activities']['activityCode'] = slots['activityCode']
                        test_data['activities']['activityId'] = slots['activityId']
                        test_data['activities']['activitySlotId'] = slots['activitySlotId']
                        test_data['activities']['code'] = slots['code']
                        test_data['activities']['creationTime'] = slots['creationTime']
                        test_data['activities']['modificationTime'] = slots['modificationTime']
                        test_data['activities']['startDateTime'] = slots['startDateTime']
                        test_data['activities']['endDateTime'] = slots['endDateTime']
                        test_data['activities']['modificationTimeTS'] = slots['modificationTimeTS']
                        test_data['activities']['creationTimeTS'] = slots['creationTimeTS']
                        for activitytype in activities['activityTypes']:
                            test_data['activities']['activityTypeId'] = activitytype['activityTypeId']
                        break
                else:
                    continue
                break
        else:
            pytest.skip(msg="no slots available to update")

        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {'size': 99999, "parts": "activityAccounts,sellingPrices,activitySlots.capacity,costPrices"}
        body = {"activityCode": test_data['activities']['cmsId'], "activitySlotCode": test_data['activities']['code'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True,
                "page": 1, "endDate": f"{test_data['debarkDate']}T23:59", "includeVendorDetail": True,
                "activityEndDateGE": f"{test_data['embarkDate']}T00:00:00"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        assert len(_content) != 0, "empty activity list"
        is_key_there_in_dict('activities', _content)
        for count in range(0, len(_content['activities'][0]['sellingPrices'])):
            if 'ALL' == _content['activities'][0]['sellingPrices'][count]['levelType']:
                _content['activities'][0]['sellingPrices'][count]['price'] = 150
                _content['activities'][0]['capacity']['holdCapacity'] = 50
                url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
                body = _content['activities']
                rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
                break
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        body = {
            "activityCodes": [
                test_data['activities']['cmsId']
            ],
            "includeDetails": True,
            "activitySlotCode": test_data['activities']['code'],
            "includeCancelledSlots": True,
            "includeVendorDetail": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty activity list"
        is_key_there_in_dict('activities', _content)
        for count in range(0, len(_content['activities'][0]['sellingPrices'])):
            if 'ALL' == _content['activities'][0]['sellingPrices'][count]['levelType']:
                assert _content['activities'][0]['sellingPrices'][count][
                           'price'] == 150.0, "selling price not updated in booking " \
                                              "management "
                assert _content['activities'][0]['capacity'][
                           'holdCapacity'] == 50.0, "hold capacity not updated in booking " \
                                                    "management "
                break

    @pytestrail.case(32276623)
    def test_22_filter_ent_activity_list(self, config, test_data, rest_ship):
        """
        filter and verify inventoried and non inventoried activity list
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['activities']['slotTime'] = change_epoch_of_datetime(test_data['crew_framework']['currentDate'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {'size': 99999, "parts": "activityAccounts,sellingPrices,activitySlots.capacity,costPrices"}
        body = {"activityGroupCodes": ["IET"], "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "includeCancelledSlots": True, "includeActivityGroupName": True, "includeSellingPrices": True,
                "activityName": "", "includeVendorDetail": False, "fetchActivityNameFromCMS": True,
                "port": "", "statuses": [], "access": [],
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        assert len(_content) != 0, "empty inventoried activity list"

        test_data['activities']['slotTime'] = change_epoch_of_datetime(test_data['crew_framework']['currentDate'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {'size': 99999, "parts": "activityAccounts,sellingPrices,activitySlots.capacity,costPrices"}
        body = {"activityGroupCodes": ["NET"], "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "includeCancelledSlots": True, "includeActivityGroupName": True, "includeSellingPrices": True,
                "activityName": "", "includeVendorDetail": False, "fetchActivityNameFromCMS": True,
                "port": "", "statuses": [], "access": [],
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        assert len(_content) != 0, "empty non inventoried activity list"


    @pytestrail.case(33575287)
    def test_23_dining_slots_on_debark_day(self, config, test_data, rest_ship):
        """
        filter and verify dining activity list on debarkation day
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        debark_date = change_epoch_time(test_data['debarkDate'])
        current_date = change_epoch_time(test_data['crew_framework']['currentDate'][:10])
        if debark_date == current_date:
            url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/slots/search?sort=startDateTime"
                                                                         "&sort=activityCode&sort=status&page=&")
            body = {"includeArrivalCount": True, "startDate": f"{test_data['embarkDate']}T06:30",
                    "endDate": f"{test_data['debarkDate']}T23:59", "activityGroupCodes": ["RT"], "statuses": [],
                    "access": [],
                    "activityEndDateGE": None, "activityName": ""}
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            assert len(_content) != 0, "empty dinning activity list"
        else:
            pytest.skip(msg="today is not a debark day hence skipping this test case")

    @pytestrail.case(67643605)
    def test_24_reinstate_cancelled_slot(self, config, test_data, rest_ship):
        """
        to verify cancelled slot reinstate successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"activityGroupCode": test_data['activityGroupCode'],
                 "activityId": test_data['activities']['activityGroupId'],
                 "code": test_data['activityCode'],
                 "activitySlots":
                     [{"isCancelled": False, "activitySlotId": test_data['activitySlotId'],
                       "code": test_data['activitySlotCode']}]}]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content['failedActivityCodes']) == 0, "slot not reinstate successfully"
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1, "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "activityGroupCode": test_data['activityGroupCode'],
                "disableDbSearch": False, "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activitySlotCode": test_data['activitySlotCode'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            if not activity['activitySlots'][0]['isCancelled'] == False:
                raise Exception ("slot not reinstate successfully")

    @pytestrail.case(67643606)
    def test_25_move_slot(self, config, test_data, rest_ship):
        """
        Verify Slots moving successfully
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/{test_data['activityCode']}")
        body = {"code": test_data['activityCode'],
                "activitySlots":
                    [{"code": test_data['activitySlotCode'],
                      "startDateTime": f"{test_data['embarkDate']}T00:00:00",
                      "endDateTime": f"{test_data['debarkDate']}T23:59",
                      "moveBookings": True}]}
        rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1, "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "activityGroupCode": test_data['activityGroupCode'],
                "disableDbSearch": False, "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activitySlotCode": test_data['activitySlotCode'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            if not activity['activitySlots'][0]['code'] == test_data['activitySlotCode'] and \
               activity['activitySlots'][0]['endDateTime'] != test_data['end_time']:
                raise Exception("slot not moved successfully")

    @pytestrail.case(67645976)
    def test_26_stop_slot(self, config, test_data, rest_ship):
        """
        Verify Slots stopped successfully
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/slots/"
                                                                     f"{test_data['activitySlotCode']}")
        body = {"isBookingStopped": True, "isWaitListEnable": False, "code": test_data['activitySlotCode'],
                "capacity":
                    {"totalCapacity": 0, "holdCapacity": 0, "maximumWaitlistCount": 0, "minimumSelling": 0}}
        rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1, "includeVendorDetail": True,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activitySlotCode": test_data['activitySlotCode'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            assert activity['activitySlots'][0]['isBookingStopped'] == True, "slot not stopped successfully"

    @pytestrail.case(67646023)
    def test_27_filter_shore_thing_activity_list(self, config, test_data, rest_ship):
        """
        filter and verify Shore Thing Activity list
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?parts=sellingPrices&page=1")
        body = {"startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "requiredNoSlot": False, "includeSellingPrices": True, "includeCancelledSlots": True,
                "includeActivityGroupName": True, "voyageNumber": test_data['voyageNumber'],
                "includeVendorDetail": False, "canFilterByPort": True, "page": 1,
                "sortField": None, "type": None, "statuses": ["OPEN", "CLOSE"], "access": ["PUBLIC", "PRIVATE"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"], "fetchActivityNameFromCMS": True, "activityName": None,
                "activityGroupCode": "PA", "disableDbSearch": False, "portCodes": [test_data['activities']['portCode']]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        if len(_content['activities']) == 0:
            logger.info('empty Shore Thing Activity list')
        for activity in _content['activities']:
            if not activity['activityGroupCode'] == 'PA':
                raise Exception('GroupCode not matched')

    @pytestrail.case(67646024)
    def test_28_filter_spa_activity_list(self, config, test_data, rest_ship):
        """
        filter and verify Spa Activity list
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        activity_date = test_data['crew_framework']['currentDate'][:10]
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?parts=sellingPrices&page=1")
        body = {"startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "requiredNoSlot": False, "includeSellingPrices": True, "includeCancelledSlots": True,
                "includeActivityGroupName": True, "voyageNumber": test_data['voyageNumber'],
                "includeVendorDetail": False, "canFilterByPort": True, "page": 1,
                "sortField": "", "type": "", "statuses": ["OPEN", "CLOSE"], "access": ["PUBLIC", "PRIVATE"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"], "fetchActivityNameFromCMS": True, "activityName": "",
                "activityGroupCode": "SPA", "disableDbSearch": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['activities']) == 0:
            if not test_data['embarkDate'] == activity_date:
                raise Exception('empty Spa Activity list')
            logger.info('empty Spa Activity List')
        for activity in _content['activities']:
            if not activity['activityGroupCode'] == 'SPA':
                raise Exception('GroupCode not matched')

    @pytestrail.case(67646070)
    def test_29_filter_restaurant_activity_list(self, config, test_data, rest_ship):
        """
        filter and verify Restaurant Activity list
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/slots/search?sort=startDateTime&"
                                                                     "sort=activityCode&sort=status&page=&")
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59", "activityGroupCode": "RT",
                "statuses": ["OPEN", "CLOSE"], "access": ["PUBLIC", "PRIVATE"], "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "activityEndDateGE": None, "activityName": "", "includeArrivalCount": True, "disableDbSearch": False}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if "data" not in _content:
            pytest.skip('empty Restaurant Activity list')
        for activity in _content['data']:
            if not activity['groupCode'] == 'RT':
                raise Exception('GroupCode not matched')

    @pytestrail.case(67646071)
    def test_30_edit_activity_organizer(self, config, test_data, rest_ship):
        """
        To verify Organizer for Activity edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['activities']['activityId'] = activity['activityId']
            test_data['activities']['activityAccountId'] = activity['activityAccounts'][0]['activityAccountId']
            test_data['activities']['departmentCode'] = activity['activityAccounts'][0]['departmentCode']
            test_data['activities']['vendoractivityid'] = activity['vendorActivity'][0]['vendoractivityid']
            test_data['activities']['vendorId'] = activity['vendorActivity'][0]['vendorId']
            test_data['activities']['accountType'] = activity['activityAccounts'][0]['accountType']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/{test_data['activityCode']}")
        body = {"activityGroupCode": test_data['activityGroupCode'],
                "activityId": test_data['activities']['activityId'], "code": test_data['activityCode'],
                "inheritParentToChild": False, "sendSlotTimeUpdateNotification": True,
                "isMoveSlotEnabled": True, "activitySlots": [],
                "activityAccounts":
                    [{"departmentCode": test_data['activities']['departmentCode'], "isDeleted": False,
                      "activityAccountId": test_data['activities']['activityAccountId'],
                      "activityId": test_data['activities']['activityId'],
                      "accountType": test_data['activities']['accountType']}],
                "vendorActivity":
                    [{"activityId": test_data['activities']['activityId'],
                      "vendoractivityid": test_data['activities']['vendoractivityid'],
                      "vendorId": test_data['activities']['vendorId']}]}
        rest_ship.send_request(method="Patch", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            for booking in activity['vendorActivity']:
                if booking['vendorId'] == test_data['activities']['vendorId'] and \
                        booking['vendoractivityid'] == test_data['activities']['vendoractivityid']:
                    break
            for booking in activity['activityAccounts']:
                if booking['departmentCode'] == test_data['activities']['departmentCode'] and \
                    booking['accountType'] == test_data['activities']['accountType'] and \
                        booking['activityAccountId'] == test_data['activities']['activityAccountId']:
                    break
            else:
                raise Exception('Organizer for Activity not edited successfully')

    @pytestrail.case(67646072)
    def test_31_edit_activity_location_and_time(self, config, test_data, rest_ship):
        """
        To verify Location & Time for Activity edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['activities']['activityId'] = activity['activityId']
            test_data['activities']['activityLocationId'] = activity['activityLocation']['activityLocationId']
            test_data['activities']['activityDuration'] = activity['activityLocation']['activityDuration']
            test_data['activities']['locationType'] = activity['activityLocation']['locationType']
            test_data['activities']['activitySlotsCode'] = activity['activitySlots'][00]['code']
            test_data['activities']['activitySlotId'] = activity['activitySlots'][00]['activitySlotId']
            test_data['activities']['startTime'] = activity['meetingLocations'][0]['startTime']
            test_data['activities']['endTime'] = activity['meetingLocations'][0]['endTime']
            test_data['activities']['meetingLocationId'] = activity['meetingLocations'][0]['meetingLocationId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"activityGroupCode": test_data['activityGroupCode'],
                 "activityId": test_data['activities']['activityId'], "code":test_data['activityCode'],
                 "activitySlots":
                     [{"activitySlotId": test_data['activities']['activitySlotId'],
                       "code": test_data['activities']['activitySlotsCode'], "bookingCloseDuration": 0,
                       "meetingLocations":
                           [{"locationType": test_data['activities']['locationType'],
                             "meetingLocationId": test_data['activities']['meetingLocationId'],
                             "startTime": test_data['activities']['startTime'],
                             "endTime": test_data['activities']['endTime'],
                             "deckCode": "", "directionCode": "", "sectionCode": "", "arsVenueId": ""}],
                       "activityLocation":
                           {"locationType": test_data['activities']['locationType'],
                            "activityLocationId": test_data['activities']['activityLocationId'],
                            "activityDuration": test_data['activities']['activityDuration'], "deckCode": "",
                            "directionCode": "", "sectionCode": "", "arsVenueId": ""},
                       "sendMeetingLocationNotification": True}]}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'],
                "activitySlotCode": test_data['activities']['activitySlotsCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            if activity['activityLocation']['activityDuration'] == test_data['activities']['activityDuration'] and \
                activity['activityLocation']['activityLocationId'] == test_data['activities']['activityLocationId'] \
                    and activity['activityLocation']['locationType'] == test_data['activities']['locationType']:
                pass
            for booking in activity['meetingLocations']:
                if booking['meetingLocationId'] == test_data['activities']['meetingLocationId']:
                    break
            else:
                raise Exception('Location & Time for Activity not edited successfully')

    @pytestrail.case(67646073)
    def test_32_edit_activity_pricing(self, config, test_data, rest_ship):
        """
        To verify Pricing for Activity edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['activities']['activityId'] = activity['activityId']
            test_data['activities']['sellingPriceId'] = activity['sellingPrices'][0]['sellingPriceId']
            test_data['activities']['price'] = activity['sellingPrices'][0]['price']
            test_data['activities']['cancellationChargeId'] = activity['cancellationCharges'][0]['cancellationChargeId']
            test_data['activities']['chargeValue'] = activity['cancellationCharges'][0]['chargeValue']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/{test_data['activityCode']}")
        body = {"activityGroupCode": test_data['activityGroupCode'],
                "activityId": test_data['activities']['activityId'], "code": test_data['activityCode'],
                "inheritParentToChild": False, "sendSlotTimeUpdateNotification": True, "isMoveSlotEnabled": True,
                "activitySlots": [], "priceType": _content['activities'][0]['priceType'],
                "sellingPrices":
                    [{"isDeleted": False, "sellingPriceId": test_data['activities']['sellingPriceId'],
                      "activityId": test_data['activities']['activityId'],
                      "personType": _content['activities'][0]['sellingPrices'][0]['personType'],
                      "levelType": _content['activities'][0]['sellingPrices'][0]['levelType'],
                      "levelValue": _content['activities'][0]['sellingPrices'][0]['levelValue'],
                      "minAge": 0, "maxAge": 99, "price": random.randint(100, 200),
                      "tax": _content['activities'][0]['sellingPrices'][0]['tax']},
                     {"levelType": _content['activities'][0]['sellingPrices'][0]['levelType'],
                      "levelValue": _content['activities'][0]['sellingPrices'][0]['levelValue'],
                      "personType": _content['activities'][0]['sellingPrices'][0]['personType'], "isDeleted": True}],
                "cancellationCharges":
                    [{"isDeleted": False, "cancellationChargeId": test_data['activities']['cancellationChargeId'],
                      "chargeUnit": _content['activities'][0]['cancellationCharges'][0]['chargeUnit'],
                      "chargeValue": random.randint(10, 80),
                      "maxDuration": random.randint(20, 500),
                      "isNoShow": False,
                      "activityId": test_data['activities']['activityId']}]}
        rest_ship.send_request(method="Patch", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            for booking in activity['sellingPrices']:
                if booking['sellingPriceId'] == test_data['activities']['sellingPriceId'] and \
                        booking['price'] != test_data['activities']['price']:
                    break
            for booking in activity['cancellationCharges']:
                if booking['cancellationChargeId'] == test_data['activities']['cancellationChargeId'] and \
                        booking['chargeValue'] != test_data['activities']['chargeValue']:
                    break
            else:
                raise Exception('Pricing for Activity not edited successfully')

    @pytestrail.case(67646385)
    def test_33_edit_activity_others_info(self, config, test_data, rest_ship):
        """
        To verify Others Info for Activity edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for activity in _content['activities']:
            test_data['activities']['waiverOpeningDuration'] = activity['activityDetail']['waiverOpeningDuration']
            test_data['activities']['activityId'] = activity['activityId']
            test_data['activities']['activityLocation'] = activity['activityLocation']
            test_data['activities']['capacity'] = activity['capacity']
            test_data['activities']['sellingPrices'] = activity['sellingPrices']
            test_data['activities']['costPrices'] = activity['costPrices']
            test_data['activities']['meetingLocations'] = activity['meetingLocations']
            test_data['activities']['cancellationCharges'] = activity['cancellationCharges']
            test_data['activities']['activityTypes'] = activity['activityTypes']
            test_data['activities']['activityAccounts'] = activity['activityAccounts']
            test_data['activities']['vendorActivity'] = activity['vendorActivity']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"isDeleted": False, "createdByUser": _content['activities'][0]['createdByUser'],
                 "activityId": _content['activities'][0]['createdByUser'],
                 "bookingCloseDuration": 0, "activityGroupCode": _content['activities'][0]['activityGroupCode'],
                 "activityGroupId": _content['activities'][0]['activityGroupId'],
                 "portCode": _content['activities'][0]['portCode'], "level": _content['activities'][0]['level'],
                 "priceType": _content['activities'][0]['priceType'], "code": _content['activities'][0]['code'],
                 "currencyCode": _content['activities'][0]['currencyCode'],
                 "activityDetail":
                     {"waiverOpeningDuration": random.randint(50, 2000), "isWaiverRequired": False},
                 "activityLocation": test_data['activities']['activityLocation'],
                 "capacity": test_data['activities']['capacity'],
                 "sellingPrices": test_data['activities']['sellingPrices'],
                 "costPrices": test_data['activities']['costPrices'],
                 "meetingLocations": test_data['activities']['meetingLocations'],
                 "cancellationCharges": test_data['activities']['cancellationCharges'],
                 "activityTypes": test_data['activities']['activityTypes'],
                 "activityTags": [],
                 "activityAccounts": test_data['activities']['activityAccounts'],
                 "isEnable": True, "isWaitListEnable": False, "isPackageable": False, "isBookable": True,
                 "isGiftable": False, "isVIP": False, "accessType": _content['activities'][0]['accessType'],
                 "isMultipleBookingAllowed": False, "name": _content['activities'][0]['name'],
                 "cmsId": _content['activities'][0]['cmsId'],
                 "activityGroupName": _content['activities'][0]['activityGroupName'],
                 "vendorActivity": test_data['activities']['vendorActivity'],
                 "includeDefaultSlot": False, "overRideSlots": False, "isUpdateRequest": False,
                 "sendMeetingLocationNotification": True, "creationTime": _content['activities'][0]['creationTime'],
                 "modifiedByUser": _content['activities'][0]['modifiedByUser'],
                 "modificationTime": _content['activities'][0]['modificationTime']}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "access": ["PRIVATE", "PUBLIC"],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "includeVendorDetail": True, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for activity in _content['activities']:
            if not activity['activityDetail']['waiverOpeningDuration'] != \
                    test_data['activities']['waiverOpeningDuration'] and \
                    activity['sellingPrices'][0]['activityId'] == test_data['activities']['activityId']:
                raise Exception('Others Info for Activity not edited successfully')

    @pytestrail.case(67646074)
    def test_34_edit_activity_capacity(self, config, test_data, rest_ship):
        """
        To verify Capacity for Activity edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['parent'] = {}
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'], "includeActivityGroupName": True,
                "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['activities']['activityId'] = activity['activityId']
            test_data['activities']['totalCapacity'] = activity['capacity']['totalCapacity']
            test_data['activities']['holdCapacity'] = activity['capacity']['holdCapacity']
            test_data['activities']['capacityId'] = activity['capacity']['capacityId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/activities/{test_data['activityCode']}")
        body = {"activityGroupCode": test_data['activityGroupCode'],
                "activityId": test_data['activities']['activityId'],
                "code": test_data['activityCode'], "inheritParentToChild": False,
                "sendSlotTimeUpdateNotification": True, "isMoveSlotEnabled": True, "activitySlots": [],
                "capacity":
                    {"capacityId": test_data['activities']['capacityId'],
                     "totalCapacity": random.randint(1000, 2000),
                     "holdCapacity": random.randint(10, 150),
                     "minimumSelling": 0, "maximumWaitlistCount": 0}}
        rest_ship.send_request(method="Patch", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1&parts=activityAccounts,"
                                                                     "activitySlots.capacity,costPrices")
        body = {"activityCode": test_data['activityCode'],
                "includeActivityGroupName": True, "includeCancelledSlots": True, "includeDetails": True, "page": 1,
                "startDate": f"{test_data['embarkDate']}T00:00:00", "endDate": f"{test_data['debarkDate']}T23:59",
                "activityGroupCode": test_data['activityGroupCode'], "includeVendorDetail": True,
                "fetchActivityNameFromCMS": True, "disableDbSearch": False, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "voyageNumber": test_data['voyageNumber'], "activityEndDateGE": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        for activity in _content['activities']:
            test_data['parent']['totalCapacity'] = activity['capacity']['totalCapacity']
            test_data['parent']['holdCapacity'] = activity['capacity']['holdCapacity']
            test_data['parent']['activityId'] = activity['activityId']
            test_data['parent']['activityCode'] = activity['code']
            test_data['parent']['venueId'] = activity['activityLocation']['arsVenueId']
            test_data['parent']['locationType'] = activity['activityLocation']['locationType']
            if not activity['capacity']['capacityId'] == test_data['activities']['capacityId'] and \
               activity['capacity']['holdCapacity'] != test_data['activities']['holdCapacity'] and \
               activity['capacity']['totalCapacity'] != test_data['activities']['totalCapacity']:
                raise Exception('Capacity for Activity not edited successfully')

    @pytestrail.case(67830276)
    def test_35_filter_private_events(self, config, test_data, rest_ship):
        """
        To filter and verify Private Events
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/slots/search?sort=startDateTime&"
                                                                     "sort=activityCode&sort=status&page=&")
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59", "activityGroupCode": "NET", "statuses": [],
                "access": ["PUBLIC", "PRIVATE"], "slotAccessTypes": ["PRIVATE"], "activityEndDateGE": None,
                "activityName": "", "includeArrivalCount": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if "data" not in _content:
            pytest.skip('empty Private Events list')
        for activity in _content['data']:
            if not activity['slotAccess'] == 'PRIVATE':
                raise Exception('Private Events not filtered successfully')

    @pytestrail.case(68042125)
    def test_36_edit_quick_code(self, config, test_data, rest_ship):
        """
        To verify QuickCode edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/quickcodes/search?page=1")
        body = {"activityGroupCodes": [test_data['activityGroupCode']], "unassigned": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activityQuickCodes', _content)
        assert _content['activityQuickCodes'] != 0, 'Empty QuickCode List'
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/quickcodes/bulkupdate")
        body = [{"isDeleted": False, "activityQuickCodeId": _content['activityQuickCodes'][00]['activityQuickCodeId'],
                 "prepaidBookingRefundQC": _content['activityQuickCodes'][00]['prepaidBookingRefundQC'],
                 "onboardBookingQC": _content['activityQuickCodes'][00]['onboardBookingQC'],
                 "fullRefundQC": _content['activityQuickCodes'][00]['fullRefundQC'],
                 "partialRefundQC": _content['activityQuickCodes'][00]['partialRefundQC'],
                 "activityId": _content['activityQuickCodes'][00]['activityId'],
                 "portCode": _content['activityQuickCodes'][00]['portCode']}]
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content['failedActivityId']) == 0, 'QuickCode not edited successfully'

    @pytestrail.case(67646387)
    def test_37_mark_slot_private(self, config, test_data, rest_ship):
        """
        To verify slot is marked as private
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['private_slot'] = {}
        slot_date = test_data['crew_framework']['currentDate']
        start_date = f"{slot_date[:10]}T{slot_date[11:16]}"
        end = test_data['debark']
        end_date = f"{end[:10]}T{end[11:16]}"
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/slots/search?")
        params = {"sort": "startDateTime", "sort": "activityCode", "sort": "status", "page": ""}
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": start_date,
                "endDate": end_date, "activityGroupCode": "NET",
                "statuses": [], "access": ["PUBLIC", "PRIVATE"], "slotAccessTypes": ["PUBLIC"],
                "activityEndDateGE": None, "activityName": "", "includeArrivalCount": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if "data" not in _content:
            test_data['activity_slot_availability'] = False
            pytest.skip("Skipping this TC as no activity slots available")
            
        test_data['activity_slot_availability'] = True
        test_data['private_slot']['activityCode'] = _content['data'][00]['activityCode']
        test_data['private_slot']['activitySlotCode'] = _content['data'][00]['activitySlotCode']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search?page=1")
        body = {"activityCodes": [test_data['private_slot']['activityCode']],
                "includeDetails": True, "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                "includeCancelledSlots": True, "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC"], "includeVendorDetail": True, "fetchActivityNameFromCMS": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('activities', _content)
        test_data['private_slot']['activityId'] = _content['activities'][0]['activityId']
        test_data['private_slot']['activitySlotId'] = _content['activities'][0]['activitySlots'][0]['activitySlotId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/bulkupdate")
        body = [{"activityGroupCode": 'NET',
                 "activityId": test_data['private_slot']['activityId'],
                 "code": test_data['private_slot']['activityCode'],
                 "activitySlots":
                     [{"accessType": "PRIVATE",
                       "activitySlotId": test_data['private_slot']['activitySlotId'],
                       "code": test_data['private_slot']['activitySlotCode']}]}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {"page": 1}
        body = {"activityCodes": [test_data['private_slot']['activityCode']], "includeDetails": True,
                "activitySlotCode": test_data['private_slot']['activitySlotCode'], "includeCancelledSlots": True,
                "access": ["PRIVATE", "PUBLIC"], "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "includeVendorDetail": True, "fetchActivityNameFromCMS": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('activities', _content)
        if len(_content['activities']) == 0:
            raise Exception("Getting no activities in response.")
        for activity in _content['activities']:
            if activity['code'] == test_data['private_slot']['activityCode']:
                for slot in activity['activitySlots']:
                    if slot['accessType'] == 'PRIVATE':
                        break
                else:
                    raise Exception("slot not marked as Private")

    @pytestrail.case(67647168)
    def test_38_book_private_slot_for_sailor(self, config, test_data, guest_data, rest_ship):
        """
        To verify Private slot for Sailor is created successfully
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        for guest in guest_data:
            url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'), "guests/search/guestdetail")
            params = {"size": 200}
            body = {"voyageNumber": test_data['voyageNumber'], "nameSearchString": guest['FirstName'],
                    "includeTravelWithGuests": True, "excludeCancelled": True, "includeCheckinStatus": True}
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            is_key_there_in_dict('_embedded', _content)
            test_data['private_slot']['guestId'] = _content['_embedded']['guestDetails'][0]['guestId']
            test_data['private_slot']['reservationNumber'] = _content['_embedded']['guestDetails'][0]['reservationNumber']
            test_data['private_slot']['reservationGuestId'] = _content['_embedded']['guestDetails'][0]['reservationGuestId']
            url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
            body = {"activityCode": test_data['private_slot']['activityCode'],
                    "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                    "activityGroupCode": "NET", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                    "bookedByPersonTypeCode": "C", "payeePersonId": test_data['private_slot']['reservationGuestId'],
                    "payeePersonTypeCode": "G", "isGift": False, "additionalNotes": "",
                    "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                    "personDetails":
                        [{"personId": test_data['private_slot']['reservationGuestId'], "personTypeCode": "G",
                          "reservationNumber": test_data['private_slot']['reservationNumber'],
                          "guestId": test_data['private_slot']['guestId']}],
                    "reservationNumber": test_data['private_slot']['reservationNumber'],
                    "voyageNumber": test_data['voyageNumber'],
                    "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                    "endDate": f"{test_data['debarkDate']}T23:59"}
            try:
                _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            except Exception as exp:
                if "409" and "Booking already exists for following person" in exp.args[0]:
                    continue
                else:
                    raise Exception(exp)
            is_key_there_in_dict('bookings', _content)
            for activity in _content['bookings']:
                test_data['private_slot']['activityBookingId'] = activity['activityBookingId']
            assert len(_content) != 0, 'Private slot is not created for sailor successfully'
            break
        else:
            pytest.skip("Booking already exits for both the sailors of guest_data.")

    @pytestrail.case(68077429)
    def test_39_sending_message_from_booking_slot(self, config, test_data, rest_ship):
        """
        To verify message from Booking slots successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "notifications")
        body = {"activityBookingIds": [test_data['private_slot']['activityBookingId']], "messageTitle": "Hello ",
                "messageDescription": title, "externalUrl": "https://www.google.com",
                "voyageNumber": test_data['voyageNumber'], "notificationType": "push"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) == 0, 'Message not Sent'

    @pytestrail.case(68077397)
    def test_40_booking_conflict(self, config, test_data, rest_ship):
        """
        To verify Booking Conflict
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        try:
            if not test_data['activity_slot_availability']:
                pytest.skip("Skipping this TC due to slots unavailability")
            url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
            body = {"activityCode": test_data['private_slot']['activityCode'],
                    "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                    "activityGroupCode": "NET", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                    "bookedByPersonTypeCode": "C", "payeePersonId": test_data['private_slot']['reservationGuestId'],
                    "payeePersonTypeCode": "G", "isGift": False, "additionalNotes": "",
                    "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                    "personDetails":
                        [{"personId": test_data['private_slot']['reservationGuestId'], "personTypeCode": "G",
                          "reservationNumber": test_data['private_slot']['reservationNumber'],
                          "guestId": test_data['private_slot']['guestId']}],
                    "reservationNumber": test_data['private_slot']['reservationNumber'],
                    "voyageNumber": test_data['voyageNumber'],
                    "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                    "endDate": f"{test_data['debarkDate']}T23:59"}
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
            raise Exception('No Booking Conflicts')
        except:
            logger.info(msg='Booking is having a Conflict')

    @retry_when_fails(retries=5, interval=3)
    @pytestrail.case(68077430)
    def test_41_book_private_slot_for_crew(self, config, test_data, rest_ship):
        """
        To verify Private slot for crew is created successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        slot_date = test_data['crew_framework']['currentDate']
        slot_time = str(datetime.strptime(slot_date.split(" ", 1)[1], "%I:%M:%S %p"))
        test_data['crew_framework']['ship_time'] = f"{slot_date[:10]}T{slot_time[11:]}"
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        test_data['private_slot']['crew_personId'] = []
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-embarkation-admin/search")
        params = {
                'q': 'ab',
                'voyagenumber': test_data['voyageNumber'],
                'isCrew': "true",
                'isGuest': "false",
                'isVisitor': "false"
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params,  auth="crew").content
        if len(_content['teamMembers']) == 0:
            pytest.skip("Skipping as no crew found in search")

        for crew in _content['teamMembers']:
            test_data['private_slot']['crew_personId'].append(crew['personId'])
        person_id = random.choice(test_data['private_slot']['crew_personId'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
        body = {"activityCode": test_data['private_slot']['activityCode'],
                "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                "activityGroupCode": "NET", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                "bookedByPersonTypeCode": "C", "payeePersonId": person_id,
                "payeePersonTypeCode": "C", "isGift": False, "additionalNotes": "",
                "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                "personDetails": [{"personId": person_id, "personTypeCode": "C"}],
                "reservationNumber": "",
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59:59"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('bookings', _content)
        assert len(_content) != 0, 'Private slot is not created for crew successfully'

    @pytestrail.case(68077431)
    def test_42_mark_slot_public(self, config, test_data, rest_ship):
        """
        To verify message from Booking slots successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "activities/bulkupdate")
        body = [{"activityGroupCode": 'NET',
                 "activityId": test_data['private_slot']['activityId'],
                 "code": test_data['private_slot']['activityCode'],
                 "activitySlots":
                     [{"accessType": "PUBLIC",
                       "activitySlotId": test_data['private_slot']['activitySlotId'],
                       "code": test_data['private_slot']['activitySlotCode']}]}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activities/search")
        params = {"page": 1}
        body = {"activityCodes": [test_data['private_slot']['activityCode']], "includeDetails": True,
                "activitySlotCode": test_data['private_slot']['activitySlotCode'], "includeCancelledSlots": True,
                "access": ["PRIVATE", "PUBLIC"], "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "includeVendorDetail": True, "fetchActivityNameFromCMS": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('activities', _content)
        if len(_content['activities']) == 0:
            raise Exception("Getting no activities in response.")
        for activity in _content['activities']:
            if activity['code'] == test_data['private_slot']['activityCode']:
                for slot in activity['activitySlots']:
                    if slot['accessType'] == 'PUBLIC':
                        break
                else:
                    raise Exception("slot not marked as Public")

    @pytestrail.case(68852213)
    def test_43_shore_thing_slot_booking_for_company_account_for_sailor(self, config, test_data, rest_ship):
        """
        To verify Shore-Thing Slots for sailors for Company-Accounts booked successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        test_data['private_slot']['companyAccount_pa'] = []
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "activities/slots/search")
        params = {"sort": "startDateTime", "sort": 'activityCode', "sort": 'status', "page": 1}
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": test_data['crew_framework']['ship_time'],
                "endDate": f"{test_data['debarkDate']}T23:59:59", "activityGroupCode": "PA",
                "statuses": [], "access": ["PUBLIC", "PRIVATE"], "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "activityEndDateGE": None, "activityName": "", "includeArrivalCount": True,
                "portCodes": test_data['portCodes']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if "data" not in _content:
            test_data['shore_thing_availability'] = False
            pytest.skip("Skipping this TC as no shore things activity available")

        test_data['shore_thing_availability'] = True
        test_data['private_slot']['activityCode'] = _content['data'][0]['activityCode']
        test_data['private_slot']['activitySlotCode'] = _content['data'][0]['activitySlotCode']
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'), "propertyFolio")
        params = {"page": 1, "size": 99}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for account in _content['_embedded']['dXPPropertyFolios']:
            test_data['private_slot']['companyAccount_pa'].append(account['folioNumber'])
        test_data['private_slot']['companyAccount'] = random.choice(test_data['private_slot']['companyAccount_pa'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
        body = {"activityCode": test_data['private_slot']['activityCode'],
                "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                "activityGroupCode": "PA", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                "bookedByPersonTypeCode": "C", "payeePersonId": test_data['private_slot']['reservationGuestId'],
                "payeePersonTypeCode": "G", "isGift": False, "isCheckedIn": True, "additionalNotes": "",
                "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                "personDetails":
                    [{"personId": test_data['private_slot']['reservationGuestId'], "personTypeCode": "G",
                      "reservationNumber": test_data['private_slot']['reservationNumber'],
                      "guestId": test_data['private_slot']['guestId']}],
                "reservationNumber": test_data['private_slot']['reservationNumber'],
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59",
                "companyAccountId": test_data['private_slot']['companyAccount']}
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            assert _content['bookings'][0]['status'] == 'CONFIRMED', \
                'Shore-Thing Slots for sailors for Company-Accounts not booked successfully'
        except Exception as exp:
            if "Booking already exists for following person" in exp.args[0]:
                pytest.skip(msg="Booking has Conflict for Shore-Thing Slots for sailors using Company Account")
            elif "Sorry, bookings for selected activity code/slotCode are closed/stopped" in exp.args[0]:
                pytest.skip(msg="Booking has been closed for the selected activity")
            else:
                raise Exception(exp)

    @pytestrail.case(68852214)
    def test_44_shore_thing_slot_booking_for_company_account_for_crew(self, config, test_data, rest_ship):
        """
        To verify Shore-Thing Slots for crew for Company-Accounts booked successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        elif not test_data['shore_thing_availability']:
            pytest.skip("Skipping this TC due to shore thing activity unavailability")
        person_id = random.choice(test_data['private_slot']['crew_personId'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
        body = {"activityCode": test_data['private_slot']['activityCode'],
                "activitySlotCode": test_data['private_slot']['activitySlotCode'],
                "activityGroupCode": "PA", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                "bookedByPersonTypeCode": "C", "payeePersonId": person_id,
                "payeePersonTypeCode": "C", "isGift": False, "isCheckedIn": True, "additionalNotes": "",
                "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                "personDetails": [{"personId": person_id, "personTypeCode": "C"}],
                "reservationNumber": "",
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59:59",
                "companyAccountId": test_data['private_slot']['companyAccount']}
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            assert _content['bookings'][0]['status'] == 'CONFIRMED', \
                'Shore-Thing Slots for crew for Company-Accounts not booked successfully'
        except Exception as exp:
            if "Booking already exists for following person" in exp.args[0]:
                pytest.skip(msg="Booking has Conflict for Shore-Thing Slots for crew using Company-Accounts")
            elif "Sorry, bookings for selected activity code/slotCode are closed/stopped" in exp.args[0]:
                pytest.skip(msg="Booking has been closed for the selected activity")
            else:
                raise Exception(exp)

    @pytestrail.case(68852215)
    def test_45_inventoried_slot_booking_for_company_account_for_sailor(self, config, test_data, rest_ship):
        """
        To verify Ent-Inventoried Slots for sailors for Company-Accounts booked successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        test_data['private_slot']['companyAccount_iet'] = []
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "activities/slots/search")
        params = {"sort": "startDateTime", "sort": 'activityCode', "sort": 'status', "page": 1}
        body = {"voyageNumber": test_data['voyageNumber'], "startDate": test_data['crew_framework']['ship_time'],
                "endDate": f"{test_data['debarkDate']}T23:59:59", "activityGroupCode": "IET",
                "statuses": [], "access": ["PUBLIC", "PRIVATE"], "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "activityEndDateGE": None, "activityName": "", "includeArrivalCount": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if "data" not in _content:
            test_data['ent_inventoried_availability'] = False
            pytest.skip("Skipping this TC as no Ent-Inventoried Activities available")

        test_data['ent_inventoried_availability'] = True
        test_data['private_slot']['iet_activityCode'] = _content['data'][0]['activityCode']
        test_data['private_slot']['iet_activitySlotCode'] = _content['data'][0]['activitySlotCode']
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'), "propertyFolio")
        params = {"page": 1, "size": 99}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for account in _content['_embedded']['dXPPropertyFolios']:
            test_data['private_slot']['companyAccount_iet'].append(account['folioNumber'])
        test_data['private_slot']['companyAccount'] = random.choice(test_data['private_slot']['companyAccount_iet'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
        body = {"activityCode": test_data['private_slot']['iet_activityCode'],
                "activitySlotCode": test_data['private_slot']['iet_activitySlotCode'],
                "activityGroupCode": "IET", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                "bookedByPersonTypeCode": "C", "payeePersonId": test_data['private_slot']['companyAccount'],
                "payeePersonTypeCode": "G", "isGift": False, "additionalNotes": "",
                "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                "personDetails":
                    [{"personId": test_data['private_slot']['reservationGuestId'], "personTypeCode": "G",
                      "reservationNumber": test_data['private_slot']['reservationNumber'],
                      "guestId": test_data['private_slot']['guestId']}],
                "reservationNumber": test_data['private_slot']['reservationNumber'],
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59",
                "companyAccountId": test_data['private_slot']['companyAccount']}
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            assert _content['bookings'][0]['status'] == 'CONFIRMED', \
                'Ent-Inventoried Slots for sailors for Company-Accounts not booked successfully'
        except Exception as exp:
            if "Booking already exists for following person" or \
                    "Sorry,no inventory available on this slot" in exp.args[0]:
                pytest.skip(msg="Booking has Conflict or No Inventory available")
            else:
                raise Exception(exp)

    @pytestrail.case(68852216)
    def test_46_inventoried_slot_booking_for_company_account_for_crew(self, config, test_data, rest_ship):
        """
        To verify Ent-Inventoried Slots for crew for Company-Accounts booked successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['activity_slot_availability']:
            pytest.skip("Skipping this TC due to slots unavailability")
        elif not test_data['ent_inventoried_availability']:
            pytest.skip("Skipping this TC as no Ent-Inventoried Activities available")
        person_id = random.choice(test_data['private_slot']['crew_personId'])
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "bookings")
        body = {"activityCode": test_data['private_slot']['iet_activityCode'],
                "activitySlotCode": test_data['private_slot']['iet_activitySlotCode'],
                "activityGroupCode": "IET", "bookedByPersonId": "f887a2b8-a027-4cbe-b09a-07e307de2429",
                "bookedByPersonTypeCode": "C", "payeePersonId": test_data['private_slot']['companyAccount'],
                "payeePersonTypeCode": "C", "isGift": False, "additionalNotes": "",
                "discountReasonId": "", "discountAmount": None, "discountUnit": "PERCENT",
                "personDetails": [{"personId": person_id, "personTypeCode": "C"}],
                "reservationNumber": "",
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code, "startDate": f"{test_data['embarkDate']}T00:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59:59",
                "companyAccountId": test_data['private_slot']['companyAccount']}
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            assert _content['bookings'][0]['status'] == 'CONFIRMED', \
                'Ent-Inventoried Slots for crew for Company-Accounts not booked successfully'
        except Exception as exp:
            if "Booking already exists for following person" or \
                    "Sorry,no inventory available on this slot" in exp.args[0]:
                pytest.skip(msg="Booking has Conflict or No Inventory available")
            else:
                raise Exception(exp)

    @retry_when_fails(retries=10, interval=10)
    @pytestrail.case(68852217)
    def test_47_searched_sailor_in_calendar(self, config, test_data, rest_ship):
        """
        To verify that searched sailor details is identical in calendar
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'), "guests/search/guestdetail")
        params = {"size": 200}
        body = {"voyageNumber": test_data['voyageNumber'], "nameSearchString": test_data['guest_details']['firstName'],
                "excludeCancelled": True, "includeCheckinStatus": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        test_data['parent']['firstName'] = _content['_embedded']['guestDetails'][0]['firstName']
        test_data['parent']['lastName'] = _content['_embedded']['guestDetails'][0]['lastName']
        test_data['parent']['reservationGuestId'] = _content['_embedded']['guestDetails'][0]['reservationGuestId']
        test_data['parent']['guestId'] = _content['_embedded']['guestDetails'][0]['guestId']
        fullName = f"{test_data['parent']['firstName']} {test_data['parent']['lastName']}"
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'), "guests/search/guestdetail")
        params = {"size": 200}
        body = {"voyageNumber": test_data['voyageNumber'], "nameSearchString": fullName,
                "excludeCancelled": True, "includeCheckinStatus": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if not test_data['parent']['guestId'] == _content['_embedded']['guestDetails'][0]['guestId'] and\
            test_data['parent']['reservationGuestId'] == _content['_embedded']['guestDetails'][0]['reservationGuestId']:
            raise Exception('searched sailor details not matched in calendar')

