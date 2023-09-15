__author__ = "vikesh"

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.INCIDENT_MANAGEMENT
@pytest.mark.run(order=41)
class TestIncident:
    """
    Test Suite to create incident
    """

    @pytestrail.case('43698114')
    def test_01_create_incident(self, config, test_data, rest_ship):
        """
        Creating new incident
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        body = {
            "propertyId": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents/teammembers')
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        team_member = []
        for team_members in _content:
            team_member.append(team_members['teamMemberId'])
            if team_members['firstName'] == 'Shubhra' and team_members['lastName'] == 'Vyas':
                test_data['loggedInCrew'] = team_members['teamMemberId']
        team_member_id = random.choice(team_member)
        test_data['teamMembers'] = team_member
        sla_time = [30, 60, 240, 600, 1440]
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents')
        body = {
            "propertyId": config.ship.code,
            "incidentCategoryCode": "CRUF",
            "description": generate_random_string(),
            "status": "ASSIGNED",
            "reporterType": "G",
            "stateroom": "",
            "reportedByPersonId": test_data['personId'],
            "assignedToTeamMemberId": team_member_id,
            "voyageNumber": test_data["voyageNumber"],
            "severity": generate_random_number(low=1, high=3, include_all=True),
            "priority": generate_random_number(low=1, high=5, include_all=True),
            "resolutionDescription": "",
            "currencyCode": "USD",
            "resolutionAmount": generate_random_number(low=1, high=200, include_all=True),
            "resolutionTime": random.choice(sla_time),
            "impactedGuest": "",
            "attendedByNotes": generate_random_string(),
            "raisedByNotes": generate_random_string(),
            "externalReferenceId": "test",
            "globalVenueId": test_data['venueId'],
            "incidentMedias": [],
            "isNotify": True,
            "departmentCode": "SAILOR_SERVICES"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('incidentId', _content)
        is_key_there_in_dict('incidentReferenceId', _content)
        test_data["incidentId"] = _content["incidentId"]

    @pytestrail.case('43698115')
    def test_02_search_incident(self, config, test_data, rest_ship):
        """
        verify created incident
        :params config
        :params test_data
        :params rest_ship
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents/search')
        params = {
            "page": 1,
            "size": 20
        }
        body = {
            "stateroom": None,
            "createdByTeamMemberId": "",
            "minAmount": "",
            "maxAmount": "",
            "voyageNumber": test_data['voyageNumber'],
            "guestTypeCodes": [],
            "departmentCodes": [],
            "statuses": [],
            "isOverdue": False,
            "isAtRisk": False,
            "isPending": False,
            "isVip": False,
            "atRiskDuration": "",
            "pendingDuration": "",
            "globalVenueId": None,
            "sortByLoyaltyLevel": True,
            "sortByAtRisk": False,
            "sortBySeverity": False,
            "sortByPriority": False,
            "sortByCreationDate": False,
            "sortByStatusChangedDate": False,
            "propertyId": config.ship.code
        }
        incident = []
        while True:
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            incident.extend(_content["_embedded"]["incidentDToes"])
            if _content['page']['number'] >= _content['page']['totalPages']:
                break
            else:
                params['page'] += 1
        test_data['staterooms'] = []
        for person in _content['_embedded']['incidentDToes']:
            test_data['staterooms'].append(person['stateroom'])
        incidentid = False
        for incident_id in incident:
            if incident_id["incidentId"] == test_data["incidentId"]:
                incidentid = True
                break
        if not incidentid:
            raise Exception("incidentId not found")

    @pytestrail.case('46374267')
    def test_03_reassign_incident(self, config, test_data, rest_ship):
        """
        Reassign the incident
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f"/incidents/{test_data['incidentId']}")
        team_member_id = random.choice(test_data['teamMembers'])
        body = {
            "incidentId": test_data['incidentId'],
            "statusChangedBy": test_data['loggedInCrew'],
            "statusChangedByPersonTypeCode": "C",
            "attendedByNotes": "",
            "status": "ASSIGNED",
            "assignedToTeamMemberId": team_member_id
        }
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content

        _content = rest_ship.send_request(method="GET", url=url, json=body, auth="crew").content
        is_key_there_in_dict('incidentId', _content)
        assert _content["assignedToTeamMemberId"] == team_member_id, "Incident reassignment not work"
        assert _content["statusChangedBy"] == test_data['loggedInCrew'], "Status Changed by not matched"

    @pytestrail.case('46374270')
    def test_04_edit_severity_priority(self, config, test_data, rest_ship):
        """
        Edit the new created incident severity and Priority
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f"/incidents/{test_data['incidentId']}")
        severity = generate_random_number(low=1, high=3, include_all=True)
        priority = generate_random_number(low=1, high=5, include_all=True)
        body = {
            "incidentId": test_data['incidentId'],
            "severity": severity,
            "priority": priority
        }
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content

        _content = rest_ship.send_request(method="GET", url=url, json=body, auth="crew").content
        is_key_there_in_dict('incidentId', _content)
        assert _content["severity"] == severity, "Severity is not updated"
        assert _content["priority"] == priority, "Priority is not updated"

    @pytestrail.case('46374268')
    def test_05_create_incident_for_himself(self, config, test_data, rest_ship):
        """
        Creating new incident for him self
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        sla_time = [30, 60, 240, 600, 1440]
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents')
        body = {
            "propertyId": config.ship.code,
            "incidentCategoryCode": "CRUF",
            "description": generate_random_string(),
            "status": "ASSIGNED",
            "reporterType": "G",
            "stateroom": "",
            "reportedByPersonId": test_data['personId'],
            "assignedToTeamMemberId": test_data['loggedInCrew'],
            "voyageNumber": test_data["voyageNumber"],
            "severity": generate_random_number(low=1, high=3, include_all=True),
            "priority": generate_random_number(low=1, high=5, include_all=True),
            "resolutionDescription": "",
            "currencyCode": "USD",
            "resolutionAmount": generate_random_number(low=1, high=200, include_all=True),
            "resolutionTime": random.choice(sla_time),
            "impactedGuest": "",
            "attendedByNotes": generate_random_string(),
            "raisedByNotes": generate_random_string(),
            "externalReferenceId": "test",
            "globalVenueId": test_data['venueId'],
            "incidentMedias": [],
            "isNotify": True,
            "departmentCode": "SAILOR_SERVICES"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['incidentContent'] = _content
        is_key_there_in_dict('incidentId', _content)
        is_key_there_in_dict('incidentReferenceId', _content)
        assert _content['assignedToTeamMemberId'] == test_data['loggedInCrew'], "Crew not able to assign the " \
                                                                                "Incident for him self"
        test_data["himself_incidentId"] = _content["incidentId"]

    @pytestrail.case('46374271')
    def test_06_verify_incident_date_time(self, test_data):
        """
        Test cases to verify the created incident have correct date and time
        :param test_data:
        :return:
        """
        _content = test_data['incidentContent']
        today_date = datetime.now().strftime('%Y-%m-%d')
        creation_date = _content['creationTime'].split('T')[0]
        assert today_date == creation_date, "Incident creation date is correct"

    @pytestrail.case('46374269')
    def test_07_filter_incident(self, config, test_data, rest_ship):
        """
        Filter the Incident on the basis of assigned team member
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents/search')
        params = {
            "page": 1,
            "size": 20
        }
        body = {
            "createdByTeamMemberId": "",
            "minAmount": "",
            "maxAmount": 500,
            "voyageNumber": test_data["voyageNumber"],
            "guestTypeCodes": [],
            "departmentCodes": [],
            "statuses": [
                "ASSIGNED"
            ],
            "isOverdue": False,
            "isAtRisk": False,
            "isPending": False,
            "isVip": False,
            "atRiskDuration": "",
            "pendingDuration": "",
            "sortByLoyaltyLevel": True,
            "sortByAtRisk": False,
            "sortBySeverity": False,
            "sortByPriority": False,
            "sortByCreationDate": False,
            "assignedToTeamMemberIds": [
                test_data['loggedInCrew']
            ],
            "sortByStatusChangedDate": False,
            "propertyId": config.ship.code
        }

        incident = []
        while True:
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            incident.extend(_content["_embedded"]["incidentDToes"])
            if _content['page']['number'] >= _content['page']['totalPages']:
                break
            else:
                params['page'] += 1
        for assignedToTeamMemberId in incident:
            assert assignedToTeamMemberId["assignedToTeamMemberId"] == \
                   test_data['loggedInCrew'], "Filter not working for Assigned team member"

    @pytestrail.case('46374266')
    def test_08_close_incident(self, config, test_data, rest_ship):
        """
        Test case to close the Incident
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f"/incidents/{test_data['incidentId']}")
        body = {
            "incidentId": test_data["incidentId"],
            "statusChangedBy": test_data['loggedInCrew'],
            "statusChangedByPersonTypeCode": "C",
            "attendedByNotes": "Closing the Incident by Automation Flow",
            "status": "CLOSED-RESOLVED",
            "isNotify": False
        }
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content

        _content = rest_ship.send_request(method="GET", url=url, json=body, auth="crew").content
        is_key_there_in_dict('status', _content)
        assert _content['status'] == "CLOSED-RESOLVED", f"test_data['incidentId'] not closed"

    @pytestrail.case(69242423)
    def test_09_reopen_closed_incident(self, config, test_data, rest_ship):
        """
        To verify Crew is able to Re-open the Closed Incidents
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), f"/incidents/{test_data['incidentId']}")
        body = {
            "incidentId": test_data["incidentId"],
            "statusChangedBy": test_data['loggedInCrew'],
            "statusChangedByPersonTypeCode": "C",
            "status": "UNASSIGNED",
            "isNotify": False,
            "assignedToTeamMemberId": None
        }
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content

        _content = rest_ship.send_request(method="GET", url=url, json=body, auth="crew").content
        is_key_there_in_dict('status', _content)
        assert _content['status'] == "UNASSIGNED", "Closed Incident not Re-opened"

    @pytestrail.case(64545238)
    def test_10_history_counts(self, config, test_data, rest_ship):
        """
        To verify while adding incident, number increases in history (all incidents)
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url_count = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        body_count = {"propertyId": config.ship.code,
                      "statuses": ["ACKNOWLEDGED", "ASSIGNED", "CLOSED-RESOLVED", "UNASSIGNED", "CLOSED-DUPLICATE",
                                   "CLOSED-UNRESOLVED", "ASSIGNED", "IN-PROGRESS", "RE-ASSIGNED"],
                      "stateroom": 'null',
                      "globalVenueId": 'null',
                      "isAtRisk": 'true',
                      "isVip": 'true',
                      "isOverdue": 'true',
                      "isPending": 'true',
                      "isAllCountRequired": 'true',
                      "voyageNumber": test_data["voyageNumber"],
                      "departmentCodes": []
                      }
        _content = rest_ship.send_request(method="POST", url=url_count, json=body_count, auth="crew").content
        is_key_there_in_dict('overdueCount', _content)
        is_key_there_in_dict('atRiskCount', _content)
        is_key_there_in_dict('pendingCount', _content)
        is_key_there_in_dict('vipCount', _content)
        is_key_there_in_dict('totalCount', _content)
        current_count = _content['totalCount']
        body = {
            "propertyId": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents/teammembers')
        _content_incident = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        team_member = []
        for team_members in _content_incident:
            team_member.append(team_members['teamMemberId'])
            if team_members['firstName'] == 'Shubhra' and team_members['lastName'] == 'Vyas':
                test_data['loggedInCrew'] = team_members['teamMemberId']
        team_member_id = random.choice(team_member)
        test_data['teamMembers'] = team_member
        sla_time = [30, 60, 240, 600, 1440]
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), '/incidents')
        body = {
            "propertyId": config.ship.code,
            "incidentCategoryCode": "CRUF",
            "description": generate_random_string(),
            "status": "ASSIGNED",
            "reporterType": "G",
            "stateroom": "",
            "reportedByPersonId": test_data['personId'],
            "assignedToTeamMemberId": team_member_id,
            "voyageNumber": test_data["voyageNumber"],
            "severity": generate_random_number(low=1, high=3, include_all=True),
            "priority": generate_random_number(low=1, high=5, include_all=True),
            "resolutionDescription": "",
            "currencyCode": "USD",
            "resolutionAmount": generate_random_number(low=1, high=200, include_all=True),
            "resolutionTime": random.choice(sla_time),
            "impactedGuest": "",
            "attendedByNotes": generate_random_string(),
            "raisedByNotes": generate_random_string(),
            "externalReferenceId": "test",
            "globalVenueId": test_data['venueId'],
            "incidentMedias": [],
            "isNotify": True,
            "departmentCode": "SAILOR_SERVICES"
        }
        _content_new = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('incidentId', _content_new)
        is_key_there_in_dict('incidentReferenceId', _content_new)
        test_data["incidentId"] = _content_new["incidentId"]
        _new_count = rest_ship.send_request(method="POST", url=url_count, json=body_count, auth="crew").content
        assert _new_count['totalCount'] > current_count, "count does not increase after adding an incident"

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(64545239)
    def test_11_search_by_first_name(self, config, test_data, rest_ship):
        """
        To search incident by guest First Name
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/findBySearchParam")
        body = {"propertyId": config.ship.code,
                "voyageNumber": test_data['voyageNumber'],
                "departmentCodes": [],
                "searchText": test_data['guest_details']['firstName']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for person in _content:
            assert person["guestFirstName"] == test_data['guest_details']['firstName'], 'first name not found'

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(64726273)
    def test_12_search_by_last_name(self, config, test_data, rest_ship):
        """
        To search incident by guest last Name
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/findBySearchParam")
        body = {"propertyId": config.ship.code,
                "voyageNumber": test_data['voyageNumber'],
                "departmentCodes": [],
                "searchText": test_data['guest_details']['lastName']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for person in _content:
            assert person["guestLastName"] == test_data['guest_details']['lastName'], 'last name not found'

    @pytestrail.case(64726274)
    def test_13_search_by_reference_id(self, config, test_data, rest_ship):
        """
        To search incident by guest Reference ID
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/findBySearchParam")
        body = {"propertyId": config.ship.code,
                "voyageNumber": test_data['voyageNumber'],
                "departmentCodes": [],
                "searchText": test_data['incidentContent']['incidentReferenceId']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for person in _content:
            assert person["incidentReferenceId"] == test_data['incidentContent']['incidentReferenceId'], \
                                                              'VIR ID not found'

    @pytestrail.case(64726306)
    def test_14_search_by_cabin_number(self, config, test_data, rest_ship):
        """
        To search incident by guest Cabin number
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/findBySearchParam")
        body = {"propertyId": config.ship.code,
                "voyageNumber": test_data['voyageNumber'],
                "departmentCodes": [],
                "searchText": test_data['cabinNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for person in _content:
            assert person["cabin"] == test_data['cabinNumber'], 'Cabin Number not found'

    @pytestrail.case(64726307)
    def test_15_verify_pdf_download(self, config, test_data, rest_ship):
        """
        To verify that pdf file is downloaded from history page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search/pdf")
        params = {
            "base url": "https%3A%2F%2Fapplication-integration.ship.virginvoyages.com"
        }
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data['voyageNumber'],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": ["CLOSED-RESOLVED"],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": False,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "sortByStatusChangedDate": True,
                "propertyId": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('PDF Not Received')

    @pytestrail.case(64726308)
    def test_16_verify_excel_download(self, config, test_data, rest_ship):
        """
        To verify that excel file is downloaded from history page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search/xlsx")
        params = {
            "base url": "https%3A%2F%2Fapplication-integration.ship.virginvoyages.com"
                 }
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data['voyageNumber'],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": ["CLOSED-RESOLVED"],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": False,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "sortByStatusChangedDate": True,
                "propertyId": config.ship.code}
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('Excel Not Received')

    @pytestrail.case(65320612)
    def test_17_filter_history_by_date_range(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the incidents in history using 'date range' option
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        current_date = datetime.now().strftime("%Y-%m-%d")
        previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        body = {"propertyId": config.ship.code,
                "staterooms": test_data['staterooms'],
                "globalVenueIds": [],
                "voyageNumber": test_data["voyageNumber"],
                "departmentCodes": [],
                "&start": previous_date,
                "&end": current_date
                }
        _content = rest_ship.send_request(method="POST", json=body, url=_url, auth="crew").content
        if len(_content) != 0:
            pass
        else:
            raise Exception("no chat conversation history available to filter")

    @pytestrail.case(65386102)
    def test_18_get_teams(self, config, test_data, rest_ship):
        """
        To verify that Team page is visible
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/lookup_min")
        param = {"shipcode": config.ship.code}
        _content = rest_ship.send_request(method="GET", params=param, url=_url, auth="crew").content
        is_key_there_in_dict('departments', _content)
        assert _content["departments"] != 0, 'Team page not found'

    @pytestrail.case(65386069)
    def test_19_get_vip_counts(self, config, test_data, rest_ship):
        """
        To validate the number of VIP Category
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": False,
                "isVip": True,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "propertyId": config.ship.code}
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        body_get = {"voyageNumber": test_data["voyageNumber"],
                    "statuses": ["ACKNOWLEDGED", "ASSIGNED", "CLOSED-RESOLVED", "UNASSIGNED",
                                 "CLOSED-DUPLICATE", "CLOSED-UNRESOLVED", "ASSIGNED", "IN-PROGRESS", "RE-ASSIGNED"],
                    "stateroom": None,
                    "globalVenueId": None,
                    "isAtRisk": True,
                    "isVip": True,
                    "isOverdue": True,
                    "isPending": True,
                    "isAllCountRequired": True,
                    "propertyId": config.ship.code,
                    "departmentCodes": []
                    }
        _content_get = rest_ship.send_request(method="POST", json=body_get, url=_url_get, auth="crew").content
        assert _content_get['vipCount'] == _content['page']['totalElements'], 'VIP Count not matched'

    @pytestrail.case(65386101)
    def test_20_get_overdue_counts(self, config, test_data, rest_ship):
        """
        To validate the number of Overdue Category
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": True,
                "isAtRisk": False,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        body_get = {"voyageNumber": test_data["voyageNumber"],
                    "statuses": ["ACKNOWLEDGED", "ASSIGNED", "CLOSED-RESOLVED", "UNASSIGNED",
                                 "CLOSED-DUPLICATE", "CLOSED-UNRESOLVED", "ASSIGNED", "IN-PROGRESS", "RE-ASSIGNED"],
                    "stateroom": None,
                    "globalVenueId": None,
                    "isAtRisk": True,
                    "isVip": True,
                    "isOverdue": True,
                    "isPending": True,
                    "isAllCountRequired": True,
                    "propertyId": config.ship.code,
                    "departmentCodes": []
                    }
        _content_get = rest_ship.send_request(method="POST", json=body_get, url=_url_get, auth="crew").content
        assert _content_get['overdueCount'] == _content['page']['totalElements'], 'Overdue Count not matched'

    @pytestrail.case(65386231)
    def test_21_get_at_risk_counts(self, config, test_data, rest_ship):
        """
        To validate the number of at_risk Category
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": True,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        body_get = {"voyageNumber": test_data["voyageNumber"],
                    "statuses": ["ACKNOWLEDGED", "ASSIGNED", "CLOSED-RESOLVED", "UNASSIGNED",
                                 "CLOSED-DUPLICATE", "CLOSED-UNRESOLVED", "ASSIGNED", "IN-PROGRESS", "RE-ASSIGNED"],
                    "stateroom": None,
                    "globalVenueId": None,
                    "isAtRisk": True,
                    "isVip": True,
                    "isOverdue": True,
                    "isPending": True,
                    "isAllCountRequired": True,
                    "propertyId": config.ship.code,
                    "departmentCodes": []
                    }
        _content_get = rest_ship.send_request(method="POST", json=body_get, url=_url_get, auth="crew").content
        assert _content_get['atRiskCount'] == _content['page']['totalElements'], 'At Risk Count not matched'

    @pytestrail.case(65386232)
    def test_22_get_pending_counts(self, config, test_data, rest_ship):
        """
        To validate the number of pending Category
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": True,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/counts")
        body_get = {"voyageNumber": test_data["voyageNumber"],
                    "statuses": ["ACKNOWLEDGED", "ASSIGNED", "CLOSED-RESOLVED", "UNASSIGNED",
                                 "CLOSED-DUPLICATE", "CLOSED-UNRESOLVED", "ASSIGNED", "IN-PROGRESS", "RE-ASSIGNED"],
                    "stateroom": None,
                    "globalVenueId": None,
                    "isAtRisk": True,
                    "isVip": True,
                    "isOverdue": True,
                    "isPending": True,
                    "isAllCountRequired": True,
                    "propertyId": config.ship.code,
                    "departmentCodes": []
                    }
        _content_get = rest_ship.send_request(method="POST", json=body_get, url=_url_get, auth="crew").content
        assert _content_get['pendingCount'] == _content['page']['totalElements'], 'Pending Count not matched'

    @pytestrail.case(65386233)
    def test_23_to_check_pending_incidents_not_closed(self, config, test_data, rest_ship):
        """
        To validate that pending incidents are non-closed incidents
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": True,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "parentIncidentCategory": [],
                "incidentCategoryCodes": [],
                "globalVenueIds": [],
                "fromDate": None,
                "toDate": None,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for incidents in _content['_embedded']['incidentDToes']:
                if incidents['status'] != 'CLOSED-RESOLVED' or incidents['status'] != 'CLOSED-UNRESOLVED':
                    pass
                else:
                    raise Exception('Pending Incidents are found Closed')
        else:
            pytest.skip(msg="No Records found for Validation")

    @pytestrail.case(65386234)
    def test_24_to_check_overdue_incidents_not_closed(self, config, test_data, rest_ship):
        """
        To validate that overdue incidents are non-closed incidents
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": True,
                "isAtRisk": False,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "parentIncidentCategory": [],
                "incidentCategoryCodes": [],
                "globalVenueIds": [],
                "fromDate": None,
                "toDate": None,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for incidents in _content['_embedded']['incidentDToes']:
                if incidents['status'] != 'CLOSED-RESOLVED' or incidents['status'] != 'CLOSED-UNRESOLVED':
                    pass
                else:
                    raise Exception('Overdue Incidents are found Closed')
        else:
            pytest.skip(msg="No Records found for Validation")

    @pytestrail.case(65386235)
    def test_25_to_check_vip_incidents_not_closed(self, config, test_data, rest_ship):
        """
        To validate that VIP incidents are non-closed incidents
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": False,
                "isPending": False,
                "isVip": True,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "parentIncidentCategory": [],
                "incidentCategoryCodes": [],
                "globalVenueIds": [],
                "fromDate": None,
                "toDate": None,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for incidents in _content['_embedded']['incidentDToes']:
                if incidents['status'] != 'CLOSED-RESOLVED' or incidents['status'] != 'CLOSED-UNRESOLVED':
                    pass
                else:
                    raise Exception('VIP Incidents are found Closed')
        else:
            pytest.skip(msg="No Records found for Validation")

    @pytestrail.case(65878340)
    def test_26_to_check_at_risk_incidents_not_closed(self, config, test_data, rest_ship):
        """
        To validate that At Risk incidents are non-closed incidents
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "/incidents/search")
        param = {"page": 1, "size": 100}
        body = {"stateroom": None,
                "createdByTeamMemberId": "",
                "minAmount": "",
                "maxAmount": "",
                "voyageNumber": test_data["voyageNumber"],
                "guestTypeCodes": [],
                "departmentCodes": [],
                "statuses": [],
                "isOverdue": False,
                "isAtRisk": True,
                "isPending": False,
                "isVip": False,
                "atRiskDuration": "",
                "pendingDuration": "",
                "globalVenueId": None,
                "sortByLoyaltyLevel": True,
                "sortByAtRisk": False,
                "sortBySeverity": False,
                "sortByPriority": False,
                "sortByCreationDate": False,
                "parentIncidentCategory": [],
                "incidentCategoryCodes": [],
                "globalVenueIds": [],
                "fromDate": None,
                "toDate": None,
                "propertyId": config.ship.code
                }
        _content = rest_ship.send_request(method="POST", params=param, json=body, url=_url, auth="crew").content
        if _content['page']['totalElements'] != 0:
            for incidents in _content['_embedded']['incidentDToes']:
                if incidents['status'] != 'CLOSED-RESOLVED' or incidents['status'] != 'CLOSED-UNRESOLVED':
                    pass
                else:
                    raise Exception('At Risk Incidents are found Closed')
        else:
            pytest.skip(msg="No Records found for Validation")
