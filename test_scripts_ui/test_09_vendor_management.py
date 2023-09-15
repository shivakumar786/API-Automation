__author__ = 'Saloni.pattnaik'

import time

from ui_pages.ars_admin.login.login import Login
from ui_pages.ars_admin.dashboard.dashboard import ArsDashboard
from ui_pages.ars_admin.bookings.booking import ArsBookings
from ui_pages.ars_admin.apihit.apihit import Apihit
from ui_pages.ars_admin.vendor_management.vendor_activities import Arsvendor
from ui_pages.ars_admin.vendor_management.settings import ArsSettings
from ui_pages.ars_admin.vendor_management.accounting import ArsAccounting
from virgin_utils import *


@pytest.mark.VENDOR_MANAGEMENT_UI
@pytest.mark.run(order=9)
class TestVendorManagement:
    """
    Test ui suite to run Ars Vendor Management
    """

    @pytestrail.case(6036369)
    def test_01_access_vendor_tab(self, page, web_driver, config, test_data, rest_ship, creds):
        """
        To verify crew should be able to access Bookings after login
        :param rest_ship:
        :param test_data:
        :param config:
        :param page:
        :param web_driver:
        """
        try:
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', ArsDashboard(web_driver, test_data))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'booking', ArsBookings(web_driver))
            setattr(page, 'vendor', Arsvendor(web_driver))
            setattr(page, "settings", ArsSettings(web_driver))
            setattr(page, "accounting", ArsAccounting(web_driver))
            web_driver.open_website(
                url=urljoin(config.ship.url.replace('/svc', ''), "/activityReservationCrew/login"))
            page.login.verify_vv_logo_is_displayed_on_login_screen()
            page.login.login_into_ars_admin_web_app(user_name=creds.verticalqa.username,
                                                    password=creds.verticalqa.password)
            time.sleep(20)
            page.apihit.get_ship_reservation_details()
            page.dashboard.click_on_vendor_tab_from_dashboard()
            if page.vendor.verify_vendor_page_header() != "Vendor Activities":
                raise Exception("user is not on vendor activity page")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to access vendor tab")
            raise Exception(exp)

    @pytestrail.case(6036370)
    def test_02_verify_vendor_page_ui(self, page, web_driver):
        """
        To verify ui of vendor page
        :param page:
        :param web_driver:
        """
        try:
            if page.vendor.verify_vendor_page_header() == "Vendor Activities":
                logger.debug("Crew able to access ARS vendor")
            else:
                raise Exception("Crew is not on ARS vendor page")
            if page.vendor.verify_activity_list() is None:
                raise Exception("No activity available")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to access vendors")
            raise Exception(exp)

    @pytestrail.case(67949077)
    def test_03_sort_vendor_list(self, page, web_driver, test_data):
        """
        Filter vendor list with vendor name, vendor code, account status, balance amount
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.vendor.set_column_name(test_data)
            page.vendor.sort_report_and_verify(test_data, 'Vendor Name')
            page.vendor.sort_report_and_verify(test_data, 'Vendor Code')
            page.vendor.sort_report_and_verify(test_data, 'Account Status')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Applied filter failed")
            raise Exception(exp)

    @pytestrail.case(6036372)
    def test_04_verify_filter_on_vendor_list(self, page, web_driver):
        """
        To verify filter on vendor list
        :param page:
        :param web_driver:
        """
        try:
            page.vendor.click_on_activity_filter()
            page.vendor.select_filter_option()
            filtered_activities = page.vendor.verify_applied_filter()
            if len(filtered_activities) == 0:
                logger.debug("No activity available with active status")
            else:
                page.vendor.select_first_activity()
                if page.vendor.verify_vendor_status() != "Active":
                    raise Exception("Filter has not applied")
                page.vendor.click_back_button()

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Applied filter failed")
            raise Exception(exp)

    @pytestrail.case(24937015)
    def test_05_file_complaints_for_activity(self, page, web_driver):
        """
        To file complaints for activity
        :param test_data:
        :param page:
        :param web_driver:
        """
        try:
            if page.vendor.is_no_records_found():
                pytest.skip(msg="No vendors in list to log complaint")
            page.vendor.log_complaint()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to file complaints")
            raise Exception(exp)

    @pytestrail.case([6036371, 6036374])
    def test_06_bulk_settlement(self, page, web_driver):
        """
        To verify bulk settlement of activities
        :param test_data:
        :param page:
        :param web_driver:
        """
        try:
            if page.vendor.is_no_records_found():
                pytest.skip(msg="No vendors in list to perform bulk settlement")
            page.vendor.bulk_settlement()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed bulk settlement")
            raise Exception(exp)

    @pytestrail.case(24938091)
    def test_07_reject_invoice_from_dashboard(self, page, web_driver):
        """
        To verify reject invoice from dashboard
        :param test_data:
        :param page:
        :param web_driver:
        """
        try:
            page.dashboard.click_on_dashboard_tab_from_dashboard()
            previous_count = page.dashboard.get_approval_count()
            if previous_count == 0:
                pytest.skip(msg='No Pending vendor accounts for approval')
            if previous_count >= 1:
                page.dashboard.click_pending_approval()
                page.dashboard.reject_approval()
                page.dashboard.click_on_dashboard_tab_from_dashboard()
                current_count = page.dashboard.get_approval_count()
                if not previous_count > current_count:
                    raise Exception("Invoice not rejected")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed reject invoice")
            raise Exception(exp)

    @pytestrail.case(24938087)
    def test_08_adjust_amount_of_activity(self, page, web_driver):
        """
        To adjust the amount of rejected activity slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_vendor_tab_from_dashboard()
            if page.vendor.is_no_records_found():
                pytest.skip(msg="No vendors in list to adjust amount for rejected slot")
            page.vendor.adjust_vendor_amount()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Adjust amount failed")
            raise Exception(exp)

    @pytestrail.case(44938889)
    def test_09_verify_total_adjustment_amount(self, page, test_data, web_driver):
        """
        To verify total adjustment amount
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            activities = page.vendor.verify_applied_filter()
            for activity in range(0, len(activities)):
                activities = page.vendor.verify_applied_filter()
                page.vendor.select_each_activity(activities[activity])
                if page.vendor.calculate_total_adjustment_amount() == 0:
                    page.vendor.click_back_button()
                    continue
                else:
                    if not page.vendor.calculate_total_adjustment_amount():
                        raise Exception("Adjustment amount not matching")
                    break
            else:
                test_data['adjustment_amount'] = 0
                pytest.skip("No adjustment amount available to verify")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("verify Adjust amount failed")
            raise Exception(exp)

    @pytestrail.case(44938951)
    def test_10_verify_total_balance_amount(self, page, web_driver):
        """
        To verify total balance amount
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_vendor_tab_from_dashboard()
            if page.vendor.is_no_records_found():
                pytest.skip(msg="No vendors in list to adjust amount for rejected slot")
            page.vendor.compare_vendor_balance()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("verify balance amount failed")
            raise Exception(exp)

    @pytestrail.case(67554651)
    def test_11_verify_elements_on_settings_page(self, page,  web_driver):
        """
        To verify all the elements on settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_settings_tab_from_dashboard()
            page.settings.verify_settings_page_elements()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("settings_page_elements")
            raise Exception(exp)

    @pytestrail.case(67553865)
    def test_12_create_notification_template_from_settings(self, page, web_driver):
        """
        Create new notification template from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.create_new_notification_template()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("create_notification")
            raise Exception(exp)

    @pytestrail.case(67554646)
    def test_13_edit_notification_template_from_settings(self, page, web_driver):
        """
        Edit notification template from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.edit_newly_created_notification_template()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("edit_notification")
            raise Exception(exp)

    @pytestrail.case(67554647)
    def test_14_delete_notification_template_from_settings(self, page, web_driver):
        """
        Delete notification template from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.delete_created_notification_template()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_notification")
            raise Exception(exp)

    @pytestrail.case(67554648)
    def test_15_create_meeting_location_from_settings(self, page, web_driver):
        """
        Create new activity meeting location from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.create_new_meeting_location()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("create_meeting_location")
            raise Exception(exp)

    @pytestrail.case(67554649)
    def test_16_edit_meeting_location_from_settings(self, page, web_driver):
        """
        Edit new activity meeting location from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.edit_newly_created_meeting_location()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("edit_meeting_location")
            raise Exception(exp)

    @pytestrail.case(67554650)
    def test_17_delete_meeting_location_from_settings(self, page, web_driver):
        """
        Delete new activity meeting location from settings page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.settings.delete_newly_created_meeting_location()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_meeting_location")
            raise Exception(exp)

    @pytestrail.case(67623504)
    def test_18_login_to_ars_admin_as_shipboard_accounting_manager(self, page, web_driver):
        """
        login to ARS Admin as shipboard accounting manger
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.logout_from_ars()
            page.login.login_into_ars_admin_web_app(user_name="BKAN01",
                                                    password="Test@1234")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("login_as_accounting_manager")
            raise Exception(exp)

    @pytestrail.case(67623505)
    def test_19_verify_elements_in_accounting_tab(self, page, web_driver):
        """
        To verify UI elements from accounting tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.clik_on_accounting_tab()
            page.accounting.verify_accounting_tab_elements()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("elements_of_accounting_tab")
            raise Exception(exp)

    @pytestrail.case(67650531)
    def test_20_edit_quick_code_from_accounting_tab(self, page, web_driver):
        """
        To verify user is able to edit charge id from accounting tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.accounting.edit_quick_code_from_accounting_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("quick_code_from_accounting_tab")
            raise Exception(exp)