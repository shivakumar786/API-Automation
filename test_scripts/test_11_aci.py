__author__ = 'anshuman.goyal'
__maintainer__ = 'sarvesh.singh'

from virgin_utils import *


@pytest.mark.CHECKIN_ONBORD
@pytest.mark.SHIP
@pytest.mark.ACI
@pytest.mark.run(order=12)
class TestACI:
    """
    Test Suite to test Validate (Skipped as of now)
    """

    @pytestrail.case(30685007)
    def test_01_get_rules_dex_version_and_match(self, config, rest_ship, rest_shore):
        """
        To match rules engine version present on both core ship and couch ship side.
        :param config:
        :param rest_ship:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, "url.path.dxprulesengine"), "api/rules/version")
        content = rest_shore.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('LatestVersionNumber', content)
        _url = urljoin(config.ship.sync, "/RulesDEX::v1")
        _content = rest_ship.send_request(method="GET", url=_url).content
        is_key_there_in_dict("version", _content)
        assert _content['version'] == content[
            'LatestVersionNumber'], "Rules version published at core ship side is not matching with couch ship side."

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(205)
    def test_02_get_voyage_id(self, config, test_data, rest_ship):
        """
        Get Voyage ID to be used by Couch
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['aci'] = dict()
        params = {
            "shipcode": config.ship.code
        }
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'voyages/search/findByactiveVoyage')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        is_key_there_in_dict('_embedded', _content)
        voyages = sorted(_content['_embedded']['voyages'], key=lambda i: i['embarkDate'])
        for voyage in voyages:
            test_data['aci']['voyageIdCouch'] = voyage['voyageId']
            test_data['aci']['ship_voyage_id'] = voyage['voyageId']
            break
        else:
            raise Exception("ERROR: voyageId not found in Response !!")

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(96)
    def test_03_validate_ship_time(self, config, test_data, rest_ship):
        """
        Get ship time
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {'shipcode': config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        ship_off_set = _content['shipOffset']
        epoch_time_stamp = _content['epocTimestamp']
        test_data['aci']['shipEpochTime'] = epoch_time_stamp
        ship_off_set = ship_off_set * 60
        test_data['aci']['shipOffSet'] = ship_off_set
        ship_time = (epoch_time_stamp + ship_off_set) * 1000

        test_data['aci']['shipTimeDate'] = datetime.fromtimestamp(ship_time / 1000).strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        test_data['aci']['currentDate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        test_data['demo'] = ship_time
        test_data['aci']['boardingStatusDateEpoch'] = ship_time
        test_data['aci']['validationStatusDate'] = ship_time

    @pytestrail.case(101)
    def test_04_get_doc_id_for_moci_rejected_guest(self, config, test_data, rest_ship, guest_data):
        """
        Get Rejected Document(s) to be verified and to check by default voyage well acknowledgement
        form should be pending
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _content = rest_ship.send_request(method="GET", url=_url).content
            test_data['aci']['guests'] = _content
            test_data[_res_id] = _content
            _res_id = guest['reservationGuestId']
            if not test_data[_res_id]['IsTermsAccepted']:
                _content = rest_ship.send_request(method="GET", url=_url).content
                test_data[_res_id] = _content
        assert "False" != test_data['aci']['guests']['CheckinStatus'], "By default voyage well contract is not" \
                                                                       " coming into pending status. "

    @pytestrail.case(151)
    def test_05_do_aci_for_moci_rejected_guest(self, config, test_data, rest_ship, guest_data):
        """
        Approve Document(s) through ACI
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        params = {"shipcode": config.ship.code}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), 'crew-embarkation/shiptime')
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content

        ship_off_set = _content['shipOffset']
        epoch_time_stamp = _content['epocTimestamp']
        test_data['aci']['shipDate'] = _content['utcTimestamp'].split('T')[0]
        ship_off_set = ship_off_set * 60
        ship_time = (epoch_time_stamp + ship_off_set) * 1000
        test_data['aci']['validationStatusDate'] = str(datetime.fromtimestamp(epoch_time_stamp)).replace(' ', 'T')

        test_data['aci']['shipTimeDate'] = datetime.fromtimestamp(ship_time / 1000).strftime(
            '%Y-%m-%dT%H:%M:%S.%f')
        for count, guest in enumerate(guest_data):
            _res_id = guest['reservationGuestId']
            _data = test_data[_res_id]
            params = {"rev": _data['_rev']}
            _url = f"{config.ship.sync}/GuestStatus::{_res_id}"
            _to_set_true = [
                'IsAssistedCheckInDone', 'IsHealthQuestionsAnswered',
                'IsValidationSuccessful', 'IsIdVerified', 'IsIdentificationDetailsAvailable',
                'IsModerateOnlineCheckInDone', 'IsOnlineCheckedIn', 'IsPartyHealthCompleted',
                'IsPaymentInfoAvailable', 'IsPersonalInformationAvailable', 'IsPhotoVerified',
                'IsPrePostCruiseDetailsAvailable', 'IsContractAgreed'
            ]
            # Set to True-
            for _to_true in _to_set_true:
                _data[_to_true] = True

            _data['lastModifiedBy'] = "Script Automation"
            _data["lastModifiedDate"] = test_data['aci']['shipTimeDate']
            _data["sourceId"] = "CouchDatabase"
            _data["ValidationStatusDate"] = test_data['aci']['validationStatusDate']
            _data["ValidationStatusDateEpoch"] = test_data['aci']['boardingStatusDateEpoch']
            _data['CheckInStatusDateEpoch'] = test_data['aci']['boardingStatusDateEpoch']
            _data['CheckinStatusDate'] = test_data['aci']['validationStatusDate']
            _data['TerminalCheckinStatus'] = 'COMPLETED'

            _content = rest_ship.send_request(method="PUT", url=_url, json=_data, params=params,
                                              auth="crew").content
            assert _content['ok'], "ACI for Rejected Guests Failed !!"

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(30406678)
    def test_06_verify_voyage_well_email_guest_status(self, config, test_data, rest_shore):
        """
        Check that provided email in voyage well form should get save in GuestStatus.
        :param test_data:
        :param rest_shore:
        :return:
        """
        _url = urljoin(config.ship.sync, f"/GuestStatus::{test_data['aci']['guests']['ReservationGuestID']}")
        _content = rest_shore.send_request(method="GET", url=_url).content
        _content["CruisewellContractSignedBy"] = ""
        _content["CruisewellContractSignedByEmail"] = "vertical-qa@decurtis.com"
        _content["CruisewellContractSignedDateEpoch"] = test_data['aci']['boardingStatusDateEpoch']
        _content["CruisewellContractSignedID"] = ""
        params = {"rev": _content['_rev']}
        to_content = rest_shore.send_request(method="PUT", url=_url, json=_content, params=params,
                                             auth="admin").content
        assert to_content['ok'], "Crew is not able to pass sailor through voyage well."
        _to_content = rest_shore.send_request(method="GET", url=_url).content
        assert _to_content['CruisewellContractSignedByEmail'] == _content[
            "CruisewellContractSignedByEmail"], "Email address provided in voyage well information during" \
                                                " ACI did not get save to GuestStatus. "

    @pytestrail.case(41362620)
    def test_07_get_not_checked_guests(self, test_data, config, rest_ship ):
        """
        Function to get Untouched guests
        :param config:
        :param test_data:
        :param rest_ship
        :return:
        """
        url = urljoin(config.ship.sync, '_config')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        url = _content['server']
        if config.platform == 'DCL' and config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
            test_data['server_url'] = url
            test_data['bucket'] = _content['bucket']

        query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{test_data['voyageNumber']}'" \
                f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{test_data['bucket']}` b where " \
                f"meta(b).id not like '_sync%' and b.type='GuestStatus' and (b.IsOnBoarded is missing))"
        url = urljoin(f"{test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if config.envMasked == "CERT":
            url = urljoin(f"{test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('results', _content)
        test_data['not_checkedin'] = _content['results']
        assert _content['results'], "ACI done for untouched guests !!"

    @pytestrail.case(1124999)
    def test_08_get_ocidone_moci_pending(self, test_data, config, rest_ship):
        """
        get oci done moci pending guest from the couchbase
        :param config:
        :param test_data:
        :param rest_ship
        :return:
        """
        url = urljoin(config.ship.sync, '_config')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        is_key_there_in_dict('username', _content)
        is_key_there_in_dict('password', _content)
        url = _content['server']
        if config.platform == 'DCL' and config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
            test_data['server_url'] = url
            test_data['bucket'] = _content['bucket']
            test_data['username'] = _content['username']
            test_data['password'] = _content['password']

        query = f"select raw a.ReservationNumber from `{test_data['bucket']}` a where " \
                f"a.type = 'GuestPersonalInformation'and a.ReservationGuestID in " \
                f"( select raw b.ReservationGuestID  from `{test_data['bucket']}`  b where b.type = 'GuestStatus' " \
                f"and b.IsContractAgreed = true " \
                f"and b.IsPrePostCruiseDetailsAvailable = true " \
                f"and b.IsIdentificationDetailsAvailable = true " \
                f"and b.IsTermsAccepted = false " \
                f"and b.IsPaymentInfoAvailable = true " \
                f"and b.IsPersonalInformationAvailable = true " \
                f"and (b.PreValidateStatus = 'PENDING' or b.PreValidateStatus is MISSING) " \
                f"and (b.IsValidationSuccessful = false and " \
                f"(b.checkinStatus = false or (b.IsOnBoarded is missing or b.IsOnBoarded = false))) " \
                f"and EmbarkDateEpoch = '' " \
                f"and meta().id not like '_sync%')"

        url = urljoin(f"{test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if config.envMasked == "CERT":
            url = urljoin(f"{test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query,"pretty":False,"timeout":"600s","client_context_id":""
        }
        _content = rest_ship.send_request(method="POST", url= url, json=body, auth="crew").content
        is_key_there_in_dict('results', _content)
        test_data['moci_pending'] = _content['results']

    @pytestrail.case(1125000)
    def test_09_get_ocidone_moci_approved(self, test_data, config, rest_ship):
        """
        get oci done moci approved guest from the couchbase
        :param config:
        :param test_data:
        :param rest_ship
        :return:
        """
        url = urljoin(config.ship.sync, '_config')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        is_key_there_in_dict('username', _content)
        is_key_there_in_dict('password', _content)
        url = _content['server']
        if config.platform == 'DCL' and config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
            test_data['server_url'] = url
            test_data['bucket'] = _content['bucket']
            test_data['username'] = _content['username']
            test_data['password'] = _content['password']

        query = f"select raw a.ReservationNumber from `{test_data['bucket']}` a where " \
                f"a.type = 'GuestPersonalInformation' and a.ReservationGuestID in " \
                f"( select raw b.ReservationGuestID from `{test_data['bucket']}` b where b.type = 'GuestStatus' " \
                f"and b.IsIdentificationDetailsAvailable = true " \
                f"and b.IsPersonalInformationAvailable = true and " \
                f"b.IsPrePostCruiseDetailsAvailable = true and " \
                f"b.IsPaymentInfoAvailable = true and b.IsTermsAccepted = true " \
                f"and b.IsContractAgreed = true and (b.PreValidateStatus ='APPROVED') " \
                f"and (b.IsValidationSuccessful = false and " \
                f"(b.checkinStatus = false or (b.IsOnBoarded is missing or b.IsOnBoarded = false))) and " \
                f"b.EmbarkDateEpoch = 1660867200000 and meta().id not like '_sync%')"

        url = urljoin(f"{test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if config.envMasked == "CERT":
            url = urljoin(f"{test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query, "pretty": False, "timeout": "600s", "client_context_id": "","profile": "timings",
            "scan_consistency": "not_bounded"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('results', _content)
        test_data['moci_approved'] = _content['results']

    @pytestrail.case(1125001)
    def test_10_get_ocidone_moci_rejected(self, test_data, config, rest_ship):
        """
        get oci done moci rejected guest from the couchbase
        :param config:
        :param test_data:
        :param rest_ship
        :return:
        """
        url = urljoin(config.ship.sync, '_config')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        is_key_there_in_dict('username', _content)
        is_key_there_in_dict('password', _content)
        url = _content['server']
        if config.platform == 'DCL' and config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
            test_data['server_url'] = url
            test_data['bucket'] = _content['bucket']
            test_data['username'] = _content['username']
            test_data['password'] = _content['password']

        query = f"select raw a.ReservationNumber from `{test_data['bucket']}` a where " \
                f"a.type = 'GuestPersonalInformation' and a.ReservationGuestID in" \
                f"( select raw b.ReservationGuestID from `{test_data['bucket']}` b where b.type = 'GuestStatus'" \
                f"and b.IsIdentificationDetailsAvailable = true " \
                f"and b.IsPersonalInformationAvailable = true and " \
                f"b.IsPrePostCruiseDetailsAvailable = true and " \
                f"b.IsPaymentInfoAvailable = true and b.IsTermsAccepted = true and " \
                f"b.IsContractAgreed = true and (b.PreValidateStatus = 'REJECTED') " \
                f"and (b.IsValidationSuccessful = false and " \
                f"(b.checkinStatus = false or (b.IsOnBoarded is missing or b.IsOnBoarded = false))) and " \
                f"b.EmbarkDateEpoch = '' and meta().id not like '_sync%')"

        url = urljoin(f"{test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if config.envMasked == "CERT":
            url = urljoin(f"{test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query, "pretty": False, "timeout": "600s", "client_context_id": "", "profile": "timings",
            "scan_consistency": "not_bounded"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('results', _content)
        test_data['moci_rejected'] = _content['results']

    @pytestrail.case(41367757)
    def test_11_get_acidone_not_checkin(self, test_data, config, rest_ship):
        """
        get oci done not checkdin guest from the couchbase
        :param config:
        :param test_data:
        :param rest_ship
        :return:
        """
        url = urljoin(config.ship.sync, '_config')
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        is_key_there_in_dict('server', _content)
        is_key_there_in_dict('bucket', _content)
        is_key_there_in_dict('username', _content)
        is_key_there_in_dict('password', _content)
        url = _content['server']
        if config.platform == 'DCL' and config.envMasked == 'LATEST':
            ServerIP = url.split(",")
            # url = f"{ServerIP[0]}:{ServerIP[1].split(':')[1]}"
            url = f"http:{ServerIP[0].split(':')[1]}:8091"
        else:
            url = f"http:{_content['server'].split(':')[1]}:8091"
            test_data['server_url'] = url
            test_data['bucket'] = _content['bucket']
            test_data['username'] = _content['username']
            test_data['password'] = _content['password']

        query = f"select a.FirstName,a.LastName,a.ReservationNumber, a.VoyageNumber, a.ReservationGuestID from `{test_data['bucket']}` a where " \
                f"meta(a).id not like '_sync%' and a.type='GuestPersonalInformation' and a.VoyageNumber = '{test_data['voyageNumber']}'" \
                f" and a.ReservationGuestID in ( select raw b.ReservationGuestID from `{test_data['bucket']}` b where " \
                f"meta(b).id not like '_sync%' and b.type='GuestStatus' and (b.IsOnBoarded is missing or b.IsOnBoarded = true))"

        url = urljoin(f"{test_data['server_url'].rsplit(':', 1)[0]}:8093/query/service")
        if config.envMasked == "CERT":
            url = urljoin(f"{test_data['server_url'].rsplit(',')[0]}:8093/query/service")
        body = {
            "creds": [{"user": "selectuser", "pass": "Cbsselect*101"}],
            "statement": query, "pretty": False, "timeout": "600s", "client_context_id": "", "profile": "timings",
            "scan_consistency": "not_bounded"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('results', _content)
        test_data['not_checkedin'] = _content['results']
        assert _content['results'], "ACI done for not checked in guests !!"
