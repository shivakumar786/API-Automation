__author__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.MOCI_APPROVED
@pytest.mark.run(order=4)
class TestMoci:
    """
    Suite to test MOCI
    """

    @retry_when_fails(retries=40, interval=5)
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
            if config.envMasked == "DEV":
                couch_url = urljoin(config.shore.url,
                                    f"syncgatewayfeedersadmin/reporting/ReservationGuestModeration::{_res}")
            elif config.envMasked == "INTEGRATION":
                couch_url = urljoin(config.shore.url,
                                    f"syncgateway-admin/reporting/ReservationGuestModeration::{_res}")
            else:
                couch_url = urljoin(config.shore.url,
                                    f"syncgateway-admin/reporting/ReservationGuestModeration::{_res}")
            _content = rest_shore.send_request(method="GET", url=couch_url, auth="basic").content
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

    @pytestrail.case(122)
    def test_03_dashboard_ship(self, test_data, rest_shore):
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
            is_key_there_in_dict('voyageDetails', ship)
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

    @retry_when_fails(retries=40, interval=5)
    @pytestrail.case(117)
    def test_04_get_moci_guests(self, config, test_data, rest_shore, guest_data):
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
    def test_05_check_all_guests_in_pending_before_approving(self, rest_shore, guest_data):
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
            for _count, _item in enumerate(_data['identificationInfo']['visas']):
                assert _item['status'] == "PENDING", "ERROR: Visa Not in Pending !!"
            # Verify Passport Document(s)
            _item = _data['identificationInfo']['passport']
            assert _item['status'] == "PENDING", "ERROR: Passport Not in Pending !!"

    @pytestrail.case(179)
    def test_06_search(self, config, test_data, rest_shore, guest_data):
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
                    is_key_there_in_dict('href', _data['_links']['requiredFieldsUrl'])
                    is_key_there_in_dict('href', _data['_links']['detailUrl'])
                    guest_data[count]['DetailUrl'] = _data['_links']['detailUrl']['href']
                    guest_data[count]['RequiredFieldsUrl'] = _data['_links']['requiredFieldsUrl']['href']
                    break

    @pytestrail.case(118)
    def test_07_guest_details_virgin(self, rest_shore, guest_data):
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

    @pytestrail.case(116)
    def test_08_validate(self, rest_shore, guest_data):
        """
        Validate MOCI Guest Details
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            url = guest['ValidateUrl']
            body = {"guestDetail": guest['ShoreGuestDetail']}
            rest_shore.send_request(method="POST", url=url, json=body, auth="admin")

    @pytestrail.case(92)
    def test_09_approve_reject_guests(self, rest_shore, guest_data):
        """
        Validate MOCI Guest Details
        :param rest_shore:
        :param guest_data:
        :return:
        """
        for count, guest in enumerate(guest_data):
            _content = rest_shore.send_request(method="GET", url=guest['DetailUrl'], auth="admin").content
            _data = _content['guestDetail']

            # Approve/Reject Photo
            for _count, _ in enumerate(_data['personalInfo']['photoDetail']):
                _data['personalInfo']['photoDetail'][_count]['status'] = "APPROVED"

            # Approve (always) Visa
            for _count, _ in enumerate(_data['identificationInfo']['visas']):
                _data['identificationInfo']['visas'][_count]['status'] = "APPROVED"

            # Approve (always) Passport
            _data['identificationInfo']['passport']['status'] = "APPROVED"

            to_delete = ['guestId', 'birthCertificate', 'drivingLicence', 'alienResidentCard', 'visas',
                         'expectedVisaCountryList', 'reservationNumber', 'reviewLaterFlag', 'paymentInfo', 'travelInfo',
                         'contractInfo', 'reservationId', 'identificationDocumentInfo', '']
            delete = [key for key in _data if key in to_delete]
            for key in delete: del _data[key]
            rest_shore.send_request(method="PUT", url=guest['UpdateUrl'], json={"guestDetail": _data}, auth="admin")

    @pytestrail.case(75588747)
    def test_10_edit_middle_name(self, config, rest_shore, guest_data, test_data):
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
