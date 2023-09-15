__author__ = 'HT'

import pytest

from ui_pages.crew_applications.apihit.apihit import Apihit
from virgin_utils import *
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.crew_framework.dashboard import CrewDashboard


@pytest.mark.CREW_FRAMEWORK_UI
@pytest.mark.run(order=17)
class TestCrewFramework:
    """
    Test Suite to test Crew Framework Apk
    """
    @pytestrail.case(37797589)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into table management application
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param test_data:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'login', CrewAppLogin(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'dashboard', CrewDashboard(web_driver))
            page.apihit.get_ship_reservation_details()
            page.login.allow_call_popup()
            if page.login.verify_select_ship():
                web_driver.allure_attach_jpeg("availability_of_virgin_select_ship_page")
            else:
                raise Exception("Invalid select ship page")
            page.login.sign_in(username='vertical-qa', password='4BWm2tz4Xz')
            if not page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("login unsuccessful")
                raise Exception("Error in login")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(6139354)
    def test_02_verify_ui_elements_of_dashboard(self, page, web_driver):
        """
        To verify all the elements on crew dashboard
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.dashboard.verify_dashboard_ui_elements()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dashboard_elements")
            raise Exception(exp)

    @pytestrail.case(6139349)
    def test_03_verify_user_is_able_to_open_sailor_faqs_and_help_center(self, page, web_driver):
        """
        To verify user is able to access frequently asked questions
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.dashboard.open_and_verify_frequently_asked_questions()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("frequently_asked_questions")
            raise Exception(exp)

    @pytestrail.case(6139352)
    def test_04_verify_crew_area_manager_is_able_to_access_defined_functionality(self, page, web_driver):
        """
        To verify crew area manager is able to access defined functionalities
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.dashboard.verify_crew_are_manager_is_able_to_access_defined_functionality()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cam_hamburger_menu_modules")
            raise Exception(exp)

    @pytestrail.case(58599895)
    def test_05_verify_nearby_toggle_button_in_settings(self, page, web_driver):
        """
        To verify user is able to see toggle button in settings page
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.dashboard.verify_toggle_button_in_settings()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("toggle_button")
            raise Exception(exp)

    @pytestrail.case(6139353)
    def test_06_verify_user_is_able_reset_sailor_pin(self, page, web_driver, test_data):
        """
        To verify user is able to reset sailor PIN
        :return:
        :param web_driver:
        :param test_data:
        :param page:
        """
        try:
            page.dashboard.reset_sailor_pin(test_data[
                                                'searched_sailor_name'], test_data['searched_sailor_stateroom'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_pin_reset")
            raise Exception(exp)

    @pytestrail.case(6139350)
    def test_07_verify_runer_is_able_to_access_defined_functionality(self, page, web_driver):
        """
        To verify runner is able to access defined functionality
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.login.sign_in(username="DJYOTI01", password="Test@1234")
            page.login.verify_create_pin_page()
            page.dashboard.verify_runner_is_able_to_access_defined_functionality()
            page.login.click_logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("runner_hamburger_menu_modules")
            raise Exception(exp)

    @pytestrail.case(6139351)
    def test_08_verify_delivery_manager_is_able_to_access_defined_functionality(self, page, web_driver):
        """
        To verify delivery manager is able to access defined functionality
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.login.wait_for_select_ship_page()
            page.login.sign_in(username="HJHA01", password="Test@1234")
            page.login.verify_create_pin_page()
            page.dashboard.verify_delivery_manager_is_able_to_access_defied_functionalities()
            page.login.click_logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("runner__housekeeping_modules")
            raise Exception(exp)

    @pytestrail.case(68970403)
    def test_09_verify_box_office_manager_is_able_to_access_defined_functionality(self, page, web_driver):
        """
        To verify box office manager is able to access defined functionality
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.login.wait_for_select_ship_page()
            page.login.sign_in(username="VKHOLI01", password="Test@1234")
            page.login.verify_create_pin_page()
            page.dashboard.verify_box_office_manager_is_able_to_access_defied_functionalities()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("box_office_manager_suport_queue_module")
            raise Exception(exp)

    @pytestrail.case(44927561)
    def test_10_verify_login_with_invalid_user(self, page, web_driver, test_data):
        """
        To verify crew app login with sailor credential
        :return:
        :param web_driver:
        :param page:
        """
        try:
            page.login.click_logout()
            page.login.wait_for_select_ship_page()
            page.login.verify_invalid_login(username=test_data['guestEmail'], password="Voyages@9876")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("login_with_invalid_user")
            raise Exception(exp)