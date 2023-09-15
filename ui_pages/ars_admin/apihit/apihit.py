__author__ = 'vanshika.arora'

from virgin_utils import *


class Apihit:
    """
    Page Class for ARS admin apihit
    """

    def __init__(self, config, rest_ship, test_data, creds):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_ship:
        :param test_data:
        """
        self.config = config
        self.rest_oci = rest_ship
        self.test_data = test_data
        self.creds = creds

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
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        self.test_data['shipDate'] = str(
            datetime.utcfromtimestamp(_content['epocTimestamp']).date())

    def get_sailor_details(self, flag):
        """
        Function to get the sailor details
        :param flag:
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
            "shipTime": f"{self.test_data['shipDate']}T00:00:01",
        }
        if flag:
            body.update({"checkedInStatus": "CHECKED_IN", "boardingStatus": "ONBOARD"})
        self.rest_oci.session.headers.update({'Content-Type': 'application/json'})
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        checked_in_cabins = []
        for count in range(0, len(_content['reservationGuests'])):
            if _content['reservationGuests'][count]['stateroom'] != 'GTY':
                checked_in_cabins.append(_content['reservationGuests'][count]['stateroom'])
        choose_cabin = random.choice(checked_in_cabins)
        if len(_content['reservationGuests']) > 0:
            for _guests in _content['reservationGuests']:
                if _guests['stateroom'] == choose_cabin:
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
        _url = urljoin(self.config.ship.url, '/user-account-service/signin/username')
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
        self.get_checkin_and_onboarded_crew()

    def get_previous_voyage(self, test_data):
        """
        This function is used to get the previous voyage details
        :param test_data:
        """
        _time = get_ship_time(self.rest_oci, self.config, self.test_data)
        test_data['OnBoardingStatusDate'] = _time.utcTimestamp.split('.')[0]
        test_data['OnBoardingStatusDateEpoch'] = _time[3]
        _date = _time.shipDate

        start_date = "2021-06-01"
        end_date = str(_date.date() + timedelta(days=31))
        url = urljoin(self.config.ship.url,
                      f"dxpcore/voyages/search/findbyembarkdate?startdate={start_date}&enddate={end_date}")

        # Get Voyages present in system from today + 31 days, Raise exception if there is no voyage present in system
        _content = self.rest_oci.send_request(method="GET", url=url, auth="bearer").content
        test_data['_voyages'] = sorted([x for x in _content['_embedded']['voyages'] if x['shipCode']
                                        == self.config.ship.code], key=lambda i: i['embarkDate'])
        for voyage in test_data['_voyages']:
            if voyage['debarkDate'][0:10] == self.test_data['raw_embarkDate'][0:10] and voyage[
                'shipCode'] == self.config.ship.code:
                self.test_data['prefirstDay'] = voyage['embarkDate'].split('T')[0]
                self.test_data['prelastDay'] = voyage['debarkDate'].split('T')[0]
                self.test_data['preraw_embarkDate'] = voyage['embarkDate']
                self.test_data['preraw_debarkDate'] = voyage['debarkDate']
                self.test_data['preembarkDate'] = datetime.strptime(voyage['embarkDate'].split('T')[0],
                                                                    "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['pre_debarkDate'] = datetime.strptime(voyage['debarkDate'].split('T')[0],
                                                                     "%Y-%m-%d").strftime(
                    "%m/%d/%Y")
                self.test_data['prevoyageId'] = voyage['voyageId']
                self.test_data['prevoyageNumber'] = voyage['number']
                self.test_data['preshipCode'] = voyage['shipCode']
                break
            else:
                continue

        params = {
            "voyagenumber": self.test_data['pre_voyageNumber']
        }

        url = urljoin(getattr(self.config.shore.contPath, 'url.path.dxpcore'), 'voyages/search/findbyvoyagenumber')
        _content = self.rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
        for voyage in _content['_embedded']['voyages']:
            self.test_data['pre_namekey_shore'] = voyage['nameKey']
            break
        else:
            raise Exception("There's no active voyage in system !!")
        self.test_data[
            'pre_voyage_name_shore'] = f"{self.test_data['pre_namekey_shore']} " \
                                       f"{self.test_data['pre_embarkDate']}-{self.test_data['pre_debarkDate']}"

    def get_checkin_and_onboarded_crew(self):
        """
        Function to get the checkin and onboarded crew members from embarkation supervisor
        :return:
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/team-members/search')
        params = {
            'page': '1',
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "checkedInStatus": "CHECKED_IN",
            "boardingStatus": "ONBOARD",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        active_crew_list = []
        for crew in _content['teamMembers']:
            active_crew_list.append(crew['fullName'])
        self.test_data['activeCrew'] = random.choice(active_crew_list)
