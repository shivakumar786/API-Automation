from virgin_utils import *
from decurtis.common import *


class Apihits:
    """
    Page Class for moci
    """

    def __init__(self, config, rest_shore, test_data, guest_data, db_core):
        """
        API's to fetch shore side reservation details
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :param db_core:
        """
        self.guest_data = guest_data
        self.rest_shore = rest_shore
        self.config = config
        self.test_data = test_data
        self.db_core = db_core

    def setup_active_voyage(self):
        """
        Get/Set Ship's Active Voyage
        """

        url = urljoin(getattr(self.config.shore.contPath, 'url.path.identityaccessmanagement'), 'oauth/token')

        params = {
            "grant_type": "client_credentials"
        }
        _content = self.rest_shore.send_request(method="POST", url=url, params=params, auth="basic").content
        is_key_there_in_dict('access_token', _content)
        _token = _content['access_token']
        self.rest_shore.userToken = f"bearer {_token}"
        self.test_data['userToken'] = self.rest_shore.userToken

        if self.config.startDate is None:
            start_date = datetime.now(tz=pytz.utc).date()
        else:
            date_use = self.config.startDate
            start_date = datetime.strptime(date_use, "%Y-%m-%d")
        url = urljoin(self.config.shore.url, 'bookvoyage-bff/voyages')
        body = {
            "searchQualifier": {
                "sailingDateRange": [{"start": str(start_date), "end": str(start_date + timedelta(days=40))}],
                "cabins": [{"guestCounts": [{"ageCategory": "Adult", "count": self.test_data['guests']}]}],
                "currencyCode": "USD",
                "accessible": False
            }
        }
        # Get available voyages
        _content = self.rest_shore.send_request(method="POST", url=url, json=body, auth="user").content
        is_key_there_in_dict('sailings', _content)
        is_key_there_in_dict('packages', _content)
        self.test_data['voyages'] = sorted(_content['sailings'], key=lambda i: i['startDate'])
        voyages = sorted(_content['sailings'], key=lambda i: i['startDate'])
        if len(voyages) == 0:
            raise Exception("Zero Voyages Returned !!")
        for _voyage in voyages:
            if _voyage['startDate'] > str(start_date) and _voyage['ship']['name'] != 'Valiant Lady':
                self.test_data['voyage'] = _voyage
                break
        if len(self.test_data['voyage']) == 0:
            raise Exception("Scarlet lady voyayes are not available !!")

    def get_ship_time(self):
        """
        Update Ship Time Not done for Production environments
        :return:
        """
        # Get Current Ship Time
        ship_time = get_ship_time(self.rest_shore, self.config)
        self.test_data['ship_time'] = ship_time
        if ship_time is None:
            logger.debug(f"Current Ship-Time -> {str(ship_time.shipDate)}")

    def reservation_details(self):
        """
        Get Reservation form DB
        """
        _shore = self.config.shore.url
        self.test_data['shore_guest_detail'] = dict()
        self.test_data['shore_guestIds'] = []
        guest_details = get_pending_and_pending_overdue_guest(self.db_core, self.test_data, self.rest_shore, _shore,
                                                              self.config)
        self.test_data["personid"] = guest_details['reservationguestid']

    def us_reservation_details(self):
        """
        Get Reservation form DB
        """
        _shore = self.config.shore.url
        self.test_data['shore_guest_detail'] = dict()
        self.test_data['shore_guestIds'] = []
        guest_details = get_united_state_pending_and_pending_overdue_guest(self.db_core, self.test_data, self.rest_shore, _shore,
                                                              self.config)
        if guest_details == None:
            self.test_data["personid"] = None
        else:
            self.test_data["personid"] = guest_details['reservationguestid']

    def in_reservation_details(self):
        """
        Get Reservation form DB
        """
        _shore = self.config.shore.url
        self.test_data['shore_guest_detail'] = dict()
        self.test_data['shore_guestIds'] = []
        guest_details = get_indian_pending_and_pending_overdue_guest(self.db_core, self.test_data, self.rest_shore, _shore,
                                                              self.config)
        if guest_details == None:
            self.test_data["personid"] = None
        else:
            self.test_data["personid"] = guest_details['reservationguestid']

    def shore_reservation_details(self, guest_data):
        """
        Get the guest details for shore side reservation.
        """
        # Get Reservation ID.
        _shore = self.config.shore.url
        person_id = self.test_data["personid"]
        self.rest_shore.session.headers.update({'Content-Type': 'application/json'})
        _url = urljoin(_shore, f"dxpcore/reservationguests/{person_id}")
        content = self.rest_shore.send_request(method='GET', url=_url, auth="bearer").content
        self.test_data['shore_reservationID'] = content['reservationId']
        self.test_data['shore_cabinNumber'] = content['stateroom']
        # Get Reservation Number.
        _url = urljoin(_shore, 'dxpcore/reservations/search/findByreservationIds')
        _body = {
            "reservationIds": [f"{content['reservationId']}"]
        }
        _content = self.rest_shore.send_request(method='POST', url=_url, json=_body, auth="bearer").content
        # check_reservation(_content['_embedded']['reservations'][0]['reservationNumber'], rest_shore, config)
        self.test_data['shore_reservationNumber'] = _content['_embedded']['reservations'][0]['reservationNumber']
        logger.info(f"reservation numbers fetched to perform rts is {self.test_data['shore_reservationNumber']}")
        # Get Reservation Guest Details.
        _url = urljoin(_shore, "/dxpcore/reservationevents/search/getguestsdetailbyreservationnumber")
        param = {
            "reservationnumber": _content['_embedded']['reservations'][0]['reservationNumber']
        }
        _content = self.rest_shore.send_request(method='GET', url=_url, auth="bearer", params=param).content
        self.test_data['shore_guestDetails'] = _content['guestDetails']
        for _details in _content['guestDetails']:
            self.guest_data.append(_details)
            self.test_data['shore_guestIds'].append(_details['guestId'])
        for guests in guest_data:
            url_guest = urljoin(_shore, f"/dxpcore/guests/{guests['guestId']}")
            content_guests = self.rest_shore.send_request(method='GET', url=url_guest, auth="bearer",
                                                          params=param).content
            guests.update(content_guests)
        _url = urljoin(_shore, "/dxpcore/checkin/guest/detail-info")
        param = {
            "reservation-number": self.test_data['shore_reservationNumber'],
            "exclude-cancelled": True
        }
        _content = self.rest_shore.send_request(method='GET', url=_url, auth="bearer", params=param).content
        self.test_data['guest_details'] = _content['_embedded']

    def get_voyages(self):
        """
        Get the upcoming voyages.
        """
        if self.config.startDate is None:
            start_use = str(datetime.today().date())
            date = start_use.split("-")
            start_date = f"{date[1]}-{date[2]}-{date[0]}"
        else:
            date_use = self.config.startDate
            start_date = datetime.strptime(date_use, "%m-%d-%y")

        _shore = self.config.shore.url
        self.rest_shore.session.headers.update({'Content-Type': 'application/json'})
        _url = urljoin(getattr(self.config.shore.contPath, 'url.path.crewbff'),"moci/dashboard/voyage")
        content = self.rest_shore.send_request(method='GET', url=_url, auth="crew").content
        _content = content['graph']['voyages']

        self.test_data['voyages'] = sorted(_content, key=lambda i: i['embarkDate'])
        voyages = sorted(_content, key=lambda i: i['embarkDate'])
        if len(voyages) == 0:
            raise Exception("Zero Voyages Returned !!")
        for _voyage in voyages:
            voyage_date = _voyage['embarkDate'].split("-")
            v_date = f"{voyage_date[2]}-{voyage_date[0]}-{voyage_date[1]}"
            if str(v_date) >= str(start_use) and _voyage['shipCode'] != 'VL' and _voyage['shipCode'] != 'RS':
                self.test_data['voyage'] = _voyage
                break
        if len(self.test_data['voyage']) == 0:
            raise Exception("Scarlet lady voyayes are not available !!")
