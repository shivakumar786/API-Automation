__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.CHECKIN_ONBORD
@pytest.mark.SHIP
@pytest.mark.GANGWAY
@pytest.mark.run(order=13)
class TestGangway:
    """
    Test Suite to test Gangway
    """

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(138)
    def test_01_get_document_to_be_updated_first_pass(self, config, test_data, rest_ship, guest_data):
        """
        Get up 1st Layer of user data for modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['gangway'] = dict()
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
            test_data[_res_id] = _content

    @pytestrail.case(89)
    def test_02_update_document_first_pass(self, config, test_data, rest_ship, guest_data):
        """
        Put up 1st Layer of user data modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = test_data[_res_id]
            _rev = _data['_rev']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _data['IsOnBoarded'] = True
            _data['lastModifiedBy'] = "Script Automation"
            _data['OnBoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['BoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['OnBoardingStatusDateEpoch'] = test_data[_res_id]['EmbarkDateEpoch']
            _data['BoardingStatusDateEpoch'] = test_data[_res_id]['EmbarkDateEpoch']
            _data['lastModifiedDate'] = test_data[_res_id]['lastModifiedDate']
            _data['sourceId'] = 'CouchDatabase'
            _data['boardingStatusChangedBy'] = "SYSTEM"
            for i in range(0, 5):
                try:
                    revision = rest_ship.send_request(method="GET", url=url, auth="crew").content['_rev']
                    params = {"rev": revision}
                    _content = rest_ship.send_request(method="PUT", url=url, json=_data, params=params, auth="crew").content
                    assert _content['ok'], "Documents update Failed 1st Time !!"
                    test_data[_res_id] = _content
                    break
                except (Exception, ValueError):
                    pass
            else:
                raise Exception(f"Update Document 1st Pass Res-ID: {_res_id}, not updated via sync !!")

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(184)
    def test_03_get_document_to_be_updated_second_pass(self, config, test_data, rest_ship, guest_data):
        """
        Get 2nd Layer of user data for modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
            test_data[_res_id] = _content

    @pytestrail.case(183)
    def test_04_update_document_second_pass(self, config, test_data, rest_ship, guest_data):
        """
        Put up 2nd Layer of user data modification on Gangway
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = test_data[_res_id]
            _rev = _data['_rev']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _data['IsOnBoarded'] = True
            _data['lastModifiedBy'] = "Script Automation"
            _data['OnBoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['BoardingStatusDate'] = test_data['aci']['validationStatusDate']
            _data['OnBoardingStatusDateEpoch'] = test_data[_res_id]['OnBoardingStatusDateEpoch']
            _data['BoardingStatusDateEpoch'] = test_data[_res_id]['BoardingStatusDateEpoch']
            _data['lastModifiedDate'] = test_data[_res_id]['lastModifiedDate']
            _data['sourceId'] = 'CouchDatabase'
            _data['boardingStatusChangedBy'] = "SYSTEM"
            for i in range(0, 5):
                try:
                    revision = rest_ship.send_request(method="GET", url=url, auth="crew").content['_rev']
                    params = {"rev": revision}
                    _content = rest_ship.send_request(method="PUT", url=url, json=_data, params=params, auth="crew").content
                    assert _content['ok'], "Documents update Failed 2nd Time !!"
                    test_data[_res_id] = _content
                    break
                except (Exception, ValueError):
                    pass
            else:
                raise Exception(f"Update Document 1st Pass Res-ID: {_res_id}, not updated via sync !!")

    @pytestrail.case(8555793)
    def test_05_check_guest_status_in_db(self, db_core, guest_data, request):
        """
        Check Guests in Database
        :param db_core:
        :param guest_data:
        :param request:
        :return:
        """
        ok_status = ['COMPLETED', 'ONBOARD']
        for count, guest in enumerate(guest_data):
            res_id = guest['reservationGuestId']
            query = f"select * from personstatus where personid = '{res_id}'"
            rows = db_core.ship.run_and_fetch_data(query=query)
            nc = [x for x in rows if x['status'] not in ok_status and x['statustypecode'] not in ['OC', 'CC']]
            if request.config.getoption("--embark-date") is None:
                if len(nc) > 0:
                    pytest.xfail(reason=f"{res_id}: {nc[0]['statustypecode']} status in DB is {nc[0]['status']} !!")

    @pytestrail.case(8744382)
    def test_06_get_final_updated_document(self, config, test_data, rest_ship, guest_data):
        """
        Save the updated document (after changes being made by gangway)
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['guestStatusDocument'] = dict()
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
            test_data['guestStatusDocument'][_res_id] = _content
            assert test_data['guestStatusDocument'][_res_id]['TerminalCheckinStatus'] == 'COMPLETED', "Sailor is not " \
                                                                                                      "Checked IN "
            assert test_data['guestStatusDocument'][_res_id]['IsOnBoarded'], "Sailor is not Onboard"

    @pytestrail.case(24987998)
    def test_07_verify_gangway_location(self, test_data, config, rest_ship):
        """
        To verify the gangway location Document.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/GangwayLocations::{test_data['shipCode']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        if len(_content) == 0:
            raise Exception("Gangway location document is not created !!")
        else:
            is_key_there_in_dict('GangwayLocations', _content)
            test_data['gangway_locations'] = _content['GangwayLocations']

    @pytestrail.case(26741257)
    def test_08_create_person_event_doc(self, config, test_data, couch, guest_data):
        """
        Create a person event document in couch
        :param guest_data:
        :param test_data:
        :param config:
        :pram test_data:
        :param couch:
        """
        location = test_data['gangway_locations'][0]['GangWayLocation']
        gangway_location_id = test_data['gangway_locations'][0]['LocationID']
        current_date = str(datetime.now()).split(" ")[0]
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _event_id = generate_guid()
            body = {
                "_id": f"PersonEvent::{_res_id}::{_event_id}",
                "DebarkDateEpoch": change_epoch_time(test_data['debarkDate']) * 1000,
                "EmbarkDateEpoch": change_epoch_time(test_data['embarkDate']) * 1000,
                "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                "X-DEVICE-ID": "1f7c8d34357bbb0f",
                "channels": [
                    "PersonEvent",
                    config.ship.code,
                    f"{config.ship.code}_PersonEvent",
                    f"{config.ship.code}_emb_gw_t"
                ],
                "deviceName": "SM-G975F",
                "eventDateEpoch": int(round(time.time() * 1000)),
                "eventGenerationMethod": "MANUAL",
                "eventID": _event_id,
                "eventType": "ON_BOARD",
                "gangwayLocationId": gangway_location_id,
                "lastModifiedBy": "Script Automation",
                "lastModifiedDate": f"{datetime.now().strftime('%Y-%b-%dT%H:%M:00')}.751Z",
                "lastModifiedDateEpoch": int(round(time.time() * 1000)),
                "location": location,
                "personID": _res_id,
                "personType": "GUEST",
                "portCode": test_data['crew_framework']['portCode'],
                "portName": test_data['crew_framework']['portName'],
                "shipCode": config.ship.code,
                "sourceId": "CouchDatabase",
                "teamMemberID": test_data['personId'],
                "teamMemberName": "rosa.yang",
                "type": "PersonEvent",
                "voyageNumber": test_data['voyageId']
            }
            content = couch.send_request(method="POST", url=f"{config.ship.sync}/", json=body,
                                         auth="basic").content
            is_key_there_in_dict('ok', content)
            assert content['ok'], "Document not created !!!"
