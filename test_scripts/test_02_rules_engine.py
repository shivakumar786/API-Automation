__author__ = 'piyush.kumar'

from virgin_utils import *


@pytest.mark.RULE_ENGINE
@pytest.mark.run(order=2)
class TestRuleEngine:
    """
    Test Suite to test Rule Engine
    """

    @pytestrail.case(772916)
    def test_01_shore_get_version(self, config, test_data, rest_shore):
        """
        Get Version
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        test_data['ruleEngine'] = {"ship": dict(), "shore": dict()}
        url = (getattr(config.shore.contPath, 'dxp.rules.jar.server.url.check.version'))
        _content = rest_shore.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('LatestVersionNumber', _content)
        test_data['ruleEngine']['shore']['LatestVersionNumber'] = _content['LatestVersionNumber']

    @pytestrail.case(772917)
    def test_02_shore_download_jar_file(self, config, test_data, rest_shore):
        """
        Download Jar File
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        version = test_data['ruleEngine']['shore']['LatestVersionNumber']
        params = {
            'version': version
        }
        url = urljoin(config.shore.url, "/dxprulesengine/api/rules")
        response = rest_shore.send_request(method="GET", url=url, params=params, stream=True)
        if response.content is None:
            raise Exception('Empty Response')
        if response.headers.get('content-type', None) != 'application/jar':
            raise Exception('JAR File is not there in Response')
        if response.headers.get('content-length', None) == 0:
            raise Exception('There is no data in JAR file')

    @pytestrail.case(772918)
    def test_03_shore_download_dex_file(self, config, test_data, rest_shore):
        """
        Download Dex File
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        version = test_data['ruleEngine']['shore']['LatestVersionNumber']
        params = {
            'version': version,
            'fileType': 'dex'
        }
        url = urljoin(config.shore.url, "/dxprulesengine/api/rules")
        response = rest_shore.send_request(method="GET", url=url, params=params, stream=True)
        if response.content is None:
            raise Exception('Empty Response')
        if response.headers.get('content-type', None) != 'application/dex':
            raise Exception('DEX File is not there in Response')
        if response.headers.get('content-length', None) == 0:
            raise Exception('There is no data in DEX file')

    @pytestrail.case(772919)
    def test_04_ship_get_version(self, config, test_data, rest_ship):
        """
        Get Version
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, "/dxprulesengine/api/rules/version")
        _content = rest_ship.send_request(method="GET", url=url, auth="basic").content
        is_key_there_in_dict('LatestVersionNumber', _content)
        test_data['ruleEngine']['ship']['LatestVersionNumber'] = _content['LatestVersionNumber']

    @pytestrail.case(772920)
    def test_05_ship_download_jar_file(self, config, test_data, rest_ship):
        """
        Download Jar File
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _version = test_data['ruleEngine']['ship']['LatestVersionNumber']
        params = {'version': _version}
        url = urljoin(config.ship.url, "/dxprulesengine/api/rules")
        response = rest_ship.send_request(method="GET", url=url, params=params, stream=True)
        if response.content is None:
            raise Exception('Empty Response')
        if response.headers.get('content-type', None) != 'application/jar':
            raise Exception('JAR File is not there in Response')
        if response.headers.get('content-length', None) == 0:
            raise Exception('There is no data in JAR file')

    @pytestrail.case(772921)
    def test_06_ship_download_dex_file(self, config, test_data, rest_ship):
        """
        Download Dex File
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        version = test_data['ruleEngine']['ship']['LatestVersionNumber']
        params = {'version': version, 'fileType': 'dex'}
        url = urljoin(config.ship.url, "/dxprulesengine/api/rules")
        response = rest_ship.send_request(method="GET", url=url, params=params, stream=True)
        if response.content is None:
            raise Exception('Empty Response')
        if response.headers.get('content-type', None) != 'application/dex':
            raise Exception('DEX File is not there in Response')
        if response.headers.get('content-length', None) == 0:
            raise Exception('There is no data in DEX file')

    @pytestrail.case(772922)
    def test_07_shore_login(self, config, rest_shore):
        """
        Verify Shore Login
        :param config:
        :param rest_shore:
        :return:
        """
        url = urljoin(config.shore.url, "/dxprulesengine/")
        body = {"UserName": "admin", "Password": "admin"}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="basic").content
        if _content is None:
            raise Exception('Rules data not available on shore side')

    @pytestrail.case(772923)
    def test_08_ship_login(self, config, rest_ship):
        """
        Verify Ship Login
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, "/dxprulesengine/")
        body = {"UserName": "admin", "Password": "admin"}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        if _content is None:
            raise Exception('Rules data not available on ship side')

    @pytestrail.case(5791744)
    def test_09_validate_rules_both_ship_and_shore_side(self, config, rest_shore, rest_ship):
        """
        Validate Rules in Rules Engine both Ship and Shore Side
        :param config:
        :param rest_shore:
        :return:
        """
        rules = [
            'VoyageDetails', 'GuestOnlineCheckInInformation', 'GuestPaymentInformation',
            'GuestPersonalInformation', 'GuestIdentification', 'PassportIdentification',
            'BirthCertificateIdentification', 'AlienResidentCertificateIdentification',
            'DrivingLicenceIdentification', 'VisaIdentification', 'GuestTravelInformation',
            'GuestTravelInformation', 'GuestPortArrivalInformation', 'GuestCruiseContract',
            'MinorDebarkationAuthorization', 'ChildActivityRegistration', 'GuestPaymentInformation'
        ]
        body = []
        for rule in rules:
            body.append({"className": f"com.decurtis.dxp.rules.entities.{rule}", "request": None})
        for side in [config.shore]:
            url = urljoin(getattr(side.contPath, 'url.path.dxpcore'), "oci/validate")
            _content = rest_shore.send_request(method="POST", url=url, json=body, auth="bearer").content
            is_key_there_in_dict('DEFAULT', _content)
            if len(_content['DEFAULT']) == 0:
                raise Exception("No Rules Returned !!")
            for rule in _content['DEFAULT']:
                if str(rule['entityName']).split('-')[0] not in rules:
                    raise Exception(f"Rule {rule['entityName']} has not been requested !!")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(30139565)
    def test_10_validate_passport_as_primary_document(self, rest_shore, test_data, config, rest_ship):
        """
        Check if passport is appearing as primary document in downloaded jar file response.
        :param test_data:
        :param rest_shore:
        :param config:
        :param rest_ship:
        :return:
        """
        for side in [config.ship.url, config.shore.url]:
            url = urljoin(side, f"/dxpcore/oci/validate")
            body = [
                {
                    "className": "com.decurtis.dxp.rules.entities.VoyageDetails",
                    "request": {
                        "embarkCountry": "US",
                        "debarkCountry": "US",
                        "embarkPort": "",
                        "debarkPort": "",
                        "isClosedLoop": False,
                        "countryVisited": "US"
                    }
                },
                {
                    "className": "com.decurtis.dxp.rules.entities.VoyageDetails",
                    "request": {}
                },
                {
                    "className": "com.decurtis.dxp.rules.entities.GuestIdentification",
                    "request": {
                        "citizenship": "US",
                        "currentDate": str(datetime.utcnow().isoformat())+"Z",
                        "documentCollection": [
                            {}
                        ]
                    }
                },
                {
                    "className": "com.decurtis.dxp.rules.entities.GuestPersonalInformation",
                    "request": {}
                }
            ]
        content = rest_ship.send_request(method="POST", url=url, json=body, auth="bearer").content
        is_key_there_in_dict("DEFAULT", content)
        test_data['ruleEngine']['identificationDocument'] = content
        for _items in test_data['ruleEngine']['identificationDocument']['DEFAULT']:
            for _key in _items:
                if _items[_key] == "GuestIdentification-identificationDocument":
                    if 'fieldOptions' in _items:
                        for document in _items['fieldOptions']:
                            assert document == "P", "Passport as primary document is not coming through rules"
                            break
                break
            break
