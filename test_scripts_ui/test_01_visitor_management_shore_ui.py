__author__ = 'prahlad.sharma'

import pytest

from ui_pages.embarkation_supervisor.apihit import Apihit
from virgin_utils import *
from ui_pages.embarkation_supervisor.supervisor_login import SupervisorLogin
from ui_pages.embarkation_supervisor.dashboard import Dashboard
from ui_pages.visitor_management.select_ship_shore import SelectShip
from ui_pages.embarkation_supervisor.reports import Reports
from ui_pages.visitor_management.visitors import Visitors
from ui_pages.visitor_management.filter import Filter
from ui_pages.visitor_management.settings import Settings
from ui_pages.embarkation_supervisor.boarding_slots import Boarding_slots
import pathlib


@pytest.mark.VISITOR_MANAGEMENT_SHORE_UI
@pytest.mark.run(order=1)
class TestVisitorManagementShore:
    """
    Test Suite to test Embarkation Supervisor
    """

    @pytestrail.case(26323331)
    def test_01_launch_website_and_check_invalid_login(self, web_driver, page, config, rest_shore, test_data):
        """
        Test cases to Launch the embarkation Supervisor/visitor Management and login into application with invalid
        user details
        :param web_driver:
        :param page:
        :param config:
        :param rest_shore:
        :param test_data:
        :return:
        """
        try:
            setattr(page, 'login', SupervisorLogin(web_driver))
            setattr(page, 'dashboard', Dashboard(web_driver))
            setattr(page, "select_ship", SelectShip(web_driver))
            setattr(page, 'visitor', Visitors(web_driver))
            setattr(page, 'setting', Settings(web_driver))
            setattr(page, 'filter', Filter(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data))
            setattr(page, 'reports', Reports(web_driver))
            setattr(page, 'boarding', Boarding_slots(web_driver))
            download_path = os.getcwd() + '/downloaded_files/'
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            file = pathlib.Path(download_path + 'visitors.csv')
            if file.exists():
                os.remove(file)
            file = pathlib.Path(download_path + 'exception.csv')
            if file.exists():
                os.remove(file)
            web_driver.open_website(url=urljoin(config.shore.url.replace('/svc', ''), "/embarkation-supervisor/login"))
            page.login.verification_of_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            page.login.login_into_embarkation_supervisor(username='vertical_ma', password='abcd123')
            page.login.verification_of_invalid_login_toast()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_error")
            raise Exception(exp)

    @pytestrail.case(26323332)
    def test_02_login(self, page, test_data, web_driver, creds):
        """
        Login with valid credentials
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data['reviewer'] = 'Adrain Church'
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username="Vijay.tiwari", password="SqaECa5KP7BB")
            if page.select_ship.verify_ship_page_availability():
                logger.debug("User is able to login successfully and Ship selection page display")
            else:
                web_driver.allure_attach_jpeg('login_not_done')
                raise Exception("Login is not working and user not landed on ship selection page")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('invalid_login_error')
            raise Exception(exp)

    @pytestrail.case(25747307)
    def test_03_select_ship(self, page, web_driver, test_data):
        """
        select the ship
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_next_voyage(test_data)
            page.select_ship.select_ship(test_data)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_select_ship")
            raise Exception(exp)

    @pytestrail.case(26331342)
    def test_04_change_ship(self, page, web_driver, test_data):
        """
        change the ship
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.click_setting_in_left_panel()
            page.setting.verify_setting_page_title()
            page.setting.click_change_ship_button()
            page.setting.select_ship_from_list(test_data['shipName'])
            page.setting.click_change()
            page.dashboard.availability_of_ship_name(test_data['shipName'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_select_ship")
            raise Exception(exp)

    @pytestrail.case(37828488)
    def test_05_select_upcoming_voyage(self, page, test_data, web_driver):
        """
        select the active voyage
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.select_active_voyage(test_data['next_voyage_name_shore'])
            page.dashboard.get_active_voyage_name(test_data['next_voyage_name_shore'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_select_voyage")
            raise Exception(exp)

    @pytestrail.case(25782201)
    def test_06_select_active_voyage(self, page, test_data, web_driver):
        """
        select the active voyage
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.select_active_voyage(test_data['voyage_name_space'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_select_voyage")
            raise Exception(exp)

    @pytestrail.case(26323303)
    def test_07_verify_dashboard(self, page, test_data, web_driver):
        """
        Verify the dashboard fields
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.availability_of_search_option()
            page.dashboard.availability_of_user_profile()
            page.dashboard.availability_of_application_name()
            page.dashboard.availability_of_refresh_icon()
            page.dashboard.availability_of_report()
            page.dashboard.availability_of_ship_date_time()
            page.dashboard.availability_of_copyright_info()
            page.dashboard.availability_of_ship_name(test_data['shipName'])

            page.dashboard.availability_of_visitor_expected_today()
            page.dashboard.availability_of_visitor_approved()
            page.dashboard.availability_of_visitor_onboard()
            page.dashboard.availability_of_visitor_ashore()
            page.dashboard.availability_of_visitor_checkout()
            page.dashboard.availability_of_visitor_rejected()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_dashboard")
            raise Exception(exp)

    @pytestrail.case(26328033)
    def test_08_match_visitor_count(self, page, web_driver):
        """
        Match the total visitor count
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.match_total_visitor()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_visitor_count")
            raise Exception(exp)

    @pytestrail.case(26323329)
    def test_09_on_board_ashore_visitor_click(self, page, web_driver):
        """
        TestCase to verify onboard and ashore count should be click-able and count should match
        :param page:
        :param web_driver:
        :return:
        """
        try:
            onboard_count = page.dashboard.get_onboard_visitor_count()
            if onboard_count == 0:
                logger.debug("Onboard count is not clickable")
            else:
                pytest.skip("Onboard visitor count is not clickable")
                page.dashboard.click_onboard_count()
                list_count = page.visitor.get_count_on_list()
                assert list_count == onboard_count, "On-board count is not matching"

            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            ashore_count = page.dashboard.get_ashore_visitor_count()
            if ashore_count == 0:
                logger.debug("Ashore count is not clickable")
            else:
                pytest.skip("Ashore visitor count is not clickable")
                page.dashboard.click_ashore_count()
                list_count = page.visitor.get_count_on_list()
                assert list_count == ashore_count, "Ashore count is not matching"

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(26323334)
    def test_10_add_visitor(self, page, test_data, web_driver):
        """
        add the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data['visitorExpectedCount'] = page.dashboard.get_expected_today_visitor_count()
            test_data['visitorApprovedCount'] = page.dashboard.get_approved_visitor_count()
            test_data['visitorRejectedCount'] = page.dashboard.get_rejected_visitor_count()
            page.dashboard.click_refresh_icon()
            ship_date = page.dashboard.get_ship_time_ui()
            test_data["visit_date"] = ship_date.rsplit(" ")[2].replace(",", "")
            test_data['visitor_first_name'] = generate_first_name()
            test_data['visitor_last_name'] = generate_last_name()
            test_data['citizenship'] = "United States"
            test_data['visitor_name'] = f"{test_data['visitor_first_name']} {test_data['visitor_last_name']}"
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.visitor.click_add_visitor()
            page.visitor.fill_visitor_form_and_save(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                    test_data['citizenship'], test_data['reviewer'],
                                                    test_data["visit_date"], test_data, 'shore')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(31473366)
    def test_11_verify_visitor_pending_count(self, page, test_data, web_driver):
        """
        Check Visitor approval pending count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            assert test_data[
                       'visitorExpectedCount'] + 1 == page.dashboard.get_expected_today_visitor_count(), \
                'Visitor expected count did not get increased after creating new visitor !!'
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(26323307)
    def test_12_visitor_filter(self, page, test_data, web_driver):
        """
        Check teh Visitor on List
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        current_ship_date = datetime.strptime(test_data["visit_date"], "%m/%d/%Y").strftime("%m/%-d/%Y")
        try:
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.apihit.get_token(side='shore')
            page.apihit.get_visitor_details()
            page.visitor.click_filter_option()
            page.filter.select_start_date(current_ship_date)
            page.filter.select_end_date(current_ship_date)
            page.filter.click_visit_status()
            page.filter.click_approved()
            page.filter.select_department("Engine")
            if test_data['port_name'] != '':
                page.filter.select_port(test_data['port_name'])
            page.filter.click_apply()
            page.visitor.add_new_column_in_list('ID Number')
            page.visitor.add_new_column_in_list('Citizenship')
            page.visitor.verify_visitor_get_added(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                  test_data['citizenship'], 'ID', test_data, test_data["visit_date"])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_visitor_list_filter")
            raise Exception(exp)

    @pytestrail.case(26335700)
    def test_13_visitor_on_list(self, page, test_data, web_driver):
        """
        Check teh Visitor on List
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verify_visitor_get_added(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                  test_data['citizenship'], 'ID', test_data, test_data["visit_date"])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_visitor_list")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-105878')
    @pytestrail.case(26328942)
    def test_14_export_visitor(self, page, web_driver):
        """
        Export the visitor
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verify_export('visitors')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_export_visitor")
            raise Exception(exp)

    @pytestrail.case(26323337)
    def test_15_info_visitor(self, page, test_data, web_driver):
        """
        Info the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.set_column_name(test_data)
            page.visitor.view_visitor(test_data)
            page.visitor.verify_visitor_details_on_details_screen(test_data['visitor_first_name'],
                                                                  test_data['visitor_last_name'],
                                                                  test_data['citizenship'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_info_visitor")
            raise Exception(exp)

    @pytestrail.case(26323342)
    def test_16_edit_visitor(self, page, test_data, web_driver):
        """
        Edit the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.click_edit_visitor()
            test_data['visitor_first_name'] = page.visitor.edit_visitor()
            test_data['visitor_name'] = f"{test_data['visitor_first_name']} {test_data['visitor_last_name']}"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_edit_visitor")
            raise Exception(exp)

    @pytestrail.case(26323336)
    def test_17_reject_visitor(self, page, web_driver):
        """
        Reject the visitor
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.reject_visit()
            if page.visitor.get_visit_status_in_visitor_details() == 'Rejected':
                logger.debug("Visit is Rejected after Rejected by Supervisor")
            else:
                raise Exception("Visit is not Rejected after Rejected by Supervisor")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_reject_visit")
            raise Exception(exp)

    @pytestrail.case(26323335)
    def test_18_approve_visitor(self, page, web_driver):
        """
        Approve the visitor
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.open_visit_tab()
            visit_status = page.visitor.get_visit_status()
            if visit_status == 'Rejected':
                page.visitor.approve_visit()
            else:
                raise Exception("After create the visitor , visit is not coming in pending state")
            if page.visitor.get_visit_status_in_visitor_details() == 'Approved':
                logger.debug("Visit is approved after Approved by Supervisor")
            else:
                raise Exception("Visit is not approved after Approved by Supervisor")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_approve_visit")
            raise Exception(exp)

    @pytestrail.case(31474125)
    def test_19_verify_visitor_approved_count(self, page, test_data, web_driver):
        """
        Check Visitor approved count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            assert test_data[
                       'visitorApprovedCount'] + 1 == page.dashboard.get_approved_visitor_count(), \
                'Visitor approved count did not get increased after approving visitor !!'
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(31474127)
    def test_20_verify_visitor_rejected_count(self, page, test_data, web_driver):
        """
        Check Visitor rejected count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            assert test_data[
                       'visitorRejectedCount'] == page.dashboard.get_rejected_visitor_count(), \
                'Visitor rejected count did not get increased after rejecting visitor !!'
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(26323309)
    def test_21_create_alert(self, page, test_data, web_driver):
        """
        create the alert
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        current_ship_date = datetime.strptime(test_data["visit_date"], "%m/%d/%Y").strftime("%m/%-d/%Y")
        try:
            page.dashboard.click_visitor_tab()
            page.visitor.click_filter_option()
            page.filter.select_start_date(current_ship_date)
            page.filter.select_end_date(current_ship_date)
            page.filter.click_visit_status()
            page.filter.click_approved()
            page.filter.select_department("Engine")
            if test_data['port_name'] != '':
                page.filter.select_port(test_data['port_name'])
            page.filter.click_apply()
            page.visitor.add_new_column_in_list('ID Number')
            page.visitor.add_new_column_in_list('Citizenship')
            page.visitor.set_column_name(test_data)
            page.visitor.verify_visitor_get_added(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                  test_data['citizenship'], 'ID', test_data, test_data["visit_date"])
            page.visitor.view_visitor(test_data)
            page.visitor.open_more_option_drawer_details()
            page.visitor.click_create_alert()
            test_data['alert_text'] = 'alert for visitor'
            page.visitor.create_alert(test_data['alert_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_create_alert")
            raise Exception(exp)

    @pytestrail.case(26351573)
    def test_22_verification_alert_on_tab(self, page, test_data, web_driver):
        """
        TestCase to verify the alert after creation, in alert Tab
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_alert_after_creation(test_data['alert_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_verify_alert_tab")
            raise Exception(exp)

    @pytestrail.case(26323311)
    def test_23_verification_alert_on_details(self, page, test_data, web_driver):
        """
        TestCase to verify the alert after creation, on alert details screen
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_alert_on_details_screen(test_data['alert_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_verify_alert_on_details")
            raise Exception(exp)

    @pytestrail.case(26323314)
    def test_24_edit_alert_and_verify(self, page, test_data, web_driver):
        """
        Test case to edit the alert and verification
        :param page:
        :param test_data:
        :param web_driver:
        """
        try:
            test_data['updated_alert_text'] = "alert for visitor after edit"
            page.visitor.edit_alert_and_verify(test_data['updated_alert_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_edit_alert")
            raise Exception(exp)

    @pytestrail.case(26323315)
    def test_25_delete_alert(self, page, web_driver):
        """
        Test case to Delete the alert
        :param page:
        :param web_driver:
        """
        try:
            page.visitor.delete_alert()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_delete_alert")
            raise Exception(exp)

    @pytestrail.case(26323310)
    def test_26_create_message(self, page, test_data, web_driver):
        """
        create the message
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.open_more_option_drawer_details()
            page.visitor.click_create_message()
            test_data['message_text'] = 'message for visitor'
            page.visitor.create_message(test_data['message_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_create_message")
            raise Exception(exp)

    @pytestrail.case(26351574)
    def test_27_verification_message_on_message_tab(self, page, test_data, web_driver):
        """
        TestCase to verify the message after creation, in message Tab
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_message_after_creation(test_data['message_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_message_verification")
            raise Exception(exp)

    @pytestrail.case(26323312)
    def test_28_verification_message_on_details(self, page, test_data, web_driver):
        """
        TestCase to verify the message after creation, in message details
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_message_on_details_screen(test_data['message_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_message_verify_details")
            raise Exception(exp)

    @pytestrail.case(26323313)
    def test_29_edit_message_and_verify(self, page, test_data, web_driver):
        """
        Test case to edit the message and verification
        :param page:
        :param test_data:
        :param web_driver:
        """
        try:
            test_data['updated_message_text'] = "message for visitor after edit"
            page.visitor.edit_message_and_verify(test_data['updated_message_text'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_edit_message")
            raise Exception(exp)

    @pytestrail.case(26323316)
    def test_30_delete_message(self, page, web_driver):
        """
        Test case to Delete the message
        :param page:
        :param web_driver:
        """
        try:
            page.visitor.delete_message()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_delete_message")
            raise Exception(exp)

    @pytestrail.case(26323339)
    def test_31_add_new_visit(self, page, test_data, web_driver):
        """
        Test case to add the visit in already created visitor
        :param page:
        :param test_data:
        :param web_driver:
        """
        try:
            test_data["additional_visit_purpose"] = 'testing in additional visit'
            page.visitor.add_additional_visit(test_data["additional_visit_purpose"], test_data["visit_date"],
                                              test_data['reviewer'], 'shore')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_new_visit")
            raise Exception(exp)

    @pytestrail.case(26323304)
    def test_32_search_visitor(self, page, test_data, web_driver):
        """
        TestCase to verify the Global Search
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.enter_search_keywords(test_data['visitor_first_name'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['visitor_name'], "Global Search")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_search_visitor")
            raise Exception(exp)

    @pytestrail.case(26323308)
    def test_33_advance_search_visitor(self, page, test_data, web_driver):
        """
        TestCase to verify the Search with Visitor first name, last name, doc num. doc type, DOB
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.enter_search_keywords(test_data['searched_dob'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_dob'], 'DOB')

            page.dashboard.enter_search_keywords(test_data['searched_doc_number'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_doc_number'], 'Doc Number')

            page.dashboard.enter_search_keywords(test_data['searched_ln'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_ln'], 'LastName')

            page.dashboard.enter_search_keywords(test_data['searched_fn'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_fn'], 'FirstName')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_search_visitor")
            raise Exception(exp)

    @pytestrail.case(26323341)
    def test_34_bulk_visitor_approve(self, page, web_driver, test_data):
        """
        Test case to approve the multiple visitor
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.visitor.add_new_column_in_list('ID Number')
            page.visitor.set_column_name(test_data)
            test_data['id_numbers'] = page.visitor.select_custom_visitors_by_id_number(test_data['ID Number_position'], 10, test_data)
            page.visitor.select_all_visitor()
            page.visitor.all_approve()
            page.visitor.verify_toast_title()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_bulk_visitor_approve")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-105878')
    @pytestrail.case(31597789)
    def test_35_verify_bulk_visitor_approve(self, page, web_driver, test_data):
        """
        Test case to verify the status of bulk approved visitor
        :param page :
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            today_date = date.today().strftime("%m-%d-%Y")
            file_name = f'Visitors_ScarletLady_{today_date}'
            page.visitor.verify_export(file_name)
            page.visitor.verify_bulk_approve(file_name, test_data['id_numbers'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_bulk_visitor_verify")
            raise Exception(exp)

    @pytestrail.case(26323324)
    def test_36_missing_image_report(self, page, web_driver, test_data):
        """
        TestCase to verify the missing image exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.apihit.get_missing_picture_count_api(side='shore')
            page.reports.open_exception_report()
            assert test_data['total_missing_picture_count'] == page.reports.get_missing_picture_count(), \
                "missing picture count not matching"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("missing_image_exception_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-113516')
    @pytestrail.case(31364272)
    def test_37_export_missing_image_report(self, page, web_driver):
        """
        TestCase to verify the export the missing image report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.export_and_verify_reports("exception")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("export_missing_image_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(26323328)
    def test_38_not_checked_in_onboard_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Not Checked in On board exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.apihit.get_not_checked_in_onboard_count_api(side='shore')
            assert test_data['total_not_checked_in_count'] == page.reports.get_not_checkedin_onboard_count(), \
                "Not Checked in On board count not matching on UI"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("expire_card_exception_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-113516')
    @pytestrail.case(31365788)
    def test_39_export_not_checked_in_onboard_report(self, page, web_driver):
        """
        TestCase to verify the export the Not Checked in On board report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.export_and_verify_reports("exception")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("export_expire_card_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(26323326)
    def test_40_checked_in_not_onboard_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Checked in Not On board exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.apihit.get_checked_in_not_onboard_count_api(side='shore')
            assert test_data['total_checked_in_count'] == page.reports.get_checked_in_not_onboard_count(), \
                "Checked in but Not On board count not matching on UI"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("expire_card_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(26323305)
    def test_41_cbp_report(self, page, web_driver):
        """
        TestCase to verify the CBP report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.reports.open_cbp_report()
            page.reports.check_availability_of_fields_in_cbp()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("cbp_report_error")
            raise Exception(exp)

    @pytestrail.case(26331832)
    def test_42_export_cbp_report(self, page, web_driver):
        """
        TestCase to verify the export CBP report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            display_sailor_count = page.reports.get_total_sailor_count_cbp()
            exported_sailor_count = page.reports.export_and_verify_reports("cbp")
            assert int(display_sailor_count) == int(exported_sailor_count), "Count not matching in CPB report after " \
                                                                            "export "
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("cbp_report_export_report_error")
            raise Exception(exp)

    @pytestrail.case(26328944)
    def test_43_filter_apply_cbp_report(self, page, web_driver):
        """
        TestCase to verify the Filter can be apply on CBP report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_boarding_status()
            page.reports.select_clearance_status()
            page.reports.select_department()
            page.reports.click_apply()
            if page.reports.blank_list():
                logger.debug("Filter applied successfully")
            else:
                raise Exception("Filter is not applied successfully")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("CBP_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(26323321)
    def test_44_movement_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Movement report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.reports.open_movement_report()
            if page.reports.blank_list():
                raise Exception("Movement reports are blank")
            else:
                page.reports.set_column_name(test_data)
                page.reports.check_movement_availability(test_data)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("movement_report_error")
            raise Exception(exp)

    @pytestrail.case(26331830)
    def test_45_export_movement_report(self, page, web_driver, test_data):
        """
        TestCase to verify the export Movement report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            test_data['display_movement_count'] = page.reports.get_total_report_count('Movement Report')
            exported_movement_count = page.reports.export_and_verify_reports("movement")
            assert int(test_data['display_movement_count']) == int(
                exported_movement_count), "Count not matching in movement report after export"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("movement_report_export_report_error")
            raise Exception(exp)

    @pytestrail.case(26323322)
    def test_46_filter_apply_movement_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Filter can be apply on Movement report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_clearance_status()
            page.reports.click_apply()
            if int(test_data['display_movement_count']) > 0:
                assert int(test_data['display_movement_count']) != int(
                    page.reports.get_total_report_count('Movement Report')), \
                    "Filter is not applied successfully"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("location_report_filter_error")
            raise Exception(exp)

    @retry_when_fails(10, 10)
    @pytestrail.case(26328949)
    def test_47_ipm_report(self, page, web_driver, test_data):
        """
        TestCase to verify the IPM report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.apihit.get_in_port_manning_count_api(test_data, side='shore')
            page.reports.open_ipm_report()
            assert test_data['total_ipm_count'] == page.reports.get_total_report_count('IPM Report'), \
                "IPM reports count not matching on UI"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("ipm_report_error")
            raise Exception(exp)

    @pytestrail.case(26331833)
    def test_48_export_ipm_report(self, page, web_driver, test_data):
        """
        TestCase to verify the export IPM report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            test_data['display_ipm_count'] = page.reports.get_total_report_count('IPM Report')
            exported_ipm_count = page.reports.export_and_verify_reports("ipm")
            assert int(test_data['display_ipm_count']) == int(
                exported_ipm_count), "Count not matching in ipm report after export"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("ipm_report_export_error")
            raise Exception(exp)

    @pytestrail.case(26323330)
    def test_49_filter_apply_ipm_report(self, page, web_driver):
        """
        TestCase to verify the Filter can be apply on IPM report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_assignment_status()
            page.reports.click_apply()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(26323317)
    def test_50_logout(self, page, web_driver):
        """
        Test case to logout from Visitor Management
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_logout")
            raise Exception(exp)

    @pytest.mark.SkipForIntEnv
    @pytestrail.case(26323318)
    def test_51_login_with_supervisor_role(self, page, config, web_driver, creds):
        """
        Login with valid credentials of supervisor
        :param page:
        :param config:
        :param web_driver:
        :return:
        """
        username = None
        password = None
        try:
            if config.envMasked == "CERT":
                username = creds.visitormanagement.shore.supervisor.username
                password = creds.visitormanagement.shore.supervisor.password
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username=username, password=password)
            page.select_ship.get_ship_name()
            page.select_ship.select_ship()
            page.dashboard.verification_of_dashboard_visitor()
            if page.dashboard.verify_report_tab_availability():
                raise Exception("Report tab is available")
            else:
                logger.debug("Report tab is not available")
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_error")
            raise Exception(exp)

    @pytest.mark.SkipForIntEnv
    @pytestrail.case(26323320)
    def test_52_login_with_report_manager_role(self, page, config, web_driver, creds):
        """
        Login with valid report manager role
        :param page:
        :param config:
        :param web_driver:
        :return:
        """
        username = None
        password = None
        try:
            if config.envMasked == "CERT":
                username = creds.visitormanagement.shore.manager.username
                password = creds.visitormanagement.shore.manager.password
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username=username, password=password)
            page.select_ship.get_ship_name()
            page.select_ship.select_ship()
            if page.dashboard.verify_report_tab_availability():
                raise Exception("Report tab is available")
            else:
                logger.debug("Report tab is not available")
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_error")
            raise Exception(exp)

    @pytest.mark.SkipForIntEnv
    @pytestrail.case(26323319)
    def test_53_login_with_admin_role(self, page, config, web_driver, creds):
        """
        Login with valid admin role
        :param page:
        :param config:
        :param web_driver:
        :return:
        """
        username = None
        password = None
        try:
            if config.envMasked == "CERT":
                username = creds.visitormanagement.shore.admin.username
                password = creds.visitormanagement.shore.admin.password
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username=username, password=password)
            page.select_ship.get_ship_name()
            page.select_ship.select_ship()
            page.dashboard.verification_of_dashboard_visitor()
            if page.dashboard.verify_report_tab_availability():
                logger.debug("Report tab is available for admin role")
            else:
                raise Exception("Report tab is not available for admin role, which wrong access rights")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_error_admin_role")
            raise Exception(exp)

    @pytestrail.case(26323340)
    @pytest.mark.xfail(reason='DCP-62417')
    def test_54_import_visitor(self, page, test_data, web_driver, creds):
        """
        Import the visitor from excel
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.verification_of_dashboard_visitor()
            test_data['import_visitor_first_name'] = generate_first_name()
            test_data['import_visitor_last_name'] = generate_last_name()
            test_data['import_citizenship'] = "India"
            test_data['import_visitor_id'] = generate_phone_number(8)
            test_data['import_visit_date'] = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime(
                "%d/%m/%Y")
            test_data['import_visitor_name'] = f"{test_data['import_visitor_first_name']} " \
                                               f"{test_data['import_visitor_last_name']}"
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.visitor.verify_import_visitors()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_import_visitor")
            raise Exception(exp)

    @pytestrail.case(37829331)
    def test_55_boarding_slot_available_in_current_voyage(self, page, web_driver, test_data):
        """
        Verify that boarding slots available for current voyage
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username='kapil.gupta', password='633D9jHGQjby')
            page.select_ship.select_ship(test_data)
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.click_boarding_in_left_panel()
            page.boarding.verify_boarding_slot_page()
            page.dashboard.select_active_voyage(test_data['voyage_name_space'])
            page.boarding.availability_of_boarding_data()
            page.dashboard.select_active_voyage_in_boarding_page(test_data['next_voyage_name_shore'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_visitor_count")
            raise Exception(exp)

    @pytestrail.case(37829545)
    def test_56_add_boarding_slots(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            today_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime("%Y-%m-%d")
            embark_date = datetime.strptime(test_data['embarkDate'], "%m/%d/%Y").strftime("%Y-%m-%d")
            debark_date = datetime.strptime(test_data['debarkDate'], "%m/%d/%Y").strftime("%Y-%m-%d")
            if today_date == embark_date or today_date == debark_date:
                page.apihit.get_next_to_next_voyage(test_data)
                page.dashboard.select_active_voyage_in_boarding_page(test_data['next_to_next_voyage_name_shore'])
                page.boarding.set_column_name(test_data)
                test_data['Slot_can_be_added_or_not'] = page.boarding.check_if_slot_can_be_added(test_data)
                page.boarding.click_action_dropdown()
                test_data['added_slot_value'] = page.boarding.add_new_slot(test_data)

            elif today_date != embark_date or today_date != debark_date:
                page.dashboard.select_active_voyage_in_boarding_page(test_data['next_voyage_name_shore'])
                page.boarding.set_column_name(test_data)
                test_data['Slot_can_be_added_or_not'] = page.boarding.check_if_slot_can_be_added(test_data)
                if test_data['Slot_can_be_added_or_not']:
                    page.boarding.click_action_dropdown()
                    test_data['added_slot_value'] = page.boarding.add_new_slot(test_data)
                else:
                    pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(37829544)
    def test_57_edit_capacity(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if test_data['Slot_can_be_added_or_not']:
                capacity = page.boarding.update_capacity(test_data)
                if capacity == '20':
                    logger.debug(f"Capacity is updated for {test_data['added_slot_value']}")
                else:
                    raise Exception(f"Updated Capacity is not display {test_data['added_slot_value']} and value is :"
                                    f"{capacity}")
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(37829547)
    def test_58_disable_slot(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if test_data['Slot_can_be_added_or_not']:
                enabled = page.boarding.enable_disable_slot(test_data, False)
                if enabled == 'False':
                    logger.debug("Slot is Disabled successfully")
                else:
                    raise Exception("Slot is still enabled")
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(37829546)
    def test_59_enable_slot(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if test_data['Slot_can_be_added_or_not']:
                enabled = page.boarding.enable_disable_slot(test_data, True)
                if enabled == 'True':
                    logger.debug("Slot is Disabled successfully")
                else:
                    raise Exception("Slot is still enabled")
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(37829549)
    def test_60_move_slot(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if test_data['Slot_can_be_added_or_not']:
                page.boarding.move_slot(test_data)
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(37829548)
    def test_61_remove_slot(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if test_data['Slot_can_be_added_or_not']:
                if page.boarding.remove_slot(test_data):
                    logger.debug("Slot is removed successfully")
                else:
                    raise Exception("Slot is still display")
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

