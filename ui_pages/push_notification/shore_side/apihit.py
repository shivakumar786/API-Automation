__author__ = 'aatir.fayyaz'

from virgin_utils import *


class Apihit:
    """
    Page Class for push notification shore side apihit
    """

    def __init__(self, config, rest_shore, test_data, creds):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_shore:
        :param test_data:
        """
        self.config = config
        self.rest_oci = rest_shore
        self.test_data = test_data
        self.creds = creds

    def get_token(self, side):
        """
        This function is used to get the user Token
        :param side:
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
        today = date.today()
        six_months = date.today() + relativedelta(months=+6)
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'),
                      'voyages/search/findbyshipcodeandsailingpackagecode')
        params = {
            "shipcodes": self.config.ship.code,
            "embarkdate": today,
            "debarkdate": six_months,
            "size": 9999,
            "sort": "embarkdate"
        }
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        if _content['_embedded']['voyages'] != 0:
            voyage = _content['_embedded']['voyages'][0]
            self.test_data['firstDay'] = voyage['embarkDate'].split('T')[0]
            self.test_data['lastDay'] = voyage['debarkDate'].split('T')[0]
            self.test_data['raw_firstDay'] = voyage['embarkDate']
            self.test_data['raw_lastDay'] = voyage['debarkDate']
            self.test_data['FirstDay'] = datetime.strptime(voyage['embarkDate'].split('T')[0], "%Y-%m-%d").strftime(
                                                                                               "%m/%d/%Y")
            self.test_data['LastDay'] = datetime.strptime(voyage['debarkDate'].split('T')[0], "%Y-%m-%d").strftime(
                                                                                              "%m/%d/%Y")
            self.test_data['voyageId'] = voyage['voyageId']
            self.test_data['voyageNumber'] = voyage['number']
            self.test_data['shipCode'] = voyage['shipCode']
            self.test_data['namekey'] = voyage['nameKey']
            if voyage['shipCode'] == self.config.ship.code:
                self.test_data['shipName'] = 'Scarlet Lady'
        else:
            raise Exception("There's no voyage in system !!")
        self.test_data[
            'voyage_name_space'] = f"{self.test_data['namekey']} {self.test_data['FirstDay']}-{self.test_data['LastDay']}"
        self.test_data[
            'voyage_name'] = f"{self.test_data['namekey'].strip()} {self.test_data['FirstDay']}-{self.test_data['LastDay']}"

    def get_ship_date(self):
        """
        Function to get the ship date
        """
        params = {"shipcode": self.config.ship.code}
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        self.test_data['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp']).date())

    def get_sailor_details(self, flag):
        """
        Function to get the sailor details
        :param flag:
        """
        url = urljoin(getattr(self.config.shore.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/reservation-guests/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01",
        }
        if flag:
            body.update({"checkedInStatus": "CHECKED_IN", "boardingStatus": "ONBOARD"})
        self.rest_oci.session.headers.update({'Content-Type': 'application/json'})
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        if len(_content['reservationGuests']) > 0:
            for _guests in _content['reservationGuests']:
                if _guests['stateroom'] != 'GTY':
                    self.test_data['searched_sailor_fn'] = _guests['firstName']
                    self.test_data['searched_sailor_ln'] = _guests['lastName']
                    self.test_data['searched_sailor_stateroom'] = _guests['stateroom']
                    self.test_data['searched_sailor_booking'] = _guests['reservationNumber']
                    self.test_data['searched_sailor_reservationGuestId'] = _guests['reservationGuestId']
                    break

            self.test_data[
                'searched_sailor_name'] = f"{self.test_data['searched_sailor_fn']} " \
                                          f"{self.test_data['searched_sailor_ln']}"
            self.test_data["sailor_data"] = True
        else:
            self.test_data["sailor_data"] = False

    def crew_app_dashboard(self):
        """
        Get Crew App Dashboard Items
        :return:
        """
        _url = urljoin(self.config.shore.url, '/user-account-service/signin/username')
        body = {
            "userName": self.creds.verticalqa.username, "password": self.creds.verticalqa.password,
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = self.rest_oci.send_request(method="POST", url=_url, json=body, auth="basic").content
        self.rest_oci.crewToken = f"{_content['tokenType']} {_content['accessToken']}"
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'), "/crew-dashboard/dashboard")
        _content = self.rest_oci.send_request(method="GET", url=url, auth="crew").content
        self.test_data['currentShipTime'] = twenty_four_hour_format_converter(_content['currentDate'][11:])[:5]

    def get_ship_reservation_details(self):
        """
        To get ship side reservation details
        """
        self.get_token(side='ship')
        self.get_ship_date()
        self.get_voyage_details()
        self.get_sailor_details(flag=True)
        self.crew_app_dashboard()