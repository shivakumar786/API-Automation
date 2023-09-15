__author__ = 'mohit.raghav'

from virgin_utils import *


class Apihit:
    """
    Page Class to mark sailor as check-in onboard before sign-in sailor app ship
    """
    def __init__(self, config, test_data, rest_shore, guest_data, rest_ship, db_iam, couch, db_core, creds):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_shore:
        :param rest_ship:
        :param test_data:
        :param guest_data:
        :param db_iam:
        :param couch:
        :param db_core:
        :param creds:
        """
        self.config = config
        self.rest_ship = rest_ship
        self.rest_shore = rest_shore
        self.test_data = test_data
        self.guest_data = guest_data
        self.db_iam = db_iam
        self.couch = couch
        self.db_core = db_core
        self.creds = creds

    def crew_sign_up(self, config, test_data, rest_shore, guest_data, rest_ship, creds):
        """
        Register a User
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param rest_ship:
        :param creds:
        :return:
        """
        first_name = generate_first_name(from_saved=True)
        last_name = generate_last_name(from_saved=True)
        test_data['username'] = generate_email_id(first_name=first_name, last_name=last_name)
        test_data['password'] = "Voyages@9876"
        test_data['appId'] = str(generate_guid()).upper()
        test_data['deviceId'] = str(generate_random_alpha_numeric_string(length=32)).lower()
        url = urljoin(config.ship.url, "user-account-service/signup")
        rest_shore.session.headers.update({'Content-Type': 'application/json'})
        body = {
            "birthDate": guest_data[0]['BirthDate'],
            "email": test_data['username'],
            "firstName": guest_data[0]['FirstName'],
            "userType": "guest",
            "preferredName": guest_data[0]['FirstName'],
            "lastName": guest_data[0]['LastName'],
            "password": test_data['password'],
            "enableEmailNewsOffer": False
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        is_key_there_in_dict('authenticationDetails', _content)
        _token = _content['authenticationDetails']['accessToken']
        rest_shore.userToken = f"bearer {_token}"
        is_key_there_in_dict('accessToken', _content['authenticationDetails'])
        test_data['userToken'] = rest_shore.userToken

        _url = urljoin(config.ship.url, '/user-account-service/signin/username')
        body = {
            "userName": creds.verticalqa.username, "password": creds.verticalqa.password,
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = rest_shore.send_request(method="POST", url=_url, json=body).content
        rest_shore.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

        url = urljoin(config.shore.url, "identityaccessmanagement-service/oauth/token")
        params = {"grant_type": "client_credentials"}
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="basic").content
        rest_ship.bearerToken = f"{_content['token_type']} {_content['access_token']}"

    def get_data_shipboard(self, config, test_data, rest_shore, db_core):
        """
        Checking and fetching the guest details to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param db_core:
        :return:
        """
        # To get the voyage Id for our active voyage
        _ship = config.ship.url
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            if voyage['isActive']:
                test_data['embarkDate'] = voyage['embarkDate'].split('T')[0]
                test_data['debarkDate'] = voyage['debarkDate'].split('T')[0]
                test_data['voyageId'] = voyage['voyageId']
                test_data['voyageNumber'] = voyage['number']
                test_data['shipCode'] = voyage['shipCode']
                break
        else:
            raise Exception("There's no active voyage in system !!")
        test_data['shipside_guests'] = []
        sql_query = f"with cte as (SELECT reservationguestid, reservationid, guestid, isprimary, row_number() " \
                 f"over(partition by reservationid) AS rownum FROM public.reservationguest where embarkdate = " \
                 f"'{test_data['embarkDate']}' and debarkdate ='{test_data['debarkDate']}' and reservationstatuscode = '" \
                 f"RS' and stateroom!= 'GTY') select reservationguestid, reservationid, guestid, isprimary from cte " \
                 f"where reservationid in (select reservationid  from cte where rownum > 1);"
        _query = sql_query.format(test_data['embarkDate'], test_data['debarkDate'])
        _data = db_core.ship.run_and_fetch_data(query=_query)
        for _guests in _data:
            test_data['shipside_guests'].append({
                "reservationguestid": _guests['reservationguestid'],
                "reservationid": _guests['reservationid'],
                "isprimary": _guests['isprimary'],
                "guestid": _guests['guestid']
            })
        if len(test_data['shipside_guests']) == 0:
            raise Exception('No guest available on ship side for running E2E Ship Side')
        else:
            random.shuffle(test_data['shipside_guests'])

    def get_guest_details_ship_side(self, config, guest_data, test_data, rest_shore):
        """
        Fetching the guest details from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _ship = config.ship.url
        for guest in test_data['shipside_guests']:
            params = {"personid": guest['guestid']}
            _url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),
                           "/userprofiles/getuserdetails")
            _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="crew").content
            if len(_content) != 0 and True is guest['isprimary']:
                url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                              f"/guests/search/findbyreservationguests/{guest['reservationguestid']}")
                _content_findbyreservationguests = rest_shore.send_request(method="GET", url=url, auth="user").content
                if '@mailinator.com' in _content_findbyreservationguests['email']:
                    test_data['shipside_guests'].clear()
                    test_data['iam_user_id'] = _content['userId']
                    test_data['shipside_guests'].append(guest)
                    test_data['shipside_guests'][0]['email'] = _content_findbyreservationguests['email']
                    break

    def get_guest_guest_id_ship_side(self, config, test_data, rest_shore, guest_data, db_iam):
        """
        Fetching the guest guestid from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param db_iam:
        :return:
        """
        guest_data.clear()
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/reservationguests/search/findbyguestids")
        body = {"guestIds": [test_data['shipside_guests'][0]['guestid']]}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        _query = f"select * from public.userprofile where personid  = '{_content['_embedded']['reservationGuests'][0]['guestId']}';"
        _data = db_iam.ship.run_and_fetch_data(query=_query)
        guest_data.append({
            "reservationId": _content['_embedded']['reservationGuests'][0]['reservationId'],
            "reservationGuestId": _content['_embedded']['reservationGuests'][0][
                'reservationGuestId'],
            "guestId": _content['_embedded']['reservationGuests'][0]['guestId'],
            "email": _data[0]['email'],
            "FirstName": _data[0]['firstname'],
            "LastName": _data[0]['lastname'],
            "GenderCode": _data[0]['gendercode'],
            "birthDate": str(_data[0]['birthdate']),
            "CitizenshipCountryCode": _data[0]['citizenshipcountrycode']
        })
        test_data['reservation_guest_ids'] = guest_data[0]['reservationGuestId']
        test_data['cabinNumber'] = _content['_embedded']['reservationGuests'][0]['stateroom']

    @retry_when_fails(retries=20, interval=5)
    def crew_app_dashboard(self, config, rest_ship, rest_shore, test_data):
        """
        Get Crew App Dashboard Items
        :param config:
        :param rest_ship:
        :param rest_shore:
        :param test_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.useraccountservice"), "/userprofile")
        _content = rest_shore.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('personId', _content)
        test_data['personId'] = _content['personId']
        test_data['crew_framework'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-dashboard/dashboard")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('profileImageUrl', _content)
        is_key_there_in_dict('isOnDuty', _content)
        is_key_there_in_dict('isDutyManager', _content)
        is_key_there_in_dict('voyageDetails', _content)
        is_key_there_in_dict('shiftDetails', _content)
        is_key_there_in_dict('currentDate', _content)
        test_data['crew_framework']['currentDate'] = _content['currentDate']
        current_date = change_epoch_time(datetime.today().date())
        for count, voyageItineraries in enumerate(_content['voyageDetails']['voyageItineraries']):
            if not voyageItineraries['isSeaDay']:
                try:
                    current_ship_date = change_epoch_time(voyageItineraries['arrivalTime'][:10])
                except Exception:
                    current_ship_date = change_epoch_time(voyageItineraries['departureTime'][:10])
                if current_date == current_ship_date:
                    test_data['crew_framework']['portCode'] = voyageItineraries['portCode']
                    test_data['crew_framework']['portName'] = voyageItineraries['portName']
                    break
            else:
                test_data['crew_framework']['portCode'] = ""
                test_data['crew_framework']['portName'] = "At Sea"
                break

    @retry_when_fails(retries=120, interval=5)
    def validate_ship_time(self, config, test_data, rest_ship):
        """
        Get ship time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['aci'] = dict()
        params = {'shipcode': config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        ship_off_set = _content['shipOffset']
        epoch_time_stamp = _content['epocTimestamp']
        test_data['aci']['shipEpochTime'] = epoch_time_stamp
        ship_off_set = ship_off_set * 60
        test_data['aci']['shipOffSet'] = ship_off_set
        ship_time = (epoch_time_stamp + ship_off_set) * 1000

        test_data['aci']['shipTimeDate'] = datetime.fromtimestamp(ship_time / 1000).strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        test_data['aci']['currentDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        test_data['demo'] = ship_time
        test_data['aci']['boardingStatusDateEpoch'] = ship_time
        test_data['aci']['validationStatusDate'] = ship_time

    def get_doc_id_for_moci_rejected_guest(self, config, test_data, rest_ship, guest_data):
        """
        Get Rejected Document(s) to be verified and to check by default voyage well acknowledgement
        form should be pending
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=_url, auth='couch').content
            test_data['aci']['guests'] = _content
            test_data[_res_id] = _content
            _res_id = guest['reservationGuestId']
            if not test_data[_res_id]['IsTermsAccepted']:
                _content = rest_ship.send_request(method="GET", url=_url).content
                test_data[_res_id] = _content
        assert "False" != test_data['aci']['guests']['CheckinStatus'], "By default voyage well contract is not" \
                                                                       " coming into pending status. "

    def do_aci_for_moci_rejected_guest(self, config, test_data, rest_ship, guest_data):
        """
        Approve Document(s) through ACI
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {"shipcode": config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        ship_off_set = _content['shipOffset']
        epoch_time_stamp = _content['epocTimestamp']
        test_data['aci']['shipDate'] = _content['utcTimestamp'].split('T')[0]
        ship_off_set = ship_off_set * 60
        ship_time = (epoch_time_stamp + ship_off_set) * 1000
        test_data['aci']['validationStatusDate'] = str(datetime.fromtimestamp(epoch_time_stamp)).replace(' ', 'T')

        test_data['aci']['shipTimeDate'] = datetime.fromtimestamp(ship_time / 1000).strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = test_data[_res_id]
            params = {"rev": _data['_rev']}
            _url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _to_set_true = [
                'IsAssistedCheckInDone', 'IsHealthQuestionsAnswered',
                'IsValidationSuccessful', 'IsIdVerified', 'IsIdentificationDetailsAvailable',
                'IsModerateOnlineCheckInDone', 'IsOnlineCheckedIn', 'IsPartyHealthCompleted',
                'IsPaymentInfoAvailable', 'IsPersonalInformationAvailable', 'IsPhotoVerified',
                'IsPrePostCruiseDetailsAvailable', 'IsContractAgreed'
            ]
            # Set to True-
            for _to_true in _to_set_true:
                _data[_to_true] = True

            _data['lastModifiedBy'] = "Script Automation"
            _data["lastModifiedDate"] = test_data['aci']['shipTimeDate']
            _data["sourceId"] = "CouchDatabase"
            _data["ValidationStatusDate"] = test_data['aci']['validationStatusDate']
            _data["ValidationStatusDateEpoch"] = test_data['aci']['boardingStatusDateEpoch']
            _data['CheckInStatusDateEpoch'] = test_data['aci']['boardingStatusDateEpoch']
            _data['CheckinStatusDate'] = test_data['aci']['validationStatusDate']
            _data['TerminalCheckinStatus'] = 'COMPLETED'

            _content = rest_ship.send_request(method="PUT", url=_url, json=_data, params=params,
                                              auth='couch').content
            assert _content['ok'], "ACI for Rejected Guests Failed !!"

    @retry_when_fails(retries=120, interval=5)
    def get_document_to_be_updated_first_pass(self, config, test_data, rest_ship, guest_data):
        """
        Get up 1st Layer of user data for modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['gangway'] = dict()
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url, auth='couch').content
            guest[_res_id] = _content

    def update_document_first_pass(self, config, test_data, rest_ship, guest_data):
        """
        Put up 1st Layer of user data modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = guest[_res_id]
            _rev = _data['_rev']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _data['IsOnBoarded'] = True
            _data['lastModifiedBy'] = "Script Automation"
            _data['OnBoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['BoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['OnBoardingStatusDateEpoch'] = guest[_res_id]['EmbarkDateEpoch']
            _data['BoardingStatusDateEpoch'] = guest[_res_id]['EmbarkDateEpoch']
            _data['lastModifiedDate'] = guest[_res_id]['lastModifiedDate']
            _data['sourceId'] = 'CouchDatabase'
            _data['boardingStatusChangedBy'] = "SYSTEM"
            for count in range(0, 5):
                try:
                    revision = rest_ship.send_request(method="GET", url=url,  auth='couch').content['_rev']
                    params = {"rev": revision}
                    _content = rest_ship.send_request(method="PUT", url=url, json=_data, params=params,
                                                      auth='couch').content
                    assert _content['ok'], "Documents update Failed 1st Time !!"
                    test_data[_res_id] = _content
                    break
                except (Exception, ValueError):
                    pass
            else:
                raise Exception(f"Update Document 1st Pass Res-ID: {_res_id}, not updated via sync !!")

    @retry_when_fails(retries=120, interval=5)
    def get_document_to_be_updated_second_pass(self, config, test_data, rest_ship, guest_data):
        """
        Get 2nd Layer of user data for modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url,  auth='couch').content
            guest[_res_id] = _content

    def update_document_second_pass(self, config, test_data, rest_ship, guest_data):
        """
        Put up 2nd Layer of user data modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = guest[_res_id]
            _rev = _data['_rev']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _data['IsOnBoarded'] = True
            _data['lastModifiedBy'] = "Script Automation"
            _data['OnBoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['BoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['OnBoardingStatusDateEpoch'] = guest[_res_id]['OnBoardingStatusDateEpoch']
            _data['BoardingStatusDateEpoch'] = guest[_res_id]['BoardingStatusDateEpoch']
            _data['lastModifiedDate'] = guest[_res_id]['lastModifiedDate']
            _data['sourceId'] = 'CouchDatabase'
            _data['boardingStatusChangedBy'] = "SYSTEM"
            for count in range(0, 5):
                try:
                    revision = rest_ship.send_request(method="GET", url=url,  auth='couch').content['_rev']
                    params = {"rev": revision}
                    _content = rest_ship.send_request(method="PUT", url=url, json=_data, params=params,
                                                      auth='couch').content
                    assert _content['ok'], "Documents update Failed 2nd Time !!"
                    test_data[_res_id] = _content
                    break
                except (Exception, ValueError):
                    pass
            else:
                raise Exception(f"Update Document 2nd Pass Res-ID: {_res_id}, not updated via sync !!")

    def get_final_updated_document(self, config, test_data, rest_ship, guest_data):
        """
        Save the updated document (after changes being made by gangway)
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['guestStatusDocument'] = dict()
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url,  auth='couch').content
            test_data['guestStatusDocument'][_res_id] = _content
            assert test_data['guestStatusDocument'][_res_id]['TerminalCheckinStatus'] == 'COMPLETED', "Sailor is not " \
                                                                                                      "Checked IN "
            assert test_data['guestStatusDocument'][_res_id]['IsOnBoarded'], "Sailor is not Onboard"

    def verify_gangway_location(self, test_data, config, rest_ship):
        """
        To verify the gangway location Document.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = f"{config.ship.sync}/GangwayLocations::{test_data['shipCode']}"
        _content = rest_ship.send_request(method="GET", url=url, auth='couch', timeout=60).content
        if len(_content) == 0:
            raise Exception("Gangway location document is not created !!")
        else:
            is_key_there_in_dict('GangwayLocations', _content)
            test_data['gangway_locations'] = _content['GangwayLocations']

    def create_person_event_doc(self, config, test_data, couch, guest_data):
        """
        Create a person event document in couch
        :param guest_data:
        :param test_data:
        :param config:
        :pram test_data:
        :param couch:
        """
        location = test_data['gangway_locations'][0]['GangWayLocation']
        gangway_location_id = test_data['gangway_locations'][0]['LocationID']
        current_date = str(datetime.now()).split(" ")[0]
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _event_id = generate_guid()
            body = {
                "_id": f"PersonEvent::{_res_id}::{_event_id}",
                "DebarkDateEpoch": change_epoch_time(test_data['debarkDate']) * 1000,
                "EmbarkDateEpoch": change_epoch_time(test_data['embarkDate']) * 1000,
                "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                "X-DEVICE-ID": "1f7c8d34357bbb0f",
                "channels": [
                    "PersonEvent",
                    config.ship.code,
                    f"{config.ship.code}_PersonEvent",
                    f"{config.ship.code}_emb_gw_t"
                ],
                "deviceName": "SM-G975F",
                "eventDateEpoch": int(round(time.time() * 1000)),
                "eventGenerationMethod": "MANUAL",
                "eventID": _event_id,
                "eventType": "ON_BOARD",
                "gangwayLocationId": gangway_location_id,
                "lastModifiedBy": "Script Automation",
                "lastModifiedDate": f"{datetime.now().strftime('%Y-%b-%dT%H:%M:00')}.751Z",
                "lastModifiedDateEpoch": int(round(time.time() * 1000)),
                "location": location,
                "personID": _res_id,
                "personType": "GUEST",
                "portCode": test_data['crew_framework']['portCode'],
                "portName": test_data['crew_framework']['portName'],
                "shipCode": config.ship.code,
                "sourceId": "CouchDatabase",
                "teamMemberID": test_data['personId'],
                "teamMemberName": "vertical-qa",
                "type": "PersonEvent",
                "voyageNumber": test_data['voyageId']
            }
            content = couch.send_request(method="POST", url=f"{config.ship.sync}/", json=body,
                                         auth='couch').content
            is_key_there_in_dict('ok', content)
            assert content['ok'], "Document not created !!!"

    def checkin_onboard_guest(self, config, test_data, rest_shore, guest_data, rest_ship, db_iam, couch, db_core, creds):
        """
        Function to mark sailor as checkin onboard
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :param rest_ship:
        :param creds:
        :param db_iam:
        :param couch:
        :param db_core:
        :return:
        """
        self.crew_sign_up(config, test_data, rest_shore, guest_data, rest_ship, creds)
        self.get_data_shipboard(config, test_data, rest_shore, db_core)
        self.get_guest_details_ship_side(config, guest_data, test_data, rest_shore)
        self.get_guest_guest_id_ship_side(config, test_data, rest_shore, guest_data, db_iam)
        self.crew_app_dashboard(config, rest_ship, rest_shore, test_data)
        self.validate_ship_time(config, test_data, rest_ship)
        self.get_doc_id_for_moci_rejected_guest(config, test_data, rest_ship, guest_data)
        self.do_aci_for_moci_rejected_guest(config, test_data, rest_ship, guest_data)
        self.get_document_to_be_updated_first_pass(config, test_data, rest_ship, guest_data)
        self.update_document_first_pass(config, test_data, rest_ship, guest_data)
        self.get_document_to_be_updated_second_pass(config, test_data, rest_ship, guest_data)
        self.update_document_second_pass(config, test_data, rest_ship, guest_data)
        self.get_final_updated_document(config, test_data, rest_ship, guest_data)
        self.verify_gangway_location(test_data, config, rest_ship)
        self.create_person_event_doc(config, test_data, couch, guest_data)

    def generate_sigup_email_id(self, test_data):
        """
        Function to generate random email id
        :param test_data:
        :return:
        """
        first_name = generate_first_name()
        last_name = generate_last_name()
        signup_email_id = generate_email_id(from_saved=True, first_name=first_name, last_name=last_name)
        test_data['signup_email_id'] = signup_email_id
