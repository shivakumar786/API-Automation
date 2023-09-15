__author__ = 'sarvesh.singh'

import time

from virgin_utils import *


class ApiHit:
    """
    Page Class for ACI app
    """

    def __init__(self, config, rest_shore, rest_ship, test_data):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_shore:
        :param test_data:
        """
        self.config = config
        self.rest_oci = rest_ship
        self.test_data = test_data

    def get_token(self):
        """
        This function is used to get the user Token
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.identityaccessmanagement'), 'oauth/token')
        params = {
            "grant_type": "client_credentials"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, params=params, auth="basic").content
        is_key_there_in_dict('access_token', _content)
        self.rest_oci.userToken = f"bearer {_content['access_token']}"
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
                    if self.config.ship.code == 'DD':
                        self.test_data['shipName'] = 'Disney Dream'
                    else:
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
        self.test_data['shipEpochDate'] = _content['epocTimestamp'] * 1000

    def get_document_bucket(self):
        """
        Function to get the bucket and server link
        """
        url = urljoin(self.config.ship.sync, '_config')
        _content = self.rest_oci.send_request(method="GET", url=url, auth="user").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        is_key_there_in_dict('username', _content)
        is_key_there_in_dict('password', _content)
        url = _content['server']
        if self.config.platform == 'DCL' and self.config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
        self.test_data['server_url'] = url
        self.test_data['bucket'] = _content['bucket']
        self.test_data['username'] = _content['username']
        self.test_data['password'] = _content['password']

    def get_cabin(self):
        """
        Function to get cabin for which rts is not done
        """
        query = f"select Stateroom from {self.test_data['bucket']} where type = 'GuestStatus' and VoyageNumber = "\
                f"'{self.test_data['voyageNumber']}' and IsOnlineCheckedIn = true and ReservationStatusCode ='RS' " \
                f" and TerminalCheckinStatus = 'NOT_COMPLETED' and Stateroom != '9999' and meta().id not " \
                f"like '_sync%' limit 10"
        params = {
            "statement": query,
        }
        token_string = str(
            base64.b64encode(bytes(f"{self.config.ship.couch.username}:{self.config.ship.couch.password}", 'utf-8')),
            'ascii').strip()
        token = f'Basic {token_string}'
        header = {'Authorization': token, 'Content-Type': 'application/x-www-form-urlencoded'}
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        response = requests.get(url=url, params=params, headers=header).json()
        self.test_data['line'] = True
        if len(response['results']) == 0:
            query = f"select Stateroom from {self.test_data['bucket']} where type = 'GuestPersonalInformation' and VoyageNumber = " \
                    f"'{self.test_data['voyageNumber']}' and ReservationStatusCode ='RS' and Stateroom != '9999' " \
                    f"and FirstName != 'TBD' and meta().id not like '_sync%' limit 10"
            params = {
                "statement": query,
            }
            url = urljoin(self.config.ship.couch.url, "/query")
            response = requests.get(url=url, params=params, headers=header).json()
            self.test_data['line'] = False
        time.sleep(5)
        is_key_there_in_dict('results', response)
        self.test_data['cabins'] = [x['Stateroom'] for x in response['results'] if x['Stateroom'] != 'GTY']

    def get_reservation_details(self, stateroom):
        """
        Get all cabin reservation details
        """
        query = f"select BirthDate,FirstName,LastName,Gender,ReservationGuestID from {self.test_data['bucket']} where type = 'GuestPersonalInformation' and VoyageNumber = " \
                f"'{self.test_data['voyageNumber']}' and Stateroom = '{stateroom}' and ReservationStatusCode ='RS' and " \
                f"meta().id not like '_sync%'"
        params = {
            "statement": query,
        }
        token_string = str(
            base64.b64encode(bytes(f"{self.config.ship.couch.username}:{self.config.ship.couch.password}", 'utf-8')),
            'ascii').strip()
        token = f'Basic {token_string}'
        header = {'Authorization': token, 'Content-Type': 'application/x-www-form-urlencoded'}
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        response = requests.get(url=url, params=params, headers=header).json()
        is_key_there_in_dict('results', response)
        self.test_data['guests_details'] = response['results']

    def get_moci_approved_guests(self):
        """
        Function to get moci approved guests
        """
        if self.config.platform == 'DCL':
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=true) and PMSID is not missing"
        else:
            query = f"select a.FirstName,a.LastName,a.ReservationNumber,a.VoyageNumber,a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=False and b.PreValidateStatus = 'APPROVED'" \
                    f"and b.IsOnlineCheckedIn = True and b.TerminalCheckinStatus = 'NOT_COMPLETED')"

        # url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        # if self.config.envMasked == "CERT":
        #     url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        # body = {
        #     "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
        #     "statement": query,
        # }
        # _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        # is_key_there_in_dict('results', _content)
        params = {
            "statement": query,
        }
        token_string = str(
            base64.b64encode(bytes(f"{self.config.ship.couch.username}:{self.config.ship.couch.password}", 'utf-8')),
            'ascii').strip()
        token = f'Basic {token_string}'
        header = {'Authorization': token, 'Content-Type': 'application/x-www-form-urlencoded'}
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        response = requests.get(url=url, params=params, headers=header).json()
        self.test_data['line'] = True
        if len(response['results']) == 0:
            query = f"select Stateroom from {self.test_data['bucket']} where type = 'GuestStatus' and VoyageNumber = " \
                    f"'{self.test_data['voyageNumber']}' and ReservationStatusCode ='RS' "
            params = {
                "statement": query,
            }
            url = urljoin(self.config.ship.couch.url, "/query")
            response = requests.get(url=url, params=params, headers=header).json()
            self.test_data['line'] = False
        time.sleep(5)
        is_key_there_in_dict('results', response)
        self.test_data['moci_approved_guests'] = response['results']

    def get_moci_rejected_guests(self):
        """
        Function to get moci rejected guests
        """
        if self.config.platform == 'DCL':
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=true) and PMSID is not missing"
        else:
            query = f"select a.FirstName,a.LastName,a.ReservationNumber,a.VoyageNumber,a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=False and b.PreValidateStatus = 'REJECTED'" \
                    f"and b.IsOnlineCheckedIn = False and b.TerminalCheckinStatus = 'NOT_COMPLETED')"

        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['moci_reject_guests'] = _content['results']

    def get_rfid_onboard_sailors(self):
        """
        Function to get the onboard sailors with trackable a
        """
        from datetime import date
        today = date.today()
        self.test_data['current_date'] = today.strftime("%Y-%m-%d")
        if self.config.platform != 'DCL':
            query = f"Select a.FirstName, a.LastName, a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a " \
                    f"where  meta(a).id not like '_sync%' and a.type = 'GuestPersonalInformation' and a.VoyageNumber = " \
                    f"'{self.test_data['voyageNumber']}' and  a.ReservationGuestID" \
                    f" in (select raw b.ReservationGuestID from `{self.test_data['bucket']}` b " \
                    f"where meta(b).id not like '_sync%' and b.type = 'GuestStatus' and b.IsOnBoarded = TRUE " \
                    f"and b.DebarkDate = '{self.test_data['current_date']}' " \
                    f" and b.ReservationGuestID in (select raw c.hostId from `{self.test_data['bucket']}` c where " \
                    f"c.type = 'TrackableInfo' and c.trackables != []))"

            url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
            if self.config.envMasked == "CERT":
                url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
            body = {
                "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
                "statement": query,
            }
            _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
            is_key_there_in_dict('results', _content)
            self.test_data['onboard_rfid_sailors'] = _content['results']

