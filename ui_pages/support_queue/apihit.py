__author__ = 'Vanshika.Arora'

import random

from virgin_utils import *


class Apihit:
    """
    Page Class for Support Queue apihit page
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
        if len(_content['reservationGuests']) > 0:
            for _guests in range(len(_content['reservationGuests'])):
                _guests = random.choice(_content['reservationGuests'])
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
