__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.ARS_ADMIN_REPORTS
@pytest.mark.run(order=31)
class TestArsAdminReports:
    """
    Test Suite to test ARS Admin Reports
    """

    @pytestrail.case(1134981)
    def test_01_reports_filter_data(self, config, request, test_data, rest_ship):
        """
        Get Reports Filter Data
        :param request:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['arsReports'] = {}
        test_data['arsReports']['ActivityGroupCode'] = []
        test_data['arsReports']['ActivityName'] = []
        test_data['arsReports']['VendorName'] = []
        test_data['arsReports']['PortCode'] = []
        test_data['arsReports']['status'] = []
        _file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/ars_report_data.json')
        with open(_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/filterdata/", test_data['voyageNumber'])
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content)
        for status in _content['Status']:
            test_data['arsReports']['status'].append(status['Status'])
            for _key in _ship_data['Status']:
                is_key_there_in_dict(_key, status)
        for port in _content['PortData']:
            test_data['arsReports']['PortCode'].append(port['code'])
            for _key in _ship_data['PortData']:
                is_key_there_in_dict(_key, port)
        for activity in _content['Activities']:
            test_data['arsReports']['ActivityGroupCode'].append(activity['ActivityGroupCode'])
            for _key in _ship_data['Activities']:
                is_key_there_in_dict(_key, activity)
            for activity_list in activity['ActivityList']:
                test_data['arsReports']['ActivityName'].append(activity_list['ActivityName'])
                for _key in _ship_data['Activities']['ActivityList']:
                    is_key_there_in_dict(_key, activity_list)
        for vendor in _content['Vendors']:
            test_data['arsReports']['VendorName'].append(vendor['VendorName'])
            for _key in _ship_data['Vendors']:
                is_key_there_in_dict(_key, vendor)

    @pytestrail.case(1134982)
    def test_02_reports_vendor_data(self, config, test_data, rest_ship):
        """
        Get Reports Vendor Data
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        params = {"size": "300"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendorslot")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        is_key_there_in_dict('activityDetails', _content)

    @pytestrail.case(1126671)
    def test_03_sailor_experience_report_pdf(self, config, test_data, rest_ship):
        """
        Get Sailor Experience Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sailorexperience/newpdf")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Byte Array Not Received !!')
        allure.attach(_content, name='sailorExperienceReport.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(1134979)
    def test_04_sailor_experience_report_csv(self, config, test_data, rest_ship):
        """
        Get Sailor Experience Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sailorexperience/csv")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, str):
            raise Exception(f'String Not Received !!')
        allure.attach(_content, name='sailorExperienceReport.csv', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(1126670)
    def test_05_activity_detail_report_pdf(self, config, test_data, rest_ship):
        """
        Get Activity Detail Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/activitydetail/newpdf")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Byte Array Not Received !!')
        allure.attach(_content, name='activityDetailReport.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(1134978)
    def test_06_activity_detail_report_csv(self, config, test_data, rest_ship):
        """
        Get Activity Detail Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/activitydetail/csv")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, str):
            raise Exception(f'String Not Received !!')
        allure.attach(_content, name='activityDetailReport.csv', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(1126669)
    def test_07_sailor_waiver_report_pdf(self, config, test_data, rest_ship):
        """
        Get Sailor Waiver Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sailorwaiver/newpdf")
        body = {
            "voyageNumber": test_data['voyageNumber'],
            "waiverRequired": "true"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Byte Array Not Received !!')
        allure.attach(_content, name='sailorWaiverReport.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(1134977)
    def test_08_sailor_waiver_report_csv(self, config, test_data, rest_ship):
        """
        Get Sailor Waiver Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sailorwaiver/csv")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, str):
            raise Exception(f'String Not Received !!')
        allure.attach(_content, name='sailorWaiverReport.csv', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(1126672)
    def test_09_vendor_manifest_report_pdf(self, config, test_data, rest_ship):
        """
        Get Vendor Manifest Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendormanifest/newpdf")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Byte Array Not Received !!')
        allure.attach(_content, name='vendorManifestReport.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(1134980)
    def test_10_vendor_manifest_report_csv(self, config, test_data, rest_ship):
        """
        Get Vendor Manifest Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendormanifest/csv")
        body = {
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, str):
            raise Exception(f'String Not Received !!')
        allure.attach(_content, name='vendorManifestReport.csv', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(67292832)
    def test_11_current_booking_report_pdf(self, config, test_data, rest_ship):
        """
        Get Current Booking Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/current/bookings/pdf")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Current Booking Report PDF not found !!')
        allure.attach(_content, name='CurrentBooking.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(67292833)
    def test_12_current_booking_report_csv(self, config, test_data, rest_ship):
        """
        Get Current Booking Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/current/bookings/xlsx")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Current Booking Report CSV not found !!')
        allure.attach(_content, name='CurrentBooking.xlsx', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(67292834)
    def test_13_sales_report_pdf(self, config, test_data, rest_ship, creds):
        """
        Get Sales Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sales/pdf")
        body = {"voyageNumber": test_data['voyageNumber'],
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "offset": 330,
                "activityNames": test_data['arsReports']['ActivityName'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "reportGeneratedBy": creds.verticalqa.username}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Sales Report PDF not found !!')
        allure.attach(_content, name='Sales.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(67292835)
    def test_14_sales_report_csv(self, config, test_data, rest_ship, creds):
        """
        Get Sales Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sales/xlsx")
        body = {"voyageNumber": test_data['voyageNumber'],
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "offset": 330,
                "activityNames": test_data['arsReports']['ActivityName'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "reportGeneratedBy": creds.verticalqa.username}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Sales Report CSV not found !!')
        allure.attach(_content, name='Sales.xlsx', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(67292836)
    def test_15_cancellation_report_pdf(self, config, test_data, rest_ship):
        """
        Get Cancellation Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/cancelled/bookings/pdf")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Cancellation Report PDF not found !!')
        allure.attach(_content, name='Cancellation.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(67292837)
    def test_16_cancellation_report_csv(self, config, test_data, rest_ship):
        """
        Get Cancellation Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/cancelled/bookings/xlsx")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Cancellation Report CSV not found !!')
        allure.attach(_content, name='Cancellation.xlsx', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(67292838)
    def test_17_cancellation_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Cancellation Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        test_data['ars_reports_ports'] = []
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/cancelled/bookings")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "currentPage": 1}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['data']) != 0:
            pass
        else:
            logger.info("no Cancellation Reports available")

    @pytestrail.case(67292839)
    def test_18_current_booking_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Current Booking Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/current/bookings")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "ports": test_data['arsReports']['PortCode'],
                "currentPage": 1}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['data']) != 0:
            pass
        else:
            logger.info("no Current Booking Reports available")

    @pytestrail.case(67292840)
    def test_19_sales_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Sales Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/sales")
        body = {"voyageNumber": test_data['voyageNumber'],
                "activityNames": test_data['arsReports']['ActivityName'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "currentPage": 1}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['data']) != 0:
            pass
        else:
            logger.info("no Sales Reports available for this filter ")

    @pytestrail.case(67292841)
    def test_20_full_activity_detail_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Full Activity Detail Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendorslot")
        body = {"voyageNumber": test_data['voyageNumber'],
                "status": test_data['arsReports']['status'],
                "access": ["PUBLIC", "PRIVATE"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "vendorNames": test_data['arsReports']['VendorName'],
                "ports": test_data['arsReports']['PortCode'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "activityNames": test_data['arsReports']['ActivityName'],
                "profilePic": True,
                "allDataNeeded": True,
                "waiverRequired": False,
                "startDate": f"{test_data['embarkDate']}T06:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59",
                "cancelled": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['activityDetails']) != 0:
            pass
        else:
            logger.info("no Full Activity Detail Reports available for this filter")

    @pytestrail.case(67292842)
    def test_21_vendor_manifest_detail_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Vendor Manifest Detail Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendorslot")
        body = {"voyageNumber": test_data['voyageNumber'],
                "status": test_data['arsReports']['status'],
                "access": ["PUBLIC", "PRIVATE"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "vendorNames": test_data['arsReports']['VendorName'],
                "ports": test_data['arsReports']['PortCode'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "activityNames": test_data['arsReports']['ActivityName'],
                "profilePic": True,
                "startDate": f"{test_data['embarkDate']}T06:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59",
                "cancelled": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['activityDetails']) != 0:
            pass
        else:
            logger.info("no Vendor Manifest Detail Reports available for this filter")

    @pytestrail.case(67292843)
    def test_22_waiver_detail_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Waiver Detail Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/vendorslot")
        body = {"voyageNumber": test_data['voyageNumber'],
                "status": test_data['arsReports']['status'],
                "access": ["PUBLIC", "PRIVATE"],
                "slotAccessTypes": ["PUBLIC", "PRIVATE"],
                "vendorNames": test_data['arsReports']['VendorName'],
                "ports": test_data['arsReports']['PortCode'],
                "activityGroupCodes": test_data['arsReports']['ActivityGroupCode'],
                "activityNames": test_data['arsReports']['ActivityName'],
                "profilePic": True,
                "allDataNeeded": False,
                "waiverRequired": True,
                "startDate": f"{test_data['embarkDate']}T06:00:00",
                "endDate": f"{test_data['debarkDate']}T23:59",
                "cancelled": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content['activityDetails']) != 0:
            pass
        else:
            logger.info("no Waiver Detail Reports available for this filter")

    @pytestrail.case(68852211)
    def test_23_refunded_booking_report_pdf(self, config, test_data, rest_ship):
        """
        Get Refunded Booking Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/refunded/bookings/pdf")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "bookingLocation": "",
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Refunded Booking Report PDF not found !!')
        allure.attach(_content, name='RefundedBookings.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(68852212)
    def test_24_refunded_booking_report_csv(self, config, test_data, rest_ship):
        """
        Get Refunded Booking Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/refunded/bookings/xlsx")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "bookingLocation": "",
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Refunded Booking Report CSV not found !!')
        allure.attach(_content, name='RefundedBookings.xlsx', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(69021126)
    def test_25_company_posted_booking_report_pdf(self, config, test_data, rest_ship):
        """
        Get Company Posted Booking Report PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/company/posted/bookings/pdf")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Company Posted Booking Report PDF not found !!')
        allure.attach(_content, name='CompanyPostedBookings.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(69021127)
    def test_26_company_posted_booking_report_csv(self, config, test_data, rest_ship):
        """
        Get Company Posted Booking Report CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/company/posted/bookings/xlsx")
        body = {"shipCode": config.ship.code,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "offset": 330}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Company Posted Booking Report CSV not found !!')
        allure.attach(_content, name='CompanyPostedBookings.xlsx', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(69021128)
    def test_27_refunded_booking_reports_filter(self, config, test_data, rest_ship):
        """
        To filter the Refunded Bookings Reports
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        booking_location = ['Pre-Cruise', 'Ship-Board']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/reports/refunded/bookings")
        params = {"page": 1}
        body = {"offset": 330,
                "sailDate": f"{test_data['embarkDate']} - {test_data['debarkDate']}",
                "voyageNumber": test_data['voyageNumber'],
                "bookingLocation": random.choice(booking_location),
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content['data']) != 0:
            pass
        else:
            logger.info("no Waiver Detail Reports available for this filter")
