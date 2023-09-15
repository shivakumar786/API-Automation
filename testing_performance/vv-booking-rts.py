__author__ = 'Sarvesh.Singh'

from locust import HttpLocust, TaskSequence, seq_task, between
from locust.exception import StopLocust
from decurtis import tokens
from virgin_utils import *
import argparse
from decurtis.generate_mrz import GenerateMrzImages
from decurtis.generate_photo import GeneratePhoto


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
        self.authorization_url = self.parent.authorization_url
        self.request = self.parent.request
        self.user_data = dict()
        self.guest_data = None

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
                "status": "36",
                "guestCount": self.user_data['guestCount'],
                "sailors": user_data
            }],
            "paymentInfo": {"currencyCode": "USD"}
        }
        headers = {
            "Authorization": self.user_data['accessToken'], "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.post('bookvoyage-bff/booknow', name='TC-09 Book reservation', json=body,
                                    headers=headers)
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
        time.sleep(30)  # TODO Remove Delay
        response_userprofile = self.client.post('reservation-service/reservations/search/findbyreservationnumber',
                                                name='TC-10 Get guest id',
                                                json=body, headers=headers).json()
        for count, guest in enumerate(self.guest_data):
            for guest_detail in response_userprofile[0]['guestDetails']:
                if guest['email'] == guest_detail['email']:
                    if guest_detail['guestId'] == '' or guest_detail['guestId'] is None:
                        raise StopLocust()
                    self.guest_data[count].update({"guestId": guest_detail['guestId']})
                    break

        for count, guest in enumerate(self.guest_data):
            body = {"guestIds": [guest['guestId']]}
            response_res_id = self.client.post('dxpcore/reservationguests/search/findbyguestids',
                                               name='TC-11 Get reservation guest id',
                                               json=body, headers=headers).json()
            for res_guest in response_res_id['_embedded']['reservationGuests']:
                if guest['guestId'] == res_guest['guestId']:
                    if res_guest['reservationGuestId'] == '' or res_guest['reservationGuestId'] is None:
                        raise StopLocust()
                    self.guest_data[count].update({
                        "reservationGuestId": res_guest['reservationGuestId'],
                        "reservationId": res_guest['reservationId']
                    })
                    break

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
    def rts_bff_assets_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        self.client.get('rts-bff/assets', name='TC-18 Get rts assets', headers=headers)

    @seq_task(18)
    def start_up_virgin(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        response = self.client.get('rts-bff/startup', name='TC-19 Startu sailor app',
                                   headers=headers)
        self.check_response_code(response)
        response = response.json()
        self.user_data['lookupDataUrl'] = response['lookupDataURL']
        self.user_data['multimediaUploadURL'] = response['multimediaUploadURL']
        self.user_data['securityPhotoValidatorURL'] = response['securityPhotoValidatorURL']
        self.user_data['landingURL'] = response['landingURL']

    @seq_task(19)
    def health_check_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            response = self.client.get('rts-bff/healthcheck', name='TC-20 Healthcheck rts',
                                       params=params, headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['health_check_updateURL'] = response['updateURL']

    @seq_task(20)
    def look_up_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        headers = {
            "Authorization": self.user_data['accessToken'],
            "Content-Type": "application/json"
        }
        headers.update(self.user_data['headers'])
        self.client.get(self.user_data['lookupDataUrl'], name='TC-21 Look up sailor', headers=headers)

    @seq_task(21)
    def landing_check_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            _res = guest['reservationGuestId']
            _res_num = guest['reservationId']
            params = {
                "reservation-guest-id": _res,
                "reservation-number": _res_num
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/landing', name='TC-22 RTS landing check', params=params,
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

    @seq_task(22)
    def check_taskpercentage_before_rts_virgin(self):
        """
        Get Token that we want to use here
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-number": guest['reservationId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/landing', name='TC-23 RTS task percentage', params=params,
                                       headers=headers)
            self.check_response_code(response)

    @seq_task(23)
    def voyage_contract_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/voyagecontract', name='TC-24 Voyage contract get', params=params,
                                       headers=headers)
            self.check_response_code(response)

    @seq_task(24)
    def voyage_contract_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            body = {
                "isCruiseContractSigned": True,
                "contractSignedDate": str(datetime.now(tz=pytz.utc).date()),
                "signForOtherGuests": [],
                "signedByReservationGuestId": guest['reservationGuestId']
            }
            response = self.client.put('rts-bff/voyagecontract', name='TC-25 Voyage contract update', params=params,
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(25)
    def emergency_contract_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/emergencycontact', name='TC-26 Emergency contact get', params=params,
                                       headers=headers)
            self.check_response_code(response)

    @seq_task(26)
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
            headers.update(self.user_data['headers'])
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
            response = self.client.put(guest['emergencyContact_detailsURL'], name='TC-27 Emergency contact update',
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(27)
    def embarkation_slot_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/embarkationslot', name='TC-28 embarkation slot get', params=params,
                                       headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['isVip'] = response['isVip']

    @seq_task(28)
    def flight_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
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
            headers.update(self.user_data['headers'])
            body = {
                "flightDetails": flight_details,
                "isFlyingIn": True
            }
            self.guest_data[count].update(body)
            body = body
            response = self.client.put('rts-bff/flight', name='TC-29 Embarkation slot flight update', params=params,
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(29)
    def embarkation_slot_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
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
            headers.update(self.user_data['headers'])
            body = {
                "isFlyingIn": True,
                "isVip": self.user_data['isVip'],
                "flightDetails": flight_details,
                "slotNumber": 9,
                "isParkingOpted": False,
                "optedByReservationGuestIds": [],
                "postCruiseInfo": {"isFlyingOut": True, "flightDetails": flight_details}
            }
            response = self.client.put('rts-bff/embarkationslot', name='TC-30 Embarkation slot update', params=params,
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(30)
    def payment_get_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/paymentmethod', name='TC-31 Payment method get', params=params,
                                       headers=headers)
            self.check_response_code(response)
            response = response.json()
            self.user_data['paymentModes'] = response['paymentModes'][0]

    @seq_task(31)
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
            headers.update(self.user_data['headers'])
            url = guest['pregnancy_detailsURL']
            body = {
                "pregnancyDetails": {
                    "isPregnant": bool(random.getrandbits(1))
                }
            }
            response = self.client.put(url, name='TC-32 Pregnancy update',
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(32)
    def paymentmethod_update_call(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId'],
                "reservation-id": guest['reservationId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            body = {
                "selectedPaymentMethodCode": self.user_data['paymentModes'],
                "partyMembers": [],
                "isDeleted": False,
                "cardPaymentToken": str(generate_guid()).lower()
            }
            response = self.client.put('rts-bff/paymentmethod', name='TC-33 Payment update', params=params,
                                       json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(33)
    def upload_security_photo(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            first_name = guest['firstName']
            last_name = guest['lastName']
            email_id = guest['email']
            birth_date = guest['birthDate']
            security_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                           birth_date=birth_date).add_text()
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            headers.pop('Content-Type', None)
            files = {'file': open(security_photo, 'rb')}
            response = self.client.post('dxpcore/mediaitems?mediagroupid=f67c581d-4a9b-e611-80c2-00155df80332',
                                        name='TC-34 Upload security photo', files=files, headers=headers)
            self.check_response_code(response)
            guest['SecurityPhotoUrl'] = response.headers.get('Location', None)

    @seq_task(34)
    def get_security_photo(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            params = {
                "reservation-guest-id": guest['reservationGuestId']
            }
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            response = self.client.get('rts-bff/security',
                                       name='TC-35 Get security photo', params=params, headers=headers)
            self.check_response_code(response)

    @seq_task(35)
    def update_security_photo(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            body = {
                "securityPhotoURL": guest['SecurityPhotoUrl'],
                "isDeleted": False
            }
            response = self.client.put(guest['security_detailsURL'],
                                       name='TC-36 Update security photo', json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(36)
    def upload_travel_photo(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            # Generate Document
            passport_number = generate_document_number()
            passport_expiry = generate_document_expiry()
            guest['_exp_date'] = str(passport_expiry)
            guest['passport_number'] = passport_number
            gender = guest['genderCode']
            gender_code = gender[:1]
            country_code = convert_country_code(self.guest_data[0]['citizenshipCountryCode'], 3)
            mrz_data = {
                'document_type': "P",
                'country_code': country_code,
                'given_names': guest['firstName'],
                'surname': guest['lastName'],
                'document_number': passport_number,
                'birth_date': modify_birth_date(guest['birthDate']),
                'sex': gender_code,
                'expiry_date': str(passport_expiry.strftime('%y%m%d')),
                'nationality': country_code
            }
            _mrz = GenerateMrzImages(**mrz_data).mrz_image()
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            headers.pop('Content-Type', None)
            files = {'file': open(_mrz, 'rb')}
            response = self.client.post('dxpcore/mediaitems?mediagroupid=f67c581d-4a9b-e611-80c2-00155df80332',
                                        name='TC-37 Upload travel photo', files=files, headers=headers)
            self.check_response_code(response)
            guest['PassportDocumentId'] = response.headers.get('Location', None)

    @seq_task(37)
    def update_travel_photo(self):
        """
        Get Token that we want to use here TODO Update the documentation
        :return:
        """
        for count, guest in enumerate(self.guest_data):
            # Generate Document
            headers = {
                "Authorization": self.user_data['accessToken'],
                "Content-Type": "application/json"
            }
            headers.update(self.user_data['headers'])
            body = {
                "travelDocumentsDetail": {
                    "passport": {
                        "documentPhotoUrl": guest['PassportDocumentId'],
                        "nationalityCountryCode": convert_country_code(self.guest_data[0]['citizenshipCountryCode'], 3),
                        "surname": guest['lastName'],
                        "givenName": guest['firstName'],
                        "number": guest['passport_number'],
                        "issueCountryCode": "US",
                        "expiryDate": guest['_exp_date'],
                        "issueDate": "Feb 4 2011",
                        "isDeleted": False
                    }
                }
            }
            response = self.client.put(guest['travelDocuments_detailsURL'],
                                       name='TC-38 Update travel photo', json=body, headers=headers)
            self.check_response_code(response)

    @seq_task(38)
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
        response = self.client.post('reservation-service/reservations/cancel', name='TC-39 Cancel reservation',
                                    json=body,
                                    headers=headers)
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
