__author__ = 'Sarvesh.Singh'

import shutil
import xlrd
import os
import openpyxl
import csv
import pytest
import pytz
from datetime import datetime
from datetime import date
import base64
from datetime import timedelta
from decurtis.common import *
from decurtis.workers import *
from timeout_decorator import timeout
from decurtis.bitbucket import BitBucketApi
from decurtis.helm_creds import HelmCreds
from decurtis.generate_photo import GeneratePhoto
from decurtis.generate_mrz import GenerateMrzImages
from decurtis.database import Database
from collections import namedtuple
from decurtis.logger import Logger
from decurtis.web_drivers import WebDriver
import xmltodict
from dict2xml import dict2xml
from decurtis.general import General
from pytest_pytestrail import pytestrail
import PyPDF2
import random

logger = Logger(name="VIRGIN").get_logger
VALID_RESPONSE_CODES = [200, 201]


def save_allure(**kwargs):
    """
    Override Function to save Allure Report
    :param kwargs:
    :return:
    """
    return General.save_allure(**kwargs)


def generate_guid():
    """
    Override function to generate GUID
    :return:
    """
    return General.generate_guid()


def urljoin(*args):
    """
    Override function to Join URL's
    :param args:
    :return:
    """
    return General.urljoin(*args)


def get_active_voyage_data(voyage):
    """
    Get active voyage in voyages (Virgin)
    :param voyage:
    :return:
    """
    test_data = dict()
    embark_date = datetime.strptime(voyage['embarkDate'], "%Y-%m-%dT%H:%M:%S").date()
    for window in [datetime.now(tz=pytz.utc).date() + timedelta(days=x) for x in range(0, 5)]:
        if embark_date >= window:
            test_data['shipCode'] = voyage['shipCode']
            test_data['voyageId'] = voyage['number']
            test_data['sailingEmbarkDate'] = voyage['embarkDate'].split("T")[0]
            test_data['sailingDebarkDate'] = voyage['debarkDate'].split("T")[0]
            return test_data
        break


