__author__ = 'prahlad.sharma'

from virgin_utils import *
from ui_pages.ars_admin.reports.ars_reports import ArsReports
from ui_pages.ars_admin.login.login import Login
from ui_pages.ars_admin.dashboard.dashboard import ArsDashboard
from ui_pages.ars_admin.inventory_management.activities import Activities
from ui_pages.ars_admin.apihit.apihit import Apihit


@pytest.mark.Reports
@pytest.mark.run(order=7)
class TestActivityReservationCrewReports:
    """
    Test Suite to test ARS admin reports
    """

    @pytestrail.case(6036334)
    def test_01_access_reports_sections(self, page, config, web_driver, rest_shore, test_data, creds):
        """
        Access reports section with authenticated credentials
        :param page:
        :param config:
        :param web_driver:
        :param rest_shore:
        :param test_data:
        """
        try:
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', ArsDashboard(web_driver, test_data))
            setattr(page, 'activities', Activities(web_driver, test_data))
            setattr(page, 'ars_reports', ArsReports(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data, creds))
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/activityReservationCrew/login"))
            download_path = os.getcwd() + '/downloaded_files/'
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            page.login.verify_vv_logo_is_displayed_on_login_screen()
            page.login.login_into_ars_admin_web_app(user_name=creds.verticalqa.username, password=creds.verticalqa.password)
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.ars_reports.click_reports_in_left_panel()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_opening_reports_section")
            raise Exception(exp)

    @pytestrail.case(6036336)
    def test_02_verify_ui_of_reports_sections(self, page, web_driver, test_data):
        """
        Verify UI of reports section
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.verify_ars_admin_header_on_top_left_corner()
            page.ars_reports.verify_search_bar_present()
            page.ars_reports.verify_reports_header()
            page.ars_reports.verify_active_voyage_name(test_data['voyage_name_space'])
            page.ars_reports.verify_all_reports('Waiver Detail Report')
            page.ars_reports.verify_all_reports('Full Activity Detail Report')
            page.ars_reports.verify_all_reports('Sailor Experience Status Report')
            page.ars_reports.verify_all_reports('Vendor Manifest Detail Report')
            page.ars_reports.verify_all_reports('Current Booking Report')
            page.ars_reports.verify_all_reports('Sales Report')
            page.ars_reports.verify_all_reports('Cancellation Report')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_verifying_ui_of_reports_section")
            raise Exception(exp)

    @pytestrail.case(6036337)
    def test_03_access_waiver_detail_report(self, page, web_driver, test_data):
        """
        Access waiver detail report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Waiver Detail Report')
            page.ars_reports.verify_report_header('Waiver Detail Report')
            page.ars_reports.verify_report_ui(test_data, report_name="")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_accessing_waiver_detail_report")
            raise Exception(exp)

    @pytestrail.case(6036343)
    def test_04_export_waiver_detail_report(self, page, web_driver, test_data):
        """
        Export Waiver Detail report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_WaiverDetail", test_data, report_name="")
            page.ars_reports.export_report_as_pdf('')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_WaiverDetail", test_data, report_name="")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_exporting_waiver_detail_report")
            raise Exception(exp)

    @pytestrail.case(41062697)
    def test_05_sort_waiver_detail_report(self, page, web_driver, test_data):
        """
        Test case to verify that crew should be able to sort the reports
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.sort_report_and_verify(test_data, 'Event Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Type')
                page.ars_reports.sort_report_and_verify(test_data, 'Vendor Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Date')
                page.ars_reports.sort_report_and_verify(test_data, 'Port')
            else:
                pytest.skip('Data not available in Waiver Detail Report')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_sorting_waiver_detail_report")
            raise Exception(exp)

    @pytestrail.case(6036345)
    def test_06_apply_filter_in_waiver_detail_report(self, page, web_driver, test_data):
        """
        Test case to verify that crew should be able to apply filters
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.apply_and_verify_activity_filter_in_waiver_detail_report(test_data)
                page.ars_reports.apply_and_verify_vendor_filter(test_data)
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_waiver_detail_report")
            raise Exception(exp)

    @pytestrail.case(6036338)
    def test_07_access_full_activity_detail_report(self, page, web_driver, test_data):
        """
        Access Full Activity Detail report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.verify_reports_header()
            page.ars_reports.open_particular_report('Full Activity Detail Report')
            page.ars_reports.verify_report_header('Full Activity Detail Report')
            page.ars_reports.verify_report_ui(test_data, report_name="")
            page.ars_reports.availability_of_data()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_accessing_full_activity_detail_report")
            raise Exception(exp)

    @pytestrail.case(44743261)
    def test_08_export_full_activity_detail_report(self, page, web_driver, test_data):
        """
        Export Full Activity Detail Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_FullActivityDetail",
                                                             test_data, report_name="")
            page.ars_reports.export_report_as_pdf('')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_FullActivityDetail", test_data, report_name="")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_exporting_full_activity_detail_report")
            raise Exception(exp)

    @pytestrail.case(44750243)
    def test_09_sort_full_activity_detail_report(self, page, web_driver, test_data):
        """
        Test case to verify that crew should be able to sort the reports
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.sort_report_and_verify(test_data, 'Event Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Type')
                page.ars_reports.sort_report_and_verify(test_data, 'Vendor Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Date')
            else:
                pytest.skip('Data not available in Full Activity Detail Report')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_sorting_full_activity_detail_report")
            raise Exception(exp)

    @pytestrail.case(44750241)
    def test_10_apply_filter_in_full_activity_detail_report(self, page, web_driver, test_data):
        """
        Crew should be able to apply filters in Full Activity Detail Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.apply_and_verify_activity_filter(test_data)
                page.ars_reports.apply_and_verify_vendor_filter(test_data)
                page.ars_reports.add_column('Event Status')
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.apply_and_verify_status_filter(test_data)
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_full_activity_detail_report")
            raise Exception(exp)

    @pytestrail.case(6036340)
    def test_11_access_sailor_experience_status_report(self, page, web_driver, test_data):
        """
        Access Sailor Experience Status report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.verify_reports_header()
            page.ars_reports.open_particular_report('Sailor Experience Status Report')
            page.ars_reports.verify_report_header('Sailor Experience Status Report')
            page.ars_reports.verify_report_ui(test_data, report_name="")
            page.ars_reports.availability_of_data()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_accessing_sailor_experience_status_report")
            raise Exception(exp)

    @pytestrail.case(44743262)
    def test_12_export_sailor_experience_status_report(self, page, web_driver, test_data):
        """
        Export and verify Sailor Experience Status report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_SailorExperience", test_data, report_name="")
            page.ars_reports.export_report_as_pdf('Sailor Experience Status Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_SailorExperience",
                                                           test_data, report_name="")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_exporting_sailor_experience_status_report")
            raise Exception(exp)

    @pytestrail.case(44750244)
    def test_13_sort_sailor_experience_status_report(self, page, web_driver, test_data):
        """
        Test case to verify that crew should be able to sort the reports
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.sort_report_and_verify(test_data, 'Sailor')
                page.ars_reports.sort_report_and_verify(test_data, 'Cabin')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Date')
                page.ars_reports.sort_report_and_verify(test_data, 'Booking Status')
                page.ars_reports.click_back_button()
            else:
                pytest.skip('Data not available in Sailor Experience Status Report')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_sorting_sailor_experience_status_report")
            raise Exception(exp)

    @pytestrail.case(6036341)
    def test_14_access_vendor_manifest_detail_report(self, page, web_driver, test_data):
        """
        Access Vendor Manifest Detail report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.verify_reports_header()
            page.ars_reports.open_particular_report('Vendor Manifest Detail Report')
            page.ars_reports.verify_report_header('Vendor Manifest Detail Report')
            page.ars_reports.verify_report_ui(test_data, report_name="")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_accessing_vendor_manifest_detail_report")
            raise Exception(exp)

    @pytestrail.case(44750240)
    def test_15_export_vendor_manifest_detail_report(self, page, web_driver, test_data):
        """
        Export and Verify Vendor manifest Detail Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_VendorManifestDetail",
                                                             test_data, report_name="")
            page.ars_reports.export_report_as_pdf('')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_VendorManifestDetail",
                                                           test_data, report_name="")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_exporting_vendor_manifest_detail_report")
            raise Exception(exp)

    @pytestrail.case(44750245)
    def test_16_sort_vendor_manifest_detail_report(self, page, web_driver, test_data):
        """
        Test case to verify that crew should be able to sort the reports
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.sort_report_and_verify(test_data, 'Vendor Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Name')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Date')
                page.ars_reports.sort_report_and_verify(test_data, 'Event Type')
            else:
                pytest.skip('Data not available in Vendor Manifest Detail Report')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_sorting_vendor_manifest_detail_report")
            raise Exception(exp)

    @pytestrail.case(44750242)
    def test_17_apply_filter_in_vendor_manifest_detail_report(self, page, web_driver, test_data):
        """
        Crew should be able to apply filters in Vendor Manifest Detail Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.apply_and_verify_activity_filter(test_data)
                page.ars_reports.apply_and_verify_vendor_filter(test_data)
                page.ars_reports.add_column('Event Status')
                page.ars_reports.set_column_name(test_data)
                page.ars_reports.apply_and_verify_status_filter(test_data)
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_vendor_manifest_detail_report")
            raise Exception(exp)

    @pytestrail.case(67089483)
    def test_18_access_current_booking_report(self, page, web_driver, test_data):
        """
        Access current booking report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Current Booking Report')
            page.ars_reports.verify_report_header('Current Booking Report')
            page.ars_reports.verify_report_ui(test_data, report_name="Current Booking Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_accessing_current_booking_report")
            raise Exception(exp)

    @pytestrail.case(67089486)
    def test_19_export_current_booking_detail_report(self, page, web_driver, test_data):
        """
        Export current booking details report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_CurrentBooking", test_data, report_name="Current Booking Report")
            page.ars_reports.export_report_as_pdf('Current Booking Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_CurrentBooking", test_data, report_name="Current Booking Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_exporting_current_booking_report")
            raise Exception(exp)

    @pytestrail.case(67110827)
    def test_20_apply_filter_in_current_booking_report(self, page, web_driver):
        """
        Test case to verify that crew should be able to apply filters
        :param page:
        :param web_driver:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.apply_filter_report()
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_current_booking_report")
            raise Exception(exp)

    @pytestrail.case(67089484)
    def test_21_access_sales_report(self, page, web_driver, test_data):
        """
        Access sales report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Sales Report')
            page.ars_reports.verify_report_header('Sales Report')
            page.ars_reports.verify_report_ui(test_data, report_name="Sales Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_accessing_sales_report")
            raise Exception(exp)

    @pytestrail.case(67089487)
    def test_22_export_sales_detail_report(self, page, web_driver, test_data):
        """
        Export sales details report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_Sales", test_data,
                                                             report_name="")
            page.ars_reports.export_report_as_pdf('Sales Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_Sales", test_data,
                                                           report_name="Sales Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_exporting_sales_report")
            raise Exception(exp)

    @pytestrail.case(67117286)
    def test_23_apply_filter_sales_report(self, page, web_driver):
        """
        Test case to verify that crew should be able to apply filters
        :param page:
        :param web_driver:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.apply_filter_report()
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_sales_report")
            raise Exception(exp)

    @pytestrail.case(67089485)
    def test_24_access_cancellation_report(self, page, web_driver, test_data):
        """
        Access cancellation report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Cancellation Report')
            page.ars_reports.verify_report_header('Cancellation Report')
            page.ars_reports.verify_report_ui(test_data, report_name="Cancellation Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_accessing_cancellation_report")
            raise Exception(exp)

    @pytestrail.case(67089488)
    def test_25_export_cancellation_detail_report(self, page, web_driver, test_data):
        """
        Export cancellation details report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_Cancellation", test_data,
                                                             report_name="Cancellation Report")
            page.ars_reports.export_report_as_pdf('Cancellation Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_Cancellation", test_data,
                                                           report_name="Cancellation Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_exporting_cancellation_report")
            raise Exception(exp)

    @pytestrail.case(67117287)
    def test_26_apply_filter_cancellation_report(self, page, web_driver):
        """
        Test case to verify that crew should be able to apply filters
        :param page:
        :param web_driver:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.apply_filter_report()
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_cancellation_report")
            raise Exception(exp)

    @pytestrail.case(69471943)
    def test_27_access_refund_booking_report(self, page, web_driver, test_data):
        """
        access Refunded Bookings Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Refunded Bookings Report')
            page.ars_reports.verify_report_header('Refunded Bookings Report')
            page.ars_reports.verify_report_ui(test_data, report_name="Refunded Bookings Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_refunded bookings report")
            raise Exception(exp)

    @pytestrail.case(69474038)
    def test_28_export_refund_booking_detail_report(self, page, web_driver, test_data):
        """
        Export Refunded Bookings Report details report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_RefundedBookings", test_data,
                                                             report_name="Refunded Bookings Report")
            page.ars_reports.export_report_as_pdf('Refunded Bookings Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_RefundedBookings", test_data,
                                                           report_name="Refunded Bookings Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_exporting_refund_booking_report")
            raise Exception(exp)

    @pytestrail.case(69474039)
    def test_29_apply_filter_refund_booking_report(self, page, web_driver):
        """
        Test case to verify that crew should be able to apply filters on Refunded Bookings Report
        :param page:
        :param web_driver:
        """
        try:
            if not page.ars_reports.blank_list():
                page.ars_reports.apply_filter_report()
                page.ars_reports.click_back_button()
            else:
                page.ars_reports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_applying_filter_refund_booking_report")
            raise Exception(exp)

    @pytestrail.case(69984444)
    def test_30_access_refund_booking_report(self, page, web_driver, test_data):
        """
        access Company Posted Bookings Report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.open_particular_report('Company Posted Bookings Report')
            page.ars_reports.verify_report_header('Company Posted Bookings Report')
            page.ars_reports.verify_report_ui(test_data, report_name="Company Posted Bookings Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_company_posted_bookings_report")
            raise Exception(exp)

    @pytestrail.case(69984445)
    def test_31_export_refund_booking_detail_report(self, page, web_driver, test_data):
        """
        Export Company Posted Bookings Report details report
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.ars_reports.export_report_as_excel()
            page.ars_reports.verify_exported_report_as_excel(f"{test_data['voyageNumber']}_CompanyPostedBookings", test_data,
                                                             report_name="Company Posted Bookings Report")
            page.ars_reports.export_report_as_pdf('Refunded Bookings Report')
            page.ars_reports.verify_exported_report_as_pdf(f"{test_data['voyageNumber']}_CompanyPostedBookings", test_data,
                                                           report_name="Company Posted Bookings Report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_company_posted_bookings_report")
            raise Exception(exp)