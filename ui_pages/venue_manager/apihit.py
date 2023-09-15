__author__ = 'H T Krishnakumara'

import random

from virgin_utils import *


class Apihit:
    """
    Page Class for venue manager apihit page
    """
    def __init__(self, config, rest_shore, rest_ship, test_data, creds, db_core):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_ship:
        :param test_data:
        """
        self.config = config
        self.rest_shore = rest_shore
        self.rest_ship = rest_ship
        self.test_data = test_data
        self.creds = creds
        self.db_core = db_core

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
        _content = self.rest_shore.send_request(method="POST", url=url, params=params, auth="basic").content
        is_key_there_in_dict('access_token', _content)
        _token = _content['access_token']
        self.rest_shore.userToken = f"bearer {_token}"
        self.test_data['userToken'] = self.rest_shore.userToken

        _url = urljoin(self.config.ship.url, '/user-account-service/signin/username')
        body = {
            "userName": self.creds.verticalqa.username, "password": self.creds.verticalqa.password,
            "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"
        }
        _content = self.rest_shore.send_request(method="POST", url=_url, json=body).content
        self.rest_shore.crewToken = f"{_content['tokenType']} {_content['accessToken']}"

        url = urljoin(self.config.shore.url, "identityaccessmanagement-service/oauth/token")
        params = {"grant_type": "client_credentials"}
        _content = self.rest_ship.send_request(method="POST", url=url, params=params, auth="basic").content
        self.rest_ship.bearerToken = f"{_content['token_type']} {_content['access_token']}"

    def get_data_shipboard(self):
        """
        Checking and fetching the guest details to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :param db_core:
        :return:
        """
        # To get the voyage Id for our active voyage
        self.get_token(side='ship')
        _ship = self.config.ship.url
        params = {
            "shipcode": self.config.ship.code
        }
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = self.rest_shore.send_request(method="GET", url=url, params=params, auth="user").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            if voyage['isActive']:
                self.test_data['embarkDate'] = voyage['embarkDate'].split('T')[0]
                self.test_data['debarkDate'] = voyage['debarkDate'].split('T')[0]
                self.test_data['voyageId'] = voyage['voyageId']
                self.test_data['voyageNumber'] = voyage['number']
                self.test_data['shipCode'] = voyage['shipCode']
                break
        else:
            raise Exception("There's no active voyage in system !!")

        self.test_data['shipSideGuests'] = []
        _query = f"with cte as (SELECT reservationguestid, reservationid, guestid, isprimary, row_number() " \
                 f"over(partition by reservationid) AS rownum FROM public.reservationguest where embarkdate = " \
                 f"'{self.test_data['embarkDate']}' and debarkdate ='{self.test_data['debarkDate']}' and reservationstatuscode = '" \
                 f"RS' and stateroom!= 'GTY') select reservationguestid, reservationid, guestid, isprimary from cte " \
                 f"where reservationid in (select reservationid  from cte where rownum > 1);"
        _data = self.db_core.ship.run_and_fetch_data(query=_query)
        for _guests in _data:
            self.test_data['shipSideGuests'].append({
                "reservationguestid": _guests['reservationguestid'],
                "reservationid": _guests['reservationid'],
                "isprimary": _guests['isprimary'],
                "guestid": _guests['guestid']
            })
        if len(self.test_data['shipSideGuests']) == 0:
            raise Exception('No guest available on ship side for running E2E Ship Side')
        else:
            random.shuffle(self.test_data['shipSideGuests'])

    def get_guest_details_ship_side(self):
        """
        Fetching the guest details from bulk guest to proceed for ship side testing
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _ship = self.config.ship.url
        for guest in self.test_data['shipSideGuests']:
            params = {"personid": guest['guestid']}
            _url = urljoin(getattr(self.config.ship.contPath, 'url.path.identityaccessmanagement'),
                           "/userprofiles/getuserdetails")
            _content = self.rest_shore.send_request(method="GET", url=_url, params=params, auth="crew").content
            if len(_content) != 0 and True is guest['isprimary']:
                url = urljoin(getattr(self.config.ship.contPath, 'url.path.dxpcore'),
                              f"/guests/search/findbyreservationguests/{guest['reservationguestid']}")
                _content_findbyreservationguests = self.rest_shore.send_request(method="GET", url=url, auth="user").content
                if '@mailinator.com' in _content_findbyreservationguests['email']:
                    self.test_data['shipSideGuests'].clear()
                    self.test_data['iamUserId'] = _content['userId']
                    self.test_data['shipSideGuests'].append(guest)
                    self.test_data['shipSideGuests'][0]['email'] = _content_findbyreservationguests['email']
                    break
