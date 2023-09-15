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
        self.guest_data = generate_guest_data(guest_count=1, guest_countries=['US'])
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
                "givenName": guest['firstName'], "lastName": guest['lastName'],
                "genderCode": guest['genderCode'], "dateOfBirth": guest['birthDate'],
                "citizenShip": guest['citizenshipCountryCode'], "email": guest['email'],
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
        response = self.client.get('bookvoyage-bff/startup', name='TC-10 Get signature token', headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['signatureToken'] = "bearer " + response['tokendetails']['accessToken']

    @seq_task(11)
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
        response = self.client.post('bookvoyage-bff/signature', name='TC-11 Make signature', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['signedFields'] = response['signedFields']
        self.user_data['signedTimeStamp'] = response['signedTimeStamp']
        self.user_data['signature'] = response['signature']

    @seq_task(12)
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
        response = self.client.post('payment-bff/initiatepayment', name='TC-12 Initiate payment', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['sessionKey'] = response['sessionKey']
        self.user_data['transactionId'] = response['transactionId']

    @seq_task(13)
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
        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post(self.parent.authorization_url, name='TC-13 Authorize payment', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['payment_token'] = response['payment_token']
        self.user_data['receiptReference'] = response['card_token']['receipt_reference']

    @seq_task(14)
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
        response = self.client.post('payment-bff/transaction', name='TC-14 Payment transaction', json=body,
                                    headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['responseSignature'] = response

    @seq_task(15)
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
                "paymentMethod": [
                    {
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
                    }
                ],
                "currencyCode": "USD",
                "paidAmount": int(self.user_data['amount'])
            }
        }
        headers = {
            "Authorization": self.user_data['signatureToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('bookvoyage-bff/reservation/pay', name='TC-15 Pay for reservation', json=body,
                                    headers=headers)
        self.check_response_code(response)

    @seq_task(16)
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
        response = self.client.post('reservation-service/reservations/cancel', name='TC-16 Cancel reservation',
                                    json=body, headers=headers)
        self.check_response_code(response)


class SailorAppUser(HttpLocust):
    task_set = SailorApp
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host')
    args = parser.parse_known_args()
    host = args[0].host
    authorization_url = "https://demohpp.fmsapps.com/hpp/authorization"
    creds = read_creds(host)
    request = tokens.ShoreTokens(shore=host, ship=None)
    wait_time = between(5, 10)


if __name__ == "__main__":
    SailorAppUser().run()
