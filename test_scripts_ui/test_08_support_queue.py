__author__ = 'vanshika.arora'

import pytest

from virgin_utils import *
from ui_pages.support_queue.apihit import Apihit
from ui_pages.support_queue.login import Login
from ui_pages.support_queue.dashboard import Dashboard
from ui_pages.support_queue.new_chat import NewChat
from ui_pages.support_queue.canned_message import CannedMessage
from ui_pages.support_queue.filter import Filter


@pytest.mark.SUPPORT_QUEUE
@pytest.mark.run(order=7)
class TestSupportQueue:
    """
    Test Suite to test Support Queue
    """
    @pytestrail.case(6139338)
    def test_01_login_support_queue(self, page, config, web_driver, rest_shore, test_data, creds):
        """
        Login support queue with authenticated credentials
        :param page:
        :param config:
        :param web_driver:
        :param rest_shore:
        :param test_data:
        """
        try:
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data))
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', Dashboard(web_driver))
            setattr(page, 'new_chat', NewChat(web_driver))
            setattr(page, 'canned_message', CannedMessage(web_driver))
            setattr(page, 'filter', Filter(web_driver))

            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            get_ship_date(config, rest_shore, test_data)
            page.apihit.get_sailor_details(flag=True)
            download_path = os.getcwd() + '/downloaded_files/'
            if not os.path.isdir(download_path):
                os.makedirs(download_path)
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/supportQueue/login"))
            page.login.verification_of_login_page()
            page.login.login_into_support_queue(username=creds.supportqueue.login.username, password=creds.supportqueue.login.password)
            page.dashboard.verify_support_queue_header_on_top_right_corner()
            page.dashboard.availability_of_search_option()
            page.dashboard.availability_of_new_chat_button()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("login_support_queue")
            raise Exception(exp)

    @pytestrail.case(6139339)
    def test_02_initiate_chat_with_sailor(self, page, test_data, web_driver):
        """
        Initiate chat with sailor
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_new_chat_button()
            page.new_chat.search_sailor(test_data['searched_sailor_stateroom'])
            page.new_chat.click_searched_sailor(test_data)
            page.dashboard.verify_sailor_details_header_on_right_side()
            page.dashboard.verify_sailor_name_in_sailor_details(test_data['sailor_name'])
            page.dashboard.send_message(test_data)
        except(Exception, ValueError)as exp:
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
            page.dashboard.verify_sailor_in_progress_section(test_data['sailor_name'])
        except(Exception, ValueError)as exp:
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
            page.canned_message.create_canned_message(test_data)
            page.canned_message.verify_canned_message(test_data)
        except(Exception, ValueError)as exp:
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
            page.dashboard.verify_sent_message(test_data['canned_message'])
            page.canned_message.delete_canned_message(test_data['canned_message'])
        except(Exception, ValueError)as exp:
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
            page.dashboard.send_media_item_in_message()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("send_media_items_into_chat")
            raise Exception(exp)

    @pytestrail.case(41557139)
    def test_07_send_hyperlink_to_sailor(self, page, web_driver):
        """
        Send hyperlink to sailor and verify that it is clickable from conversation
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.send_hyperlink_to_sailor()
            page.dashboard.verify_clickable_hyperlink()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("send_hyperlink_to_sailor")
            raise Exception(exp)

    @pytestrail.case(6139344)
    def test_08_search_chat_by_keyword(self, page, web_driver, test_data):
        """
        Function to verify search chat by keyword
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.verify_search_chat_by_keyword(test_data)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("search_chat_by_keyword")
            raise Exception(exp)

    @pytestrail.case(65499537)
    def test_09_own_request(self, page, web_driver):
        """
        Function to verify crew is able to own the request
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.own_the_request()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("own_request")
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
            page.dashboard.mark_chat_status_to_resolved()
            page.dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom'], test_data['sailor_name'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("mark_chat_status_to_resolved")
            raise Exception(exp)

    @pytestrail.case(45235569)
    def test_11_apply_filters_for_today_and_yesterday(self, page, web_driver, test_data):
        """
        Function to apply filters of today and yesterday
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_filter_icon()
            page.filter.apply_filter_for_day('Yesterday',test_data)
            page.dashboard.click_filter_icon()
            page.filter.apply_filter_for_day('All', test_data)
            page.dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom'], test_data['sailor_name'])
            page.dashboard.click_filter_icon()
            page.filter.apply_filter_for_day('Date Range', test_data)
            page.dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom'], test_data['sailor_name'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("apply_filters_for_today_and_yesterday")
            raise Exception(exp)

    @pytestrail.case(6139343)
    def test_12_access_history_of_resolved_request(self, page, web_driver, test_data):
        """
        Verify that crew should be able to access history of resolved requests
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_new_chat_button()
            page.new_chat.search_sailor(test_data['sailor_name'])
            page.new_chat.click_searched_sailor(test_data)
            page.dashboard.send_message(test_data)
            page.dashboard.open_resolved_chat(test_data['sailor_name'])
            page.dashboard.verify_history_of_resolved_request(test_data['canned_message'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("access_history_of_resolved_request")
            raise Exception(exp)

    @pytestrail.case(6139348)
    def test_13_apply_filters(self, page, web_driver, test_data):
        """
        Verify that crew should be able to apply filters
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_filter_icon()
            page.filter.apply_vip_filters()
            page.filter.get_list_of_vip_filters(test_data)
            page.dashboard.click_filter_icon()
            page.filter.clear_filter()
            page.filter.apply_filter_and_verify(test_data, False)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("apply_filters")
            raise Exception(exp)

    @pytestrail.case(69496420)
    def test_14_apply_multiple_filters(self, page, web_driver, test_data):
        """
        Verify that crew should be able to apply multiple filters
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_filter_icon()
            page.filter.apply_vip_filters()
            page.filter.get_list_of_vip_filters(test_data)
            page.dashboard.click_filter_icon()
            page.filter.clear_filter()
            page.filter.apply_filter_and_verify(test_data, True)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("apply_filters")
            raise Exception(exp)

    @pytestrail.case(68159907)
    def test_15_filter_using_deck_and_cabin(self, page, web_driver, test_data):
        """
        filter using deck and cabin cta in filters
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_filter_icon()
            page.filter.apply_filter_for_cabin(test_data['searched_sailor_stateroom'])
            page.dashboard.verify_chat_mark_as_resolved(test_data['searched_sailor_stateroom'], test_data['sailor_name'])
            page.dashboard.click_filter_icon()
            page.filter.clear_filter_applied_for_deck()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cabin_and_deck_filter")
            raise Exception(exp)

    @pytestrail.case(44927569)
    def test_16_logout_and_verify_invalid_login_with_sailor_credentials(self, page, web_driver):
        """
        To verify user shouldn't login with sailor credentials to application
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.logout()
            page.login.verification_of_login_page()
            page.login.login_into_support_queue(username='harrypotter123@gmail.com', password='Yellow*99')
            page.login.verify_invalid_login_toast()
            page.login.verification_of_login_page()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("logout_and_verify_invalid_login_with_sailor_credentails")
            raise Exception(exp)