def get_ship_time(rest_ship, config, test_data):
    """
    Get Ship Time using crew-bff/crew-embarkation/shiptime?shipcode={} Call
    :param test_data:
    :param rest_ship:
    :param config:
    :return:
    """
    # Get UTC Ship Time
    url = urljoin(config.ship.url, f"crew-bff/crew-embarkation/shiptime?shipcode={config.ship.code}")
    _content = rest_ship.send_request(method="GET", url=url, auth="bearer").content
    ship_date = datetime.strptime(_content['utcTimestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").astimezone(pytz.timezone('UTC'))
    test_data['current_ship_time'] = str(ship_date)[0:18]
    data = {
        'shipDate': ship_date, 'shipOffset': _content['shipOffset'], 'utcTimestamp': _content['utcTimestamp'],
        'epocTimestamp': _content['epocTimestamp']
    }
    return namedtuple('GenericDict', data.keys())(**data)


def get_ship_date(config, rest_oci, test_data):
    """
    Function to get the ship date
    :param test_data:
    :param rest_oci:
    :param config:
    """
    params = {"shipcode": config.ship.code}
    url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation/shiptime')
    _content = rest_oci.send_request(method="GET", url=url, params=params, auth="user").content
    test_data['shipDate'] = str(
    datetime.utcfromtimestamp(_content['epocTimestamp'] + 19800).date())


def payment_virgin(config, test_data, guest_data, rest_oci, amount, signature, signed_time_stamp, consumer_id,
                   signed_fields, client_ref_num):
    """
    Complete Payment for Info
    :param config:
    :param test_data:
    :param guest_data:
    :param rest_oci:
    :param amount:
    :param signature:
    :param signed_time_stamp:
    :param consumer_id:
    :param signed_fields:
    :param client_ref_num:
    :return:
    """
    guest = guest_data[0]

    url = urljoin(config.shore.url, "payment-bff/initiatepayment")
    body = {
        "billToCountryCode": "AT",
        "lastName": test_data['signupGuest']['lastName'],
        "signedTimeStamp": signed_time_stamp,
        "signature": signature,
        "billToState": test_data['signupGuest']['addresses'][0]['stateCode'],
        "clientTransactionId": consumer_id,
        "signedFields": signed_fields,
        "clientReferenceNumber": client_ref_num,
        "billToCity": test_data['signupGuest']['addresses'][0]['city'],
        "shipToCity": test_data['signupGuest']['addresses'][0]['city'],
        "billToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
        "shipToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
        "shipToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
        "requestData": "dummy",
        "shipToState": test_data['signupGuest']['addresses'][0]['stateCode'],
        "shipToLastName": test_data['signupGuest']['lastName'],
        "amount": f"{str(amount)}.0",
        "billToLine2": test_data['signupGuest']['addresses'][0]['lineOne'],
        "shipToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
        "billToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
        "shipToFirstName": test_data['signupGuest']['firstName'],
        "consumerId": consumer_id,
        "clientUserIP": "103.93.185.99",
        "transactionType": "sale",
        "firstName": test_data['signupGuest']['firstName'],
        "consumerType": "DXPUserId",
        "shipToCountryCode": "AT",
        "currencyCode": "USD",
        "targetUrl": "https://localhost:8443"
    }
    _initial = rest_oci.send_request(method="POST", url=url, json=body, auth='user').content

    url = 'https://demohpp.fmsapps.com/hpp/authorization'
    if config.envMasked == 'STAGE':
        url = url.replace('demohpp', 'hppstaging')
    body = {
        "bluefin_token": "",
        "payment_token": _initial['sessionKey'],
        "txn_amount": str(amount) + '.0',
        "txn_currency": "USD",
        "credit_card": {
            "payment_method_type": "new_card",
            "card_number": "4111 1111 1111 1111",
            "card_scheme": "visa",
            "holder_full_name": f"{test_data['signupGuest']['firstName']} {test_data['signupGuest']['lastName']}",
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
            "first_name": test_data['signupGuest']['firstName'],
            "last_name": test_data['signupGuest']['lastName'],
            "street_1": "21",
            "apartment_number": "",
            "city": test_data['signupGuest']['addresses'][0]['city'],
            "stateId": "6557",
            "postal_code": test_data['signupGuest']['addresses'][0]['zipCode'],
            "country": test_data['signupGuest']['addresses'][0]['countryCode']
        },
        "ship_as_bill_details": "true",
        "ship_to_details": {
            "first_name": test_data['signupGuest']['firstName'],
            "last_name": test_data['signupGuest']['lastName'],
            "street_1": "21",
            "apartment_number": "",
            "city": test_data['signupGuest']['addresses'][0]['city'],
            "postal_code": test_data['signupGuest']['addresses'][0]['zipCode'],
            "country": test_data['signupGuest']['addresses'][0]['countryCode']
        }
    }
    _auth = rest_oci.send_request(method="POST", url=url, json=body, auth=None).content
    is_key_there_in_dict('payment_token', _auth)
    assert _auth['status'] == 'SUCCESS', f"ERROR: Payment Status !!"
    assert _auth['response_message'] == 'Success', f"ERROR: Payment Response Message !!"
    assert _auth['payment_mode'] == 'card', f"ERROR: Payment Mode !!"
    test_data['paymentDetails'] = _auth

    url = _initial['_links']['transactionUrl']['href']
    body = {
        "transactionId": _auth['reference_number'],
        "billToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
        "billToLine2": test_data['signupGuest']['addresses'][0]['lineOne'],
        "billToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
        "billToCity": test_data['signupGuest']['addresses'][0]['city'],
        "billToState": test_data['signupGuest']['addresses'][0]['stateCode'],
        "billToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
        "cardUsername": f"{guest['firstName']} {guest['lastName']}",
        "cvvNumber": 123,
        "cardExpiryMonth": _auth['card_token']['expiry_date'][2::],
        "cardExpiryYear": _auth['card_token']['expiry_date'][0:2],
        "paymentToken": _auth['payment_token'],
        "gatewayPaymentToken": _auth['payment_token'],
        "isSaveCard": True,
        "cardScheme": _auth['card_token']['card_scheme'],
        "receiptReference": _auth['card_token']['receipt_reference'],
        "maskedPan": _auth['card_token']['masked_pan'],
        "tokenProvider": _auth['card_token']['token_provider'],
        "shipToCountryCode": test_data['signupGuest']['addresses'][0]['countryCode'],
        "shipToLine2": test_data['signupGuest']['addresses'][0]['lineTwo'],
        "shipToLine1": test_data['signupGuest']['addresses'][0]['lineOne'],
        "shipToCity": test_data['signupGuest']['addresses'][0]['city'],
        "shipToState": test_data['signupGuest']['addresses'][0]['stateCode'],
        "shipToZipCode": test_data['signupGuest']['addresses'][0]['zipCode'],
        "paymentMode": str(_auth['payment_mode']).upper(),
        "status": _auth['status'],
        "statusCode": _auth['status_code'],
        "utcOffset": -330
    }
    _transaction = rest_oci.send_request(method="POST", url=url, json=body, auth="user").content
    return _transaction


def cancel_reservation(config, test_data, rest_shore):
    """
    Cancel Reservation
    :param config:
    :param test_data:
    :param rest_shore:
    """
    rest_shore.userToken = test_data['signupGuest']['accessToken']
    try:
        url = urljoin(config.shore.url, "dxpcore/reservations/cancel")
        body = {"reservationId": test_data['reservationNumber']}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="User").content
        logger.debug(_content)
    except Exception as exp:
        logger.error(exp)
        pass


def add_celebration(config, test_data, guest_data, rest_shore):
    """
    Add Celebration
    :param config:
    :param test_data:
    :param guest_data:
    :param rest_shore:
    """
    rest_shore.userToken = test_data['userToken']
    for count, guest in enumerate(guest_data):
        try:
            url = urljoin(config.shore.url, f"dxpcore/reservationguests/{guest['reservationGuestId']}")
            body = {
                "guestTypeCode": config.vipLevel,
                "guestCelebrations": [
                    {
                        "celebrationDate": test_data['sailingEmbarkDate'],
                        "isDeleted": False,
                        "celebrationCode": config.celebrationLevel
                    }
                ]
            }
            _content = rest_shore.send_request(method="PATCH", url=url, json=body, auth="User").content
            logger.debug(_content)
        except Exception as exp:
            logger.error(exp)
            pass


@timeout(600)
def wait_for_guest_id(config, rest, guest_data, data):
    """
    Wait for Guest ID and other data to populate, retry after 5 seconds of interval
    This will timeout after 60 seconds with an exception
    :param config:
    :param rest:
    :param guest_data:
    :param data:
    :return:
    """
    while True:
        try:
            url = urljoin(config.shore.url, "dxpcore/reservations/search/findbyreservationnumber")
            body = {"reservationNumbers": [data['encResId']]}
            _content = rest.send_request(method="POST", url=url, json=body, auth="User").content[0]
            for count, guest in enumerate(guest_data):
                for guest_detail in _content['guestDetails']:
                    if guest['Email'] == guest_detail['email']:
                        if guest_detail['guestId'] == '' or guest_detail['guestId'] is None:
                            logger.info("Missing guestId !! Retrying after 5 Seconds !!")
                            raise Exception("Missing guestId !! Retrying after 5 Seconds !!")
                        guest_data[count].update(guest_detail)
                        break
                else:
                    raise Exception("guestId Not Found !!")
            return guest_data
        except Exception as exp:
            logger.debug(exp)
            time.sleep(5)
            pass


@timeout(300)
def wait_for_reservation_guest_id(config, rest, guest_data):
    """
    Wait for Guest ID and other data to populate, retry after 5 seconds of interval
    This will timeout after 60 seconds with an exception
    :param config:
    :param rest:
    :param guest_data:
    :return:
    """
    while True:
        try:
            url = urljoin(config.shore.url, "dxpcore/reservationguests/search/findbyguestids")
            for count, guest in enumerate(guest_data):
                body = {"guestIds": [guest['guestId']]}
                _content = rest.send_request(method="POST", url=url, json=body, auth="User").content
                for res_guest in _content['_embedded']['reservationGuests']:
                    if guest['guestId'] == res_guest['guestId']:
                        if res_guest['reservationGuestId'] == '' or res_guest['reservationGuestId'] is None:
                            logger.info("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                            raise Exception("Missing reservationGuestId !! Retrying after 5 Seconds !!")
                        guest_data[count].update(res_guest)
                        break
                else:
                    raise Exception("reservationGuestId Not Found !!")
            return guest_data
        except Exception as exp:
            logger.debug(exp)
            time.sleep(5)
            pass


@retry_when_fails(retries=120, interval=5)
def wait_for_signature(config, rest, amount_due, reservationNumber, tx_id):
    """
    Wait for bookvoyage-bff/signature call to retrieve data, it sometimes takes some time to come up.
    :param config:
    :param rest:
    :param amount_due:
    :param reservationNumber:
    :param tx_id:
    :return:
    """
    body = {
        "clientTransactionId": tx_id,
        "signedFields": "clientTransactionId,currencyCode,clientReferenceNumber,transactionType,signedFields",
        "currencyCode": "USD",
        "clientReferenceNumber": reservationNumber,
        "transactionType": "sale",
        "amount": str(amount_due)
    }
    url = urljoin(config.shore.url, "bookvoyage-bff/signature")
    _content = rest.send_request(method="POST", url=url, json=body, auth="user").content
    return _content


def verify_db_config(database, config, helm_values, comp):
    """
    Verify Database Configuration
    """
    _ship = config.ship.url
    _shore = config.shore.url
    _external_url_ship = urlsplit(_ship).hostname
    _external_url_shore = urlsplit(_shore).hostname

    if urlsplit(_ship).hostname == urlsplit(comp).hostname:
        _info_calls = helm_values.ship.info_calls
    elif urlsplit(_shore).hostname == urlsplit(comp).hostname:
        _info_calls = helm_values.shore.info_calls
    else:
        _info_calls = None

    _query = "select * from public.ufngetsettingvalueforverification();"
    _db_rows = database.run_and_fetch_data(query=_query)
    _db_check = "Pass"
    for _row in _db_rows:
        # Temporary Save DB Row's Values
        _key = _row['yamlkey']
        _value = _row['value']
        _place_holder = _row['value_with_placeholder']
        _category = _row['category']

        # Validate Internal and External URL's
        if _category == 'INTERNAL URL':
            _host = urlsplit(_value).hostname
            if _host in [_external_url_ship, _external_url_shore]:
                _db_check = "Fail"
                logger.warning(f"Internal URL Can't have {_host} as host")
            else:
                if _host in _info_calls:
                    _info_host = _info_calls[_host]
                    _helm_path = str(urlsplit(_info_host).path).split('/')[1]
                    _db_path = str(urlsplit(_value).path).split('/')[1]
                    if _helm_path != _db_path:
                        _db_check = "Fail"
                        logger.warning(f"DB: {_db_path} and Helm: {_helm_path} Don't match for {_host}")
                else:
                    logger.warning(f"{_host} not present in Helm Values")
        elif _category == 'EXTERNAL URL':
            _host = urlsplit(_value).hostname
            _host_place_holder = urlsplit(_place_holder).hostname
            if _host_place_holder in ["$external_domain_url_ship$", '$external_domain_url_ship_1$']:
                if _host not in [_external_url_ship]:
                    _db_check = "Fail"
                    logger.warning(f"{_key} → External Ship URL Can't be: {_host}")
            elif _host_place_holder == "$external_domain_url_shore$":
                if _host not in [_external_url_shore]:
                    _db_check = "Fail"
                    logger.warning(f"{_key} → External Shore URL Can't be: {_host}")
            elif _host_place_holder == "$external_domain_url$":
                if _host not in [_external_url_ship, _external_url_shore]:
                    _db_check = "Fail"
                    logger.warning(f"{_key} → External Domain URL Can't be: {_host}")
            else:
                continue
        elif _category == 'EXPOSED URL':
            continue
        else:
            raise Exception(f"Category {_category} Not Supported !!")

    if _db_check != "Pass":
        return False
    else:
        return True


def generate_guest_data(guest_count, guest_countries):
    """
    To create random apihit for load testing
    :param guest_count:
    :param guest_countries:
    """
    all_guest_details = []
    gender_codes = ['Male', 'Female']
    unique_names = []
    for count in range(guest_count):
        if len(guest_countries) > 1:
            country = random.choice(guest_countries)
        else:
            country = guest_countries[0]
        first_name = generate_first_name(from_saved=True)
        last_name = generate_last_name(from_saved=True)
        name = f"{first_name} {last_name}"

        # Make sure we have a unique name for all guests in one single reservation
        while name in unique_names:
            first_name = generate_first_name(from_saved=True)
            last_name = generate_last_name(from_saved=True)
            name = f"{first_name} {last_name}"
            continue
        unique_names.append(name)
        email_id = generate_email_id(first_name=first_name, last_name=last_name)
        # We make sure the One Adult, One Child and One Minor
        if count in [0, 1]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        elif count == 3:  # 4th Guest as always Minor
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        else:  # 3rd and other guests are randomly chose between adult and child
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        if count in [0, 4]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        body = {
            "firstName": first_name, "lastName": last_name, "genderCode": random.choice(gender_codes),
            "birthDate": birth_date, "citizenshipCountryCode": country, "email": email_id,
            "phones": [{"number": str(generate_phone_number(max_digits=10)), "phoneTypeCode": "Home"}],
            "addresses": [{
                "lineOne": "221b Baker Street", "lineTwo": "wallaby way",
                "city": "Miami", "stateCode": "FL", "countryCode": "US", "zipCode": "33012"
            }]
        }
        all_guest_details.append(body)
    return all_guest_details


def read_creds(shore):
    """
    Read token from creds file to use in locust
    :param shore:
    :return:
    """
    data = get_environment_data(ship=None, shore=shore, nt=False)
    _data = HelmCreds(ship=None, shore=shore).read_helms_data()
    _auth_moci = _data.moci
    _auth_oci = _data.book
    return _auth_moci, _auth_oci


@pytest.fixture(scope="session")
def db_guest(config, db_details):
    """
    Guest Database for Virgin Only
    :param config:
    :param db_details:
    :return:
    """
    nt = namedtuple('vv', "ship shore")
    # vv guest database for ship
    ship = Database(
        host=db_details.ship.host, username=db_details.ship.username, password=db_details.ship.password,
        port=db_details.ship.port, database='dxpcore'
    )

    # vv guest database for shore
    shore = Database(
        host=db_details.shore.host, username=db_details.shore.username, password=db_details.shore.password,
        port=db_details.shore.port, database='dxpcore'
    )

    return nt(ship=ship, shore=shore)


@pytest.fixture(autouse=True, scope='session')
def cancel_reservation_at_end(config, rest_shore, test_data, guest_data):
    """
    Function to cancel reservation at the end
    :param config:
    :param rest_shore:
    :param test_data:
    :param guest_data:
    :return:
    """
    yield

    # We cancel reservation for Virgin at the end of session
    if config.cancel:
        cancel_reservation(config, test_data=test_data, rest_shore=rest_shore)

    # We add the vip level and celebration level if needed
    if config.extra:
        add_celebration(config, test_data=test_data, guest_data=guest_data, rest_shore=rest_shore)


def get_all_trackables(config, rest_oci):
    """
    get all the trackables for dxp.
    :param config:
    :param rest_oci:
    """
    _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "trackables")
    content = rest_oci.send_request(method='GET', url=_url, auth="bearer").content
    trackable_uuids = []
    for trackable in content['_embedded']['trackables']:
        for _key in trackable.keys():
            if _key == 'uuid':
                trackable_uuids.append(trackable['uuid'])
            else:
                continue
    if trackable_uuids is not None:
        return random.choice(trackable_uuids)
    else:
        logger.debug("Virgin trackables UUIDs are not available...")


def next_year_date(date):
    """
    check february's days.
    :param date:
    """
    dates = date.split('-')
    month = dates[1]
    year = dates[0]
    day = dates[2]
    if month == '02':
        day = '26'
        year = int(year) + 1
    year = int(year) + 1
    date = f"{year}-{month}-{day}"
    return date


def change_epoch_time(date):
    """
    Change date and time in epoch milliseconds
    param date:
    """
    pattern = '%Y-%m-%d %H:%M:%S'
    mil_sec_time = f"{date} 0:0:0"
    epoch = int(time.mktime(time.strptime(mil_sec_time, pattern)))
    return epoch


def change_epoch_of_datetime(mydatetime):
    """
    convert datetime to 24 hours format and get epoch time
    param datetime:
    """
    time = mydatetime[11:]
    date = mydatetime[:10]
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if time[-2:] == "AM" and time[:2] == "12":
        data = date + " " + "00" + time[2:-3]
        # remove the AM
    elif time[-2:] == "AM":
        data = date + " " + time[:-3]

        # Checking if last two elements of time
    # is PM and first two elements are 12
    elif time[-2:] == "PM" and time[:2] == "12":
        data = date + " " + time[:-3]

    else:

        # add 12 to hours and remove PM
        data = date + " " + str(int(time[:2]) + 12) + time[2:8]

    # Driver Code
    epoch = datetime(1970, 1, 1)

    myformat = "%Y-%m-%d %H:%M:%S"

    mydt = datetime.strptime(data, myformat)

    epoch = (mydt - epoch).total_seconds() * 1000

    return epoch


def four_digit_random_number():
    number = random.randint(1111, 9999)
    return number


def twenty_four_hour_format_converter(input_time):
    if input_time[-2:] == "AM" and input_time[:2] == "12":
        return "00" + input_time[2:-2]
    elif input_time[-2:] == "AM":
        return input_time[:-2]
    elif input_time[-2:] == "PM" and input_time[:2] == "12":
        return input_time[:-2]
    else:
        return str(int(input_time[:2]) + 12) + input_time[2:8]


def get_pending_and_pending_overdue_guest(db_core, test_data, rest_shore, _shore, config):
    """
    Fetch the guest in shore core DB.
    :param db_core:
    :param test_data:
    :param rest_shore:
    :param _shore:
    :param config:
    """
    if len(test_data['voyage']) >= 1:
        embark_date = test_data['voyage']['embarkDate']
        debark_date = test_data['voyage']['debarkDate']
        voyage_number = test_data['voyage']['id']

        _query = f"select * from guestmoderationdetail g  where reservationguestid  in (select reservationguestid from " \
                 f"reservationguest r2 where embarkdate = '{embark_date}' and debarkdate = '{debark_date}'and " \
                 f"reservationstatuscode = 'RS' and isprimary = True) and g.verificationstatuscode in ('P','PO');"

        response = db_core.shore.run_and_fetch_data(query=_query)
        if len(response) > 0:
            for count, details in enumerate(response):
                rest_shore.session.headers.update({'Content-Type': 'application/json'})
                _url = urljoin(_shore, f"dxpcore/reservationguests/{details['reservationguestid']}")
                content = rest_shore.send_request(method='GET', url=_url, auth="bearer").content
                query = f"SELECT * FROM reservation WHERE reservationid = '{content['reservationId']}';"
                response1 = db_core.shore.run_and_fetch_data(query=query)
                _url = urljoin(_shore,
                               "/dxpcore/reservationevents/search/getguestsdetailbyreservationnumber")
                param = {
                    "reservationnumber": response1[0]['reservationnumber']
                }
                content = rest_shore.send_request(method='GET', url=_url, auth="bearer",
                                                  params=param).content
                for num, data in enumerate(content['guestDetails']):
                    if data['reservationGuestId'] == details['reservationguestid']:
                        dob_year = int(data['birthDate'].split("-")[0])
                        current_year = int(str(datetime.now()).split("-")[0])
                        adult = current_year - dob_year
                        if 18 < adult:
                            if response1[0]['shipcode'] == config.ship.code:
                                return details
                else:
                    continue

        else:
            raise Exception(" VV ship Future voyage data is not available in DB !!")
    else:
        raise Exception(" Future voyage is not available !!")


def get_united_state_pending_and_pending_overdue_guest(db_core, test_data, rest_shore, _shore, config):
    """
    Fetch the united state pending and oending overdue guest in shore core DB.
    :param db_core:
    :param test_data:
    :param rest_shore:
    :param _shore:
    :param config:
    """
    if len(test_data['voyage']) >= 1:
        embark_date = test_data['voyage']['embarkDate']
        debark_date = test_data['voyage']['debarkDate']
        voyage_number = test_data['voyage']['id']

        _query = f"select g.citizenshipcountrycode , gm.* from guestmoderationdetail gm  join reservationguest rg on " \
                 f"gm.reservationguestid = rg.reservationguestid join guest g on g.guestid = rg.guestid where " \
                 f"rg.embarkdate = '{embark_date}' and rg.debarkdate = '{debark_date}'and rg.reservationstatuscode = 'RS' " \
                 f"and rg.isprimary = True and gm.verificationstatuscode in ('P','PO'); "

        response = db_core.shore.run_and_fetch_data(query=_query)
        if len(response) > 0:
            for count, details in enumerate(response):
                if details['citizenshipcountrycode'] == "US":
                    rest_shore.session.headers.update({'Content-Type': 'application/json'})
                    _url = urljoin(_shore, f"dxpcore/reservationguests/{details['reservationguestid']}")
                    content = rest_shore.send_request(method='GET', url=_url, auth="bearer").content
                    query = f"SELECT * FROM reservation WHERE reservationid = '{content['reservationId']}';"
                    response1 = db_core.shore.run_and_fetch_data(query=query)
                    _url = urljoin(_shore,
                                   "/dxpcore/reservationevents/search/getguestsdetailbyreservationnumber")
                    param = {
                        "reservationnumber": response1[0]['reservationnumber']
                    }
                    content = rest_shore.send_request(method='GET', url=_url, auth="bearer",
                                                      params=param).content
                    for num, data in enumerate(content['guestDetails']):
                        if data['reservationGuestId'] == details['reservationguestid']:
                            dob_year = int(data['birthDate'].split("-")[0])
                            current_year = int(str(datetime.now()).split("-")[0])
                            adult = current_year - dob_year
                            if 18 < adult:
                                if response1[0]['shipcode'] == config.ship.code:
                                    return details
                    else:
                        continue

        else:
            raise Exception(" DD ship Future voyage data is not available in DB !!")
    else:
        raise Exception(" Future voyage is not available !!")


def get_indian_pending_and_pending_overdue_guest(db_core, test_data, rest_shore, _shore, config):
    """
    Fetch the Indian pending and pending overdue guest in shore core DB.
    :param db_core:
    :param test_data:
    :param rest_shore:
    :param _shore:
    :param config:
    """
    if len(test_data['voyage']) >= 1:
        embark_date = test_data['voyage']['embarkDate']
        debark_date = test_data['voyage']['debarkDate']
        voyage_number = test_data['voyage']['id']

        _query = f"select g.citizenshipcountrycode , gm.* from guestmoderationdetail gm  join reservationguest rg on " \
                 f"gm.reservationguestid = rg.reservationguestid join guest g on g.guestid = rg.guestid where " \
                 f"rg.embarkdate = '{embark_date}' and rg.debarkdate = '{debark_date}'and rg.reservationstatuscode = 'RS' " \
                 f"and rg.isprimary = True and gm.verificationstatuscode in ('P','PO'); "

        response = db_core.shore.run_and_fetch_data(query=_query)
        if len(response) > 0:
            for count, details in enumerate(response):
                if details['citizenshipcountrycode'] == "IN":
                    rest_shore.session.headers.update({'Content-Type': 'application/json'})
                    _url = urljoin(_shore, f"dxpcore/reservationguests/{details['reservationguestid']}")
                    content = rest_shore.send_request(method='GET', url=_url, auth="bearer").content
                    query = f"SELECT * FROM reservation WHERE reservationid = '{content['reservationId']}';"
                    response1 = db_core.shore.run_and_fetch_data(query=query)
                    _url = urljoin(_shore,
                                   "/dxpcore/reservationevents/search/getguestsdetailbyreservationnumber")
                    param = {
                        "reservationnumber": response1[0]['reservationnumber']
                    }
                    content = rest_shore.send_request(method='GET', url=_url, auth="bearer",
                                                      params=param).content
                    for num, data in enumerate(content['guestDetails']):
                        if data['reservationGuestId'] == details['reservationguestid']:
                            dob_year = int(data['birthDate'].split("-")[0])
                            current_year = int(str(datetime.now()).split("-")[0])
                            adult = current_year - dob_year
                            if 18 < adult:
                                if response1[0]['shipcode'] == config.ship.code:
                                    return details
                    else:
                        continue

        else:
            raise Exception(" DD ship Future voyage data is not available in DB !!")
    else:
        raise Exception(" Future voyage is not available !!")


def upload_guest_media_file(test_data, rest_ship, couch, config):
    """
    User upload photo
    """
    first_name = test_data['guest_detail']['fname']
    last_name = test_data['guest_detail']['lname']
    email_id = f"{first_name}.{last_name}@test.com"
    birth_date = test_data['guest_detail']['dob']
    gender = test_data['guest_detail']['gender']
    profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                  birth_date=birth_date, gender=gender).add_text()
    logger.debug(f"Uploading Profile Photo #1 ...")
    url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
    params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
    files = {"file": open(profile_photo, "rb")}
    content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
        "Location"]
    test_data['profilePhotoUrl'] = content.rsplit('/', 1)[1]
    for count, details in enumerate(test_data['guests_details']):
        if details['FirstName'] == first_name.strip():
            test_data['guest_detail']['res_id'] = details['ReservationGuestID']
            break
    url = urljoin(config.ship.sync, f"GuestPersonalInformation::{test_data['guest_detail']['res_id']}")
    for i in range(0, 5):
        try:
            finalJson = couch.send_request(method="GET", url=url, auth="basic").content
            finalJson.update({
                'GuestSecurityMediaItemID': test_data['profilePhotoUrl'],
                "lastModifiedBy": "Script Automation",
                "sourceId": "CouchDatabase",
            })
            couch.send_request(method="PUT", url=url, json=finalJson, auth="basic")
            break
        except (Exception, ValueError) as Exp:
            logger.error(f"Sailor image Create failed {Exp}, retrying ...")
    else:
        raise Exception(f"Sailor Photo not updated via sync after 5 tries !!")

