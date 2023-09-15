__author__ = 'bhanu.pratap'

import pytest

from virgin_utils import *
from ui_pages.crew_applications.table_management_web.admin_web import TableManagementAdmin
from ui_pages.crew_applications.table_management_web.apihit_web import Apihit
from ui_pages.crew_applications.table_management_web.login_web import TableManagementShipLogin
from ui_pages.crew_applications.table_management_web.host_web import TableManagementHost


@pytest.mark.TABLE_MANAGEMENT_WEB
@pytest.mark.run(order=24)
class TestTableManagementWeb:
    """
    Test Suite to test Table Management Web
    """
    @pytestrail.case(37797589)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, db_core, creds):
        """
        Launch the Crew app and login into table management application
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param test_data:
        :param db_core:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'login', TableManagementShipLogin(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data))
            setattr(page, 'admin', TableManagementAdmin(web_driver))
            setattr(page, 'host', TableManagementHost(web_driver))
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/tableui/"))
            page.login.verification_of_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            page.login.login_into_table_management(username=creds.verticalqa.username, password=creds.verticalqa.password)
            page.login.verify_table_management_dashboard()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_error_popup")
            raise Exception(exp)

    @pytestrail.case(37800921)
    def test_02_verify_availability_of_venues(self, web_driver, page, test_data):
        """
        To verify all availability of all venues
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.hamburger_menus()
            page.admin.choose_module("Host")
            if not page.host.verify_host_module():
                web_driver.allure_attach_jpeg("invalid_host_page_error")
                raise Exception("user not landed on host page")
            test_data['venues'] = page.host.get_venue_list()
            if not page.host.verify_venue_list(venues=test_data['venues']):
                raise Exception("venue list not matching")
            page.host.click_venue_drop_down()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venues_error")
            raise Exception(exp)

    @pytestrail.case(6139372)
    def test_03_verify_venue_background(self, web_driver, page, test_data):
        """
        To verify background of venue is displaying or not
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.click_venue_drop_down()
            page.host.select_venue(test_data)
            if not page.host.verify_background_plan():
                web_driver.allure_attach_jpeg("background_layout_error")
                raise Exception("Background option is not displaying")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venues_background_option_error")
            raise Exception(exp)

    @pytestrail.case(41556470)
    def test_04_verify_current_tab(self, web_driver, page, test_data):
        """
        To verify current tab in admin module
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.hamburger_menus()
            page.admin.choose_module("Admin")
            page.admin.open_current_tab()
            if not page.admin.verify_current_tab(test_data):
                web_driver.allure_attach_jpeg("current_page")
                raise Exception("current voyage is not displaying in current tab")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("current_tab_error")
            raise Exception(exp)

    @pytestrail.case(41556471)
    def test_05_verify_completed_tab(self, web_driver, page, test_data):
        """
        To verify completed tab in admin module
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_completed_tab()
            page.admin.verify_completed_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("completed_tab_error")
            raise Exception(exp)

    @pytestrail.case(41556474)
    def test_06_verify_preset_applied(self, web_driver, page, test_data):
        """
        To verify preset applied for all voyages
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_upcoming_tab()
            if not page.admin.verify_applied_preset():
                web_driver.allure_attach_jpeg("reset_page")
                raise Exception("preset not been applied for upcoming voyage")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("applied_preset_error")
            raise Exception(exp)

    @pytestrail.case(65111306)
    def test_07_add_new_preset(self, web_driver, page, test_data):
        """
        To add new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_manage_preset()
            page.admin.delete_if_already_present()
            test_data['preset_name'] = f"Test Preset - Automation {generate_random_number()}"
            value = test_data['preset_name']
            page.admin.new_preset(value)
            page.admin.verify_created_preset(value)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("add_preset_error")
            raise Exception(exp)

    @pytestrail.case(65111307)
    def test_08_rename_new_preset(self, web_driver, page, test_data):
        """
        To rename new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            value = test_data['preset_name']
            page.admin.find_created_preset(value)
            page.admin.rename_created_preset(test_data)
            if page.admin.verify_rename_preset(test_data['preset_rename']):
                logger.info("preset rename done")
            else:
                raise Exception("preset rename error")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("rename_preset_error")
            raise Exception(exp)

    @pytestrail.case(64605406)
    def test_09_delete_created_preset(self, web_driver, page, test_data):
        """
        To delete new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            value = test_data['preset_rename']
            page.admin.delete_new_preset(value)
            if not page.admin.verify_delete_preset(value):
                web_driver.allure_attach_jpeg("delete preset error")
                raise Exception("Preset not deleted")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_preset_error")
            raise Exception(exp)


    @pytestrail.case(61409290)
    def test_10_verify_logout_from_table_management(self, web_driver, page):
        """
        To verify logout functionality from table management
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.admin.hamburger_menus()
            page.login.click_logout()
            page.login.verify_logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("logout_error")
            raise Exception(exp)