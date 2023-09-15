__author__ = 'aatir.fayyaz'

import pytest

from virgin_utils import *
from ui_pages.crew_applications.apihit.apihit import Apihit
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.crew_framework.dashboard import CrewDashboard
from ui_pages.crew_applications.support_queue.sq_dashboard import SupportQueue
from ui_pages.crew_applications.support_queue.new_chat import NewChat
from ui_pages.crew_applications.support_queue.enter_chat import EnterChat
from ui_pages.crew_applications.support_queue.canned_message import CannedMessage
from ui_pages.crew_applications.support_queue.filter import Filter


@pytest.mark.CREW_SUPPORT_QUEUE
@pytest.mark.run(order=19)
class TestCrewSupportQueue:
    """
    Test Suite to test Support Queue Apk
    """
    @pytestrail.case(6139338)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into Support Queue Application
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param test_data:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'login', CrewAppLogin(web_driver))
            setattr(page, 'dashboard', CrewDashboard(web_driver))
            setattr(page, 'sq_dashboard', SupportQueue(web_driver))
            setattr(page, 'new_chat', NewChat(web_driver))
            setattr(page, 'enter_chat', EnterChat(web_driver))
            setattr(page, 'canned_message', CannedMessage(web_driver))
            setattr(page, 'filter', Filter(web_driver))
            page.apihit.get_ship_reservation_details()
            page.login.allow_call_popup()
            if page.login.verify_select_ship():
                web_driver.allure_attach_jpeg("availability_of_virgin_select_ship_page")
            else:
                raise Exception("Invalid select ship page")
            page.login.sign_in(username=creds.supportqueue.login.username, password=creds.supportqueue.login.password)
            if not page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("login unsuccessful")
                raise Exception("Error in login")
            page.login.verify_crew_dashboard()
            page.dashboard.open_crew_app_module(module_name='Support Queue', module_heading='Support Queue')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(6139339)
    def test_02_initiate_chat_with_sailor(self, page, web_driver, test_data):
        """
        To verify that crew is able to add sailor to new request list
        :return:
        :param web_driver:
        :param page:
        :param test_data:
        """
        try:
            page.sq_dashboard.verify_support_queue_header()
            page.sq_dashboard.availability_of_new_chat_button()
            page.sq_dashboard.click_new_chat_button()
            page.new_chat.search_sailor(test_data['searched_sailor_stateroom_1'])
            page.new_chat.click_searched_sailor(test_data)
            page.new_chat.send_message(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("initiate_chat_with_sailor")
            raise Exception(exp)

    @pytestrail.case(6139340)
    def test_03_verify_chat_status_in_progress_after_initiating_chat(self, page, test_data, web_driver):
        """
        Verify that initiated chat should have status in progress
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.sq_dashboard.verify_support_queue_header()
            page.sq_dashboard.verify_sailor_in_progress_section(test_data['sailor_name'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_chat_status_in_progress_after_initiating_chat")
            raise Exception(exp)

    @pytestrail.case(6139346)
    def test_04_create_canned_message(self, page, web_driver, test_data):
        """
        Verify creating canned message
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.sq_dashboard.open_sailor_chat(test_data['sailor_name'])
            page.canned_message.create_canned_message(test_data)
            page.canned_message.verify_canned_message(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("create_canned_message")
            raise Exception(exp)

    @pytestrail.case(6139347)
    def test_05_send_canned_message(self, page, web_driver, test_data):
        """
        Send Canned message
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.canned_message.send_canned_message(test_data['canned_message'])
            page.enter_chat.verify_sent_message(test_data['canned_message'])
            page.canned_message.delete_canned_message(test_data['canned_message'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("send_canned_message")
            raise Exception(exp)

    @pytestrail.case(6139345)
    def test_06_send_media_items_into_chat(self, page, web_driver):
        """
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.enter_chat.send_media_item_in_message()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("send_media_items_into_chat")
            raise Exception(exp)

    @pytestrail.case(6139344)
    def test_07_search_chat_by_keyword(self, page, web_driver, test_data):
        """
        Function to verify search chat by keyword
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.enter_chat.verify_search_chat_by_keyword(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("search_chat_by_keyword")
            raise Exception(exp)

    @pytestrail.case(59426966)
    def test_08_own_request(self, page, web_driver, test_data):
        """
        Function to verify crew is able to own the request
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.sq_dashboard.open_sailor_chat(test_data['sailor_name'])
            page.enter_chat.own_the_request()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("own_request")
            raise Exception(exp)

    @pytestrail.case(41557139)
    def test_09_send_hyperlink_to_sailor(self, page, web_driver, test_data):
        """
        Send hyperlink to sailor and verify that it is clickable from conversation
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.enter_chat.send_hyperlink_to_sailor()
            page.enter_chat.verify_clickable_hyperlink()
            page.sq_dashboard.back_to_crew_dashboard()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("send_hyperlink_to_sailor")
            raise Exception(exp)

    @pytestrail.case(6139341)
    def test_10_mark_chat_status_to_resolved(self, page, web_driver, test_data):
        """
        Mark chat status to resolved after resolving sailor's query
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.open_crew_app_module(module_name='Support Queue', module_heading='Support Queue')
            page.sq_dashboard.open_sailor_chat(test_data['sailor_name'])
            page.enter_chat.mark_chat_status_to_resolved()
            page.sq_dashboard.verify_support_queue_header()
            page.sq_dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom_1'],
                                                           test_data['sailor_name'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("mark_chat_status_to_resolved")
            raise Exception(exp)

    @pytestrail.case(6139343)
    def test_11_access_history_of_resolved_request(self, page, web_driver, test_data):
        """
        Verify that crew should be able to access history of resolved requests
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.sq_dashboard.verify_history_of_resolved_request(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("access_history_of_resolved_request")
            raise Exception(exp)

    @pytestrail.case(45235569)
    def test_12_apply_filters_for_today_and_yesterday(self, page, web_driver, test_data):
        """
        Function to apply filters of today and yesterday
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.sq_dashboard.click_filter_icon()
            page.filter.apply_filter_for_day('Yesterday', test_data)
            page.sq_dashboard.click_filter_icon()
            page.filter.apply_filter_for_day('All', test_data)
            page.sq_dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom_1'],
                                                           test_data['sailor_name'])
            page.sq_dashboard.back_to_filter()
            page.filter.apply_filter_for_day('Date Range', test_data)
            page.sq_dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom_1'],
                                                           test_data['sailor_name'])
            page.sq_dashboard.back_to_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("apply_filters_for_today_and_yesterday")
            raise Exception(exp)

    @pytestrail.case(68159907)
    def test_13_filter_using_deck_and_cabin(self, page, web_driver, test_data):
        """
        filter using deck and cabin cta in filters
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.filter.apply_filter_for_deck_cabin(test_data)
            page.filter.verify_deck_cabin_filters(test_data)
            page.sq_dashboard.click_filter_icon()
            page.filter.clear_filter_applied_for_deck_cabin()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cabin_and_deck_filter")
            raise Exception(exp)

    @pytestrail.case([69496420, 6139348])
    def test_14_apply_multiple_filters(self, page, web_driver, test_data):
        """
        Verify that crew should be able to apply multiple filters
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.sq_dashboard.click_filter_icon()
            page.filter.vip_filters()
            page.filter.filter_by_owner()
            page.filter.sort_by_filter()
            page.filter.apply_filters()
            page.filter.verify_filters()
            page.sq_dashboard.click_filter_icon()
            page.filter.clear_all_filters()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("apply_multiple_filters")
            raise Exception(exp)

    @pytestrail.case(44927569)
    def test_15_logout_and_verify_invalid_login_with_sailor_credentials(self, page, web_driver, test_data):
        """
        To verify crew is not able to login with sailor credential
        :return:
        :param web_driver:
        :param page:
        :param test_data:
        """
        try:
            page.sq_dashboard.back_to_crew_dashboard()
            page.login.click_hamburger_menu()
            page.login.click_logout()
            page.login.verify_logout()
            page.login.wait_for_select_ship_page()
            page.login.verify_invalid_login(username=test_data['guestEmail'], password="Voyages@9876")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("login_with_invalid_user")
            raise Exception(exp)