# def upload_guest_identification_image(test_data, rest_ship, couch, config):
#     """
#     User upload photo
#     """
#     first_name = test_data['guest_detail']['fname']
#     last_name = test_data['guest_detail']['lname']
#     _date = test_data['guest_detail']['dob'].strip().split("/")
#     dob = f"{_date[2]}-{_date[0]}-{_date[1]}"
#     gender = 'M' if test_data['guest_detail']['gender'].upper() == 'MALE' else 'F'
#     passport_number = str(generate_document_number())
#     passport_expiry = date_compare()
#     # visa_expiry = date_compare()
#     # visa_number = generate_document_number()
#     country_code = convert_country_code(test_data['citizenshipCountryCode'], 3)
#     mrz_data = {
#         'document_type': "P",
#         'country_code': country_code,
#         'given_names': first_name,
#         'surname': last_name,
#         'document_number': passport_number,
#         'birth_date':modify_birth_date(dob),
#         'sex': gender,
#         'expiry_date': str(passport_expiry.strftime('%y%m%d')),
#         'nationality': country_code
#     }
#     # Passport mrz image
#     mrz_image = GenerateMrzImages(**mrz_data).mrz_image()
#     # Visa mrz image
#     # del mrz_data['document_number']
#     # mrz_data['document_type'] = "V"
#     # mrz_data['expiry_date'] = str(visa_expiry.strftime('%y%m%d'))
#     # mrz_data['document_number'] = generate_document_number()
#     # mrz_visa_image = GenerateMrzImages(**mrz_data).mrz_image()
#     # _visa_id = upload_media_file(config, rest_ship, mrz_visa_image)
#     # identification_photo = GenerateMrzImages(document_type="P", country_code="USA", surname=last_name, given_names=first_name, document_number="WP9281A96", nationality="USA", birth_date="950601", sex=gender, expiry_date="260418").mrz_image()
#     logger.debug(f"Uploading Document Photo #1 ...")
#     url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
#     params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
#     files = {"file": open(mrz_image, "rb")}
#     content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
#         "Location"]
#     test_data['docPhotoUrl'] = content.rsplit('/', 1)[1]
#     for count, details in enumerate(test_data['guests_details']):
#         if details['FirstName'] == first_name.strip():
#             test_data['guest_detail']['res_id'] = details['ReservationGuestID']
#             break
#     url = urljoin(config.ship.sync, f"GuestIdentification::{test_data['guest_detail']['res_id']}")
#     doc_id = generate_guid()
#     for i in range(0, 5):
#         try:
#             _url = urljoin(config.ship.sync, f"GuestPersonalInformation::{test_data['guest_detail']['res_id']}")
#             Ginfo = couch.send_request(method="GET", url=_url, auth="basic").content
#             finalJson = couch.send_request(method="GET", url=url, auth="basic").content
#             finalJson['GuestDocuments'].update({
#                   "DocumentID": doc_id,
#                   "DocumentType": "P",
#                   "IsDeleted": False,
#                   "IsVerifiedAtTerminal": False
#                 })
#             finalJson['Identifications'].update({
#                           "BirthDateEpoch": Ginfo['BirthDateEpoch'],
#                           "DocumentTypeCode": "P",
#                           "ExpiryDateEpoch": 1924713000000,
#                           "FirstName": first_name,
#                           "GenderCode": gender,
#                           "GuestID": Ginfo['GuestID'],
#                           "IdentificationID": doc_id,
#                           "IsModerateOnlineCheckInDone": False,
#                           "IsPersonalInformationMismatch": False,
#                           "IsVerifiedAtTerminal": True,
#                           "IssueCountryCode": "US",
#                           "LastName": last_name,
#                           "Number": 1234556666,
#                           "ScannedCopyMediaItemID": test_data['docPhotoUrl'],
#                           "isOcrDirty": False,
#                           "lastModifiedDateEpoch": 1652357078456
#                         })
#             couch.send_request(method="PUT", url=url, json=finalJson, auth="basic")
#             break
#         except (Exception, ValueError) as Exp:
#             logger.error(f"Sailor image Create failed {Exp}, retrying ...")
#     else:
#         raise Exception(f"Sailor Photo not updated via sync after 5 tries !!")

def date_compare():
    """
    Document exp. date compare to current date.
    :return:
    """
    today = str(date.today()+timedelta(days=10))
    doc_date = generate_document_expiry()
    today_date = today.split("-")
    d1 = datetime(int(today_date[0]), int(today_date[1]), int(today_date[2]))
    future_date = str(doc_date).split("-")
    d2 = datetime(int(future_date[0]), int(future_date[1]), int(future_date[2]))
    if d1 > d2:
        doc_date = generate_document_expiry()
        return doc_date
    else:
        return doc_date