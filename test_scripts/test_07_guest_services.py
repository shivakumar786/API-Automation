__author__ = 'anshuman.goyal'
__maintainer__ = 'sarvesh.singh'

from virgin_utils import *

@pytest.mark.GUEST_SERVICES
@pytest.mark.run(order=8)
class TestGuestServices:
    """
    Test Suite to test Guest Services and check data in ship couch
    """

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(381547)
    def test_01_guest_service_reservations(self, config, test_data, rest_shore):
        """
        Get Guest Details by Reservation ID's
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _res_id = test_data['signupGuest']['reservationId']
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'reservations', _res_id)
        _content_shore = rest_shore.send_request(method="GET", url=url, auth="admin").content
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservations', _res_id)
        _content_ship = rest_shore.send_request(method="GET", url=url, auth="admin").content
        compare_ship_shore_data(_content_shore, _content_ship,
                                {'lockedDate', 'lockedBy', 'rowCheckSum', 'loyaltyLevelTypeCode'})

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(381548)
    def test_02_guest_service_guests(self, config, rest_shore, guest_data, rest_ship):
        """
        Get Guest Details by Reservation ID's
        :param config:
        :param rest_shore:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'guests', guest['guestId'])
            _content_shore = rest_shore.send_request(method="GET", url=url, auth="admin").content
            url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'guests', guest['guestId'])
            _content_ship = rest_ship.send_request(method="GET", url=url, auth="bearer").content
            compare_ship_shore_data(_content_shore, _content_ship,
                                    {'lockedDate', 'lockedBy', 'rowCheckSum', 'loyaltyLevelTypeCode', 'issueDate', 'verifiedBy', 'guestMediaItemId', 'issueCountryCode', 'mediaType', 'scannedCopyMediaItemId', 'expiryDate', 'verificationStatus', 'rowCheckSum', 'identificationId', 'birthCountryCode', 'documentTypeCode', 'isOcrDirty', 'multiMediaItemId'})

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(381549)
    def test_03_guest_service_reservation_guests(self, config, rest_shore, guest_data, rest_ship):
        """
        Get Guest Details by Reservation ID's
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'reservationguests',
                          guest['reservationGuestId'])
            _content_shore = rest_shore.send_request(method="GET", url=url, auth="admin").content
            url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservationguests',
                          guest['reservationGuestId'])
            _content_ship = rest_ship.send_request(method="GET", url=url, auth="bearer").content
            compare_ship_shore_data(_content_shore, _content_ship,
                                    {'lockedDate', 'lockedBy', 'rowCheckSum', 'loyaltyLevelTypeCode',
                                            'isVerifiedAtTerminal', 'documentId', 'guestDocumentId', 'documentType'})

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(381550)
    def test_04_guest_service_guest_moderation_details(self, config, rest_shore, guest_data):
        """
        Get Guest Details by Reservation ID's
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            params = {
                'reservation-guest-id': guest['reservationGuestId']
            }
            url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'),
                          'guestmoderationdetails/search/findbyreservationguestid')
            _content_shore = rest_shore.send_request(method="GET", url=url, params=params, auth="admin").content
            url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                          'guestmoderationdetails/search/findbyreservationguestid')
            _content_ship = rest_shore.send_request(method="GET", url=url, params=params, auth="bearer").content
            compare_ship_shore_data(_content_shore, _content_ship,
                                    {'lockedDate', 'lockedBy', 'rowCheckSum', 'loyaltyLevelTypeCode'})

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(199)
    def test_05_get_details_by_reservation_ids(self, config, test_data, rest_shore):
        """
        Get Guest Details by Reservation ID's
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      "reservationguests/search/findbyreservationids")
        reservation = test_data['signupGuest']['reservationId']
        body = {"reservationIds": [reservation]}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="admin").content
        if '_embedded' not in _content or _content['_embedded'] is None:
            raise Exception(f"ERROR: Reservation #{reservation} not synced to ship !!")
        else:
            reservation_check = _content['_embedded']['reservationGuests'][0]['reservationId']
            if reservation != reservation_check:
                raise Exception(f"ERROR: Reservation #{reservation} does not match")

    @pytestrail.case(194)
    def test_06_guest_details_verification_ship_core(self, config, test_data, rest_shore, guest_data):
        """
        Verify Ship Code Guest Details
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            'page': '1',
            'size': '200'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'guests/search')
        test_data['reservationGuestIds'] = []
        for count, guest in enumerate(guest_data):
            test_data['reservationGuestIds'].append(guest['reservationGuestId'])
        body = {"shipCode": config.ship.code, "reservationGuestIds": test_data['reservationGuestIds']}
        _content = rest_shore.send_request(method="POST", url=_url, json=body, params=params, auth="admin").content
        for _data in _content['_embedded']['bulkAPIResponses']:
            for guest in guest_data:
                if guest['reservationGuestId'] == _data['reservationGuestId']:
                    assert guest['firstName'].upper() == _data['firstName'].upper(), "ERROR: firstName mis-match !!"
                    assert guest['lastName'].upper() == _data['lastName'].upper(), "ERROR: lastName mis-match !!"
                    assert guest['birthDate'] == _data['birthDate'], "ERROR: birthDate mis-match !!"
                    """assert guest['isPrimary'] == _data['isPrimary'], "ERROR: isPrimary mis-match !!"""""
                    assert guest['CitizenshipCountryCode'] == _data[
                        'citizenshipCountryCode'], "ERROR: citizenshipCountryCode mis-match !!"
                    is_key_there_in_dict('reservationNumber', _data)
                    is_key_there_in_dict('stateroom', _data)
                    is_key_there_in_dict('travelWithUpdated', _data)
                    is_key_there_in_dict('voyageNumber', _data)
                    is_key_there_in_dict('embarkDate', _data)
                    is_key_there_in_dict('debarkDate', _data)

    @pytestrail.case(209)
    def test_07_security_photo_multimedia_check(self, config, rest_shore, guest_data):
        """
        Security Photo Check
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _id = guest['SecurityPhotoUrl'].rsplit('/', 1)[-1]
            _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f'/mediaitems/{_id}/details')
            _content = rest_shore.send_request(method="GET", url=_url, auth="admin").content
            assert _id == _content['mediaItemId'], "ERROR: Document ID Mismatch !!"
            for mediaGroupItemStatus in _content['mediaGroupItemStatuses']:
                assert mediaGroupItemStatus['isDeleted'] is False, "ERROR: isDeleted != False !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(204)
    def test_08_validate_ship_data_in_ship_couch(self, config, request, test_data, rest_shore, guest_data):
        """
        Check Shore<->Couch data Sync
        :param request:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/ship_data_ship_couch.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        for count, guest in enumerate(guest_data):
            ship_url = f"{config.ship.sync}/GuestStatus::{guest['reservationGuestId']}"
            _content = rest_shore.send_request(method="GET", url=ship_url).content
            guest["health_info"] = _content
            # Check all keys are there in received document.
            for _key in _ship_data:
                is_key_there_in_dict(_key, _content)

            assert _content['ShipCode'] == config.ship.code, "Ship Code Mismatch !!"
            assert _content['EmbarkDate'] == test_data['voyage']['startDate'], "EmbarkDate Mismatch !!"
            assert _content['DebarkDate'] == test_data['voyage']['endDate'], "DebarkDate Mismatch !!"
            assert _content['VoyageNumber'] == test_data['voyage']['id'], "PreValidateStatus Mismatch !!"

    @retry_when_fails(retries=60, interval=5)
    @pytestrail.case(186251)
    def test_09_validate_guest_identification_data_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Function to check Guest Identification data in Shore and Ship Couch
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _exp_date = guest['passportExpiry']
            _number = guest['passportNumber']
            _doc_type = "P"
            _res_c_code = guest['CitizenshipCountryCode']
            _url = f"{config.ship.sync}/GuestIdentification::{_res_id}"
            _content = rest_shore.send_request(method="GET", url=_url).content

            # Verify Identification
            for identification in _content['Identifications']:
                assert identification['ExpiryDate'] == _exp_date
                assert identification['GuestID'] == guest['guestId'], "Guest ID Mismatch !!"
                assert identification['FirstName'] == guest['FirstName'], "Guest First Name Mismatch !!"
                assert identification['DocumentTypeCode'] == _doc_type, "Document Type Code Mismatch !!"
                assert identification['LastName'] == guest['LastName'], "Last Name Mismatch !!"
                assert identification['Number'] == _number, "Number Mismatch !!"
                assert identification['BirthCountryCode'] == guest[
                    'CitizenshipCountryCode'], "Birth Country Code Mismatch !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(167)
    def test_10_validate_guest_identification_in_ship_couch(self, config, test_data, rest_shore, guest_data):
        """
        Function to check Guest Identification data in Shore and Ship Couch
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestIdentification::{_res_id}"
            _content = rest_shore.send_request(method="GET", url=_url).content

            # Verify Passport
            passport_id = guest['PassportDocumentId'].rsplit('/', 1)[-1]
            for identification in _content['Identifications']:
                assert identification['ScannedCopyMediaItemID'] == passport_id, "Passport ID Mismatch !!"

            # Verify Visa
            if test_data['countries'][0] != "US":
                visa_id = guest['VisaDocumentId'].rsplit('/', 1)[-1]
                for visa in _content['VisaDetail']:
                    assert visa['ScannedCopyMediaItemID'] == visa_id, "Visa ID Mismatch !!"

            # Make sure we have correct Document Type
            assert _content['type'] == "GuestIdentification", "Wrong Document Type !!"

    @pytestrail.case(115)
    def test_11_validate_media_items_in_ship_couch(self, config, request, rest_shore, guest_data):
        """
        Check Guest Personal data in Shore and Ship Couch has synced or not
        :param config:
        :param request:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/ship_data_couch.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestPersonalInformation::{_res_id}"

            security_id = guest['SecurityPhotoUrl'].rsplit('/', 1)[-1]

            _content = rest_shore.send_request(method="GET", url=_url).content

            # Check all keys are there in received document.
            for _key in _ship_data:
                is_key_there_in_dict(_key, _content, False)
            guest_data[count]['CouchGuestDetail'] = _content

            assert security_id == _content['GuestSecurityMediaItemID'], "Security Photo Mismatch !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(186252)
    def test_12_validate_guest_pre_cruise_data_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Check Guest Personal data in Shore and Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestPreCruise::'f'{_res_id}')
            _content = rest_shore.send_request(method="GET", url=_url).content

            for _pre_cruise in _content['PreCruiseDetails']:
                for _precruise in _pre_cruise['FlightDetails']:
                    assert _precruise['AirlineCode'] == guest['flightDetails'][
                        'airlineCode'], "Guest Air Line  Code Mismatch !!"
                    assert _precruise['ArrivalAirportCode'] == guest['flightDetails'][
                        'arrivalAirportCode'], "Guest Air Line ID Mismatch !!"
                    assert _precruise['ArrivalCity'] == guest['flightDetails'][
                        'arrivalCity'], "Guest City Code Mismatch !!"
                    assert _precruise['ArrivalTime'] == guest['flightDetails'][
                        'arrivalTime'], "Guest Arrival Time Mismatch !!"
                    assert _precruise['DepartureAirportCode'] == guest['flightDetails'][
                        'departureAirportCode'], "Guest Departure Air Port Code Mismatch !!"
                    assert _precruise['DepartureCity'] == guest['flightDetails'][
                        'departureCity'], "Guest Departure City Mismatch !!"
                    assert _precruise['FlightNumber'] == guest['flightDetails'][
                        'number'], "Guest Flight Number Mismatch !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(186253)
    def test_13_validate_guest_post_cruise_data_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Check Guest Personal data in Shore and Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestPostCruise::'f'{_res_id}')
            _content = rest_shore.send_request(method="GET", url=_url).content

            for _pre_cruise in _content['PostCruiseDetails']:
                for _precruise in _pre_cruise['FlightDetails']:
                    assert _precruise['AirlineCode'] == guest['flightDetails'][
                        'airlineCode'], "Guest Air Line  Code Mismatch !!"
                    assert _precruise['ArrivalAirportCode'] == guest['flightDetails'][
                        'arrivalAirportCode'], "Guest Air Line ID Mismatch !!"
                    assert _precruise['ArrivalCity'] == guest['flightDetails'][
                        'arrivalCity'], "Guest City Code Mismatch !!"
                    assert _precruise['ArrivalTime'] == guest['flightDetails'][
                        'arrivalTime'], "Guest Arrival Time Mismatch !!"
                    assert _precruise['DepartureAirportCode'] == guest['flightDetails'][
                        'departureAirportCode'], "Guest Departure Air Port Code Mismatch !!"
                    assert _precruise['DepartureCity'] == guest['flightDetails'][
                        'departureCity'], "Guest Departure City Mismatch !!"
                    assert _precruise['FlightNumber'] == guest['flightDetails'][
                        'number'], "Guest Flight Number Mismatch !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(11777687)
    def test_14_validate_guest_payment_information_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Check Guest Payment info in Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestPayForDetail::'f'{_res_id}')

            _content = rest_shore.send_request(method="GET", url=_url).content
            assert _content['PaymentId'] == guest["details_content"]['guestDetail']['paymentInfo'][
                'paymentId'], f"{_content['PaymentId']} Payment Id not sync to Ship Couche or mis match"
            assert _content[
                       'PaymentMode'] == "Credit Card", f"{_content['PaymentMode']} Payment Mode not sync" \
                                                        f" to Ship Couche or mis match"
            assert _content['PaymentModeID'] == guest["details_content"]['guestDetail']['paymentInfo'][
                'paymentModeId'], f"{_content['paymentModeId']} Payment Mode Id not sync to Ship Couche or mis match"

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(11777690)
    def test_15_validate_guest_cruise_contract_information_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Check Guest Cruise Contract info in Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestStatus::'f'{_res_id}')

            _content = rest_shore.send_request(method="GET", url=_url).content
            assert _content[
                'IsCruiseContractSigned'], f"{_content['IsCruiseContractSigned']}Contract not sync to" \
                                           f" Ship Couch or mismatch"
            assert _content[
                       'CruiseContractSignedByReservationguestID'] == guest[
                       'reservationGuestId'], f"{_content['reservationGuestId']} reservation Guest ID is mismatch"

    @pytestrail.case(11777688)
    def test_16_validate_guest_health_information_in_ship_couch(self, config, rest_shore, guest_data, test_data):
        """
        Check Guest Health info in Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :param test_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestHealthDetail::'f'{_res_id}')

            _content = rest_shore.send_request(method="GET", url=_url).content
            couch_question = []
            shore_core_question = []

            for data in test_data['health_question']['healthQuestions']:
                shore_core_question.append(data['questionCode'])

            for health_questions in _content['HealthDetails']:
                couch_question.append(health_questions['Code'])

            missing_question = list(set(shore_core_question) - set(couch_question))

            if len(missing_question) > 0:
                raise Exception(f"{missing_question} is missing in Ship Couch")
            else:
                for health_questions in _content['HealthDetails']:
                    assert health_questions['Answer'] == 'NO', "Question Answer is not matching"
            return

    @pytestrail.case(26111506)
    def test_17_validate_guest_pregnancy_information_in_ship_couch(self, guest_data):
        """
        Check Guest Pregnancy info in Ship Couch has synced or not
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _content = guest["health_info"]
            if guest['genderCode'] == 'Female':
                assert _content['PregnancyWeeks'] == guest['noOfWeeks'], "Pregnancy Weeks is not matching for the guest"
            else:
                continue

    @pytestrail.case(11777691)
    def test_18_validate_guest_emergency_information_in_ship_couch(self, config, rest_shore, guest_data):
        """
        Check Guest emergency data in Shore and Ship Couch has synced or not
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(config.ship.sync, 'GuestPersonalInformation::'f'{_res_id}')

            _content = rest_shore.send_request(method="GET", url=_url).content
            for emergency_contacts in _content['EmergencyContacts']:
                assert emergency_contacts['Name'] == guest['emergencyContactDetails'][
                    'name'], "Guest Emergency Name Mismatch !!"
                assert emergency_contacts['PhoneNumber'] == guest['emergencyContactDetails'][
                    'phoneNumber'], "Guest Emergency Contact Number Mismatch !!"
                assert emergency_contacts['Relationship'] == guest['emergencyContactDetails'][
                    'relationship'], "Guest Emergency Relationship Mismatch !!"

    @pytestrail.case(11777696)
    def test_19_validate_guest_embarkation_slot_information_in_ship_couch(self, guest_data):
        """
        Check Guest Embarkation Slot info in Ship Couch has synced or not
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _content = guest["health_info"]
            if guest['isVIP'] is not True:
                assert _content['BoardingNumber'] == guest[
                    'slotnumber'], "Boarding Number is not matching for the guest"
                assert _content['BoardingTime'] == guest['slot'].rsplit(':', 1)[
                    0], "Boarding Time is not matching for the guest"
            else:
                continue

    @pytestrail.case(33979027)
    def test_20_verify_elastic_search_request(self, guest_data, config, rest_ship):
        """
        Check elastic request is not giving time out.
        :param guest_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _url = config.ship.url
        if "integration" in _url:
            _url = urljoin(getattr(config.ship.contPath, 'url.path.elasticsearch'),
                           f"int-ship-{guest_data[0]['health_info']['VoyageNumber'].lower()}/_search")
        elif "k8s" in _url:
            _url = urljoin(getattr(config.ship.contPath, 'url.path.elasticsearch'),
                           f"qa-ship-{guest_data[0]['health_info']['VoyageNumber'].lower()}/_search")

        _body = {
            "query": {
                "multi_match": {
                    "query": guest_data[0]['CouchGuestDetail']['ReservationNumber'],
                    "fields": [
                        "FirstName",
                        "LastName",
                        "FullName",
                        "Stateroom",
                        "ReservationNumber"
                    ]
                }
            }
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=_body).content
        is_key_there_in_dict("hits", _content)
        is_key_there_in_dict("hits", _content["hits"])
        for _contentData in _content["hits"]["hits"]:
            is_key_there_in_dict('_source', _contentData)
            assert len(_contentData['_source']) != 0, "Elastic Search result is coming empty."
        for detail in _content['hits']['hits'][0:]:
            assert detail['_source']['ReservationNumber'] == guest_data[0]['CouchGuestDetail'][
                'ReservationNumber'], "Elastic search is not giving correct result."

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(75588748)
    def test_21_validate_guest_middle_name_ship_core(self, config, rest_shore, test_data, rest_ship):
        """
        Validate Guest Middle Name (edited through MOCI) sync to ship core
        :param config:
        :param rest_shore:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                      f"crew-embarkation-admin/reservation-guests/{test_data['m_guestId']}")
        params = {"shipCode": config.ship.code, "fetchAdditionalDetails": True}
        _content = rest_shore.send_request(method="GET", params=params, url=url, auth="admin").content
        test_data['m_guestId'] = _content['guestId']
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'guests', test_data['m_guestId'])
        _content_shore = rest_shore.send_request(method="GET", url=url, auth="admin").content
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'guests', test_data['m_guestId'])
        _content_ship = rest_ship.send_request(method="GET", url=url, auth="bearer").content
        assert test_data['m_guest_middleName'] == _content_shore['middleName'], "Middle Name not synced to ship side"
        assert test_data['m_guest_middleName'] == _content_ship['middleName'], "Middle Name not synced to ship side"