__author__ = 'sarvesh.singh'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.WAYFINDING
@pytest.mark.run(order=22)
class TestWayFinding:
    """
    Test Suite to test WayFinding
    """

    @pytestrail.case(9161563)
    def test_01_stop_already_running_simulations(self, config, rest_ship):
        """
        Stop already running Simulations
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/simulations/running")
        _content = rest_ship.send_request(method="GET", url=url, auth="bearer").content
        for simulation in _content:
            is_key_there_in_dict('__etag', simulation)
            is_key_there_in_dict('id', simulation)
            is_key_there_in_dict('runnerId', simulation)
            is_key_there_in_dict('startedTime', simulation)
            is_key_there_in_dict('tp', simulation)
            _id = simulation['id']
            start_time = int(simulation['startedTime'] / 1000)
            time_now = int(datetime.now(timezone('GMT')).strftime("%s"))
            if time_now - start_time > 60 * 60 * 24 * 7:
                logger.debug(
                    f"Simulation {_id} Started at {str(datetime.fromtimestamp(start_time))} > 1 Week, stopping")
                url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), f"v1/simulations/{_id}/stop")
                rest_ship.send_request(method="PUT", url=url, auth="basic")

    @pytestrail.case(9161564)
    def test_02_check_running_simulations_count(self, config, rest_ship):
        """
        Check if there are no more than 10 running simulations
        :param self:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/simulations/running")
        _content = rest_ship.send_request(method="GET", url=url, auth="bearer").content
        if len(_content) > 10:
            raise Exception(f"There are {len(_content)} Simulations already running, Cannot Continue !!")

    @pytestrail.case(9161565)
    def test_03_purge_stopped_simulations(self, config, rest_ship):
        """
        Purge all stopped simulations
        :param self:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/trash/empty")
        _content = rest_ship.send_request(method="DELETE", url=url, auth="bearer").content

    @pytestrail.case(186540)
    def test_04_get_available_trackables(self, config, test_data, rest_ship):
        """
        Get available track ables and pick a random one to be used, generate one if there is none.
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['wayFinder'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "trackables")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        required = {'major', 'minor', 'rfId', 'uuid', 'beaconId'}
        if "_embedded" in _content and len(_content['_embedded']['trackables']) > 0:
            trackables = _content['_embedded']['trackables']
            trackables = [x for x in trackables if not x['isDamaged'] and not x['isLost'] and not x['isDeleted'] and x[
                'trackableStatusCode'] == 'A' and len(required & set(x.keys())) == len(required)]
            if len(trackables) > 0:
                test_data['wayFinder'].update(random.choice([x for x in trackables]))
                return

        # In case we don't see any old trackable that can be used !!
        major = generate_random_number(low=0, high=99, include_all=True)
        minor = generate_random_number(low=0, high=99, include_all=True)
        rf_id = generate_random_number(low=0, high=99999, include_all=True)
        uu_id = generate_guid()
        test_data['wayFinder']['major'] = major
        test_data['wayFinder']['minor'] = minor
        test_data['wayFinder']['rfId'] = rf_id
        test_data['wayFinder']['uuid'] = uu_id
        test_data['wayFinder']['beaconId'] = f"{uu_id}:{major}:{minor}"

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(473)
    def test_05_assign_trackable_hydration(self, config, test_data, rest_ship, guest_data):
        """
        Assign trackable to a guest through hydration
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        test_data['wayFinder']['hostId'] = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.hydration'), "trackablehosts/bulk")
        _body = {
            "trackableHosts": [{
                "hostId": test_data['wayFinder']['hostId'], "hostIdType": "RG",
                "trackableAttributes": {
                    "beaconId": test_data['wayFinder']['beaconId'], "rfId": test_data['wayFinder']['rfId']
                }
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=_body, auth="crew").content
        for _host in _content['succeededTrackableHosts']:
            if _host['hostId'] == test_data['wayFinder']['hostId']:
                test_data['wayFinder']['trackableId'] = _host['trackableId']
                break
        else:
            raise Exception(f"ERROR: Trackable assignment to {test_data['wayFinder']['hostId']} Failed !!")

    @pytestrail.case(474)
    def test_06_retrieve_trackable_details(self, config, test_data, rest_ship):
        """
        Assign trackable to a guest through hyderation-service
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"trackableId": test_data['wayFinder']['beaconId'], "trackableIdType": "beaconId"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.hydration'), "trackablehosts")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        assert _content['trackableId'] == test_data['wayFinder']['beaconId'], "ERROR: Trackable beacon Id mismatch"
        assert _content['hostId'] == test_data['wayFinder'][
            'hostId'], "ERROR: ReservationGuest ID of guest does not match"

    @pytestrail.case(475)
    def test_07_create_simulation(self, config, test_data, rest_ship):
        """
        Create trackable simulation for the guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/simulations")
        _data = [
            (13329, 573), (13522, 693), (13728, 718), (13909, 766), (14139, 730), (14380, 657), (14441, 947),
            (14416, 1104), (14429, 1310), (14441, 1406), (14465, 1527), (14465, 1636), (14465, 1733), (14465, 1865),
            (14453, 1962), (14429, 2131), (14404, 2361), (14392, 2530), (14392, 2651), (14380, 2784), (14368, 2977),
            (14429, 3110), (14646, 3243), (14670, 3364), (14706, 3630), (14706, 3811), (14247, 3835), (14030, 3920),
            (13836, 3895), (13643, 3859), (13462, 3726), (13196, 3799), (13136, 3920), (12967, 3920), (12797, 3907),
            (12604, 3920), (12411, 3920), (12266, 3714), (12217, 3195), (12145, 2796), (12024, 2554), (11915, 2276),
            (12109, 2035), (12012, 1648), (12109, 1225), (12024, 971), (12387, 1189), (12592, 1382), (12749, 1588),
            (12942, 1745), (13112, 1914), (13353, 1672), (13402, 1430), (13559, 1056), (13293, 802)
        ]
        body = {
            "tp": "Simulation", "__etag": "697906", "name": "New_Test_simulation", "structure": "Scarlet Lady",
            "level": 1, "uuid": test_data['wayFinder']['uuid'],
            "guestsParties": [{
                "name": "Party1", "major": test_data['wayFinder']['major'],
                "minorStart": test_data['wayFinder']['minor'], "guestsNum": 1,
                "paceMs": 0.8, "guestStartDelayMs": 500,
                "points": [{"position": {"x": x, "y": y}, "lingerTimeMs": 500} for (x, y) in _data],
                "guests": [{
                    "minor": 0, "pos": {"x": 13160, "y": 3870}, "trackPos": {"x": 13501, "y": 3684},
                    "confRadiusCm": 100, "id": "0:0"
                }]
            }],
            "gaussianNoise": 0, "whiteNoise": 0, "visualGuestsNumPerParty": 1, "sensorCoverageCm": 8000,
            "readerReportIntervalMs": 1000, "showBleEvents": True, "showCameraEvents": True, "showFusionEvents": False,
            "viewSizeCutoff": 0.2, "lmDeviation": 0.6
        }

        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="basic").content
        test_data['wayFinder']['simulationId'] = _content['id']
        test_data['wayFinder']['__etag'] = _content['__etag']
        test_data['wayFinder']['guestName'] = _content['name']

    @pytestrail.case(476)
    def test_08_retrieve_created_simulation_details(self, config, test_data, rest_ship):
        """
        Retrieve simulation of guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/simulations")
        _content = rest_ship.send_request(method="GET", url=url, auth="basic").content
        for _data in _content:
            if _data['__etag'] == test_data['wayFinder']['__etag']:
                if _data['id'] == test_data['wayFinder']['simulationId']:
                    assert _data['name'] == test_data['wayFinder']['guestName'], "ERROR: guest name mismatch !!"
                    assert _data['uuid'] == test_data['wayFinder']['uuid'], "ERROR: UUID mismatch !!"
                    break
        else:
            raise Exception(f"ERROR: E-Tag: {test_data['wayFinder']['__etag']} not Found !!")

    @pytestrail.case(477)
    def test_09_start_simulation(self, config, test_data, rest_ship):
        """
        start simulation of guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'),
                      f"v1/simulations/{test_data['wayFinder']['simulationId']}/start")
        rest_ship.send_request(method="PUT", url=url, auth="basic")

    @pytestrail.case(478)
    def test_10_search_guest_location(self, config, test_data, rest_ship):
        """
        search Guest Location on the Deck from the simulation created
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.locationService'), "hostLocations/search")
        body = {
            "hosts": {"ids": [test_data['wayFinder']['hostId']], "type": "RG"},
            "include": ["location.coordinates"]
        }
        content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert content['_embedded']['hostLocations'] is not None, "ERROR: Location of Guest Not found!"

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(507097)
    def test_11_guest_venue(self, config, rest_ship):
        """
        Guest Ship Venue
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.locationconstruct'), "venues")
        params = {"onlyPublic": "1", "closestToSector": "true"}
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="bearer").content
        for _data in _content:
            is_key_there_in_dict('venue', _data)
            assert _data['venue'] is not None, " ERROR: Guests Venues Missing !!"

    @retry_when_fails(retries=2, interval=5)
    @pytestrail.case(507098)
    def test_12_guest_categories(self, config, rest_ship):
        """
        Get Guest categories
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.locationconstruct'), "categories")
        _content = rest_ship.send_request(method="GET", url=_url, auth="bearer").content
        for _data in _content:
            is_key_there_in_dict('category', _data)
            is_key_there_in_dict('venuesCount', _data)
            is_key_there_in_dict('crewVenuesCount', _data)
            is_key_there_in_dict('sailorVenuesCount', _data)
            assert _data['category'] is not None, "ERROR: Guests Categories Missing !!"

    @pytestrail.case(479)
    def test_13_stop_guest_simulation(self, config, test_data, rest_ship):
        """
        stop Guest simulation
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'),
                      f"v1/simulations/{test_data['wayFinder']['simulationId']}/stop")
        rest_ship.send_request(method="PUT", url=url, auth="basic")

    @pytestrail.case(480)
    def test_14_delete_simulation(self, config, test_data, rest_ship):
        """
        Delete complete Guest simulation
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'),
                      f"v1/simulations/{test_data['wayFinder']['simulationId']}")
        rest_ship.send_request(method="DELETE", url=url, auth="basic")

        # Verify Simulation has been deleted, as delete request is not returning any content
        url = urljoin(getattr(config.ship.contPath, 'url.path.gistask'), "v1/simulations")
        _content = rest_ship.send_request(method="GET", url=url, auth="basic").content
        for _data in _content:
            if _data['id'] == test_data['wayFinder']['simulationId']:
                raise Exception("ERROR: Simulation ID: {} not deleted !!")
