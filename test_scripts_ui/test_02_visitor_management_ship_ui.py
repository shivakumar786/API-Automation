__author__ = 'prahlad.sharma'

import pytest

from ui_pages.embarkation_supervisor.alert_message import Alertmessage
from ui_pages.embarkation_supervisor.apihit import Apihit
from ui_pages.embarkation_supervisor.ipm_report import IPM_reports
from ui_pages.embarkation_supervisor.reports import Reports
from ui_pages.embarkation_supervisor.sailors import Sailorscrew
from ui_pages.visitor_management.filter import Filter
from virgin_utils import *
from ui_pages.embarkation_supervisor.supervisor_login import SupervisorLogin
from ui_pages.embarkation_supervisor.dashboard import Dashboard
from ui_pages.visitor_management.select_ship_shore import SelectShip
from ui_pages.visitor_management.visitors import Visitors
from ui_pages.embarkation_supervisor.boarding_slots import Boarding_slots
import pathlib


@pytest.mark.VISITOR_MANAGEMENT_SHIP_UI
@pytest.mark.run(order=2)
class TestVisitorManagementShip:
    """
    Test Suite to test Embarkation Supervisor
    """

    @pytestrail.case(6440480)
    def test_01_launch_website_and_check_invalid_login(self, web_driver, config, page, rest_shore, test_data):
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
            setattr(page, 'sailor_crew', Sailorscrew(web_driver))
            setattr(page, 'filter', Filter(web_driver))
            setattr(page, 'alert_message', Alertmessage(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data))
            setattr(page, 'reports', Reports(web_driver))
            setattr(page, 'ipm_reports', IPM_reports(web_driver))
            setattr(page, 'boarding', Boarding_slots(web_driver))
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/embarkation-supervisor/login"))
            download_path = os.getcwd() + '/downloaded_files/'
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            file = pathlib.Path(download_path + 'visitors.csv')
            if file.exists():
                os.remove(file)
            file = pathlib.Path(download_path + 'exception.csv')
            if file.exists():
                os.remove(file)
            page.login.verification_of_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            page.login.login_into_embarkation_supervisor(username='verticalieoer', password='abcd123')
            page.login.verification_of_invalid_login_toast()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_error_popup")
            raise Exception(exp)

    @pytestrail.case(6440481)
    def test_02_login(self, page, config, test_data, web_driver, creds):
        """
        Login with valid credentials
        :param page:
        :param config:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.login.verification_of_login_page()
            test_data['reviewer'] = 'Vijay Tiwari'
            page.login.login_into_embarkation_supervisor(username=creds.visitormanagement.ship.login.username,
                                                         password=creds.visitormanagement.ship.login.password)
            page.dashboard.verification_of_dashboard_visitor()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_error")
            raise Exception(exp)

    @pytestrail.case(26262923)
    def test_03_verify_active_voyage(self, page, test_data, web_driver):
        """
        select the active voyage
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_sailor_details()
            page.apihit.get_crew_details()
            page.apihit.get_visitor_details_ship()
            page.apihit.get_next_voyage(test_data)
            test_data['visitor_first_name'] = generate_first_name()
            test_data['visitor_last_name'] = generate_last_name()
            test_data['citizenship'] = "United States"
            test_data['visitor_name'] = f"{test_data['visitor_first_name']} {test_data['visitor_last_name']}"

            # page.dashboard.get_active_voyage_name(test_data['voyage_name'])
            web_driver.allure_attach_jpeg("active_voyage")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_verify_voyage")
            raise Exception(exp)

    @pytestrail.case(26339978)
    def test_04_verify_dashboard(self, page, test_data, web_driver):
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
            page.dashboard.availability_of_in_port_manning()
            page.dashboard.availability_of_report()
            page.dashboard.availability_of_ship_date_time()
            page.dashboard.availability_of_copyright_info()
            page.dashboard.availability_of_ship_name(test_data['shipName'])

            page.dashboard.click_view_more()
            page.dashboard.availability_of_onboard_sailor()
            page.dashboard.availability_of_ashore_sailor()
            page.dashboard.availability_of_sailor_checked_out()
            page.dashboard.availability_of_sailor_total_embarking_today()
            page.dashboard.availability_of_sailor_total_leaving_today()
            page.dashboard.availability_of_sailor_sailor_with_alerts()
            page.dashboard.availability_of_sailor_us()
            page.dashboard.availability_of_sailor_need_assistance()

            page.dashboard.availability_of_crew_embarking_today()
            page.dashboard.availability_of_crew_checked_in()
            page.dashboard.availability_of_crew_onboard()
            page.dashboard.availability_of_crew_ashore()
            page.dashboard.availability_of_crew_leaving_today()

            page.dashboard.availability_of_visitor_expected_today()
            page.dashboard.availability_of_visitor_approved()
            page.dashboard.availability_of_visitor_onboard()
            page.dashboard.availability_of_visitor_ashore()
            page.dashboard.availability_of_visitor_checkout()
            page.dashboard.availability_of_visitor_rejected()
            test_data['visitorExpectedCount'] = page.dashboard.get_expected_today_visitor_count()
            test_data['visitorApprovedCount'] = page.dashboard.get_approved_visitor_count()
            test_data['visitorRejectedCount'] = page.dashboard.get_rejected_visitor_count()
            test_data['visitorPendingCount'] = page.dashboard.get_approval_pending_visitor_count()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_dashboard")
            raise Exception(exp)

    @pytestrail.case(26328034)
    def test_05_match_sailor_count(self, page, web_driver):
        """
        Match the total visitor count
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.match_total_sailors()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_count")
            raise Exception(exp)

    @pytestrail.case(2917006)
    def test_06_sailor_percentage_of_statuses(self, page, web_driver):
        """
        Match the total visitor count
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.verify_percent_of_checked_in_onboard()
            page.dashboard.verify_percent_of_checked_in_not_onboard()
            page.dashboard.verify_percent_of_rts_completed_approved()
            page.dashboard.verify_percent_of_rts_completed_approval_pending()
            page.dashboard.verify_percent_of_rts_not_completed()
            page.dashboard.verify_percent_of_not_checked_in_onboard()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_percent")
            raise Exception(exp)

    @pytestrail.case(26328035)
    def test_07_match_crew_count(self, page, web_driver):
        """
        Match the crew count which is sum of On board and Ashore count
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.match_total_crew()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_crew_count")
            raise Exception(exp)

    @pytestrail.case(25782202)
    def test_08_match_visitor_count(self, page, web_driver):
        """
        Match the total visitor count
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.match_total_visitor()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_visitor_count")
            raise Exception(exp)

    @pytestrail.case(6440464)
    def test_09_on_board_ashore_visitor(self, page, web_driver):
        """
        TestCase to verify onboard and ashore count should be click-able and count should match
        :param page:
        :param web_driver:
        :return:
        """
        try:
            onboard_count = page.dashboard.get_onboard_visitor_count()
            if onboard_count > 0:
                pytest.skip("Onboard count is not clickable")
                page.dashboard.click_onboard_count()
                list_count = page.visitor.get_count_on_list()
                assert list_count == onboard_count, "On-board count is not matching"
            else:
                logger.debug("On-board count is 0")

            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            ashore_count = page.dashboard.get_ashore_visitor_count()
            if ashore_count > 0:
                pytest.skip("Ashore count is not clickable")
                page.dashboard.click_ashore_count()
                list_count = page.visitor.get_count_on_list()
                assert list_count == ashore_count, "Ashore count is not matching"
            else:
                logger.debug("Ashore count is 0")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(6440462)
    def test_10_sailor_click_able_counts(self, page, web_driver):
        """
        TestCase to verify sailor click able counts
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            onboard_count = page.dashboard.get_sailor_onboard_count()
            if onboard_count > 0:
                page.dashboard.click_sailor_onboard_count()
                page.visitor.verification_of_page_header('Sailors')
                if page.visitor.blank_list():
                    raise Exception("Sailor list is blank")
            else:
                logger.debug("On-board sailor count is 0")

            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.click_view_more()
            ashore_count = page.dashboard.get_sailor_ashore_count()
            if ashore_count > 0:
                page.dashboard.click_sailor_ashore_count()
                page.visitor.verification_of_page_header('Sailors')
                if page.visitor.blank_list():
                    raise Exception("Sailor list is blank")
            else:
                logger.debug("Ashore sailor count is 0")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_sailor")
            raise Exception(exp)

    @pytestrail.case(6440465)
    def test_11_crew_click_able_counts(self, page, web_driver):
        """
        TestCase to verify crew click able counts
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            onboard_count = page.dashboard.get_crew_onboard_count()
            if onboard_count > 0:
                page.dashboard.click_crew_onboard_count()
                page.visitor.verification_of_page_header('Crew')
                if page.visitor.blank_list():
                    web_driver.allure_attach_jpeg("error_blank_crew_on_board_count")
                    raise Exception("Crew list is blank for on board count ")
            else:
                logger.debug("On-board Crew count is 0")

            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            ashore_count = page.dashboard.get_crew_ashore_count()
            if ashore_count > 0:
                page.dashboard.click_crew_ashore_count()
                page.visitor.verification_of_page_header('Crew')
                if page.visitor.blank_list():
                    web_driver.allure_attach_jpeg("error_blank_crew_ashore_count")
                    raise Exception("Crew list is blank for ashore count")
            else:
                logger.debug("Ashore Crew count is 0")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_crew_counts")
            raise Exception(exp)

    @pytestrail.case(6440439)
    def test_12_advance_search_sailor(self, page, test_data, web_driver):
        """
        TestCase to verify the Search with Sailor first name, last name, state room, booking number
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.enter_search_keywords(test_data['searched_sailor_stateroom'])
            page.dashboard.open_sailor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_sailor_name'], 'StateRoom')

            page.dashboard.enter_search_keywords(test_data['searched_sailor_booking'])
            page.dashboard.open_sailor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_sailor_name'], 'Reservation Number')

            page.dashboard.enter_search_keywords(test_data['searched_sailor_ln'])
            page.dashboard.open_sailor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_sailor_name'], 'LastName')

            page.dashboard.enter_search_keywords(test_data['searched_sailor_fn'])
            page.dashboard.open_sailor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_sailor_name'], 'FirstName')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_search_sailor")
            raise Exception(exp)

    @pytestrail.case(6440440)
    def test_13_advance_search_crew(self, page, test_data, web_driver):
        """
        TestCase to verify the Search with Crew first name, last name, Employee No
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            page.dashboard.enter_search_keywords(test_data['searched_crew_emp_num'])
            page.dashboard.open_crew_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_crew_name'], 'Employee Number')

            page.dashboard.enter_search_keywords(test_data['searched_crew_ln'])
            page.dashboard.open_crew_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_crew_name'], 'LastName')

            page.dashboard.enter_search_keywords(test_data['searched_crew_fn'])
            page.dashboard.open_crew_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_crew_name'], 'FirstName')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_search_crew")
            raise Exception(exp)

    @pytestrail.case(6440441)
    def test_14_advance_search_visitor(self, page, test_data, web_driver):
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
            page.dashboard.verify_search_result(test_data['searched_visitor_name'], 'DOB')

            page.dashboard.enter_search_keywords(test_data['searched_doc_number'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_visitor_name'], 'Doc Number')

            page.dashboard.enter_search_keywords(test_data['searched_ln'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_visitor_name'], 'LastName')

            page.dashboard.enter_search_keywords(test_data['searched_fn'])
            page.dashboard.open_visitor_tab_in_global_search()
            page.dashboard.verify_search_result(test_data['searched_visitor_name'], 'FirstName')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_search_visitor")
            raise Exception(exp)

    @pytestrail.case(26334722)
    def test_15_sailor_export(self, page, web_driver):
        """
        TestCase to verify sailor export
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_sailor_tab()
            page.visitor.verification_of_page_header('Sailors')
            page.visitor.verify_export('guests')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_export")
            raise Exception(exp)

    @pytestrail.case(26334721)
    def test_16_see_sailor_list(self, page, web_driver):
        """
        TestCase to verify sailor list is display and verify the count
        :param page:
        :param web_driver:
        :return:
        """
        # TODO count verification in excel after export
        try:
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_filter")
            raise Exception(exp)

    @pytestrail.case(26335701)
    def test_17_sailor_filter(self, page, test_data, web_driver):
        """
        TestCase to verify sailor list is display and verify the count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.sailor_crew.click_filter_option()
            page.filter.click_citizenship()
            page.filter.select_country(test_data['citizenship'])
            page.filter.click_sailor_apply()
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            else:
                page.sailor_crew.view_first_sailor()
                assert test_data['citizenship'] == page.sailor_crew.get_sailor_citizenship(), "Citizenship is not " \
                                                                                              "matching "
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_filter")
            raise Exception(exp)

    @pytestrail.case(26334724)
    def test_18_crew_export(self, page, web_driver):
        """
        TestCase to verify crew export
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_crew_tab()
            page.visitor.verification_of_page_header('Crew')
            page.visitor.verify_export('crew')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_crew_export")
            raise Exception(exp)

    @pytestrail.case(26334723)
    def test_19_see_crew_list(self, page, web_driver):
        """
        TestCase to verify crew list is display and verify the count
        :param page:
        :param web_driver:
        :return:
        """
        # TODO count verification in excel after export
        try:
            if page.visitor.blank_list():
                raise Exception("Crew list is blank")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_crew_list")
            raise Exception(exp)

    @pytestrail.case(26335702)
    def test_20_crew_filter(self, page, web_driver):
        """
        TestCase to verify crew filter option
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.sailor_crew.click_crew_filter_option()
            page.filter.click_checkin_status()
            page.filter.select_checked_in()
            page.filter.click_apply()
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            else:
                page.sailor_crew.view_first_crew()
                assert 'Checked-In' == page.sailor_crew.get_crew_checked_in_status(), "Correct checked in status " \
                                                                                      "is display"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_crew_filter")
            raise Exception(exp)

    @pytestrail.case(6740702)
    def test_21_add_visitor(self, page, test_data, web_driver):
        """
        add the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            page.dashboard.verification_of_dashboard_visitor()
            test_data['visitorExpectedCount'] = page.dashboard.get_expected_today_visitor_count()
            test_data['visitorApprovedCount'] = page.dashboard.get_approved_visitor_count()
            test_data['visitorRejectedCount'] = page.dashboard.get_rejected_visitor_count()
            test_data['visitorPendingCount'] = page.dashboard.get_approval_pending_visitor_count()
            page.dashboard.click_refresh_icon()
            ship_date = page.dashboard.get_ship_time_ui()
            test_data["visit_date"] = ship_date.rsplit(" ")[2].replace(",", "")
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.visitor.click_add_visitor()
            page.visitor.fill_visitor_form_and_save(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                    test_data['citizenship'], test_data['reviewer'],
                                                    test_data["visit_date"], test_data, side='ship')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(31473367)
    def test_22_verify_visitor_pending_count(self, page, test_data, web_driver):
        """
        Check Visitor approval pending count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_dashboard_in_left_panel()
            assert test_data['visitorApprovedCount'] +1 == page.dashboard.get_approved_visitor_count(), \
                'Visitor approved count did not get increased after creating new visitor !!'
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(26328943)
    def test_23_visitor_filter(self, page, test_data, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_visitor_list_filter")
            raise Exception(exp)

    @pytestrail.case(26335212)
    def test_24_visitor_on_list(self, page, test_data, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_visitor_list")
            raise Exception(exp)

    @pytest.mark.skip(reason='DCP-109029')
    @pytestrail.case(26332326)
    def test_25_export_visitor(self, page, web_driver, test_data):
        """
        Export the visitor
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_visitor_tab()
            if page.visitor.blank_list():
                pytest.skip("Visitors not available")
            page.apihit.get_active_voyage_itinerary(test_data)
            page.ipm_reports.get_list_of_dates_and_ports_from_backend(test_data)
            page.visitor.get_current_portcode(test_data)
            today_date = date.today().strftime("%m-%d-%Y")
            portcode = test_data['current_portcode']
            if test_data['current_portcode']:
                file_name = f'Visitors_ScarletLady_{today_date}_{portcode}'
            else:
                file_name = f'Visitors_ScarletLady_{today_date}'
            page.visitor.verify_visitor_export(file_name)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_export_visitor")
            raise Exception(exp)

    @pytestrail.case(6740705)
    def test_26_info_visitor(self, page, test_data, web_driver):
        """
        Info the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verify_visitor_get_added(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                  test_data['citizenship'], 'ID', test_data, test_data["visit_date"])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_info_visitor")
            raise Exception(exp)

    @pytestrail.case(25811572)
    def test_27_edit_visitor(self, page, test_data, web_driver):
        """
        Edit the visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.set_column_name(test_data)
            page.visitor.view_visitor(test_data)
            page.visitor.click_edit_visitor()
            test_data['visitor_first_name'] = page.visitor.edit_visitor()
            test_data['visitor_name'] = f"{test_data['visitor_first_name']} {test_data['visitor_last_name']}"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_edit_visitor")
            raise Exception(exp)

    @pytestrail.case(6740704)
    def test_28_reject_visitor(self, page, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_reject_visitor")
            raise Exception(exp)

    @pytestrail.case(6740703)
    def test_29_approve_visitor(self, page, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_approve_visitor")
            raise Exception(exp)

    @pytestrail.case(31474126)
    def test_30_verify_visitor_approved_count(self, page, test_data, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(31474128)
    def test_31_verify_visitor_rejected_count(self, page, test_data, web_driver):
        """
        Check Visitor rejected count
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            assert test_data[
                       'visitorRejectedCount'] == page.dashboard.get_rejected_visitor_count(), \
                'Visitor rejected count did not get increased after rejecting visitor !!'

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_add_visitor")
            raise Exception(exp)

    @pytestrail.case(26340954)
    def test_32_create_alert(self, page, test_data, web_driver):
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
            page.visitor.verify_visitor_get_added(test_data['visitor_first_name'], test_data['visitor_last_name'],
                                                  test_data['citizenship'], 'ID', test_data, test_data["visit_date"])

            page.visitor.set_column_name(test_data)
            page.visitor.view_visitor(test_data)
            page.visitor.open_more_option_drawer_details()
            page.visitor.click_create_alert()
            test_data['alert_text'] = f'alert for visitor at {datetime.now()}'
            page.visitor.create_alert(test_data['alert_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_create_alert")
            raise Exception(exp)

    @pytestrail.case(26339979)
    def test_33_verification_alert_on_alert_tab(self, page, test_data, web_driver):
        """
        TestCase to verify the alert after creation, in alert Tab
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_alert_after_creation(test_data['alert_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_verify_alert")
            raise Exception(exp)

    @pytestrail.case(6440444)
    def test_34_verification_alert_on_details(self, page, test_data, web_driver):
        """
        TestCase to verify the alert after creation, in alert Tab
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_alert_on_details_screen(test_data['alert_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_verify_alert_on_details")
            raise Exception(exp)

    @pytestrail.case(6440448)
    def test_35_edit_alert_and_verify(self, page, test_data, web_driver):
        """
        Test case to edit the alert and verification
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data['updated_alert_text'] = "alert for visitor after edit"
            page.visitor.edit_alert_and_verify(test_data['updated_alert_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_edit_alert")
            raise Exception(exp)

    @pytestrail.case(6440449)
    def test_36_delete_alert(self, page, web_driver):
        """
        Test case to Delete the alert
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.delete_alert()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_delete_alert")
            raise Exception(exp)

    @pytestrail.case(26340955)
    def test_37_create_message(self, page, test_data, web_driver):
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
            test_data['message_text'] = f'message for visitor at {datetime.now()}'
            page.visitor.create_message(test_data['message_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_create_message")
            raise Exception(exp)

    @pytestrail.case(26348163)
    def test_38_verification_message_on_message_tab(self, page, test_data, web_driver):
        """
        TestCase to verify the message after creation, in message Tab
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_message_after_creation(test_data['message_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_message_verification")
            raise Exception(exp)

    @pytestrail.case(6440446)
    def test_39_verification_of_message_on_details(self, page, test_data, web_driver):
        """
        TestCase to verify the alert after creation, in message details screen
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.verification_of_message_on_details_screen(test_data['message_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_message_verify_details")
            raise Exception(exp)

    @pytestrail.case(6440447)
    def test_40_edit_message_and_verify(self, page, test_data, web_driver):
        """
        Test case to edit the message and verification
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data['updated_message_text'] = "message for visitor after edit"
            page.visitor.edit_message_and_verify(test_data['updated_message_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_edit_message")
            raise Exception(exp)

    @pytestrail.case(6440450)
    def test_41_delete_message(self, page, web_driver):
        """
        Test case to Delete the message
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.visitor.delete_message()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_delete_message")
            raise Exception(exp)

    @pytestrail.case(6740707)
    def test_42_add_new_visit(self, page, test_data, web_driver):
        """
        Test case to add the visit in already created visitor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data["additional_visit_purpose"] = 'testing in additional visit'
            page.visitor.add_additional_visit(test_data["additional_visit_purpose"], test_data["visit_date"],
                                              test_data['reviewer'], 'ship')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_new_visit")
            raise Exception(exp)

    @pytestrail.case(6740709)
    def test_43_bulk_visitor_approve(self, page, web_driver, test_data):
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
            test_data['lastNames'] = page.visitor.select_custom_visitors_by_id_number(test_data['ID Number_position'],
                                                                                      10, test_data)
            page.visitor.all_approve()
            page.visitor.verify_toast_title()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_bulk_visitor_approve")
            raise Exception(exp)

    @pytestrail.case(31597790)
    def test_44_verify_bulk_visitor_approve(self, page, web_driver, test_data):
        """
        Test case to verify the status of bulk approved visitor
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            today_date = date.today().strftime("%m-%d-%Y")
            page.apihit.get_active_voyage_itinerary(test_data)
            page.ipm_reports.get_list_of_dates_and_ports_from_backend(test_data)
            page.visitor.get_current_portcode(test_data)
            if test_data['current_portcode']:
                portcode = test_data['current_portcode']
                file_name = f'Visitors_ScarletLady_{today_date}_{portcode}'
            else:
                file_name = f'Visitors_ScarletLady_{today_date}'
            page.visitor.verify_visitor_export(file_name)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_bulk_visitor_verify")
            raise Exception(exp)

    @pytestrail.case(26356401)
    def test_45_search_visitor(self, page, test_data, web_driver):
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
            page.dashboard.verify_search_result(test_data['visitor_name'], 'Global Search')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_search_visitor")
            raise Exception(exp)

    @pytestrail.case(26337165)
    def test_46_sailor_create_alert(self, page, web_driver, test_data):
        """
        TestCase to verify the bulk alert for sailor
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_sailor_tab()
            page.visitor.verification_of_page_header('Sailors')
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            page.sailor_crew.click_checkbox()
            page.sailor_crew.click_action()
            page.sailor_crew.click_create_alert()
            page.visitor.verification_of_page_header('Create Alert')
            test_data['sailor_alert_text'] = f"alert for sailors {datetime.now()}"
            page.visitor.create_alert(test_data['sailor_alert_text'])
            page.sailor_crew.view_first_sailor()
            # page.visitor.verification_of_alert_description_after_creation(test_data['sailor_alert_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_create_alert")
            raise Exception(exp)

    @pytestrail.case(26337653)
    def test_47_sailor_create_message(self, page, web_driver, test_data):
        """
        TestCase to verify the bulk message for sailor
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_sailor_tab()
            page.visitor.verification_of_page_header('Sailors')
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            page.sailor_crew.click_checkbox()
            page.sailor_crew.click_action()
            page.sailor_crew.click_create_message()
            page.visitor.verification_of_page_header('Create Message')
            test_data['sailor_message_text'] = f"message for sailors {datetime.now()}"
            page.visitor.create_message(test_data['sailor_message_text'])
            page.sailor_crew.view_first_sailor()
            # page.visitor.verification_of_message_description_after_creation(test_data['sailor_message_text'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_create_message")
            raise Exception(exp)

    @pytestrail.case(6440452)
    def test_48_login_with_supervisor_role(self, page, web_driver, creds):
        """
        TestCase to change the embarkation slots for bulk sailors
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username=creds.visitormanagement.ship.supervisor.username,
                                                         password=creds.visitormanagement.ship.supervisor.password)
            page.dashboard.verification_of_dashboard_visitor()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_login_with_supervisor_role")
            raise Exception(exp)

    @pytestrail.case(26338119)
    def test_49_sailor_change_embark_slots(self, page, web_driver):
        """
        TestCase to change the embarkation slots for bulk sailors
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_sailor_tab()
            page.visitor.verification_of_page_header('Sailors')
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            page.sailor_crew.click_checkbox()
            page.sailor_crew.click_action()
            page.sailor_crew.click_change_embark_slot()
            page.visitor.verification_of_page_header('Change Boarding Slot')
            boarding_time = page.sailor_crew.select_boarding_time()
            page.sailor_crew.click_update_button()
            page.sailor_crew.view_first_sailor()
            display_time = page.sailor_crew.get_boarding_time_on_details()
            if display_time == boarding_time:
                logger.debug(f"Boarding time is display correct on details page {display_time} and selected time is "
                             f"{boarding_time}")
            else:
                raise Exception(f"Boarding time is not display correct on details page {display_time} "
                                f"and selected time is {boarding_time}")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_change_debark_slot")
            raise Exception(exp)

    @pytestrail.case(40881804)
    def test_50_add_boarding_slots(self, page, web_driver, test_data):
        """
        TestCase to verify add the new Boarding slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_boarding_in_left_panel()
            page.boarding.verify_boarding_slot_page()
            page.boarding.set_column_name(test_data)
            test_data['Slot_can_be_added_or_not'] = page.boarding.check_if_slot_can_be_added(test_data)
            if test_data['Slot_can_be_added_or_not']:
                page.boarding.click_action_dropdown()
                test_data['added_slot_value'] = page.boarding.add_new_slot(test_data)
            else:
                pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(40881803)
    def test_51_edit_capacity(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(40881806)
    def test_52_disable_slot(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(40881805)
    def test_53_enable_slot(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(40881808)
    def test_54_move_slot(self, page, web_driver, test_data):
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
            if today_date == embark_date:
                if test_data['Slot_can_be_added_or_not']:
                    page.boarding.move_slot(test_data)
                else:
                    pytest.skip("Boarding slot cannot be added as slot starting time is set after 11:45pm")
            else:
                pytest.skip("Slots cannot be moved after embark date")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(40881807)
    def test_55_remove_slot(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_on_board_ashore_visitor")
            raise Exception(exp)

    @pytestrail.case(41565060)
    def test_56_verify_active_boarding_slot(self, page, test_data, web_driver):
        """
        Test case to verify active boarding slot
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.boarding.click_checkbox(test_data)
            page.boarding.active_boarding_slot()
            page.boarding.verify_active_boarding_slot(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_edit_message")
            raise Exception(exp)

    @pytestrail.case(41565061)
    def test_57_verify_inactive_boarding_slot(self, page, test_data, web_driver):
        """
        Test case to verify inactive boarding slot
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.boarding.click_checkbox(test_data)
            page.boarding.inactive_boarding_slot()
            page.boarding.verify_inactive_boarding_slot(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_edit_message")
            raise Exception(exp)

    @pytestrail.case(40881802)
    def test_58_boarding_slot_available_in_upcoming_voyage(self, page, web_driver, test_data, creds):
        """
        Verify that boarding slots available for current voyage
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_boarding_in_left_panel()
            page.dashboard.select_active_voyage(test_data['next_voyage_name_shore'])
            page.boarding.availability_of_boarding_data()
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
            page.login.verification_of_login_page()
            page.login.login_into_embarkation_supervisor(username=creds.visitormanagement.ship.bordingslot.username,
                                                         password=creds.visitormanagement.ship.bordingslot.password)
            page.dashboard.verification_of_dashboard_visitor()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_visitor_count")
            raise Exception(exp)

    @pytestrail.case(26336677)
    def test_59_sailor_reservation_parties(self, page, web_driver):
        """
        TestCase to verify reservation Parties
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_sailor_tab()
            page.visitor.verification_of_page_header('Sailors')
            if page.visitor.blank_list():
                raise Exception("Sailor list is blank")
            page.sailor_crew.click_include_reservation_party()
            if page.sailor_crew.verify_list_in_reservation_party_level():
                logger.debug('Sailor list is converted in Reservation party level')
            else:
                raise Exception(f"Sailor list is converted in Reservation party level")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sailor_reservation_parties")
            raise Exception(exp)

    @pytestrail.case(6440473)
    def test_60_passenger_search(self, page, web_driver, test_data):
        """
        TestCase to verify the search the Passenger in add alert and message screen
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_alert_message_in_left_panel()
            page.alert_message.click_new_alert()
            page.visitor.verification_of_page_header('Create Alert')
            try:
                page.alert_message.click_add_passenger()
                page.alert_message.search_passengers(test_data['searched_sailor_stateroom'])
                test_data[
                    'sailor_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
                page.alert_message.click_add_button()
                page.alert_message.verify_added_passenger(test_data['sailor_passenger'])
            except Exception as exp:
                page.alert_message.click_add_passenger()
                page.alert_message.search_passengers(test_data['searched_sailor_fn'])
                test_data[
                    'sailor_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
                page.alert_message.click_add_button()
                page.alert_message.verify_added_passenger(test_data['sailor_passenger'])

            page.alert_message.click_add_passenger()
            page.alert_message.search_passengers(test_data['searched_crew_fn'])
            test_data[
                'crew_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
            page.alert_message.click_add_button()
            page.alert_message.verify_added_passenger(test_data['crew_passenger'])

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("add_passenger_error_in_search")
            raise Exception(exp)

    @pytestrail.case(6440442)
    def test_61_create_bulk_alerts(self, page, web_driver, test_data):
        """
        TestCase to verify the bulk alert for passenger
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            test_data['bulk_alert_text'] = f"Bulk alert for passengers {datetime.now()}"
            page.visitor.create_alert(test_data['bulk_alert_text'])
            page.visitor.verification_of_alert_description_after_creation(test_data['bulk_alert_text'])

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("bulk_alert_error")
            raise Exception(exp)

    @pytestrail.case(6440443)
    def test_62_create_bulk_message(self, page, web_driver, test_data):
        """
        TestCase to verify the bulk message for passenger
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.alert_message.click_new_message()
            page.visitor.verification_of_page_header('Create Message')
            try:
                page.alert_message.click_add_passenger()
                page.alert_message.search_passengers(test_data['searched_sailor_stateroom'])
                test_data[
                    'sailor_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
                page.alert_message.click_add_button()
                page.alert_message.verify_added_passenger(test_data['sailor_passenger'])
            except Exception as exp:
                page.alert_message.click_add_passenger()
                page.alert_message.search_passengers(test_data['searched_sailor_fn'])
                test_data[
                    'sailor_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
                page.alert_message.click_add_button()
                page.alert_message.verify_added_passenger(test_data['sailor_passenger'])

            page.alert_message.click_add_passenger()
            page.alert_message.search_passengers(test_data['searched_crew_fn'])
            test_data[
                'crew_passenger'] = page.alert_message.click_checkbox_on_passenger_search_and_get_passenger_name()
            page.alert_message.click_add_button()
            page.alert_message.verify_added_passenger(test_data['crew_passenger'])

            test_data['bulk_message_text'] = f"Bulk message for passengers {datetime.now()}"
            page.visitor.create_message(test_data['bulk_message_text'])
            page.alert_message.click_message_tab()
            page.visitor.verification_of_message_description_after_creation(test_data['bulk_message_text'])

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("bulk_message_error")
            raise Exception(exp)

    @pytestrail.case(6440458)
    def test_63_missing_image_report(self, page, web_driver, test_data):
        """
        TestCase to verify the missing image exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='ship')
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.apihit.get_missing_picture_count_api(side='ship')
            page.reports.open_exception_report()
            assert test_data['total_missing_picture_count'] == page.reports.get_missing_picture_count(), \
                "missing picture count not matching"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("missing_image_exception_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-111978')
    @pytestrail.case(26331834)
    def test_64_export_missing_image_report(self, page, web_driver):
        """
        TestCase to verify the export the missing image report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            # assert test_data['total_missing_picture_count'] == page.reports.export_and_verify_reports("exception"),\
            # "Missing image count is not matching after download the CSV"
            page.reports.export_and_verify_reports("exception")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("export_missing_image_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(6440463)
    def test_65_not_checked_in_onboard_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Not Checked in On board exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='ship')
            page.apihit.get_not_checked_in_onboard_count_api(side='ship')
            assert test_data['total_not_checked_in_count'] == page.reports.get_not_checkedin_onboard_count(), \
                "Not Checked in On board count not matching on UI"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("expire_card_exception_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-111978')
    @pytestrail.case(29743195)
    def test_66_export_not_checked_in_onboard_report(self, page, web_driver):
        """
        TestCase to verify the export the Not Checked in On board report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.export_and_verify_reports("exception")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("export_expire_card_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(6440460)
    def test_67_checked_in_not_onboard_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Checked in Not On board exception report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='ship')
            page.apihit.get_checked_in_not_onboard_count_api(side='ship')
            assert test_data['total_checked_in_count'] == page.reports.get_checked_in_not_onboard_count(), \
                "Checked in but Not On board count not matching on UI"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("expire_card_exception_report_error")
            raise Exception(exp)

    @pytestrail.case(6440436)
    def test_68_cbp_report(self, page, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cbp_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-116853')
    @pytestrail.case(26331837)
    def test_69_export_cbp_report(self, page, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cbp_report_export_report_error")
            raise Exception(exp)

    @pytestrail.case(26332327)
    def test_70_filter_apply_cbp_report(self, page, web_driver):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("CBP_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440457)
    def test_71_location_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Location report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.reports.open_location_history_report()
            if page.reports.blank_list():
                raise Exception("Location reports are blank")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("location_report_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-111978')
    @pytestrail.case(26331836)
    def test_72_export_location_report(self, page, web_driver, test_data):
        """
        TestCase to verify the export Location report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            test_data['display_location_count'] = page.reports.get_total_location_count()
            exported_sailor_location_count = page.reports.export_and_verify_reports("Sailor Location History")
            assert int(test_data['display_location_count']) == int(
                exported_sailor_location_count), "Count not matching in location report " \
                                          "after export"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("location_report_export_report_error")
            raise Exception(exp)

    @pytestrail.case(6440459)
    def test_73_filter_apply_location_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Filter can be apply on Location report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_gender()
            page.reports.select_boarding_status()
            page.reports.click_apply()
            if int(test_data['display_location_count']) > 0:
                assert int(test_data['display_location_count']) != int(page.reports.get_total_location_count()), \
                    "Filter is not applied successfully"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("location_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440455)
    def test_74_movement_report(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("movement_report_error")
            raise Exception(exp)

    @pytestrail.case(26331835)
    def test_75_export_movement_report(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("movement_report_export_report_error")
            raise Exception(exp)

    @pytestrail.case(6440456)
    def test_76_filter_apply_movement_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Filter can be apply on Movement report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_gender()
            page.reports.select_clearance_status()
            page.reports.click_apply()
            if int(test_data['display_movement_count']) > 0:
                assert int(test_data['display_movement_count']) != int(
                    page.reports.get_total_report_count('Movement Report')), \
                    "Filter is not applied successfully"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("location_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(28822399)
    def test_77_ipm_report(self, page, web_driver, test_data):
        """
        TestCase to verify the IPM report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.apihit.get_in_port_manning_count_api(test_data, side='ship')
            page.reports.open_ipm_report()
            assert test_data['total_ipm_count'] == page.reports.get_total_report_count('IPM Report'), \
                "IPM reports count not matching on UI"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_error")
            raise Exception(exp)

    @pytestrail.case(26331838)
    def test_78_export_ipm_report(self, page, web_driver, test_data):
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
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_export_error")
            raise Exception(exp)

    @pytestrail.case(6440466)
    def test_79_filter_apply_ipm_report(self, page, web_driver, test_data):
        """
        TestCase to verify the Filter can be apply on IPM report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.reports.click_filter_option()
            page.reports.select_assignment_status()
            page.reports.click_apply()
            if int(test_data['display_ipm_count']) > 0:
                assert int(test_data['display_ipm_count']) != int(page.reports.get_total_report_count('IPM Report')), \
                    "Filter is not applied successfully"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440476)
    def test_80_ipm_report_past_days_disabled(self, page, web_driver, test_data):
        """
        TestCase to verify the past days should not be click able
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        test_data['report_data'] = dict()
        current_ship_date = test_data["visit_date"]
        try:
            page.dashboard.open_ipm_reports_tab()
            page.ipm_reports.verification_of_ipm_report_page()
            page.ipm_reports.open_calendar()
            page.ipm_reports.check_previous_dates_not_click_able(current_ship_date)

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_past_day_error")
            raise Exception(exp)

    @pytestrail.case(6440477)
    def test_81_verify_date_wise_voyage_itinerary(self, page, web_driver, test_data):
        """
        TestCase to verify the future day should be click able that have ports
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_active_voyage_itinerary(test_data)
            page.ipm_reports.get_list_of_dates_and_ports_from_backend(test_data)
            page.ipm_reports.verify_date_wise_voyage_itinerary(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440478)
    def test_82_ipm_report_future_days_click(self, page, web_driver, test_data):
        """
        TestCase to verify the future day should be click able that have ports
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        test_data['report_data'] = dict()
        current_ship_date = test_data["visit_date"]
        try:
            page.ipm_reports.check_future_dates_click_able(current_ship_date, test_data)
            page.ipm_reports.get_selected_date_month_year(test_data)
            page.ipm_reports.get_selected_port_group(test_data)
            if test_data['report_data']['date'] == test_data['report_data']['cal_date']:
                logger.info("correct date is display on Report dashboard")
            else:
                raise Exception(f"Date is mismatch, Dashboard:{test_data['report_data']['date']}, Calendar : "
                                f"{test_data['report_data']['cal_date']} ")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440479)
    def test_83_ipm_report_group_assignment(self, page, web_driver, test_data):
        """
        TestCase to verify the group assignment
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            group_list = ['A', 'B', 'C', 'D']
            page.ipm_reports.get_selected_port_group(test_data)
            if test_data['report_data']['group'].strip() == "No Group Assigned for this date":
                group_name = random.choice([group for group in group_list])
            else:
                selected_group = test_data['report_data']['group'].strip().split(" ")[1]
                group_name = random.choice([group for group in group_list if group != selected_group])
            page.ipm_reports.open_assign_group()
            page.ipm_reports.select_group(group_name)
            page.ipm_reports.set_column_name_ipm_report(test_data)
            page.ipm_reports.get_selected_port_group(test_data)
            if test_data['report_data']['group'].strip().split(" ")[1] == group_name:
                logger.info("Correct group is assigned")
            else:
                raise Exception(f"{group_name}: Group is not selected after assignment")
            page.ipm_reports.get_data_for_assigned_group(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("group_assignment_error")
            raise Exception(exp)

    @pytestrail.case(26328950)
    def test_84_data_displayed_in_port_manning_report(self, page, web_driver, test_data):
        """
        TestCase to verify data displayed In Port Manning report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_reports_tab()
            page.reports.verification_of_report_page()
            page.reports.open_ipm_report()
            page.reports.click_filter_option()
            page.filter.select_start_date(test_data['report_data']['port_date'])
            page.filter.select_end_date(test_data['report_data']['port_date'])
            page.filter.select_assigned_group(test_data)
            page.reports.click_apply()
            page.reports.set_column_name(test_data)
            page.ipm_reports.availability_of_data_in_ipm_report(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_data_displayed_in_ipm_report")
            raise Exception(exp)

    @pytestrail.case(6440471)
    def test_85_ipm_edit_assignment(self, page, web_driver, test_data):
        """
        TestCase to verify In Port Manning report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_ipm_reports_tab()
            page.ipm_reports.verification_of_ipm_report_page()
            page.ipm_reports.set_column_name_ipm_report(test_data)
            page.ipm_reports.edit_assignment(test_data)
            was_selected = page.ipm_reports.check_uncheck_box(test_data)
            row_number = page.ipm_reports.get_row_number_for_matched_data(test_data)
            group_name = page.ipm_reports.group_name_in_report_for_crew(test_data, row_number)
            if was_selected:
                assert group_name == '-', f"Group name not matching: {group_name}, selected:{was_selected}"
            else:
                assert group_name == test_data['crew_data']['edit_Group'], f"Group name not matching: {group_name}, " \
                                                                           f"selected:{was_selected} "
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytest.mark.xfail(reason='DCP-112115')
    @pytestrail.case(6440472)
    def test_86_ipm_remove_assignment(self, page, web_driver, test_data):
        """
        TestCase to verify In Port Manning report
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.ipm_reports.set_column_name_ipm_report(test_data)
            page.ipm_reports.remove_assignment(test_data)
            row_number = page.ipm_reports.get_row_number_for_matched_data_after_un_assign(test_data)
            group_name = page.ipm_reports.group_name_in_report_for_crew(test_data, row_number)
            assert group_name == '-', f"Group name not matching: {group_name}"

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ipm_report_filter_error")
            raise Exception(exp)

    @pytestrail.case(6440451)
    def test_87_logout(self, page, web_driver):
        """
        Test case to logout from Visitor Management
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_logout")
            raise Exception(exp)

    @pytestrail.case(6740708)
    @pytest.mark.skip(reason='DCP-62417')
    def test_88_import_visitor(self, page, test_data, web_driver):
        """
        Import the visitor from excel
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            test_data['import_visitor_first_name'] = generate_first_name()
            test_data['import_visitor_last_name'] = generate_last_name()
            test_data['import_citizenship'] = "India"
            test_data['import_visitor_id'] = generate_phone_number(8)
            test_data['import_visit_date'] = datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").strftime(
                "%d/%m/%Y")
            test_data[
                'import_visitor_name'] = f"{test_data['import_visitor_first_name']} " \
                                         f"{test_data['import_visitor_last_name']}"
            page.dashboard.click_visitor_tab()
            page.visitor.verification_of_page_header('Visitors')
            page.visitor.import_visitors(test_data['import_visitor_first_name'], test_data['import_visitor_last_name'],
                                         test_data['import_citizenship'], test_data['import_visitor_id'],
                                         test_data['import_visit_date'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_import_visitor")
            raise Exception(exp)
