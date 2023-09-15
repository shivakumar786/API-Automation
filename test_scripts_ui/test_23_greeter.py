__author__ = 'HT'

import pytest

from ui_pages.crew_applications.apihit.apihit import Apihit
from virgin_utils import *
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.crew_framework.dashboard import CrewDashboard
from ui_pages.crew_applications.greeter.greeter_dashboard import GreeterDashboard


@pytest.mark.GREETER_UI
@pytest.mark.run(order=23)
class TestGreeter:
    """
    Test Suite to verify Greeter Apk
    """
    @pytestrail.case(6036362)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into Crew Application
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
            setattr(page, 'greeter_dashboard', GreeterDashboard(web_driver, test_data))
            page.apihit.get_ship_reservation_details()
            page.login.allow_call_popup()
            if page.login.verify_select_ship():
                web_driver.allure_attach_jpeg("availability_of_virgin_select_ship_page")
            else:
                raise Exception("Invalid select ship page")
            page.login.sign_in(username='Shubhra.Vyas', password='Gomo7411')
            if not page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("login unsuccessful")
                raise Exception("Error in login")
            page.dashboard.open_crew_app_module("GREETER")
            page.dashboard.click_on_greeter_module()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(6036364)
    def test_02_greeter_dashboard_settings_ui_elements(self, web_driver, page):
        """
        Verify greeter dashboard and settings screen elements
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.verify_greeter_dashboard_elements()
            page.greeter_dashboard.verify_settings_tab_elements()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("greeter_dashboard_elements")
            raise Exception(exp)

    @pytestrail.case(6036365)
    def test_03_select_activity_from_settings_page(self, web_driver, page):
        """
        select activity from settings dropdown and check for information
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.select_activity_from_drop_down()
            page.greeter_dashboard.save_non_inventoried_activity()
            page.greeter_dashboard.verify_information_of_selected_activity()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("activity_selection_from_settings")
            raise Exception(exp)

    @pytestrail.case([6036361, 6036367, 6036368, 57430590])
    def test_04_book_activity_for_sailor_from_greeter(self, web_driver, page):
        """
        book activity for sailor from greeter application
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.book_activity_for_sailor_from_greeter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("activity_booking")
            raise Exception(exp)

    @pytestrail.case(6036363)
    def test_05_verify_checkin_history(self, web_driver, page):
        """
        Verify checkin history for sailors checkin done from greeter
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.verify_history_after_booking_and_checkin_from_greeter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("greeter_checkin_history")
            raise Exception(exp)

    @pytestrail.case(71101184)
    def test_06_greet_again_after_un_greeted_from_history_page(self, web_driver, page):
        """
        To verify user is abe to check in sailor again after un check from history page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.checkin_again_from_sailor_details_page()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("greet_again_from_sailor_details")
            raise Exception(exp)

    @pytestrail.case(63153742)
    def test_07_verify_booking_conflict(self, web_driver, page):
        """
        Verify Booking conflict error message
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.greeter_dashboard.verify_booking_conflict()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("greeter_booking _conflict")
            raise Exception(exp)