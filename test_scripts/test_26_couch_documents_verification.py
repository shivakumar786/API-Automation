__author__ = "vishesh.t"
__maintainer__ = 'vishal.gupta'

from virgin_utils import *
import concurrent


@pytest.mark.COUCH_DOC_VERIFICATION
@pytest.mark.run(order=27)
class TestCouchVerification:
    """
    Test Suite to Verify Couch Document
    """

    @pytest.mark.skip(reason='DCP-114776')
    @pytestrail.case(24986867)
    def test_01_verify_master_data_document(self, config, couch):
        """
        To verify Documents with master data
        :param config:
        :param couch:
        :return:
        """
        documents = {
            "AddressType", "Airline", "Airport", "AlertCode", "AlertType", "AstrologicalSign", "Brands",
            "City", "Country", "CountryCodeMap", "Department", "Genders", "HealthQuestion", "Language",
            "LoyaltyLevel", "PaymentMode", "Ports", "Preference", "PreferenceValue", "Relation",
            "RentalCarAgency", "Roles", "RulesDEX", "Ships", "SpecialNeedType", "State", "Title",
            "TransportationType", "TravelOption", "VisaType", "VisitBoardingType", "VisitorDepartment", "VisitorType",
            "VisitorVisitStatus"
        }
        fail_doc = []
        url = urljoin(config.ship.couch.url, 'query')

        def func_parallel(document):
            query = f'select meta().id, * from {config.ship.couch.bucket} where type = "{document}" limit 1'
            params = {'Statement': query}
            _content = couch.send_request(method='GET', url=url, params=params, auth='basic', timeout=120).nt
            return _content

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            thread_executor = {
                executor.submit(func_parallel, document): document for document in documents
            }
            for completed_thread in concurrent.futures.as_completed(thread_executor):
                doc = thread_executor[completed_thread]
                try:
                    if completed_thread.exception():
                        raise Exception(completed_thread.exception())
                    content = completed_thread.result()
                    if len(content.results) == 0:
                        fail_doc.append(doc)
                except (Exception, ValueError) as exc:
                    logger.error(f"Failed for document {doc}")
                    fail_doc.append(doc)
                    continue

        if len(fail_doc) != 0:
            raise Exception(f"These {fail_doc} documents are not created on couchbase !")

    @pytestrail.case(24986868)
    @retry_when_fails(retries=120, interval=5)
    def test_02_verify_guest_person_alert(self, config, rest_ship, guest_data, verification):
        """
        To verify guest person alert Document.
        :param config:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/GuestPersonAlert::{guest_data[0]['reservationGuestId']}")
        _content = rest_ship.send_request(method="GET", url=url, auth=None, timeout=60).content
        for _key in verification.guest_person_alert_doc:
            is_key_there_in_dict(_key, _content)
        assert len(_content['PersonAlerts']) != 0, "ERROR: Guest Person Alert Document is not created !!"

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(24987997)
    def test_03_verify_boarding_group_voyage(self, test_data, config, rest_ship):
        """
        To verify the boarding group voyage document.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/BoardingGroupVoyage::{test_data['voyageId']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        if len(_content) == 0:
            raise Exception("Boarding Group Voyage document is not created !!")

    @retry_when_fails(retries=120, interval=5)
    @pytestrail.case(24987999)
    def test_04_verify_guest_all_documents(self, config, rest_ship, guest_data):
        """
        To verify the guest Documents
        :param config:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        documents = [
            "GuestMessage", "GuestPayForDetail", "GuestPersonAlert",
            "GuestPersonalInformation", "GuestPostCruise", "GuestPreCruise", "GuestSecurityImage",
            "GuestStatus", "TrackableInfo"
        ]
        fail_doc = []
        for count, guest in enumerate(guest_data):
            for document in documents:
                url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                              f"{config.ship.couch.bucket}/{document}::{guest_data[0]['reservationGuestId']}")
                _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
                if len(_content) != 0:
                    if 'Identifications' in _content:
                        if len(_content['Identifications']) == 0:
                            fail_doc.append(document)
                    elif 'Messages' in _content:
                        if len(_content['Messages']) == 0:
                            fail_doc.append(document)
                    elif 'PayForDetails' in _content:
                        if len(_content['PayForDetails']) == 0:
                            fail_doc.append(document)
                    elif 'PersonAlerts' in _content:
                        if len(_content['PersonAlerts']) == 0:
                            fail_doc.append(document)
                    elif 'PersonAlerts' in _content:
                        if len(_content['PersonAlerts']) == 0:
                            fail_doc.append(document)
                    elif 'PostCruiseDetails' in _content:
                        if len(_content['PostCruiseDetails']) == 0:
                            fail_doc.append(document)
                    elif 'PreCruiseDetails' in _content:
                        if len(_content['PreCruiseDetails']) == 0:
                            fail_doc.append(document)
                    elif '_attachments' in _content:
                        if len(_content['_attachments']) == 0:
                            fail_doc.append(document)
                else:
                    fail_doc.append(document)
                break
        if len(fail_doc) != 0:
            raise Exception(f"These {fail_doc} documents are not created on couchbase !")

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(27802576)
    def test_05_verify_team_member_documents(self, test_data, config, rest_ship):
        """
        To verify the Team Member Documents.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/TeamMember::{test_data['embarkSupervisorShip']['crewDetail']['personId']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        assert len(_content) != 0, "The team member document is not created in couch !!"

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(24988000)
    def test_06_verify_team_member_details_document(self, test_data, config, rest_ship):
        """
        To verify the Team Member Details Documents.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/TeamMemberDetails::{test_data['embarkSupervisorShip']['crewDetail']['personId']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        assert len(_content) != 0, "The team member document is not created in couch !!"

    @pytestrail.case(24988001)
    def test_07_verify_ship_time_document(self, test_data, config, rest_ship, guest_data):
        """
        To verify the Ship Time Documents.
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/ShipTime::{test_data['shipCode']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        assert len(_content) != 0, "The team member document is not created in couch !!"

    @retry_when_fails(retries=30, interval=5)
    @pytestrail.case(24988002)
    def test_08_verify_team_member_status_document(self, test_data, config, rest_ship):
        """
        To verify the Team Member Status Documents.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/TeamMemberStatus::{test_data['embarkSupervisorShip']['crewDetail']['personId']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        assert len(_content) != 0, "The team member document is not created in couch !!"

    @pytestrail.case(24988003)
    def test_09_verify_voyage_documents(self, test_data, config, rest_ship):
        """
        To verify the voyage Documents.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.couchbase'),
                      f"{config.ship.couch.bucket}/Voyage::{test_data['embarkSupervisorShip']['voyageId']}")
        _content = rest_ship.send_request(method="GET", url=url, timeout=60).content
        assert len(_content) != 0, "The team member document is not created in couch !!"

    @pytest.mark.xfail(reason="DCP-114159")
    @pytestrail.case(26570921)
    def test_10_verify_guest_total_documents(self, config, couch):
        """
        To verify Validating all Couch docs for guests.
        :param config:
        :param couch:
        :return:
        """
        documents = {
            "GuestPersonalInformation", "GuestIdentification", "GuestStatus"
        }
        counts = dict()
        url = urljoin(config.ship.couch.url, 'query')
        for document in documents:
            query = f'Select count(*) from {config.ship.couch.bucket} where type = "{document}" limit 1'
            params = {'Statement': query}
            _content = couch.send_request(method='GET', url=url, params=params, auth='basic',
                                          timeout=120).content
            counts[f'{document}'] = _content['results'][0]['$1']

        if counts['GuestPersonalInformation'] != counts['GuestIdentification'] \
                or counts['GuestIdentification'] != counts['GuestStatus'] or \
                counts['GuestPersonalInformation'] != counts['GuestStatus']:
            raise Exception("ERROR: Guest Documents Counts Mismatch !!")
