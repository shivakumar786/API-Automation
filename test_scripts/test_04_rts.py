__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.SHORE
@pytest.mark.RTS
@pytest.mark.run(order=4)
class TestRTS:
    """
    Test Suite to test RTS
    """

    @pytestrail.case(186204)
    def test_01_sign_up_connect_booking(self, config, test_data, rest_shore, guest_data):
        """
        Verify signup with email functionality
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        first_name = generate_first_name(from_saved=True)
        last_name = generate_last_name(from_saved=True)
        test_data['usernameConnect'] = generate_email_id(first_name=first_name, last_name=last_name)
        url = urljoin(config.shore.url, "user-account-service/signup")
        body = {
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "birthDate": guest['birthDate'],
            "email": test_data['usernameConnect'],
            "firstName": first_name,
            "userType": "guest",
            "lastName": last_name,
            "password": "Voyages@9876"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('accessToken', _content['authenticationDetails'])

    @pytestrail.case(55245705)
    def test_02_user_logout(self, config, rest_shore):
        """
        Log out Sailor app shore
        :param config:
        :param rest_shore:
        :return:
        """
        _url = urljoin(config.shore.url, "user-account-service/logout")
        _content = rest_shore.send_request(method="POST", url=_url, auth="user").content

    @pytestrail.case(7883784)
    def test_03_update_email(self, config, test_data, guest_data, rest_shore):
        """
        Update the email id
        :param config:
        :param test_data:
        :param guest_data :
        :param rest_shore:
        :return:
        """
        for email_id in guest_data:
            if email_id['Email'] == test_data['signupGuest']['email']:
                old_user_name = email_id['Email']
                test_data['oldEmail'] = old_user_name
                break
        else:
            raise Exception("E-Mail ID Not Found !!")

        test_data['signupGuest']['email'] = generate_email_id(first_name=guest_data[0]['FirstName'],
                                                              last_name=guest_data[0]['LastName'])
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/account/username")
        body = {"oldUserName": old_user_name, "newUserName": test_data['signupGuest']['email']}
        _content = rest_shore.send_request(method="PUT", url=url, json=body, auth="bearer").content

        url = urljoin(config.shore.url, "user-account-service/signin/email")
        body = {"userName": test_data['signupGuest']['email'], "password": test_data['signupGuest']['password']}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        test_data['signupGuest']['accessToken'] = f"{_content['tokenType']} {_content['accessToken']}"
        rest_shore.userToken = test_data['signupGuest']['accessToken']

    @pytestrail.case(7883785)
    def test_04_update_password(self, config, test_data, rest_shore):
        """
        Update the email id
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/account/password")
        test_data['signupGuest']['password'] = 'Voyages@9899'
        body = {
            "userName": test_data['signupGuest']['email'],
            "newPassword": test_data['signupGuest']['password'],
            "oldPassword": test_data["signupGuest"]['oldPassword']
        }
        _content = rest_shore.send_request(method="PUT", url=url, json=body, auth="user").content

    @pytestrail.case(186207)
    def test_05_login(self, config, test_data, rest_shore):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(config.shore.url, "user-account-service/signin/email")
        body = {
            "userName": test_data['signupGuest']['email'],
            "password": test_data['signupGuest']['password']
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        test_data['signupGuest']['accessToken'] = f"{_content['tokenType']} {_content['accessToken']}"
        rest_shore.userToken = test_data['signupGuest']['accessToken']

    @pytestrail.case(9918211)
    def test_06_verify_cms_sailor_app(self, config, rest_shore):
        """
        Test CMS call to launch the app
        :param config:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.contentmanagement'), "/content/sailorApp/all")
        _content = rest_shore.send_request(method="POST", url=url, auth="user").content

        is_key_there_in_dict('messages', _content)
        is_key_there_in_dict('resources', _content)
        is_key_there_in_dict('styles', _content)

    @pytestrail.case(186254)
    def test_07_rts_bff_assets(self, config, rest_shore):
        """
        Test RTS Assets
        :param config:
        :param rest_shore:
        :return:
        """
        url = urljoin(config.shore.url, "rts-bff/assets")
        response = rest_shore.send_request(method="GET", url=url, auth="user")
        if len(response) == 0:
            raise Exception("Response is Empty in rts-bff/assets")

    @pytestrail.case(186255)
    def test_08_start_up(self, config, test_data, rest_shore):
        """
        Test RTS Startup
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['rts'] = dict()
        rest_shore.userToken = test_data['signupGuest']['accessToken']
        url = urljoin(config.shore.url, "rts-bff/startup")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('configurations', _content)
        is_key_there_in_dict('lookupDataURL', _content)
        is_key_there_in_dict('multimediaUploadURL', _content)
        is_key_there_in_dict('securityPhotoValidatorURL', _content)
        is_key_there_in_dict('landingURL', _content)

        test_data['rts'].update(_content)

    @pytestrail.case(186219)
    def test_09_health_check(self, config, test_data, rest_shore, guest_data):
        """
        Test RTS Guest Health
        :param config:
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
            is_key_there_in_dict('updateURL', _content)
            is_key_there_in_dict('isFitToTravel', _content)
            is_key_there_in_dict('isHealthCheckComplete', _content)
            assert _content['isHealthCheckComplete'] is False, "isHealthCheckComplete is True !!"
            test_data['healthCheck'].update(_content)

    @pytestrail.case(186256)
    def test_10_look_up(self, test_data, rest_shore):
        """
        Test RTS Startup
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['rts']['lookupDataURL']
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('referenceData', _content)

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844834'), pytestrail.param('USA', '186211')])
    def test_11_landing_check(self, config, rest_shore, test_data, guest_data, v_guest_data, country):
        """
        Test RTS Guest Health
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

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
            is_key_there_in_dict('voyageContract', _content)
            is_key_there_in_dict('reservationId', _content)
            is_key_there_in_dict('voyageContract', _content)
            is_key_there_in_dict('emergencyContact', _content)
            is_key_there_in_dict('security', _content)
            is_key_there_in_dict('travelDocuments', _content)
            is_key_there_in_dict('paymentMethod', _content)
            is_key_there_in_dict('tasksOrder', _content)
            is_key_there_in_dict('detailsURL', _content['security'])

            guest_data[count]['rts'].update(_content)

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844835'), pytestrail.param('USA', '1064153')])
    def test_12_check_task_percentage_before_rts(self, config, rest_shore, test_data, guest_data, v_guest_data,
                                                 country):
        """
        To check that the task percentage should be 0 before rts
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

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
                assert tasks[task] == 0, f"{task} is not 0% before starting RTS"

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844836'), pytestrail.param('USA', '186212')])
    def test_13_security_update_check(self, test_data, guest_data, v_guest_data, rest_shore, country):
        """
        Test RTS Guest security details
        :param test_data:
        :param guest_data:
        :param v_guest_data:
        :param rest_shore:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        for count, guest in enumerate(guest_data):
            url = guest['rts']['security']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            # is_key_there_in_dict(response_get.content, 'securityPhotoURL')
            is_key_there_in_dict('photoCapturedPage', _content)
            is_key_there_in_dict('cameraButtonPage', _content)

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
            # if not rest_shore.send_request(method="GET", url=url).ok:
            #     raise Exception(f"Cannot Download Security Photo !!")

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844837'), pytestrail.param('USA', '186213')])
    def test_14_travel_document_update_check(self, config, test_data, guest_data, v_guest_data, rest_shore, country):
        """
        Test RTS check Guest travel documents
        :param config:
        :param test_data:
        :param guest_data:
        :param v_guest_data:
        :param rest_shore:
        :param country:
        :return:
        """
        # Update Guest Data, that is required for RTS. Make sure we save this for future use
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

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

            # Check if we are able to download the uploaded image
            # image = _content['finalPage']['imageURL']
            # if not rest_shore.send_request(method='GET', url=image).ok:
            #     raise Exception(f"Unable to Download Uploaded Image: {image} !!")

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
                    "travelDocumentsDetail": {
                        "countryOfResidenceCode": guest['visaCountryCode'],
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
                            "isDeleted": False,
                            "issueDate": "January 01 2022",
                            "issuedFor": "US"
                        }]
                    }
                }
                url = guest['rts']['travelDocuments']['detailsURLV1']
                _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content

                # Check if we are able to download the uploaded image
                # image = _content['finalPage']['imageURL']
                # if not rest_shore.send_request(method='GET', url=image).ok:
                #     raise Exception(f"Unable to Download Uploaded Image: {image} !!")

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
                            "addressTypeCode": "HOTEL"
                        },
                        "flightDetails": {
                            "idDeleted": True
                        },
                        "isStayingIn": True,
                        "residenceName": "Hyat",
                        "stayTypeCode": "HOTEL"
                    }
                }
                _content = rest_shore.send_request(method="PUT", url=url, json=body, auth='user').content

            is_key_there_in_dict('tasksCompletionPercentage', _content)
            _progress = _content['tasksCompletionPercentage']
            assert _progress['travelDocuments'] == 100, "travelDocuments is not 100% !!"
        
    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844838'), pytestrail.param('USA', '186215')])
    def test_15_pregnancy_update_check(self, rest_shore, guest_data, v_guest_data, test_data, country):
        """
        Test RTS Guest Pregnancy
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :param test_data:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        for count, guest in enumerate(guest_data):
            url = guest['rts']['pregnancy']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            is_key_there_in_dict('requiredFields', _content)
            is_key_there_in_dict('fitToTravelPage', _content)
            is_key_there_in_dict('notFitToTravelPage', _content)
            is_key_there_in_dict('unKnownResponsePage', _content)

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

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844839'), pytestrail.param('USA', '186216')])
    def test_16_voyage_contract_update_check(self, rest_shore, guest_data, v_guest_data, test_data, country):
        """
        Test RTS Guest Contracts
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :param test_data:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        for count, guest in enumerate(guest_data):
            url = guest['rts']['voyageContract']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            is_key_there_in_dict('buttons', _content)
            is_key_there_in_dict('contractStartPage', _content)
            is_key_there_in_dict('contractContent', _content)
            is_key_there_in_dict('dependentPage', _content)
            is_key_there_in_dict('contractDenyPage', _content)
            is_key_there_in_dict('contractDetails', _content)

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

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844840'), pytestrail.param('USA', '186217')])
    def test_17_emergency_contract_update_check(self, rest_shore, guest_data, v_guest_data, test_data, country):
        """
        Test RTS Guest emergency Contracts
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :param test_data:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        for count, guest in enumerate(guest_data):
            url = guest['rts']['emergencyContact']['detailsURL']
            _content = rest_shore.send_request(method="GET", url=url, auth="user").content
            is_key_there_in_dict('requiredFields', _content)
            is_key_there_in_dict('contactNamePage', _content)
            is_key_there_in_dict('relationshipPage', _content)
            is_key_there_in_dict('contactNumberPage', _content)
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

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844841'), pytestrail.param('USA', '186218')])
    def test_18_embarkation_slot_update_check(self, config, rest_shore, guest_data, v_guest_data, test_data, country):
        """
        Test RTS Guest Embarkation Slot
        :param config:
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param test_data:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        for count, guest in enumerate(guest_data):
            guest_data[count]['flightDetails'] = dict()
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/embarkationslot")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            guest_data[count]['isVIP'] = _content['isVip']
            is_key_there_in_dict('sailorServicesEmailId', _content)

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

    @retry_when_fails(retries=20, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844842'), pytestrail.param('USA', '186214')])
    def test_19_payment_update(self, config, test_data, rest_shore, guest_data, v_guest_data, country):
        """
        Test Guest Payment Method Update on RTS
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
            reservationNumber = 'reservationNumber'
            paymentDetails = 'paymentDetails'
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
            reservationNumber = 'v_reservationNumber'
            paymentDetails = 'v_paymentDetails'

        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/paymentmethod")
            method = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            is_key_there_in_dict('paymentModes', method)

            tx_id = generate_guid()
            body = {
                "clientTransactionId": tx_id,
                "signedFields": "clientTransactionId,currencyCode,clientReferenceNumber,transactionType,signedFields",
                "currencyCode": "USD",
                "clientReferenceNumber": test_data[reservationNumber],
                "transactionType": "create_payment_token",
                "amount": "0"
            }
            url = urljoin(config.shore.url, "rts-bff/signature")
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth='user').content
            is_key_there_in_dict('signedFields', _content)
            is_key_there_in_dict('signedTimeStamp', _content)
            is_key_there_in_dict('signature', _content)
            signed_fields = _content['signedFields']
            signed_time_stamp = _content['signedTimeStamp']
            signature = _content['signature']

            url = urljoin(config.shore.url, "payment-bff/initiatepayment")
            body = {
                "billToCountryCode": "USA",
                "lastName": test_data[signupGuest]['lastName'],
                "signedTimeStamp": signed_time_stamp,
                "signature": signature,
                "billToState": test_data[signupGuest]['addresses'][0]['stateCode'],
                "clientTransactionId": tx_id,
                "signedFields": signed_fields,
                "clientReferenceNumber": test_data[reservationNumber],
                "billToCity": test_data[signupGuest]['addresses'][0]['city'],
                "shipToCity": test_data[signupGuest]['addresses'][0]['city'],
                "billToZipCode": test_data[signupGuest]['addresses'][0]['zipCode'],
                "shipToLine2": test_data[signupGuest]['addresses'][0]['lineTwo'],
                "shipToLine1": test_data[signupGuest]['addresses'][0]['lineOne'],
                "requestData": "dummy",
                "shipToState": test_data[signupGuest]['addresses'][0]['stateCode'],
                "shipToLastName": test_data[signupGuest]['lastName'],
                "amount": "0",
                "billToLine2": test_data[signupGuest]['addresses'][0]['lineOne'],
                "shipToZipCode": test_data[signupGuest]['addresses'][0]['zipCode'],
                "billToLine1": test_data[signupGuest]['addresses'][0]['lineOne'],
                "shipToFirstName": test_data[signupGuest]['firstName'],
                "consumerId": guest['reservationGuestId'],
                "clientUserIP": "103.93.185.99",
                "transactionType": "create_payment_token",
                "firstName": test_data[signupGuest]['firstName'],
                "consumerType": "DXPReservationGuestId",
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
                    "holder_full_name": f"{test_data[signupGuest]['firstName']} {test_data[signupGuest]['lastName']}",
                    "card_expiry_month": "06",
                    "card_expiry_year": "2033",
                    "card_cvc": "123"
                },
                "payment_type": "ACCOUNT_STATUS",
                "origin": {},
                "bill_to_details": {
                    "first_name": test_data[signupGuest]['firstName'],
                    "last_name": test_data[signupGuest]['lastName'],
                    "street_1": "21",
                    "apartment_number": "213",
                    "city": test_data[signupGuest]['addresses'][0]['city'],
                    "stateId": "6557",
                    "postal_code": test_data[signupGuest]['addresses'][0]['zipCode'],
                    "country": test_data[signupGuest]['addresses'][0]['countryCode']
                },
                "ship_as_bill_details": "true",
                "ship_to_details": {
                    "first_name": test_data[signupGuest]['firstName'],
                    "last_name": test_data[signupGuest]['lastName'],
                    "street_1": "21",
                    "apartment_number": "213",
                    "city": test_data[signupGuest]['addresses'][0]['city'],
                    "postal_code": test_data[signupGuest]['addresses'][0]['zipCode'],
                    "country": test_data[signupGuest]['addresses'][0]['countryCode']
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
            test_data[paymentDetails] = _auth

            url = _initial['_links']['transactionUrl']['href']
            body = {
                "transactionId": _initial['transactionId'],
                "billToCountryCode": test_data[signupGuest]['addresses'][0]['countryCode'],
                "billToLine2": test_data[signupGuest]['addresses'][0]['lineOne'],
                "billToLine1": test_data[signupGuest]['addresses'][0]['lineOne'],
                "billToCity": test_data[signupGuest]['addresses'][0]['city'],
                "billToState": test_data[signupGuest]['addresses'][0]['stateCode'],
                "billToZipCode": test_data[signupGuest]['addresses'][0]['zipCode'],
                "cardUsername": f"{guest['firstName']} {guest['lastName']}",
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
                "shipToCountryCode": test_data[signupGuest]['addresses'][0]['countryCode'],
                "shipToLine2": test_data[signupGuest]['addresses'][0]['lineTwo'],
                "shipToLine1": test_data[signupGuest]['addresses'][0]['lineOne'],
                "shipToCity": test_data[signupGuest]['addresses'][0]['city'],
                "shipToState": test_data[signupGuest]['addresses'][0]['stateCode'],
                "shipToZipCode": test_data[signupGuest]['addresses'][0]['zipCode'],
                "paymentMode": 'CARD',
                "status": _auth['status'],
                "statusCode": _auth['status_code'],
                "utcOffset": -330
            }
            _transaction = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            url = urljoin(config.shore.url, "rts-bff/paymentmethod")
            guest['payment_method'] = method['paymentModes'][0]
            body = {
                "selectedPaymentMethodCode": method['paymentModes'][0], "partyMembers": [], "isDeleted": False,
                "cardPaymentToken": test_data[paymentDetails]['payment_token']
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, params=params, auth='user').content

            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)

            _progress = _content['tasksCompletionPercentage']
            is_key_there_in_dict('paymentMethod', _progress)
            assert _progress['paymentMethod'] == 100, f"paymentMethod is not 100% !!"

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44844843'), pytestrail.param('USA', '186257')])
    def test_20_check_health_status_after_rts(self, config, test_data, rest_shore, guest_data, v_guest_data, country):
        """
        Test Guest Status After RTS
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            test_data['countries'][0] = 'US'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
            reservationNumber = 'reservationNumber'
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            test_data['countries'][0] = 'IN'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
            reservationNumber = 'v_reservationNumber'

        for count, guest in enumerate(guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-number": test_data[reservationNumber]
            }
            url = urljoin(config.shore.url, "rts-bff/landing")
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            tasks = _content['tasksCompletionPercentage']
            for task in tasks:
                if task == 'pregnancy' and guest['genderCode'][0] != "F":
                    continue
                assert tasks[task] == 100, f"{task} is not 100% after performing RTS"

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '25210171'), pytestrail.param('USA', '12150719')])
    def test_21_validate_security_photo(self, config, guest_data, test_data, v_guest_data, rest_shore, country):
        """
        validate security photo
        :param test_data:
        :param guest_data:
        :param config:
        :param rest_shore:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            signupGuest = 'signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            signupGuest = 'v_signupGuest'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        url = url = urljoin(config.shore.url, "rts-bff/photo/security/validate")
        for count, guest in enumerate(guest_data):
            with open(guest['security_photo'], "rb") as img:
                img_str = base64.b64encode(img.read()).decode("utf-8")
            body = {
                "photoContent": img_str
            }
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
            is_key_there_in_dict('isValidPhoto', _content)
            break

    @pytestrail.case(15312384)
    def test_22_get_health_check_question(self, config, test_data, rest_shore):
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
        is_key_there_in_dict('landingPage', _content)
        is_key_there_in_dict('healthCheckRefusePage', _content)
        is_key_there_in_dict('healthCheckReviewPage', _content)

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(9002000)
    def test_23_update_health_check_question(self, config, test_data, rest_shore, guest_data):
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

            # Todo this after get the complete requirement but for now we need to push above code to check the Health check question in ACI and MOCI
            # assert _content['isHealthCheckComplete'] is False, "isHealthCheckComplete is False !!"
            # assert _content['isFitToTravel'] is False, "isFitToTravel is False !!"

            # params = {
            #     "reservation-guest-id": guest['reservationGuestId'],
            # }
            # url = urljoin(config.shore.url, "dxpcore/checkin/guest/detail-info")
            # _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            #
            # for status in _content['_embedded']['eCheckinGuestDetailsList']:
            #     if status['reservationGuestId'] == guest['reservationGuestId']:
            #         assert status['healthInfo']['isFitToTravel'], "isFitToTravel is not correct in dxpcore service"
            #     else :
            #         raise Exception (f"{guest['reservationGuestId']} is not matching")

    @pytestrail.case(23748121)
    def test_24_update_personal_info(self, config, rest_shore, guest_data):
        """
        Verify the update personal info
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        body = {
            "firstName": guest['FirstName'],
            "lastName": guest['LastName'],
            "middleName": "",
            "birthDate": guest['BirthDate'],
            "genderCode": guest['GenderCode'][0],
            "preferredName": "prename"
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/personal")
        _content = rest_shore.send_request(method="PUT", url=_url, json=body, auth="user").content

        _content = rest_shore.send_request(method="GET", url=_url, auth="user").content
        is_key_there_in_dict('firstName', _content)
        is_key_there_in_dict('lastName', _content)
        is_key_there_in_dict('preferredName', _content)
        assert _content['firstName'] == guest['FirstName'], "First Name is not matching !!"
        assert _content['lastName'] == guest['LastName'], "Last Name is not matching !!"
        assert _content['preferredName'] == "prename", "preferred Name is not matching !!"

    @pytestrail.case(12150723)
    def test_25_emergency_contact_in_setting(self, config, test_data, rest_shore, guest_data):
        """
        Verification of emergency contact in Setting
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        time.sleep(60)
        params = {
            "reservation-guest-id": test_data['signupGuest']['reservationGuestId'],
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/emergencycontact")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content

        is_key_there_in_dict('requiredFields', _content)
        is_key_there_in_dict('readOnlyFields', _content)
        is_key_there_in_dict('hiddenFields', _content)
        is_key_there_in_dict('pageDetails', _content)
        is_key_there_in_dict('emergencyContactDetails', _content)

        assert _content['header'] == "Emergency contact", "Header is not matching !!"
        for guest in guest_data:
            if guest['reservationGuestId'] == test_data['signupGuest']['reservationGuestId']:
                assert _content['emergencyContactDetails']['name'] == guest['emergencyContactDetails'][
                    'name'], "Name is not matching !!"
                assert _content['emergencyContactDetails']['relationship'] == guest['emergencyContactDetails'][
                    'relationship'], "relationship is not matching !!"
                assert _content['emergencyContactDetails']['dialingCountryCode'] == guest['emergencyContactDetails'][
                    'dialingCountryCode'], "dialingCountryCode is not matching !!"
                assert _content['emergencyContactDetails']['phoneNumber'] == guest['emergencyContactDetails'][
                    'phoneNumber'], "phoneNumber is not matching !!"
                return
        else:
            raise Exception("Emergency Contact is not Matching or Update in Setting")

    @pytestrail.case(31700025)
    def test_26_verify_emergency_contact_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the emergency contact updated in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(config.shore.ota, 'OTA_ReadRQ')
        xml = xml_data.read_rq_seaware.format(test_data['reservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/xml'})
        try:
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('vx:OTA_ResRetrieveRS', _content_json)
            is_key_there_in_dict('vx:ReservationsList', _content_json['vx:OTA_ResRetrieveRS'])
            is_key_there_in_dict('vx:CruiseReservation', _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList'])
            _cruise = _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation']
            is_key_there_in_dict('vx:ReservationInfo', _cruise)
            is_key_there_in_dict('vx:GuestDetails', _cruise['vx:ReservationInfo'])
            is_key_there_in_dict('vx:GuestDetail', _cruise['vx:ReservationInfo']['vx:GuestDetails'])
            assert len(_cruise['vx:ReservationInfo']['vx:GuestDetails'][
                           'vx:GuestDetail']) == 2, 'Guest Count is not matching in seaware !!'
            _guest_detail = _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation'][
                'vx:ReservationInfo']['vx:GuestDetails']['vx:GuestDetail']
            for _guest in range(0, len(_guest_detail)):
                if '@ContactType' not in _guest_detail[_guest]['vx:ContactInfo']:
                    pytest.skip("@ContactType is not available in vx:ContactInfo")
                assert _guest_detail[_guest]['vx:ContactInfo'][
                           '@ContactType'] == 'REGULAR', 'Emergency contact update did not get synced to Seaware !!'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(8943152)
    def test_27_update_contact_info(self, config, test_data, rest_shore):
        """
        Update Guest Contact info
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.guestbff'), "/voyage-account-settings/user/contact")
        for address in test_data['signupGuest']['addresses']:
            address['lineOne'] = "Baker Street"
            address['lineTwo'] = "345"
            address['city'] = "Orlando"
            address['stateCode'] = "FL"
            address['countryCode'] = "US"
            address['zipCode'] = "30987"
            body = {
                "addresses": [{
                    "countryCode": address['countryCode'],
                    "city": address['city'],
                    "line1": address['lineOne'],
                    "line2": address['lineTwo'],
                    "zip": address['zipCode'],
                    "stateCode": address['stateCode']
                }]
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, auth="user").content

            _content = rest_shore.send_request(method="GET", url=url, json=body, auth="user").content
            for addresses in _content['addresses']:
                assert address['countryCode'] == addresses['countryCode'], "ERROR: countryCode not matching !!"
                assert address['city'] == addresses['city'], "ERROR: city not matching !!"
                assert address['lineOne'] == addresses['line1'], "ERROR: lineOne not matching !!"
                assert address['lineTwo'] == addresses['line2'], "ERROR: lineTwo not matching !!"
                assert address['zipCode'] == addresses['zip'], "ERROR: zipCode not matching !!"
                assert address['stateCode'] == addresses['stateCode'], "ERROR: stateCode not matching !!"

    @pytestrail.case(26974574)
    def test_28_get_id_type(self, config, test_data, rest_shore):
        """
        Get id types from dxpcore
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/idtypes")
        params = {
            'size': '200'
        }
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth='user').content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('idtypes', _content['_embedded'])
        if len(_content['_embedded']['idtypes']) == 0:
            raise Exception('There are no idTypes available !!')
        for _type in _content['_embedded']['idtypes']:
            if _type['name'] == 'VXP - Guest':
                test_data['idtypeId'] = _type['idtypeId']
                break
        else:
            raise Exception('Id type for Guest is not found !!')

    @pytestrail.case(26974575)
    def test_29_get_reference_sailor_api(self, config, test_data, rest_shore, guest_data):
        """
        Get references from sailor API
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(config.shore.url, "xref-api/v1/references/search/findByType")
        body = {
            "nativeSourceIDValue": guest['guestId'],
            "referenceTypeID": test_data['idtypeId']
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth='user').content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('references', _content['_embedded'])
        if len(_content['_embedded']['references']) == 0:
            raise Exception('There are no references available !!')
        for _refer in _content['_embedded']['references']:
            if _refer['referenceType'] == 'Person':
                test_data['nativeSourceIDValue'] = _refer['nativeSourceIDValue']
                break
        else:
            raise Exception('nativeSourceIDValue for Guest is not found !!')

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(26975646)
    def test_30_check_sailor_salesforce(self, config, test_data, rest_shore, guest_data):
        """
        Check Sailor details in Salesforce
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(config.shore.url, f"sailor-api/v1/sailors/{test_data['nativeSourceIDValue']}")
        _content = rest_shore.send_request(method="GET", url=url, auth='user').content
        is_key_there_in_dict('addressLine1', _content)
        is_key_there_in_dict('city', _content)
        is_key_there_in_dict('postalCode', _content)
        for _guest in guest_data:
            for _address in _guest['Addresses']:
                assert _address['lineOne'] == _content['addressLine1'], 'Line One mismatch !!'
                assert _address['city'] == _content['city'], 'city mismatch !!'
                assert _address['zipCode'] == _content['postalCode'], 'Line One mismatch !!'
                return

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(25013508)
    def test_31_check_guest_details_updated_seaware(self, config, rest_shore, test_data, guest_data, xml_data):
        """
        Check the updated address in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :param xml_data:
        :return:
        """
        try:
            url = urljoin(config.shore.ota, 'OTA_ReadRQ')
            xml = xml_data.read_rq_seaware.format(test_data['reservationNumber'])
            rest_shore.session.headers.update({'Content-Type': 'application/xml'})
            _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
            _content_json = xmltodict.parse(_content)
            is_key_there_in_dict('vx:OTA_ResRetrieveRS', _content_json)
            is_key_there_in_dict('vx:ReservationsList', _content_json['vx:OTA_ResRetrieveRS'])
            is_key_there_in_dict('vx:CruiseReservation', _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList'])
            _cruise = _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation']
            is_key_there_in_dict('vx:ReservationInfo', _cruise)
            is_key_there_in_dict('vx:GuestDetails', _cruise['vx:ReservationInfo'])
            is_key_there_in_dict('vx:GuestDetail', _cruise['vx:ReservationInfo']['vx:GuestDetails'])
            assert len(_cruise['vx:ReservationInfo']['vx:GuestDetails'][
                           'vx:GuestDetail']) == 2, 'Guest Count is not matching in seaware !!'
            _guest_detail = _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation'][
                'vx:ReservationInfo']['vx:GuestDetails']['vx:GuestDetail']
            for _guest in range(0, len(_guest_detail)):
                if 'vx:Address' in _guest_detail[_guest]['vx:ContactInfo']:
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address']['vx:AddressLine'][_guest] == \
                           guest_data[_guest]['Addresses'][_guest]['lineOne'], 'Address LineOne Mismatch !!'
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address']['vx:CityName'] == \
                           guest_data[_guest]['Addresses'][_guest]['city'], 'City Mismatch !!'
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address']['vx:PostalCode'] == \
                           guest_data[_guest]['Addresses'][_guest]['zipCode'], 'zipCode Mismatch !!'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(26258538)
    def test_32_check_address_update_shore_core(self, config, rest_shore, guest_data):
        """
        Check address update in shore core
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'guests', guest['guestId'])
            _content_shore = rest_shore.send_request(method="GET", url=url, auth="admin").content
            if len(_content_shore['addresses']) == 0:
                raise Exception("Address of guest did not get sync to shore core")
            for _address in _content_shore['addresses']:
                assert _address['line1'] == guest['Addresses'][0]['lineOne'], "Guest Address Line1 Mismatch !!"
                assert _address['line2'] == guest['Addresses'][0]['lineTwo'], "Guest Address Line2 Mismatch !!"
                assert _address['state'] == guest['Addresses'][0]['stateCode'], "Guest State Mismatch !!"
                assert _address['countryCode'] == guest['Addresses'][0][
                    'countryCode'], "Guest country Code Mismatch !!"
            break

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(26261948)
    def test_33_check_address_update_ship_core(self, config, rest_shore, guest_data):
        """
        Check address update in ship core
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'guests', guest['guestId'])
            _content_ship = rest_shore.send_request(method="GET", url=url, auth="bearer").content
            if len(_content_ship['addresses']) == 0:
                raise Exception("Address of guest did not get sync to ship core")
            for _address in _content_ship['addresses']:
                assert _address['line1'] == guest['Addresses'][0]['lineOne'], "Guest Address Line1 Mismatch !!"
                assert _address['line2'] == guest['Addresses'][0]['lineTwo'], "Guest Address Line2 Mismatch !!"
                assert _address['state'] == guest['Addresses'][0]['stateCode'], "Guest State Mismatch !!"
                assert _address['countryCode'] == guest['Addresses'][0][
                    'countryCode'], "Guest country Code Mismatch !!"
            break

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(186244)
    def test_34_validate_guest_personal_information_in_ship_couch(self, config, rest_ship, guest_data):
        """
        Check Guest Personal data in Ship Couch has synced or not
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestPersonalInformation::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
            if len(_content['Addresses']) == 0:
                raise Exception('Address did not get Synced to Ship couch !!')
            for address in _content['Addresses']:
                assert address['Line1'] == guest['Addresses'][0]['lineOne'], "Guest Address Line1 Mismatch !!"
                assert address['Line2'] == guest['Addresses'][0]['lineTwo'], "Guest Address Line2 Mismatch !!"
                assert address['State'] == guest['Addresses'][0]['stateCode'], "Guest State Mismatch !!"
                assert address['CountryCode'] == guest['Addresses'][0]['countryCode'], "Guest country Code Mismatch !!"
            assert _content['Stateroom'] == guest['stateroom'], "Guest Cabin Number Mismatch !! "
            break

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(5313659)
    def test_35_validate_guest_payment_information_in_ship_couch(self, config, rest_ship, guest_data):
        """
        Check Guest Payment data in Ship Couch has synced or not
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestPayForDetail::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
            is_key_there_in_dict('PaymentMethodDetail', _content)
            is_key_there_in_dict('PaymentMode', _content)
            is_key_there_in_dict('PaymentModeID', _content)
            is_key_there_in_dict('ReservationGuestID', _content)
            assert _content['PaymentMode'] == 'Credit Card', "Payment Mode Mismatch !!"
            assert _content['ReservationGuestID'] == _res_id, "Reservation Guest Id Mismatch !!"
            is_key_there_in_dict('CVV', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardExpiryDate', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardExpiryDateEpoch', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardExpiryMonth', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardExpiryYear', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardNumber', _content['PaymentMethodDetail'])
            is_key_there_in_dict('CreditCardType', _content['PaymentMethodDetail'])
            is_key_there_in_dict('NameOnCreditCard', _content['PaymentMethodDetail'])
            is_key_there_in_dict('ZipCode', _content['PaymentMethodDetail'])
            assert _content['PaymentMethodDetail']['CreditCardExpiryDate'] == '2033-06-01', "Card Expiry Date Mismatch!"
            assert _content['PaymentMethodDetail']['CreditCardExpiryMonth'] == '06', "Card Expiry Month Mismatch!"
            assert _content['PaymentMethodDetail']['CreditCardExpiryYear'] == '33', "Card Expiry Year Mismatch!"
            assert _content['PaymentMethodDetail']['CreditCardType'] == 'visa', "Card Type Mismatch!"
            assert _content['PaymentMethodDetail']['ZipCode'] == '33012', "Zip Code Mismatch!"
            assert _content['PaymentMethodDetail'][
                       'NameOnCreditCard'] == f"{guest['FirstName']} {guest['LastName']}", "Name on Card Mismatch!"

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(28237964)
    def test_36_check_rts_completed_status(self, config, rest_ship, guest_data):
        """
        Check guest rts completed status in ship core
        :param config:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'personstatuses/search/findbypersonids')
            json = {
                "personTypeCode": "RG",
                "personIds": [
                    _res_id
                ]
            }
            _content = rest_ship.send_request(method="POST", url=_url, json=json, auth="bearer").content
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('personStatuses', _content['_embedded'])
            assert len(_content['_embedded']['personStatuses']) != 0, 'There is no person status for the guest !!'
            for _status in _content['_embedded']['personStatuses']:
                if _status['statusTypeCode'] == 'OC':
                    assert _status['status'] == 'COMPLETED', 'RTS did not get COMPLETED for the guest !!'
                    break
            else:
                raise Exception('There is no person status for RTS !!')

            _url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
            is_key_there_in_dict('IsOnlineCheckedIn', _content)
            assert _content['IsOnlineCheckedIn'] == True, 'Guest is not RTS Completed in Ship Couch !!'
