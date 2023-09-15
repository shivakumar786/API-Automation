__author__ = "HT"

from virgin_utils import *
import datetime

@pytest.mark.xfail(reason="DCP-114159")
@pytest.mark.CORE_COUCH_COUNTS_MATCH
@pytest.mark.run(order=38)
class TestCoreCouchCounts:
    """
    Test Suite to Test Core And Couch Counts
    """

    @pytestrail.case(24938092)
    def test_01_guest_onboard_count(self, config, test_data, couch, verification, db_core):
        """
         Check Core and Couch guest Onboard count.
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Onboard guests counts on couch.
        embarkdate = test_data['embarkDate'][:10]
        data = verification.couch_queries['guest_onboard'].format(config.ship.couch.bucket, embarkdate)
        query = f"query?Statement={data}"
        url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=url, auth='basic', timeout=60).content
        couch_onboard_guest_count = _content['results'][0]['$1']

        # Onboard guests counts on Core.
        data = verification.sql['guest_core_count']['onboard']
        query = data.format(embarkdate)
        core_onboard_guest_count = db_core.ship.run_and_fetch_data(query=query)[0]['count']

        if couch_onboard_guest_count == core_onboard_guest_count:
            pass
        else:
            raise Exception("on-board guest count does not matched from core and couch")

    @pytestrail.case(24938093)
    def test_02_guest_checked_in_count(self, config, test_data, couch, verification, db_core):
        """
        Check Core and Couch guest checked-in count.
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Checked-in guests counts on couch.
        embarkdate = test_data['embarkDate'][:10]
        data = verification.couch_queries['guest_checkin'].format(config.ship.couch.bucket, embarkdate)
        query = f"query?Statement={data}"
        url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=url, auth='basic', timeout=60).content
        couch_check_in_guest_count = _content['results'][0]['$1']

        # Checked-in guests counts on Core.
        data = verification.sql['guest_core_count']['check_in']
        query = data.format(embarkdate)
        core_check_in_guest_count = db_core.ship.run_and_fetch_data(query=query)[0]['count']
        if couch_check_in_guest_count == core_check_in_guest_count:
            pass
        else:
            raise Exception("guest checked-in count not matched between core and couch ")

    @pytestrail.case(24938094)
    def test_03_guest_leaving_count(self, config, couch, verification, db_core):
        """
        Check Core and Couch guest leaving.
        :param config:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Today's leaving guests counts on couch.
        currentdate = datetime.date.today()
        data = verification.couch_queries['guest_leaving'].format(config.ship.couch.bucket, currentdate)
        query = f"query?Statement={data}"
        url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=url, auth='basic', timeout=60).content
        couch_leaving_guest_count = _content['results'][0]['$1']

        # Today's leaving guests counts on core.
        data = verification.sql['guest_core_count']['leaving']
        query = data.format(currentdate)
        core_leaving_guest_count = db_core.ship.run_and_fetch_data(query=query)[0]['count']
        if couch_leaving_guest_count == core_leaving_guest_count:
            pass
        else:
            raise Exception("guest leaving count not matching from core and couch ")

    @pytest.mark.xfail(reason='DCP-120203')
    @pytestrail.case(24938095)
    def test_04_crew_onboard_count(self, config, test_data, couch, verification, db_core):
        """
        Check Core and Couch Crew Onboard count.
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Onboard Crew counts on Couch.
        embarkdate = test_data['embarkDate'][:10]
        data = verification.couch_queries['crew_onboard'].format(config.ship.couch.bucket)
        query = f"query?Statement={data}"
        url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=url, auth='basic', timeout=60).content
        couch_onboard_crew_count = _content['results'][0]['$1']

        # Onboard Crew counts on Core.
        data = verification.sql['crew_core_count']['onboard']
        query = data.format(embarkdate)
        core_onboard_crew_count = len(db_core.ship.run_and_fetch_data(query=query))
        if couch_onboard_crew_count == core_onboard_crew_count:
            pass
        else:
            raise Exception("crew on-board count not matched from core and couch")

    @pytestrail.case(24938098)
    def test_05_crew_checkin_count(self, config, test_data, couch, verification, db_core):
        """
        Check Core and Couch crew leaving.
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Today's leaving Crew counts on Couch.
        embarkdate = test_data['embarkDate'][:10]
        data = verification.couch_queries['crew_checkin'].format(config.ship.couch.bucket)
        query = f"query?Statement={data}"
        _url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=_url, auth='basic', timeout=60).content
        couch_leaving_crew_count = _content['results'][0]['$1']

        # Today's leaving Crew counts on core.

        data = verification.sql['crew_core_count']['check_in']
        query = data.format(embarkdate)
        core_leaving_crew_count = len(db_core.ship.run_and_fetch_data(query=query))
        if couch_leaving_crew_count == core_leaving_crew_count:
            pass
        else:
            raise Exception("crew check-in count not matched from core and couch")

    @pytestrail.case(24938096)
    def test_06_crew_ashore_count(self, config, couch, verification, db_core):
        """
        Check Core and Couch crew ashore.
        :param config:
        :param couch:
        :param verification:
        :param db_core:
        :return:
        """
        # Ashore crew counts on couch.
        data = verification.couch_queries['crew_ashore'].format(config.ship.couch.bucket)
        query = f"query?Statement={data}"
        _url = urljoin(config.ship.couch.url, query)
        _content = couch.send_request(method="GET", url=_url, auth='basic', timeout=60).content
        couch_crew_ashore_count = _content['results'][0]['$1']

        # Ashore crew counts on Core.
        query = verification.sql['crew_core_count']['ashore']
        core_crew_ashore_count = len(db_core.ship.run_and_fetch_data(query=query))
        if couch_crew_ashore_count == core_crew_ashore_count:
            pass
        else:
            raise Exception("crew ashore count not matched between core and couch")

    @pytestrail.case(30698394)
    def test_07_guest_reservation_count(self, config, test_data, rest_ship):
        """
        check the reservation count on shore and ship side for current voyage
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        # shore reservation counts.
        _url = urljoin(getattr(config.shore.contPath, 'url.path.dxpcore'), 'reservationguests/search')
        param = {"size": "99999"}
        body = {
            "embarkDate": test_data['embarkDate'],
            "debarkDate": test_data['debarkDate']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, params=param, auth='bearer').content
        shore_reservation_count = len(_content['_embedded']['reservationGuestDetailsResponses'])

        # ship reservation counts
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservationguests/search')
        param = {"size": "99999"}
        body = {
            "embarkDate": test_data['embarkDate'],
            "debarkDate": test_data['debarkDate']
        }
        content = rest_ship.send_request(method="POST", url=_url, json=body, params=param, auth='bearer').content
        ship_reservation_count = len(content['_embedded']['reservationGuestDetailsResponses'])
        if shore_reservation_count == ship_reservation_count:
            pass
        else:
            raise Exception("ship and shore reservation counts mismatch !!")

    @pytestrail.case(35081797)
    def test_08_visitor_approved_count(self, config, test_data, rest_ship, couch, verification, rest_shore):
        """
        To check the visitor approved count in core shore, core ship and couch ship.
        :param rest_ship:
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :return:
        """
        test_data['core_ship'] = {}
        test_data['core_shore'] = {}
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        content = rest_ship.send_request(url=url, method='POST', json=body, auth='bearer').content
        test_data['core_ship']['approved_visitor_ship'] = content['dashboard']['visitorEmbarkStats']['approved']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        _body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        _content = rest_shore.send_request(url=_url, method='POST', json=_body, auth='bearer').content
        test_data['core_shore']['approved_visitor_shore'] = _content['dashboard']['visitorEmbarkStats']['approved']
        to_date = test_data['aci']['shipDate']
        data = verification.couch_queries['visitor_approved'].format(config.ship.couch.bucket, to_date)
        query = f"query?Statement={data}"
        to_url = urljoin(config.ship.couch.url, query)
        to_content = couch.send_request(method="GET", url=to_url, auth='basic', timeout=60).content
        assert test_data['core_shore']['approved_visitor_shore'] == test_data['core_ship']['approved_visitor_ship'] == \
               to_content['results'][0][
                   '$1'], "Visitor approved counts are not matching in core shore, core ship and couch ship."

    @pytestrail.case(35103146)
    def test_09_visitor_rejected_count(self, config, test_data, rest_ship, rest_shore, verification, couch):
        """
        To check the visitor rejected count in core shore, core ship and couch ship.
        :param rest_shore:
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        content = rest_ship.send_request(url=url, method='POST', json=body, auth='bearer').content
        test_data['core_ship']['rejected_visitor_ship'] = content['dashboard']['visitorEmbarkStats']['rejected']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        _body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        _content = rest_shore.send_request(url=_url, method='POST', json=_body, auth='bearer').content
        test_data['core_shore']['rejected_visitor_shore'] = _content['dashboard']['visitorEmbarkStats']['rejected']
        to_date = test_data['aci']['shipDate']
        data = verification.couch_queries['visitor_rejected'].format(config.ship.couch.bucket, to_date)
        query = f"query?Statement={data}"
        to_url = urljoin(config.ship.couch.url, query)
        to_content = couch.send_request(method="GET", url=to_url, auth='basic', timeout=60).content
        assert test_data['core_shore']['rejected_visitor_shore'] == test_data['core_ship']['rejected_visitor_ship'] == \
               to_content['results'][0][
                   '$1'], "Visitor approved counts are not matching in core shore, core ship and couch ship."

    @pytestrail.case(35103147)
    def test_10_visitor_pending_count(self, config, test_data, rest_shore, rest_ship, verification, couch):
        """
        To check the visitor pending count in core shore, core ship and couch ship.
        :param rest_shore:
        :param config:
        :param test_data:
        :param couch:
        :param verification:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        content = rest_ship.send_request(url=url, method='POST', json=body, auth='bearer').content
        test_data['core_ship']['pending_visitor_ship'] = content['dashboard']['visitorEmbarkStats']['approvalPendingCount']
        _url = urljoin(getattr(config.shore.contPath, 'url.path.crewbff'), '/crew-embarkation-admin/dashboard')
        _body = {
            "shipCode": "SC",
            "fromDate": f"{test_data['embarkDate']}T00:00:00",
            "toDate": f"{test_data['debarkDate']}T00:00:00",
            "voyageNumber": test_data['voyageNumber'],
            "shipTime": f"{test_data['aci']['shipDate']}T06:07:20",
            "status": [
                "COMPLETED",
                "ASHORE",
                "ONBOARD"
            ],
            "statusTypeCode": [
                "TC",
                "BS"
            ]
        }
        _content = rest_shore.send_request(url=_url, method='POST', json=_body, auth='bearer').content
        test_data['core_shore']['pending_visitor_shore'] = _content['dashboard']['visitorEmbarkStats']['approvalPendingCount']
        to_date = test_data['aci']['shipDate']
        data = verification.couch_queries['visitor_pending'].format(config.ship.couch.bucket, to_date)
        query = f"query?Statement={data}"
        to_url = urljoin(config.ship.couch.url, query)
        to_content = couch.send_request(method="GET", url=to_url, auth='basic', timeout=60).content
        assert test_data['core_ship']['pending_visitor_ship'] == test_data['core_shore'][
            'pending_visitor_shore'] == to_content['results'][0][
                   '$1'], "Visitor approved counts are not matching in core shore, core ship and couch ship."
