__author__ = 'sarvesh.singh'

from virgin_utils import *


@pytest.mark.skip(reason="DCP-107830")
@pytest.mark.INTEGRATION
@pytest.mark.GANGWAY_GANGWAY_ADMIN
@pytest.mark.run(order=40)
class TestGangwayGangwayAdmin:
    """
    Test Suite to check integration between Gangway and Gangway Admin
    """

    @pytestrail.case(11777699)
    def test_01_verify_sailor_alert(self, config, test_data, couch, guest_data, rest_ship):
        """
        Create a alert document in couch
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        current_date = str(datetime.now()).split(" ")[0]
        test_data['gangwayIntegration'] = dict()
        number = four_digit_random_number()
        test_data['gangwayIntegration']['doc'] = False
        test_data['gangwayIntegration']['sailorPersonAlertID'] = f"5ef51ce1-{number}-493b-8a8a-ec022e279aca"
        for count, guest in enumerate(guest_data):
            is_key_there_in_dict('reservationGuestId', guest)
            _res_id = guest['reservationGuestId']
            test_data['gangwayIntegration']['_res_aid'] = _res_id
            try:
                url = urljoin(config.ship.sync, f"GuestPersonAlert::{_res_id}")
                _content = couch.send_request(method="GET", url=url, auth="basic").content
                test_data['gangwayIntegration']['doc'] = True
                break
            except (Exception, ValueError):
                pytest.skip(msg=f"failed to get couch document for res_guest_id {guest['reservationGuestId']}")
            body = {
                "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                "PersonAlerts": [
                    {
                        "AddedBy": "53952924-fad5-4a02-813b-150900b8c981",
                        "AddedDate": f"{test_data['aci']['validationStatusDate']}.751Z",
                        "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                        "AlertCode": "IN", "AlertID": "11b53343-bdba-4581-a826-f299be4a460b", "AlertPriority": 0,
                        "AlertSeverity": 0, "AlertTypeName": "Info", "Description": "Script Automation - Integration",
                        "DueDate": f"{test_data['aci']['validationStatusDate']}.000Z",
                        "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                        "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00.000Z",
                        "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000, "IsCleared": False,
                        "IsDeleted": False, "IsOverridable": True, "IsRead": False, "IsSoundEnabled": True,
                        "LastModifiedDate": f"{test_data['aci']['validationStatusDate']}.751Z",
                        "LastModifiedDateEpoch": int(round(time.time() * 1000)),
                        "PersonAlertID": test_data['gangwayIntegration']['sailorPersonAlertID'], "PersonTypeCode": "RG",
                        "PropertyID": config.ship.code, "Source": "ACI", "FromPersonFirstName": "vertical-qa",
                        "TeammemberDepartmentID": "bfa3b2b5-ded0-4c13-b8ff-702ed56ca338"
                    }
                ],
                "ReservationGuestID": _res_id,
                "_id": f"GuestPersonAlert::{_res_id}",
                "channels": [
                    config.ship.code, "GuestPersonAlert", f"{config.ship.code}_emb_gw_t",
                    f"{config.ship.code}_emb_aci_t", f"{config.ship.code}_GuestPersonAlert"
                ],
                "lastModifiedBy": "Script Automation",
                "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.773602+00:00",
                "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
                "type": "GuestPersonAlert",
            }
            if 'rev' in test_data['gangway']:
                body['_rev'] = test_data['gangway']['rev']
            url = urljoin(config.ship.sync, f'GuestPersonAlert::{_res_id}')
            content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
            is_key_there_in_dict('ok', content)
            assert content['ok'], "Document not created !!!"
            test_data['gangway']['rev'] = content['rev']
            del test_data['gangway']['rev']
            retries = 60
            while retries >= 0:
                url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                              f"/crew-embarkation-admin/reservation-guests/{_res_id}")
                params = {
                    'shipCode': config.ship.code
                }
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                if len(_content['alerts']) > 0:
                    if not any(d['alertId'] == test_data['gangwayIntegration']['sailorPersonAlertID'] and d[
                        'description'] == 'Script Automation - Integration' for d in _content['alerts']):
                        if retries > 0:
                            retries -= 1
                            logger.debug(
                                'Alert created from couch for Sailor is not shown in Embarkation Supervisor ')
                        else:
                            raise Exception('Alert created from couch for Sailor is not shown in Embarkation '
                                            'Supervisor !!')
                    else:
                        break
                else:
                    if retries > 0:
                        retries -= 1
                        logger.debug('Alert created from couch for Sailor is not shown in Embarkation Supervisor ')
                    else:
                        raise Exception('Alert created from couch for Sailor is not shown in Embarkation Supervisor !!')

    @pytestrail.case(11777700)
    def test_02_update_sailor_alert(self, config, test_data, couch, rest_ship):
        """
        Edit alert document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['doc']:
            pytest.skip(msg="failed create alert for sailor in couch")
        _res_id = test_data['gangwayIntegration']['_res_aid']
        url = urljoin(config.ship.sync, f"GuestPersonAlert::{_res_id}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['PersonAlerts'][0]['Description'] = "new sailor alert"
        url = urljoin(config.ship.sync, f'GuestPersonAlert::{_res_id}')
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/reservation-guests/{_res_id}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['alerts']) > 0:
                if not any(d['alertId'] == test_data['gangwayIntegration']['sailorPersonAlertID'] and d[
                    'description'] == 'new sailor alert' for d in _content['alerts']):
                    if retries > 0:
                        retries -= 1
                        logger.debug(
                            'Alert updated from couch for Sailor is not shown in Embarkation Supervisor ')
                    else:
                        raise Exception('Alert updated from couch for Sailor is not shown in Embarkation Supervisor !!')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Alert updated from couch for Sailor is not shown in Embarkation Supervisor ')
                else:
                    raise Exception('Alert updated from couch for Sailor is not shown in Embarkation Supervisor !!')

    @pytestrail.case(29874178)
    def test_03_verify_sailor_message(self, config, test_data, couch, guest_data, rest_ship):
        """
        Create a message document in couch
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        current_date = str(datetime.now()).split(" ")[0]
        number = four_digit_random_number()
        test_data['gangwayIntegration']['sailor_msg'] = False
        test_data['gangwayIntegration']['messageId'] = f"7ccde1c4-7057-{number}-ba04-33c94db07a1f"
        for count, guest in enumerate(guest_data):
            is_key_there_in_dict('reservationGuestId', guest)
            _res_id = guest['reservationGuestId']
            test_data['gangwayIntegration']['res_id'] = _res_id
            try:
                url = urljoin(config.ship.sync, f"GuestMessage::{_res_id}")
                _content = couch.send_request(method="GET", url=url, auth="basic").content
                _content = couch.send_request(method="GET", url=url, auth="basic").content
                test_data['gangway']['rev'] = _content['_rev']
                break
            except (Exception, ValueError):
                pass
            body = {
                "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                "Messages": [
                    {
                        "AddedDate": f"{test_data['aci']['validationStatusDate']}.773602+00:00",
                        "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                        "DueDate": f"{test_data['aci']['validationStatusDate']}",
                        "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                        "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00",
                        "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                        "FromPersonFirstName": "vertical-qa", "IsCleared": False, "IsDeleted": False,
                        "IsOverridable": False, "IsRead": False, "IsSoundEnabled": True,
                        "MessageBody": "Script Automation - Integration",
                        "MessageID": test_data['gangwayIntegration']['messageId'],
                        "MessagePriority": 0, "MessageSeverity": 0,
                        "PropertyID": config.ship.code, "Source": "Couchbase", "sourceId": "core_ship"
                    }
                ],
                "ReservationGuestID": _res_id,
                "_id": f"GuestMessage::{_res_id}",
                "channels": [
                    config.ship.code, "GuestMessage", f"{config.ship.code}_emb_gw_t", f"{config.ship.code}_GuestMessage"
                ],
                "lastModifiedBy": "Script Automation",
                "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.773602+00:00",
                "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
                "type": "GuestMessage",
            }
            if 'rev' in test_data['gangway']:
                body['_rev'] = test_data['gangway']['rev']
            url = urljoin(config.ship.sync, f'GuestMessage::{_res_id}')
            content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
            is_key_there_in_dict('ok', content)
            test_data['gangwayIntegration']['sailor_msg'] = True
            assert content['ok'], "Document not created !!!"
            is_key_there_in_dict('rev', content)
            test_data['gangway']['rev'] = content['rev']
            del test_data['gangway']['rev']
            retries = 60
            while retries >= 0:
                url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                              f"/crew-embarkation-admin/reservation-guests/{_res_id}")
                params = {
                    'shipCode': config.ship.code
                }
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                if len(_content['messages']) > 0:
                    if not any(d['messageId'] == test_data['gangwayIntegration']['messageId'] and d['description'] ==
                               'Script Automation - Integration' for d in _content['messages']):
                        if retries > 0:
                            retries -= 1
                            logger.debug(
                                'Message created from couch for Sailor is not shown in Embarkation Supervisor !')
                        else:
                            raise Exception(
                                'Message created from couch for Sailor is not shown in Embarkation Supervisor')
                    else:
                        break
                else:
                    if retries > 0:
                        retries -= 1
                        logger.debug(
                            'Message created from couch for Sailor is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception('Message created from couch for Sailor is not shown in Embarkation Supervisor')
                break

    @pytestrail.case(31042591)
    def test_04_update_sailor_message(self, config, test_data, couch, rest_ship):
        """
        Update sailor message document in couch
        :param config:
        :param test_data:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['sailor_msg']:
            pytest.skip(msg="message not created to update")
        _res_id = test_data['gangwayIntegration']['res_id']
        url = urljoin(config.ship.sync, f"GuestMessage::{_res_id}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['Messages'][0]['MessageBody'] = "new script automation"
        url = urljoin(config.ship.sync, f'GuestMessage::{_res_id}')
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/reservation-guests/{_res_id}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['messages']) > 0:
                if not any(d['messageId'] == test_data['gangwayIntegration']['messageId'] and d['description'] ==
                           "new script automation" for d in _content['messages']):
                    if retries > 0:
                        retries -= 1
                        logger.debug(
                            'Message updated from couch for Sailor is not shown in Embarkation Supervisor !')
                    else:
                        raise Exception('Message updated from couch for Sailor is not shown in Embarkation Supervisor')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug(
                        'Message updated from couch for Sailor is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception('Message updated from couch for Sailor is not shown in Embarkation Supervisor')

    @pytestrail.case(29919033)
    def test_05_crew_landing(self, config, test_data, rest_ship):
        """
        To verify the landing call for Crew
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/team-members/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": config.ship.code,
            "fromDate": f"{test_data['aci']['shipDate']}T00:00:01",
            "toDate": f"{test_data['aci']['shipDate']}T23:59:59",
            "shipTime": f"{test_data['aci']['shipDate']}T00:00:01"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        random.shuffle(_content['teamMembers'])
        for _crew in _content['teamMembers']:
            test_data['gangway']['teamMemberId'] = _crew['teamMemberId']
            break
        else:
            raise Exception("No crew available for testing integration !!")

    @pytestrail.case(11777702)
    def test_06_verify_crew_alert(self, config, test_data, couch, rest_ship):
        """
        Create a alert document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        current_date = str(datetime.now()).split(" ")[0]
        number = four_digit_random_number()
        test_data['gangwayIntegration']['crew_alert'] = False
        test_data['gangwayIntegration']['PersonAlertID'] = f"ba38880b-{number}-4fb5-af23-37b4337ed580"
        url = urljoin(config.ship.sync, f"TeamMemberPersonAlert::{test_data['gangway']['teamMemberId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('_rev', _content)
        test_data['gangway']['rev'] = _content['_rev']
        body = {
            "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
            "PersonAlerts": [
                {
                    "AddedBy": "53952924-fad5-4a02-813b-150900b8c981",
                    "AddedDate": f"{test_data['aci']['validationStatusDate']}.309637+00:00",
                    "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "AlertCode": "CBP", "AlertCreatedBy": "995855bc-02fc-476d-9a20-c924303cb0b6",
                    "AlertID": "58a2b9bc-e21c-49cf-a1f1-b1ef1e6dd01d", "AlertPriority": 1, "AlertSeverity": 0,
                    "AlertTypeName": "CBP Hold", "AlertTypeSeverity": 0,
                    "CreatedBy": "995855bc-02fc-476d-9a20-c924303cb0b6",
                    "Description": "Script Automation - Integration",
                    "DueDate": f"{test_data['aci']['shipDate']}T00:00:01",
                    "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00",
                    "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000, "IsCleared": False,
                    "IsDeleted": False, "IsOverridable": True, "IsRead": False, "IsSoundEnabled": True,
                    "LastModifiedDate": f"{test_data['aci']['validationStatusDate']}.313826+00:00",
                    "LastModifiedDateEpoch": int(round(time.time() * 1000)),
                    "PersonAlertID": test_data['gangwayIntegration']['PersonAlertID'], "PersonTypeCode": "C",
                    "PropertyID": config.ship.code, "Source": "GANGWAY-ADMIN", "sourceId": "core_ship"
                }
            ],
            "TeamMemberID": test_data['gangway']['teamMemberId'],
            "_id": f"TeamMemberPersonAlert::{test_data['gangway']['teamMemberId']}",
            "channels": [
                config.ship.code, "TeamMemberPersonAlert", f"{config.ship.code}_emb_gw_t",
                f"{config.ship.code}_TeamMemberPersonAlert"
            ],
            "lastModifiedBy": "Script Automation",
            "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.313826+00:00",
            "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
            "type": "TeamMemberPersonAlert",
        }
        if 'rev' in test_data['gangway']:
            body['_rev'] = test_data['gangway']['rev']
        url = urljoin(config.ship.sync,
                      f"TeamMemberPersonAlert::{test_data['gangway']['teamMemberId']}")
        content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
        is_key_there_in_dict('ok', content)
        test_data['gangwayIntegration']['crew_alert'] = True
        assert content['ok'], "Document not created !!!"
        is_key_there_in_dict('rev', content)
        test_data['gangway']['rev'] = content['rev']
        del test_data['gangway']['rev']
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['alerts']) > 0:
                if not any(d['alertId'] == test_data['gangwayIntegration']['PersonAlertID'] and d[
                    'description'] == 'Script Automation - Integration' for d in _content['alerts']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Alert created from couch for Crew is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception('Alert created from couch for Crew does not sync to Embarkation Supervisor')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Alert created from couch for Crew is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception('Alert created from couch for Crew does not sync to Embarkation Supervisor')

    @pytestrail.case(11777703)
    def test_07_update_crew_alert(self, config, test_data, couch, rest_ship):
        """
        update alert document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['crew_alert']:
            pytest.skip(msg="crew alert not created to update")
        url = urljoin(config.ship.sync, f"TeamMemberPersonAlert::{test_data['gangway']['teamMemberId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['PersonAlerts'][0]['Description'] = 'new script automation crew'
        url = urljoin(config.ship.sync, f"TeamMemberPersonAlert::{test_data['gangway']['teamMemberId']}")
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        is_key_there_in_dict('rev', content)
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['alerts']) > 0:
                if not any(d['alertId'] == test_data['gangwayIntegration']['PersonAlertID'] and d[
                    'description'] == 'new script automation crew' for d in _content['alerts']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Alert updated from couch for Crew is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception('Alert updated from couch for Crew does not sync to Embarkation Supervisor')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Alert updated from couch for Crew is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception('Alert updated from couch for Crew does not sync to Embarkation Supervisor')

    @pytestrail.case(29925096)
    def test_08_verify_crew_message(self, config, test_data, couch, rest_ship):
        """
        Create a message document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        current_date = str(datetime.now()).split(" ")[0]
        number = four_digit_random_number()
        test_data['gangwayIntegration']['crew_msg'] = False
        test_data['gangwayIntegration']['crewMessageID'] = f"2f4e2505-cc39-{number}-b7fa-0165938916b0"
        try:
            url = urljoin(config.ship.sync, f"TeamMemberMessage::{test_data['gangway']['teamMemberId']}")
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            test_data['gangway']['rev'] = _content['_rev']
        except (Exception, ValueError):
            pass
        body = {
            "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
            "Messages": [
                {
                    "AddedDate": f"{test_data['aci']['validationStatusDate']}.797289+00:00",
                    "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "AlertCreatedBy": "995855bc-02fc-476d-9a20-c924303cb0b6",
                    "CreatedBy": "995855bc-02fc-476d-9a20-c924303cb0b6",
                    "DueDate": f"{test_data['aci']['shipDate']}T00:00:01",
                    "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00",
                    "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                    "IsCleared": False, "IsDeleted": False, "IsOverridable": False, "IsRead": False,
                    "IsSoundEnabled": False, "MessageBody": "Script Automation - Integration",
                    "MessageID": test_data['gangwayIntegration']['crewMessageID'], "MessagePriority": 0,
                    "MessageSeverity": 0,
                    "PropertyID": config.ship.code, "Source": "Couchbase", "sourceId": "core_ship"
                }
            ],
            "TeamMemberID": test_data['gangway']['teamMemberId'],
            "_id": f"TeamMemberMessage::{test_data['gangway']['teamMemberId']}",
            "channels": [
                config.ship.code, "TeamMemberMessage", f"{config.ship.code}_emb_gw_t",
                f"{config.ship.code}_TeamMemberMessage"
            ],
            "lastModifiedBy": "Script Automation",
            "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.801074+00:00",
            "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
            "type": "TeamMemberMessage",
        }
        if 'rev' in test_data['gangway']:
            body['_rev'] = test_data['gangway']['rev']
        url = urljoin(config.ship.sync, f"TeamMemberMessage::{test_data['gangway']['teamMemberId']}")
        content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
        is_key_there_in_dict('ok', content)
        test_data['gangwayIntegration']['crew_msg'] = True
        assert content['ok'], "Document not created !!!"
        is_key_there_in_dict('rev', content)
        test_data['gangway']['rev'] = content['rev']
        del test_data['gangway']['rev']
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['messages']) > 0:
                if not any(d['messageId'] == test_data['gangwayIntegration']['crewMessageID'] and d[
                    'description'] == 'Script Automation - Integration' for d in _content['messages']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Message created from couch for Crew is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception("Alert created from couch for Crew is not shown in Embarkation Supervisor !!")
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Message created from couch for Crew is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception("Alert created from couch for Crew is not shown in Embarkation Supervisor !!")

    @pytestrail.case(31042593)
    def test_09_update_crew_message(self, config, test_data, couch, rest_ship):
        """
        update message document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['crew_msg']:
            pytest.skip(msg="crew message not created to edit")
        url = urljoin(config.ship.sync, f"TeamMemberMessage::{test_data['gangway']['teamMemberId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['Messages'][0]['MessageBody'] = "new message crew"
        url = urljoin(config.ship.sync, f"TeamMemberMessage::{test_data['gangway']['teamMemberId']}")
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['messages']) > 0:
                if not any(d['messageId'] == test_data['gangwayIntegration']['crewMessageID'] and
                           d['description'] == "new message crew" for d in _content['messages']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Message updated from couch for Crew is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception("Alert updated from couch for Crew is not shown in Embarkation Supervisor !!")
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Message updated from couch for Crew is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception("Alert updated from couch for Crew is not shown in Embarkation Supervisor !!")

    @pytestrail.case(30107087)
    def test_10_visitor_landing(self, config, test_data, rest_ship):
        """
        To verify the landing call for visitor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'gangway/visitors/search')
        params = {
            'page': '1'
        }
        body = {
            "shipCode": config.ship.code,
            "startDate": f"{test_data['aci']['shipDate']}T00:00:01",
            "endDate": f"{test_data['aci']['shipDate']}T23:59:59",
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        random.shuffle(_content['_embedded']['visitors'])
        for _visitor in _content['_embedded']['visitors']:
            test_data['gangway']['visitorId'] = _visitor['visitorId']
            break
        else:
            raise Exception("No Visitor available for testing integration !!")

    @pytestrail.case(11777706)
    def test_11_verify_visitor_alert(self, config, test_data, couch, rest_ship):
        """
        Create a alert document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        current_date = str(datetime.now()).split(" ")[0]
        number = four_digit_random_number()
        test_data['gangwayIntegration']['visitor_alert'] = False
        test_data['gangwayIntegration']['v_PersonAlertID'] = f"08d13c5b-0720-{number}-8274-c4406efbd116"
        url = urljoin(config.ship.sync,
                      f"VisitorPersonAlert::{test_data['gangway']['visitorId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        body = {
            "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
            "PersonAlerts": [
                {
                    "AddedBy": "Couchbase",
                    "AddedDate": f"{test_data['aci']['shipDate']}.49681+00:00",
                    "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "AlertCode": "IN", "AlertID": "1f9d9da0-1ee3-4ac9-a975-f5ce0ccf413e", "AlertPriority": 0,
                    "AlertSeverity": 0, "AlertTypeName": "Info", "AlertTypeSeverity": 0,
                    "Description": "Script Automation - Integration",
                    "DueDate": f"{test_data['aci']['shipDate']}T00:00:01",
                    "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00",
                    "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                    "IsCleared": False, "IsDeleted": False, "IsOverridable": True,
                    "IsRead": False, "IsSoundEnabled": True,
                    "LastModifiedDate": f"{test_data['aci']['validationStatusDate']}.965Z",
                    "LastModifiedDateEpoch": int(round(time.time() * 1000)),
                    "PersonAlertID": test_data['gangwayIntegration']['v_PersonAlertID'], "PersonTypeCode": "V",
                    "PropertyID": config.ship.code, "Source": "ACI", "TeammemberDepartmentCode": "INFO_SYSTEMS",
                    "TeammemberDepartmentID": "50b55b3e-5407-4d39-b4bc-18e75c5fb9d7",
                    "TeammemberDepartmentName": "Info Systems", "sourceId": "core_ship"
                }
            ],
            "VisitorID": test_data['gangway']['visitorId'],
            "_id": f"VisitorPersonAlert::{test_data['gangway']['visitorId']}",
            "channels": [
                config.ship.code, "VisitorPersonAlert", f"{config.ship.code}_emb_gw_t",
                f"{config.ship.code}_VisitorPersonAlert"
            ],
            "lastModifiedBy": "Script Automation",
            "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.503346+00:00",
            "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
            "type": "VisitorPersonAlert"
        }
        url = urljoin(config.ship.sync,
                      f"VisitorPersonAlert::{test_data['gangway']['visitorId']}")
        content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
        is_key_there_in_dict('ok', content)
        test_data['gangwayIntegration']['visitor_alert'] = True
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
            params = {
                'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['alerts']) > 0:
                if not any(d['alertId'] == test_data['gangwayIntegration']['v_PersonAlertID'] and d[
                    'description'] == 'Script Automation - Integration' for d in _content['alerts']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Alert created from couch for Visitor is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception('Alert created from couch for Visitor does not sync to Embarkation '
                                        'Supervisor !!')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Alert created from couch for Visitor is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception('Alert created from couch for Visitor does not sync to Embarkation '
                                    'Supervisor !!')

    @pytestrail.case(11777707)
    def test_12_update_visitor_alert(self, config, test_data, couch, rest_ship):
        """
        update alert document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['visitor_alert']:
            pytest.skip(msg="visitor alert not create to update")
        url = urljoin(config.ship.sync, f"VisitorPersonAlert::{test_data['gangway']['visitorId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['PersonAlerts'][0]['Description'] = "new visitor alert"
        url = urljoin(config.ship.sync,
                      f"VisitorPersonAlert::{test_data['gangway']['visitorId']}")
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
            params = {
                'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['alerts']) > 0:
                if not any(d['alertId'] == test_data['gangwayIntegration']['v_PersonAlertID'] and d[
                    'description'] == 'new visitor alert' for d in _content['alerts']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Alert updated from couch for Visitor is not shown in Embarkation Supervisor !!')
                    else:
                        raise Exception('Alert updated from couch for Visitor does not sync to Embarkation '
                                        'Supervisor !!')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Alert updated from couch for Visitor is not shown in Embarkation Supervisor !!')
                else:
                    raise Exception('Alert updated from couch for Visitor does not sync to Embarkation '
                                    'Supervisor !!')

    @pytestrail.case(30107700)
    def test_13_verify_visitor_message(self, config, test_data, couch, rest_ship):
        """
        Create a message document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        test_data['gangwayIntegration']['visitor_msg'] = False
        current_date = str(datetime.now()).split(" ")[0]
        try:
            url = urljoin(config.ship.sync, f"VisitorMessage::{test_data['gangway']['visitorId']}")
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            test_data['gangway']['rev'] = _content['_rev']
        except (Exception, ValueError):
            pass
        body = {
            "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
            "Messages": [
                {
                    "AddedDate": f"{test_data['aci']['validationStatusDate']}.797289+00:00",
                    "AddedDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "DueDate": f"{test_data['aci']['shipDate']}T00:00:01",
                    "DueDateEpoch": test_data['aci']['boardingStatusDateEpoch'],
                    "ExpiryDate": f"{test_data['aci']['shipDate']}T23:59:00",
                    "ExpiryDateEpoch": change_epoch_time(next_year_date(current_date)) * 1000,
                    "FromPersonFirstName": "vertical-qa",
                    "IsCleared": False, "IsDeleted": False, "IsOverridable": False, "IsRead": False,
                    "IsSoundEnabled": True, "MessageBody": "Script Automation - Integration",
                    "MessageID": "f3d9fa56-8a0a-4491-8be7-2b07c793b969", "MessagePriority": 0,
                    "MessageSeverity": 0, "PropertyID": config.ship.code, "Source": "Couchbase", "sourceId": "core_ship"
                }
            ],
            "VisitorID": test_data['gangway']['visitorId'],
            "_id": f"VisitorMessage::{test_data['gangway']['visitorId']}",
            "channels": [
                config.ship.code, "VisitorMessage", f"{config.ship.code}_emb_gw_t",
                f"{config.ship.code}_VisitorMessage"
            ],
            "lastModifiedBy": "Script Automation",
            "lastModifiedDate": f"{test_data['aci']['validationStatusDate']}.801074+00:00",
            "lastModifiedDateEpoch": int(round(time.time() * 1000)), "sourceId": "CouchDatabase",
            "type": "VisitorMessage",
        }
        if 'rev' in test_data['gangway']:
            body['_rev'] = test_data['gangway']['rev']
        url = urljoin(config.ship.sync, f"VisitorMessage::{test_data['gangway']['visitorId']}")
        content = couch.send_request(method="PUT", url=url, json=body, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        is_key_there_in_dict('rev', content)
        test_data['gangwayIntegration']['visitor_msg'] = True
        test_data['gangway']['rev'] = content['rev']
        del test_data['gangway']['rev']

        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
            params = {
                'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['messages']) > 0:
                if not any(d['messageId'] == "f3d9fa56-8a0a-4491-8be7-2b07c793b969" and d[
                    'description'] == 'Script Automation - Integration' for d in _content['messages']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Message created from couch for Visitor is not shown in Embarkation Supervisor!')
                    else:
                        raise Exception('Message created from couch for Visitor is not shown in Embarkation '
                                        'Supervisor !!')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Message created from couch for Visitor is not shown in Embarkation Supervisor!')
                else:
                    raise Exception('Message created from couch for Visitor is not shown in Embarkation '
                                    'Supervisor !!')

    @pytestrail.case(31046033)
    def test_14_update_visitor_message(self, config, test_data, couch, rest_ship):
        """
        update message document in couch
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['visitor_msg']:
            pytest.skip(msg="visitor message not created to update")
        url = urljoin(config.ship.sync, f"VisitorMessage::{test_data['gangway']['visitorId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content['Messages'][0]['MessageBody'] = "new visitor message"
        url = urljoin(config.ship.sync, f"VisitorMessage::{test_data['gangway']['visitorId']}")
        content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        is_key_there_in_dict('ok', content)
        assert content['ok'], "Document not created !!!"
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
            params = {
                'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if len(_content['messages']) > 0:
                if not any(d['messageId'] == "f3d9fa56-8a0a-4491-8be7-2b07c793b969" and
                           d['description'] == "new visitor message" for d in _content['messages']):
                    if retries > 0:
                        retries -= 1
                        logger.debug('Message updated from couch for Visitor is not shown in Embarkation Supervisor!')
                    else:
                        raise Exception('Message updated from couch for Visitor is not shown in Embarkation '
                                        'Supervisor !!')
                else:
                    break
            else:
                if retries > 0:
                    retries -= 1
                    logger.debug('Message updated from couch for Visitor is not shown in Embarkation Supervisor!')
                else:
                    raise Exception('Message updated from couch for Visitor is not shown in Embarkation '
                                    'Supervisor !!')

    @pytestrail.case(11777698)
    def test_15_verify_sailor_image(self, config, test_data, couch, guest_data, rest_ship):
        """
        Verify Clicked image for sailor gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        test_data['gangwayIntegration']['sailor_image'] = True
        for count, guest in enumerate(guest_data):
            is_key_there_in_dict('FirstName', guest)
            test_data['gangwayIntegration']['count'] = count
            first_name = guest['FirstName']
            test_data['gangwayIntegration']['first_name'] = first_name
            is_key_there_in_dict('LastName', guest)
            last_name = guest['LastName']
            test_data['gangwayIntegration']['last_name'] = last_name
            is_key_there_in_dict('email', guest)
            email_id = guest['email']
            test_data['gangwayIntegration']['email'] = email_id
            is_key_there_in_dict('birthDate', guest)
            birth_date = guest['birthDate']
            test_data['gangwayIntegration']['birthdate'] = birth_date
            if len(guest) > 0:
                gender = guest['GenderCode'][0]
            else:
                gender = guest['GenderCode']
            test_data['gangwayIntegration']['gender'] = gender
            _res_id = guest['reservationGuestId']
            test_data['gangwayIntegration']['sailor_image_resid'] = _res_id
            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()
            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
            params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
            files = {"file": open(profile_photo, "rb")}
            content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
                "Location"]
            time.sleep(0.1)
            guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
            url = urljoin(config.ship.sync, f"GuestPersonalInformation::{_res_id}")
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            test_data['gangway']['rev'] = _content['_rev']
            _content['GuestSecurityMediaItemID'] = guest_data[count]['ProfilePhotoUrl']
            _content["lastModifiedBy"] = "Script Automation"
            _content["sourceId"] = "CouchDatabase"
            _content['_rev'] = test_data['gangway']['rev']
            url = urljoin(config.ship.sync, f"GuestPersonalInformation::{_res_id}")
            _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
            retries = 60
            while retries >= 0:
                url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                              f"/crew-embarkation-admin/reservation-guests/{_res_id}")
                params = {
                    'shipCode': config.ship.code
                }
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                try:
                    is_key_there_in_dict('profilePicture', _content)
                    if guest_data[count]['ProfilePhotoUrl'] not in _content['profilePicture']:
                        if retries > 0:
                            retries -= 1
                            logger.debug('Security photo for Sailor is not synced from couch to Gangway Admin !!')
                        else:
                            test_data['gangwayIntegration']['sailor_image'] = False
                            raise Exception(
                                "created Security photo for Sailor is not synced from couch to Gangway Admin !!")
                    else:
                        break
                except (Exception, ValueError):
                    if retries > 0:
                        retries -= 1
                        logger.debug('created Security photo for Sailor is not synced from couch to Gangway Admin !!')
                    else:
                        test_data['gangwayIntegration']['sailor_image'] = False
                        raise Exception(
                            "created Security photo for Sailor is not synced from couch to Gangway Admin !!")
            break

    @pytestrail.case(31042592)
    def test_16_update_sailor_image(self, config, test_data, couch, guest_data, rest_ship):

        """
        updated image for sailor gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['sailor_image']:
            pytest.skip("image not created or updated to edit")
        first_name = test_data['gangwayIntegration']['first_name']
        last_name = test_data['gangwayIntegration']['last_name']
        email_id = test_data['gangwayIntegration']['email']
        birth_date = test_data['gangwayIntegration']['birthdate']
        count = test_data['gangwayIntegration']['count']
        gender = test_data['gangwayIntegration']['gender']
        _res_id = test_data['gangwayIntegration']['sailor_image_resid']
        profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                      birth_date=birth_date, gender=gender).add_text()
        logger.debug(f"Uploading Profile Photo #{count + 1} ...")
        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
        params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
        files = {"file": open(profile_photo, "rb")}
        content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
            "Location"]
        time.sleep(0.1)
        guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
        url = urljoin(config.ship.sync, f"GuestPersonalInformation::{_res_id}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        test_data['gangway']['rev'] = _content['_rev']
        _content['GuestSecurityMediaItemID'] = guest_data[count]['ProfilePhotoUrl']
        _content["lastModifiedBy"] = "Script Automation"
        _content["sourceId"] = "CouchDatabase"
        _content['_rev'] = test_data['gangway']['rev']
        url = urljoin(config.ship.sync, f"GuestPersonalInformation::{_res_id}")
        _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/reservation-guests/{_res_id}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            try:
                is_key_there_in_dict('profilePicture', _content)
                if guest_data[count]['ProfilePhotoUrl'] not in _content['profilePicture']:
                    if retries > 0:
                        retries -= 1
                        logger.debug('Security photo for Sailor is not synced from couch to Gangway Admin !!')
                    else:
                        test_data['gangwayIntegration']['sailor_image'] = False
                        raise Exception("Security photo for Sailor is not synced from couch to Gangway Admin !!")
                else:
                    break
            except (Exception, ValueError):
                if retries > 0:
                    retries -= 1
                    logger.debug('updated Security photo for Sailor is not synced from couch to Gangway Admin !!')
                else:
                    test_data['gangwayIntegration']['sailor_image'] = False
                    raise Exception("updated Security photo for Sailor is not synced from couch to Gangway Admin !!")

    @pytestrail.case(11777701)
    def test_17_verify_crew_image(self, config, test_data, couch, guest_data, rest_ship):
        """
        Verify Clicked image for crew gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        test_data['gangwayIntegration']['crew_image'] = True
        for count, guest in enumerate(guest_data):
            test_data['gangwayIntegration']['crew_count'] = count
            is_key_there_in_dict('FirstName', guest)
            first_name = guest['FirstName']
            test_data['gangwayIntegration']['crew_first_name'] = first_name
            is_key_there_in_dict('LastName', guest)
            last_name = guest['LastName']
            test_data['gangwayIntegration']['crew_last_name'] = last_name
            is_key_there_in_dict('email', guest)
            email_id = guest['email']
            test_data['gangwayIntegration']['crew_email'] = email_id
            is_key_there_in_dict('birthDate', guest)
            birth_date = guest['birthDate']
            test_data['gangwayIntegration']['crew_birthdate'] = birth_date
            if len(guest) > 0:
                gender = guest['GenderCode'][0]
            else:
                gender = guest['GenderCode']
            test_data['gangwayIntegration']['crew_gender'] = gender
            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()
            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
            params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
            files = {"file": open(profile_photo, "rb")}
            content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
                "Location"]
            time.sleep(0.1)
            guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
            url = urljoin(config.ship.sync, f"TeamMember::{test_data['gangway']['teamMemberId']}")
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            is_key_there_in_dict('_rev', _content)
            test_data['gangway']['rev'] = _content['_rev']
            _content['PhotoMediaItemID'] = guest_data[count]['ProfilePhotoUrl']
            _content['_rev'] = test_data['gangway']['rev']
            _content["lastModifiedBy"] = "Script Automation"
            _content["sourceId"] = "CouchDatabase"
            url = urljoin(config.ship.sync, f"TeamMember::{test_data['gangway']['teamMemberId']}")
            _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
            retries = 60
            while retries >= 0:
                url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                              f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
                params = {
                    'shipCode': config.ship.code
                }
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                try:
                    is_key_there_in_dict('profilePicture', _content)
                    if guest['ProfilePhotoUrl'] not in _content['profilePicture']:
                        if retries > 0:
                            retries -= 1
                            logger.debug('created Security photo for Crew is not synced from couch to Gangway Admin !!')
                        else:
                            test_data['gangwayIntegration']['crew_image'] = False
                            raise Exception("created Security photo for Crew is not synced from couch to Gangway "
                                            "Admin !!")
                    else:
                        break
                except (Exception, ValueError):
                    if retries > 0:
                        retries -= 1
                        logger.debug('created Security photo for Crew is not synced from couch to Gangway Admin !!')
                    else:
                        test_data['gangwayIntegration']['crew_image'] = False
                        raise Exception("created Security photo for Crew is not synced from couch to Gangway "
                                        "Admin !!")
            break

    @pytestrail.case(31045363)
    def test_18_update_crew_image(self, config, test_data, couch, guest_data, rest_ship):
        """
        updated image for crew gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['crew_image']:
            pytest.skip("image not created or updated to edit")
        first_name = test_data['gangwayIntegration']['crew_first_name']
        last_name = test_data['gangwayIntegration']['crew_last_name']
        email_id = test_data['gangwayIntegration']['crew_email']
        birth_date = test_data['gangwayIntegration']['crew_birthdate']
        gender = test_data['gangwayIntegration']['crew_gender']
        count = test_data['gangwayIntegration']['crew_count']
        profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                      birth_date=birth_date, gender=gender).add_text()
        logger.debug(f"Uploading Profile Photo #{test_data['gangwayIntegration']['crew_count'] + 1} ...")
        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
        params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
        files = {"file": open(profile_photo, "rb")}
        content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
            "Location"]
        time.sleep(0.1)
        guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
        url = urljoin(config.ship.sync, f"TeamMember::{test_data['gangway']['teamMemberId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('_rev', _content)
        test_data['gangway']['rev'] = _content['_rev']
        _content['PhotoMediaItemID'] = guest_data[count]['ProfilePhotoUrl']
        _content['_rev'] = test_data['gangway']['rev']
        _content["lastModifiedBy"] = "Script Automation"
        _content["sourceId"] = "CouchDatabase"
        url = urljoin(config.ship.sync, f"TeamMember::{test_data['gangway']['teamMemberId']}")
        _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/crew/{test_data['gangway']['teamMemberId']}")
            params = {
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            try:
                is_key_there_in_dict('profilePicture', _content)
                if guest_data[count]['ProfilePhotoUrl'] not in _content['profilePicture']:
                    if retries > 0:
                        retries -= 1
                        logger.debug('Security photo for Crew is not synced from Gangway to Gangway Admin !!')
                    else:
                        test_data['gangwayIntegration']['crew_image'] = False
                        raise Exception("updated Security photo for Crew is not synced from couch to Gangway "
                                        "Admin !!")
                else:
                    break
            except (Exception, ValueError):
                if retries > 0:
                    retries -= 1
                    logger.debug('Security photo for Crew is not synced from Gangway to Gangway Admin !!')
                else:
                    test_data['gangwayIntegration']['crew_image'] = False
                    raise Exception("updated Security photo for Crew is not synced from couch to Gangway "
                                    "Admin !!")

    @pytestrail.case(11777704)
    def test_19_verify_visitor_image(self, config, test_data, couch, guest_data, rest_ship):
        """
        Verify Clicked image for visitor gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        test_data['gangwayIntegration']['visitor_image'] = True
        for count, guest in enumerate(guest_data):
            test_data['gangwayIntegration']['visitor_count'] = count
            is_key_there_in_dict('FirstName', guest)
            first_name = guest['FirstName']
            test_data['gangwayIntegration']['visitor_first_name'] = first_name
            is_key_there_in_dict('LastName', guest)
            last_name = guest['LastName']
            test_data['gangwayIntegration']['visitor_last_name'] = last_name
            is_key_there_in_dict('email', guest)
            email_id = guest['email']
            test_data['gangwayIntegration']['visitor_email'] = email_id
            is_key_there_in_dict('birthDate', guest)
            birth_date = guest['birthDate']
            test_data['gangwayIntegration']['visitor_birthdate'] = birth_date
            if len(guest) > 0:
                gender = guest['GenderCode'][0]
            else:
                gender = guest['GenderCode']
            test_data['gangwayIntegration']['visitor_gender'] = gender
            profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                          birth_date=birth_date, gender=gender).add_text()
            logger.debug(f"Uploading Profile Photo #{count + 1} ...")
            url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
            params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
            files = {"file": open(profile_photo, "rb")}
            content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
                "Location"]
            time.sleep(0.1)
            guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
            url = urljoin(config.ship.sync, f"VisitorPersonalInformation::{test_data['gangway']['visitorId']}")
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            _content = couch.send_request(method="GET", url=url, auth="basic").content
            is_key_there_in_dict('_rev', _content)
            test_data['gangway']['rev'] = _content['_rev']
            _content['SecurityPhotoID'] = guest_data[count]['ProfilePhotoUrl']
            _content["lastModifiedBy"] = "Script Automation"
            _content["sourceId"] = "CouchDatabase"
            _content['_rev'] = test_data['gangway']['rev']
            url = urljoin(config.ship.sync, f"VisitorPersonalInformation::{test_data['gangway']['visitorId']}")
            _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
            retries = 60
            while retries >= 0:
                url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                              f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
                params = {
                    'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                    'shipCode': config.ship.code
                }
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                try:
                    is_key_there_in_dict('profileImageUrl', _content)
                    if guest['ProfilePhotoUrl'] not in _content['profileImageUrl']:
                        if retries > 0:
                            retries -= 1
                            logger.debug('created Security photo for Visitor is not synced from Gangway to Gangway '
                                         'Admin !!')
                        else:
                            raise Exception("created Security photo for Visitor is not synced from Gangway to Gangway "
                                            "Admin !!")
                    else:
                        break
                except (Exception, ValueError):
                    if retries > 0:
                        retries -= 1
                        logger.debug(
                            'created Security photo for Visitor is not synced from Gangway to Gangway Admin !!')
                    else:
                        raise Exception("created Security photo for Visitor is not synced from Gangway to Gangway "
                                        "Admin !!")
            break

    @pytestrail.case(11777705)
    def test_20_update_visitor_image(self, config, test_data, couch, guest_data, rest_ship):
        """
        updated image for visitor gets synced to gangway admin
        :param guest_data:
        :param test_data:
        :param config:
        :param couch:
        :param rest_ship:
        """
        if not test_data['gangwayIntegration']['visitor_image']:
            pytest.skip("image not created or updated to edit")
        first_name = test_data['gangwayIntegration']['visitor_first_name']
        last_name = test_data['gangwayIntegration']['visitor_last_name']
        email_id = test_data['gangwayIntegration']['visitor_email']
        birth_date = test_data['gangwayIntegration']['visitor_birthdate']
        gender = test_data['gangwayIntegration']['visitor_gender']
        count = test_data['gangwayIntegration']['visitor_count']
        profile_photo = GeneratePhoto(first_name=first_name, last_name=last_name, email_id=email_id,
                                      birth_date=birth_date, gender=gender).add_text()
        logger.debug(f"Uploading Profile Photo #{test_data['gangwayIntegration']['visitor_count'] + 1} ...")
        url = urljoin(getattr(config.ship.contPath, "url.path.dxpcore"), "mediaitems")
        params = {"mediagroupid": "f67c581d-4a9b-e611-80c2-00155df80332"}
        files = {"file": open(profile_photo, "rb")}
        content = rest_ship.send_request(method="POST", url=url, params=params, files=files, auth="bearer").headers[
            "Location"]
        time.sleep(0.1)
        guest_data[count]['ProfilePhotoUrl'] = content.rsplit('/', 1)[1]
        url = urljoin(config.ship.sync, f"VisitorPersonalInformation::{test_data['gangway']['visitorId']}")
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        _content = couch.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('_rev', _content)
        test_data['gangway']['rev'] = _content['_rev']
        _content['SecurityPhotoID'] = guest_data[count]['ProfilePhotoUrl']
        _content["lastModifiedBy"] = "Script Automation"
        _content["sourceId"] = "CouchDatabase"
        _content['_rev'] = test_data['gangway']['rev']
        url = urljoin(config.ship.sync, f"VisitorPersonalInformation::{test_data['gangway']['visitorId']}")
        _content = couch.send_request(method="PUT", url=url, json=_content, auth="basic").content
        retries = 60
        while retries >= 0:
            url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'),
                          f"/crew-embarkation-admin/visitor/{test_data['gangway']['visitorId']}")
            params = {
                'shipTime': f"{test_data['aci']['shipDate']}T00:00:01",
                'shipCode': config.ship.code
            }
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            try:
                is_key_there_in_dict('profileImageUrl', _content)
                if guest_data[count]['ProfilePhotoUrl'] not in _content['profileImageUrl']:
                    if retries > 0:
                        retries -= 1
                        logger.debug(
                            'updated Security photo for Visitor is not synced from Gangway to Gangway Admin !!')
                    else:
                        raise Exception("updated Security photo for Visitor is not synced from Gangway to Gangway "
                                        "Admin !!")
                else:
                    break
            except (Exception, ValueError):
                if retries > 0:
                    retries -= 1
                    logger.debug('updated Security photo for Visitor is not synced from Gangway to Gangway Admin !!')
                else:
                    raise Exception("updated Security photo for Visitor is not synced from Gangway to Gangway "
                                    "Admin !!")
