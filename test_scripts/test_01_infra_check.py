__author__ = 'piyush.kumar'
__maintainer__ = 'anshuman.goyal'

from virgin_utils import *


@pytest.mark.INFRA_CHECK
@pytest.mark.run(order=1)
class TestInfra:
    """
    Test Suite to test Infrastructure
    """

    @pytestrail.case(186203)
    def test_01_ship_info_calls(self, config, test_data, rest_ship, kubectl):
        """
        Verify Ship Info Calls
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        shipVersions = dict()
        failingCalls = dict()
        knownFailing = [
            'dxprulesengine/info', 'housekeepingreports/info',
            'https://application-integration.ship.virginvoyages.com/guest-ui/info', 'gistask-service/info',
            'entertainment-service/info', 'syncgatewayfeedersadmin/info', 'crew-bff/trackable-management/info',
            'https://elasticsearch-integration.ship.virginvoyages.com/info', 'wayfinding-bff/info'
        ]
        infoCalls = set()
        for item, url in config.ship.contPath.__dict__.items():
            if str(url).endswith('/') and str(url).startswith('https://'):
                infoCalls.add(f"{url}info")
        arguments = [{'method': 'GET', 'url': x, 'auth': None} for x in list(infoCalls)]
        results = kubectl.run_in_parallel(function=rest_ship.send_request, arguments=arguments, max_workers=30)
        for count, result in results.items():
            contPath = result['args']['url'].replace(config.ship.url, "")
            if contPath in knownFailing:
                continue
            elif result['exception']:
                logger.error(f"Ship Failing info call → {result['args']['url']}")
                failingCalls[contPath] = {'Failed': True, 'url': result['args']['url']}
            else:
                shipVersions[contPath] = {
                    'version': get_version(result['result'].content), 'url': result['args']['url']
                }

        allure.attach(
            json.dumps(shipVersions, sort_keys=True, indent=2),
            name='ship-versions.json', attachment_type=allure.attachment_type.JSON
        )
        test_data['shipVersions'] = shipVersions
        if len(failingCalls) > 0:
            raise Exception(f"Ship Side: Some info calls failed !! {failingCalls}")

    @pytestrail.case(186202)
    def test_02_shore_info_calls(self, config, test_data, rest_shore, kubectl):
        """
        Verify Shore Info Calls
        :param config:
        :param test_data:
        :param rest_shore:
        :param kubectl:
        :return:
        """
        shoreVersions = dict()
        failingCalls = dict()
        knownFailing = [
            '/reservation-bff/info', '/crew-bff/trackable-management/info', '/cabin-bff/info', '/wayfinding-bff/info',
            '/housekeepingreports/info', '/gistask-service/info', '/guest-ui/info', '/syncgatewayfeedersadmin/info',
            '/dxprulesengine/info', 'https://elasticsearch-int.gcpshore.virginvoyages.com/info', '/guest-bff/oci/info',
            '/housekeeping-service/info', '/stateroomcontrol-service/info'
        ]
        infoCalls = set()
        for item, url in config.shore.contPath.__dict__.items():
            if str(url).endswith('/') and str(url).startswith('https://'):
                infoCalls.add(f"{url}info")
        arguments = [{'method': 'GET', 'url': x, 'auth': None} for x in list(infoCalls)]
        results = kubectl.run_in_parallel(function=rest_shore.send_request, arguments=arguments, max_workers=30)
        for count, result in results.items():
            contPath = result['args']['url'].replace(config.shore.url, "")
            if contPath in knownFailing:
                continue
            elif result['exception']:
                logger.error(f"Shore Failing info call → {result['args']['url']}")
                failingCalls[contPath] = {'Failed': True, 'url': result['args']['url']}
            else:
                shoreVersions[contPath] = {
                    'version': get_version(result['result'].content), 'url': result['args']['url']
                }

        test_data['shoreVersions'] = shoreVersions
        allure.attach(
            json.dumps(shoreVersions, sort_keys=True, indent=2),
            name='shore-versions.json', attachment_type=allure.attachment_type.JSON
        )
        if len(failingCalls) > 0:
            raise Exception(f"Shore Side: Some info calls failed !! {failingCalls}")

    @pytestrail.case(760020)
    def test_03_compare_ship_shore_versions(self, test_data):
        """
        Function to compare ship and shore versions received from info calls
        :param test_data:
        :return:
        """
        for context, versionInfo in test_data['shoreVersions'].items():
            if context in test_data['shipVersions']:
                shoreVersion = versionInfo['version']
                shipVersion = test_data['shipVersions'][context]['version']
                assert shoreVersion == shipVersion, f"ERROR: Shore and Ship Versions for {context} mismatch !!"

        for context, versionInfo in test_data['shipVersions'].items():
            if context in test_data['shoreVersions']:
                shipVersion = versionInfo['version']
                shoreVersion = test_data['shoreVersions'][context]['version']
                assert shoreVersion == shipVersion, f"ERROR: Shore and Ship Versions for {context} mismatch !!"

    @pytest.mark.xfail(reason="DCP-94110")
    @pytestrail.case(3380948)
    def test_04_verify_ship_urls_accessible_from_dxp_core(self, config, rest_ship):
        """
        Validate all internal URL's working using dxp core (Ship Side)
        :param config:
        :param rest_ship:
        :return:
        """
        failed = get_failed_context_path_urls(base=config.ship, rest=rest_ship)
        known_failures = ['seawareBaseUrl', 'url.path.sailorAPI', 'url.path.elasticsearch']
        for _known in known_failures:
            if _known in failed:
                del failed[_known]
        if len(failed) > 0:
            save_allure(data=failed, name='shipContextPathsNotWorkingDxpCore.json')
            raise Exception(f"DXP-Core-Ship Side not able to access {failed}")

    @pytest.mark.xfail(reason="DCP-94110")
    @pytestrail.case(3380949)
    def test_05_verify_shore_urls_accessible_from_dxp_core(self, config, rest_shore):
        """
        Validate all internal URL's working using dxp core (Shore Side)
        :param config:
        :param rest_shore:
        :return:
        """
        failed = get_failed_context_path_urls(base=config.shore, rest=rest_shore)
        known_failures = ['sailorAppQRCodeUrl', 'url.path.sailorAPI']
        for _known in known_failures:
            if _known in failed:
                del failed[_known]
        if len(failed) > 0:
            save_allure(data=failed, name='shoreContextPathsNotWorkingDxpCore.json')
            raise Exception(f"DXP-Core-Shore Side not able to access {failed}")

    @pytestrail.case(697951)
    def test_06_validate_cms_magnolia(self, config, rest_shore, creds):
        """
        Validate CMS Magnolia
        :param config:
        :param rest_shore:
        :param creds:
        :return:
        """
        _iam_url = urljoin(config.shore.url, 'identityaccessmanagement-service/oauth/token?grant_type=password')
        params = {
            "username": getattr(creds.VIRGIN.cms, config.envMasked).username,
            "password": getattr(creds.VIRGIN.cms, config.envMasked).password
        }

        rest_shore.userToken = f'Basic {config.cms}'
        _content = rest_shore.send_request(method="POST", url=_iam_url, params=params, auth='user').content

        _api = '.rest/app-ui'
        if 'svc' in config.shore.url:
            url = f"{config.shore.url.strip('/svc')}/{_api}"
        else:
            url = f"{config.shore.url}/{_api}"
        rest_shore.userToken = f"bearer {_content['access_token']}"
        _content = rest_shore.send_request(method="GET", url=url, auth="user").content

    @pytestrail.case(4766956)
    def test_07_verify_config_ui_urls_accessible_from_dxp_core(self, config, ui_configs, rest_shore, rest_ship):
        """
        Validate URL's in Ship and Shore UI Configurations accessible by DXP Core
        :param config:
        :param ui_configs:
        :param rest_shore:
        :param rest_ship:
        :return:
        """
        failShip = get_failed_ui_urls(ui_configs.ship, config.ship.url, rest_ship)
        failShore = get_failed_ui_urls(ui_configs.shore, config.shore.url, rest_shore)
        failedBoth = []
        failedBothKnown = []
        knownIssues = [
            'url.path.elasticSearchServerAddress', 'voyage.xmlns', 'kafka.registry.server', 'url.path.cart',
            'magnoliaBaseURL', 'disney.com', 'cybersource.com', 'url.path.fexco.hpp'
        ]

        for shore in failShore:
            for ship in failShip:
                if (
                        shore['component'] == ship['component'] and
                        shore['configuration'] == ship['configuration'] and
                        shore['url'] == ship['url']
                ):
                    for known in knownIssues:
                        if known in shore['configuration'] or known in shore['url']:
                            failedBothKnown.append({
                                'component': shore['component'], 'configuration': shore['configuration'],
                                'rc': shore['rc'], 'url': shore['url']
                            })
                            break
                    else:
                        failedBoth.append({
                            'component': shore['component'], 'configuration': shore['configuration'],
                            'rc': shore['rc'], 'url': shore['url']
                        })

        if len(failedBothKnown) > 0:
            save_allure(data=failedBoth, name='Known-Links-Not-Working-Both-Sides.json')

        if len(failedBoth) > 0:
            save_allure(data=failedBoth, name='Links-Not-Working-Both-Sides.json')
            raise Exception(f"DXP-Core not able to access {failedBoth}")

    @pytestrail.case(4766958)
    def test_08_fetch_ui_config_invalid_urls(self, ui_configs):
        """
        Get all Invalid URL's in UI Configs (Ship & Shore Side)
        :param ui_configs:
        :return:
        """
        ignored = [
            "url.path.fidelio", "seawareUrl", "seawareBaseUrl", "seawareOtaUrl", "seawareXmlApiUrl",
            "url.path.seawareOTA",
        ]
        bad = {'SHIP': [], 'SHORE': []}
        for component in ui_configs.ship.finalData.keys():
            for configuration, url in ui_configs.ship.finalData[component].items():
                if str(url).startswith('http://'):
                    if 'VALUE_NOT_AVAILABLE' in url or 'VALUE_NOT_APPLICABLE' in url:
                        continue
                    elif configuration in ignored:
                        continue
                    else:
                        bad['SHIP'].append({"component": component, "configuration": configuration, "url": url})

        for component in ui_configs.shore.finalData.keys():
            for configuration, url in ui_configs.shore.finalData[component].items():
                if str(url).startswith('http://'):
                    if 'VALUE_NOT_AVAILABLE' in url or 'VALUE_NOT_APPLICABLE' in url:
                        continue
                    elif configuration in ignored:
                        continue
                    else:
                        bad['SHORE'].append({"component": component, "configuration": configuration, "url": url})

        if len(bad['SHIP']) > 0 or len(bad['SHORE']) > 0:
            save_allure(data=bad, name='uiConfigBadLinks.json')
            raise Exception("UI Config has some invalid URLs See uiConfigBadLinks.json")
