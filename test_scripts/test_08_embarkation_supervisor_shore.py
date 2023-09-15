__author__ = 'sarvesh.singh'

from virgin_utils import *
import pandas as pd
import json


@pytest.mark.SHORE
@pytest.mark.EMBARKATION_SUPERVISOR_SHORE
@pytest.mark.run(order=9)
class TestEmbarkationSupervisorShoreSide:
    """
    Test Suite to test Embarkation Supervisor Shore Side
    """

    @pytestrail.case(65132676)
    def test_01_login(self, config, rest_shore, creds):
        """
         Login to Embarkation Supervisor Shore side
        :param config:
        :param rest_shore:
        :param creds:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, "url.path.crewbff"), "crew-embarkation-admin/login")
        body = {
            "username": creds.visitormanagement.shore.login.username,
            "password": creds.visitormanagement.shore.login.password,
            "rememberMe": False,
            "appId": "0a21443d-210b-4b81-8b56-b497d369c0d0"
            }
        _content = rest_shore.send_request(method="POST", json=body, url=url, auth="basic").content
        is_key_there_in_dict('tokenDetail', _content)
        is_key_there_in_dict('accessToken', _content['tokenDetail'])
        is_key_there_in_dict('tokenType', _content['tokenDetail'])
        is_key_there_in_dict('userProfileDetail', _content)
        is_key_there_in_dict('appid', _content['tokenDetail'])
        assert _content['tokenDetail']['appid'] == body['appId'], "App ID mismatch !!"

    @pytestrail.case(14832074)
    def test_02_get_ship_date(self, config, test_data, rest_shore):
        """
        To get the current ship date
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['embarkSupervisorShore'] = dict()
        if config.envMasked == "CERT":
            test_data['embarkSupervisorShore']['reviewerTeamMemberId'] = "bd13947a-f4e4-4b65-90df-d2393b1eb477"
            test_data['embarkSupervisorShore']['reviewerEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShore']['reviewerName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShore']['submittedByEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShore']['submittedByName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShore']['submittedBy'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShore']['submittedByDesignation'] = ""
            test_data['embarkSupervisorShore']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
        else:
            test_data['embarkSupervisorShore']['reviewerTeamMemberId'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShore']['reviewerEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShore']['reviewerName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShore']['submittedByEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShore']['submittedByName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShore']['submittedBy'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShore']['submittedByDesignation'] = ""
            test_data['embarkSupervisorShore']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
        params = {"shipcode": config.ship.code}
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        test_data['embarkSupervisorShore']['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())
        test_data['embarkSupervisorShore']['shipDateTime'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800))
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            if voyage['isActive']:
                test_data['embarkSupervisorShore']['embarkDate'] = voyage['embarkDate'].split('T')[0]
                test_data['embarkSupervisorShore']['debarkDate'] = voyage['debarkDate'].split('T')[0]
                test_data['embarkSupervisorShore']['voyageId'] = voyage['voyageId']
                test_data['embarkSupervisorShore']['voyageNumber'] = voyage['number']
                test_data['embarkSupervisorShore']['shipCode'] = voyage['shipCode']
                break
        else:
            raise Exception("There's no active voyage in system !!")

    @pytestrail.case(14832075)
    def test_03_get_available_ships(self, config, rest_shore):
        """
        To verify the available ships
        :param config:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/ships')
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        if not any(d['shipCode'] == config.ship.code for d in _content):
            raise Exception(f'There is no ship available for {config.ship.code} in embarkation supervisor')
        for _ship in _content:
            is_key_there_in_dict('imageUrl', _ship)
            is_key_there_in_dict('brandCode', _ship)
            is_key_there_in_dict('shipCode', _ship)
            is_key_there_in_dict('shipName', _ship)
            is_key_there_in_dict('label', _ship)
            is_key_there_in_dict('value', _ship)

    @pytestrail.case(14846116)
    def test_04_get_master_data(self, config, rest_shore):
        """
        To get the master data
        :param config:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/masterdata')
        body = {"shipCode": config.ship.code}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('shipDetails', _content)
        is_key_there_in_dict('voyages', _content)
        is_key_there_in_dict('shipLocations', _content)
        is_key_there_in_dict('visitorBoardingStatuses', _content)
        is_key_there_in_dict('visitorTypes', _content)
        is_key_there_in_dict('visitorDepartments', _content)
        is_key_there_in_dict('alertTypes', _content)
        is_key_there_in_dict('departments', _content)
        is_key_there_in_dict('ports', _content)
        is_key_there_in_dict('documentTypes', _content)
        is_key_there_in_dict('shipTimes', _content)
        is_key_there_in_dict('personTypes', _content)
        is_key_there_in_dict('countries', _content)
        is_key_there_in_dict('loyaltyLevelTypes', _content)
        is_key_there_in_dict('visitPurposes', _content)
        is_key_there_in_dict('alertCodes', _content)
        is_key_there_in_dict('ipmDutyGroups', _content)
        is_key_there_in_dict('genders', _content)
        is_key_there_in_dict('reviewerList', _content)
        is_key_there_in_dict('specialNeeds', _content)
        is_key_there_in_dict('visitorRejectionReasons', _content)
        is_key_there_in_dict('gangwayLocations', _content)
        for country in _content['countries']:
            if len(country['value']) == 0:
                is_key_there_in_dict('name', _content['countries'])
                raise Exception("The name is missing in master data !!!")

    @pytestrail.case(14846117)
    def test_05_get_dashboard(self, config, test_data, rest_shore):
        """
        To get the dashboard data
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T19:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "voyageNumber": test_data['embarkSupervisorShore']['voyageNumber'],
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T19:00:01",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('teamMemberEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('alertDetail', _content['dashboard'])
        is_key_there_in_dict('messageDetail', _content['dashboard'])

    @pytestrail.case(681472)
    def test_06_create_visitor(self, config, test_data, rest_shore, guest_data):
        """
        Creating a Visitor by Crew
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 0
        test_data['embarkSupervisorShore']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShore']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        body = {
            "identifications": [
                {
                    "documentTypeCode": "P",
                    "number": test_data['embarkSupervisorShore']['employeeNumber']
                }
            ],
            "visits": [
                {
                    "needEscort": False,
                    "validForShip": config.ship.code,
                    "voyageNumber": test_data['embarkSupervisorShore']['voyageNumber'],
                    "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                    "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
                    "purpose": "Script Automation",
                    "boardingTypeCode": "GB",
                    "reviewerTeamMemberId": [
                        test_data['embarkSupervisorShore']['reviewerTeamMemberId']
                    ],
                    "reviewers": [
                        {
                            "reviewerTeamMemberId": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                            "reviewerEmail": test_data['embarkSupervisorShore']['reviewerEmail'],
                            "reviewerName": test_data['embarkSupervisorShore']['reviewerName']
                        }
                    ],
                    "submittedBy": test_data['embarkSupervisorShore']['submittedBy'],
                    "createdByUser": test_data['embarkSupervisorShore']['submittedBy'],
                    "assistance": []
                }
            ],
            "submittedBy": test_data['embarkSupervisorShore']['submittedBy'],
            "submittedByEmail": test_data['embarkSupervisorShore']['submittedByEmail'],
            "validForShip": config.ship.code,
            "submittedByName": test_data['embarkSupervisorShore']['submittedByName'],
            "submittedByDesignation": test_data['embarkSupervisorShore']['submittedByDesignation'],
            "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
            "genderCode": guest_data[guest]['GenderCode'][guest],
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
            "companyName": test_data['embarkSupervisorShore']['companyName'],
            "employeeNumber": test_data['embarkSupervisorShore']['employeeNumber'],
            "visitorTypeCode": "EB",
            "departmentId": test_data['embarkSupervisorShore']['departmentId'],
            "departmentPOC": "Test",
            "firstName": guest_data[guest]['FirstName'],
            "lastName": guest_data[guest]['LastName'],
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

    @pytestrail.case(14857183)
    def test_07_get_visitor(self, config, test_data, rest_shore):
        """
        Check if the visitor got created
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        test_data['embarkSupervisorShore']['availableVisitor'] = False
        params = {'page': 1, 'size': 99999}
        body = {"shipCode": config.ship.code,
                "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59"
                }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('visitors', _content['_embedded'])
        for _visitor in range(0, len(_content['_embedded']['visitors'])):
            is_key_there_in_dict('visits', _content['_embedded']['visitors'][_visitor])
            if 'employeeNumber' in _content['_embedded']['visitors'][_visitor]:
                if test_data['embarkSupervisorShore']['employeeNumber'] == _content['_embedded']['visitors'][_visitor][
                    'employeeNumber']:
                    test_data['embarkSupervisorShore']['visitorId'] = _content['_embedded']['visitors'][_visitor][
                        'visitorId']
            for visit in _content['_embedded']['visitors'][_visitor]['visits']:
                is_key_there_in_dict('visitReviewers', _content['_embedded']['visitors'][_visitor]['visits'][0])
                if len(visit['visitReviewers']) != 0:
                    is_key_there_in_dict('reviewerTeamMemberId',
                                         _content['_embedded']['visitors'][_visitor]['visits'][0]['visitReviewers'][0])
                    if test_data['embarkSupervisorShore']['reviewerTeamMemberId'] == visit['reviewerTeamMemberId']:
                        test_data['embarkSupervisorShore']['availableVisitor'] = True
                        break
                else:
                    raise Exception("Visitor Reviewer Team Members Id more then 1")
            else:
                continue

        if not test_data['embarkSupervisorShore']['availableVisitor']:
            raise Exception('created reviewerTeamMemberId is not available in the list of visitor reviewerTeamMemberId')

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(5079336)
    def test_08_get_visitor_shore_ship_core(self, config, test_data, rest_shore):
        """
        Check if the visitor is synced to shore and ship core
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"/visitors/{test_data['embarkSupervisorShore']['visitorId']}")
        _content_shore = rest_shore.send_request(method="GET", url=url, auth="user").content
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'),
                      f"/visitors/{test_data['embarkSupervisorShore']['visitorId']}")
        _content_ship = rest_shore.send_request(method="GET", url=url, auth="user").content
        compare_ship_shore_data(_content_shore, _content_ship)

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(5079337)
    def test_09_validate_visitor_data_in_ship_couch(self, config, request, test_data, rest_ship):
        """
        Check Visitor Data in ship couch
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/visitor_data_ship_couch.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        ship_url = f"{config.ship.sync}/VisitorStatus::{test_data['embarkSupervisorShore']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        # Check all keys are there in received document.
        for _key1 in _ship_data:
            is_key_there_in_dict(_key1, _content)
            for _key2 in _ship_data['Visits'][0]:
                is_key_there_in_dict(_key2, _content['Visits'][0])
                for _key3 in _content['Visits'][0]['VisitReviewers'][0]:
                    is_key_there_in_dict(_key3, _ship_data['Visits'][0]['VisitReviewers'][0])

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(26111994)
    def test_10_validate_visitor_personal_data_in_ship_couch(self, config, test_data, rest_ship, guest_data):
        """
        Check Visitor Personal Information Data in ship couch
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        ship_url = f"{config.ship.sync}/VisitorPersonalInformation::{test_data['embarkSupervisorShore']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        assert _content['FirstName'] == guest['firstName'], "ERROR: FirstName Mismatch !!"
        assert _content['LastName'] == guest['lastName'], "ERROR: LastName Mismatch !!"
        assert _content['Gender'] == guest['genderCode'][0].upper(), "ERROR: Gender Mismatch !!"
        assert _content['Identifications'][0]['DocumentTypeCode'] == 'P', "ERROR: DocumentTypeCode Mismatch !!"

    @pytestrail.case(14859397)
    def test_11_visitor_detail(self, config, test_data, rest_shore, guest_data):
        """
        Go to the visitor detail page
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 0
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShore']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        is_key_there_in_dict('visits', _content)
        is_key_there_in_dict('identifications', _content)
        is_key_there_in_dict('alerts', _content)
        is_key_there_in_dict('messages', _content)
        test_data['embarkSupervisorShore']['personId'] = _content['personId']
        for _identity in _content['identifications']:
            test_data['embarkSupervisorShore']['identificationId'] = _identity['identificationId']
        for _visit in _content['visits']:
            test_data['embarkSupervisorShore']['visitId'] = _visit['visitId']
            test_data['embarkSupervisorShore']['visitReviewerId'] = _visit['visitReviewerId']
            test_data['embarkSupervisorShore']['reviewerTeamMemberId'] = _visit['reviewerTeamMemberId']
            test_data['embarkSupervisorShore']['visitorId'] = _visit['visitorId']
        assert _content['lastName'] == guest_data[guest]['LastName'], "lastName Mismatch !!"
        assert _content['firstName'] == guest_data[guest]['FirstName'], "firstName Mismatch !!"
        assert _content['departmentId'] == test_data['embarkSupervisorShore'][
            'departmentId'], "departmentId Mismatch !!"

    @pytestrail.case(14859398)
    def test_12_edit_visitor(self, config, test_data, rest_shore, guest_data):
        """
        Edit the created Visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 1
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        body = {
            "isDeleted": False,
            "lastName": guest_data[guest]['LastName'],
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00",
            "genderCode": guest_data[guest]['GenderCode'][0],
            "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
            "departmentPOC": "Test",
            "firstName": guest_data[guest]['FirstName'],
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "departmentId": test_data['embarkSupervisorShore']['departmentId'],
            "visits": [
            ],
            "companyName": test_data['embarkSupervisorShore']['companyName'],
            "employeeNumber": test_data['embarkSupervisorShore']['employeeNumber'],
            "visitorTypeCode": "EB",
            "identifications": [
                {
                    "isDeleted": False,
                    "number": test_data['embarkSupervisorShore']['employeeNumber'],
                    "documentTypeCode": "P",
                    "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                    "identificationId": test_data['embarkSupervisorShore']['identificationId']
                }],
            "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
            "visitorId": test_data['embarkSupervisorShore']['visitorId'],
            "securityPhotoMediaItemId": "",
            "personId": test_data['embarkSupervisorShore']['personId'],
            "personTypeCode": "V",
            "age": 35,
            "alerts": [],
            "messages": [],
            "propertyId": config.ship.code,
            "validForShip": config.ship.code,
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
            "submittedBy": test_data['embarkSupervisorShore']['submittedBy'],
            "submittedByEmail": test_data['embarkSupervisorShore']['submittedByEmail'],
            "submittedByName": test_data['embarkSupervisorShore']['submittedByName'],
            "submittedByDesignation": test_data['embarkSupervisorShore']['submittedByDesignation'],
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

    @pytestrail.case(14859399)
    def test_13_visitor_detail_edit(self, config, test_data, rest_shore, guest_data):
        """
        Check the visitor detail after editing
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 1
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShore']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        assert _content['lastName'] == guest_data[guest]['LastName'], "lastName Mismatch !!"
        assert _content['firstName'] == guest_data[guest]['FirstName'], "firstName Mismatch !!"
        test_data['embarkSupervisorShore']['visitsBody'] = _content['visits']
        test_data['embarkSupervisorShore']['identificationBody'] = _content['identifications']
        test_data['embarkSupervisorShore']['visitorShore'] = _content

    @pytestrail.case(681470)
    def test_14_create_alert(self, config, test_data, rest_shore, guest_data):
        """
        Create alert for visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        # Search person in alert
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "crew-embarkation-admin/persons")
        params = {"page": 1}
        body = {"fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:00",
                "shipCode": config.ship.code,
                "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59"}
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict('currentPage', _content['page'])
        if _content['page']['currentPage'] != 1:
            raise Exception("Searching the  Wrong page !!!")
        guest = 1
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShore']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShore']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [
                {
                    "isDeleted": False,
                    "lastName": guest_data[guest]['LastName'],
                    "birthDate": guest_data[guest]['birthDate'],
                    "genderCode": guest_data[guest]['GenderCode'][0],
                    "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
                    "departmentPOC": "Test",
                    "firstName": guest_data[guest]['FirstName'],
                    "contactNumber": str(generate_phone_number(max_digits=10)),
                    "departmentId": test_data['embarkSupervisorShore']['departmentId'],
                    "visits": test_data['embarkSupervisorShore']['visitsBody'],
                    "companyName": test_data['embarkSupervisorShore']['companyName'],
                    "employeeNumber": test_data['embarkSupervisorShore']['employeeNumber'],
                    "visitorTypeCode": "EB",
                    "identifications": test_data['embarkSupervisorShore']['identificationBody'],
                    "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
                    "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                    "securityPhotoMediaItemId": "",
                    "personId": test_data['embarkSupervisorShore']['personId'],
                    "personTypeCode": "V",
                    "age": 35,
                    "alerts": [],
                    "messages": [],
                    "propertyId": config.ship.code,
                    "validForShip": config.ship.code,
                    "fullName": f"{guest_data[guest]['FirstName']} {guest_data[guest]['LastName']}"
                }
            ]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        test_data['embarkSupervisorShore']['alertResponse'] = _content
        test_data['embarkSupervisorShore']['alertResponseVisitorShore'] = _content

    @pytestrail.case(14937937)
    def test_15_verify_created_alert(self, config, test_data, rest_shore):
        """
        Check if the alert got created
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShore']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content['alerts']) == 0:
            raise Exception('Alert did not get created for the visitor')
        if not any(d['alertId'] == test_data['embarkSupervisorShore']['alertResponse']['alertId'] for d in
                   _content['alerts']):
            raise Exception('Alert did not get created for the visitor')

    @pytestrail.case(681471)
    def test_16_create_message(self, config, test_data, rest_shore, guest_data):
        """
        Create Message for visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        # Search person in message
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "crew-embarkation-admin/persons")
        params = {"page": 1}
        body = {"fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:00",
                "shipCode": config.ship.code,
                "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59"}
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict('currentPage', _content['page'])
        if _content['page']['currentPage'] != 1:
            raise Exception("Searching the  Wrong page !!!")
        guest = 1
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/messages")
        body = {
            "alertTypeCode": None,
            "departmentId": None,
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": False,
            "createdBy": test_data['embarkSupervisorShore']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [
                {
                    "isDeleted": False,
                    "lastName": guest_data[guest]['LastName'],
                    "birthDate": guest_data[guest]['birthDate'],
                    "genderCode": guest_data[guest]['GenderCode'][0],
                    "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
                    "departmentPOC": "Test",
                    "firstName": guest_data[guest]['FirstName'],
                    "contactNumber": str(generate_phone_number(max_digits=10)),
                    "departmentId": test_data['embarkSupervisorShore']['departmentId'],
                    "visits": test_data['embarkSupervisorShore']['visitsBody'],
                    "companyName": test_data['embarkSupervisorShore']['companyName'],
                    "employeeNumber": test_data['embarkSupervisorShore']['employeeNumber'],
                    "visitorTypeCode": "EB",
                    "identifications": test_data['embarkSupervisorShore']['identificationBody'],
                    "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
                    "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                    "securityPhotoMediaItemId": "",
                    "personId": test_data['embarkSupervisorShore']['personId'],
                    "personTypeCode": "V",
                    "age": 35,
                    "alerts": test_data['embarkSupervisorShore']['alertResponse'],
                    "messages": [],
                    "propertyId": config.ship.code,
                    "validForShip": config.ship.code,
                    "fullName": f"{guest_data[guest]['FirstName']} {guest_data[guest]['LastName']}"
                }
            ]
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('personMessages', _content)
        is_key_there_in_dict('personMessageCount', _content)
        test_data['embarkSupervisorShore']['messageResponse'] = _content
        test_data['embarkSupervisorShore']['messageResponseVisitorShore'] = _content

    @pytestrail.case(14954191)
    def test_17_verify_created_message(self, config, test_data, rest_shore):
        """
        Check if the message got created
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShore']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content['messages']) == 0:
            raise Exception('Message did not get created for the visitor')
        if not any(d['messageId'] == test_data['embarkSupervisorShore']['messageResponse']['messageId'] for d in
                   _content['messages']):
            raise Exception('Message did not get created for the visitor')

    @pytestrail.case(6740703)
    def test_18_approve_visit(self, config, test_data, rest_shore):
        """
        Approve the visit of visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShore']['visitsBody']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                            "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                            "statusCode": "approved",
                            "portCode": "ATSEA",
                            "boardingTypeCode": "GB",
                            "reviewerName": "Vertical QA",
                            "purpose": "Script Automation",
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": "1e41681f-b19e-4d89-ae12-89b688f8a137"
                        }
                    ]
                }
            ]
            _content = rest_shore.send_request(method="POST", params=params, url=url, json=body, auth="user").content

    @pytestrail.case(6740704)
    def test_19_reject_visit(self, config, test_data, rest_shore):
        """
        Reject the visit of visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShore']['visitsBody']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                    "reviewerName": "Vertical QA",
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": test_data['embarkSupervisorShore']['visitorId'],
                            "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                            "statusCode": "rejected",
                            "portCode": "CCC",
                            "boardingTypeCode": "EB",
                            "reviewerName": "Vertical QA",
                            "purpose": "general purpose",
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": "53952924-fad5-4a02-813b-150900b8c981",
                            "visitReviewerId": "3787d305-84c4-4d44-bc56-fe8c80bfd673",
                            "isDeleted": False
                        }
                    ]
                }
            ]
            _content = rest_shore.send_request(method="POST", params=params, url=url, json=body, auth="user").content

    @pytestrail.case(14956405)
    def test_20_export_visitors(self, config, test_data, rest_shore):
        """
        Export visitors
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'size': '999999'
        }
        body = {
            "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "reviewerTeamMemberIds": [test_data['embarkSupervisorShore']['reviewerTeamMemberId']],
            "shipCode": config.ship.code,
            "visitWiseVisitor": True
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        for _visitor in _content['_embedded']['visitors']:
            is_key_there_in_dict('firstName', _visitor)
            is_key_there_in_dict('lastName', _visitor)
            is_key_there_in_dict('genderCode', _visitor)
            is_key_there_in_dict('visitorId', _visitor)
            is_key_there_in_dict('visitorTypeCode', _visitor)
            is_key_there_in_dict('visitorDepartmentId', _visitor)
            is_key_there_in_dict('visits', _visitor)
            is_key_there_in_dict('identifications', _visitor)

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(14958620)
    def test_21_search_visitor(self, config, test_data, rest_shore, guest_data):
        """
        Import visitors
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 1
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/search")
        params = {
            'q': guest_data[guest]['FirstName'],
            'voyagenumber': test_data['embarkSupervisorShore']['voyageNumber'],
            "shipCode": config.ship.code,
            "isCrew": "true",
            "isGuest": "true",
            "isVisitor": "true"
        }
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        if len(_content) == 0:
            raise Exception('The created visitor is not shown in global search')
        for visitor in _content['visitors']:
            if visitor['firstName'] == guest_data[guest]['FirstName']:
                break
        else:
            raise Exception('The created visitor is not shown in global search')

    @pytestrail.case(9079229)
    def test_22_verify_exception_report(self, config, test_data, rest_shore):
        """
        Verify exception report
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway-reports/exception")
        params = {
            'page': '1'
        }
        body = {
            "reportType": "exception",
            "exceptions": [
                "MISSING-PICTURE"
            ],
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])

    @pytestrail.case(9079228)
    def test_23_verify_movement_report(self, config, test_data, rest_shore):
        """
        Verify movement report
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway-reports/movement")
        params = {
            'page': '1'
        }
        body = {
            "reportType": "movement",
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "movementActivityFrom": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "movementActivityTo": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('movements', _content['_embedded'])

    @pytestrail.case(9079230)
    def test_24_verify_location_report(self, config, test_data, rest_shore):
        """
        Verify location report
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway-reports/location")
        params = {
            'page': '1'
        }
        body = {
            "reportType": "location",
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "movementActivityFrom": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "movementActivityTo": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('locations', _content['_embedded'])

    @pytestrail.case(29563511)
    def test_25_cbp_reports(self, config, test_data, rest_shore):
        """
        Verify cbp reports
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway-reports/cbp-summary/v1")
        params = {
            'page': '1'
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "personTypeCode": "C",
            "reportType": "cbp"
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('cbpSummary', _content['_embedded'])

    @pytestrail.case(29563512)
    def test_26_ipm_reports(self, config, test_data, rest_shore):
        """
        Verify Ipm reports
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway-reports/in-port-manning")
        params = {
            'page': '1'
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
            "reportType": "ipm",
            "safetyPositionAssigned": True
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('inPortMannings', _content['_embedded'])

    @pytestrail.case(14956406)
    def test_27_import_visitors(self, config, test_data, rest_shore):
        """
        Import visitors
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        datetime_obj = datetime.strptime(test_data['embarkSupervisorShore']['shipDate'], '%Y-%m-%d').date()
        _filePath = f"{os.getcwd()}/test_data/visitor.xlsx"
        df = pd.DataFrame(
            {'First Name': [generate_first_name()], 'Last Name': [generate_last_name()], 'Citizenship': ['India'],
             'Gender': ['Male'], 'Date Of Birth': ['01/01/1975'], 'Contact No.': ['343433434'], 'Company Name': ['VV'],
             'Employee Number': [generate_document_number()], 'Department': ['Deck'],
             'Visitor Notes': ['Uploaded via bulk upload'],
             'Visitor Type': ['Vendor or Contractor'], 'Visit Purpose': ['Decor Install'],
             'Boarding Type': ['General Boarding'],
             'Visit Date': datetime_obj, 'License Plate Number': [''],
             'ID Type': ['Passport'],
             'ID Number': [generate_document_number()],
             'Department POC': ['john']})
        df.to_excel(_filePath, index=False)
        _dateTime = test_data['embarkSupervisorShore']['shipDateTime'].split(" ")
        _shipDateTime = f"{_dateTime[0]}T{_dateTime[1]}"
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/gangway/visitors/import/v1")
        params = {"reviewerteammemberid": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                  "submittedbyid": test_data['embarkSupervisorShore']['submittedBy'], "shipcode": config.ship.code,
                  "shiptime": _shipDateTime, "autoApprove": False}
        rest_shore.session.headers.update({'Content-Type': 'multipart/form-data'})
        _file = open(_filePath, 'rb')
        body = {"file": _file}
        _content = rest_shore.send_request(method="POST", url=url, files=body, params=params, auth="user").content
        is_key_there_in_dict('fileDownloadURL', _content)
        is_key_there_in_dict('lastStatus', _content)
        is_key_there_in_dict('success', _content)
        is_key_there_in_dict('totalRecords', _content)
        is_key_there_in_dict('visitorImportReq', _content)
        assert _content['success'], "visitor import failed!!"
        test_data['embarkSupervisorShore']['bulkImportResponse'] = _content['visitorImportReq'][0]
        for _visitor in _content['visitorImportReq']:
            if _visitor['status'] != 'Added':
                raise Exception('Visitor did not get Added')

    @pytestrail.case(41413326)
    def test_28_import_status(self, rest_shore, config):
        """
        Verify Import Status
        :param config:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/visitors/importstatus")
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('createdByUser', _content)
        is_key_there_in_dict('creationTime', _content)
        is_key_there_in_dict('expiryTime', _content)
        is_key_there_in_dict('fileDownloadURL', _content)
        is_key_there_in_dict('fileName', _content)
        is_key_there_in_dict('isDeleted', _content)
        is_key_there_in_dict('mediaItemId', _content)
        is_key_there_in_dict('modificationTime', _content)
        is_key_there_in_dict('modifiedByUser', _content)
        is_key_there_in_dict('reviewer', _content)
        is_key_there_in_dict('status', _content)
        is_key_there_in_dict('visitorImportInfoId', _content)
        assert _content['status'] == 'success', "visitor import failed!!"

    @pytestrail.case(6740709)
    def test_29_bulk_approve(self, config, test_data, rest_shore):
        """
        Bulk approve the imported visitors
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {"bulkApproval": True}
        datetime_obj = datetime.strptime(test_data['embarkSupervisorShore']['shipDate'], '%Y-%m-%d').date()
        _startDate = f"{datetime_obj}T00:00:01"
        body = [{"visitorId": test_data['embarkSupervisorShore']['bulkImportResponse']['visitorId'], "visits": [
            {"visitId": test_data['embarkSupervisorShore']['bulkImportResponse']['visitId'],
             "visitorId": test_data['embarkSupervisorShore']['bulkImportResponse']['visitorId'],
             "startDate": _startDate, "statusCode": "approved",
             "portCode": test_data['embarkSupervisorShore']['bulkImportResponse']['portCode'], "boardingTypeCode": "GB",
             "reviewerName": test_data['embarkSupervisorShore']['reviewerName'],
             "purpose": test_data['embarkSupervisorShore']['bulkImportResponse']['visitPurpose'],
             "propertyId": config.ship.code,
             "reviewerTeamMemberId": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
             "reviewerEmail": test_data['embarkSupervisorShore']['reviewerEmail'],
             "submittedBy": test_data['embarkSupervisorShore']['submittedBy']}]}]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="user").content
        if len(_content) != 0:
            for _visitor in _content:
                for _visit in _visitor['visits']:
                    if _visit['statusCode'] != 'approved':
                        raise Exception('The visit for the visitor did not get approved')
        else:
            raise Exception("No visitor Approved!!")

    @pytestrail.case(34403885)
    def test_30_visitor_image_not_disappear(self, config, test_data, rest_shore, guest_data):
        """
        Visitor image should not disappear if visits added through bulk import.
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        guest = 1
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        visitor_data = test_data['embarkSupervisorShore']['bulkImportResponse']
        body = {
            "isDeleted": False,
            "lastName": visitor_data['lastName'],
            "birthDate": f"{visitor_data['birthDate']}T00:00:00",
            "citizenShipCountryCode": "IN",
            "genderCode": "M",
            "departmentPOC": visitor_data["departmentPOC"],
            "firstName": visitor_data['firstName'],
            "contactNumber": visitor_data['phone'],
            "departmentId": test_data['embarkSupervisorShore']['departmentId'],
            "visits": [
            ],
            "companyName": visitor_data['companyName'],
            "employeeNumber": visitor_data['employeeNumber'],
            "visitorTypeCode": "VC",
            "identifications": [
                {
                    "isDeleted": False,
                    "number": visitor_data['idNumber'],
                    "documentTypeCode": "P",
                    "visitorId": visitor_data['visitorId'],
                    "identificationId": visitor_data['identificationId']
                }],
            "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
            "visitorId": visitor_data['visitorId'],
            "securityPhotoMediaItemId": "",
            "personId": visitor_data['identificationId'],
            "personTypeCode": "V",
            "age": 35,
            "alerts": [],
            "messages": [],
            "propertyId": config.ship.code,
            "validForShip": config.ship.code,
            "dateOfBirth": f"{visitor_data['birthDate']}T18:30:00.000Z",
            "submittedBy": visitor_data['submittedBy'],
            "submittedByEmail": test_data['embarkSupervisorShore']['submittedByEmail'],
            "submittedByName": test_data['embarkSupervisorShore']['submittedByName'],
            "submittedByDesignation": test_data['embarkSupervisorShore']['submittedByDesignation'],
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content

        _filePath = f"{os.getcwd()}/test_data/visitor.xlsx"
        df = pd.read_excel(_filePath)
        datetime_obj = datetime.strptime(test_data['embarkSupervisorShore']['shipDate'], '%Y-%m-%d').date()
        df['Visit Date'] = datetime_obj + timedelta(days=1)
        df.to_excel(_filePath, index=False)
        _dateTime = test_data['embarkSupervisorShore']['shipDateTime'].split(" ")
        _shipDateTime = f"{_dateTime[0]}T{_dateTime[1]}"
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/gangway/visitors/import/v1")
        params = {"reviewerteammemberid": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                  "submittedbyid": test_data['embarkSupervisorShore']['submittedBy'], "shipcode": config.ship.code,
                  "shiptime": _shipDateTime, "autoApprove": False}
        rest_shore.session.headers.update({'Content-Type': 'multipart/form-data'})
        _file = open(_filePath, 'rb')
        body = {"file": _file}
        _content = rest_shore.send_request(method="POST", url=url, files=body, params=params, auth="user").content
        assert _content['success'], "Importing new visit failed!!"
        to_url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'),
                         f"crew-embarkation-admin/visitor/{visitor_data['visitorId']}")
        to_params = {'shipTime': f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01", 'shipCode': 'SC'}
        to_content = rest_shore.send_request(url=to_url, method='GET', params=to_params, auth='user').content
        is_key_there_in_dict('profileImageUrl', to_content)
        is_key_there_in_dict('visits', to_content)
        assert to_content[
                   'profileImageUrl'] != "", "Visitor image got disappeared after adding multiple visits through" \
                                             " bulk import for this visitor."
        assert to_content['profileImageUrl'] == guest_data[guest][
            'ProfilePhotoUrl'], "Profile photo is not matching with the uploaded one"
        assert len(to_content['visits']) >= 1, "After uploading multiple visits one of the visits is getting remove."

    @pytestrail.case(40881810)
    def test_31_search_boarding_slots(self, config, test_data, rest_shore):
        """
        Search boarding slots
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id']
        }
        _content = rest_shore.send_request(method="POST", url=url, params=params, auth="crew").content

        if len(_content) == 0:
            raise Exception('No boarding slots are available')
        test_data['embarkationSupervisor']['boarding_slot'] = _content[len(_content)-1]
        test_data['embarkationSupervisor']['boardingSlotStartTime'] = _content[len(_content)-1]['boardingSlotStartTime']
        test_data['embarkationSupervisor']['boardingSlotEndTime'] = _content[len(_content)-1]['boardingSlotEndTime']
        test_data['embarkationSupervisor']['boardingNumber'] = _content[len(_content)-1]['boardingNumber']
        test_data['embarkationSupervisor']['slotNumber'] = _content[len(_content)-1]['slotNumber']
        test_data['embarkationSupervisor']['expectedGuestCount'] = _content[len(_content)-1]['expectedGuestCount']

        test_data['embarkationSupervisor']['oldboardingSlotStartTime'] = test_data['embarkationSupervisor']['boardingSlotEndTime']
        h, m, s = test_data['embarkationSupervisor']['boardingSlotEndTime'].split(":")
        test_data['embarkationSupervisor']['oldboardingSlotEndTime'] = f"{h}:{int(m)+15}:{s}"

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(36588305)
    def test_32_move_boarding_slot(self, config, test_data, rest_shore, db_core):
        """
        Move boarding slot
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
            "isMovingSlots": True
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['oldboardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['oldboardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "assignedGuestCount": 0,
            "checkedInGuestCount": 0,
            "onBoardedGuestCount": 0,
            "isEnabled": True,
            "isDeleted": False,
            "isActive": False,
            "isReserved": False,
            "oldBoardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "oldBoardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime']
        }]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)


        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(64537059)
    def test_33_update_capacity_boarding_slot(self, config, test_data, rest_shore, db_core):
        """
        Update boarding slot capacity
        :param config:
        :param test_data:
        :param rest_shore:
        :param db_core:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
                "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
                "shipcode": config.ship.code,
                "voyagenumber": test_data['voyage']['id'],
                "isMovingSlots": False
                 }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['oldboardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['oldboardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'] + 50,
            "isEnabled": True,
            "isDeleted": False,
            "isActive": False,
            "isReserved": False
        }]

        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('expectedGuestCount', _content[0])
            assert _content[0]['expectedGuestCount'] == test_data['embarkationSupervisor'][
                'expectedGuestCount'] + 50, "Boarding slot capacity not updated"
        else:
            raise Exception("Response is empty for updating slot capacity")
        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and"
                  f" voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break
        else:
            raise Exception("Can't find the updated boarding slot in the DB")

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(36588308)
    def test_34_disable_boarding_slot(self, config, test_data, rest_shore, db_core):
        """
        Disable boarding slot
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "assignedGuestCount": 0,
            "checkedInGuestCount": 0,
            "onBoardedGuestCount": 0,
            "isEnabled": False,
            "isDeleted": False,
            "isActive": False,
            "isReserved": False,
        }]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(36588307)
    def test_35_enable_boarding_slot(self, config, test_data, rest_shore, db_core):
        """
        Enable boarding slot
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "assignedGuestCount": 0,
            "checkedInGuestCount": 0,
            "onBoardedGuestCount": 0,
            "isEnabled": True,
            "isDeleted": False,
            "isActive": True,
            "isReserved": False
        }]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(36589191)
    def test_36_remove_slot(self, config, test_data, rest_shore, db_core):
        """
        Remove boarding slot
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
            "isMovingSlots": False
        }
        body = [{
            "assignedGuestCount": 0,
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "checkedInGuestCount": 0,
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isActive": False,
            "isDeleted": True,
            "isEnabled": False,
            "onBoardedGuestCount": 0,
            "shipCode": config.ship.code,
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "voyageNumber": test_data['voyage']['id']
        }]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(36588306)
    def test_37_add_boarding_slot(self, config, test_data, rest_shore, db_core):
        """
        Add boarding slot
        :param config:
        :param test_data:
        :param rest_shore:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyage']['id'],
            "effectiveFromDate": test_data['voyage']['startDate'],
            "effectiveToDate": test_data['voyage']['startDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isEnabled": True,
            "isDeleted": False,
            "isActive": False
        }]
        _content = rest_shore.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='{config.ship.code}' and voyagenumber ='{test_data['voyage']['id']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(65561132)
    def test_38_change_boarding_slot_for_sailor(self, config, test_data, rest_shore, guest_data):
        """
        Change boarding slot for sailor
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
        }
        _content = rest_shore.send_request(method="POST", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception('No boarding slots are available')
        boarding_slots = []
        for slot in _content:
            if slot['boardingNumber'] not in boarding_slots:
                boarding_slots.append(slot['boardingNumber'])

        guest = 0
        url_for_sailor = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                                 f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params_for_sailor = {
            'shipCode': config.ship.code
        }
        _content = rest_shore.send_request(method="GET", url=url_for_sailor, params=params_for_sailor, auth="crew"). \
            content
        if len(_content['boardingNumbers']) != 0 and 'boardingNumber' in _content['boardingNumbers'][0]:
            if _content['boardingNumbers'][0]['boardingNumber'] in boarding_slots:
                boarding_slots.remove(_content['boardingNumbers'][0]['boardingNumber'])

        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/slots')
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id'],
        }
        updated_boarding_slot = str(random.choice(boarding_slots))
        body = [
            {
                "reservationGuestId": guest_data[guest]['reservationGuestId'],
                "boardingNumber": updated_boarding_slot,
                "slotNumber": updated_boarding_slot,
                "shipCode": config.ship.code,
                "embarkDate": f"{test_data['voyage']['startDate']}T00:00:00",
                "guestId": guest_data[guest]['guestId'],
                "reservationId": guest_data[guest]['reservationId']
            }
        ]
        if len(_content['boardingNumbers']) != 0 and 'boardingNumber' in _content['boardingNumbers'][0]:
            body[0]["guestBoardingNumberId"] = _content['boardingNumbers'][0]['guestBoardingNumberId']
        rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="crew")
        _content = rest_shore.send_request(method="GET", url=url_for_sailor, params=params_for_sailor, auth="crew"). \
            content
        is_key_there_in_dict('boardingNumbers', _content)
        assert len(_content['boardingNumbers']) != 0, "Boarding Numbers list is empty."
        for boarding_number in _content['boardingNumbers']:
            if boarding_number['guestId'] == body[0]['guestId']:
                assert boarding_number['boardingNumber'] == int(updated_boarding_slot), \
                    "Boarding number not updated for sailor"
                assert boarding_number['slotNumber'] == int(updated_boarding_slot), \
                    "Boarding slot not updated for sailor"
                break
        else:
            raise Exception("GuestId mismatch !!")

    @pytestrail.case(65561233)
    def test_39_verify_boarding_slot_appearing_for_upcoming_voyage(self, config, test_data, rest_ship):
        """
        To Verify user is able to see boarding slots for upcoming voyages at ship side
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['voyage']['startDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyage']['id']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for slot in _content:
                is_key_there_in_dict('boardingNumber', slot)
                is_key_there_in_dict('slotNumber', slot)
                is_key_there_in_dict('boardingSlotStartTime', slot)
                is_key_there_in_dict('boardingSlotEndTime', slot)
        else:
            raise Exception("No boarding slots are available for future voyage")

    @pytestrail.case(65658213)
    def test_40_create_visit_for_same_day_on_different_ships(self, config, test_data, guest_data, rest_shore):
        """
        Create same day visits on different ships for a visitor
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        multiple_ships = [config.ship.code, "VL"]
        multi_ship_voyage_number = dict()
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/masterdata')
        for ship in multiple_ships:
            body = {"shipCode": ship}
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
            for voyage in _content['voyages']:
                embark_date = datetime.strptime(voyage['embarkDate'][:-9], "%Y-%m-%d")
                debark_date = datetime.strptime(voyage['debarkDate'][:-9], "%Y-%m-%d")
                current_date = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d")
                if current_date >= embark_date:
                    if current_date <= debark_date:
                        multi_ship_voyage_number[ship] = dict()
                        multi_ship_voyage_number[ship]['voyage_number'] = voyage['value']
                        break
                else:
                    continue
            else:
                raise Exception("No active voyage found")
        guest = 0
        test_data['embarkSupervisorShore']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShore']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        for ship in multiple_ships:
            body = {
                "identifications": [
                    {
                        "documentTypeCode": "P",
                        "number": test_data['embarkSupervisorShore']['employeeNumber']
                    }
                ],
                "visits": [
                    {
                        "needEscort": False,
                        "validForShip": ship,
                        "voyageNumber": multi_ship_voyage_number[ship]['voyage_number'],
                        "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                        "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59",
                        "purpose": "Script Automation",
                        "boardingTypeCode": "GB",
                        "reviewerTeamMemberId": [
                            test_data['embarkSupervisorShore']['reviewerTeamMemberId']
                        ],
                        "reviewers": [
                            {
                                "reviewerTeamMemberId": test_data['embarkSupervisorShore']['reviewerTeamMemberId'],
                                "reviewerEmail": test_data['embarkSupervisorShore']['reviewerEmail'],
                                "reviewerName": test_data['embarkSupervisorShore']['reviewerName']
                            }
                        ],
                        "submittedBy": test_data['embarkSupervisorShore']['submittedBy'],
                        "createdByUser": test_data['embarkSupervisorShore']['submittedBy'],
                        "assistance": []
                    }
                ],
                "submittedBy": test_data['embarkSupervisorShore']['submittedBy'],
                "submittedByEmail": test_data['embarkSupervisorShore']['submittedByEmail'],
                "validForShip": ship,
                "submittedByName": test_data['embarkSupervisorShore']['submittedByName'],
                "submittedByDesignation": test_data['embarkSupervisorShore']['submittedByDesignation'],
                "profileImageUrl": guest_data[guest]['ProfilePhotoUrl'],
                "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
                "genderCode": guest_data[guest]['GenderCode'][guest],
                "contactNumber": str(generate_phone_number(max_digits=10)),
                "citizenShipCountryCode": guest_data[guest]['CitizenshipCountryCode'],
                "companyName": test_data['embarkSupervisorShore']['companyName'],
                "employeeNumber": test_data['embarkSupervisorShore']['employeeNumber'],
                "visitorTypeCode": "EB",
                "departmentId": test_data['embarkSupervisorShore']['departmentId'],
                "departmentPOC": "Test",
                "firstName": guest_data[guest]['FirstName'],
                "lastName": guest_data[guest]['LastName'],
                "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
            }
            rest_shore.send_request(method="POST", url=url, json=body, auth="user")
        url = urljoin(getattr(config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        test_data['embarkSupervisorShore']['availableVisitor'] = False
        params = {
            'page': 1,
            'size': 99999
        }
        body = {
                "shipCode": config.ship.code,
                "startDate": f"{test_data['embarkSupervisorShore']['shipDate']}T00:00:01",
                "endDate": f"{test_data['embarkSupervisorShore']['shipDate']}T23:59:59"
                }
        _content = rest_shore.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('visitors', _content['_embedded'])
        for _visitor in _content['_embedded']['visitors']:
            is_key_there_in_dict('visits', _visitor)
            if 'employeeNumber' in _visitor:
                if test_data['embarkSupervisorShore']['employeeNumber'] == _visitor['employeeNumber']:
                    assert len(_visitor["visits"]) == len(multiple_ships), "No. of visits created is not " \
                                                                           "matching with no. of multiple ships"
                    for visit in _visitor["visits"]:
                        if visit['propertyId'] in multiple_ships:
                            assert visit['purpose'] == 'Script Automation', f"Visit purpose not matching for " \
                                                                    f"visit created for {visit['propertyId']} ship"
                        else:
                            raise Exception(f"{visit['propertyId']} not found in multiple ships.")
                    break
        else:
            raise Exception(f"Can not find the visitor having employeee "
                            f"number {test_data['embarkSupervisorShore']['employeeNumber']}")