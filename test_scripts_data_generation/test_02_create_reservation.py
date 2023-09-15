__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.RESERVATION
@pytest.mark.run(order=2)
class TestReservation:
    """
    Test Suite to Make Reservation
    """

    @pytestrail.case(132)
    def test_01_sign_up(self, config, test_data, rest_shore, guest_data):
        """
        Register a User
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        # Required for Kubernetes Logs Fetching
        test_data['start_time'] = int(time.time())

        # Save Guest we are signing up and use this one for all E2E
        test_data['signupGuest'] = dict()
        test_data['signupGuest']['addresses'] = guest_data[0]['Addresses']
        test_data['signupGuest']['password'] = 'Voyages@9876'
        test_data['signupGuest']['appId'] = str(generate_guid()).upper()
        test_data['signupGuest']['userType'] = 'guest'
        test_data['signupGuest']['enableEmailNewsOffer'] = False
        test_data['signupGuest']['deviceId'] = str(generate_random_alpha_numeric_string(length=32)).lower()
        url = urljoin(config.shore.url, "user-account-service/signup")
        body = {
            "birthDate": guest_data[0]['BirthDate'],
            "email": guest_data[0]['Email'],
            "firstName": guest_data[0]['FirstName'],
            "userType": test_data['signupGuest']['userType'],
            "preferredName": guest_data[0]['FirstName'],
            "lastName": guest_data[0]['LastName'],
            "password": test_data['signupGuest']['password'],
            "enableEmailNewsOffer": test_data['signupGuest']['enableEmailNewsOffer']
        }
        test_data['signupGuest'].update(body)
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('authenticationDetails', _content)
        token = _content['authenticationDetails']
        is_key_there_in_dict('accessToken', token)
        is_key_there_in_dict('tokenType', token)
        test_data['signupGuest']['accessToken'] = f"{token['tokenType']} {token['accessToken']}"
        rest_shore.userToken = test_data['signupGuest']['accessToken']
        test_data['userToken'] = rest_shore.userToken

    @pytestrail.case(760022)
    def test_02_setup_active_voyage(self, config, test_data, rest_shore):
        """
        Get/Set Ship's Active Voyage
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        if config.startDate is None:
            start_date = datetime.now(tz=pytz.utc).date()
        else:
            date_use = config.startDate
            start_date = datetime.strptime(date_use, "%Y-%m-%d") - timedelta(days=1)
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
        test_data['voyages'] = sorted(_content['sailings'], key=lambda i: i['startDate'])
        voyages = sorted(_content['sailings'], key=lambda i: i['startDate'])
        if len(voyages) == 0:
            raise Exception("Zero Voyages Returned !!")
        if config.startDate is None:
            for _voyage in voyages:
                if _voyage['startDate'] > str(start_date):
                    if _voyage['ship']['name'] != 'Valiant Lady' and _voyage['ship']['name'] != 'Resilient Lady':
                        test_data['voyage'] = _voyage
                        break
            if len(test_data['voyage']) == 0:
                raise Exception("Scarlet lady voyayes are not available !!")
        else:
            test_data['voyage'] = voyages[0]

    @pytestrail.case(129)
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
            "voyageId": test_data['voyage']['id'],
            "searchQualifier": {
                "sailingDateRange": [{
                    "start": test_data['voyage']['startDate'],
                    "end": test_data['voyage']['endDate']}],
                "cabins": [
                    {
                        "guestCounts": [
                            {
                                "ageCategory": "Adult", "count": test_data['guests']
                            }
                        ]
                    }
                ], "priceRange": {
                    "currencyCode": "USD"
                }
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
                    test_data['cabin'] = category
                    return
        else:
            raise Exception(f"Cannot Find Cabin with {test_data['guests']} Guests !!")

    @pytestrail.case(26111504)
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
            "voyageId": test_data['voyage']['id'],
            "cabins": [{
                "categoryCode": test_data['cabin']['categoryCode'],
                "guestCounts": [{"count": test_data['guests']}]
            }]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if 'cabinOptions' not in _content and len(_content['cabinOptions']) == 0:
            raise Exception(f"No Cabins Returned !!")

        # Choose a Random Cabin
        test_data['cabin'].update(random.choice(_content['cabinOptions']))

    @pytestrail.case(26111505)
    def test_05_get_vip_status(self, config, test_data, rest_shore):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {"cabinMetaCode": test_data['cabin']['genericCategoryCode']}
        url = urljoin(config.shore.url, f"bookvoyage-bff/cabins/{test_data['cabin']['categoryCode']}/details")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('vip', _content)
        test_data['cabin']['vip'] = _content["vip"]

    @pytestrail.case(381551)
    def test_06_hold_cabin(self, config, test_data, rest_shore):
        """
        Hold the cabin
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        voyage_id = test_data['voyage']['id']
        url = urljoin(config.shore.url, "bookvoyage-bff/cabin/hold")
        body = {
            "voyageId": voyage_id,
            "currencyCode": "USD",
            "cabinDetails": [{
                "cabinCategoryCode": test_data['cabin']["categoryCode"],
                "cabinNumber": test_data['cabin']['cabinNumber'],
                "maxOccupancy": test_data['guests']
            }]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        for cabin in _content:
            is_key_there_in_dict('cabinNumber', cabin)
            is_key_there_in_dict('dueDateTime', cabin)
            if cabin['cabinNumber'] == test_data['cabin']['cabinNumber']:
                break
        else:
            raise Exception(f"Failed to Hold the Cabin # {test_data['cabin']['cabinNumber']}")

    @pytestrail.case(121)
    def test_07_reservation(self, config, request, test_data, rest_shore, guest_data):
        """
        Perform Reservation
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        user_data = []
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/reservation_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)

        for count, guest in enumerate(guest_data):
            user_data.append({
                "guestRefNumber": str(count + 1),
                "givenName": guest['FirstName'],
                "lastName": guest['LastName'],
                "gender": guest['GenderCode'][0],
                "dateOfBirth": guest['BirthDate'],
                "citizenShip": guest['CitizenshipCountryCode'],
                "email": guest['Email'],
                "contactNumber": guest['Phones'][0]['number'],
                "mobileCountryCode": "91"
            })

        url = urljoin(config.shore.url, "bookvoyage-bff/booknow")
        body = {
            "voyageId": test_data['voyage']['id'],
            "shipCode": config.ship.code,
            "cabins": [{
                "accessKeys": [],
                "promoCode": [],
                "guestCount": test_data['guests'],
                "cabinNumber": test_data["cabin"]['cabinNumber'],
                "cabinCategoryCode": test_data["cabin"]['categoryCode'],
                "sailors": user_data
            }],
            "currencyCode": "USD"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content[0]
        is_key_there_in_dict('reservationNumber', _content)
        is_key_there_in_dict('voyageId', _content)
        is_key_there_in_dict('paymentDetails', _content)
        amount_due = _content['paymentDetails'][0]['dueAmount']
        test_data['reservationNumber'] = _content['reservationNumber']
        if test_data['voyage']['id'] != _content['voyageId']:
            raise Exception(f"Voyage ID ${_content['voyageId']} Mismatch !!")

        guest_id_data = wait_for_guest_id(config, rest_shore, guest_data, _content)
        res_id_data = wait_for_reservation_guest_id(config, rest_shore, guest_id_data)

        for count, guest in enumerate(guest_data):
            for res_id in res_id_data:
                if res_id['email'] == guest['Email']:
                    guest_data[count].update(res_id)
                if res_id['Email'] == test_data['signupGuest']['email']:
                    test_data['signupGuest']['guestId'] = res_id['guestId']
                    test_data['signupGuest']['reservationId'] = res_id['reservationId']
                    test_data['signupGuest']['reservationGuestId'] = res_id['reservationGuestId']

        # Get Different Moci and Doc Rejected Guests, they should not be same (applicable for > 2 Guests)
        test_data['mociRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
        test_data['docRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
        while test_data['mociRejected'] == test_data['docRejected'] and test_data['guests'] > 2:
            test_data['mociRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
            test_data['docRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])

        tx_id = generate_guid()
        # Do retries for bookvoyage-bff/signature Call
        time.sleep(5)
        _content = wait_for_signature(config, rest_shore, amount_due, test_data['reservationNumber'], tx_id)
        is_key_there_in_dict('signedFields', _content)
        is_key_there_in_dict('signedTimeStamp', _content)
        is_key_there_in_dict('signature', _content)
        signed_fields = _content['signedFields']
        signed_time_stamp = _content['signedTimeStamp']
        signature = _content['signature']

        tx = payment_virgin(config, test_data, guest_data, rest_shore, amount_due, signature, signed_time_stamp, tx_id,
                            signed_fields, client_ref_num=test_data['reservationNumber'])
        url = urljoin(config.shore.url, "bookvoyage-bff/reservation/pay")
        body = {
            "responseSignature": tx,
            "reservationNumber": test_data['reservationNumber'],
            "paymentInfo": {
                "paymentMode": "card",
                "paymentMethod": [{
                    "expiryDate": "06",
                    "cardHolderName": f"{test_data['signupGuest']['firstName']} "
                                      f"{test_data['signupGuest']['lastName']}",
                    "cardType": "001",
                    "billingAddress": {
                        "zipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
                        "lineTwo": test_data['signupGuest']['addresses'][0]['lineTwo'],
                        "city": test_data['signupGuest']['addresses'][0]['city'],
                        "countryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
                        "lineOne": test_data['signupGuest']['addresses'][0]['lineOne'],
                        "state": test_data['signupGuest']['addresses'][0]['stateCode'],
                    }
                }],
                "currencyCode": "USD",
                "paidAmount": int(amount_due)
            }
        }

        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if _content['paymentDetail']['paidAmount'] != amount_due:
            raise Exception("Amount not completely paid after doing reservation !!")

    @pytestrail.case(26113960)
    def test_08_upload_photo(self, config, rest_shore, guest_data, test_data):
        """
        Upload Security Photo for each guest
        :param config:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            first_name = guest['firstName']
            last_name = guest['lastName']
            email_id = guest['email']
            birth_date = guest['birthDate']
            gender = guest['GenderCode'][0]
            security_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                           birth_date=birth_date, gender=gender).add_text()
            logger.debug(f"Uploading Security Photo #{count + 1} ...")
            security_photo_url = upload_media_file(config, rest_shore, security_photo)
            time.sleep(0.1)
            guest_data[count]['SecurityPhotoUrl'] = security_photo_url

            url = urljoin(config.shore.url, "rts-bff/security")
            params = {
                'reservation-guest-id': guest['reservationGuestId']
            }
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            is_key_there_in_dict('photoCapturedPage', _content)
            is_key_there_in_dict('cameraButtonPage', _content)
            body = {
                "securityPhotoURL": guest['SecurityPhotoUrl'],
                "isDeleted": False
            }
            _content = rest_shore.send_request(method="PUT", url=url, json=body, params=params, auth='user').content
            is_key_there_in_dict('tasksCompletionPercentage', _content)
            is_key_there_in_dict('finalPage', _content)
            assert _content['tasksCompletionPercentage']['security'] == 100, \
                f"Failed to upload security photo for {guest['FirstName']} {guest['LastName']} guest !!"

