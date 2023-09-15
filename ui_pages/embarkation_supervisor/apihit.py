__author__ = 'prahlad.sharma'

from virgin_utils import *


class Apihit:
    """
    Page Class for Embarkation Supervisor/Visitor Management Dashboard page
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

    def get_ship_date(self):
        """
        Function to get the ship date
        """
        params = {"shipcode": self.config.ship.code}
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        self.test_data['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())

    def get_sailor_details(self):
        """
        Function to get the sailor details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/reservation-guests/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        for _guests in _content['reservationGuests']:
            if _guests['stateroom'] != 'GTY':
                self.test_data['searched_sailor_fn'] = _guests['firstName']
                self.test_data['searched_sailor_ln'] = _guests['lastName']
                self.test_data['searched_sailor_stateroom'] = _guests['stateroom']
                self.test_data['searched_sailor_booking'] = _guests['reservationNumber']
                break

        self.test_data[
            'searched_sailor_name'] = f"{self.test_data['searched_sailor_fn']} {self.test_data['searched_sailor_ln']}"

    def get_crew_details(self):
        """
        Function to get the crew details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/team-members/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        if len(_content['teamMembers']) == 0:
            raise Exception('No crew member available in active voyage')
        for _crew in _content['teamMembers']:
            self.test_data['searched_crew_fn'] = _crew['firstName']
            self.test_data['searched_crew_ln'] = _crew['lastName']
            self.test_data['searched_crew_emp_num'] = _crew['teamMemberNumber']
            break

        self.test_data[
            'searched_crew_name'] = f"{self.test_data['searched_crew_fn']} {self.test_data['searched_crew_ln']}"

    def get_visitor_details(self):
        """
        Function to get the visitor details
        """
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {'size': '10'}
        body = {"shipCode": self.config.ship.code, "startDate": f"{self.test_data['firstDay']}T00:00:01",
                "endDate": f"{self.test_data['lastDay']}T23:59:59"}
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('visitors', _content['_embedded'])
        for visitor in _content['_embedded']['visitors']:
            self.test_data['searched_fn'] = visitor['firstName']
            self.test_data['searched_ln'] = visitor['lastName']
            self.test_data['searched_dob'] = visitor['birthDate']
            if len(visitor['identifications'][0]) > 0:
                is_key_there_in_dict('documentTypeCode', visitor['identifications'][0])
                self.test_data['searched_doc_type'] = visitor['identifications'][0]['documentTypeCode']
                self.test_data['searched_doc_number'] = visitor['identifications'][0]['number']
            break
        else:
            raise Exception("There's no Visitor in response!!")

        self.test_data['searched_visitor_name'] = f"{self.test_data['searched_fn']} {self.test_data['searched_ln']}"

    def get_visitor_details_ship(self):
        """
        Function to get the visitor details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {'size': '10'}
        body = {"shipCode": self.config.ship.code, "startDate": f"{self.test_data['firstDay']}T00:00:01",
                "endDate": f"{self.test_data['lastDay']}T23:59:59"}
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('visitors', _content['_embedded'])
        for visitor in _content['_embedded']['visitors']:
            self.test_data['searched_fn'] = visitor['firstName']
            self.test_data['searched_ln'] = visitor['lastName']
            self.test_data['searched_dob'] = visitor['birthDate']
            if len(visitor['identifications'][0]) > 0:
                is_key_there_in_dict('documentTypeCode', visitor['identifications'][0])
                self.test_data['searched_doc_type'] = visitor['identifications'][0]['documentTypeCode']
                self.test_data['searched_doc_number'] = visitor['identifications'][0]['number']
            break
        else:
            raise Exception("There's no Visitor in response!!")

        self.test_data['searched_visitor_name'] = f"{self.test_data['searched_fn']} {self.test_data['searched_ln']}"

    def get_missing_picture_count_api(self, side):
        """
        Function to get the missing picture count
        """

        if side == 'ship':
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        else:
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        params = {'page': '1'}
        body = {"fromDate": f"{self.test_data['firstDay']}T00:00:00",
                "toDate": f"{self.test_data['lastDay']}T23:59:59", "reportType": "exception", "shipCode":
                    self.config.ship.code, "exceptionType": "MISSING-PICTURE", "useOptimized": True,
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_missing_picture_count'] = _content['page']['totalElements']

    def get_expired_card_count_api(self):
        """
        Function to get the expired card count
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        params = {'page': '1'}
        body = {"fromDate": f"{self.test_data['firstDay']}T00:00:00",
                "toDate": f"{self.test_data['lastDay']}T23:59:59", "reportType": "exception", "shipCode":
                    self.config.ship.code, "exceptionType": "EXPIRED-CARD", "useOptimized": True,
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_expired_card_count'] = _content['page']['totalElements']

    def get_not_checked_in_onboard_count_api(self, side):
        """
        Function to get the Not Checked-in, Onboard count
        """
        if side == 'ship':
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        else:
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        params = {'page': '1'}
        body = {"fromDate": f"{self.test_data['firstDay']}T00:00:00",
                "toDate": f"{self.test_data['lastDay']}T23:59:59", "reportType": "exception", "shipCode":
                    self.config.ship.code, "exceptionType": "OB-NTC", "useOptimized": True,
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_not_checked_in_count'] = _content['page']['totalElements']

    def get_checked_in_not_onboard_count_api(self, side):
        """
        Function to get the Checked-in, Not Onboard count
        """
        if side == 'ship':
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        else:
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        params = {'page': '1'}
        body = {"fromDate": f"{self.test_data['firstDay']}T00:00:00",
                "toDate": f"{self.test_data['lastDay']}T23:59:59", "reportType": "exception", "shipCode":
                    self.config.ship.code, "exceptionType": "TC-NOB", "useOptimized": True,
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_checked_in_count'] = _content['page']['totalElements']

    def get_visitor_onboard_count_api(self, side):
        """
        Function to get the visitor onboard count
        """
        if side == 'ship':
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        else:
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), "/gangway-reports/exception")
        params = {'page': '1'}
        body = {"fromDate": f"{self.test_data['firstDay']}T00:00:00",
                "toDate": f"{self.test_data['lastDay']}T23:59:59", "reportType": "exception", "shipCode":
                    self.config.ship.code, "exceptionType": "VISITOR-ONBOARD", "useOptimized": True,
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('exceptions', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_visitor_onboard_count'] = _content['page']['totalElements']

    def get_wearable_assigned_count_api(self):
        """
        Function to get the visitor onboard count
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/trackables/assignments/report")
        params = {
            'page': '1',
            'sourceIds': '38c1ab51-ce97-439c-9d20-c48d724e1fe5',
            'fromAssignedDate': self.test_data['firstDay'],
            'toAssignedDate': self.test_data['lastDay']
        }
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content

    def get_in_port_manning_count_api(self, test_data, side):
        """
        Function to get the In port mining count
        :param test_data:
        :param side:
        """
        get_ship_time(self.rest_oci, self.config, test_data)
        if side == 'ship':
            url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), "/gangway-reports/in-port-manning")
        else:
            url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), "/gangway-reports/in-port-manning")
        today = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        params = {'page': '1'}
        body = {"fromDate": f"{today}T00:00:00",
                "toDate": f"{today}T23:59:59", "reportType": "ipm", "shipCode":
                    self.config.ship.code, "safetyPositionAssigned": True, "shipTime": test_data['current_ship_time']
                }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('inPortMannings', _content['_embedded'])
        is_key_there_in_dict('page', _content)
        self.test_data['total_ipm_count'] = _content['page']['totalElements']

    def get_next_to_next_voyage(self, test_data):
        """
        This function is used to get the next to next voyage details
        :param test_data:
        """
        for voyage in test_data['_voyages']:
            if voyage['embarkDate'].split('T')[0] == str(date.today()):
                self.test_data['next_to_next_firstDay'] = self.test_data['next_raw_debarkDate'].split('T')[0]
                self.test_data['next_to_next_raw_embarkDate'] = self.test_data['next_raw_debarkDate']
                self.test_data['next_to_next_embarkDate'] = datetime.strptime(
                    self.test_data['next_raw_debarkDate'].split('T')[0],
                    "%Y-%m-%d").strftime("%m/%d/%Y")
                break

        for voyage in test_data['_voyages']:
            if voyage['embarkDate'].split('T')[0] == self.test_data['next_raw_debarkDate'].split('T')[0]:
                self.test_data['next_to_next_lastDay'] = voyage['debarkDate'].split('T')[0]
                self.test_data['next_to_next_raw_debarkDate'] = voyage['debarkDate']
                self.test_data['next_to_next_debarkDate'] = datetime.strptime(voyage['debarkDate'].split('T')[0],
                                                                              "%Y-%m-%d").strftime("%m/%d/%Y")
                self.test_data['next_to_next_voyageId'] = voyage['voyageId']
                self.test_data['next_to_next_voyageNumber'] = voyage['number']
                self.test_data['next_to_next_shipCode'] = voyage['shipCode']
                break
        else:
            raise Exception(f"There's no Future voyage with embark day as {self.test_data['next_raw_embarkDate']} !!")

        params = {
            "voyagenumber": self.test_data['next_to_next_voyageNumber']
        }

        url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), 'voyages/search/findbyvoyagenumber')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        for voyage in _content['_embedded']['voyages']:
            self.test_data['next_namekey_shore'] = voyage['nameKey']
            break
        else:
            raise Exception("There's no active voyage in system !!")
        self.test_data['next_to_next_voyage_name_shore'] = f"{self.test_data['next_namekey_shore']} " \
                                                           f"{self.test_data['next_to_next_embarkDate']}" \
                                                           f"-{self.test_data['next_to_next_debarkDate']}"

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

    def get_active_voyage_itinerary(self, test_data):
        """
        This function is used to get the next voyage details
        :param test_data:
        """
        voyage_number = test_data['voyageNumber']
        url = urljoin(self.config.ship.url,
                      f"dxpcore/voyages/search/findbyvoyagenumber?voyagenumber={voyage_number}")
        _content = self.rest_oci.send_request(method="GET", url=url, auth="bearer").content
        test_data['active_voyage_date_wise_itinerary'] = sorted(_content["_embedded"]["voyages"][0]['voyageItineraries'], key=lambda i: i['itineraryDay'])


