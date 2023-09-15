__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.RTS
@pytest.mark.run(order=3)
class TestRTS:
    """
    Test Suite to test RTS
    """

    @pytestrail.case(186255)
    def test_01_start_up(self, config, test_data, rest_shore):
        """
        Test RTS Startup
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['rts'] = dict()
        rest_shore.userToken = test_data['signupGuest']['accessToken']
        url = urljoin(config.shore.url, "rts-bff/startup")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        test_data['rts'].update(_content)

    @pytestrail.case(186219)
    def test_02_health_check(self, config, test_data, rest_shore, guest_data):
        """
        Test RTS Guest Health
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        test_data['healthCheck'] = dict()
        for count, guest in enumerate(guest_data):
            res_guest_id = guest['reservationGuestId']
            res_id = guest['reservationId']
            params = {"reservation-guest-id": res_guest_id, "reservation-id": res_id}
            url = urljoin(config.shore.url, "rts-bff/healthcheck")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            assert _content['isHealthCheckComplete'] is False, "isHealthCheckComplete is True !!"
            test_data['healthCheck'].update(_content)

    @pytestrail.case(186211)
    def test_03_landing_check(self, config, rest_shore, guest_data):
        """
        Test RTS Guest Health
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            guest_data[count]['rts'] = dict()
            res_guest_id = guest['reservationGuestId']
            res_id = guest['reservationId']
            params = {
                "reservation-guest-id": res_guest_id,
                "reservation-number": res_id
            }
            url = urljoin(config.shore.url, "rts-bff/landing")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            guest_data[count]['rts'].update(_content)

    @pytestrail.case(1064153)
    def test_04_check_task_percentage_before_rts(self, config, rest_shore, guest_data):
        """
        To check that the task percentage should be 0 before rts
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-number": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/landing")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            tasks = _content['tasksCompletionPercentage']
            for task in tasks:
                if task == 'pregnancy' and guest['genderCode'] != "F":
                    continue
                if tasks[task] != 0:
                    logger.info(f"{task} is not 0% before starting RTS")

    @pytestrail.case(186212)
    def test_05_security_update_check(self, config, guest_data, rest_shore):
        """
        Test RTS Guest security details
        :param guest_data:
        :param rest_shore:
        :return:
        """

        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-number": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/landing")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            tasks = _content['tasksCompletionPercentage']
            if tasks['security'] == 100:
                logger.info("Security photo is already uploaded !!")
                continue
            url = guest['rts']['security']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            # is_key_there_in_dict(response_get.content, 'securityPhotoURL')

            url = guest['rts']['security']['detailsURL']
            body = {
                "securityPhotoURL": guest['SecurityPhotoUrl'],
                "isDeleted": False
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)

            # Download Security Photo and check if we are able to do so
            url = _content['finalPage']['imageURL']
            assert _content['tasksCompletionPercentage']['security'] == 100, "security is not 100% !!"
            if not rest_shore.send_request(method="GET", url=url).ok:
                raise Exception(f"Cannot Download Security Photo !!")

    @pytestrail.case(186213)
    def test_06_travel_document_update_check(self, config, test_data, guest_data, rest_shore):
        """
        Test RTS check Guest travel documents
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_shore:
        :return:
        """
        # Update Guest Data, that is required for RTS. Make sure we save this for future use
        for count, guest in enumerate(guest_data):
            expiry = generate_document_expiry(from_year=int(datetime.now().year) + 1)
            guest_data[count]['passportNumber'] = str(generate_document_number())
            guest_data[count]['passportExpiry'] = str(expiry.strftime('%Y-%m-%d'))
            guest_data[count]['mrzExpiry'] = str(expiry.strftime('%y%m%d'))
            guest_data[count]['countryCode'] = convert_country_code(guest['citizenshipCountryCode'], 3)
            guest_data[count]['visaCountryCode'] = convert_country_code(guest['citizenshipCountryCode'], 2)

            url = guest['rts']['travelDocuments']['detailsURLV1']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content

            # Generate MRZ Document
            mrz_data = {
                'document_type': "P", 'country_code': guest['countryCode'], 'given_names': guest['firstName'],
                'surname': guest['lastName'], 'document_number': guest['passportNumber'],
                'birth_date': modify_birth_date(guest['birthDate']), 'sex': guest['genderCode'],
                'expiry_date': guest['mrzExpiry'], 'nationality': guest['countryCode']
            }

            with open(GenerateMrzImages(**mrz_data).mrz_image(), "rb") as imageFile:
                _str = base64.b64encode(imageFile.read())
            _body = _str.decode("utf-8")
            body = {"photoContent": _body}
            params = {"isV1Call": True}
            url = urljoin(config.shore.url, "rts-bff/traveldocuments/ocr/passport")
            _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth='user').content
            if len(_content) != 0:
                is_key_there_in_dict('number', _content)
                is_key_there_in_dict('surname', _content)
                is_key_there_in_dict('givenName', _content)
                is_key_there_in_dict('issueCountryCode', _content)
                is_key_there_in_dict('expiryDate', _content)
            else:
                raise Exception("No data displayed after OCR Scan!!")

        for count, guest in enumerate(guest_data):
            url = guest['rts']['travelDocuments']['detailsURLV1']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            is_key_there_in_dict('travelDocumentsDetail', _content)
            is_key_there_in_dict('primaryDocumentOptions', _content)

            guest['PassportDocumentId'] = upload_media_file(config, rest_shore,
                                                            GenerateMrzImages(**mrz_data).mrz_image())

            # To add passport
            body = {
                "travelDocumentsDetail": {
                    "countryOfResidenceCode": guest['CitizenshipCountryCode'],
                    "identificationDocuments": [
                        {
                            "birthCountryCode": guest['CitizenshipCountryCode'],
                            "documentTypeCode": "P",
                            "isDeleted": False,
                            "documentPhotoUrl": guest['PassportDocumentId'],
                            "number": guest['passportNumber'],
                            "gender": "F",
                            "expiryDate": guest['passportExpiry'],
                            "issueCountryCode": guest['CitizenshipCountryCode'],
                            "birthDate": guest['BirthDate'],
                            "givenName": guest['firstName'],
                            "surname": guest['lastName'],
                            "issueDate": "Jan 01 2011"
                        }
                    ]
                }
            }

            _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content

            # To add Visa for non US
            if test_data['countries'][0] != "US":
                # Generate Visa Document
                del mrz_data['document_number']
                mrz_data['document_type'] = "V"
                mrz_data['document_number'] = generate_document_number()

                with open(GenerateMrzImages(**mrz_data).mrz_image(), "rb") as imageFile:
                    _str = base64.b64encode(imageFile.read())
                _body = _str.decode("utf-8")
                params = {"isV1Call": True}
                body = {"photoContent": _body}
                url = urljoin(config.shore.url, "rts-bff/traveldocuments/ocr/visa")
                _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth='user').content
                if len(_content) != 0:
                    is_key_there_in_dict('surname', _content)
                    is_key_there_in_dict('givenName', _content)
                    is_key_there_in_dict('issueCountryCode', _content)
                else:
                    raise Exception("No data displayed after OCR Scan!!")

                guest['visaDocumentId'] = upload_media_file(config, rest_shore,
                                                            GenerateMrzImages(**mrz_data).mrz_image())
                body = {
                    "countryOfResidenceCode": guest['visaCountryCode'],
                    "travelDocumentsDetail": {
                        "visaInfoList": [{
                            "documentTypeCode": "V",
                            "documentPhotoUrl": guest['visaDocumentId'],
                            "number": guest['passportNumber'],
                            "surname": guest['lastName'],
                            "givenName": guest['firstName'],
                            "issueCountryCode": "US",
                            "expiryDate": guest['passportExpiry'],
                            "visaTypeCode": "H-1B1",
                            "visaEntries": "MULTIPLE",
                            "isDeleted": False
                        }]
                    }
                }
                url = guest['rts']['travelDocuments']['detailsURLV1']
                _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content

                # Post Cruise
                body = {
                    "postCruiseInfo": {
                        "addressInfo": {
                            "countryCode": guest['CitizenshipCountryCode'],
                            "city": guest['Addresses'][0]['city'],
                            "line1": guest['Addresses'][0]['lineOne'],
                            "line2": guest['Addresses'][0]['lineTwo'],
                            "zipCode": guest['Addresses'][0]['zipCode'],
                            "stateCode": guest['Addresses'][0]['stateCode'],
                            "addressTypeCode": "OTHER"
                        }
                    }
                }
                _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content

            is_key_there_in_dict('tasksCompletionPercentage', _content)
            _progress = _content['tasksCompletionPercentage']
            assert _progress['travelDocuments'] == 100, "travelDocuments is not 100% !!"

    @pytestrail.case(186215)
    def test_07_pregnancy_update_check(self, rest_shore, guest_data):
        """
        Test RTS Guest Pregnancy
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['rts']['pregnancy']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content

            if guest['genderCode'] == 'F' or guest['genderCode'][0] == 'F':
                guest['pregnancyStatus'] = True
                guest['noOfWeeks'] = 15
                body = {
                    "pregnancyDetails": {
                        "isPregnant": guest['pregnancyStatus'],
                        "noOfWeeks": guest['noOfWeeks']
                    }
                }
                _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content
                is_key_there_in_dict('tasksCompletionPercentage', _content)
                is_key_there_in_dict('finalPage', _content)
                _progress = _content['tasksCompletionPercentage']
                assert _progress['pregnancy'] == 100, f"pregnancy is not 100% !!"

    @pytestrail.case(186216)
    def test_08_voyage_contract_update_check(self, rest_shore, guest_data):
        """
        Test RTS Guest Contracts
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['rts']['voyageContract']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content

            body = {
                "isCruiseContractSigned": True,
                "contractSignedDate": str(datetime.now(tz=pytz.utc).date()),
                "signForOtherGuests": [],
                "signedByReservationGuestId": guest['reservationGuestId']
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)
            _progress = _content['tasksCompletionPercentage']
            assert _progress['voyageContract'] == 100, f"voyageContract is not 100% !!"

    @pytestrail.case(186217)
    def test_09_emergency_contract_update_check(self, rest_shore, guest_data):
        """
        Test RTS Guest emergency Contracts
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['rts']['emergencyContact']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            body = {
                "emergencyContactDetails": {
                    "name": generate_first_name(), "relationship": "FRIEND", "dialingCountryCode": "US",
                    "phoneNumber": str(generate_phone_number())
                }
            }
            guest_data[count].update(body)
            _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)
            _progress = _content['tasksCompletionPercentage']
            assert _progress['emergencyContact'] == 100, f"emergencyContact is not 100% !!"

    @pytestrail.case(186218)
    def test_10_embarkation_slot_update_check(self, config, rest_shore, guest_data):
        """
        Test RTS Guest Embarkation Slot
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            guest_data[count]['flightDetails'] = dict()
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/embarkationslot")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            guest_data[count]['isVIP'] = _content['isVip']

            if not guest['isVIP']:
                is_key_there_in_dict('availableSlots', _content)
                for slots in _content['availableSlots']:
                    guest['slot'] = slots['time']
                    guest['slotnumber'] = slots['number']
                    break
            else:
                guest['slotnumber'] = 9

            guest_data[count]['flightDetails'].update({
                "airlineCode": "AA", "departureAirportCode": "YYZ", "arrivalAirportCode": "MIA",
                "number": "1565", "departureTime": "11:25:00", "arrivalTime": "14:41:00", "arrivalCity": "Zanesville",
                "departureCity": "Wollaston Lake"
            })
            body = {
                "isFlyingIn": True, "isVip": guest['isVIP'],
                "flightDetails": guest_data[count]['flightDetails'],
                "slotNumber": guest['slotnumber'],
                "isParkingOpted": False,
                "optedByReservationGuestIds": [],
                "postCruiseInfo": {"isFlyingOut": True, "flightDetails": guest_data[count]['flightDetails']}
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, params=params, auth='user').content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)
            _progress = _content['tasksCompletionPercentage']
            assert _progress['embarkationSlotSelection'] == 100, f"embarkationSlotSelection is not 100% !!"

    @pytestrail.case(186214)
    def test_11_payment_update(self, config, test_data, rest_shore, guest_data):
        """
        Test Guest Payment Method Update on RTS
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/paymentmethod")
            method = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            guest['payment_method'] = method['paymentModes'][0]
            body = {
                "selectedPaymentMethodCode": method['paymentModes'][0], "partyMembers": [], "isDeleted": False,
                "cardPaymentToken": test_data['paymentDetails']['payment_token']
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, params=params, auth='user').content

            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)

            _progress = _content['tasksCompletionPercentage']
            assert _progress['paymentMethod'] == 100, f"paymentMethod is not 100% !!"

    @pytestrail.case(186257)
    def test_12_check_health_status_after_rts(self, config, test_data, rest_shore, guest_data):
        """
        Test Guest Status After RTS
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-number": test_data['reservationNumber']
            }
            url = urljoin(config.shore.url, "rts-bff/landing")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            tasks = _content['tasksCompletionPercentage']
            for task in tasks:
                if task == 'pregnancy' and guest['genderCode'][0] != "F":
                    continue
                assert tasks[task] == 100, f"{task} is not 100% after performing RTS"

    @pytestrail.case(15312384)
    def test_13_get_health_check_question(self, config, test_data, rest_shore):
        """
        Get the Health Question
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
            "reservation-id": test_data['signupGuest']['reservationId'],
        }
        url = urljoin(config.shore.url, "rts-bff/healthcheck")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

        test_data['health_question'] = dict()
        healthQuestions = []

        for questions_code in _content['landingPage']['questionsPage']['healthQuestions']:
            healthQuestions.append({'questionCode': questions_code['questionCode'], 'selectedOption': 'NO'})
        test_data['health_question'].update({'healthQuestions': healthQuestions, 'signForOtherGuests': []})

        assert _content['buttons']['okay'] == 'Okay', "Button value is not Okay"

    @pytestrail.case(9002000)
    def test_14_update_health_check_question(self, config, test_data, rest_shore, guest_data):
        """
        Update the Health Question and check the status
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_shore:
        :return:
        """
        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }

            url = urljoin(config.shore.url, "rts-bff/healthcheck")
            _content = rest_shore.send_request(method="PUT", url=url, params=params, json=test_data['health_question'],
                                             auth="user").content

            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

            assert _content['buttons']['okay'] == 'Okay', "Button value is not Okay"
