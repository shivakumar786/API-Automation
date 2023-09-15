__author__ = 'Sarvesh.Singh'

from locust import HttpLocust, TaskSequence, seq_task, between
from locust.exception import StopLocust
from decurtis import tokens
from virgin_utils import *
from decurtis.database import Database
import argparse


class SailorApp(TaskSequence):
    """
    Locust User Behavior File
    """

    def __init__(self, parent):
        """
        Init Function
        :param parent:
        """
        super().__init__(parent)
        self.shore = self.parent.host
        self.authorization_url = self.parent.authorization_url
        self.user_data = dict()
        current_date = datetime.now(tz=pytz.utc).date()
        self.creds = read_creds(self.shore)
        self.request = tokens.ShoreTokens(shore=self.shore, ship=None)
        _query = f"SELECT * FROM public.reservationguest where embarkdate > '{current_date}' and addeddate > \'2020-02-12\' limit 2000"
        guest = parent.shore.run_and_fetch_data(query=_query)
        self.guest_data = generate_guest_data(guest_count=1, guest_countries=['US'])
        random.shuffle(guest)
        for count, guests in enumerate(guest):
            headers = {
                "Authorization": self.request.basic_token,
                "Content-Type": "application/json"
            }
            response = self.client.post(
                "identityaccessmanagement-service/oauth/token?grant_type=client_credentials",
                name='Get Client token',
                headers=headers).json()
            self.user_data['bearerToken'] = "bearer " + response['access_token']
            headers = {
                "Authorization": self.user_data['bearerToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get(f"dxpcore/guests/{guests['guestid']}",
                                       name='Get Guests',
                                       headers=headers).json()
            if "mailinator" in response['email']:
                self.guest_data[0].update(guests)
                self.user_data['username'] = response['email']
                break

    @staticmethod
    def check_response_code(response):
        """
        This function stop the locust thread of response code is not 200 and 201!
        :return:
        """
        if response.status_code not in [200, 201]:
            raise StopLocust()

    @seq_task(1)
    def get_access_token(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        body = {
            "userName": self.user_data['username'],
            "password": "Yellow*99"
        }
        response = self.client.post('user-account-service/signin/email', name='login_booking', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['accessToken'] = "bearer {}".format(response['accessToken'])

    @seq_task(2)
    def rts_bff_assets_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        response = self.client.get('rts-bff/assets', name='rts_bff_assets',
                                   headers=headers)

    @seq_task(3)
    def start_up_virgin(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        response = self.client.get('rts-bff/startup', name='start_up_sailor_rtsbff',
                                   headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['lookupDataUrl'] = response['lookupDataURL']
        self.user_data['multimediaUploadURL'] = response['multimediaUploadURL']
        self.user_data['securityPhotoValidatorURL'] = response['securityPhotoValidatorURL']
        self.user_data['landingURL'] = response['landingURL']

    @seq_task(4)
    def health_check_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            response = self.client.get('rts-bff/healthcheck', name='health_check_sailor',
                                       params=params, headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['health_check_updateURL'] = response['updateURL']

    @seq_task(5)
    def look_up_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        response = self.client.get(self.user_data['lookupDataUrl'], name='look_up_sailor',
                                   headers=headers)

    @seq_task(6)
    def landing_check_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            _res = guest['reservationguestid']
            _res_num = guest['reservationid']
            params = {
                "reservation-guest-id": _res,
                "reservation-number": _res_num
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get('rts-bff/landing', name='landing_check_sailor', params=params,
                                       headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['security_detailsURL'] = response['security']['detailsURL']
            guest['security_detailsURL'] = response['security']['detailsURL']
            self.user_data['travelDocuments_detailsURL'] = response['travelDocuments']['detailsURL']
            guest['travelDocuments_detailsURL'] = response['travelDocuments']['detailsURL']
            self.user_data['paymentMethod_detailsURL'] = response['paymentMethod']['detailsURL']
            guest['paymentMethod_detailsURL'] = response['paymentMethod']['detailsURL']
            self.user_data['pregnancy_detailsURL'] = response['pregnancy']['detailsURL']
            guest['pregnancy_detailsURL'] = response['pregnancy']['detailsURL']
            self.user_data['voyageContract_detailsURL'] = response['voyageContract']['detailsURL']
            guest['voyageContract_detailsURL'] = response['voyageContract']['detailsURL']
            self.user_data['emergencyContact_detailsURL'] = response['emergencyContact']['detailsURL']
            guest['emergencyContact_detailsURL'] = response['emergencyContact']['detailsURL']
            self.user_data['embarkationSlotSelection_detailsURL'] = response['embarkationSlotSelection']['detailsURL']
            guest['embarkationSlotSelection_detailsURL'] = response['embarkationSlotSelection']['detailsURL']

    @seq_task(7)
    def check_taskpercentage_before_rts_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-number": guest['reservationid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get('rts-bff/landing', name='check_taskpercentage_before_rts_virgin', params=params,
                                       headers=headers)

    @seq_task(8)
    def voyage_contract_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get('rts-bff/voyagecontract', name='voyage_contract_get_call', params=params,
                                       headers=headers)

    @seq_task(9)
    def voyage_contract_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            body = {
                "isCruiseContractSigned": True,
                "contractSignedDate": str(datetime.now(tz=pytz.utc).date()),
                "signForOtherGuests": [],
                "signedByReservationGuestId": guest['reservationguestid']
            }
            response = self.client.put('rts-bff/voyagecontract', name='voyage_contract_update_call', params=params,
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(10)
    def emergency_contract_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get('rts-bff/emergencycontact', name='emergency_contract_get_call', params=params,
                                       headers=headers)

    @seq_task(11)
    def emergency_contract_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            body = {
                "emergencyContactDetails": {
                    "name": generate_first_name(),
                    "relationship": "FRIEND",
                    "dialingCountryCode": "US",
                    "phoneNumber": str(generate_phone_number())
                }
            }
            self.guest_data[count].update(body)
            body = body
            response = self.client.put(guest['emergencyContact_detailsURL'], name='emergency_contract_update_call',
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(12)
    def embarkation_slot_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json",
                "correlationid": "67890-09876545"
            }
            response = self.client.get('rts-bff/embarkationslot', name='embarkation_slot_get_call', params=params,
                                       headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['isVip'] = response['isVip']

    @seq_task(13)
    def flight_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            flight_details = {
                "airlineCode": "AA",
                "departureAirportCode": "YYZ",
                "arrivalAirportCode": "MIA",
                "number": "1565",
                "departureTime": "11:25:00",
                "arrivalTime": "14:41:00",
                "arrivalCity": "Zanesville",
                "departureCity": "Wollaston Lake"
            }
            guest['flight_details'] = []
            guest['flight_details'].append(flight_details)
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            body = {
                "flightDetails": flight_details,
                "isFlyingIn": True
            }
            self.guest_data[count].update(body)
            body = body
            response = self.client.put('rts-bff/flight', name='flight_update_call', params=params, json=body,
                                       headers=headers)

    @seq_task(14)
    def embarkation_slot_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            flight_details = {
                "airlineCode": "AA",
                "departureAirportCode": "YYZ",
                "arrivalAirportCode": "MIA",
                "number": "1565",
                "departureTime": "11:25:00",
                "arrivalTime": "14:41:00",
                "arrivalCity": "Zanesville",
                "departureCity": "Wollaston Lake"
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            body = {
                "isFlyingIn": True, "isVip": self.user_data['isVip'], "flightDetails": flight_details,
                "slotNumber": 9, "isParkingOpted": False, "optedByReservationGuestIds": [],
                "postCruiseInfo": {"isFlyingOut": True, "flightDetails": flight_details}
            }
            response = self.client.put('rts-bff/embarkationslot', name='embarkation_slot_update_call', params=params,
                                       json=body, headers=headers)

    @seq_task(15)
    def payment_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            response = self.client.get('rts-bff/paymentmethod', name='payment_get_call', params=params,
                                       headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['paymentModes'] = response['paymentModes'][0]

    @seq_task(16)
    def pregnancy_update(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            url = guest['pregnancy_detailsURL']
            body = {
                "pregnancyDetails": {
                    "isPregnant": bool(random.getrandbits(1))
                }
            }
            response = self.client.put(url, name='pregnancy update', json=body, headers=headers)

    @seq_task(17)
    def paymentmethod_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationguestid'],
                "reservation-id": guest['reservationid']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            body = {
                "selectedPaymentMethodCode": self.user_data['paymentModes'],
                "partyMembers": [], "isDeleted": False,
                "cardPaymentToken": str(generate_guid()).lower()
            }
            response = self.client.put('rts-bff/paymentmethod', name='paymentmethod_update_call', params=params,
                                       json=body, headers=headers)


class SailorAppUser(HttpLocust):
    task_set = SailorApp
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host')
    args = parser.parse_known_args()
    host = args[0].host
    authorization_url = "https://demohpp.fmsapps.com/hpp/authorization"
    db_host = None
    username = None
    password = None
    database = 'dxpcore'
    port = '5432'
    if re.search("dev", host):
        db_host = 'vv-dev-pgdb-n.cbduemg5i5w8.us-east-1.rds.amazonaws.com'
        username = 'pgappuser'
        password = 'pgappuser*101'
    elif re.search("integration", host):
        db_host = 'vv-int-pgdb.cbduemg5i5w8.us-east-1.rds.amazonaws.com'
        username = 'pgappuser'
        password = 'ADtjQqf6KgELqn58'
    else:
        db_host = 'vv-qa-pgdb.cbduemg5i5w8.us-east-1.rds.amazonaws.com'
        username = 'pgappuser'
        password = 'pgappuser*101'

    shore = Database(
        host=db_host,
        username=username,
        password=password,
        database=database,
        port=port
    )
    wait_time = between(5, 10)


if __name__ == "__main__":
    SailorAppUser().run()
