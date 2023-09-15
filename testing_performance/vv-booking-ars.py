__author__ = 'Sarvesh.Singh'

from locust import HttpLocust, TaskSequence, seq_task, between
from locust.exception import StopLocust
from decurtis import tokens
from virgin_utils import *
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
        self.authroization_url = self.parent.authorization_url
        self.request = self.parent.request

    @staticmethod
    def check_response_code(response):
        """
        This function stop the locust thread of response code is not 200 and 201!
        :return:
        """
        if response.status_code not in [200, 201]:
            print(
                f"Failed thread correlation id : {response.request.headers['correlationid']} \nThread is failed on this call : {response.request.url}")
            raise StopLocust()

    @seq_task(1)
    def signup_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        self.user_data = dict()
        self.user_data['headers'] = {
            "correlationid": str(generate_guid().lower())
        }
        self.guest_data = generate_guest_data(guest_count=2, guest_countries=['US'])
        _data = self.guest_data[0]
        self.user_data['guestCount'] = len(self.guest_data)
        self.user_data['GenderCode'] = _data['genderCode']
        self.user_data['CitizenshipCountryCode'] = _data['citizenshipCountryCode']
        self.user_data['username'] = _data['email']
        self.user_data['password'] = "Yellow*99"
        self.user_data['LastName'] = _data['lastName']
        self.user_data['FirstName'] = _data['firstName']
        self.user_data['stateCode'] = _data['addresses'][0]['stateCode']
        self.user_data['city'] = _data['addresses'][0]['city']
        self.user_data['zipCode'] = _data['addresses'][0]['zipCode']
        self.user_data['lineTwo'] = _data['addresses'][0]['lineTwo']
        self.user_data['lineOne'] = _data['addresses'][0]['lineOne']
        self.user_data['BirthDate'] = _data['birthDate']
        contact_number = str(generate_phone_number(max_digits=10))
        body = {
            "contact_number": contact_number,
            "birthDate": self.user_data['BirthDate'],
            "email": self.user_data['username'],
            "firstName": self.user_data['FirstName'],
            "userType": "guest",
            "lastName": self.user_data['LastName'],
            "password": self.user_data['password']
        }
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('user-account-service/signup', name='TC-01 Signup booking', json=body,
                                    headers=headers)
        self.check_response_code(response)

    @seq_task(2)
    def startup_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('user-account-service/startup', name='TC-02 Startup booking',
                                   headers=headers)
        self.check_response_code(response)

    @seq_task(3)
    def login_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "userName": self.user_data['username'],
            "password": self.user_data['password']
        }
        response = self.client.post('user-account-service/signin/email', name='TC-03 Login booking', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['accessToken'] = "bearer {}".format(response['accessToken'])

    @seq_task(4)
    def get_active_voyage_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        start_date = datetime.now(tz=pytz.utc).date()
        end_date = str(start_date + timedelta(days=120)).split(" ")[0]
        start_date = str(start_date)
        # Get Voyages and see if there's any active voyage or not !!
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "searchQualifier": {
                "sailingDateRange": [{
                    "start": start_date,
                    "end": end_date
                }],
                "cabins": [{
                    "guestCounts": [{
                        "ageCategory": "Adult",
                        "count": self.user_data['guestCount']
                    }]
                }],
                "currencyCode": "USD",
                "accessible": False
            }
        }
        response = self.client.post('bookvoyage-bff/voyages', name='TC-04 Choose voyage', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['voyages'] = sorted(response['sailings'], key=lambda i: i['startDate'])
        voyages = sorted(response['sailings'], key=lambda i: i['startDate'])
        if len(voyages) == 0:
            raise StopLocust()
        voyage = random.choice(voyages)
        self.user_data['sailingEmbarkDate'] = voyage['startDate']
        self.user_data['sailingDebarkDate'] = voyage['endDate']
        self.user_data['shipCode'] = voyage['ship']['code']
        self.user_data['voyageId'] = voyage['id']

    @seq_task(5)
    def get_cabin_category_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        body = {
            "voyageId": self.user_data['voyageId'],
            "searchQualifier": {
                "sailingDateRange": [
                    {"start": self.user_data['sailingEmbarkDate'], "end": self.user_data['sailingDebarkDate']}],
                "cabins": [{
                    "guestCounts": [{"ageCategory": "Adult", "count": self.user_data['guestCount']}]
                }]
            }
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('reservation-service/cabincategories/search', name='TC-05 Search cabin',
                                    json=body, headers=headers)
        self.check_response_code(response)
        response = response.json()
        if response['cabins'] is None:
            raise StopLocust()
        else:
            if response['cabins'][0]['categoryOptions'][0]['maxOccupancy'] >= self.user_data['guestCount']:
                self.user_data['categoryCode'] = response['cabins'][0]['categoryOptions'][0]['categoryCode']
                self.user_data['metaCategoryCode'] = response['cabins'][0]['categoryOptions'][0]['genericCategoryCode']
        # self.user_data['categoryCode'] = None
        # if 'stage' in self.parent.host:
        #     for _cabin in response['cabins'][0]['categoryOptions']:
        #         if 'ROCKSTAR' in _cabin['genericCategoryCode'] or 'MEGA' in _cabin[
        #             'genericCategoryCode'] or 'SUITES' in _cabin['genericCategoryCode']:
        #             self.user_data['categoryCode'] = _cabin['categoryCode']
        #             self.user_data['metaCategoryCode'] = _cabin['genericCategoryCode']
        #             break
        #     if self.user_data['categoryCode'] == None:
        #         raise StopLocust()
        # else:
        #     if response['cabins'][0]['categoryOptions'][0]['maxOccupancy'] >= self.user_data['guestCount']:
        #         self.user_data['categoryCode'] = response['cabins'][0]['categoryOptions'][0]['categoryCode']
        #         self.user_data['metaCategoryCode'] = response['cabins'][0]['categoryOptions'][0][
        #             'genericCategoryCode']

    @seq_task(6)
    def cabin_search_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        body = {
            "voyageId": self.user_data['voyageId'],
            "cabins": [{
                "categoryCode": self.user_data['categoryCode'],
                "guestCounts": [{
                    "count": self.user_data['guestCount']
                }]
            }]
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('reservation-service/cabins/search', name='TC-06 Choose cabin', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['cabinNumber'] = response['cabinOptions'][0]['cabinNumber']

    @seq_task(7)
    def getvip_status_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            f"bookvoyage-bff/cabins/{self.user_data['categoryCode']}"
            f"/details?cabinMetaCode={self.user_data['metaCategoryCode']}",
            name='TC-07 Get vip status', headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['isVip'] = response["vip"]

    @seq_task(8)
    def hold_cabin(self):
        """
        Get Token that we want to use here
        :return:
        """
        body = {
            "voyageId": self.user_data['voyageId'],
            "currencyCode": "USD",
            "cabinDetails": [{
                "cabinCategoryCode": self.user_data['categoryCode'],
                "cabinNumber": self.user_data['cabinNumber'],
                "maxOccupancy": self.user_data['guestCount']
            }]
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('bookvoyage-bff/cabin/hold', name='TC-08 Hold cabin', json=body,
                                    headers=headers)
        self.check_response_code(response)

    @seq_task(9)
    def book_reservation_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        user_data = []
        for count, guest in enumerate(self.guest_data):
            user_data.append({
                "givenName": guest['firstName'],
                "lastName": guest['lastName'],
                "genderCode": guest['genderCode'],
                "dateOfBirth": guest['birthDate'],
                "citizenShip": guest['citizenshipCountryCode'],
                "email": guest['email'],
                "guestRefNumber": str(count + 1)
            })
        body = {
            "voyageId": self.user_data['voyageId'],
            "shipCode": self.user_data['shipCode'],
            "cabins": [{
                "cabinNumber": self.user_data['cabinNumber'],
                "cabinCategoryCode": self.user_data['categoryCode'],
                "status": "36", "guestCount": self.user_data['guestCount'], "sailors": user_data
            }],
            "paymentInfo": {"currencyCode": "USD"}
        }
        headers = {"Authorization": self.user_data['accessToken'], "Content-Type": "application/json"}
        headers.update(self.user_data['headers'])
        response = self.client.post('bookvoyage-bff/booknow', name='TC-09 Book reservation', json=body, headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['reservationNumber'] = response[0]['reservationNumber']
        self.user_data['voyageNumber'] = response[0]['voyageId']
        self.user_data['amount'] = response[0]['paymentDetails'][0]['dueAmount']
        self.user_data['encResId'] = response[0]['encResId']

    @seq_task(10)
    def get_guest_reservationguest_id(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {"reservationNumbers": [self.user_data['encResId']]}
        time.sleep(20)  # TODO Remove Delay
        response_userprofile = self.client.post('reservation-service/reservations/search/findbyreservationnumber',
                                                name='TC-10 Get guest id', json=body, headers=headers).json()
        for count, guest in enumerate(self.guest_data):
            for guest_detail in response_userprofile[0]['guestDetails']:
                if guest['email'] == guest_detail['email']:
                    if guest_detail['guestId'] == '' or guest_detail['guestId'] is None:
                        logger.info("Missing guestId !! Retrying after 5 Seconds !!")
                        raise Exception("Missing guestId !! Retrying after 5 Seconds !!")
                    self.guest_data[count].update({
                        "guestId": guest_detail['guestId']
                    })
                    break
            else:
                raise StopLocust()
        for count, guest in enumerate(self.guest_data):
            body = {"guestIds": [guest['guestId']]}
            response_res_id = self.client.post('dxpcore/reservationguests/search/findbyguestids',
                                               name='TC-11 Get reservation guest id',
                                               json=body, headers=headers).json()
            for res_guest in response_res_id['_embedded']['reservationGuests']:
                if guest['guestId'] == res_guest['guestId']:
                    if res_guest['reservationGuestId'] == '' or res_guest['reservationGuestId'] is None:
                        logger.info("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                        raise Exception("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                    self.guest_data[count].update({
                        "reservationGuestId": res_guest['reservationGuestId'],
                        "reservationId": res_guest['reservationId']
                    })
                    break
            else:
                raise StopLocust()

    @seq_task(11)
    def signature_token_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('bookvoyage-bff/startup', name='TC-12 Get signature token', headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['signatureToken'] = "bearer " + response['tokendetails']['accessToken']

    @seq_task(12)
    def signature_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        self.user_data['client_transaction_id'] = generate_guid()
        self.user_data['consumer_id'] = self.user_data['client_transaction_id']
        headers = {
            "Authorization": self.user_data['signatureToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "clientTransactionId": self.user_data['client_transaction_id'],
            "signedFields": "clientTransactionId,currencyCode,clientReferenceNumber,transactionType,signedFields",
            "currencyCode": "USD",
            "clientReferenceNumber": self.user_data['reservationNumber'],
            "transactionType": "sale",
            "amount": str(self.user_data['amount'])

        }
        response = self.client.post('bookvoyage-bff/signature', name='TC-13 Make signature', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['signedFields'] = response['signedFields']
        self.user_data['signedTimeStamp'] = response['signedTimeStamp']
        self.user_data['signature'] = response['signature']

    @seq_task(13)
    def initiate_payment_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "billToCountryCode": "AT",
            "lastName": _data['firstName'],
            "signedTimeStamp": self.user_data['signedTimeStamp'],
            "signature": self.user_data['signature'],
            "billToState": _data['addresses'][0]['stateCode'],
            "clientTransactionId": self.user_data['client_transaction_id'],
            "signedFields": self.user_data['signedFields'],
            "clientReferenceNumber": self.user_data['reservationNumber'],
            "billToCity": _data['addresses'][0]['city'],
            "shipToCity": _data['addresses'][0]['city'],
            "billToZipCode": _data['addresses'][0]['zipCode'],
            "shipToLine2": _data['addresses'][0]['lineTwo'],
            "shipToLine1": _data['addresses'][0]['lineOne'],
            "requestData": "dummy",
            "shipToState": _data['addresses'][0]['stateCode'],
            "shipToLastName": _data['lastName'],
            "amount": str(self.user_data['amount']) + ".0",
            "billToLine2": _data['addresses'][0]['lineTwo'],
            "shipToZipCode": _data['addresses'][0]['zipCode'],
            "billToLine1": _data['addresses'][0]['lineOne'],
            "shipToFirstName": _data['lastName'],
            "consumer_id": self.user_data['consumer_id'],
            "clientUserIP": "103.93.185.99",
            "transactionType": "sale",
            "firstName": _data['lastName'],
            "consumerType": "DXPUserId",
            "shipToCountryCode": "AT",
            "currencyCode": "USD",
            "targetUrl": "https://localhost:8443"
        }
        headers = {
            "Authorization": self.user_data['signatureToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('payment-bff/initiatepayment', name='TC-14 Initiate payment', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['sessionKey'] = response['sessionKey']
        self.user_data['transactionId'] = response['transactionId']

    @seq_task(14)
    def authroization_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        if 'stage' in self.parent.host:
            self.parent.authorization_url = self.parent.authorization_url.replace('demohpp', 'hppstaging')
        _data = self.guest_data[0]
        body = {
            "bluefin_token": "",
            "payment_token": self.user_data['sessionKey'],
            "txn_amount": str(self.user_data['amount']) + '.0',
            "txn_currency": "USD",
            "credit_card": {
                "payment_method_type": "new_card",
                "card_number": "4111 1111 1111 1111",
                "card_scheme": "visa",
                "holder_full_name": f"{self.guest_data[0]['firstName']} {self.guest_data[0]['lastName']}",
                "card_expiry_month": "06",
                "card_expiry_year": "2033",
                "card_cvc": "123",
                "ats": "true"
            },
            "payment_type": "PREAUTH",
            "origin": {
                "hpp_type": "fullpageredirect",
                "hpp_origin": ""
            },
            "bill_to_details": {
                "first_name": self.guest_data[0]['firstName'],
                "last_name": self.guest_data[0]['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": self.guest_data[0]['addresses'][0]['city'],
                "stateId": "6557",
                "postal_code": self.guest_data[0]['addresses'][0]['zipCode'],
                "country": self.guest_data[0]['addresses'][0]['countryCode']
            },
            "ship_as_bill_details": "true",
            "ship_to_details": {
                "first_name": self.guest_data[0]['firstName'],
                "last_name": self.guest_data[0]['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": self.guest_data[0]['addresses'][0]['city'],
                "postal_code": self.guest_data[0]['addresses'][0]['zipCode'],
                "country": self.guest_data[0]['addresses'][0]['countryCode']
            }
        }
        headers = {"Content-Type": "application/json"}
        headers.update(self.user_data['headers'])
        response = self.client.post(self.parent.authorization_url, name='TC-15 Authorize payment', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['payment_token'] = response['payment_token']
        self.user_data['receiptReference'] = response['card_token']['receipt_reference']

    @seq_task(15)
    def transaction_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "transactionId": self.user_data['transactionId'],
            "billToCountryCode": _data['addresses'][0]['countryCode'],
            "billToLine2": _data['addresses'][0]['lineTwo'],
            "billToLine1": _data['addresses'][0]['lineOne'],
            "billToCity": _data['addresses'][0]['city'],
            "billToState": _data['addresses'][0]['stateCode'],
            "billToZipCode": _data['addresses'][0]['zipCode'],
            "cardUsername": _data['firstName'] + ' ' + _data['lastName'],
            "cvvNumber": 123,
            "cardExpiryMonth": "06",
            "cardExpiryYear": "33",
            "paymentToken": self.user_data['payment_token'],
            "gatewayPaymentToken": self.user_data['payment_token'],
            "isSaveCard": True,
            "cardScheme": "visa",
            "receiptReference": self.user_data['receiptReference'],
            "maskedPan": "411111******1111",
            "tokenProvider": "firstdata",
            "shipToCountryCode": _data['addresses'][0]['countryCode'],
            "shipToLine2": _data['addresses'][0]['lineTwo'],
            "shipToLine1": _data['addresses'][0]['lineOne'],
            "shipToCity": _data['addresses'][0]['city'],
            "shipToState": _data['addresses'][0]['stateCode'],
            "shipToZipCode": _data['addresses'][0]['zipCode'],
            "paymentMode": "CARD",
            "status": "SUCCESS",
            "statusCode": 0,
            "utcOffset": -330
        }
        headers = {
            "Authorization": self.user_data['signatureToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('payment-bff/transaction', name='TC-16 Payment transaction', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['responseSignature'] = response

    @seq_task(16)
    def pay_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "responseSignature": self.user_data['responseSignature'],
            "reservationNumber": self.user_data['reservationNumber'],
            "paymentInfo": {
                "paymentMode": "card",
                "paymentMethod": [{
                    "expiryDate": "06",
                    "cardHolderName": self.user_data['FirstName'] + ' ' + self.user_data['LastName'],
                    "cardType": "001",
                    "billingAddress": {
                        "zipCode": _data['addresses'][0]['zipCode'],
                        "lineTwo": _data['addresses'][0]['lineTwo'],
                        "city": _data['addresses'][0]['city'],
                        "countryCode": _data['addresses'][0]['countryCode'],
                        "lineOne": _data['addresses'][0]['lineOne'],
                        "state": _data['addresses'][0]['stateCode'],
                    }
                }],
                "currencyCode": "USD",
                "paidAmount": int(self.user_data['amount'])
            }
        }
        headers = {
            "Authorization": self.user_data['signatureToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('bookvoyage-bff/reservation/pay', name='TC-17 Pay for reservation', json=body,
                                    headers=headers)
        self.check_response_code(response)

    @seq_task(17)
    def user_account_service_user_profile(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('user-account-service/userprofile', name='TC-18 Userprofile',
                                   headers=headers)
        self.check_response_code(response)

    @seq_task(18)
    def get_wearable(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-id": self.guest_data[0]['reservationId'],
            "reservation-guest-id": self.guest_data[0]['reservationGuestId']
        }

        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('guest-dashboard-bff/wearable/delivery',
                                   name='TC-19 Get wearable', params=params,
                                   headers=headers).json()

    @seq_task(19)
    def discovery_startup(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('discovery-bff/startup', name='TC-20 Discovery bff startup', headers=headers)
        self.check_response_code(response)

    @seq_task(20)
    def discover_landing(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-id": self.guest_data[0]['reservationId'],
            "shipCode": self.user_data['shipCode']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('discovery-bff/discover/landing', name='TC-21 Discovery bff landing',
                                   params=params,
                                   headers=headers)
        self.check_response_code(response)

    @seq_task(21)
    def discover_lineup(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-id": self.guest_data[0]['reservationId'],
            "shipCode": self.user_data['shipCode']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'discovery-bff/discover/lineup/landing', name='TC-22 Discover lineup landing', params=params,
            headers=headers).json()

    @seq_task(22)
    def discover_ship(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-id": self.guest_data[0]['reservationId'],
            "shipCode": self.user_data['shipCode']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'discovery-bff/discover/ship/landing', name='TC-23 Discover ship landing', params=params,
            headers=headers).json()

    @seq_task(23)
    def discover_guides(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-id": self.guest_data[0]['reservationId'],
            "shipCode": self.user_data['shipCode']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'discovery-bff/discover/guides/landing', name='TC-24 Discover guides landing', params=params,
            headers=headers).json()

    @seq_task(24)
    def activity_reservation_resources(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('activity-reservation-system-bff/resources',
                                   name='TC-25 ARS resources', headers=headers).json()

    @seq_task(25)
    def get_port_code(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-number": self.user_data['reservationNumber']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'embarkation-service/reservation/summary/', name='TC-26 Reservation summary', params=params,
            headers=headers).json()

    @seq_task(26)
    def discover_ports_landing(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-id": self.guest_data[0]['reservationId'],
            "shipCode": self.user_data['shipCode']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'discovery-bff/discover/ports/landing', name='TC-27 Discover ports landing', params=params,
            headers=headers)
        self.check_response_code(response)

    @seq_task(27)
    def list_Activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        guestCount = self.user_data['guestCount']
        body = {
            "voyageNumber": self.user_data['voyageId'],
            "reservationNumber": self.user_data['reservationNumber'],
            "reservationGuestId": self.guest_data[0]['reservationGuestId'],
            "categoryCode": "PA",
            "guestCount": guestCount
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('activity-reservation-system-bff/v2/activities', name='TC-28 Activities list',
                                    json=body, headers=headers)
        self.check_response_code(response)
        response = response.json()
        for count, _activity in enumerate(response['activities']):
            if len(response['activities'][count]['activitySlots']) > 0:
                self.user_data['activityCode'] = _activity['activityCode']
                self.user_data['amount'] = _activity['amount']
                self.user_data['activitySlotCode'] = _activity['activitySlots'][0]['activitySlotCode']
                self.user_data['startTime'] = _activity['activitySlots'][0]['startDate']
                self.user_data['endTime'] = _activity['activitySlots'][0]['endDate']
                break

    @seq_task(28)
    def add_excursion_lovelist(self):
        """
        Get Token that we want to use here
        :return:
        """
        guest = self.guest_data[0]
        _num = self.user_data['reservationNumber']
        _id = guest['reservationGuestId']
        _res_id = guest['reservationId']
        body = {"reservationGuestId": _id, "categoryCode": "PA", "activityCode": self.user_data['activityCode'],
                "isFavourite": True}
        headers = {"Authorization": self.user_data['accessToken'], "Content-Type": "application/json"}
        headers.update(self.user_data['headers'])
        response = self.client.put('my-voyage-bff/favourites', name='TC-29 Add excursion to lovelist', json=body,
                                   headers=headers)

        params = {"reservationNumber": _num, "reservationGuestId": _id, "categoryCodes": "PA", "size": 10}
        response = self.client.get('my-voyage-bff/favourites', name='TC-30 Get added excursion to lovelist',
                                   json=body, params=params, headers=headers).json()

    @seq_task(29)
    def book_Activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        guest = self.guest_data[0]
        body = {
            "activityCode": self.user_data['activityCode'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": self.user_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": self.user_data['reservationNumber'],
                "guestId": guest['guestId']
            }],
            "activitySlotCode": self.user_data['activitySlotCode'],
            "accessories": [],
            "totalAmount": self.user_data['amount'],
            "operationType": None,
            "currencyCode": "USD"
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json",
            "correlationid": "89bjbncd-khssjdkhjed"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('activity-reservation-system-bff/v2/book',
                                    name='TC-31 Book activities', json=body, headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['amount'] = response['paymentDetails']['amount'].split('.')[0]
        self.user_data['signature'] = response['paymentDetails']['signature']
        self.user_data['signedTimeStamp'] = response['paymentDetails']['signedTimeStamp']
        self.user_data['clientTransactionId'] = response['paymentDetails']['clientTransactionId']
        self.user_data['consumerId'] = response['paymentDetails']['consumerId']
        self.user_data['signedFields'] = response['paymentDetails']['signedFields']
        self.user_data['clientReferenceNumber'] = response['paymentDetails']['clientReferenceNumber']
        self.user_data['clientToken'] = response['paymentDetails']['clientToken']
        self.user_data['appointmentLinkId'] = response['appointmentLinkId']

    @seq_task(30)
    def initiate_payment_activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "billToCountryCode": "AT",
            "lastName": _data['lastName'],
            "signedTimeStamp": self.user_data['signedTimeStamp'],
            "signature": self.user_data['signature'],
            "billToState": _data['addresses'][0]['stateCode'],
            "clientTransactionId": self.user_data['clientTransactionId'],
            "signedFields": self.user_data['signedFields'],
            "clientReferenceNumber": self.user_data['clientReferenceNumber'],
            "billToCity": _data['addresses'][0]['city'],
            "shipToCity": _data['addresses'][0]['city'],
            "billToZipCode": _data['addresses'][0]['zipCode'],
            "shipToLine2": _data['addresses'][0]['lineTwo'],
            "shipToLine1": _data['addresses'][0]['lineOne'],
            "requestData": "dummy",
            "shipToState": _data['addresses'][0]['stateCode'],
            "shipToLastName": _data['lastName'],
            "amount": str(self.user_data['amount']) + ".0",
            "billToLine2": _data['addresses'][0]['lineTwo'],
            "shipToZipCode": _data['addresses'][0]['zipCode'],
            "billToLine1": _data['addresses'][0]['lineOne'],
            "shipToFirstName": _data['lastName'],
            "consumerId": self.user_data['consumerId'],
            "clientUserIP": "103.93.185.99",
            "transactionType": "sale",
            "firstName": _data['lastName'],
            "consumerType": "DXPUserId",
            "shipToCountryCode": "AT",
            "currencyCode": "USD",
            "targetUrl": "https://localhost:8443"
        }
        headers = {
            "Authorization": self.user_data['clientToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('payment-bff/initiatepayment', name='TC-32 Activities initiate payment', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['sessionKey'] = response['sessionKey']
        self.user_data['transactionId'] = response['transactionId']

    @seq_task(31)
    def authroization_activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        if 'stage' in self.parent.host:
            self.parent.authorization_url = self.parent.authorization_url.replace('demohpp', 'hppstaging')
        _data = self.guest_data[0]
        body = {
            "bluefin_token": "",
            "payment_token": self.user_data['sessionKey'],
            "txn_amount": str(self.user_data['amount']) + '.0',
            "txn_currency": "USD",
            "credit_card": {
                "payment_method_type": "new_card",
                "card_number": "4111 1111 1111 1111",
                "card_scheme": "visa",
                "holder_full_name": f"{self.guest_data[0]['firstName']} {self.guest_data[0]['lastName']}",
                "card_expiry_month": "06",
                "card_expiry_year": "2033",
                "card_cvc": "123"
            },
            "origin": {
                "hpp_type": "fullpageredirect",
                "hpp_origin": ""
            },
            "bill_to_details": {
                "first_name": self.guest_data[0]['firstName'],
                "last_name": self.guest_data[0]['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": self.guest_data[0]['addresses'][0]['city'],
                "stateId": "6557",
                "postal_code": self.guest_data[0]['addresses'][0]['zipCode'],
                "country": self.guest_data[0]['addresses'][0]['countryCode']
            },
            "ship_as_bill_details": "True",
            "ship_to_details": {
                "first_name": self.guest_data[0]['firstName'],
                "last_name": self.guest_data[0]['lastName'],
                "street_1": "21",
                "apartment_number": "213",
                "city": self.guest_data[0]['addresses'][0]['city'],
                "postal_code": self.guest_data[0]['addresses'][0]['zipCode'],
                "country": self.guest_data[0]['addresses'][0]['countryCode']
            }
        }
        headers = {"Content-Type": "application/json"}
        headers.update(self.user_data['headers'])
        response = self.client.post(self.parent.authorization_url, name='TC-33 Activities authorize paymemnt',
                                    json=body, headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['payment_token'] = response['payment_token']
        self.user_data['receiptReference'] = response['card_token']['receipt_reference']

    @seq_task(32)
    def transaction_activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "transactionId": self.user_data['transactionId'],
            "billToCountryCode": _data['addresses'][0]['countryCode'],
            "billToLine2": _data['addresses'][0]['lineTwo'],
            "billToLine1": _data['addresses'][0]['lineOne'],
            "billToCity": _data['addresses'][0]['city'],
            "billToState": _data['addresses'][0]['stateCode'],
            "billToZipCode": _data['addresses'][0]['zipCode'],
            "cardUsername": _data['firstName'] + ' ' + _data['lastName'],
            "cvvNumber": 123,
            "cardExpiryMonth": "06",
            "cardExpiryYear": "33",
            "paymentToken": self.user_data['payment_token'],
            "gatewayPaymentToken": self.user_data['payment_token'],
            "isSaveCard": True,
            "cardScheme": "visa",
            "receiptReference": self.user_data['receiptReference'],
            "maskedPan": "411111******1111",
            "tokenProvider": "firstdata",
            "shipToCountryCode": _data['addresses'][0]['countryCode'],
            "shipToLine2": _data['addresses'][0]['lineTwo'],
            "shipToLine1": _data['addresses'][0]['lineOne'],
            "shipToCity": _data['addresses'][0]['city'],
            "shipToState": _data['addresses'][0]['stateCode'],
            "shipToZipCode": _data['addresses'][0]['zipCode'],
            "paymentMode": "CARD",
            "status": "SUCCESS",
            "statusCode": 0,
            "utcOffset": -330
        }
        headers = {
            "Authorization": self.user_data['clientToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('payment-bff/transaction', name='TC-34 activities payment transaction', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['paymentToken'] = response['paymentToken']
        self.user_data['signedFields'] = response['signedFields']
        self.user_data['signature'] = response['signature']
        self.user_data['signedTimeStamp'] = response['signedTimeStamp']
        self.user_data['clientTransactionId'] = response['clientTransactionId']
        self.user_data['clientReferenceNumber'] = response['clientReferenceNumber']
        self.user_data['amount'] = response['amount']
        self.user_data['transactionId'] = response['transactionId']
        self.user_data['consumerId'] = response['consumerId']

    @seq_task(33)
    def pay_activities(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        body = {
            "reservationGuestId": _data['reservationGuestId'],
            "appointmentLinkId": self.user_data['appointmentLinkId'],
            "paymentDetails": {
                "transactionId": self.user_data['transactionId'],
                "consumerId": self.user_data['consumerId'],
                "consumerType": "DXPUserId",
                "cardMaskedNo": "411111******1111",
                "cardType": "001",
                "cardExpiryMonth": "06",
                "cardExpiryYear": "33",
                "paymentToken": self.user_data['paymentToken'],
                "signedFields": self.user_data['signedFields'],
                "signature": self.user_data['signature'],
                "status": "ACCEPT",
                "statusCode": 100,
                "statusMessage": "Request successfully processed",
                "signedTimeStamp": self.user_data['signedTimeStamp'],
                "clientTransactionId": self.user_data['clientTransactionId'],
                "clientReferenceNumber": self.user_data['appointmentLinkId'],
                "amount": self.user_data['amount'],
                "currencyCode": "USD",
                "firstName": _data['firstName'],
                "lastName": _data['lastName'],
                "billToLine1": _data['addresses'][0]['lineOne'],
                "billToLine2": _data['addresses'][0]['lineTwo'],
                "billToCity": _data['addresses'][0]['city'],
                "billToState": _data['addresses'][0]['stateCode'],
                "billToCountryCode": _data['addresses'][0]['countryCode'],
                "billToZipCode": _data['addresses'][0]['zipCode'],
                "shipToLine2": _data['addresses'][0]['lineTwo'],
                "shipToLine1": _data['addresses'][0]['lineOne'],
                "shipToCity": _data['addresses'][0]['city'],
                "shipToState": _data['addresses'][0]['stateCode'],
                "shipToCountryCode": _data['addresses'][0]['countryCode'],
                "shipToZipCode": _data['addresses'][0]['zipCode'],
                "paymentMode": "card"
            }
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('activity-reservation-system-bff/pay', name='TC-35 Pay for activities',
                                    json=body, headers=headers)
        self.check_response_code(response)

    @seq_task(34)
    def verify_guest_activities_virgin(self):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        _res_num = self.user_data['reservationNumber']
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "activityCode": self.user_data['activityCode'],
            "reservationNumber": _res_num,
            "startTime": self.user_data['startTime'],
            "endTime": self.user_data['endTime']
        }
        response_userprofile = self.client.post('activity-reservation-system-bff/guestactivities',
                                                name='TC-36 Verify purchased activities',
                                                json=body, headers=headers).json()

    @seq_task(35)
    def verify_activities_virgin(self):
        """
        Verify that activities has been purchased
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        _res_num = self.user_data['reservationNumber']
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        body = {
            "activityCode": self.user_data['activityCode'],
            "reservationNumber": _res_num,
            "startTime": self.user_data['startTime'],
            "endTime": self.user_data['endTime']
        }
        response_userprofile = self.client.post('activity-reservation-system-bff/guestactivities',
                                                name='TC-37 Get sailor activities',
                                                json=body, params=params, headers=headers).json()

    @seq_task(36)
    def update_activities_virgin(self):
        """
        Update activities that has been purchased
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        second_guest = self.guest_data[1]
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "activityCode": self.user_data['activityCode'],
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": self.user_data['reservationNumber'],
            "isGift": False,
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": self.user_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CONFIRMED"
            },
                {
                    "personId": second_guest['reservationGuestId'],
                    "reservationNumber": self.user_data['reservationNumber'],
                    "guestId": second_guest['guestId']
                }],

            "activitySlotCode": self.user_data['activitySlotCode'],
            "accessories": [],
            "currencyCode": "USD",
            "appointmentLinkId": self.user_data['appointmentLinkId'],
            "operationType": "EDIT"
        }
        response_userprofile = self.client.post('activity-reservation-system-bff/v2/book',
                                                name='TC-38 Update activities',
                                                json=body, headers=headers)
        self.check_response_code(response_userprofile)
        response = response_userprofile.json()
        self.user_data['appointmentLinkIdUpdated'] = response['appointmentLinkId']

    @seq_task(37)
    def verify_update_activities_virgin(self):
        """
        Verify activities has been updated
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        response_userprofile = self.client.get('my-voyage-bff/guestItineraries',
                                               name='TC-39 Verify updated activities', params=params,
                                               headers=headers).json()

    @seq_task(38)
    def delete_activities_virgin(self):
        """
        Delete Activity
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        body = {
            "appointmentLinkId": self.user_data['appointmentLinkIdUpdated'],
            "isRefund": False,
            "operationType": "CANCEL",
            "loggedInReservationGuestId": guest['reservationGuestId'],
            "reservationNumber": self.user_data['reservationNumber'],
            "personDetails": [{
                "personId": guest['reservationGuestId'],
                "reservationNumber": self.user_data['reservationNumber'],
                "guestId": guest['guestId'],
                "status": "CANCELLED"
            }]
        }
        response_userprofile = self.client.post('activity-reservation-system-bff/v2/book',
                                                name='TC-40 Delete activities', json=body,
                                                headers=headers)
        self.check_response_code(response_userprofile)

    @seq_task(39)
    def verify_deleted_activities_virgin(self):
        """
        Verify Deleted Activities
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :return:
        """
        guest = self.guest_data[0]
        params = {
            "reservationGuestId": guest['reservationGuestId']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response_userprofile = self.client.get('my-voyage-bff/guestItineraries',
                                               name='TC-41 Verify deleted activities', params=params,
                                               headers=headers).json()

    @seq_task(40)
    def help_support_resource(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('dxp-helpsupport-bff/resources', name='TC-42 Helpsupport resources',
                                   headers=headers).json()

    @seq_task(41)
    def messaging_resource(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('dxp-messaging-bff/resources', name='TC-43 Messaging bff resources',
                                   headers=headers).json()

    @seq_task(42)
    def my_voyage_dashboard(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        params = {
            "reservationNumber": self.user_data['reservationNumber'],
            "reservationGuestId": self.guest_data[0]['reservationGuestId']

        }
        response = self.client.get('my-voyage-bff/dashboard', name='TC-44 My voyage bff dashboard', params=params,
                                   headers=headers).json()

    @seq_task(43)
    def voyage_account_settings_lookup(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('voyage-account-settings-bff/lookup', name='TC-45 Voyage setting bff lookup',
                                   headers=headers)
        self.check_response_code(response)

    @seq_task(44)
    def my_voyage_accounts_settings(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-number": self.user_data['reservationNumber'],
            "reservation-id": self.guest_data[0]['reservationId']
        }
        response = self.client.get(
            'voyage-account-settings-bff/landing', name='TC-46 Voyage setting bff landing', params=params,
            headers=headers)
        self.check_response_code(response)
        response = response.json()

    @seq_task(45)
    def voyage_account_setting_personal_info_virgin(self):
        """
        Check if the first and last name is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :param request:
        :return:
        """
        guest = self.guest_data[0]
        _num = self.user_data['reservationNumber']
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get(
            'voyage-account-settings-bff/user/personal', name='TC-47 Voyage setting bff personal',
            headers=headers).json()

    @seq_task(46)
    def signup_connect_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        _data = self.guest_data[0]
        self.user_data['password'] = "Yellow*99"
        self.user_data['LastName'] = generate_last_name(from_saved=True)
        self.user_data['FirstName'] = generate_first_name(from_saved=True)
        self.user_data['username'] = generate_email_id(first_name=self.user_data['FirstName'],
                                                       last_name=self.user_data['LastName'])
        self.user_data['BirthDate'] = _data['birthDate']
        contact_number = str(generate_phone_number(max_digits=10))
        body = {
            "contact_number": contact_number,
            "birthDate": self.user_data['BirthDate'],
            "email": self.user_data['username'],
            "firstName": self.user_data['FirstName'],
            "userType": "guest",
            "lastName": self.user_data['LastName'],
            "password": self.user_data['password']
        }
        headers = {
            "Authorization": self.request.basic_token,
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('user-account-service/signup', name='TC-48 Signup connect booking', json=body,
                                    headers=headers)
        self.check_response_code(response)

    @seq_task(47)
    def connect_booking(self):
        """
        Get Token that we want to use here
        :return:
        """
        guest = self.guest_data[0]
        _res_num = self.user_data['reservationNumber']
        _res_guest_id = guest['reservationGuestId']
        body = {
            "surname": guest['lastName'],
            "dateOfBirth": guest['birthDate'],
            "reservationId": _res_num,
            "guestId": guest['guestId'],
            "reservationGuestId": _res_guest_id
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('voyage-account-settings-bff/booking/connect', name='TC-49 Connect booking',
                                    json=body, headers=headers)

    @seq_task(48)
    def guest_dashboard_landing(self):
        """
        Get Token that we want to use here
        :return:
        """
        params = {
            "reservation-guest-id": self.guest_data[0]['reservationGuestId'],
            "reservation-number": self.user_data['reservationNumber']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('guest-dashboard-bff/landing', name='TC-50 Guest dashboard landing',
                                   params=params,
                                   headers=headers)

    @seq_task(49)
    def cancel_reservation(self):
        """
        Get Token that we want to use here
        :return:
        """
        body = {
            "reservationId": self.user_data['reservationNumber']
        }
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('reservation-service/reservations/cancel', name='TC-51 Cancel reservation',
                                    json=body, headers=headers)
        self.check_response_code(response)

    @seq_task(50)
    def logout(self):
        """
        Check if the first and last name is matching with the reservation booked
        :param config:
        :param test_data:
        :param rest_oci:
        :param guest_data:
        :param request:
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post(
            'user-account-service/logout', name='TC-52 Logout', headers=headers)
        self.check_response_code(response)


class SailorAppUser(HttpLocust):
    task_set = SailorApp
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host')
    args = parser.parse_known_args()
    host = args[0].host
    authorization_url = "https://demohpp.fmsapps.com/hpp/authorization"
    creds = read_creds(host)
    request = tokens.ShoreTokens(ship=None, shore=host)
    wait_time = between(5, 10)


if __name__ == "__main__":
    SailorAppUser().run()
