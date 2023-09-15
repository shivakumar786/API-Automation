__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.SHORE
@pytest.mark.RESERVATION
@pytest.mark.run(order=3)
class TestReservation:
    """
    Test Suite to Make Reservation
    """

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44792459'), pytestrail.param('USA', '132')])
    def test_01_sign_up(self, config, test_data, rest_shore, guest_data, v_guest_data, country):
        """
        Register a User
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param v_guest_data:
        :param country:
        :return:
        """
        # Required for Kubernetes Logs Fetching
        if country == 'USA':
            signupGuest = 'signupGuest'
            userToken = 'userToken'
            body = {
                "email": guest_data[0]['Email'],
                "firstName": guest_data[0]['FirstName'],
                "lastName": guest_data[0]['LastName'],
                "birthDate": guest_data[0]['BirthDate'],
                "preferredName": guest_data[0]['FirstName'],
            }
        else:
            signupGuest = 'v_signupGuest'
            userToken = 'v_userToken'
            body = {
                "birthDate": v_guest_data[0]['BirthDate'],
                "email": v_guest_data[0]['Email'],
                "firstName": v_guest_data[0]['FirstName'],
                "lastName": v_guest_data[0]['LastName'],
                "preferredName": v_guest_data[0]['FirstName'],
            }

        test_data['start_time'] = int(time.time())

        # Save Guest we are signing up and use this one for all E2E
        test_data[signupGuest] = dict()
        test_data[signupGuest]['addresses'] = guest_data[0]['Addresses']
        test_data[signupGuest]['password'] = 'Voyages@9876'
        test_data[signupGuest]['oldPassword'] = test_data[signupGuest]['password']
        test_data[signupGuest]['appId'] = str(generate_guid()).upper()
        test_data[signupGuest]['userType'] = 'guest'
        test_data[signupGuest]['enableEmailNewsOffer'] = False
        test_data[signupGuest]['deviceId'] = str(generate_random_alpha_numeric_string(length=32)).lower()
        url = urljoin(config.shore.url, "user-account-service/signup")
        body.update({
            "password": test_data[signupGuest]['password'],
            "userType": test_data[signupGuest]['userType'],
            "enableEmailNewsOffer": test_data[signupGuest]['enableEmailNewsOffer']
        })
        test_data[signupGuest].update(body)
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('authenticationDetails', _content)
        token = _content['authenticationDetails']
        is_key_there_in_dict('accessToken', token)
        is_key_there_in_dict('tokenType', token)
        test_data[signupGuest]['accessToken'] = f"{token['tokenType']} {token['accessToken']}"
        rest_shore.userToken = test_data[signupGuest]['accessToken']
        test_data[userToken] = rest_shore.userToken

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
        test_data['voyages'] = sorted(_content['sailings'], key=lambda i: i['startDate'])
        voyages = sorted(_content['sailings'], key=lambda i: i['startDate'])
        if len(voyages) == 0:
            raise Exception("Zero Voyages Returned !!")
        for _voyage in voyages:
            if _voyage['startDate'] > str(start_date):
                if _voyage['ship']['name'] != 'Valiant Lady' and _voyage['ship']['name'] != 'Resilient Lady':
                    test_data['voyage'] = _voyage
                    break
        if len(test_data['voyage']) == 0:
            raise Exception("Scarlet lady voyayes are not available !!")

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44792460'), pytestrail.param('USA', '129')])
    def test_03_get_cabin_category(self, config, test_data, rest_shore, country):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :param country:
        :return:
        """
        if country == 'USA':
            cabin = 'cabin'
        else:
            cabin = 'v_cabin'

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

        for cabinn in cabins:
            for category in cabinn['categoryOptions']:
                if category['maxOccupancy'] >= test_data['guests']:
                    is_key_there_in_dict('categoryCode', category)
                    is_key_there_in_dict('genericCategoryCode', category)
                    test_data[cabin] = category
                    return
        else:
            raise Exception(f"Cannot Find Cabin with {test_data['guests']} Guests !!")

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44841427'), pytestrail.param('USA', '26111504')])
    def test_04_cabin_search(self, config, test_data, rest_shore, country):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :param country:
        :return:
        """
        if country == 'USA':
            cabin = 'cabin'
        else:
            cabin = 'v_cabin'
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'cabins/search')
        body = {
            "voyageId": test_data['voyage']['id'],
            "cabins": [{
                "categoryCode": test_data[cabin]['categoryCode'],
                "guestCounts": [{"count": test_data['guests']}]
            }]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if 'cabinOptions' not in _content and len(_content['cabinOptions']) == 0:
            raise Exception(f"No Cabins Returned !!")

        # Choose a Random Cabin
        test_data[cabin].update(random.choice(_content['cabinOptions']))

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44841428'), pytestrail.param('USA', '26111505')])
    def test_05_get_vip_status(self, config, test_data, rest_shore, country):
        """
        Get Cabin Categories
        :param config:
        :param test_data:
        :param rest_shore:
        :param country:
        :return:
        """
        if country == 'USA':
            cabin = 'cabin'
        else:
            cabin = 'v_cabin'

        params = {"cabinMetaCode": test_data[cabin]['genericCategoryCode']}
        url = urljoin(config.shore.url, f"bookvoyage-bff/cabins/{test_data[cabin]['categoryCode']}/details")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('vip', _content)
        test_data[cabin]['vip'] = _content["vip"]

    @retry_when_fails(retries=10, interval=5)
    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44841429'), pytestrail.param('USA', '381551')])
    def test_06_hold_cabin(self, config, test_data, rest_shore, country):
        """
        Hold the cabin
        :param config:
        :param test_data:
        :param rest_shore:
        :param country:
        :return:
        """
        if country == 'USA':
            cabin = 'cabin'
        else:
            cabin = 'v_cabin'

        voyage_id = test_data['voyage']['id']
        url = urljoin(config.shore.url, "bookvoyage-bff/cabin/hold")
        body = {
            "voyageId": voyage_id,
            "currencyCode": "USD",
            "cabinDetails": [{
                "cabinCategoryCode": test_data[cabin]["categoryCode"],
                "cabinNumber": test_data[cabin]['cabinNumber'],
                "maxOccupancy": test_data['guests']
            }]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        for cabins in _content:
            is_key_there_in_dict('cabinNumber', cabins)
            is_key_there_in_dict('dueDateTime', cabins)
            if cabins['cabinNumber'] == test_data[cabin]['cabinNumber']:
                break
        else:
            raise Exception(f"Failed to Hold the Cabin # {test_data['cabin']['cabinNumber']}")

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44841430'), pytestrail.param('USA', '121')])
    def test_07_reservation(self, config, request, test_data, rest_shore, guest_data, v_guest_data, country):
        """
        Perform Reservation
        :param config:
        :param request:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param country:
        :param v_guest_data:
        :return:
        """
        if country == 'USA':
            guest_data = guest_data
            cabin = 'cabin'
            signupGuest = 'signupGuest'
            reservationNumber = 'reservationNumber'
            rest_shore.userToken = test_data[signupGuest]['accessToken']
        else:
            guest_data = v_guest_data
            cabin = 'v_cabin'
            signupGuest = 'v_signupGuest'
            reservationNumber = 'v_reservationNumber'
            rest_shore.userToken = test_data[signupGuest]['accessToken']

        user_data = []
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/reservation_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)

        for count, guest in enumerate(guest_data):
            user_data.append({
                "guestRefNumber": str(count+1),
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
                "cabinNumber": test_data[cabin]['cabinNumber'],
                "cabinCategoryCode": test_data[cabin]['categoryCode'],
                "sailors": user_data
            }],
            "currencyCode": "USD"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content[0]
        is_key_there_in_dict('reservationNumber', _content)
        is_key_there_in_dict('voyageId', _content)
        is_key_there_in_dict('paymentDetails', _content)
        amount_due = _content['paymentDetails'][0]['dueAmount']
        test_data[reservationNumber] = _content['reservationNumber']
        if test_data['voyage']['id'] != _content['voyageId']:
            raise Exception(f"Voyage ID ${_content['voyageId']} Mismatch !!")

        guest_id_data = wait_for_guest_id(config, rest_shore, guest_data, _content)
        res_id_data = wait_for_reservation_guest_id(config, rest_shore, guest_id_data)

        for count, guest in enumerate(guest_data):
            for res_id in res_id_data:
                if res_id['Email'] == guest['Email']:
                    guest_data[count].update(res_id)
                if res_id['Email'] == test_data[signupGuest]['email']:
                    test_data[signupGuest]['guestId'] = res_id['guestId']
                    test_data[signupGuest]['reservationId'] = res_id['reservationId']
                    test_data[signupGuest]['reservationGuestId'] = res_id['reservationGuestId']

        # Get Different Moci and Doc Rejected Guests, they should not be same (applicable for > 2 Guests)
        test_data['mociRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
        test_data['docRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
        while test_data['mociRejected'] == test_data['docRejected'] and test_data['guests'] > 2:
            test_data['mociRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])
            test_data['docRejected'] = random.choice([x['reservationGuestId'] for x in guest_data])

        tx_id = generate_guid()
        # Do retries for bookvoyage-bff/signature Call
        _content = wait_for_signature(config, rest_shore, amount_due, test_data[reservationNumber], tx_id)
        is_key_there_in_dict('signedFields', _content)
        is_key_there_in_dict('signedTimeStamp', _content)
        is_key_there_in_dict('signature', _content)
        signed_fields = _content['signedFields']
        signed_time_stamp = _content['signedTimeStamp']
        signature = _content['signature']

        tx = payment_virgin(config, test_data, guest_data, rest_shore, amount_due, signature, signed_time_stamp, tx_id,
                            signed_fields, client_ref_num=test_data[reservationNumber])
        url = urljoin(config.shore.url, "bookvoyage-bff/reservation/pay")
        body = {
            "responseSignature": tx,
            "reservationNumber": test_data[reservationNumber],
            "paymentInfo": {
                "paymentMode": "card",
                "paymentMethod": [{
                    "expiryDate": "06",
                    "cardHolderName": f"{test_data[signupGuest]['firstName']} "
                                      f"{test_data[signupGuest]['lastName']}",
                    "cardType": "001",
                    "billingAddress": {
                        "zipCode": test_data[signupGuest]['addresses'][0]['zipCode'],
                        "lineTwo": test_data[signupGuest]['addresses'][0]['lineTwo'],
                        "city": test_data[signupGuest]['addresses'][0]['city'],
                        "countryCode": test_data[signupGuest]['addresses'][0]['countryCode'],
                        "lineOne": test_data[signupGuest]['addresses'][0]['lineOne'],
                        "state": test_data[signupGuest]['addresses'][0]['stateCode'],
                    }
                }],
                "currencyCode": "USD",
                "paidAmount": int(amount_due)
            }
        }

        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if _content['paymentDetail']['paidAmount'] != amount_due:
            raise Exception("Amount not completely paid after doing reservation !!")

    @pytest.mark.parametrize('country', [pytestrail.param('INDIA', '44841431'), pytestrail.param('USA', '26113960')])
    def test_08_upload_photo(self, config, rest_shore, guest_data, test_data, v_guest_data, country):
        """
        Upload Profile and Security Photos for each guest and save their URL's (Used during OCI)
        :param config:
        :param rest_shore:
        :param guest_data:
        :param test_data:
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
            first_name = guest['FirstName']
            last_name = guest['LastName']
            email_id = guest['Email']
            birth_date = guest['BirthDate']
            gender = guest['GenderCode'][0]

            security_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                           birth_date=birth_date, gender=gender).add_text()
            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()

            logger.debug(f"Uploading Security Photo #{count + 1} ...")
            security_photo_url = upload_media_file(config, rest_shore, security_photo)
            time.sleep(0.1)

            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            profile_photo_url = upload_media_file(config, rest_shore, profile_photo)
            time.sleep(0.1)

            guest_data[count]['security_photo'] = security_photo
            guest_data[count]["profile_photo"] = profile_photo
            guest_data[count]['SecurityPhotoUrl'] = security_photo_url
            guest_data[count]['ProfilePhotoUrl'] = profile_photo_url

            # Save Data for Signup Guest
            if guest['Email'] == test_data[signupGuest]['email']:
                test_data[signupGuest]['SecurityPhotoUrl'] = security_photo_url
                test_data[signupGuest]['ProfilePhotoUrl'] = profile_photo_url

    @pytestrail.case(32174395)
    def test_09_get_printing_templates(self, config, test_data, rest_shore):
        """
        Get Printing Templates
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(config.shore.url, "/fcstask-service/templates")
        _content = rest_shore.send_request(method="GET", url=_url, auth=None).content
        if len(_content) != 0:
            test_data['fcsTaskService'] = dict()
            for template in _content:
                is_key_there_in_dict('id', template)
                is_key_there_in_dict('name', template)
                is_key_there_in_dict('type', template)
                if template['type'] == 'tray':
                    test_data['fcsTaskService']['tray'] = template['name']
                if template['type'] == 'trackable':
                    test_data['fcsTaskService']['template'] = template['name']
        else:
            raise Exception("No print template Found!!")

    @pytestrail.case(32174396)
    def test_10_print_trackable(self, config, test_data, rest_shore, guest_data):
        """
        Print Trackable
        :param guest_data:
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(config.shore.url, "/fcstask-service/print/queue/")
        _body = {
            "template": test_data['fcsTaskService']['template'], "tray": test_data['fcsTaskService']['tray'],
            "items": [
                {
                    "orderId": generate_guid(),
                    "items": [
                        {
                            "hostId": guest_data[0]['reservationGuestId'],
                            "text": {
                                "caption7": "A3",
                                "caption6": "1(866)234-7350",
                                "caption1": "Rosemarie",
                                "caption5": "BLISS",
                                "caption4": "01/12/2019",
                                "caption3": "Mphfnlcpiq"
                            }
                        }
                    ]
                }
            ],
            "space": "0"
        }
        rest_shore.send_request(method="POST", url=_url, json=_body, auth=None)

    #@pytest.mark.skip(reason="DCP-89688")
    @pytestrail.case(32174397)
    def test_11_verify_printed_trackable(self, config, rest_shore, guest_data):
        """
        Verify Printed Trackable
        :param guest_data:
        :param config:
        :param rest_shore:
        :return:
        """
        # add retries after removing xfail

        _url = urljoin(config.shore.url, "/fcstask-service/print/queue/")
        _content = rest_shore.send_request(method="GET", url=_url, auth=None).content
        if len(_content) != 0:
            _status = False
            for template in _content:
                is_key_there_in_dict('id', template)
                is_key_there_in_dict('hostIds', template)
                is_key_there_in_dict('status', template)
                for host in template['hostIds']:
                    if host == guest_data[0]['reservationGuestId']:
                        _status = True
            if not _status:
                logger.debug("Trackable not printed successfully!!")
        else:
            raise Exception("No Printed Trackable Found!!")

    @pytest.mark.SkipForStageEnv
    @pytestrail.case(26821387)
    def test_12_seaware_session_login(self, config, rest_shore, creds, test_data, xml_data):
        """
        Login to seaware for session id
        :param config:
        :param rest_shore:
        :param creds:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.login_seaware.format(creds.seaware.username, creds.seaware.password)
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('Login_OUT', _content_json)
        is_key_there_in_dict('MsgHeader', _content_json['Login_OUT'])
        is_key_there_in_dict('SessionGUID', _content_json['Login_OUT']['MsgHeader'])
        test_data['seawareSessionId'] = _content_json['Login_OUT']['MsgHeader']['SessionGUID']

    @pytest.mark.SkipForStageEnv
    @pytestrail.case(22855412)
    def test_13_check_reservation_seaware(self, config, rest_shore, test_data, xml_data):
        """
        Check the created booking in seaware
        :param config:
        :param rest_shore:
        :param test_data:
        :param xml_data:
        :return:
        """
        url = urljoin(config.shore.seaware, 'SwBizLogic/Service.svc/LoadBooking_IN')
        xml = xml_data.load_booking_seaware.format(test_data['seawareSessionId'], test_data['reservationNumber'])
        rest_shore.session.headers.update({'Content-Type': 'application/x-versonix-api'})
        _content = rest_shore.send_request(method="POST", url=url, data=xml, auth=None).content
        _content_json = xmltodict.parse(_content)
        is_key_there_in_dict('LoadBooking_OUT', _content_json)
        is_key_there_in_dict('ResShell', _content_json['LoadBooking_OUT'])
        is_key_there_in_dict('ResPackages', _content_json['LoadBooking_OUT']['ResShell'])
        is_key_there_in_dict('ResPackage', _content_json['LoadBooking_OUT']['ResShell']['ResPackages'])
        is_key_there_in_dict('VacationDates', _content_json['LoadBooking_OUT']['ResShell']['ResPackages']['ResPackage'])
        _res_package = _content_json['LoadBooking_OUT']['ResShell']['ResPackages']['ResPackage']
        assert _res_package['PackageCode'] == test_data['voyage']['id'], 'Voyage Id Mismatch !!'
        assert _res_package['Ship'] == test_data['voyage']['ship']['code'], 'Ship Code Mismatch !!'
        assert _res_package['VacationDates']['From'].split('T')[0] == test_data['voyage'][
            'startDate'], 'Embark Date Mismatch !!'
        assert _res_package['VacationDates']['To'].split('T')[0] == test_data['voyage'][
            'endDate'], 'Debark Date Mismatch !!'
        rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytest.mark.SkipForStageEnv
    @pytestrail.case(25013129)
    def test_14_check_guest_details_seaware(self, config, rest_shore, test_data, guest_data, xml_data):
        """
        Check the guest details in seaware
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
            _guest_detail = \
                _content_json['vx:OTA_ResRetrieveRS']['vx:ReservationsList']['vx:CruiseReservation'][
                    'vx:ReservationInfo'][
                    'vx:GuestDetails']['vx:GuestDetail']
            assert len(_guest_detail) == 2, 'Guest Count is not matching in seaware !!'
            for _guest in range(0, len(_guest_detail)):
                is_key_there_in_dict('vx:ContactInfo', _guest_detail[_guest])
                is_key_there_in_dict('vx:PersonName', _guest_detail[_guest]['vx:ContactInfo'])
                assert _guest_detail[_guest]['vx:ContactInfo']['vx:PersonName']['vx:GivenName'] == guest_data[_guest][
                    'FirstName'], 'First Name Mismatch !!'
                assert _guest_detail[_guest]['vx:ContactInfo']['vx:PersonName']['vx:Surname'] == guest_data[_guest][
                    'LastName'], 'Last Name Mismatch !!'
                if 'vx:Address' in _guest_detail[_guest]['vx:ContactInfo']:
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address'][_guest]['vx:AddressLine'][_guest] == \
                           guest_data[_guest]['Addresses'][_guest]['lineOne'], 'Address LineOne Mismatch !!'
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address'][_guest]['vx:CityName'] == \
                           guest_data[_guest]['Addresses'][_guest]['city'], 'City Mismatch !!'
                    assert _guest_detail[_guest]['vx:ContactInfo']['vx:Address'][_guest]['vx:PostalCode'] == \
                           guest_data[_guest]['Addresses'][_guest]['zipCode'], 'zipCode Mismatch !!'
        finally:
            rest_shore.session.headers.update({'Content-Type': 'application/json'})

    @pytestrail.case(68992715)
    def test_15_calculate_invoice(self, config, test_data, rest_shore):
        """
        Calculate the total invoice on the summary page
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        voyage_id = test_data['voyage']['id']
        url = urljoin(config.shore.url, "bookvoyage-bff/calculateinvoice")
        body = {
            "voyageId": voyage_id,
            "cabins": [{"adultsCount": test_data['guests'], "cabinTypeCode": test_data["cabin"]["categoryCode"], "accessible": False}],
            "currencyCode": "USD",
            "guestDetails": [{"hasOptedForTripInsurance": True, "hasOptedForContactForFlights": True},
                             {"hasOptedForTripInsurance": True, "hasOptedForContactForFlights": True}]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if _content['isSoldOut']!= False:
            raise Exception("Cannot able to calculate invoice because no data is found")

    @pytestrail.case(68992716)
    def test_16_voyage_dashboard(self, config, test_data, rest_shore, guest_data):
        """
        Get the information regarding the Voyage dashboard
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            'reservationNumber': test_data['reservationNumber']
        }
        url = urljoin(config.shore.url, f"bookvoyage-bff/voyagedashboard?")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

        if len(_content) == 0:
            raise Exception("there are no available Data !!")

    @pytestrail.case(68992717)
    def test_17_credits(self, config, test_data, rest_shore):
        """
        get credits call
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(config.shore.url, f"bookvoyage-bff/users/credits")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        if len(_content) != 0:
            raise Exception("there are nothing credited!")

    @pytestrail.case(68992719)
    def test_18_whats_included(self, config, test_data, rest_shore, guest_data):
        """
        get the information of whats included
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(config.shore.url, f"bookvoyage-bff/whatsIncluded")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content

        if len(_content[0]['description']) == 0:
            raise Exception("there is nothing included!!")

    @pytestrail.case(68992720)
    def test_19_sailing_voyages(self, config, test_data, rest_shore, guest_data):
        """
        get the sailing voyages for selected user
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        voyage_id = test_data['voyage']['id']
        params = {
            'voyageId': voyage_id,
            'packageCode': ""
        }
        url = urljoin(config.shore.url, f"bookvoyage-bff/sailings?")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

        if len(_content) != 0:
            raise Exception("no voyages present")

    @pytestrail.case(68992721)
    def test_20_search_qualifier(self, config, test_data, rest_shore, guest_data):
        """
        Search qualifier call
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        url = urljoin(config.shore.url, "bookvoyage-bff/cabincategories/search")

        body = {
                "voyageId": test_data['voyage']['id'],
                "searchQualifier": {
                    "accessible": False,
                    "cabins": [{"guestCounts":
                                    [{
                                        "ageCategory": "Adult",
                                        "count": test_data['guests']
                                      }]
                                }],
                    "currencyCode": "USD",
                    "promoCodes": []
                }
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        if len(_content) == 0:
            raise Exception(f"No data is returned !!")

    @pytestrail.case(68993502)
    def test_21_user_profile(self, config, test_data, rest_shore, guest_data):
        """
        Get User details call
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data
        :return:
        """
        url = urljoin(config.shore.url, f"bookvoyage-bff/userprofile")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        if len(_content['guestId'] ) == 0:
            raise Exception("no user data found!!")

    @pytestrail.case(68993503)
    def test_22_rts_details(self, config, test_data, rest_shore, guest_data):
        """
        get rts details
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            'reservationNumber': test_data['reservationNumber']
        }
        url = urljoin(config.shore.url, f"bookvoyage-bff/rtsdetails?")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content

        if len(_content[0]['reservationGuestId']) == 0:
            raise Exception("there are no rts details !!")

    @pytestrail.case(68993504)
    def test_23_availiable_addons(self, config, test_data, rest_shore, guest_data):
        """
        get availiable addons
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            'reservationNumber': test_data['reservationNumber'], 'codes': ""
        }
        url = urljoin(config.shore.url, f"bookvoyage-bff/availableAddOns?")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        if len(_content) != 0:
            raise Exception("there are no available AddOnss !!")

    @pytestrail.case(68993505)
    def test_24_purchased_addons(self, config, test_data, rest_shore, guest_data):
        """
        get purchased addons
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        params = {
            'reservationNumber': test_data['reservationNumber']
        }
        url = urljoin(config.shore.url, f"bookvoyage-bff/purchasedAddOns?")
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        if len(_content) != 0:
            raise Exception("there are no purchased addons !!")

    @pytestrail.case(69829227)
    def test_25_verify_badges_array(self, config, rest_shore):
        """
        To verify badges array
        :param config:
        :param rest_shore:
        :return:
        """

        url = urljoin(config.shore.url, f"/bookvoyage-bff/lookup")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        if len(_content) == 0:
            raise Exception("Badges array are empty")
        is_key_there_in_dict('badges', _content)
        for badges_ar in _content['badges']:
            if badges_ar["name"] not in ['FOODIE', 'HOLIDAY', 'MERMAIDEN', 'MIAMI RESIDENT', 'TRANSATLANTIC', 'SEA-BLAZER']:
                raise Exception("Data is not available")

    @pytestrail.case(69683655)
    def test_26_verify_agent_details(self, config, rest_shore):
        """
        :To verify agent details if the agent is valid and agent detail information is present.
        :param config:
        :param rest_shore:
        :return:
        """
        if config.env == 'INTEGRATION':
            pytest.skip("URL is not available")
        else:
            url = urljoin(config.shore.url, f"dxpcore/reservations/agentdetail/validation")
            params = {
                'agentId': 41738,
                'includeAgentDetails': "true"
            }
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            if len(_content) == 0:
                raise Exception("Details are not available")
            is_key_there_in_dict('agentName', _content)
            is_key_there_in_dict('agencyName', _content)
            is_key_there_in_dict('isValid', _content)
            is_key_there_in_dict('phoneNumber', _content)
            is_key_there_in_dict('email', _content)

    @pytestrail.case(69683656)
    def test_27_verify_agent_details_agentid_wrong(self, config, rest_shore):
        """
        :To verify the agent details if Id is wrong.
        :param config:
        :param rest_shore:
        :return:
        """
        if config.env == 'INTEGRATION':
            pytest.skip("URL is not available")
        else:
            url = urljoin(config.shore.url, f"dxpcore/reservations/agentdetail/validation")
            params = {
                'agentId': 417381,
                'includeAgentDetails': "true"
            }
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            if len(_content) == 0:
                raise Exception("Details are not available")
            is_key_there_in_dict('isValid', _content)
            if _content['isValid']:
                raise Exception("Id is not wrong")

    @pytestrail.case(69683657)
    def test_28_verify_agent_details_info_not_present(self, config, rest_shore):
        """
        :To verify the agent details if details info is not present.
        :param config:
        :param rest_shore:
        :return:
        """
        if config.env == 'INTEGRATION':
            pytest.skip("URL is not available")
        else:
            url = urljoin(config.shore.url, f"dxpcore/reservations/agentdetail/validation")
            params = {
                'agentId': 41738,
                'includeAgentDetails': "false"
            }
            _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
            is_key_there_in_dict('isValid', _content)
            if _content['isValid']:
                logger.debug("Information details is available")
