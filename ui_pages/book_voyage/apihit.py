__author__ = 'saloni.pattnaik'

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
