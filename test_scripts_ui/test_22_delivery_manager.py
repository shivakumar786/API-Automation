_author_ = 'sudhansh.arora'

import pytest
from ui_pages.crew_applications.apihit.apihit import Apihit
from virgin_utils import *
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.delivery_manager.selection import Selection
from ui_pages.crew_applications.delivery_manager.scheduled import Scheduled


@pytest.mark.DELIVERY_MANAGER_UI
@pytest.mark.run(order=22)
class TestDeliverymanager:
    """
    Test Suite to test delivery manager
    """

    @pytestrail.case(70811775)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into delivery application
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
            setattr(page, 'Selection', Selection(web_driver))
            setattr(page, 'scheduled', Scheduled(web_driver))

            page.login.allow()
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

    @pytestrail.case(5966421)
    def test_02_open_delivery_manager(self, page, web_driver):
        """
         Test for Opening delivery manager
         :param web_driver:
         :param page:
         :return:
         """
        try:
            page.scheduled.click_hamburger_menu()
            page.scheduled.select_delivery_manager()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("select_delivery_manager")
            raise Exception(exp)

    @pytestrail.case(63928128)
    def test_03_select_venue(self, page, web_driver):
        """
        Selection of venue
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.select_bell_box()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("select_venue")
            raise Exception(exp)

    @pytestrail.case(70811776)
    def test_04_open_pending_tab(self, page, web_driver):
        """
        to verify pending tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_pending")
            raise Exception(exp)

    @pytestrail.case(5966422)
    def test_05_verify_pending_tab(self, page, web_driver):
        """
        to open scheduled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.verify_pending()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_scheduled_tab")
            raise Exception(exp)

    @pytestrail.case(70811777)
    def test_06_open_scheduled_tab(self, page, web_driver):
        """
        to open pending tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_scheduled_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(5966418)
    def test_07_place_on_deck(self, page, web_driver):
        """
        to open scheduled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.place_on_deck()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(70812269)
    def test_08_ondeck_tab(self, page, web_driver):
        """
        to open ondeck tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_OnDeck_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_ondeck_tab")
            raise Exception(exp)

    @pytestrail.case(5966419)
    def test_09_bump_order(self, page, web_driver):
        """
        to open scheduled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.bump_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(70811774)
    def test_10_cart_tab(self, page, web_driver):
        """
        to open cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cart_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_cart_tab")
            raise Exception(exp)

    @pytestrail.case(70812270)
    def test_11_delivered_tab(self, page, web_driver):
        """
        to open delivered tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.delivered_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delivered_tab")
            raise Exception(exp)

    @pytestrail.case(70812271)
    def test_12_cancelled_tab(self, page, web_driver):
        """
        cancelled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cancelled_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cancelled_tab")
            raise Exception(exp)

    @pytestrail.case(186239)
    def test_13_deliver_order(self, page, web_driver):
        """
        to open deliver order
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cart_tab()
            page.scheduled.deliver_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("deliver_order")
            raise Exception(exp)

    @pytestrail.case(70812272)
    def test_14_verify_ondeck_tab(self, page, web_driver):
        """
        to open pending tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_OnDeck_tab()
            page.scheduled.verify_ondeck()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_ondeck")
            raise Exception(exp)

    @pytestrail.case(70812273)
    def test_15_verify_cart_tab(self, page, web_driver):
        """
        to verify cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cart_tab()
            page.scheduled.verify_cart()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_cart")
            raise Exception(exp)

    @pytestrail.case(70812274)
    def test_16_verify_delivered_tab(self, page, web_driver):
        """
        to verify delivered tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.delivered_tab()
            page.scheduled.verify_delivered()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_delivered")
            raise Exception(exp)

    @pytestrail.case(70812275)
    def test_17_verify_cancelled_tab(self, page, web_driver):
        """
        to verify cancelled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cancelled_tab()
            page.scheduled.verify_cancelled()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_cancelled")
            raise Exception(exp)

    @pytestrail.case(186237)
    def test_18_wait_time(self, page, web_driver):
        """
        to open wait time
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_wait_times()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_wait_time")
            raise Exception(exp)

    @pytestrail.case(63928127)
    def test_19_verify_scheduled_tab(self, page, web_driver):
        """
        verify scheduled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.cart_tab()
            page.scheduled.open_OnDeck_tab()
            page.scheduled.open_pending_tab()
            page.scheduled.open_scheduled_tab
            page.scheduled.verify_scheduled()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_scheduled_tab")
            raise Exception(exp)

    @pytestrail.case(71590710)
    def test_20_wait_time_ondeck(self, page, web_driver):
        """
        to verify waity time functionality on ondeck tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_OnDeck_tab()
            page.scheduled.open_wait_times()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_wait_time")
            raise Exception(exp)

    @pytestrail.case(186238)
    def test_21_wait_time_cart(self, page, web_driver):
        """
        to verify waity time functionality on cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_OnDeck_tab()
            page.scheduled.cart_tab()
            page.scheduled.open_wait_times()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_wait_time")
            raise Exception(exp)

    @pytestrail.case(63929958)
    def test_22_get_order_details(self, page, web_driver):
        """
        to verify order details
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
            page.scheduled.order_details()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(63929951)
    def test_23_notify_soon(self, page, web_driver):
        """
        to notify about order rediness as soon
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
            page.scheduled.notify_soon()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(71590708)
    def test_24_notify_fifteen_mins(self, page, web_driver):
        """
        to notify about order rediness as fifteen mins
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
            page.scheduled.notify_fifteen_mins()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(71590709)
    def test_25_notify_thirty_mins(self, page, web_driver):
        """
        to notify about order rediness as fifteen mins
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
            page.scheduled.notify_thirty_mins()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(63931782)
    def test_26_cancel_order(self, page, web_driver):
        """
        to cancel order fully
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_pending_tab()
            page.scheduled.cancel_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(63929949)
    def test_27_filter_preorder_slots(self, page, web_driver):
        """
        to filter preorder slots
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.scheduled.open_scheduled_tab()
            page.scheduled.filter_mealperiod()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_scheduled_tab")
            raise Exception(exp)