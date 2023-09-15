__author__ = 'vikesh'

from virgin_utils import *


@pytest.mark.xfail(reason='DCP-95630')
@pytest.mark.VXP_MXP
@pytest.mark.run(order=42)
class TestVxpMxp:
    """
    Test suite to verify vxp to mxp integration.
    """

    @pytestrail.case(44390062)
    def test_01_check_env(self, config, test_data):
        """
        To check execution environment
        params: config
        params: test_data
        """
        if config.envMasked == "INTEGRATION":
            test_data['mxp_db'] = "MXP_INT"
        else:
            test_data['mxp_db'] = "MXP"

    @pytestrail.case(44346733)
    def test_02_verify(self, db_mxp, test_data, guest_data, verification):
        """
        verify the reservation exits in MXP
        params: db_mxp
        params: test_data
        params: guest_data
        params: verification
        """
        data = verification.sql['mxp_db_query']['email_verification']
        query = data.format(test_data['mxp_db'], guest_data[0]['email'])
        cursor = db_mxp.ship.run_and_fetch_data(query=query)
        assert len(cursor) != 0, "record is not synced in mxp"

        assert guest_data[0]['email'] == cursor[0]['EMAIL'], 'email id is not available in mxp record'

        test_data['mxp_email'] = guest_data[0]['email']

    @pytestrail.case(44346734)
    def test_03_onboard_mxp(self, db_core, db_mxp, test_data, guest_data, verification):
        """
        This is to check guest onboard status sync from db core to mxp.
        params: db_core
        params: db_mxp
        params: test_data
        params: guest_data
        params: verification
        """
        _data = verification.sql["guest_onboard_status_db_core"]["onboard_status"]
        _query = _data.format(guest_data[0]["reservationGuestId"], test_data['embarkDate'])
        onboard_status = db_core.ship.run_and_fetch_data(query=_query)

        data = verification.sql['mxp_db_query']['onboard']
        query = data.format(test_data['mxp_db'], guest_data[0]['email'])
        mxp_data = db_mxp.ship.run_and_fetch_data(query=query)
        guest_status = []
        if len(mxp_data) != 0:
            guest_status.append("ONBOARD")
        if onboard_status != guest_status:
            logger.debug("guest data is not synced")

    @pytestrail.case(46177472)
    def test_04_verify_person(self, db_mxp, test_data, guest_data, verification):
        """
        verify name and dob in vxp to mxp
        params: db_mxp
        params : test_data
        params: guest_data
        params: verification

        """
        data = verification.sql['mxp_db_query']['verify_person_name']
        query = data.format(test_data['mxp_db'], guest_data[0]['guestId'])
        cursor = db_mxp.ship.run_and_fetch_data(query=query)
        if len(cursor) == 0:
            raise Exception("record is not available")

        assert guest_data[0]['FirstName'] == cursor[0]['PERSON_FIRST_NAME'], "First name miss matched"
        assert guest_data[0]['LastName'] == cursor[0]['PERSON_LAST_NAME'], "Last name miss matched"

    @pytestrail.case(9918215)
    def test_05_verify_person_contact_info(self, config, db_mxp, test_data, guest_data, rest_shore, verification):
        """
        verify person contact info in mxp
        params: config
        params: db_mxp
        params: test_data
        params: guest_data
        params: rest_shore
        params: verification
        """
        _url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), f"/guests/{guest_data[0]['guestId']}")
        _content = rest_shore.send_request(method='GET', url=_url, auth="bearer").content

        data = verification.sql['mxp_db_query']['verify_contact_info']
        query = data.format(test_data['mxp_db'], guest_data[0]['guestId'])
        cursor = db_mxp.ship.run_and_fetch_data(query=query)

        if (cursor[0]['PERSON_PRIMARY_PHONE'] != _content['phones']) and len(_content['phones']) != 0:
            raise Exception("Phone number miss matched")

    @pytestrail.case(9918218)
    def test_06_verify_charge_id(self, db_mxp, test_data, guest_data, verification):
        """
        verify charge id vxp to mxp
        params: db_mxp
        params: test_data
        params: guest_data
        params: verification
        """
        _data = verification.sql['mxp_db_query']['verify_sync']
        _query = _data.format(test_data['mxp_db'], guest_data[0]['reservationGuestId'])
        res = db_mxp.ship.run_and_fetch_data(_query)
        if not res[0]['CHARGE_ID']:
            raise Exception("charge Id Not found")

    @pytestrail.case(9918214)
    def test_07_verify_credit_card_info_in_mxp(self, config, test_data, rest_ship, db_mxp, verification):
        """
        verify credit card info vxp to mxp
        params: config
        params: rest_ship
        params: db_mxp
        params: test_data
        params: verification
        """
        _res_id = "d33f1e9c-7a41-4953-8e7b-48bb64905611"
        _url = f"{config.ship.sync}/GuestPayForDetail::{_res_id}"
        _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content

        if 'PaymentMethodDetail' not in _content:
            pytest.skip(msg="Payment detail is not available")
        is_key_there_in_dict('PaymentMode', _content)
        is_key_there_in_dict('PaymentModeID', _content)
        credit_card_type = _content['PaymentMethodDetail']['CreditCardType']
        name_on_credit_card = _content['PaymentMethodDetail']['NameOnCreditCard']

        data = verification.sql['mxp_db_query']['verify_credit_card_info']
        query = data.format(test_data['mxp_db'], name_on_credit_card)

        mxp_data = db_mxp.ship.run_and_fetch_data(query=query)

        assert mxp_data[0]['NAME_ON_CARD'] != name_on_credit_card, "credit card info not available"

    @pytestrail.case(9918212)
    def test_08_verify_aci_dashboard_count_in_mxp(self, config, couch, db_mxp, test_data, verification):

        """
        verify aci checkin or onboard count to mxp
        params: config
        params: couch
        params: db_mxp
        params: test_data
        params: verification
        """

        embarkdate = test_data['embarkDate'][:10]
        data = verification.couch_queries['guest_onboard'].format(config.ship.couch.bucket, embarkdate)
        query = f"query?Statement={data}"
        url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=url, auth='basic', timeout=60).content
        couch_onboard_guest_count = _content['results'][0]['$1']

        data = verification.sql['mxp_db_query']['verify_aci_onboard_guest']
        query = data.format(test_data['mxp_db'], test_data['embarkDate'])

        mxp_data = db_mxp.ship.run_and_fetch_data(query=query)
        assert len(mxp_data) == couch_onboard_guest_count, "Guest count is not matched"

    @pytestrail.case(1853264)
    def test_09_verify_ars_booking_activity(self, config, rest_ship, test_data, guest_data):
        """
        verify ars booking details in mxp
        params: config
        params: rest_ship
        params: test_data
        params: guest_data
        """
        current_date = str(datetime.today().now()).split(" ")
        active_date = current_date[0]
        active_time = current_date[1].split('.')[0]
        body = {
                "voyageNumber": test_data['voyageNumber'],
                "startDate": f"{active_date}T{active_time}",
                "activityGroupCode": "PA",
                "statuses": [],
                "access": ["PRIVATE", "PUBLIC"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "activityEndDateGE": None,
                "activityName": "",
                "includeArrivalCount": True,
                "portCodes": ["BIM", "MIA", "CZM"]
        }
        params = {
            "page": 1,
            "size": 20
        }
        activity_slot = []
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'),"/activities/slots/search?sort=activityCode&sort=status")
        while True:
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            activity_slot.extend(_content["data"])
            if _content['page']['number'] >= _content['page']['totalPages']:
                break
            else:
                params['page'] += 1

        activity = activity_slot[len(activity_slot)-1]
        test_data['activityCode'] = activity['activityCode']
        test_data['activityName'] = activity['activityCode']
        test_data['activitySlotCode'] = activity['activitySlotCode']
        test_data['startDateTime'] = activity['startDateTime']
        test_data['endDateTime'] = activity['startDateTime']

        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings/conflicts")
        body = {"personDetails": [{"personId": guest_data[0]['reservationGuestId'],
                                  "reservationNumber": test_data['reservationNumber'],
                                  "personTypeCode": "G"}],
                "activityCode": test_data['activityCode'],
                "startDateTime": test_data['startDateTime'],
                "endDateTime": test_data['endDateTime'],
                "activityGroupCode": "PA",
                "isActivityPaid": True
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content

        body = {"activityCode": test_data['activityCode'],
                "activitySlotCode": test_data['activitySlotCode'],
                "activityGroupCode": "PA",
                "bookedByPersonId": guest_data[0]['guestId'],
                "bookedByPersonTypeCode": "C",
                "payeePersonId": guest_data[0]['reservationGuestId'],
                "payeePersonTypeCode": "G",
                "isGift": False,
                "isCheckedIn": False,
                "additionalNotes": "",
                "discountReasonId": "",
                "discountAmount": 0,
                "discountUnit": "PERCENT",
                "personDetails": [{"personId": guest_data[0]['reservationGuestId'],
                                  "personTypeCode": "G",
                                  "reservationNumber": test_data['reservationNumber'],
                                  "guestId": guest_data[0]['guestId']}],
                "reservationNumber": test_data['reservationNumber'],
                "voyageNumber": test_data['voyageNumber'],
                "shipCode": config.ship.code,
                "startDate": test_data['startDateTime'],
                "endDate": test_data['endDateTime']}
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/bookings")
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content


