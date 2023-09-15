__author__ = 'anshuman.goyal'

import pytest

from virgin_utils import *


@pytest.mark.SHORE
@pytest.mark.MOCI
@pytest.mark.run(order=7)
class TestMoci:
    """
    Suite to test MOCI
    """

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(720221)
    def test_01_wait_for_moci_data(self, config, request, rest_shore, guest_data):
        """
        Test MOCI Startup
        :param config:
        :param request:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _data_file = os.path.join(request.config.rootdir.strpath,
                                  'test_data/verification_data/moci_wait_for_moci_data.json')
        with open(_data_file, 'r') as _fp:
            _data = json.load(_fp)

        for count, guest in enumerate(guest_data):
            _res = guest['reservationGuestId']
            url = urljoin(getattr(config.shore.contPath, 'url.path.reporting'),
                          "/reservationguestmoderations/findbyreservationguestid")
            params = {
                'reservation-guest-id': _res
            }
            _content = rest_shore.send_request(method="GET", url=url, auth="admin", params=params).content
            diff = set(get_all_keys_in_dict(_data)) - set(get_all_keys_in_dict(_content))
            # To Do diff should be 0 after this bug gets resolved - DCP-44885
            if len(diff) > 1:
                raise Exception(f"MOCI Document Mismatch: {list(diff)}")
            count += 1

    @pytestrail.case(88)
    def test_02_startup(self, config, test_data, rest_shore):
        """
        Test MOCI Startup
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['moci'] = dict()
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/moci/startup")
        _content = rest_shore.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('loggingMode', _content)
        is_key_there_in_dict('loggingUrl', _content)
        is_key_there_in_dict('shipDashboardUrl', _content)
        is_key_there_in_dict('voyageDashboardUrl', _content)
        is_key_there_in_dict('clientToken', _content)
        is_key_there_in_dict('lookupDataUrl', _content)
        test_data['moci'].update(_content)

    @pytestrail.case(176)
    def test_03_lookup(self, test_data, rest_shore):
        """
        Test MOCI Lookup
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['moci']['lookupDataUrl']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        is_key_there_in_dict('referenceData', _content)
        is_key_there_in_dict('documentTypes', _content['referenceData'])
        is_key_there_in_dict('genders', _content['referenceData'])
        is_key_there_in_dict('cities', _content['referenceData'])
        is_key_there_in_dict('states', _content['referenceData'])
        is_key_there_in_dict('countries', _content['referenceData'])
        is_key_there_in_dict('ports', _content['referenceData'])
        is_key_there_in_dict('voyages', _content['referenceData'])
        is_key_there_in_dict('voyages', _content['referenceData'])
        is_key_there_in_dict('rejectionList', _content['referenceData'])
        is_key_there_in_dict('visaTypes', _content['referenceData'])
        is_key_there_in_dict('brands', _content['referenceData'])
        is_key_there_in_dict('ships', _content['referenceData'])

    @pytestrail.case(166)
    def test_04_dashboard_voyage(self, test_data, rest_shore):
        """
        Get Voyage Dashboard
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['moci']['voyageDashboardUrl']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        is_key_there_in_dict('graph', _content)
        is_key_there_in_dict('upcomingVoyages', _content)

        if len(_content['graph']) == 0:
            raise Exception("ERROR: No Content in Graph !!")

        is_key_there_in_dict('sailingStartDate', _content['graph'])
        is_key_there_in_dict('sailingDuration', _content['graph'])
        is_key_there_in_dict('voyages', _content['graph'])

        for voyage in _content['graph']['voyages']:
            is_key_there_in_dict('id', voyage)
            is_key_there_in_dict('shipCode', voyage)
            is_key_there_in_dict('embarkDate', voyage)
            is_key_there_in_dict('debarkDate', voyage)
            is_key_there_in_dict('totalCount', voyage)
            is_key_there_in_dict('approvedCount', voyage)
            is_key_there_in_dict('pendingOverdueCount', voyage)
            is_key_there_in_dict('pendingCount', voyage)
            is_key_there_in_dict('incompleteMessagedCount', voyage)
            is_key_there_in_dict('callNeededCount', voyage)
            is_key_there_in_dict('incompleteCount', voyage)
            is_key_there_in_dict('notStartedCount', voyage)
            is_key_there_in_dict('href', voyage['_links']['detailUrl'])
            test_data['moci']['guestListUrl'] = voyage['_links']['detailUrl']['href']

        for upcomingVoyage in _content['upcomingVoyages']:
            is_key_there_in_dict('id', upcomingVoyage)
            is_key_there_in_dict('_links', upcomingVoyage)
            is_key_there_in_dict('detailUrl', upcomingVoyage['_links'])
            is_key_there_in_dict('href', upcomingVoyage['_links']['detailUrl'])

        is_key_there_in_dict('_links', _content)
        is_key_there_in_dict('rejectionReasonReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['rejectionReasonReportUrl'])
        is_key_there_in_dict('moderationReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['moderationReportUrl'])
        is_key_there_in_dict('comparisonReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['comparisonReportUrl'])
        is_key_there_in_dict('ociStatusReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['ociStatusReportUrl'])
        is_key_there_in_dict('systemModerationReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['systemModerationReportUrl'])
        is_key_there_in_dict('historyUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['historyUrl'])

        test_data['moderationReportUrl'] = _content['_links']['moderationReportUrl']['href']
        test_data['ociStatusReportUrl'] = _content['_links']['ociStatusReportUrl']['href']
        test_data['historyUrl'] = _content['_links']['historyUrl']['href']

    @pytestrail.case(122)
    def test_05_dashboard_ship(self, test_data, rest_shore):
        """
        Get Voyage Ship Dashboard
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['moci']['shipDashboardUrl']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        is_key_there_in_dict('graph', _content)
        is_key_there_in_dict('sailingStartDate', _content['graph'])
        is_key_there_in_dict('sailingDuration', _content['graph'])
        for ship in _content['graph']['ships']:
            is_key_there_in_dict('code', ship)
            is_key_there_in_dict('nearestEmbarkDate', ship)
            is_key_there_in_dict('totalCount', ship)
            is_key_there_in_dict('approvedCount', ship)
            is_key_there_in_dict('pendingOverdueCount', ship)
            is_key_there_in_dict('pendingCount', ship)
            is_key_there_in_dict('incompleteMessagedCount', ship)
            is_key_there_in_dict('callNeededCount', ship)
            is_key_there_in_dict('voyageDetails', ship)
            for voyageDetail in ship['voyageDetails']:
                is_key_there_in_dict('id', voyageDetail)
                is_key_there_in_dict('embarkDate', voyageDetail)
                is_key_there_in_dict('debarkDate', voyageDetail)
                is_key_there_in_dict('totalCount', voyageDetail)
                is_key_there_in_dict('approvedCount', voyageDetail)
                is_key_there_in_dict('pendingOverdueCount', voyageDetail)
                is_key_there_in_dict('pendingCount', voyageDetail)
                is_key_there_in_dict('incompleteMessagedCount', voyageDetail)
                is_key_there_in_dict('callNeededCount', voyageDetail)
            is_key_there_in_dict('_links', ship)
            is_key_there_in_dict('detailUrl', ship['_links'])
            is_key_there_in_dict('href', ship['_links']['detailUrl'])
        is_key_there_in_dict('upcomingShips', _content)
        for upcomingShip in _content['upcomingShips']:
            is_key_there_in_dict('code', upcomingShip)
            is_key_there_in_dict('nearestEmbarkDate', upcomingShip)
            is_key_there_in_dict('_links', upcomingShip)
            is_key_there_in_dict('detailUrl', upcomingShip['_links'])
            is_key_there_in_dict('href', upcomingShip['_links']['detailUrl'])
        is_key_there_in_dict('_links', _content)
        is_key_there_in_dict('rejectionReasonReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['rejectionReasonReportUrl'])
        is_key_there_in_dict('moderationReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['moderationReportUrl'])
        test_data['moderationReportUrl'] = _content['_links']['moderationReportUrl']['href']
        is_key_there_in_dict('comparisonReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['comparisonReportUrl'])
        is_key_there_in_dict('ociStatusReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['ociStatusReportUrl'])
        test_data['ociStatusReportUrl'] = _content['_links']['ociStatusReportUrl']['href']
        is_key_there_in_dict('systemModerationReportUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['systemModerationReportUrl'])
        is_key_there_in_dict('historyUrl', _content['_links'])
        is_key_there_in_dict('href', _content['_links']['historyUrl'])
        test_data['historyUrl'] = _content['_links']['historyUrl']['href']

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(117)
    def test_06_get_moci_guests(self, config, test_data, rest_shore, guest_data):
        """
        Find MOCI Guests
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _res_number = test_data['reservationNumber']
        params = {
            'input': _res_number
        }
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/moci/search')
        _content = rest_shore.send_request(method="GET", url=url, params=params, auth="admin").content
        is_key_there_in_dict('guests', _content)
        for count, guest in enumerate(guest_data):
            if len(_content['guests']) == 0:
                raise Exception(f"ERROR: Zero Guests Returned by '{url}'")
            for _data in _content['guests']:
                _f_name = str(re.search(r'(\w+)\s*(\w+)', _data['name']).group(1)).lower()
                _l_name = str(re.search(r'(\w+)\s*(\w+)', _data['name']).group(2)).lower()
                if _f_name == str(guest['firstName']).lower() and _l_name == str(guest['lastName']).lower():
                    is_key_there_in_dict('reservationNumber', _data)
                    is_key_there_in_dict('name', _data)
                    is_key_there_in_dict('status', _data)
                    is_key_there_in_dict('embarkDate', _data)
                    is_key_there_in_dict('voyageId', _data)
                    is_key_there_in_dict('shipCode', _data)
                    is_key_there_in_dict('reviewLaterFlag', _data)
                    is_key_there_in_dict('photoUrl', _data)
                    is_key_there_in_dict('_links', _data)
                    is_key_there_in_dict('detailUrl', _data['_links'])
                    is_key_there_in_dict('href', _data['_links']['detailUrl'])
                    is_key_there_in_dict('requiredFieldsUrl', _data['_links'])
                    is_key_there_in_dict('href', _data['_links']['requiredFieldsUrl'])
                    guest_data[count]['EmbarkDate'] = _data['embarkDate']
                    guest_data[count]['VoyageId'] = str(_data['voyageId'])
                    guest_data[count]['ShipCode'] = str(_data['shipCode'])
                    guest_data[count]['DetailUrl'] = _data['_links']['detailUrl']['href']
                    guest_data[count]['RequiredFieldsUrl'] = _data['_links']['requiredFieldsUrl']['href']
                    guest['DetailUrl'] = _data['_links']['detailUrl']['href']
        is_key_there_in_dict('page', _content)
        is_key_there_in_dict('totalElements', _content['page'])
        is_key_there_in_dict('totalPages', _content['page'])
        is_key_there_in_dict('currentPage', _content['page'])
        is_key_there_in_dict('href', _content['page']['_links']['firstPageUrl'])
        is_key_there_in_dict('href', _content['page']['_links']['lastPageUrl'])

    @pytestrail.case(287)
    def test_07_check_all_guests_in_pending_before_approving(self, rest_shore, guest_data):
        """
        Checking if all guests are in Pending State before we do an MOCI on them
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            # Validate if what we have set has been updated on server
            _content = rest_shore.send_request(method="GET", url=guest['DetailUrl'], auth="admin").content
            _data = _content['guestDetail']
            # Verifying Photo Status
            for _count, _item in enumerate(_data['personalInfo']['photoDetail']):
                assert _item['status'] == "PENDING", "ERROR: Photo Not in Pending !!"
            # Verify Visa Document(s)
            for _count, _item in enumerate(_data['identificationDocumentInfo']['visaInfoList']['visaList']):
                assert _item['status'] == "PENDING", "ERROR: Visa Not in Pending !!"
            # Verify Passport Document(s)
            _items = _data['identificationDocumentInfo']['identificationDocuments']
            for _count, _item in enumerate(_items):
                assert _item['status'] == "PENDING", "ERROR: Passport Not in Pending !!"

    @pytestrail.case(179)
    def test_08_search(self, config, test_data, rest_shore, guest_data):
        """
        Search MOCI
        :param config:
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        _res_number = test_data['reservationNumber']
        params = {"input": _res_number}
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/moci/search")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="admin").content
        is_key_there_in_dict('guests', _content)
        for count, guest in enumerate(guest_data):
            for _data in _content['guests']:
                _f_name = re.search(r'(\w+)\s*(\w+)', _data['name']).group(1)
                _l_name = re.search(r'(\w+)\s*(\w+)', _data['name']).group(2)
                if _f_name == guest['firstName'] and _l_name == guest['lastName']:
                    is_key_there_in_dict('voyageId', _data)
                    is_key_there_in_dict('reservationNumber', _data)
                    is_key_there_in_dict('status', _data)
                    is_key_there_in_dict('embarkDate', _data)
                    is_key_there_in_dict('photoUrl', _data)
                    is_key_there_in_dict('_links', _data)
                    is_key_there_in_dict('href', _data['_links']['requiredFieldsUrl'])
                    is_key_there_in_dict('href', _data['_links']['detailUrl'])
                    guest_data[count]['DetailUrl'] = _data['_links']['detailUrl']['href']
                    guest_data[count]['RequiredFieldsUrl'] = _data['_links']['requiredFieldsUrl']['href']
                    break
        is_key_there_in_dict('totalElements', _content['page'])
        is_key_there_in_dict('totalPages', _content['page'])
        is_key_there_in_dict('currentPage', _content['page'])
        is_key_there_in_dict('href', _content['page']['_links']['firstPageUrl'])
        is_key_there_in_dict('href', _content['page']['_links']['lastPageUrl'])

    @pytestrail.case(124)
    def test_09_required_fields(self, rest_shore, guest_data):
        """
        Test MOCI Required Fields
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['RequiredFieldsUrl']
            _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
            is_key_there_in_dict('requiredFields', _content)
            is_key_there_in_dict('hiddenFields', _content)
            is_key_there_in_dict('readonlyFields', _content)

    @pytestrail.case(118)
    def test_10_guest_details_virgin(self, rest_shore, guest_data):
        """
        Get MOCI Guest Details
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['DetailUrl']
            _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
            _links = _content['_links']
            guest_data[count]['UpdateUrl'] = _links['updateUrl']['href']
            guest_data[count]['ReviewLaterUrl'] = _links['reviewLaterUrl']['href']
            guest_data[count]['AuditTrailUrl'] = _links['auditTrailUrl']['href']
            guest_data[count]['ValidateUrl'] = _links['validateUrl']['href']
            # TO DO UnlockGuestUrl field should be stored after this bug gets solved - DCP-44887
            guest_data[count]['NextGuestUrl'] = _links['nextGuestUrl']['href']
            guest_data[count]['ShoreGuestDetail'] = _content['guestDetail']
            guest_data[count]['guestsSummary'] = _content
            guest_data[count]['shipDetail'] = _content['shipDetail']
            guest_data[count]['_links'] = _content['_links']

    @pytestrail.case(116)
    def test_11_validate(self, rest_shore, guest_data):
        """
        Validate MOCI Guest Details
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['ValidateUrl']
            body = {
                "guestDetail": guest['ShoreGuestDetail'],
                "guestsSummary": [],
                "isReadOnly": False,
                "isReservationCanceled": False,
                "isValidated": False,
                "status": "A",
                "shipDetail": guest['shipDetail'],
                "_links": guest['_links']
            }
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="admin")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(92)
    def test_12_approve_reject_guests(self, test_data, rest_shore, guest_data):
        """
        Validate MOCI Guest Details
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _content = rest_shore.send_request(method="GET", url=guest['DetailUrl'], auth="admin").content
            _data = _content['guestDetail']

            # Approve/Reject Photo
            for _count, _ in enumerate(_data['personalInfo']['photoDetail']):
                if _data['guestId'] == test_data['mociRejected'] or _data['guestId'] == test_data['docRejected']:
                    _data['personalInfo']['photoDetail'][_count]['status'] = "REJECTED"
                else:
                    _data['personalInfo']['photoDetail'][_count]['status'] = "APPROVED"

            # Approve (always) Visa
            for _count, _ in enumerate(_data['identificationDocumentInfo']['visaInfoList']['visaList']):
                _data['identificationDocumentInfo']['visaInfoList']['visaList'][_count]['status'] = "APPROVED"

            # Approve (always) Passport
            for _count, _ in enumerate(_data['identificationDocumentInfo']['identificationDocuments']):
                _data['identificationDocumentInfo']['identificationDocuments'][_count]['status'] = "APPROVED"
            rest_shore.send_request(method="PUT", url=guest['UpdateUrl'], json={"guestDetail": _data}, auth="admin")

    @pytestrail.case(135)
    def test_13_audit_trail(self, rest_shore, guest_data):
        """
        Test MOCI Audit Trail
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['AuditTrailUrl']
            _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
            is_key_there_in_dict('moderationHistory', _content)
            for moderator in _content['moderationHistory']:
                is_key_there_in_dict('moderatorId', moderator)
                is_key_there_in_dict('name', moderator)
                is_key_there_in_dict('modificationTime', moderator)
                is_key_there_in_dict('activityLogs', moderator)
                for activityLog in moderator['activityLogs']:
                    is_key_there_in_dict('typeCode', activityLog)
                    is_key_there_in_dict('field', activityLog)
                    is_key_there_in_dict('isMasterDataDependent', activityLog)
                    is_key_there_in_dict('newValue', activityLog)

    @pytestrail.case(158)
    def test_14_history(self, config, test_data, rest_shore):
        """
        Test MOCI History
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        body = {
            "shipCode": config.ship.code, "fromDate": "2019-01-01T18:30:00", "toDate": "2019-12-31T18:29:59",
            "moderatorId": "1224",
            "recordStatuses": [
                "ICMCN",
                "ICMO",
                "ICM",
                "A"
            ],
            "voyageNumber": test_data['voyage']['id']
        }
        url = test_data['historyUrl']
        rest_shore.send_request(method="POST", url=url, json=body, auth="admin")

    @pytestrail.case(456)
    def test_15_verify_approved_rejected_guests(self, test_data, rest_shore, guest_data):
        """
        Verify approved/rejected guests are updated or not
        :param test_data:
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            # Validate if what we have set has been updated on server
            _content = rest_shore.send_request(method="GET", url=guest['DetailUrl'], auth="admin").content
            guest_data[count]['MOCIGuestData'] = _content['guestDetail']
            guest_data[count]['MOCIGuestStatus'] = _content['status']
            _data = _content['guestDetail']

            # Verifying Photo Status
            for _count, _item in enumerate(_data['personalInfo']['photoDetail']):
                if _data['guestId'] == test_data['mociRejected'] or _data['guestId'] == test_data['docRejected']:
                    assert _item['status'] == "REJECTED", "ERROR: Photo Not Rejected !!"
                else:
                    assert _item['status'] == "APPROVED", "ERROR: Photo Not Approved !!"

            # Verify Visa Document(s)
            for _count, _item in enumerate(_data['identificationDocumentInfo']['visaInfoList']['visaList']):
                assert _item['status'] == "APPROVED", "ERROR: Visa Not Approved !!"

            # Verify Passport Document(s)
            _items = _data['identificationDocumentInfo']['identificationDocuments']
            for _count , _item in enumerate(_items):
                assert _item['status'] == "APPROVED", "ERROR: Passport Not Approved !!"

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(1664606)
    def test_16_doc_rejected_flag(self, config, test_data, rest_shore):
        """
        Verify Doc Rejected Flag
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        _res_number = test_data['reservationNumber']
        params = {
            "input": _res_number
        }
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "/moci/search")
        _content = rest_shore.send_request(method="GET", url=_url, params=params, auth="admin").content
        is_key_there_in_dict('guests', _content)
        for _guest in _content['guests']:
            is_key_there_in_dict('isPreviouslyRejected', _guest)
            is_key_there_in_dict('status', _guest)
            if _guest['status'] == 'A':
                assert not _guest['isPreviouslyRejected'], "ERROR: Photo is Rejected for approved guest!!"
            else:
                assert _guest['isPreviouslyRejected'], "ERROR: Photo is not Rejected for rejected guest!!"

    @pytestrail.case(168)
    def test_17_review_later(self, rest_shore, guest_data):
        """
        Test MOCI Review Later
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['ReviewLaterUrl']
            body = {"reviewLaterFlag": True}
            rest_shore.send_request(method="PUT", url=url, json=body, auth="admin")

    @pytestrail.case(172)
    def test_18_report_oci_stats_virgin(self, test_data, rest_shore, config):
        """
        Test OCI Report Stats
        :param test_data:
        :param rest_shore:
        :param config:
        :return:
        """
        url = test_data['ociStatusReportUrl']
        from_date = datetime.now(tz=pytz.utc).date() - timedelta(days=2)
        to_date = datetime.now(tz=pytz.utc).date() + timedelta(days=2)
        body = {
            "shipCode": config.ship.code,
            "voyageNumbers": [test_data['voyage']['id']],
            "fromDate": from_date.strftime("%m-%d-%Y"),
            "toDate": to_date.strftime("%m-%d-%Y")
        }
        test_data["oci_status"] = True
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="admin").content
        if len(_content['statistics']) == 0:
            test_data["oci_status"] = False
            pytest.skip("Can't test the OCI report")
        test_data['emailStatusUrl'] = _content['_links']['emailStatusUrl']['href']

    @pytestrail.case(106)
    def test_19_oci_stats_email_virgin(self, test_data, rest_shore):
        """
        Test OCI Report email status
        :param test_data:
        :param rest_shore:
        :return:
        """
        if not test_data["oci_status"]:
            pytest.skip("OCI email status is false")
        url = test_data['emailStatusUrl']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        is_key_there_in_dict('isInProcess', _content)

    @pytestrail.case(119)
    def test_20_moci_report(self, config, test_data, rest_shore):
        """
        Check Moderation Report URL
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = test_data['moderationReportUrl']
        from_date = datetime.now(tz=pytz.utc).date() - timedelta(days=2)
        to_date = datetime.now(tz=pytz.utc).date() + timedelta(days=2)
        body = {
            "shipCode": config.ship.code,
            "voyageNumbers": [test_data['voyage']['id']],
            "fromDate": from_date.strftime("%m-%d-%Y"),
            "toDate": to_date.strftime("%m-%d-%Y")
        }
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="admin").content
        is_key_there_in_dict('statistics', _content)
        for stats in _content['statistics']:
            is_key_there_in_dict('startDate', stats)
            is_key_there_in_dict('endDate', stats)
            is_key_there_in_dict('voyageNumber', stats)
            is_key_there_in_dict('rejtDueToSecurityPhotoCount', stats)
            is_key_there_in_dict('rejtDueToIdDocumentCount', stats)
            is_key_there_in_dict('rejectedCount', stats)
            is_key_there_in_dict('approvedCount', stats)

    @pytestrail.case(25018397)
    def test_21_validation_of_personal_info_after_rts(self, rest_shore, guest_data):
        """
        Check the Personal Data should flow from RTS to MOCI
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for guest in guest_data:
            url = guest['DetailUrl']
            _content = rest_shore.send_request(method="GET", url=url, auth="admin").content

            guest["details_content"] = _content
            personal_info = _content['guestDetail']['personalInfo']
            if personal_info['firstName'].lower() == guest['FirstName'].lower():
                assert personal_info['citizenshipCode'] == guest[
                    'CitizenshipCountryCode'], "Guest citizenship is not matching"
                assert personal_info['lastName'].lower() == guest['LastName'].lower(), "Last name is not matching"
                assert datetime.strptime(personal_info['birthDate'], "%m-%d-%Y").strftime('%Y-%m-%d') == guest[
                    'BirthDate'], "Guest birthdate is not matching"

    @pytestrail.case(25018398)
    def test_22_validation_of_identification_info_after_rts(self, guest_data):
        """
        Check the Identification Data should flow from RTS to MOCI
        :param guest_data:
        :return:
        """
        for guest in guest_data:
            _content = guest["details_content"]
            passport_info = _content['guestDetail']['identificationDocumentInfo']['identificationDocuments']
            for passport_infos in passport_info:
                assert passport_infos['countryCode'] == guest[
                    'CitizenshipCountryCode'], "Guest citizenship is not matching"
                assert passport_infos['number'] == guest['passportNumber'], "Passport number is not matching"
                assert passport_infos['givenName'].lower() == guest['FirstName'].lower(), "Given name is not matching"
                assert passport_infos['surname'].lower() == guest['LastName'].lower(), "Surname name is not matching"
                assert datetime.strptime(passport_infos['expiresOn'], "%m-%d-%Y").strftime('%Y-%m-%d') == guest[
                    'passportExpiry'], "Passport Expiry date is not matching"
                break
            else:
                raise Exception("Passport info is not sync to MOCI")

    @pytestrail.case(25018399)
    def test_23_validation_of_payment_info_after_rts(self, guest_data):
        """
        Check the Payment Data should flow from RTS to MOCI
        :param guest_data:
        :return: 
        """
        for guest in guest_data:
            _content = guest["details_content"]
            personal_info = _content['guestDetail']['personalInfo']
            assert personal_info['firstName'].lower() == guest[
                'FirstName'].lower(), "paymentPolicyAccepted info not sync to MOCI"
            assert _content['guestDetail']['paymentInfo'][
                       'paymentPolicyAccepted'] == True, "paymentPolicyAccepted info not sync to MOCI"
            assert _content['guestDetail']['paymentInfo']['paymentModeId'] == guest[
                'payment_method'], "Payment mode is sync in MOCI"

    @pytestrail.case(25018401)
    def test_24_validation_of_contract_info_after_rts(self, guest_data):
        """
        Check the Contract Data should flow from RTS to MOCI
        :param guest_data:
        :return:
        """
        for guest in guest_data:
            _content = guest["details_content"]
            personal_info = _content['guestDetail']['personalInfo']
            if personal_info['firstName'].lower() == guest['FirstName'].lower():
                assert _content['guestDetail']['contractInfo'][
                           'contractSigned'] == True, "Contract signed info not sync to MOCI"
                assert _content['guestDetail']['contractInfo']['signedByReservationGuestId'] == guest[
                    'reservationGuestId'], "reservationGuestId is not matching"

    @pytestrail.case(25018400)
    def test_25_validation_of_pre_post_travel_info_after_rts(self, guest_data):
        """
        Check the pre and post travel Data should flow from RTS to MOCI
        :param guest_data:
        :return:
        """
        for guest in guest_data:
            _content = guest["details_content"]
            if _content['guestDetail']['personalInfo']['firstName'].lower() == guest['FirstName'].lower():
                precruise_info = _content['guestDetail']['travelInfo']['preCruiseInfo']['flightDetails'][0]
                postcruise_info = _content['guestDetail']['travelInfo']['postCruiseInfo']['flightDetails'][0]
                assert _content['guestDetail']['travelInfo'][
                           'preCruiseInfo']['flightDetails'][0]['airlineCode'] == guest['flightDetails'][
                           'airlineCode'], "airline code not sync to MOCI"
                assert precruise_info['flightNumber'] == guest['flightDetails']['number'], "Flight number is not sync"
                assert precruise_info['departureCity'] == guest['flightDetails'][
                    'departureCity'], "Departure city not sync to MOCI"
                assert precruise_info['departureTime'] == guest['flightDetails'][
                    'departureTime'], "Departure Time not sync to MOCI"
                assert precruise_info['arrivalCity'] == guest['flightDetails'][
                    'arrivalCity'], "Arrival City not sync to MOCI"
                assert precruise_info['arrivalTime'] == guest['flightDetails'][
                    'arrivalTime'], "Arrival Time not sync to MOCI"
                assert precruise_info['departureAirportCode'] == guest['flightDetails'][
                    'departureAirportCode'], "departureAirportCode not sync to MOCI"
                assert precruise_info['arrivalAirportCode'] == guest['flightDetails'][
                    'arrivalAirportCode'], "arrivalAirportCode not sync to MOCI"

                assert postcruise_info['airlineCode'] == guest['flightDetails'][
                    'airlineCode'], "airline code not sync to MOCI"
                assert postcruise_info['flightNumber'] == guest['flightDetails']['number'], "Flight number is not sync"
                assert postcruise_info['departureCity'] == guest['flightDetails'][
                    'departureCity'], "Departure city not sync to MOCI"
                assert postcruise_info['departureTime'] == guest['flightDetails'][
                    'departureTime'], "Departure Time not sync to MOCI"
                assert postcruise_info['arrivalCity'] == guest['flightDetails'][
                    'arrivalCity'], "Arrival City not sync to MOCI"
                assert postcruise_info['arrivalTime'] == guest['flightDetails'][
                    'arrivalTime'], "Arrival Time not sync to MOCI"
                assert postcruise_info['departureAirportCode'] == guest['flightDetails'][
                    'departureAirportCode'], "departureAirportCode not sync to MOCI"
                assert postcruise_info['arrivalAirportCode'] == guest['flightDetails'][
                    'arrivalAirportCode'], "arrivalAirportCode not sync to MOCI"

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(11777689)
    def test_26_validation_of_pregnancy_status_after_rts(self, guest_data):
        """
        Check the pregnancy Weeks Data should flow from RTS to MOCI
        :param guest_data:
        :return:
        """
        for guest in guest_data:
            _content = guest["details_content"]
            personal_info = _content['guestDetail']['personalInfo']
            if personal_info['firstName'].lower() == guest['FirstName'].lower() and guest['genderCode'] == 'Female':
                assert personal_info['additionalInfo']['pregnancyWeeks'] == guest[
                    'noOfWeeks'], "pregnancyStatus is not sync"

    @pytestrail.case(75588747)
    def test_27_edit_middle_name(self, config, rest_shore, guest_data, test_data):
        """
        Edit MOCI Guest Details by editing middle name
        :param config
        :param rest_shore:
        :param guest_data:
        :param test_data:
        :return:
        """
        url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), "moci/guests")
        param = {'page': 1}
        body = {"shipCode": config.ship.code,
                "voyageNumber": test_data['voyage']['id'],
                "fromDate": "", "toDate": "",
                "reviewLater": "INCLUDE", "statuses": ["PO", "P"]}
        _content = rest_shore.send_request(method="POST", url=url, params=param, json=body, auth="admin").content
        if len(_content['guests']) == 0:
            pytest.skip('No sailors available')
        test_data['m_guest_link'] = _content['guests'][00]['_links']['detailUrl']['href']
        url = test_data['m_guest_link']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        test_data['m_guestId'] = _content['guestDetail']['guestId']
        test_data['personalInfo'] = _content['guestDetail']['personalInfo']
        test_data['m_identificationDocumentInfo'] = _content['guestDetail']['identificationDocumentInfo']
        test_data['m_updateLink'] = _content['_links']['updateUrl']['href']
        middleName = generate_last_name()
        test_data['personalInfo']["middleName"] = middleName
        test_data['personalInfo']['photoDetail'][0]['status'] = 'APPROVED'
        test_data['m_identificationDocumentInfo']['identificationDocuments'][0]['status'] = 'APPROVED'
        if len(test_data['m_identificationDocumentInfo']['visaInfoList']['visaList']) != 0:
            test_data['m_identificationDocumentInfo']['visaInfoList']['visaList'][0]['status'] = 'APPROVED'
        else:
            pass
        url = test_data['m_guest_link']
        body = {"guestDetail": {"personalInfo": test_data['personalInfo'],
                                "identificationDocumentInfo": test_data['m_identificationDocumentInfo'],
                                "additionalComments": ""},
            "guestListFilter": {
                "shipCode": config.ship.code,
                "voyageNumber": test_data['voyage']['id'],
                "fromDate": "",
                "minDate": "",
                "toDate": "",
                "reviewLater": "INCLUDE",
                "statuses": ["A"],
                "guestListUrl": "https://int.gcpshore.virginvoyages.com/crew-bff/moci/guests?page=1"
            }}
        _content = rest_shore.send_request(method="PUT", url=url, json=body, auth="admin")
        url = test_data['m_updateLink']
        _content = rest_shore.send_request(method="GET", url=url, auth="admin").content
        is_key_there_in_dict('guestDetail', _content)
        test_data['m_guest_middleName'] = _content['guestDetail']['personalInfo']['middleName']
        assert test_data['m_guest_middleName'] == middleName, f"Guest MiddleName Mismatched !!"
        assert _content['status'] == 'A', "Not Approved"
