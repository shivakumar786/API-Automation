__author__ = 'sudhansh.arora'

import pytest
from ui_pages.crew_applications.apihit.apihit import Apihit
from virgin_utils import *
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.Server.select_venue import SelectVenue
from ui_pages.crew_applications.Server.pending import Pending
from ui_pages.crew_applications.Server.OnDeck import OnDeck
from ui_pages.crew_applications.Server.cart import Cart
from ui_pages.crew_applications.Server.delivered import Deliver
from ui_pages.crew_applications.crew_framework.dashboard import CrewDashboard


@pytest.mark.SERVER_UI
@pytest.mark.run(order=21)
class TestServer:
    """
    Test Suite to test Crew Framework Apk
    """
    @pytestrail.case(365)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into server application
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
            setattr(page, 'SelectVenue',SelectVenue(web_driver))
            setattr(page, 'pending',Pending(web_driver))
            setattr(page, 'OnDeck', OnDeck(web_driver))
            setattr(page, 'Cart', Cart(web_driver))
            setattr(page, 'delivered', Deliver(web_driver))

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

    @pytestrail.case(357)
    def test_02_open_server(self,page,web_driver):
        """
        Test for Opening Server
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.click_hamburger_menu()
            page.select_venue.select_server()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("select_server")
            raise Exception(exp)

    @pytestrail.case(356)
    def test_03_select_venue(self,page,web_driver):
        """
        Selection of venue
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("select_venue")
            raise Exception(exp)

    @pytestrail.case(6036332)
    def test_04_enable_notification(self,page,web_driver):
        """
        test to enable notification
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.enable_notifications()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("enable_notifications")
            raise Exception(exp)

    @pytestrail.case(358)
    def test_05_pending_tab(self, page, web_driver):
        """
        to open pending tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_pending_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_pending_tab")
            raise Exception(exp)

    @pytestrail.case(359)
    def test_06_ondeck_tab(self, page, web_driver):
        """
        to open ondeck tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_OnDeck_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_ondeck_tab")
            raise Exception(exp)

    @pytestrail.case(361)
    def test_07_cart_tab(self, page, web_driver):
        """
        to open cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_cart_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("open_cart_tab")
            raise Exception(exp)

    @pytestrail.case(363)
    def test_08_delivered_tab(self, page, web_driver):
        """
        to open delivered tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.delivered_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delivered_tab")
            raise Exception(exp)

    @pytestrail.case(70467208)
    def test_09_cancelled_tab(self, page, web_driver):
        """
        cancelled tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.cancelled_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cancelled_tab")
            raise Exception(exp)

    @pytestrail.case(360)
    def test_10_bump_order(self, page, web_driver):
        """to bump order on the ondeck tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_OnDeck_tab()
            page.OnDeck.bump_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("bump_order")
            raise Exception(exp)


    @pytestrail.case(362)
    def test_11_deliver_order(self, page, web_driver):
        """
        to deliver order from the cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_cart_tab()
            page.OnDeck.deliver_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("deliver_order")
            raise Exception(exp)

    @pytestrail.case(70467207)
    def test_12_filter_pending(self, page, web_driver):
        """
        use filter on the pending tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_pending_tab()
            page.OnDeck.filter_pending()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter_pending")
            raise Exception(exp)

    @pytestrail.case(6036319)
    def test_13_filter_ondeck(self, page, web_driver):
        """
        use filter on the ondeck tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_OnDeck_tab()
            page.OnDeck.filter_ondeck()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter_pending")
            raise Exception(exp)

    @pytestrail.case(6036322)
    def test_14_filter_cart(self, page, web_driver):
        """
        use filter on the cart tab
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.select_venue.select_server()
            page.select_venue.select_bell_box()
            page.pending.open_cart_tab()
            page.OnDeck.filter_cart()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter_pending")
            raise Exception(exp)