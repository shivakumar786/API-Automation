__author__ = 'prahlad.sharma'

from virgin_utils import *


class Apihit:
    """
    Page Class for Gangway app
    """

    def __init__(self, config, rest_shore, test_data):
        """
        To Initialize the locators of API hit page
        :param config:
        :param rest_oci:
        :param test_data:
        """
        self.config = config
        self.rest_oci = rest_shore
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
        self.test_data['shipEpochDate'] = _content['epocTimestamp'] * 1000

    def get_sailor_details(self, size):
        """
        Function to get the sailor details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/reservation-guests/search')
        params = {
            'page': '1',
            'size': size
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        self.test_data['sailor_data'] = _content

    def get_crew_details(self, size):
        """
        Function to get the crew details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.crewbff'),
                      '/crew-embarkation-admin/team-members/search')
        params = {
            'page': '1',
            'size': size
        }
        body = {
            "shipCode": self.config.ship.code,
            "fromDate": f"{self.test_data['firstDay']}T00:00:01",
            "toDate": f"{self.test_data['lastDay']}T23:59:59",
            "shipTime": f"{self.test_data['shipDate']}T00:00:01"
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params, auth="user").content
        self.test_data['crew_data'] = _content

    def get_visitor_details_ship(self, size):
        """
        Function to get the visitor details
        """
        url = urljoin(getattr(self.config.ship.contPath, 'url.path.embarkationadmin'), "/gangway/visitors/search")
        params = {
            'page': '1',
            'size': size
        }

        body = {"shipCode": self.config.ship.code, "startDate": f"{self.test_data['firstDay']}T00:00:01",
                "endDate": f"{self.test_data['lastDay']}T23:59:59"}
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, params=params,
                                              auth="user").content
        is_key_there_in_dict('visitors', _content['_embedded'])
        self.test_data['visitor_data'] = _content

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

    def get_onboarded_guests(self):
        """
        Function to get Onborded guests
        """
        if self.config.platform == 'DCL':
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=true) and PMSID is not missing"
        else:
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and b.IsOnBoarded=true)"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['onboard_guests'] = _content['results']

    def get_ashore_guests(self):
        """
        Function to get Ashore guests
        """
        if self.config.platform == 'DCL':
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and (b.IsOnBoarded=false or b.IsOnBoarded " \
                    f"is missing)) and PMSID is not missing"
        else:
            query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                    f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                    f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                    f"meta(b).id not like '_sync%' and b.type='GuestStatus' and (b.IsOnBoarded=false or b.IsOnBoarded " \
                    f"is missing))"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            # "creds": [{"user": self.test_data['username'], "pass": "yellow*99"}],
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['ashore_guests'] = _content['results']

    def get_untouched_guests(self):
        """
        Function to get Untouched guests
        """
        query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}'" \
                f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{self.test_data['bucket']}` b where " \
                f"meta(b).id not like '_sync%' and b.type='GuestStatus' and (b.IsOnBoarded is missing))"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['untouched_guests'] = _content['results']

    def get_history_for_person(self, person_id):
        """
        Function to get History of guests
        :param person_id:
        """
        query = f"select * from `{self.test_data['bucket']}` a where meta(a).id not like '_sync%' and a.type='PersonEvent' and " \
                f"a.personID='{person_id}'"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")

        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['history'] = _content['results']

    def get_untouched_crew(self):
        """
        Function to get the Untouched crew
        """
        query = f"select a.FirstName, a.FullName, a.TeamMemberNumber, a.TeamMemberID from `{self.test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and a.type='TeamMember' and a.TeamMemberID in (select raw b.TeamMemberID " \
                f"from `{self.test_data['bucket']}` b where meta(b).id not like '_sync%' and b.type='TeamMemberStatus'" \
                f" and b.IsOnBoarded is missing)"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['untouched_crew'] = _content['results']

    def get_untouched_visitor(self):
        """
        Function to get the Untouched visitor
        """
        pattern = "%Y-%m-%d"
        today = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        epoch = int(time.mktime(time.strptime(today, pattern))) * 1000
        query = f"Select c.FirstName, c.LastName, c.EmployeeNumber, c.VisitorID from `{self.test_data['bucket']}` c " \
                f"where c.type = 'VisitorPersonalInformation' and c.VisitorID in (select raw a.VisitorID from " \
                f"`{self.test_data['bucket']}` a unnest Visits v where a.type = 'VisitorStatus' and ({self.test_data['shipEpochDate']} " \
                f"between v.StartDateEpoch and v.EndDateEpoch) and v.IsDeleted = false and (a.IsOnBoarded is missing) " \
                f"and a.VisitorID in (select raw b.hostId from `{self.test_data['bucket']}`" \
                f" b where meta(b).id not like '_sync%' and b.type= 'TrackableInfo'))"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['untouchedVisitor'] = _content['results']

    def get_onboard_crew(self):
        """
        Function to get the Ashore crew
        """
        query = f"select a.FirstName, a.FullName, a.TeamMemberNumber, a.TeamMemberID from `{self.test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and ({self.test_data['shipEpochDate']} between a.EmbarkDateEpoch and " \
                f"a.DebarkDateEpoch) and a.type='TeamMember' and a.TeamMemberID in (select raw b.TeamMemberID " \
                f"from `{self.test_data['bucket']}` b where meta(b).id not like '_sync%' and b.type='TeamMemberStatus'" \
                f" and b.IsOnBoard=true)"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['onboard_crew'] = _content['results']

    def get_ashore_crew(self):
        """
        Function to get the Ashore crew
        """
        query = f"select a.FirstName, a.FullName, a.TeamMemberNumber, a.TeamMemberID from `{self.test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and a.type='TeamMember' and a.TeamMemberID in (select raw b.TeamMemberID " \
                f"from `{self.test_data['bucket']}` b where meta(b).id not like '_sync%' and b.type='TeamMemberStatus'" \
                f" and b.IsOnBoard=false)"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['ashore_crew'] = _content['results']

    def get_ashore_visitor(self):
        """
        Function to get the Ashore visitor
        """
        pattern = "%Y-%m-%d"
        today = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        epoch = int(time.mktime(time.strptime(today, pattern))) * 1000
        query = f"Select c.FirstName, c.LastName, c.EmployeeNumber, c.VisitorID, c.BirthDate from `{self.test_data['bucket']}` c " \
                f"where c.type = 'VisitorPersonalInformation' and c.VisitorID in (select raw a.VisitorID from " \
                f"`{self.test_data['bucket']}` a unnest Visits v where a.type = 'VisitorStatus' and ({self.test_data['shipEpochDate']} " \
                f"between v.StartDateEpoch and v.EndDateEpoch) and v.IsDeleted = false and (a.IsOnBoarded = false or " \
                f"a.IsOnBoarded is missing) and a.VisitorID in (select raw b.hostId from `{self.test_data['bucket']}`" \
                f" b where meta(b).id not like '_sync%' and b.type= 'TrackableInfo'))"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['ashore_visitor'] = _content['results']

    def get_on_boarded_visitor(self):
        """
        Function to get the Onboarded visitor
        """
        pattern = "%Y-%m-%d"
        today = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        epoch = int(time.mktime(time.strptime(today, pattern))) * 1000
        query = f"Select c.FirstName, c.LastName, c.EmployeeNumber, c.VisitorID, c.BirthDate from `{self.test_data['bucket']}` c " \
                f"where c.type = 'VisitorPersonalInformation' and c.VisitorID in (select raw a.VisitorID from " \
                f"`{self.test_data['bucket']}` a unnest Visits v where a.type = 'VisitorStatus' and ({self.test_data['shipEpochDate']} " \
                f"between v.StartDateEpoch and v.EndDateEpoch) and v.IsDeleted = false and a.IsOnBoarded = true and " \
                f"a.VisitorID in (select raw b.hostId from `{self.test_data['bucket']}` b where meta(b).id not like " \
                f"'_sync%' and b.type= 'TrackableInfo'))"
        url = urljoin(f"{self.test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if self.config.envMasked == "CERT":
            url = urljoin(f"{self.test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = self.rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('results', _content)
        self.test_data['onboarded_visitor'] = _content['results']

    def get_moci_approved_guests(self, db_core):
        """
        Function to get moci approved guests
        :param db_core:
        """
        if self.config.platform != 'DCL':
            query = f"select rg.reservationguestid, rg.stateroom, g.lastname, g.firstname, rg.embarkdate, rg.debarkdate, " \
                    f"r.voyagenumber  from guest g inner join reservationguest rg on g.guestid = rg.guestid inner join " \
                    f"reservation r on rg.reservationid = r.reservationid inner join guestmoderationdetail gmd on " \
                    f"rg.reservationguestid =gmd.reservationguestid and gmd.isdeleted =false where  " \
                    f"rg.reservationstatuscode <> 'CN' and r.voyagenumber = '{self.test_data['voyageNumber']}' and prevalidatestatuscode = " \
                    f"'APPROVED' "
        else:
            query = f"select rg.reservationguestid, rg.stateroom, g.lastname, g.firstname, rg.embarkdate, rg.debarkdate, " \
                    f"r.voyagenumber  from guest g inner join reservationguest rg on g.guestid = rg.guestid inner join " \
                    f"reservation r on rg.reservationid = r.reservationid inner join guestmoderationdetail gmd on " \
                    f"rg.reservationguestid =gmd.reservationguestid and gmd.isdeleted =false where  " \
                    f"rg.reservationstatuscode <> 'CN' and r.voyagenumber = '{self.test_data['voyageNumber']}' and prevalidatestatuscode = " \
                    f"'APPROVED' "
        response = db_core.shore.run_and_fetch_data(query=query)
        return response

    def get_moci_rejected_guests(self, db_core):
        """
        Function to get moci rejected guests
        :param db_core:
        """
        if self.config.platform != 'DCL':
            query = f"select rg.reservationguestid, rg.stateroom, g.lastname, g.firstname, rg.embarkdate, rg.debarkdate, " \
                f"r.voyagenumber  from guest g inner join reservationguest rg on g.guestid = rg.guestid inner join " \
                f"reservation r on rg.reservationid = r.reservationid inner join guestmoderationdetail gmd on " \
                f"rg.reservationguestid =gmd.reservationguestid and gmd.isdeleted =false where  " \
                f"rg.reservationstatuscode <> 'CN' and r.voyagenumber = '{self.test_data['voyageNumber']}' and prevalidatestatuscode = " \
                f"'REJECTED' "
        else:
            query = f"select rg.reservationguestid, rg.stateroom, g.lastname, g.firstname, rg.embarkdate, rg.debarkdate, " \
                f"r.voyagenumber  from guest g inner join reservationguest rg on g.guestid = rg.guestid inner join " \
                f"reservation r on rg.reservationid = r.reservationid inner join guestmoderationdetail gmd on " \
                f"rg.reservationguestid =gmd.reservationguestid and gmd.isdeleted =false where  " \
                f"rg.reservationstatuscode <> 'CN' and r.voyagenumber = '{self.test_data['voyageNumber']}' and prevalidatestatuscode = " \
                f"'REJECTED' "
        response = db_core.shore.run_and_fetch_data(query=query)
        return response

    def get_rfid_onboard_sailors(self):
        """
        Function to get the onboard sailors with trackable a
        """
        from datetime import date
        today = date.today()
        self.test_data['current_date'] = today.strftime("%Y-%m-%d")
        if self.config.platform != 'DCL':
            query = f"Select a.FirstName, a.LastName, a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{self.test_data['bucket']}` a " \
                    f"where  meta(a).id not like '_sync%' and a.type = 'GuestPersonalInformation' and a.VoyageNumber = '{self.test_data['voyageNumber']}' and  a.ReservationGuestID" \
                    f" in (select raw b.ReservationGuestID from `{self.test_data['bucket']}` b "\
                    f"where meta(b).id not like '_sync%' and b.type = 'GuestStatus' and b.IsOnBoarded = TRUE "\
                    f"and b.DebarkDate = '{self.test_data['shipDate']}' " \
                    f" and b.ReservationGuestID in (select raw c.hostId from `{self.test_data['bucket']}` c where "\
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
