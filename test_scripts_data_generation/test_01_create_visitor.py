__author__ = 'sarvesh.singh'

from virgin_utils import *
import dateutil.parser


@pytest.mark.VISITORS
@pytest.mark.run(order=1)
class TestVisitorCreation:
    """
    Test Suite to generate bulk Visitors
    """

    @pytestrail.case(26133578)
    def test_01_login(self, config, test_data, rest_shore, guest_data, creds):
        """
        Embarkation Supervisor Crew login
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        test_data['embarkSupervisorShip'] = dict()
        test_data['embarkSupervisorShip']['appId'] = str(generate_guid()).upper()
        test_data['embarkSupervisorShip']['deviceId'] = str(generate_random_alpha_numeric_string(length=32)).lower()
        if config.envMasked == "INTEGRATION":
            test_data['userName'] = creds.verticalqa.username
            test_data['password'] = creds.verticalqa.password
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = "995855bc-02fc-476d-9a20-c924303cb0b6"
            test_data['embarkSupervisorShip']['reviewerEmail'] = "Surbhi.jain@decurtis.com"
            test_data['embarkSupervisorShip']['reviewerName'] = "I Gede Anjaya"
            test_data['embarkSupervisorShip']['submittedBy'] = "995855bc-02fc-476d-9a20-c924303cb0b6"
            test_data['embarkSupervisorShip']['submittedByEmail'] = "Surbhi.jain@decurtis.com"
            test_data['embarkSupervisorShip']['submittedByName'] = "Surbhi Jain"
            test_data['embarkSupervisorShip']['submittedBy'] = "995855bc-02fc-476d-9a20-c924303cb0b6"
            test_data['embarkSupervisorShip']['submittedByDesignation'] = "Terminal Manager"
            test_data['embarkSupervisorShip']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
        else:
            test_data['userName'] = "paola.ortiz"
            test_data['password'] = "1234"
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = "796e5a00-1011-440b-8c8d-a10967b9691d"
            test_data['embarkSupervisorShip']['reviewerEmail'] = "crewvxptesting@virginvoyages.com"
            test_data['embarkSupervisorShip']['reviewerName'] = "Paula Ortiz"
            test_data['embarkSupervisorShip']['submittedBy'] = "796e5a00-1011-440b-8c8d-a10967b9691d"
            test_data['embarkSupervisorShip']['submittedByEmail'] = "crewvxptesting@virginvoyages.com"
            test_data['embarkSupervisorShip']['submittedByName'] = "paola ortiz"
            test_data['embarkSupervisorShip']['submittedBy'] = "796e5a00-1011-440b-8c8d-a10967b9691d"
            test_data['embarkSupervisorShip']['submittedByDesignation'] = "Terminal Manager"
            test_data['embarkSupervisorShip']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/login")
        body = {
            "username": test_data['userName'],
            "password": test_data['password'],
            "appId": test_data['embarkSupervisorShip']['appId'],
            "deviceId": test_data['embarkSupervisorShip']['deviceId']
        }
        rest_shore.basicToken = "Basic MGEyMTQ0M2QtMjEwYi00YjgxLThiNTYtYjQ5N2QzNjljMGQwOnlsS21xbUtwcWlCZXRSaEc="
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="Basic").content
        is_key_there_in_dict('accessToken', _content['tokenDetail'])
        _token = _content['tokenDetail']['accessToken']
        rest_shore.userToken = f"bearer {_token}"

        for count, guest in enumerate(guest_data):
            first_name = guest['FirstName']
            last_name = guest['LastName']
            email_id = guest['Email']
            birth_date = guest['BirthDate']
            gender = guest['GenderCode'][0]

            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()

            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
            params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
            files = {"file": open(profile_photo, "rb")}
            _content = \
                rest_shore.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
                    "Location"]
            time.sleep(0.1)
            guest_data[count]['ProfilePhotoUrl'] = _content
            break

    @pytestrail.case(26133579)
    def test_02_get_ship_date(self, config, test_data, rest_shore):
        """
        To get the current ship date
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        params = {"shipcode": config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        test_data['embarkSupervisorShip']['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())

        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            test_data['embarkSupervisorShip']['embarkDate'] = voyage['embarkDate'].split('T')[0]
            test_data['embarkSupervisorShip']['debarkDate'] = voyage['debarkDate'].split('T')[0]
            test_data['embarkSupervisorShip']['voyageId'] = voyage['voyageId']
            test_data['embarkSupervisorShip']['voyageNumber'] = voyage['number']
            test_data['embarkSupervisorShip']['shipCode'] = voyage['shipCode']
            break
        else:
            raise Exception("There's no active voyage in system !!")

    @pytestrail.case(16310740)
    def test_03_create_visitor(self, config, test_data, rest_shore, guest_data):
        """
        Creating a Visitor by Crew
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 0
        test_data['embarkSupervisorShip']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShip']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
        difference = dateutil.parser.isoparse(
            test_data['embarkSupervisorShip']['debarkDate']) - dateutil.parser.isoparse(
            test_data['embarkSupervisorShip']['shipDate'])
        days = difference.days
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        body = {
            "identifications": [
                {
                    "documentTypeCode": "P",
                    "number": test_data['embarkSupervisorShip']['employeeNumber']
                }
            ],
            "visits": [
                {
                    "needEscort": False,
                    "validForShip": config.ship.code,
                    "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
                    "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                    "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
                    "purpose": "Script Automation",
                    "boardingTypeCode": "GB",
                    "reviewerTeamMemberId": [
                        test_data['embarkSupervisorShip']['reviewerTeamMemberId']
                    ],
                    "reviewers": [
                        {
                            "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                            "reviewerEmail": test_data['embarkSupervisorShip']['reviewerEmail'],
                            "reviewerName": test_data['embarkSupervisorShip']['reviewerName']
                        }
                    ],
                    "submittedBy": test_data['embarkSupervisorShip']['submittedBy'],
                    "createdByUser": test_data['embarkSupervisorShip']['submittedBy'],
                    "assistance": []
                }
            ],
            "submittedBy": test_data['embarkSupervisorShip']['submittedBy'],
            "submittedByEmail": test_data['embarkSupervisorShip']['submittedByEmail'],
            "validForShip": config.ship.code,
            "submittedByName": test_data['embarkSupervisorShip']['submittedByName'],
            "submittedByDesignation": test_data['embarkSupervisorShip']['submittedByDesignation'],
            "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
            "dateOfBirth": f"{guest_data[guest]['BirthDate']}T18:30:00.000Z",
            "genderCode": guest_data[guest]['GenderCode'][guest],
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
            "companyName": test_data['embarkSupervisorShip']['companyName'],
            "employeeNumber": test_data['embarkSupervisorShip']['employeeNumber'],
            "visitorTypeCode": "EB",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "departmentPOC": "Test",
            "firstName": guest_data[guest]['FirstName'],
            "lastName": guest_data[guest]['LastName'],
            "birthDate": f"{guest_data[guest]['BirthDate']}T00:00:00"
        }
        for i in range(1, days + 1):
            data = {
                "needEscort": False,
                "validForShip": config.ship.code,
                "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
                "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
                "purpose": "Script Automation",
                "boardingTypeCode": "GB",
                "reviewerTeamMemberId": [
                    test_data['embarkSupervisorShip']['reviewerTeamMemberId']
                ],
                "reviewers": [
                    {
                        "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                        "reviewerEmail": test_data['embarkSupervisorShip']['reviewerEmail'],
                        "reviewerName": test_data['embarkSupervisorShip']['reviewerName']
                    }
                ],
                "submittedBy": test_data['embarkSupervisorShip']['submittedBy'],
                "createdByUser": test_data['embarkSupervisorShip']['submittedBy'],
                "assistance": []
            }
            data['startDate'] = str(dateutil.parser.isoparse(data['startDate']) + timedelta(days=i)).replace(' ', 'T')
            data['endDate'] = str(dateutil.parser.isoparse(data['endDate']) + timedelta(days=i)).replace(' ', 'T')
            body['visits'].append(data)
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

    @retry_when_fails(retries=40, interval=5)
    @pytestrail.case(16378473)
    def test_04_get_visitor(self, config, test_data, rest_shore):
        """
        Check if the visitor got created
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {'size': '99999'}
        body = {"shipCode": config.ship.code, "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59"}
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        for _visitor in _content['_embedded']['visitors']:
            if 'employeeNumber' in _visitor:
                if _visitor['employeeNumber'] == test_data['embarkSupervisorShip']['employeeNumber']:
                    test_data['embarkSupervisorShip']['visitorId'] = _visitor['visitorId']
                    break
        if 'visitorId' not in test_data['embarkSupervisorShip']:
            raise Exception('Visitor did not get created at ship side')

    @pytestrail.case(16378474)
    def test_05_visitor_detail(self, config, test_data, rest_shore, guest_data):
        """
        Go to the visitor detail page
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 0
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShip']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('visits', _content)
        is_key_there_in_dict('identifications', _content)
        is_key_there_in_dict('alerts', _content)
        is_key_there_in_dict('messages', _content)
        test_data['embarkSupervisorShip']['personId'] = _content['personId']
        for _identity in _content['identifications']:
            test_data['embarkSupervisorShip']['identificationId'] = _identity['identificationId']
        test_data['embarkSupervisorShip']['visits'] = []
        for _visit in _content['visits']:
            test_data['embarkSupervisorShip']['visits'].append(_visit['visitId'])
            test_data['embarkSupervisorShip']['visitReviewerId'] = _visit['visitReviewerId']
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = _visit['reviewerTeamMemberId']
            test_data['embarkSupervisorShip']['visitorId'] = _visit['visitorId']
        assert _content['lastName'] == guest_data[guest]['LastName'], "lastName Mismatch !!"
        assert _content['firstName'] == guest_data[guest]['FirstName'], "firstName Mismatch !!"
        assert _content['departmentId'] == test_data['embarkSupervisorShip'][
            'departmentId'], "departmentId Mismatch !!"

    @pytestrail.case(16531917)
    def test_06_approve_visit(self, config, test_data, rest_shore):
        """
        Approve the visit of visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShip']['visits']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "visits": [
                        {
                            "visitId": _visits,
                            "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                            "statusCode": "approved",
                            "portCode": "ATSEA",
                            "boardingTypeCode": "GB",
                            "reviewerName": "Vertical QA",
                            "purpose": "Script Automation",
                            "propertyId": "SC",
                            "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": "1e41681f-b19e-4d89-ae12-89b688f8a137"
                        }
                    ]
                }
            ]
            _content = rest_shore.send_request(method="POST", params=params, url=url, json=body, auth="user").content

    @retry_when_fails(retries=40, interval=5)
    @pytestrail.case(26111995)
    def test_07_validate_visitor_data_in_ship_couch(self, config, test_data, rest_ship, couch):
        """
        Check Visitor Data in ship couch
        :param config:
        :param test_data:
        :param rest_ship:
        :param couch:
        :return:
        """
        test_data['creation'] = dict()
        params = {'shipcode': config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        ship_off_set = _content['shipOffset']
        epoch_time_stamp = _content['epocTimestamp']
        ship_off_set = ship_off_set * 60
        ship_time = (epoch_time_stamp + ship_off_set) * 1000
        test_data['creation']['boardingStatusDateEpoch'] = ship_time
        test_data['creation']['validationStatusDate'] = str(datetime.fromtimestamp(epoch_time_stamp)).replace(' ', 'T')

        url = urljoin(config.ship.sync, f"VisitorStatus::{test_data['embarkSupervisorShip']['visitorId']}")
        test_data['creation']['visitorStatus'] = couch.send_request(method="GET", url=url,
                                                                              auth="basic").content
        test_data['creation']['visitorStatus'] = couch.send_request(method="GET", url=url,
                                                                              auth="basic").content

    @pytestrail.case(96)
    def test_08_assign_rf_id(self, config, test_data, rest_ship, couch):
        """
        Assign rfid to Visitor
        :param test_data:
        :param rest_ship:
        :param couch:
        :return:
        """

        test_data['creation']['visitorStatus']["CheckInBy"] = "53952924-fad5-4a02-813b-150900b8c981"
        test_data['creation']['visitorStatus'][
            "CheckInStatusDate"] = f"{test_data['creation']['validationStatusDate']}+00:00"
        test_data['creation']['visitorStatus']["CheckInStatusDateEpoch"] = test_data['creation'][
            'boardingStatusDateEpoch']
        test_data['creation']['visitorStatus']["TerminalCheckinStatus"] = "COMPLETED"
        test_data['creation']['visitorStatus']['_rev'] = test_data['creation']['visitorStatus']['_rev']
        url = urljoin(config.ship.sync, f"VisitorStatus::{test_data['embarkSupervisorShip']['visitorId']}")
        _content = couch.send_request(method="PUT", url=url, json=test_data['creation']['visitorStatus'],
                                                auth="basic").content

        # Assign RFID
        url = urljoin(getattr(config.ship.contPath, 'url.path.hydration'), 'trackablehosts/bulk')
        rf_id = generate_guid()
        json = {
            "trackableHosts": [
                {
                    "hostId": test_data['embarkSupervisorShip']['visitorId'],
                    "hostIdType": "V",
                    "trackableAttributes": {
                        "rfId": rf_id
                    }
                }
            ]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=json, auth="crew").content
