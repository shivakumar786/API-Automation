__author__ = 'prahlad.sharma'


from virgin_utils import *

class Apihit:
    """
    Page Class for Sailor app api calls page
    """

    def __init__(self, config, rest_shore, test_data):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_shore:
        :param test_data:
        """
        self.config = config
        self.rest_oci = rest_shore
        self.test_data = test_data

    def get_token(self, side):
        """
        This function is used to get the user Token
        """
        if side == 'shore':
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.identityaccessmanagement'), 'oauth/token')
        else:
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.identityaccessmanagement'), 'oauth/token')
        params = {
            "grant_type": "client_credentials"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, params=params, auth="basic").content
        is_key_there_in_dict('access_token', _content)
        _token = _content['access_token']
        self.rest_oci.userToken = f"bearer {_token}"
        self.test_data['userToken'] = self.rest_oci.userToken

    def get_ship_date(self):
        """
        Function to get the ship date
        """
        params = {"shipcode": self.config.ship.code}
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        self.test_data['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())

    def get_next_voyage(self, test_data):
        """
        This function is used to get the next voyage details
        :param test_data:
        """
        _time = get_ship_time(self.rest_oci, self.config, test_data)
        _date = _time.shipDate

        start_date = str(_date.date())
        end_date = str(_date.date() + timedelta(days=31))
        url = urljoin(self.config.ship.url,
                      f"dxpcore/voyages/search/findbyembarkdate?startdate={start_date}&enddate={end_date}")

        # Get Voyages present in system from today + 31 days, Raise exception if there is no voyage present in system
        _content = self.rest_oci.send_request(method="GET", url=url, auth="bearer").content
        test_data['_voyages'] = sorted([x for x in _content['_embedded']['voyages'] if x['shipCode']
                                        == self.config.ship.code], key=lambda i: i['embarkDate'])
        for voyage in test_data['_voyages']:
            voyage_embarkDate = datetime.strptime(voyage['embarkDate'].split('T')[0],
                                                  "%Y-%m-%d").strftime("%m/%d/%Y")
            if voyage_embarkDate == self.test_data['debarkDate'] and voyage['shipCode'] == self.config.ship.code:
                self.test_data['next_firstDay'] = voyage['embarkDate'].split('T')[0]
                self.test_data['next_lastDay'] = voyage['debarkDate'].split('T')[0]
                self.test_data['next_raw_embarkDate'] = voyage['embarkDate']
                self.test_data['next_raw_debarkDate'] = voyage['debarkDate']
                self.test_data['next_embarkDate'] = datetime.strptime(voyage['embarkDate'].split('T')[0],
                                                                      "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['next_debarkDate'] = datetime.strptime(voyage['debarkDate'].split('T')[0],
                                                                      "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['next_voyageId'] = voyage['voyageId']
                self.test_data['next_voyageNumber'] = voyage['number']
                self.test_data['next_shipCode'] = voyage['shipCode']
                # self.test_data['next_namekey'] = voyage['nameKey']
                break
        else:
            raise Exception(f"There's no Future voyage with embark day as {self.test_data['raw_embarkDate']} !!")

        params = {
            "voyagenumber": self.test_data['next_voyageNumber']
        }

        url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), 'voyages/search/findbyvoyagenumber')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        for voyage in _content['_embedded']['voyages']:
            self.test_data['next_namekey_shore'] = voyage['nameKey']
            break
        else:
            raise Exception("There's no active voyage in system !!")
        self.test_data[
            'next_voyage_name_shore'] = f"{self.test_data['next_namekey_shore']} " \
                                        f"{self.test_data['next_embarkDate']}-{self.test_data['next_debarkDate']}"

    def get_voyage_details(self):
        """
        This function is used to get the voyage details
        """
        _ship = self.config.ship.url
        params = {
            "shipcode": self.config.ship.code,
        }
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            if voyage['isActive']:
                self.test_data['firstDay'] = voyage['embarkDate'].split('T')[0]
                self.test_data['lastDay'] = voyage['debarkDate'].split('T')[0]
                self.test_data['raw_embarkDate'] = voyage['embarkDate']
                self.test_data['raw_debarkDate'] = voyage['debarkDate']
                self.test_data['embarkDate'] = datetime.strptime(voyage['embarkDate'].split('T')[0],
                                                                 "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['debarkDate'] = datetime.strptime(voyage['debarkDate'].split('T')[0],
                                                                 "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['voyageId'] = voyage['voyageId']
                self.test_data['voyageNumber'] = voyage['number']
                self.test_data['shipCode'] = voyage['shipCode']
                self.test_data['namekey'] = voyage['nameKey']
                if voyage['shipCode'] == self.config.ship.code:
                    self.test_data['shipName'] = 'Scarlet Lady'
                break
        else:
            raise Exception("There's no active voyage in system !!")
        self.test_data[
            'voyage_name_space'] = f"{self.test_data['namekey']} {self.test_data['embarkDate']}-{self.test_data['debarkDate']}"
        self.test_data[
            'voyage_name'] = f"{self.test_data['namekey'].strip()} {self.test_data['embarkDate']}-{self.test_data['debarkDate']}"

    def sign_up(self, config, test_data, rest_shore, guest_data, v_guest_data, country):
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

    def setup_active_voyage(self, config, test_data, rest_shore):
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

    def get_cabin_category(self, config, test_data, rest_shore, country):
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

    def cabin_search(self, config, test_data, rest_shore, country):
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

    def get_vip_status(self, config, test_data, rest_shore, country):
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

    def hold_cabin(self, config, test_data, rest_shore, country):
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

    def reservation(self, config, request, test_data, rest_shore, guest_data, v_guest_data, country):
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
                if res_id['email'] == guest['Email']:
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

    def upload_photo(self, config, rest_shore, guest_data, test_data, v_guest_data, country):
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
            first_name = guest['firstName']
            last_name = guest['lastName']
            email_id = guest['email']
            birth_date = guest['birthDate']
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
            if guest['email'] == test_data[signupGuest]['email']:
                test_data[signupGuest]['SecurityPhotoUrl'] = security_photo_url
                test_data[signupGuest]['ProfilePhotoUrl'] = profile_photo_url

    def create_reservation(self, config, test_data, rest_shore, guest_data, request, v_guest_data, country):
        """
        Function to create reservation
        :return:
        """
        self.sign_up(config, test_data, rest_shore, guest_data, v_guest_data, country)
        self.setup_active_voyage(config, test_data, rest_shore)
        self.get_cabin_category(config, test_data, rest_shore, country)
        self.cabin_search(config, test_data, rest_shore, country)
        self.get_vip_status(config, test_data, rest_shore, country)
        self.hold_cabin(config, test_data, rest_shore, country)
        self.reservation(config, request, test_data, rest_shore, guest_data, v_guest_data, country)

    def generate_visa_or_passport(self, guest_data, document_count, passport, visa, nationality, visa_country):
        """
        Function to generate the Dummy VISA and Passport
        """
        guest_data[0]['documents'] = {}
        for count in range(document_count):
            first_name = generate_first_name()
            last_name = generate_last_name()
            document_number = str(generate_document_number())
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
            gender = random.choice(["M", "F"])
            expiry = generate_document_expiry()
            mrz_data = {
                'document_type': "P", 'surname': last_name,
                'given_names': first_name, 'country_code': convert_country_code(nationality, 3),
                'document_number': document_number, 'nationality': convert_country_code(nationality, 3),
                'birth_date': modify_birth_date(birth_date), 'sex': gender,
                'expiry_date': str(expiry.strftime('%y%m%d'))
            }
            if passport:
                guest_data[0]['documents']['passport']=GenerateMrzImages(**mrz_data).mrz_image()

            if visa:
                if visa_country != "Germany":
                    mrz_data['country_code'] = convert_country_code(visa_country, 3)
                else:
                    mrz_data['country_code'] = "D"
                mrz_data['optional_data'] = "M550120"
                mrz_data['document_type'] = "VC"
                guest_data[0]['documents']['visa']=GenerateMrzImages(**mrz_data).mrz_image()

