__author__ = 'sarvesh.singh'

from virgin_utils import *
import pandas as pd


@pytest.mark.EMBARKATION_SUPERVISOR_SHIP
@pytest.mark.run(order=26)
class TestEmbarkationSupervisor:
    """
    Test Suite to test Embarkation Supervisor Ship Side
    """

    @pytestrail.case(26133578)
    def test_01_login(self, config, test_data, rest_ship, guest_data, creds):
        """
        Embarkation Supervisor Crew login
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :param creds:
        :return:
        """
        test_data['embarkSupervisorShip'] = dict()
        if config.envMasked == "INTEGRATION":
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShip']['reviewerEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShip']['reviewerName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShip']['submittedBy'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShip']['submittedByEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShip']['submittedByName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShip']['submittedBy'] = "9404e29c-32ed-4144-8a0a-3676ffa89115"
            test_data['embarkSupervisorShip']['submittedByDesignation'] = ""
            test_data['embarkSupervisorShip']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
            test_data['embarkSupervisorShip']['ipmDutyAssignmentId'] = '556b5ca3-569b-4844-b3d8-a4ba615de7b9'
            test_data['embarkSupervisorShip']['teamMemberId'] = '973193aa-50f8-4954-9ba3-593943a98429'
        else:
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = "b7f2fc66-ff3e-4548-9631-3a7f16a02476"
            test_data['embarkSupervisorShip']['reviewerEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShip']['reviewerName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShip']['submittedBy'] = "b7f2fc66-ff3e-4548-9631-3a7f16a02476"
            test_data['embarkSupervisorShip']['submittedByEmail'] = "vijay.tiwari@decurtis.com"
            test_data['embarkSupervisorShip']['submittedByName'] = "Vijay Tiwari"
            test_data['embarkSupervisorShip']['submittedBy'] = "b7f2fc66-ff3e-4548-9631-3a7f16a02476"
            test_data['embarkSupervisorShip']['submittedByDesignation'] = ""
            test_data['embarkSupervisorShip']['departmentId'] = "77538d48-c34c-11e9-844f-4201ac180006"
            test_data['embarkSupervisorShip']['ipmDutyAssignmentId'] = '556b5ca3-569b-4844-b3d8-a4ba615de7b9'
            test_data['embarkSupervisorShip']['teamMemberId'] = '973193aa-50f8-4954-9ba3-593943a98429'

        for count, guest in enumerate(guest_data):
            first_name = guest['FirstName']
            last_name = guest['LastName']
            email_id = guest['email']
            birth_date = guest['birthDate']
            gender = guest['GenderCode'][0]

            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()

            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
            params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
            files = {"file": open(profile_photo, "rb")}
            _content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="crew").headers[
                "location"]
            time.sleep(0.1)
            guest_data[count]['ProfilePhotoUrl'] = _content
            break
        url = urljoin(getattr(config.ship.contPath, "url.path.crewbff"), "crew-embarkation-admin/login")
        body = {
                "username": creds.visitormanagement.shore.login.username,
                "password": creds.visitormanagement.shore.login.password,
                "rememberMe": False,
                "appId": "0a21443d-210b-4b81-8b56-b497d369c0d0"
            }
        _content = rest_ship.send_request(method="POST", json=body, url=url, auth="basic").content
        is_key_there_in_dict('tokenDetail', _content)
        is_key_there_in_dict('accessToken', _content['tokenDetail'])
        is_key_there_in_dict('tokenType', _content['tokenDetail'])
        is_key_there_in_dict('userProfileDetail', _content)
        is_key_there_in_dict('appid', _content['tokenDetail'])
        assert _content['tokenDetail']['appid'] == body['appId'], "App ID mismatch !!"

    @pytestrail.case(26133579)
    def test_02_get_ship_date(self, config, test_data, rest_ship):
        """
        To get the current ship date
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"shipcode": config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['embarkSupervisorShip']['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())
        test_data['embarkSupervisorShip']['shipDateTime'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800))
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
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

    @pytestrail.case(15793374)
    def test_03_get_master_data(self, config, rest_ship):
        """
        To get the master data
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/masterdata')
        body = {"shipCode": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
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
                raise Exception(f"The name is missing  in master data !!!")

    @pytestrail.case(15795588)
    def test_04_get_dashboard(self, config, test_data, rest_ship):
        """
        To get the dashboard data
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T19:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T19:00:01",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('teamMemberEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('messageDetail', _content['dashboard'])
        is_key_there_in_dict('alertDetail', _content['dashboard'])

    @pytestrail.case(15795589)
    def test_05_get_broadcast_message(self, config, rest_ship):
        """
        To get broadcast message
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), '/gangway/broadcast/message')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('messages', _content['_embedded'])

    @pytestrail.case(15795590)
    def test_06_update_broadcast_message(self, config, test_data, rest_ship):
        """
        To update broadcast message
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), '/gangway/broadcast/message')
        body = [
            {
                "createdByUser": test_data['embarkSupervisorShip']['submittedBy'],
                "messageId": "0466a360-dbe8-4680-a088-16fb654defbc",
                "fromPersonTypeCode": "C",
                "fromPersonId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                "messageBody": "Script Automation",
                "messageType": "BC_LDR_MSG",
                "expiryDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59"
            }
        ]

        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _message in _content:
            is_key_there_in_dict('messageId', _message)
            is_key_there_in_dict('messageBody', _message)
            assert _message['messageBody'] == 'Script Automation', "messageBody Mismatch !!"

    @pytestrail.case(15924211)
    def test_07_sailors_landing(self, config, test_data, rest_ship):
        """
        To verify the landing call for Sailors
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/reservation-guests/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        for _guests in _content['reservationGuests']:
            is_key_there_in_dict('personId', _guests)
            is_key_there_in_dict('reservationGuestId', _guests)
            is_key_there_in_dict('reservationNumber', _guests)
            is_key_there_in_dict('boardingNumbers', _guests)
            is_key_there_in_dict('identifications', _guests)
            is_key_there_in_dict('embarkDate', _guests)
            is_key_there_in_dict('debarkDate', _guests)

    @pytestrail.case(15795591)
    def test_08_get_sailor_detail(self, config, test_data, rest_ship, guest_data):
        """
        To verify the sailor detail page
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict('personId', _content)
        is_key_there_in_dict('reservationGuestId', _content)
        is_key_there_in_dict('reservationNumber', _content)
        is_key_there_in_dict('alerts', _content)
        is_key_there_in_dict('messages', _content)
        is_key_there_in_dict('primaryDocuments', _content)
        is_key_there_in_dict('secondaryDocuments', _content)
        test_data['embarkSupervisorShip']['sailorDetail'] = _content

    @pytestrail.case(15812677)
    def test_09_create_message_sailor(self, config, test_data, rest_ship):
        """
        Create Message for Sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/messages")
        body = {
            "alertTypeCode": None,
            "departmentId": None,
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": False,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [test_data['embarkSupervisorShip']['sailorDetail']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('personMessages', _content)
        is_key_there_in_dict('personMessageCount', _content)
        test_data['embarkSupervisorShip']['messageResponse'] = _content

    @pytestrail.case(15817930)
    def test_10_verify_created_message(self, config, test_data, rest_ship, guest_data):
        """
        Check if the message got created for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['messages']) == 0:
            raise Exception('Message did not get created for the Sailor')
        if not any(d['messageId'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['messages']):
            raise Exception('Message did not created')

    @pytestrail.case(15899514)
    def test_11_create_alert_sailor(self, config, test_data, rest_ship):
        """
        Create alert for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [test_data['embarkSupervisorShip']['sailorDetail']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        test_data['embarkSupervisorShip']['alertResponse'] = _content

    @pytestrail.case(15901760)
    def test_12_verify_created_alert(self, config, test_data, rest_ship, guest_data):
        """
        Check if the alert got created for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['alerts']) == 0:
            raise Exception('Alert did not get created for the visitor')
        if not any(d['alertId'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['alerts']):
            raise Exception('Alert did not created')

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(67649486)
    def test_13_validate_sailor_alert_message_in_ship_couch(self, config, test_data, rest_ship, guest_data):
        """
        Check Sailor Alert and messages got synced to ship couch
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        ship_url = f"{config.ship.sync}/GuestPersonAlert::{guest_data[guest]['reservationGuestId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['AlertID'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['PersonAlerts']):
            raise Exception('Alert created for sailor is not synced to ship couch')

        ship_url = f"{config.ship.sync}/GuestMessage::{guest_data[guest]['reservationGuestId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['MessageID'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['Messages']):
            raise Exception('Message created for sailor is not synced to ship couch')

    @pytestrail.case(64694700)
    def test_14_edit_message_sailor(self, config, test_data, rest_ship, guest_data):
        """
         Edit message for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "personalerts/partialupdate")
        body = {"alertId": test_data['embarkSupervisorShip']['messageResponse']['messageId'],
                "description": "Validate MESSAGE edit for sailor",
                "dueDate": test_data['embarkSupervisorShip']['messageResponse']['startDate'],
                "expiryDate": test_data['embarkSupervisorShip']['messageResponse']['expiryDate'],
                "isOverridable": True,
                "isPriority": True,
                "isSoundEnabled": False}
        rest_ship.session.headers.update({'Accept': 'application/json'})
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        test_data['embarkSupervisorShip']['messageResponse']['description'] = body["description"]
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for message in _content['messages']:
            if message['messageId'] == test_data['embarkSupervisorShip']['messageResponse']['messageId']:
                assert message['description'] == test_data['embarkSupervisorShip']['messageResponse'][
                    'description'], "Message not edited for sailor."
                break
        else:
            raise Exception("Not able to find the MESSAGE for sailor.")

    @pytestrail.case(64694701)
    def test_15_edit_alert_sailor(self, config, rest_ship, guest_data, test_data):
        """
         Edit alert for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'),
                      f"alerts/{test_data['embarkSupervisorShip']['alertResponse']['alertId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "personalerts/partialupdate")
        body = {"alertId": _content['alertId'],
                "alertTypeCode": "DB",
                "departmentId": test_data['embarkSupervisorShip']['departmentId'],
                "teamMemberDepartmentId": _content['teamMemberDepartmentId'],
                "description": "Validate ALERT edit for sailor",
                "dueDate": _content['dueDate'],
                "expiryDate": _content['expiryDate'],
                "isOverridable": True,
                "isPriority": True,
                "isSoundEnabled": True}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        test_data['embarkSupervisorShip']['alertResponse']['description'] = body["description"]
        test_data['embarkSupervisorShip']['alertResponse']['alertTypeCode'] = body["alertTypeCode"]
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for alert in _content['alerts']:
            if alert['alertId'] == test_data['embarkSupervisorShip']['alertResponse']['alertId']:
                assert alert['description'] == test_data['embarkSupervisorShip']['alertResponse'][
                    'description'], "Description not edited for sailor."
                assert alert['alertTypeCode'] == test_data['embarkSupervisorShip']['alertResponse'][
                    'alertTypeCode'], "AlertType Code not edited for sailor."
                break
        else:
            raise Exception("Not able to find the ALERT for sailor.")

    @pytestrail.case(64694703)
    def test_16_remove_message_sailor(self, config, test_data, rest_ship, guest_data):
        """
        Remove message for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'),
                      f"alerts/{test_data['embarkSupervisorShip']['messageResponse']['messageId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        body = {"lastModifiedByUserId": _content['lastModifiedByUserId'],
                "lastModifiedByApplicationId": _content['lastModifiedByApplicationId'],
                "alertId": test_data['embarkSupervisorShip']['messageResponse']['messageId'],
                "fromPerson": "Vijay Tiwari",
                "description": _content['description'],
                "severity": _content['severity'],
                "personAlertCount": _content['personAlertCount'],
                "priority": _content['priority'],
                "dueDate": _content['dueDate'],
                "expiryDate": _content['expiryDate'],
                "isOverridable": _content['isOverridable'],
                "isSoundEnabled": _content['isSoundEnabled'],
                "isDeleted": _content['isDeleted'],
                "targetApplications": [],
                "personAlerts": [
                    {"lastModifiedByUserId": _content['personAlerts'][0]['lastModifiedByUserId'],
                     "lastModifiedByApplicationId": _content['personAlerts'][0]['lastModifiedByApplicationId'],
                     "personAlertId": _content['personAlerts'][0]['personAlertId'],
                     "personTypeCode": _content['personAlerts'][0]['personTypeCode'],
                     "personId": _content['personAlerts'][0]['personId'],
                     "propertyId": _content['personAlerts'][0]['propertyId'],
                     "isCleared": _content['personAlerts'][0]['isCleared'],
                     "isRead": _content['personAlerts'][0]['isRead'],
                     "isDeleted": True}
                ],
                "alertCreatedBy": _content['alertCreatedBy'],
                "addedDateOffset": 330,
                "source": _content['source'],
                "useBatch": _content['useBatch']}
        _content = rest_ship.send_request(method="PUT", json=body, url=url, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('personAlerts', _content)
        assert _content['personAlerts'][0]['isDeleted'], "Message not marked as Deleted for Sailor."
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if any(message['messageId'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for message in
               _content['messages']):
            raise Exception('Message not deleted for Salior.')

    @pytestrail.case(64694704)
    def test_17_remove_alert_sailor(self, config, test_data, rest_ship, guest_data):
        """
        Remove alert for Sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'),
                      f"alerts/{test_data['embarkSupervisorShip']['alertResponse']['alertId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        body = {"lastModifiedByUserId": _content['lastModifiedByUserId'],
                "lastModifiedByApplicationId": _content['lastModifiedByApplicationId'],
                "alertId": _content['alertId'],
                "teamMemberDepartmentId": _content['teamMemberDepartmentId'],
                "fromPerson": "Vijay Tiwari",
                "description": _content['description'],
                "severity": _content['severity'],
                "personAlertCount": _content['personAlertCount'],
                "priority": _content['priority'],
                "dueDate": _content['dueDate'],
                "expiryDate": _content['expiryDate'],
                "isOverridable": _content['isOverridable'],
                "isSoundEnabled": _content['isSoundEnabled'],
                "isDeleted": _content['isDeleted'],
                "alertTypeCode": _content['alertTypeCode'],
                "targetApplications": [],
                "personAlerts": [
                    {"lastModifiedByUserId": _content['personAlerts'][0]['lastModifiedByUserId'],
                     "lastModifiedByApplicationId": _content['personAlerts'][0]['lastModifiedByApplicationId'],
                     "personAlertId": _content['personAlerts'][0]['personAlertId'],
                     "personTypeCode": _content['personAlerts'][0]['personTypeCode'],
                     "personId": _content['personAlerts'][0]['personId'],
                     "propertyId": _content['personAlerts'][0]['propertyId'],
                     "isCleared": _content['personAlerts'][0]['isCleared'],
                     "isRead": _content['personAlerts'][0]['isRead'],
                     "isDeleted": True}
                ],
                "alertCreatedBy": _content['alertCreatedBy'],
                "addedDateOffset": 330,
                "source": _content['source'],
                "useBatch": _content['useBatch']}
        _content = rest_ship.send_request(method="PUT", json=body, url=url, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('personAlerts', _content)
        assert _content['personAlerts'][0]['isDeleted'], "Alert not marked as Deleted for Sailor."
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if any(alert['alertId'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for alert in
               _content['alerts']):
            raise Exception('Alert not deleted for Salior.')

    @pytestrail.case(15926457)
    def test_18_export_sailors(self, config, test_data, rest_ship):
        """
        Export sailors
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'size': '500'
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        for _guests in _content['reservationGuests']:
            is_key_there_in_dict('personId', _guests)
            is_key_there_in_dict('reservationGuestId', _guests)
            is_key_there_in_dict('reservationNumber', _guests)
            is_key_there_in_dict('boardingNumbers', _guests)
            is_key_there_in_dict('identifications', _guests)
            is_key_there_in_dict('embarkDate', _guests)
            is_key_there_in_dict('debarkDate', _guests)

    @pytestrail.case(16251184)
    def test_19_crew_landing(self, config, test_data, rest_ship):
        """
        To verify the landing call for Crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['embarkSupervisorShip']['crewData'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/team-members/search')
        params = {
            'page': 1,
            'sort': 'lastname, asc'
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content['teamMembers']) == 0:
            raise Exception('No crew member available in active voyage')
        for _crew in _content['teamMembers']:
            is_key_there_in_dict('personId', _crew)
            is_key_there_in_dict('teamMemberId', _crew)
            is_key_there_in_dict('teamMemberNumber', _crew)
            is_key_there_in_dict('identifications', _crew)
            test_data['embarkSupervisorShip']['crewData']['teamMemberNumber'] = _crew['teamMemberNumber']
            test_data['embarkSupervisorShip']['crewData']['firstName'] = _crew['firstName']
            test_data['embarkSupervisorShip']['crewData']['lastName'] = _crew['lastName']
            break
        random.shuffle(_content['teamMembers'])
        test_data['embarkSupervisorShip']['teamMemberId'] = _content['teamMembers'][0]['teamMemberId']

    @pytestrail.case(16260229)
    def test_20_get_crew_detail(self, config, test_data, rest_ship):
        """
        To verify the crew detail page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/crew/{test_data['embarkSupervisorShip']['teamMemberId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict('personId', _content)
        is_key_there_in_dict('teamMemberId', _content)
        is_key_there_in_dict('alerts', _content)
        is_key_there_in_dict('messages', _content)
        is_key_there_in_dict('identifications', _content)
        test_data['embarkSupervisorShip']['crewDetail'] = _content

    @pytestrail.case(16260230)
    def test_21_create_message_crew(self, config, test_data, rest_ship):
        """
        Create Message for Crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/messages")
        body = {
            "alertTypeCode": None,
            "departmentId": None,
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": False,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [test_data['embarkSupervisorShip']['crewDetail']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('personMessages', _content)
        is_key_there_in_dict('personMessageCount', _content)
        test_data['embarkSupervisorShip']['messageResponse'] = _content

    @pytestrail.case(16260231)
    def test_22_verify_created_message_crew(self, config, test_data, rest_ship):
        """
        Check if the message got created for crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/crew/{test_data['embarkSupervisorShip']['teamMemberId']}")
        params = {
            'shipCode': config.ship.code,
            'size': '9999'
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['messages']) == 0:
            raise Exception('Message did not get created for the Sailor')
        if not any(d['messageId'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['messages']):
            raise Exception('Message did not get created for crew')

    @pytestrail.case(16262874)
    def test_23_create_alert_crew(self, config, test_data, rest_ship):
        """
        Create alert for crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [test_data['embarkSupervisorShip']['crewDetail']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        test_data['embarkSupervisorShip']['alertResponse'] = _content

    @pytestrail.case(16267778)
    def test_24_verify_created_alert_crew(self, config, test_data, rest_ship):
        """
        Check if the alert got created for crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/crew/{test_data['embarkSupervisorShip']['teamMemberId']}")
        params = {
            'shipCode': config.ship.code,
            'size': '9999'
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['alerts']) == 0:
            raise Exception('Message did not get created for the Sailor')
        if not any(d['alertId'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['alerts']):
            raise Exception('Alert did not get created for crew')

    @pytest.mark.skip(reason='DCP-118025')
    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(67649487)
    def test_25_validate_crew_alert_message_in_ship_couch(self, config, test_data, rest_ship):
        """
        Check Crew Alert and messages got synced to ship couch
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        ship_url = f"{config.ship.sync}/TeamMemberPersonAlert::{test_data['embarkSupervisorShip']['teamMemberId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['AlertID'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['PersonAlerts']):
            raise Exception('Alert created for crew is not synced to ship couch')

        ship_url = f"{config.ship.sync}/TeamMemberMessage::{test_data['embarkSupervisorShip']['teamMemberId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['MessageID'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['Messages']):
            raise Exception('Message created for crew is not synced to ship couch')

    @pytestrail.case(16267779)
    def test_26_export_crew(self, config, test_data, rest_ship):
        """
        Export crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/team-members/search")
        params = {
            'size': '500'
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        for _teamMember in _content['teamMembers']:
            is_key_there_in_dict('personId', _teamMember)
            is_key_there_in_dict('teamMemberId', _teamMember)
            is_key_there_in_dict('teamMemberNumber', _teamMember)
            is_key_there_in_dict('identifications', _teamMember)

    @pytestrail.case(16310740)
    def test_27_create_visitor(self, config, test_data, rest_ship, guest_data):
        """
        Creating a Visitor by Crew
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        test_data['embarkSupervisorShip']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShip']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
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
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
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
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(16378473)
    def test_28_get_visitor(self, config, test_data, rest_ship):
        """
        Check if the visitor got created
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        test_data['embarkSupervisorShore']['availableVisitor'] = False
        params = {'page': 1, 'size': 99999}
        body = {
            "shipCode": config.ship.code,
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "reviewerTeamMemberIds": [test_data['embarkSupervisorShip']['reviewerTeamMemberId']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('visitors', _content['_embedded'])
        for _visitor in range(0, len(_content['_embedded']['visitors'])):
            if 'visits' in _content['_embedded']['visitors'][_visitor]:
                if 'employeeNumber' in _content['_embedded']['visitors'][_visitor] and test_data['embarkSupervisorShip']['employeeNumber'] == _content['_embedded']['visitors'][_visitor][
                    'employeeNumber']:
                    test_data['embarkSupervisorShip']['visitorId'] = _content['_embedded']['visitors'][_visitor][
                        'visitorId']
                    for visit in _content['_embedded']['visitors'][_visitor]['visits']:
                        is_key_there_in_dict('visitReviewers', _content['_embedded']['visitors'][_visitor]['visits'][0])
                        if len(visit['visitReviewers']) != 0:
                            is_key_there_in_dict('reviewerTeamMemberId',
                                                 _content['_embedded']['visitors'][_visitor]['visits'][0]['visitReviewers'][
                                                     0])
                            if test_data['embarkSupervisorShip']['reviewerTeamMemberId'] == visit['reviewerTeamMemberId']:
                                test_data['embarkSupervisorShore']['availableVisitor'] = True
                                return
                    else:
                        continue
        if not test_data['embarkSupervisorShore']['availableVisitor']:
            raise Exception('created reviewerTeamMemberId is not available in the list of visitor reviewerTeamMemberId')

    @pytestrail.case(26134532)
    def test_29_get_visitor_ship_core(self, config, test_data, rest_ship):
        """
        Check if the visitor is synced to ship core
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"/visitors/{test_data['embarkSupervisorShip']['visitorId']}")
        _content_ship = rest_ship.send_request(method="GET", url=url, auth="crew").content

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(26111995)
    def test_30_validate_visitor_data_in_ship_couch(self, config, request, test_data, rest_ship, verification):
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
        ship_url = f"{config.ship.sync}/VisitorStatus::{test_data['embarkSupervisorShip']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        for _key in verification.visitor_data_ship_couch:
            is_key_there_in_dict(_key, _content)
        assert len(_content['Visits'][0]['VisitReviewers']) != 0, "ERROR: Visitor data did not sync to Ship !!"

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(26111997)
    def test_31_validate_visitor_personal_data_in_ship_couch(self, config, request, test_data, rest_ship, verification):
        """
        Check Visitor Personal Information Data in ship couch
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :param verification:
        :return:
        """
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/visitor_data_ship_couch.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        _sync = config.ship.sync
        ship_url = f"{_sync}/VisitorPersonalInformation::{test_data['embarkSupervisorShip']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        for _key in verification.visitor_data_ship_couch:
            is_key_there_in_dict(_key, _ship_data)
        assert len(_ship_data['Visits'][0]['VisitReviewers']) != 0, "ERROR: Visitor data did not sync to Ship !!"

    @pytestrail.case(16378474)
    def test_32_visitor_detail(self, config, test_data, rest_ship, guest_data):
        """
        Go to the visitor detail page
        :param config:
        :param test_data:
        :param rest_ship:
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
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        is_key_there_in_dict('visits', _content)
        is_key_there_in_dict('identifications', _content)
        is_key_there_in_dict('alerts', _content)
        is_key_there_in_dict('messages', _content)
        test_data['embarkSupervisorShip']['personId'] = _content['personId']
        for _identity in _content['identifications']:
            test_data['embarkSupervisorShip']['identificationId'] = _identity['identificationId']
        for _visit in _content['visits']:
            test_data['embarkSupervisorShip']['visitId'] = _visit['visitId']
            test_data['embarkSupervisorShip']['visitReviewerId'] = _visit['visitReviewerId']
            test_data['embarkSupervisorShip']['reviewerTeamMemberId'] = _visit['reviewerTeamMemberId']
            test_data['embarkSupervisorShip']['visitorId'] = _visit['visitorId']
        assert _content['lastName'] == guest_data[guest]['LastName'], "lastName Mismatch !!"
        assert _content['firstName'] == guest_data[guest]['FirstName'], "firstName Mismatch !!"
        assert _content['departmentId'] == test_data['embarkSupervisorShip'][
            'departmentId'], "departmentId Mismatch !!"

    @pytestrail.case(16378475)
    def test_33_edit_visitor(self, config, test_data, rest_ship, guest_data):
        """
        Edit the created Visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/visitor")
        body = {
            "isDeleted": False,
            "lastName": guest_data[guest]['LastName'],
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00",
            "genderCode": guest_data[0]['GenderCode'][0],
            "citizenShipCountryCode": guest_data[0]['CitizenshipCountryCode'],
            "departmentPOC": "Test",
            "firstName": guest_data[guest]['FirstName'],
            "contactNumber": str(generate_phone_number(max_digits=10)),
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "visits": [
            ],
            "companyName": test_data['embarkSupervisorShip']['companyName'],
            "employeeNumber": test_data['embarkSupervisorShip']['employeeNumber'],
            "visitorTypeCode": "EB",
            "identifications": [
                {
                    "isDeleted": False,
                    "number": test_data['embarkSupervisorShip']['employeeNumber'],
                    "documentTypeCode": "P",
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "identificationId": test_data['embarkSupervisorShip']['identificationId']
                }],
            "visitorId": test_data['embarkSupervisorShip']['visitorId'],
            "securityPhotoMediaItemId": "",
            "personId": test_data['embarkSupervisorShip']['personId'],
            "personTypeCode": "V",
            "age": 35,
            "alerts": [],
            "messages": [],
            "propertyId": config.ship.code,
            "validForShip": config.ship.code,
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
            "submittedBy": test_data['embarkSupervisorShip']['submittedBy'],
            "submittedByEmail": test_data['embarkSupervisorShip']['submittedByEmail'],
            "submittedByName": test_data['embarkSupervisorShip']['submittedByName'],
            "submittedByDesignation": test_data['embarkSupervisorShip']['submittedByDesignation'],
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(16382998)
    def test_34_visitor_detail_edit(self, config, test_data, rest_ship, guest_data):
        """
        Check the visitor detail after editing
        :param config:
        :param test_data:
        :param rest_ship:
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
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        assert _content['lastName'] == guest_data[guest]['LastName'], "lastName Mismatch !!"
        assert _content['firstName'] == guest_data[guest]['FirstName'], "firstName Mismatch !!"
        test_data['embarkSupervisorShip']['visitsBody'] = _content['visits']
        test_data['embarkSupervisorShip']['identificationBody'] = _content['identifications']

    @pytestrail.case(16531912)
    def test_35_create_alert_visitor(self, config, test_data, rest_ship, guest_data):
        """
        Create alert for visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        # Search person in alert
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-embarkation-admin/persons")
        params = {"page": 1}
        body = {"fromDate": f"{test_data['embarkDate']}T00:00:00",
                "shipCode": config.ship.code,
                "toDate": f"{test_data['debarkDate']}T00:00:00"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict('currentPage', _content['page'])
        if _content['page']['currentPage'] != 1:
            raise Exception("Searching the  Wrong page !!!")
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
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
                    "genderCode": guest_data[0]['GenderCode'][0],
                    "citizenShipCountryCode": guest_data[0]['CitizenshipCountryCode'],
                    "departmentPOC": "Test",
                    "firstName": guest_data[guest]['FirstName'],
                    "contactNumber": str(generate_phone_number(max_digits=10)),
                    "departmentId": test_data['embarkSupervisorShip']['departmentId'],
                    "visits": test_data['embarkSupervisorShip']['visitsBody'],
                    "companyName": test_data['embarkSupervisorShip']['companyName'],
                    "employeeNumber": test_data['embarkSupervisorShip']['employeeNumber'],
                    "visitorTypeCode": "EB",
                    "identifications": test_data['embarkSupervisorShip']['identificationBody'],
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "securityPhotoMediaItemId": "",
                    "personId": test_data['embarkSupervisorShip']['personId'],
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
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        test_data['embarkSupervisorShip']['alertResponse'] = _content

    @pytestrail.case(16531913)
    def test_36_verify_created_alert(self, config, test_data, rest_ship):
        """
        Check if the alert got created
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShip']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if len(_content['alerts']) == 0:
            raise Exception('Alert did not get created for the visitor')
        if not any(d['alertId'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['alerts']):
            raise Exception('Alert did not get created for the visitor')

    @pytestrail.case(16531914)
    def test_37_create_message(self, config, test_data, rest_ship, guest_data):
        """
        Create Message for visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        # Search person in message
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "crew-embarkation-admin/persons")
        params = {"page": 1}
        body = {"fromDate": f"{test_data['embarkDate']}T00:00:00",
                "shipCode": config.ship.code,
                "toDate": f"{test_data['debarkDate']}T00:00:00"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict('currentPage', _content['page'])
        if _content['page']['currentPage'] != 1:
            raise Exception("Searching the  Wrong page !!!")
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/messages")
        body = {
            "alertTypeCode": None,
            "departmentId": None,
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": False,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
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
                    "genderCode": guest_data[0]['GenderCode'][0],
                    "citizenShipCountryCode": guest_data[0]['CitizenshipCountryCode'],
                    "departmentPOC": "Test",
                    "firstName": guest_data[guest]['FirstName'],
                    "contactNumber": str(generate_phone_number(max_digits=10)),
                    "departmentId": test_data['embarkSupervisorShip']['departmentId'],
                    "visits": test_data['embarkSupervisorShip']['visitsBody'],
                    "companyName": test_data['embarkSupervisorShip']['companyName'],
                    "employeeNumber": test_data['embarkSupervisorShip']['employeeNumber'],
                    "visitorTypeCode": "EB",
                    "identifications": test_data['embarkSupervisorShip']['identificationBody'],
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "securityPhotoMediaItemId": "",
                    "personId": test_data['embarkSupervisorShip']['personId'],
                    "personTypeCode": "V",
                    "age": 35,
                    "alerts": test_data['embarkSupervisorShip']['alertResponse'],
                    "messages": [],
                    "propertyId": config.ship.code,
                    "validForShip": config.ship.code,
                    "fullName": f"{guest_data[guest]['FirstName']} {guest_data[guest]['LastName']}"
                }
            ]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('personMessages', _content)
        is_key_there_in_dict('personMessageCount', _content)
        test_data['embarkSupervisorShip']['messageResponse'] = _content

    @pytestrail.case(16531915)
    def test_38_verify_created_message(self, config, test_data, rest_ship):
        """
        Check if the message got created
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShip']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if len(_content['messages']) == 0:
            raise Exception('Message did not get created for the visitor')
        if not any(d['messageId'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['messages']):
            raise Exception('Message did not get created for the visitor')

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(67649488)
    def test_39_validate_visitor_alert_message_in_ship_couch(self, config, test_data, rest_ship):
        """
        Check Visitor Alert and messages got synced to ship couch
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        ship_url = f"{config.ship.sync}/VisitorPersonAlert::{test_data['embarkSupervisorShip']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['AlertID'] == test_data['embarkSupervisorShip']['alertResponse']['alertId'] for d in
                   _content['PersonAlerts']):
            raise Exception('Alert created for visitor is not synced to ship couch')

        ship_url = f"{config.ship.sync}/VisitorMessage::{test_data['embarkSupervisorShip']['visitorId']}"
        _content = rest_ship.send_request(method="GET", url=ship_url).content
        if not any(d['MessageID'] == test_data['embarkSupervisorShip']['messageResponse']['messageId'] for d in
                   _content['Messages']):
            raise Exception('Message created for visitor is not synced to ship couch')

    @pytestrail.case(16531917)
    def test_40_approve_visit(self, config, test_data, rest_ship):
        """
        Approve the visit of visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShip']['visitsBody']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                            "statusCode": "approved",
                            "portCode": "ATSEA",
                            "boardingTypeCode": "GB",
                            "reviewerName": "Vertical QA",
                            "purpose": "Script Automation",
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": "1e41681f-b19e-4d89-ae12-89b688f8a137"
                        }
                    ]
                }
            ]
            _content = rest_ship.send_request(method="POST", params=params, url=url, json=body, auth="crew").content

    @pytestrail.case(16531918)
    def test_41_reject_visit(self, config, test_data, rest_ship):
        """
        Reject the visit of visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShip']['visitsBody']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "reviewerName": "Vertical QA",
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                            "statusCode": "rejected",
                            "portCode": "CCC",
                            "boardingTypeCode": "EB",
                            "reviewerName": "Vertical QA",
                            "purpose": "general purpose",
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": "53952924-fad5-4a02-813b-150900b8c981",
                            "visitReviewerId": "3787d305-84c4-4d44-bc56-fe8c80bfd673",
                            "isDeleted": False
                        }
                    ]
                }
            ]
            _content = rest_ship.send_request(method="POST", params=params, url=url, json=body, auth="crew").content

    @pytestrail.case(16534561)
    def test_42_export_visitors(self, config, test_data, rest_ship):
        """
        Export visitors
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'size': '999999'
        }
        body = {
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "reviewerTeamMemberIds": [test_data['embarkSupervisorShip']['reviewerTeamMemberId']],
            "shipCode": config.ship.code,
            "visitWiseVisitor": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        for _visitor in _content['_embedded']['visitors']:
            is_key_there_in_dict('firstName', _visitor)
            is_key_there_in_dict('lastName', _visitor)
            is_key_there_in_dict('genderCode', _visitor)
            is_key_there_in_dict('visitorId', _visitor)
            is_key_there_in_dict('visitorTypeCode', _visitor)
            is_key_there_in_dict('visitorDepartmentId', _visitor)
            is_key_there_in_dict('visits', _visitor)
            is_key_there_in_dict('identifications', _visitor)

    @pytestrail.case(16552651)
    def test_43_import_visitors(self, config, test_data, rest_ship):
        """
        Import visitors
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        datetime_obj = datetime.strptime(test_data['embarkSupervisorShip']['shipDate'], '%Y-%m-%d').date()
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
        _dateTime = test_data['embarkSupervisorShip']['shipDateTime'].split(" ")
        _shipDateTime = f"{_dateTime[0]}T{_dateTime[1]}"
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/gangway/visitors/import/v1")
        params = {"reviewerteammemberid": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
                  "submittedbyid": test_data['embarkSupervisorShip']['submittedBy'], "shipcode": config.ship.code,
                  "shiptime": _shipDateTime, "autoApprove": False}
        rest_ship.session.headers.update({'Content-Type': 'multipart/form-data'})
        _file = open(_filePath, 'rb')
        body = {"file": _file}
        _content = rest_ship.send_request(method="POST", url=url, files=body, params=params, auth="crew").content
        is_key_there_in_dict('fileDownloadURL', _content)
        is_key_there_in_dict('lastStatus', _content)
        is_key_there_in_dict('success', _content)
        is_key_there_in_dict('totalRecords', _content)
        is_key_there_in_dict('visitorImportReq', _content)
        assert _content['success'], "visitor import failed!!"
        test_data['embarkSupervisorShip']['bulkImportResponse'] = _content['visitorImportReq'][0]
        for _visitor in _content['visitorImportReq']:
            if _visitor['status'] != 'Added':
                raise Exception('Visitor did not get Added')

    @pytestrail.case(41413325)
    def test_44_import_status(self, rest_shore, config):
        """
        Verify Import Status
        :param config:
        :param rest_shore:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/visitors/importstatus")
        _content = rest_shore.send_request(method="GET", url=url, auth="crew").content
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

    @pytestrail.case(16552652)
    def test_45_bulk_approve(self, config, test_data, rest_ship):
        """
        Bulk approve the imported visitors
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {"bulkApproval": True}
        datetime_obj = datetime.strptime(test_data['embarkSupervisorShip']['shipDate'], '%Y-%m-%d').date()
        _startDate = f"{datetime_obj}T00:00:01"
        body = [{"visitorId": test_data['embarkSupervisorShip']['bulkImportResponse']['visitorId'], "visits": [
            {"visitId": test_data['embarkSupervisorShip']['bulkImportResponse']['visitId'],
             "visitorId": test_data['embarkSupervisorShip']['bulkImportResponse']['visitorId'],
             "startDate": _startDate, "statusCode": "approved",
             "portCode": test_data['embarkSupervisorShip']['bulkImportResponse']['portCode'], "boardingTypeCode": "GB",
             "reviewerName": test_data['embarkSupervisorShip']['reviewerName'],
             "purpose": test_data['embarkSupervisorShip']['bulkImportResponse']['visitPurpose'],
             "propertyId": config.ship.code,
             "reviewerTeamMemberId": test_data['embarkSupervisorShip']['reviewerTeamMemberId'],
             "reviewerEmail": test_data['embarkSupervisorShip']['reviewerEmail'],
             "submittedBy": test_data['embarkSupervisorShip']['submittedBy']}]}]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if len(_content) != 0:
            for _visitor in _content:
                for _visit in _visitor['visits']:
                    if _visit['statusCode'] != 'approved':
                        raise Exception('The visit for the visitor did not get approved')
        else:
            raise Exception("No visitor Approved!!")

    @pytestrail.case(16552653)
    def test_46_verify_created_message_report(self, config, test_data, rest_ship):
        """
        Check if the message shown in alerts and messages section
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        message_id = test_data['embarkSupervisorShip']['messageResponse']['messageId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/messages/{message_id}")
        _content = rest_ship.send_request(method="GET", url=_url, auth="crew").content
        assert len(_content) != 0, "message not showing in alert and message section"

    @pytestrail.case(16552654)
    def test_47_verify_created_alert_report(self, config, test_data, rest_ship):
        """
        Check if the alert shown in alerts and messages section
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        alert_id = test_data['embarkSupervisorShip']['alertResponse']['alertId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), f"/crew-embarkation-admin/alerts/{alert_id}")
        _content = rest_ship.send_request(method="GET", url=_url, auth="crew").content
        assert len(_content) != 0, "alert not showing in alert and message section"

    @pytestrail.case(16552655)
    def test_48_get_message_detail(self, config, test_data, rest_ship):
        """
        To verify the message detail page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/messages/{test_data['embarkSupervisorShip']['messageResponse']['messageId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('persons', _content)
        is_key_there_in_dict('description', _content)
        is_key_there_in_dict('startDate', _content)
        is_key_there_in_dict('endDate', _content)
        is_key_there_in_dict('createdByUser', _content)
        is_key_there_in_dict('creationTime', _content)
        is_key_there_in_dict('createdBy', _content)

    @pytestrail.case(16552656)
    def test_49_get_alert_detail(self, config, test_data, rest_ship):
        """
        To verify the alert detail page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/alerts/{test_data['embarkSupervisorShip']['alertResponse']['alertId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('persons', _content)
        is_key_there_in_dict('description', _content)
        is_key_there_in_dict('departmentId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('endDate', _content)
        is_key_there_in_dict('startDate', _content)
        is_key_there_in_dict('creationTime', _content)
        is_key_there_in_dict('createdBy', _content)

    @pytestrail.case(16534562)
    def test_50_search_visitor(self, config, test_data, rest_ship, guest_data):
        """
        Import visitors
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = 0
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/search")
        params = {
            'q': guest_data[guest]['FirstName'],
            'voyagenumber': test_data['embarkSupervisorShip']['voyageNumber'],
            "shipCode": config.ship.code,
            "isCrew": "true",
            "isGuest": "true",
            "isVisitor": "true"
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['visitors']) == 0:
            raise Exception('The created visitor is not shown in global search')
        if not any(d['firstName'] == guest_data[guest]['FirstName'] for d in _content['visitors']):
            raise Exception('The created visitor is not shown in global search')

    @pytestrail.case(29907079)
    def test_51_get_dashboard_approve_reject_ashore_counts(self, config, test_data, rest_ship):
        """
        To get the dashboard data
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['currentDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('teamMemberEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('messageDetail', _content['dashboard'])
        is_key_there_in_dict('alertDetail', _content['dashboard'])
        test_data['embarkSupervisorShip']['sailor_dashboard'] = _content['dashboard']['guestEmbarkStats']
        test_data['embarkSupervisorShip']['visitor_dashboard'] = _content['dashboard']['visitorEmbarkStats']
        test_data['embarkSupervisorShip']['crew_dashboard'] = _content['dashboard']['teamMemberEmbarkStats']

    @pytestrail.case(27405387)
    def test_52_verify_visitor_approved_count(self, config, test_data, rest_ship):
        """
        Verify visitor Approved count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'page': 1
        }
        body = {
            "shipCode": config.ship.code,
            "reviewerTeamMemberIds": [],
            "startDate": f"{test_data['aci']['shipDate']}T00:00:00",
            "endDate": f"{test_data['aci']['shipDate']}T23:59:59",
            "visitStatuses": ["approved"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Approved_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] == test_data['embarkSupervisorShip'][
            'Approved_Elements'], "approved count mismatch !!"

    @pytestrail.case(27435499)
    def test_53_verify_export_csv_of_approved(self, config, test_data, rest_ship):
        """
        Verify visitor approved count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "shipCode": config.ship.code,
            "reviewerTeamMemberIds": [],
            "startDate": f"{test_data['aci']['shipDate']}T00:00:00",
            "endDate": f"{test_data['aci']['shipDate']}T23:59:59",
            "visitStatuses": ["approved"],
            "visitWiseVisitor": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Approved_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] == test_data['embarkSupervisorShip'][
            'Approved_Elements'], "approved count mismatch !!"

    @pytestrail.case(65133493)
    def test_54_verify_visitor_approval_pending_count(self, config, test_data, rest_ship):
        """
        Verify visitor Approval Pending count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "shipCode": config.ship.code,
            "startDate": f"{test_data['aci']['shipDate']}T00:00:00",
            "endDate": f"{test_data['aci']['shipDate']}T23:59:59",
            "visitStatuses": ["pending"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Approval_Pending_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['visitor_dashboard']['approvalPendingCount'] == test_data[
                    'embarkSupervisorShip']['Approval_Pending_Elements'], "Approval Pending visitors count mismatch !!"

    @pytestrail.case(27425484)
    def test_55_verify_visitor_rejected_count(self, config, test_data, rest_ship):
        """
        Verify visitor Rejected count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'page': 1
        }
        body = {
            "shipCode": config.ship.code,
            "reviewerTeamMemberIds": [],
            "startDate": f"{test_data['aci']['shipDate']}T00:00:00",
            "endDate": f"{test_data['aci']['shipDate']}T23:59:59",
            "visitStatuses": ["rejected"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Rejected_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['visitor_dashboard']['rejected'] == test_data['embarkSupervisorShip'][
            'Rejected_Elements'], "rejected count mismatch !!"

    @pytestrail.case(27439612)
    def test_56_verify_total_sailors_count_matching(self, config, test_data, rest_ship):
        """
        Verify total sailor count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['total_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['sailor_dashboard']['totalOccupancy'] == test_data[
            'embarkSupervisorShip']['total_Elements'], "Total Sailors count mismatched !!"

    @pytestrail.case(27452433)
    def test_57_verify_sailor_checkin_count(self, config, test_data, rest_ship):
        """
        Verify sailor check in count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1
        }
        body = {
            "checkedInStatus": "CHECKED_IN",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['checkin_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['sailor_dashboard']['checkedIn'] == test_data['embarkSupervisorShip'][
            'checkin_Elements'], "check in count mismatched !!"

    @pytestrail.case(65133494)
    def test_58_verify_sailor_onboard_count(self, config, test_data, rest_ship):
        """
        Verify sailor onboard count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "boardingStatus": "ONBOARD",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "reservationStatusCodes": [],
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Sailor_Onboard_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['sailor_dashboard']['onboard'] == test_data['embarkSupervisorShip'][
            'Sailor_Onboard_Elements'], "Sailor Onboard count mismatched !!"

    @pytestrail.case(65561237)
    def test_59_verify_sailor_checkin_onboard_count(self, config, test_data, rest_ship):
        """
        Verify sailor checked-in onboard count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "checkedInStatus": "CHECKED_IN",
            "boardingStatus": "ONBOARD",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": []
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['checkIn_Onboard_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['checkIn_Onboard_Elements'] == test_data['embarkSupervisorShip'][
            'sailor_dashboard']['checkedInOnboard'], "sailor checkedIn onboard count mismatched !!"

    @pytestrail.case(65133495)
    def test_60_verify_sailor_ashore_count(self, config, test_data, rest_ship):
        """
        Verify sailor ashore count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "boardingStatus": "ASHORE",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "reservationStatusCodes": [],
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Sailor_Ashore_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['sailor_dashboard']['ashore'] == test_data['embarkSupervisorShip'][
            'Sailor_Ashore_Elements'], "Sailor Ashore count mismatched !!"

    @pytestrail.case(27452434)
    def test_61_verify_sailor_not_checkin_count(self, config, test_data, rest_ship):
        """
        Verify Not check in count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1
        }
        body = {
            "checkedInStatus": "NOT_CHECKED_IN",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['not_checkin_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['sailor_dashboard']['notCheckedIn'] == test_data[
            'embarkSupervisorShip']['not_checkin_Elements'], "not check in count mismatch !!"

    @pytestrail.case(65798572)
    def test_62_verify_sailor_not_checkedIn_onboard_count(self, config, test_data, rest_ship):
        """
         Verify sailor not checked-in onboard count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "checkedInStatus": "NOT_CHECKED_IN",
            "boardingStatus": "ONBOARD",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": []
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['Not_CheckedIn_onboard_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['Not_CheckedIn_onboard_Elements'] == test_data['embarkSupervisorShip'][
            'sailor_dashboard']['notCheckedInOnboard'], "Sailor not checked-in onboard count mismatched !!"

    @pytestrail.case(65561234)
    def test_63_verify_sailor_rts_complete_and_approved_count(self, config, test_data, rest_ship):
        """
         Verify sailor RTS Complete and approved count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 9999999
        }
        body = {
            "checkedInStatus": "OCI_DONE_APPROVED",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": []
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['OCI_Done_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['OCI_Done_Elements'] == test_data['embarkSupervisorShip'][
            'sailor_dashboard']['ociDoneAndApproved'], "Sailor RTS Complete and approved count mismatched !!"

    @pytestrail.case(65561235)
    def test_64_verify_sailor_rts_complete_and_approval_pending_count(self, config, test_data, rest_ship):
        """
         Verify sailor RTS Complete and approval Pending count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "checkedInStatus": "OCI_DONE_PENDING",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": []
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['OCI_Done_Pending_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['OCI_Done_Pending_Elements'] == test_data['embarkSupervisorShip'][
            'sailor_dashboard']['ociDoneAndPending'], "Sailor RTS Complete but approval pending count mismatched !!"

    @pytestrail.case(65561236)
    def test_65_verify_sailor_rts_not_complete_count(self, config, test_data, rest_ship):
        """
         Verify sailor RTS Not Complete count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/reservation-guests/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "checkedInStatus": "OCI_NOT_DONE",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": []
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['OCI_Not_Done_Elements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['OCI_Not_Done_Elements'] == test_data['embarkSupervisorShip'][
            'sailor_dashboard']['ociNotDone'], "Sailor RTS Not Complete count mismatched !!"

    @pytestrail.case(27461433)
    def test_66_verify_crew_onboard_count(self, config, test_data, rest_ship):
        """
        Verify Crew onboard in count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/team-members/search")
        params = {
            'page': 1
        }
        body = {
            "boardingStatus": "ONBOARD",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['crew_onboardElements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['crew_dashboard']['onboard'] == test_data['embarkSupervisorShip'][
                                                                    'crew_onboardElements'], "crew onboard mismatch !!"

    @pytestrail.case(65135804)
    def test_67_verify_crew_ashore_count(self, config, test_data, rest_ship):
        """
        Verify Crew ashore count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/team-members/search")
        params = {
            'page': 1,
            'size': 999999
        }
        body = {
            "boardingStatus": "ASHORE",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['crew_ashoreElements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['crew_dashboard']['ashore'] == test_data['embarkSupervisorShip'][
                                                                'crew_ashoreElements'], "crew ashore count mismatch !!"

    @pytestrail.case(27461434)
    def test_68_verify_crew_checkin_count(self, config, test_data, rest_ship):
        """
        Verify Crew check in count
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/team-members/search")
        params = {
            'page': 1
        }
        body = {
            "checkedInStatus": "CHECKED_IN",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:00",
            "shipCode": config.ship.code,
            "shipTime": test_data['aci']['currentDate'],
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict("totalElements", _content['page'])
        test_data['embarkSupervisorShip']['crew_totalElements'] = _content['page']['totalElements']
        assert test_data['embarkSupervisorShip']['crew_totalElements'] == test_data['embarkSupervisorShip'][
                                                            'crew_dashboard']['checkedIn'], "Checkin count mismatch !!"

    @pytestrail.case(65666149)
    def test_69_verify_guest_summary_inside_boarding_slots_tab(self, config, test_data, rest_ship):
        """
        Verify sailor Checked-in and Onboard counts in guest summary call inside boarding slots tab
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "reservationguests/search/guest-summary")
        body = {
                "boardingInventorySummary": True,
                "embarkDate": f"{test_data['embarkDate']}T19:00:00",
                "debarkDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
                "shipCode": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict("checkedIn", _content)
        is_key_there_in_dict("onboard", _content)
        assert _content["checkedIn"] == test_data['embarkSupervisorShip']['sailor_dashboard'][
                                        'checkedIn'], "Sailor checked-in counts not matching inside boarding slots tab."
        assert _content["onboard"] == test_data['embarkSupervisorShip']['sailor_dashboard'][
                                             "onboard"], "Sailor Onboard counts not matching inside boarding slots tab."

    @pytestrail.case(28822395)
    def test_70_verify_exception_reports(self, config, test_data, rest_ship):
        """
        Verify exception reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/exception")
        params = {
            'page': '1'
        }
        body = {
            "reportType": "exception",
            "exceptions": [
                "MISSING-PICTURE"
            ],
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('exceptions', _content['_embedded'])

    @pytestrail.case(65133490)
    def test_71_verify_missing_picture_data_in_exception_report(self, config, test_data, rest_ship, guest_data):
        """
         Verify missing picture data in exception report by creating a visitor without profile photo
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/exception")
        params = {
            'page': '1',
            'size': 999999
        }
        body = {
            "reportType": "exception",
            "exceptionType": "MISSING-PICTURE",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "useOptimized": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('totalElements', _content['page'])
        test_data['Exception_report'] = dict()
        test_data['Exception_report']['Missing_picture_count'] = _content['page']['totalElements']
        guest = 0
        test_data['embarkSupervisorShip']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShip']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
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
            "profileImageUrl": "",
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
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
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
        }
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/exception")
        params = {
            'page': '1',
            'size': 999999
        }
        body = {
            "reportType": "exception",
            "exceptionType": "MISSING-PICTURE",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "useOptimized": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('totalElements', _content['page'])
        assert _content['page']['totalElements'] == test_data['Exception_report']['Missing_picture_count'] + 1, \
            "Missing picture count in Exception Report not increasing after adding a visitor without profile photo."
        test_data['Exception_report']['Missing_picture_count'] += 1

    @pytestrail.case(28822396)
    def test_72_verify_movement_report(self, config, test_data, rest_ship):
        """
        Verify movement report
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/movement")
        params = {
            'page': '1'
        }
        body = {
            "reportType": "movement",
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "movementActivityFrom": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "movementActivityTo": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('movements', _content['_embedded'])

    @pytestrail.case(28822397)
    def test_73_location_history_reports(self, config, test_data, rest_ship):
        """
        Verify location history report
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        person_type_codes = ["C", "V", "RG"]
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/location-movement")
        params = {
            'page': '1',
            'size': 9999999
        }
        for code in person_type_codes:
            body = {
                "reportType": "location",
                "personTypeCode": code,
                "boardingStatus": "ONBOARD",
                "movementActivityTo": test_data['aci']['currentDate'],
                "shipCode": config.ship.code,
                "shipTime": test_data['aci']['currentDate']
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            is_key_there_in_dict('locationMovement', _content['_embedded'])

    @pytestrail.case(65789648)
    def test_74_export_location_history_reports(self, config, test_data, rest_ship):
        """
        Verify export location history report
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        person_type_codes = ["C", "V", "RG"]
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'),
                                        "/gangway-reports/location-movement/export")
        params = {
            'page': '1',
            'size': 9999999
        }
        for code in person_type_codes:
            body = {
                "reportType": "location",
                "personTypeCode": code,
                "boardingStatus": "ONBOARD",
                "movementActivityTo": test_data['aci']['currentDate'],
                "shipCode": config.ship.code,
                "shipTime": test_data['aci']['currentDate']
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            if len(str(_content)) == 0:
                raise Exception(f"Not able to export Location History report for person type code {code} !!")

    @pytestrail.case(65133491)
    def test_75_verify_onboard_sailors_with_past_debark_date_report(self, config, test_data, rest_ship):
        """
        Verify Onboard Sailor with Past Debark Date report
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'),
                      "/gangway-reports/debarked-onboarded-summary")
        params = {
            'page': '1',
            'size': 999999
        }
        body = {
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['aci']['currentDate']}"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict("_embedded", _content)
        is_key_there_in_dict("debarkedOnboardedSummary", _content["_embedded"])

    @pytestrail.case(28822398)
    def test_76_cbp_reports(self, config, test_data, rest_ship):
        """
        Verify cbp reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/cbp-summary/v1")
        params = {
            'page': '1'
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "personTypeCode": "C",
            "reportType": "cbp"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('cbpSummary', _content['_embedded'])

    @pytestrail.case(65561227)
    def test_77_verify_cbp_report_for_sailor(self, config, test_data, guest_data, rest_ship):
        """
        Verify CBP Report for Sailor by creating a CBP hold alert for Sailor
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        url_cbp = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/cbp-summary/v1")
        params_cbp = {
            'page': 1,
            'size': 9999999
        }

        body_cbp = {
            "reportType": "cbp",
            "personTypeCode": "C",
            "masterData": "{}",
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "isCleared": False,
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", json=body_cbp, params=params_cbp, url=url_cbp, auth="crew") \
            .content
        is_key_there_in_dict("_embedded", _content)
        is_key_there_in_dict("cbpSummary", _content["_embedded"])
        test_data['embarkSupervisorShip']['CBP_report_summary'] = dict()
        for _type in _content["_embedded"]["cbpSummary"][0]["cbpSummary"]:
            if _type['personTypeCode'] == 'RG':
                test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"] = dict()
                test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"][
                    'totalOnVoyage'] = _type['totalOnVoyage']
                test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"][
                    'notCleared'] = _type['notCleared']
                test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"][
                    'cleared'] = _type['cleared']
                break
        else:
            raise Exception('Can not find details for personTypeCode as "RG" in response')
        for guest in guest_data:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                                        f"/crew-embarkation-admin/reservation-guests/{guest['reservationGuestId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            is_key_there_in_dict('reservationGuestId', _content)
            is_key_there_in_dict('alerts', _content)
            if len(_content['alerts']) == 0:
                break
        else:
            pytest.skip("No sailors found with 0 alerts for validation !!")
        sailor_details = _content
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": [sailor_details]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        alert_id = _content['alertId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/reservation-guests/{guest['reservationGuestId']}")
        params = {
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict('alerts', _content)
        if len(_content['alerts']) != 0:
            for alert in _content['alerts']:
                if alert['alertId'] == alert_id:
                    assert alert['alertTypeCode'] == "CBP", "ALERT type created for sailor is not CBP Hold."
                    break
            else:
                raise Exception("CBP Alert not created for sailor.")
        else:
            raise Exception("No CBP Hold ALERT created for sailor.")
        time.sleep(3)
        _content = rest_ship.send_request(method="POST", json=body_cbp, params=params_cbp, url=url_cbp, auth="crew") \
            .content
        is_key_there_in_dict("_embedded", _content)
        is_key_there_in_dict("cbpSummary", _content["_embedded"])
        for _type in _content["_embedded"]["cbpSummary"][0]["cbpSummary"]:
            if _type['personTypeCode'] == "RG":
                assert _type['totalOnVoyage'] == test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"][
                    'totalOnVoyage'] + 1, "Sailor Total count in CBP Report is not getting increased."
                assert _type['notCleared'] == test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"][
                    'notCleared'] + 1, "Sailor Not Cleared count in CBP report is not getting increased."
                break
        else:
            raise Exception('Can not find details for personTypeCode as "RG" in response')
        test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"]['totalOnVoyage'] += 1
        test_data['embarkSupervisorShip']['CBP_report_summary']["sailor"]['notCleared'] += 1

    @pytestrail.case(28822399)
    def test_78_ipm_reports(self, config, test_data, rest_ship):
        """
        Verify Ipm reports
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway-reports/in-port-manning")
        params = {
            'page': '1'
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "shipCode": config.ship.code,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "reportType": "ipm",
            "safetyPositionAssigned": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('inPortMannings', _content['_embedded'])

    @pytestrail.case(29907635)
    def test_79_dashboard_call_of_ipm(self, config, test_data, rest_ship):
        """
        To Verify Dashboard call of IPM after editing
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['embarkSupervisorShip']['portCode_content_length'] = False
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/in-port-manning/dashboard-details")
        params = {
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T11:59:59",
            "shipCode": config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            test_data['embarkSupervisorShip']['portCode_content_length'] = False
            pytest.skip(msg="Its not a port day")
        for _request in _content:
            is_key_there_in_dict("ipmDutyDetailId", _request)
            is_key_there_in_dict("portCode", _request)
            is_key_there_in_dict("groupCode", _request)
            is_key_there_in_dict("assignedDate", _request)
            test_data['embarkSupervisorShip']['ipmDutyDetailId'] = _content[0]['ipmDutyDetailId']
            test_data['embarkSupervisorShip']['portCode'] = _content[0]['portCode']
            test_data['embarkSupervisorShip']['groupCode'] = _content[0]['groupCode']
            test_data['embarkSupervisorShip']['assignedDate'] = _content[0]['assignedDate']
            test_data['embarkSupervisorShip']['portCode_content_length'] = True

    @pytestrail.case(27465074)
    def test_80_assign_group_in_ipm(self, config, test_data, rest_ship):
        """
        Verify assign group in IPM
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['embarkSupervisorShip']['portCode_content_length']:
            pytest.skip(msg="There is no port day today")
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      "/crew-embarkation-admin/in-port-manning/bulk-assign-duty")
        body = {
            "assignedDate": test_data['embarkSupervisorShip']['assignedDate'],
            "groupCode": test_data['embarkSupervisorShip']['groupCode'],
            "portCode": test_data['embarkSupervisorShip']['portCode'],
            "shipCode": config.ship.code,
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(29907080)
    def test_81_ipm_search_call(self, config, test_data, rest_ship):
        """
        Verify ipm search call
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['embarkSupervisorShip']['portCode_content_length']:
            pytest.skip(msg="There is no port day today")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      "/gangway/in-port-manning/search")
        params = {
            "page": 1,
            "size": 999999
        }
        body = {
            "departmentKeys": [
                "Art Auction",
                "Audio/Visual Media",
                "Aux Service",
                "Beverage Guest Service",
                "Casino",
                "Culinary Arts",
                "Deck",
                "Engine",
                "Entertainment",
                "Ent - Technical",
                "F&B Mgmt",
                "Food Ops",
                "Front Desk",
                "Future Vacations",
                "Gift Shop",
                "Guest Services",
                "Hotel",
                "Hotel Director Or Guest Services",
                "Housekeeping",
                "Hr",
                "Human Resources",
                "Info Systems",
                "Infotainment",
                "Infra Structure",
                "Laundry",
                "Maintenance",
                "Medical",
                "Musicians",
                "Onboard Media",
                "Photo",
                "Porter",
                "Provision",
                "Reservations",
                "Restaurant Services",
                "Salon",
                "Security",
                "Security Services",
                "Ship/Account",
                "Shop",
                "Shore Excursions",
                "Spa",
                "Supernum",
                "Technical",
                "Youth"
            ],
            "portCode": test_data['embarkSupervisorShip']['portCode'],
            "shipCode": config.ship.code,
            "shipDate": test_data['aci']['currentDate']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('inPortMannnings', _content['_embedded'])
        test_data['embarkSupervisorShip']['ipmSafetyPositionDetailId'] = _content['_embedded']['inPortMannnings'][0][
            'ipmSafetyPositionDetails'][0]['ipmSafetyPositionDetailId']
        test_data['embarkSupervisorShip']['ipmPositionId'] = _content['_embedded']['inPortMannnings'][0][
            'ipmSafetyPositionDetails'][0]['ipmPositionId']

    @pytestrail.case(27465075)
    def test_82_edit_group_in_ipm(self, config, test_data, rest_ship):
        """
        Verify edit group in IPM
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['embarkSupervisorShip']['portCode_content_length']:
            pytest.skip(msg="There is no port day today")
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'),
                      "/gangway/changeassignedduty")
        body = {
            "assignedDate": test_data['embarkSupervisorShip']['assignedDate'],
            "ipmDutyDetailIds": [test_data['embarkSupervisorShip']['ipmDutyAssignmentId']],
            "unAssigneDutyIds": [test_data['embarkSupervisorShip']['ipmDutyAssignmentId']],
            "ipmDuties": [{
                "assignedDate": test_data['embarkSupervisorShip']['assignedDate'],
                "ipmSafetyPositionDetailId": test_data['embarkSupervisorShip']['ipmSafetyPositionDetailId'],
                "ipmPositionId": test_data['embarkSupervisorShip']['ipmPositionId'],
                "teamMemberId": test_data['embarkSupervisorShip']['teamMemberId'],
                "isDeleted": False,
                "portCode": test_data['embarkSupervisorShip']['portCode'],
                "shipCode": config.ship.code
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(27465076)
    def test_83_unassign_group_on_ipm(self, config, test_data, rest_ship):
        """
        Verify un assign group in IPM
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['embarkSupervisorShip']['portCode_content_length']:
            pytest.skip(msg="There is no port day today")
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'),
                      "/gangway/changeassignedduty")
        body = {
            "assignedDate": test_data['embarkSupervisorShip']['assignedDate'],
            "ipmDutyDetailIds": [test_data['embarkSupervisorShip']['ipmDutyDetailId']],
            "unAssigneDutyIds": [test_data['embarkSupervisorShip']['ipmDutyDetailId']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

    @pytestrail.case(67649489)
    def test_84_get_visitor_created_shore(self, config, test_data, rest_ship):
        """
        Check if the visitor created shore side is showing in ship side
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {'size': '99999'}
        body = {"shipCode": config.ship.code, "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        visitorShoreSynced = False
        for _visitor in _content['_embedded']['visitors']:
            if 'employeeNumber' in _visitor:
                if _visitor['employeeNumber'] == test_data['embarkSupervisorShore']['visitorShore']['employeeNumber']:
                    if _visitor['visitorId'] == test_data['embarkSupervisorShore']['visitorShore']['visitorId']:
                        assert _visitor['firstName'] == test_data['embarkSupervisorShore']['visitorShore'][
                            'firstName'], 'First name Mismatch !!'
                        assert _visitor['lastName'] == test_data['embarkSupervisorShore']['visitorShore'][
                            'lastName'], 'Last name Mismatch !!'
                        assert _visitor['genderCode'] == test_data['embarkSupervisorShore']['visitorShore'][
                            'genderCode'], 'Gender Mismatch !!'
                        assert _visitor['securityPhotoMediaItemId'] == \
                               test_data['embarkSupervisorShore']['visitorShore']['profileImageUrl'].split('/')[
                                   -1], 'Profile Photo Mismatch !!'
                        visitorShoreSynced = True
        if not visitorShoreSynced:
            raise Exception('Visitor created shore side is not synced to ship side !!')

    @pytestrail.case(67649490)
    def test_85_verify_created_message_alert_shore(self, config, test_data, rest_ship):
        """
        Check if the message alert created for shore side visitor got synced to ship side
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShore']['visitorShore']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if len(_content['alerts']) == 0:
            raise Exception('Alert for visitor created at shore side did not synced to ship side')
        if not any(d['alertId'] == test_data['embarkSupervisorShore']['alertResponseVisitorShore']['alertId'] for d in
                   _content['alerts']):
            raise Exception('Alert for visitor created at shore side did not synced to ship side')
        if len(_content['messages']) == 0:
            raise Exception('Message for visitor created at shore side did not synced to ship side')
        if not any(d['messageId'] == test_data['embarkSupervisorShore']['messageResponseVisitorShore']['messageId'] for d in _content['messages']):
            raise Exception('Message for visitor created at shore side did not synced to ship side')

    @pytestrail.case(32214912)
    def test_86_search_crew_by_first_last_name_team_number(self, config, test_data, rest_ship):
        """
        Check if crew can be searched with first name, last name and team member number.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/search')
        params = {
            "q": test_data['embarkSupervisorShip']['crewData']['firstName'],
            "voyagenumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipCode": "SC",
            "isCrew": "true",
            "isGuest": "true",
            "isVisitor": "true"
        }
        content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict("teamMembers", content)
        assert len(content['teamMembers']) > 0, "Search results are empty."
        for crew_list in content['teamMembers']:
            if crew_list['teamMemberNumber'] == test_data['embarkSupervisorShip']['crewData']['teamMemberNumber']:
                assert crew_list['firstName'] == test_data['embarkSupervisorShip']['crewData'][
                    'firstName'], "Crew is not getting search by firstName."
                break

        _params = {
            "q": test_data['embarkSupervisorShip']['crewData']['lastName'],
            "voyagenumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipCode": "SC",
            "isCrew": True,
            "isGuest": True,
            "isVisitor": True
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict("teamMembers", _content)
        assert len(_content['teamMembers']) > 0, "Search results are empty."
        for team_list in content['teamMembers']:
            if team_list['teamMemberNumber'] == test_data['embarkSupervisorShip']['crewData']['teamMemberNumber']:
                assert team_list['lastName'] == test_data['embarkSupervisorShip']['crewData'][
                    'lastName'], "Crew is not getting search by lastName."
                break

        to_params = {
            "q": test_data['embarkSupervisorShip']['crewData']['teamMemberNumber'],
            "voyagenumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipCode": "SC",
            "isCrew": "true",
            "isGuest": "true",
            "isVisitor": "true"
        }
        to_content = rest_ship.send_request(method="GET", url=url, params=to_params, auth="crew").content
        is_key_there_in_dict("teamMembers", to_content)
        assert len(to_content['teamMembers']) > 0, "Search results are empty."
        for crew_member in to_content['teamMembers']:
            if crew_member['teamMemberNumber'] == test_data['embarkSupervisorShip']['crewData']['teamMemberNumber']:
                break
            else:
                raise Exception('Search results are not matching with crew member if searched by team member number.')

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(67649491)
    def test_87_ashore_visitor_get_ashore(self, config, test_data, rest_ship):
        """
        To check that visitor marked ashore should get ashore
        :param rest_ship:
        :param config:
        :param test_data:
        :return:
        """
        test_data['gangway']['creation'] = {}
        url = urljoin(config.ship.sync,
                      f"/VisitorStatus::{test_data['embarkSupervisorShip']['bulkImportResponse']['visitorId']}")
        test_data['gangway']['visitorStatus'] = rest_ship.send_request(url=url, method='GET', auth='Basic').content
        test_data['gangway']['creation']['CheckInBy'] = test_data['embarkSupervisorShip']['submittedBy']
        test_data['gangway']['creation'][
            "CheckInStatusDate"] = f"{test_data['embarkSupervisorShip']['shipDate']}T18:18:24.294Z"
        test_data['gangway']['creation']["CheckInStatusDateEpoch"] = int(time.time() * 1000)
        test_data['gangway']['creation']["TerminalCheckinStatus"] = "COMPLETED"
        test_data['gangway']['creation']['_rev'] = test_data['gangway']['visitorStatus']['_rev']
        rest_ship.send_request(method="PUT", url=url, json=test_data['gangway']['creation'], auth="crew")

        # Assign RFID
        _url = urljoin(getattr(config.ship.contPath, 'url.path.hydration'), 'trackablehosts/bulk')
        rf_id = generate_guid()
        json = {
            "trackableHosts": [
                {
                    "hostId": test_data['gangway']['visitorStatus']['VisitorID'],
                    "hostIdType": "V",
                    "trackableAttributes": {
                        "rfId": rf_id
                    }
                }
            ]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=json, auth="crew").content

        content_rev = rest_ship.send_request(method='GET', url=url, auth='Basic').content
        to_url = urljoin(config.ship.sync,
                         f"/VisitorStatus::{test_data['embarkSupervisorShip']['bulkImportResponse']['visitorId']}")
        data = {
            "BoardingStatusDate": f"{test_data['embarkSupervisorShip']['shipDate']}T14:18:20.650Z",
            "BoardingStatusDateEpoch": int(time.time() * 1000),
            "ExpiryDateEpoch": test_data['gangway']['visitorStatus']['ExpiryDateEpoch'],
            "IsOnBoarded": True,
            "OnBoardingStatusDateEpoch": int(time.time() * 1000),
            "SortingNo": 10,
            "VisitorID": test_data['embarkSupervisorShip']['bulkImportResponse']['visitorId'],
            "Visits": [
                {
                    "AdditionalInfo": "",
                    "BoardingTypeCode": "GB",
                    "EndDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
                    "EndDateEpoch": test_data['gangway']['visitorStatus']['Visits'][0]['EndDateEpoch'],
                    "IsDeleted": False,
                    "PortCode": "ATSEA",
                    "PropertyID": "SC",
                    "Purpose": "Script Automation",
                    "SelectedIdentificationId": "c19890bc-45f7-4d8d-8f02-95cda0e9e087",
                    "StartDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
                    "StartDateEpoch": test_data['gangway']['visitorStatus']['Visits'][0]['StartDateEpoch'],
                    "StatusCode": "approved",
                    "SubmittedBy": test_data['embarkSupervisorShip']['submittedBy'],
                    "VisitID": test_data['embarkSupervisorShip']['bulkImportResponse']['visitId'],
                    "VisitReviewers": [
                        {
                            "IsDeleted": False,
                            "ReviewerTeamMemberID": test_data['embarkSupervisorShip']['submittedBy'],
                            "StatusCode": "approved",
                            "VisitID": test_data['embarkSupervisorShip']['bulkImportResponse']['visitId'],
                            "VisitReviewerID": test_data['embarkSupervisorShip']['submittedBy']
                        }
                    ]
                }
            ],
            "_rev": content_rev['_rev'],
            "boardingStatusChangedBy": test_data['embarkSupervisorShip']['submittedBy'],
            "channels": [
                "SC",
                "SC_emb_gw_t",
                "VisitorStatus",
                "SC_VisitorStatus"
            ],
            "lastModifiedBy": test_data['embarkSupervisorShip']['submittedBy'],
            "lastModifiedDate": f"{test_data['embarkSupervisorShip']['shipDate']}T18:18:24.294Z",
            "lastModifiedDateEpoch": test_data['gangway']['visitorStatus']['lastModifiedDateEpoch'],
            "sourceId": "CouchDatabase",
            "type": "VisitorStatus"
        }
        rest_ship.send_request(method='PUT', url=to_url, json=data, auth='crew')
        time.sleep(5)
        content_to_rev = rest_ship.send_request(method='GET', url=url, auth='Basic').content
        data['IsOnBoarded'] = False
        data['_rev'] = content_to_rev['_rev']
        rest_ship.send_request(method='PUT', url=to_url, json=data, auth='crew')
        contents = rest_ship.send_request(method='GET', url=url, auth='Basic').content
        assert not contents['IsOnBoarded'], "Visitor ashore status is automatically getting remove."

    @pytestrail.case(41005481)
    def test_88_search_boarding_slots(self, config, test_data, rest_ship):
        """
        Search boarding slots
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
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

    @pytestrail.case(41005476)
    def test_89_move_boarding_slot(self, config, test_data, rest_ship, db_core):
        """
        Move boarding slot
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": True
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
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
            "oldBoardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "oldBoardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime']
        }]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='DD' and voyagenumber ='{test_data['voyageNumber']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @pytestrail.case(64536845)
    def test_90_update_capacity_boarding_slot(self, config, test_data, rest_ship):
        """
        Update boarding slot capacity
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
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

        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('expectedGuestCount', _content[0])
            assert _content[0]['expectedGuestCount'] == test_data['embarkationSupervisor'][
                'expectedGuestCount'] + 50, "Updated Boarding Slot capacity is not getting reflected"
        else:
            raise Exception("Response is empty for updating slot capacity")

        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
                "embarkdate": f"{test_data['embarkDate']}T00:00:00",
                "shipcode": config.ship.code,
                "voyagenumber": test_data['voyageNumber']
                 }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        for slot in _content:
            if slot["boardingNumberId"] == test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId']:
                assert slot['expectedGuestCount'] == test_data['embarkationSupervisor'][
                        'expectedGuestCount'] + 50, "Boarding Slot capacity not updated."
                break
        else:
            raise Exception("Not able to find the boarding slot.")
        test_data['embarkationSupervisor']['expectedGuestCount'] += 50

    @pytestrail.case(64694664)
    def test_91_mark_boarding_slot_active(self, config, test_data, rest_ship):
        """
        Mark boarding slot as active
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }

        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['oldboardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['oldboardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isEnabled": True,
            "isDeleted": False,
            "isActive": True,
            "isReserved": False
        }]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('isActive', _content[0])
            assert _content[0]['isActive'], "Boarding Slot not marked as Active"
        else:
            raise Exception("Response is empty for marking slot as Active")

        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        for slot in _content:
            if slot["boardingNumberId"] == test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId']:
                assert slot['isActive'], "Boarding Slot not marked as Active"
                break
        else:
            raise Exception("Not able to find the boarding slot.")

    @pytestrail.case(64694699)
    def test_92_mark_boarding_slot_inactive(self, config, test_data, rest_ship):
        """
        Mark boarding slot as inactive
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }

        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['oldboardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['oldboardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isEnabled": True,
            "isDeleted": False,
            "isActive": False,
            "isReserved": False
        }]

        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('isActive', _content[0])
            assert not _content[0]['isActive'], "Boarding Slot not marked as Active"
        else:
            raise Exception("Response is empty for marking slot as Inactive.")

        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        for slot in _content:
            if slot["boardingNumberId"] == test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId']:
                assert not slot['isActive'], "Boarding Slot not marked as Inactive"
                break
        else:
            raise Exception("Not able to find the boarding slot.")

    @pytestrail.case(41005479)
    def test_93_disable_boarding_slot(self, config, test_data, rest_ship, db_core):
        """
        Disable boarding slot
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
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
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='DD' and voyagenumber ='{test_data['voyageNumber']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @pytestrail.case(41005478)
    def test_94_enable_boarding_slot(self, config, test_data, rest_ship, db_core):
        """
        Enable boarding slot
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
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
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='DD' and voyagenumber ='{test_data['voyageNumber']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @pytestrail.case(41005480)
    def test_95_remove_slot(self, config, test_data, rest_ship, db_core):
        """
        Remove boarding slot
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }
        body = [{
            "assignedGuestCount": 0,
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "checkedInGuestCount": 0,
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isActive": False,
            "isDeleted": True,
            "isEnabled": False,
            "onBoardedGuestCount": 0,
            "shipCode": config.ship.code,
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "voyageNumber": test_data['voyageNumber']
        }]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='DD' and voyagenumber ='{test_data['voyageNumber']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @pytestrail.case(41005477)
    def test_96_add_boarding_slot(self, config, test_data, rest_ship, db_core):
        """
        Add boarding slot
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/boardingnumber/update")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber'],
            "isMovingSlots": False
        }
        body = [{
            "boardingNumberId": test_data['embarkationSupervisor']['boarding_slot']['boardingNumberId'],
            "shipCode": config.ship.code,
            "voyageNumber": test_data['voyageNumber'],
            "effectiveFromDate": test_data['embarkDate'],
            "effectiveToDate": test_data['embarkDate'],
            "boardingSlotStartTime": test_data['embarkationSupervisor']['boardingSlotStartTime'],
            "boardingSlotEndTime": test_data['embarkationSupervisor']['boardingSlotEndTime'],
            "boardingNumber": test_data['embarkationSupervisor']['boardingNumber'],
            "slotNumber": test_data['embarkationSupervisor']['slotNumber'],
            "expectedGuestCount": test_data['embarkationSupervisor']['expectedGuestCount'],
            "isEnabled": True,
            "isDeleted": False,
            "isActive": False
        }]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        for _slots in _content:
            is_key_there_in_dict('boardingNumberId', _slots)
            is_key_there_in_dict('voyageNumber', _slots)
            is_key_there_in_dict('boardingSlotStartTime', _slots)
            is_key_there_in_dict('boardingSlotEndTime', _slots)

        _response = db_core.shore.run_and_fetch_data(
            query=f"SELECT * FROM boardingnumber WHERE shipcode ='DD' and voyagenumber ='{test_data['voyageNumber']}'")
        for _slot in range(0, len(_response)):
            if _content[0]['boardingNumberId'] == _response[_slot]['boardingnumberid']:
                break

    @pytestrail.case(64537075)
    def test_97_change_boarding_slot_for_sailor(self, config, test_data, rest_ship, guest_data):
        """
        Change boarding slot for sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception('No boarding slots are available')
        boarding_slots = []
        for slot in _content:
            if slot['boardingNumber'] not in boarding_slots:
                boarding_slots.append(slot['boardingNumber'])
        for guest in guest_data:
            url_for_sailor = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                                     f"/crew-embarkation-admin/reservation-guests/{guest['reservationGuestId']}")
            params_for_sailor = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url_for_sailor, params=params_for_sailor, auth="crew"). \
                content
            if len(_content['boardingNumbers']) != 0 and 'boardingNumber' in _content['boardingNumbers'][0]:
                if _content['boardingNumbers'][0]['boardingNumber'] in boarding_slots:
                    boarding_slots.remove(_content['boardingNumbers'][0]['boardingNumber'])

            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/slots')
            params = {
                "embarkdate": f"{test_data['embarkDate']}T00:00:00",
                "shipcode": config.ship.code,
                "voyagenumber": test_data['voyageNumber']
            }
            updated_boarding_slot = str(random.choice(boarding_slots))
            body = [
                {
                    "reservationGuestId": guest['reservationGuestId'],
                    "boardingNumber": updated_boarding_slot,
                    "slotNumber": updated_boarding_slot,
                    "shipCode": config.ship.code,
                    "embarkDate": f"{test_data['embarkDate']}T00:00:00",
                    "guestId": guest['guestId'],
                    "reservationId": guest['reservationId']
                }
            ]
            if len(_content['boardingNumbers']) != 0 and 'boardingNumber' in _content['boardingNumbers'][0]:
                body[0]["guestBoardingNumberId"] = _content['boardingNumbers'][0]['guestBoardingNumberId']
            rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew")
            _content = rest_ship.send_request(method="GET", url=url_for_sailor, params=params_for_sailor, auth="crew"). \
                content
            is_key_there_in_dict('boardingNumbers', _content)
            for boarding_number in _content['boardingNumbers']:
                if boarding_number['guestId'] == guest['guestId']:
                    assert boarding_number['boardingNumber'] == int(updated_boarding_slot),\
                        "Boarding number not updated for sailor"
                    assert boarding_number['slotNumber'] == int(updated_boarding_slot), \
                        "Boarding slot not updated for sailor"
                    break
            else:
                raise Exception(f"GuestId mismatch for sailor named {guest['FirstName']} {guest['LastName']} !!")

    @pytestrail.case(64540686)
    def test_98_import_ipm_list(self, config, test_data, rest_ship):
        """
        Import IPM list
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/gangway/in-port-manning/import")
        params = {
            'shipCode': config.ship.code
        }
        body = [{"positionNumber": "19",
                 "ipmPositionDepartments": [{"departmentKey": "Security", "departmentCode": "SECURITY"}],
                 "emergencyStation": "test", "inPort": True, "atAnchor": True, "shipCode": config.ship.code,
                 "ipmSafetyPositionDetails": [
                     {"safetyNo": "102", "groupCode": "A", "rank": "DECK OFFICER", "team": "OOW  ON DUTY"},
                     {"safetyNo": "342", "groupCode": "B", "rank": "DECK OFFICER", "team": "OOW  ON DUTY"},
                     {"safetyNo": "1045", "groupCode": "C", "rank": "DECK OFFICER", "team": "OOW  ON DUTY"},
                     {"safetyNo": "1065", "groupCode": "D", "rank": "DECK OFFICER", "team": "OOW  ON DUTY"}
                 ]},

                {"positionNumber": "22",
                 "ipmPositionDepartments": [{"departmentKey": "Sales", "departmentCode": "SALES"}],
                 "emergencyStation": "test", "inPort": True, "atAnchor": True, "shipCode": config.ship.code,
                 "ipmSafetyPositionDetails": [
                     {"safetyNo": "128", "groupCode": "A", "rank": "DECK TECHNICAL", "team": "ALLOW ON DUTY"},
                     {"safetyNo": "971", "groupCode": "D", "rank": "DECK TECHNICAL", "team": "ALLOW ON DUTY"},
                     {"safetyNo": "890", "groupCode": "C", "rank": "DECK TECHNICAL", "team": "ALLOW ON DUTY"},
                     {"safetyNo": "91", "groupCode": "B", "rank": "DECK TECHNICAL", "team": "ALLOW ON DUTY"}
                 ]},

                {"positionNumber": "23",
                 "ipmPositionDepartments": [{"departmentKey": "Bars", "departmentCode": "ENGINE"}],
                 "emergencyStation": "test", "inPort": True, "atAnchor": True, "shipCode": config.ship.code,
                 "ipmSafetyPositionDetails": [
                     {"safetyNo": "239", "groupCode": "D", "rank": "ENGINE OFFICER", "team": "ECR-POWER SYSTEM"},
                     {"safetyNo": "1360", "groupCode": "B", "rank": "ENGINE OFFICER", "team": "ECR-POWER SYSTEM"},
                     {"safetyNo": "105", "groupCode": "C", "rank": "ENGINE OFFICER", "team": "ECR-POWER SYSTEM"},
                     {"safetyNo": "1064", "groupCode": "A", "rank": "ENGINE OFFICER", "team": "ECR-POWER SYSTEM"}
                 ]}]

        _response = rest_ship.send_request(method="POST", json=body, url=url, params=params, auth="crew")
        assert _response.status_code == 201, f"Status code is {_response.status_code} instead of 201"
        _content = _response.content
        if len(_content) == 0:
            raise Exception("Getting a blank response")
        elif len(_content) != len(body):
            raise Exception("Data for some of the position numbers are missing")
        for ipm_position in _content:
            is_key_there_in_dict('positionNumber', ipm_position)
            is_key_there_in_dict('ipmPositionDepartments', ipm_position)
            is_key_there_in_dict('ipmSafetyPositionDetails', ipm_position)
            for position in body:
                if position["positionNumber"] == ipm_position['positionNumber']:
                    assert ipm_position['ipmPositionDepartments'][0]['departmentCode'] == position[
                        "ipmPositionDepartments"][0]['departmentCode'], f"Department Code not matching for " \
                                                    f"position number {_content[ipm_position]['positionNumber']}"
                    assert len(ipm_position['ipmSafetyPositionDetails']) == len(position["ipmSafetyPositionDetails"]),\
                        f"ipmSafetyPositionDetails not matching for" \
                        f"position number {_content[ipm_position]['positionNumber']}"

    @pytestrail.case(64694705)
    def test_99_verify_dashboard_approval_pending_count_after_new_visitor_creation(self, config, test_data, guest_data,
                                                                                   rest_ship):
        """
        Validate visitor Approval Pending count on dashboard after creating new visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        test_data['embarkSupervisorShip']['visitor_dashboard']['approvalPendingCount'] = _content['dashboard'][
                                                                        'visitorEmbarkStats']['approvalPendingCount']
        guest = 0
        test_data['embarkSupervisorShip']['companyName'] = "Decurtis"
        test_data['embarkSupervisorShip']['employeeNumber'] = str(
            generate_random_number(low=0, high=9999999999, include_all=True))
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
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
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
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
        }
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        time.sleep(3)
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        assert _content['dashboard']['visitorEmbarkStats']['approvalPendingCount'] == test_data['embarkSupervisorShip'][
            'visitor_dashboard']['approvalPendingCount'] + 1, "Visitor approval pending count on dashboard " \
            "is not changing after creating a new visitor"
        test_data['embarkSupervisorShip']['visitor_dashboard']['approvalPendingCount'] += 1

    @pytestrail.case(64694706)
    def test_100_verify_dashboard_approved_count_after_approving_visit(self, config, test_data, guest_data, rest_ship):
        """
        Validate visitor Approved count on dashboard after approving a visit
        :param config:
        :param test_data:
        "param guest_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {'page': 1, 'size': 99999}
        body = {
            "shipCode": config.ship.code,
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "reviewerTeamMemberIds": [test_data['embarkSupervisorShip']['reviewerTeamMemberId']]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('visitors', _content['_embedded'])
        for _visitor in _content['_embedded']['visitors']:
            is_key_there_in_dict('visits', _visitor)
            if 'employeeNumber' in _visitor and test_data['embarkSupervisorShip'][
                'employeeNumber'] == _visitor['employeeNumber']:
                test_data['embarkSupervisorShip']['visitorId'] = _visitor['visitorId']
                break

        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShip']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        is_key_there_in_dict('visits', _content)
        test_data['embarkSupervisorShip']['visitsBody'] = _content['visits']
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] = _content['dashboard'][
                                                                                'visitorEmbarkStats']['approved']
        test_data['embarkSupervisorShip']['visitor_dashboard']['approvalPendingCount'] = _content['dashboard'][
                                                                        'visitorEmbarkStats']['approvalPendingCount']

        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShip']['visitsBody']:
            body = [
                {
                    "visitorId": test_data['embarkSupervisorShip']['visitorId'],
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": _visits['visitorId'],
                            "startDate": f"{_visits['startDate']}T00:00:01",
                            "statusCode": "approved",
                            "portCode": "",
                            "boardingTypeCode": _visits['boardingType'],
                            "reviewerName": "Vertical QA",
                            "purpose": _visits['purpose'],
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": _visits['reviewerTeamMemberId'],
                            "reviewerEmail": "vertical-qa@decurtis.com",
                            "submittedBy": _visits['submittedBy']
                        }
                    ]
                }
            ]
            _content = rest_ship.send_request(method="POST", params=params, url=url, json=body, auth="crew").content
            is_key_there_in_dict('visits', _content[0])
            for visit in _content[0]['visits']:
                if visit['visitId'] == _visits['visitId']:
                    assert visit['statusCode'] == "approved", "Visit not marked as Approved."
                    break
            else:
                raise Exception("Visit Id not matching.")
        time.sleep(3)
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        assert _content['dashboard']['visitorEmbarkStats']['approved'] == test_data['embarkSupervisorShip'][
                        'visitor_dashboard']['approved'] + 1, "Visitor approval count on dashboard is not changing " \
                         "after approving a visitor."
        assert _content['dashboard']['visitorEmbarkStats']['approvalPendingCount'] == test_data['embarkSupervisorShip'][
            'visitor_dashboard']['approvalPendingCount'] - 1, "Visitor approval pending count on dashboard is not" \
            " changing after approving a pending approval visitor"
        test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] += 1
        test_data['embarkSupervisorShip']['visitor_dashboard']['approvalPendingCount'] -= 1

    @pytestrail.case(65132677)
    def test_101_verify_dashboard_rejected_count_after_rejecting_visit(self, config, test_data, guest_data, rest_ship):
        """
        Validate visitor rejected count on dashboard after rejecting a visit
        :param config:
        :param test_data:
        "param guest_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                       f"/crew-embarkation-admin/visitor/{test_data['embarkSupervisorShip']['visitorId']}")
        params = {
            'shipTime': f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            'shipCode': config.ship.code
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        test_data['embarkSupervisorShip']['visitsBody'] = _content['visits']

        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('teamMemberEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        test_data['embarkSupervisorShip']['visitor_dashboard']['rejected'] = _content['dashboard'][
                                                                                    'visitorEmbarkStats']['rejected']
        test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] = _content['dashboard'][
                                                                                    'visitorEmbarkStats']['approved']
        url = urljoin(getattr(config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/visitstatus")
        params = {
            'bulkApproval': 'false'
        }
        for _visits in test_data['embarkSupervisorShip']['visitsBody']:
            body = [
                {
                    "visitorId": _visits['visitorId'],
                    "reviewerName": _visits['reviewerName'],
                    "visits": [
                        {
                            "visitId": _visits['visitId'],
                            "visitorId": _visits['visitorId'],
                            "startDate": _visits['startDate'],
                            "statusCode": "rejected",
                            "portCode": "",
                            "boardingTypeCode": _visits['boardingType'],
                            "reviewerName": _visits['reviewerName'],
                            "purpose": _visits['purpose'],
                            "propertyId": config.ship.code,
                            "reviewerTeamMemberId": _visits['reviewerTeamMemberId'],
                            "reviewerEmail": _visits['submittedByEmail'],
                            "submittedBy": _visits['submittedBy'],
                            "visitReviewerId": _visits['visitReviewerId'],
                            "isDeleted": False
                        }
                    ]
                }
            ]
            rest_ship.send_request(method="POST", params=params, url=url, json=body, auth="crew")
        time.sleep(3)
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipTimeDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('teamMemberEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('visitorEmbarkStats', _content['dashboard'])
        assert _content['dashboard']['visitorEmbarkStats']['rejected'] == test_data['embarkSupervisorShip'][
            'visitor_dashboard']['rejected'] + 1, "Visitor rejected count on dashboard is not changing after" \
                                                  "          rejecting a visitor visit"
        assert _content['dashboard']['visitorEmbarkStats']['approved'] == test_data['embarkSupervisorShip'][
            'visitor_dashboard']['approved'] - 1, "Visitor approved count on dashboard is not" \
                " changing after rejecting an approved visitor visit."
        test_data['embarkSupervisorShip']['visitor_dashboard']['rejected'] += 1
        test_data['embarkSupervisorShip']['visitor_dashboard']['approved'] -= 1

    @pytestrail.case(65177680)
    def test_102_create_alert_for_bulk_sailors(self, config, test_data, guest_data, rest_ship):
        """
        Create alert for bulk sailors
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        bulk_Sailor_Details = []
        for guest in range(len(guest_data)):
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/reservation-guests/{guest_data[guest]['reservationGuestId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            is_key_there_in_dict('personId', _content)
            is_key_there_in_dict('reservationGuestId', _content)
            is_key_there_in_dict('reservationNumber', _content)
            is_key_there_in_dict('alerts', _content)
            is_key_there_in_dict('messages', _content)
            bulk_Sailor_Details.append(_content)
        test_data['embarkSupervisorShip']["bulkSailorDetails"] = bulk_Sailor_Details
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/alerts")
        body = {
            "alertTypeCode": "CBP",
            "departmentId": test_data['embarkSupervisorShip']['departmentId'],
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": True,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": bulk_Sailor_Details
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        is_key_there_in_dict('personAlerts', _content)
        is_key_there_in_dict('alertCreatedBy', _content)
        assert _content['personAlertCount'] == len(guest_data), "Person Alert Count not matching " \
                                                                "with no. of guests in guest data."
        test_data['embarkSupervisorShip']['alertResponse'] = _content
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      f"/crew-embarkation-admin/alerts/{test_data['embarkSupervisorShip']['alertResponse']['alertId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('persons', _content)
        is_key_there_in_dict('description', _content)
        is_key_there_in_dict('departmentId', _content)
        is_key_there_in_dict('alertTypeCode', _content)
        assert len(_content['persons']) == len(guest_data), f"Alert created for " \
                                                            f"only {len(_content['persons'])} guests."
        for person in _content["persons"]:
            for guest in guest_data:
                if person['personId'] == guest['reservationGuestId']:
                    assert person['fullName'] == f"{guest['FirstName']} {guest['LastName']}", f"Alert not created" \
                                                f" for guest {guest['FirstName']} {guest['LastName']} in guest data "
                    break
            else:
                raise Exception(f"Can not find person with name {person['fullName']} in the guest data.")

    @pytestrail.case(65561230)
    def test_103_create_message_for_bulk_sailors(self, config, test_data, guest_data, rest_ship):
        """
         Create message for bulk sailors
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), "/crew-embarkation-admin/messages")
        body = {
            "alertTypeCode": None,
            "departmentId": None,
            "description": "Script Automation",
            "endDate": f"{test_data['embarkSupervisorShip']['shipDate']}T23:59:59",
            "startDate": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01",
            "isOverridable": True,
            "isPriority": True,
            "isSoundEnabled": False,
            "createdBy": test_data['embarkSupervisorShip']['submittedBy'],
            "saveAsTemplate": False,
            "source": "GANGWAY-ADMIN",
            "isActive": False,
            "isDeleted": False,
            "updateTemplate": False,
            "persons": test_data['embarkSupervisorShip']["bulkSailorDetails"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('messageId', _content)
        is_key_there_in_dict('personMessages', _content)
        is_key_there_in_dict('personMessageCount', _content)
        is_key_there_in_dict('personMessageCount', _content)
        assert _content['personMessageCount'] == len(guest_data), "Person Message Count not" \
                                                                  " matching with no. of guests in guest data."
        test_data['embarkSupervisorShip']['messageResponse'] = _content
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                f"/crew-embarkation-admin/alerts/{test_data['embarkSupervisorShip']['messageResponse']['messageId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('alertId', _content)
        is_key_there_in_dict('persons', _content)
        is_key_there_in_dict('description', _content)
        assert len(_content['persons']) == len(guest_data), f"Message created for " \
                                                            f"only {len(_content['persons'])} guests in guest data."
        for person in _content["persons"]:
            for guest in guest_data:
                if person['personId'] == guest['reservationGuestId']:
                    assert person['fullName'] == f"{guest['FirstName']} {guest['LastName']}", f"Message not created" \
                                          f" for guest {guest['FirstName']} {guest['LastName']} in guest data "
                    break
            else:
                raise Exception(f"Can not find person with name {person['fullName']} in the guest data.")

    @pytestrail.case(65133489)
    def test_104_change_embark_slot_for_bulk_sailors(self, config, test_data, guest_data, rest_ship):
        """
        Change embark slot for bulk sailors
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "boardingnumber/search")
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception('No boarding slots are available')
        boarding_slots = []
        for slot in _content:
            if slot['boardingNumber'] not in boarding_slots:
                boarding_slots.append(slot['boardingNumber'])

        for guest in guest_data:
            url_for_sailor = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                                     f"/crew-embarkation-admin/reservation-guests/{guest['reservationGuestId']}")
            params_for_sailor = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url_for_sailor, params=params_for_sailor, auth="crew"). \
                content
            if 'boardingNumber' in _content['boardingNumbers'][0]:
                if _content['boardingNumbers'][0]['boardingNumber'] in boarding_slots:
                    boarding_slots.remove(_content['boardingNumbers'][0]['boardingNumber'])

        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/slots')
        params = {
            "embarkdate": f"{test_data['embarkDate']}T00:00:00",
            "shipcode": config.ship.code,
            "voyagenumber": test_data['voyageNumber']
            }
        updated_boarding_slot = str(random.choice(boarding_slots))
        guest_details = test_data['embarkSupervisorShip']['bulkSailorDetails']
        body = []
        for guest in guest_details:
            body_for_guest = {
                "guestBoardingNumberId": guest['boardingNumbers'][0]['guestBoardingNumberId'],
                "reservationGuestId": guest['reservationGuestId'],
                "boardingNumber": updated_boarding_slot,
                "slotNumber": updated_boarding_slot,
                "shipCode": config.ship.code,
                "embarkDate": f"{test_data['embarkDate']}T00:00:00",
                "guestId": guest['boardingNumbers'][0]['guestId'],
                "reservationId": guest['boardingNumbers'][0]['reservationId']
            }
            body.append(body_for_guest)

        rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew")
        for guest in guest_data:
            url_for_sailor = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                                     f"/crew-embarkation-admin/reservation-guests/{guest['reservationGuestId']}")
            params_for_sailor = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url_for_sailor, params=params_for_sailor,
                                              auth="crew").content
            is_key_there_in_dict('boardingNumbers', _content)
            for boarding_number in _content['boardingNumbers']:
                if boarding_number['guestId'] == guest['guestId']:
                    assert boarding_number['boardingNumber'] == int(
                        updated_boarding_slot), f"Boarding slot not updated for sailor {_content['fullName']}"
                    assert boarding_number['slotNumber'] == int(
                        updated_boarding_slot), f"Boarding slot not updated for sailor {_content['fullName']}"
                    break
            else:
                raise Exception(f"GuestId mismatch for {_content['fullName']} sailor.")

    @pytestrail.case(65561231)
    def test_105_validate_status_percentage_for_sailor_tiles_on_dashboard(self, config, test_data, rest_ship):
        """
        Validate the status percentage for sailor tiles on dashboard
        :param config:
        :param test_data:
        :param rest_ship:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T19:00:00",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T06:30:00",
            "voyageNumber": test_data['embarkSupervisorShip']['voyageNumber'],
            "shipTime": f"{test_data['aci']['currentDate']}",
            "status": ["COMPLETED", "ASHORE", "ONBOARD"], "statusTypeCode": ["TC", "BS"]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('dashboard', _content)
        is_key_there_in_dict('guestEmbarkStats', _content['dashboard'])
        is_key_there_in_dict('percentages', _content['dashboard']['guestEmbarkStats'])
        percentages = _content['dashboard']['guestEmbarkStats']['percentages']
        counts = _content['dashboard']['guestEmbarkStats']
        percnt_CheckedIn_NotOnboard = round(counts['checkedInAshore'] / counts['totalOccupancy'] * 100, 1)
        percnt_CheckedIn_Onboard = round(counts['checkedInOnboard'] / counts['totalOccupancy'] * 100, 1)
        percnt_RTSComplete_Approved = round(counts['ociDoneAndApproved'] / counts['totalOccupancy'] * 100, 1)
        percnt_RTSComplete_ApprovalPending = round(counts['ociDoneAndPending'] / counts['totalOccupancy'] * 100, 1)
        percnt_RTS_NotCompleted = round(counts["ociNotDone"] / counts['totalOccupancy'] * 100, 1)
        percnt_NotCheckedIn_Onbaord = round(counts["notCheckedInOnboard"] / counts['totalOccupancy'] * 100, 1)

        assert percnt_CheckedIn_NotOnboard == percentages[
                                            "checkedInAshore"], "CheckedIn NotOnboard Percentage not matching."
        assert percnt_CheckedIn_Onboard == percentages[
                                            "checkedInOnboard"], "CheckedIn Onboard Percentage not matching."
        assert percnt_RTSComplete_Approved == percentages[
                                        "ociDoneAndApproved"], "RTS Complete & Approved Percentage not matching."
        assert percnt_RTSComplete_ApprovalPending == percentages[
                                    "ociDoneAndPending"], "RTSComplete & ApprovalPending percentage not matching."
        assert percnt_RTS_NotCompleted == percentages[
                                        "ociNotDone"], "RTS NotCompleted percentage not matching."
        assert percnt_NotCheckedIn_Onbaord == percentages[
                                        "notCheckedInOnboard"], "NotCheckedIn Onbaord percentage not matching."

    @pytestrail.case(65561228)
    def test_106_verify_sailor_list_as_per_reservation_parties(self, config, test_data, rest_ship):
        """
        Verify user is able to see complete sailor list as per their reservation parties
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/reservation-guests/search')
        params = {
            'page': 1,
            'size': 9999999
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": [],
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        reservation_guest_ids = []
        if len(_content["reservationGuests"]) != 0:
            for _guests in _content['reservationGuests']:
                is_key_there_in_dict('reservationGuestId', _guests)
                reservation_guest_ids.append(_guests['reservationGuestId'])
        else:
            raise Exception("Getting empty response in Reservation Guests")

        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "gangway/persons/search")
        params = {
            "page": 1,
            "size": 9999999
        }
        body = {
            "fromDate": f"{test_data['embarkSupervisorShip']['embarkDate']}T00:00:01",
            "toDate": f"{test_data['embarkSupervisorShip']['debarkDate']}T23:59:59",
            "reservationStatusCodes": [],
            "includePartyForReservationGuestIds": reservation_guest_ids,
            "includeIdentification": True,
            "shipTime": f"{test_data['embarkSupervisorShip']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        is_key_there_in_dict('personsSearchResult', _content['_embedded'])
        if len(_content['_embedded']['personsSearchResult']) != 0:
            for reservation_number, guests in _content['_embedded']['personsSearchResult'].items():
                for guest in guests:
                    assert guest['reservationNumber'] == reservation_number, f"Reservation number not matching for" \
                                             f" guest named {guest['firstName']} {guest['lastName']} having " \
                                             f"reservation number {guest['reservationNumber']}"
        else:
            raise Exception("Getting empty search results for sailors as per reservation parties.")

    @pytestrail.case(65561232)
    def test_107_verify_no_duplicate_visit_of_same_day_for_visitor(self, config, test_data, guest_data, rest_ship):
        """
        Verify user should not be able to create duplicate visit of same day for visitor
        :param config:
        :param test_data:
        "param guest_data:
        :param rest_ship:
        """
        guest = 0
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
            "dateOfBirth": f"{guest_data[guest]['birthDate']}T18:30:00.000Z",
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
            "birthDate": f"{guest_data[guest]['birthDate']}T00:00:00"
        }
        try:
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            raise Exception("Able to create Duplicate Visits of same day for a visitor")
        except Exception as exp:
            if "400" and "duplicate visit" in exp.args[0].lower():
                pass
            else:
                raise Exception("Not getting error for Duplicate visit while trying to create a duplicate visit.")
