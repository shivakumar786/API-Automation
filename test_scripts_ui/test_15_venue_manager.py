__author__ = 'H T Krishnakumara'

from virgin_utils import *
from ui_pages.venue_manager.apihit import Apihit
from ui_pages.venue_manager.login import VenueManagerLogin
from ui_pages.venue_manager.dashboard import VenueManagerDashboard
from ui_pages.venue_manager.orders import VenueManagerOrders
from ui_pages.venue_manager.select_venue import SelectVenue
from ui_pages.venue_manager.menu import Menu
from ui_pages.venue_manager.staff import Staff
from ui_pages.venue_manager.settings import Settings
from ui_pages.venue_manager.reports_and_metrics import ReportsAndMetrics


@pytest.mark.VENUE_MANAGER_UI
@pytest.mark.run(order=15)
class TestVenueManager:
    """
    Test ui suite to run Venue Manager
    """

    @pytestrail.case(44927571)
    def test_01_login_using_invalid_user(self, page, web_driver, config, test_data, rest_shore, rest_ship, creds,
                                         db_core):
        """
        To verify login behaviour using invalid user(used sailor credential)
        :param rest_ship:
        :param rest_shore:
        :param test_data:
        :param config:
        :param db_core:
        :param page:
        :param creds:
        :param web_driver:
        """
        try:
            setattr(page, 'apihit', Apihit(config, rest_shore, rest_ship, test_data, creds, db_core))
            setattr(page, 'login', VenueManagerLogin(web_driver))
            setattr(page, 'dashboard', VenueManagerDashboard(web_driver))
            setattr(page, 'orders', VenueManagerOrders(web_driver))
            setattr(page, 'venue', SelectVenue(web_driver))
            setattr(page, 'menu', Menu(web_driver))
            setattr(page, 'staff', Staff(web_driver))
            setattr(page, 'settings', Settings(web_driver))
            setattr(page, 'reports', ReportsAndMetrics(web_driver))
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/fnbvenuemanager/login"))
            page.apihit.get_data_shipboard()
            page.apihit.get_guest_details_ship_side()
            assert 'Venue Manager' == page.login.verify_login_page_header(), 'failed to verify venuemanager login page header'
            guest_user = test_data['shipSideGuests'][0]['email']
            page.login.verify_with_invalid_login(guest_user)
            assert "Invalid username or password" == page.login.get_error_message(), 'Failed to verify with invalid login'
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("login_error_message")
            raise Exception(exp)

    @pytestrail.case(6036242)
    def test_02_login_with_valid_user(self, page, web_driver, creds):
        """
        Verify venue manager login with valid user and all dashboard elements
        :param page:
        :param web_driver:
        :param creds:
        """
        try:
            page.login.verify_with_valid_login(username=creds.venuemanager.login.username,
                                               password=creds.venuemanager.login.password)
            assert page.dashboard.verify_homepage_header() == "Dashboard", "Failed to login to venue manager application"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("venue_manager_dashboard")
            raise Exception(exp)

    @pytestrail.case(6036246)
    def test_03_verify_data_on_dashboard(self, page, web_driver):
        """
        To verify dashboard data displayed on venue manager app
        :param page:
        :param web_driver:
        """
        try:
            page.dashboard.click_on_element_on_dashboard(tab_name="today")
            page.dashboard.to_verify_data_on_dashboard("GENERAL")
            page.dashboard.to_verify_data_on_dashboard("Crew Orders")
            page.dashboard.to_verify_data_on_dashboard("Sailor Orders")
            page.dashboard.click_on_element_on_dashboard(tab_name="last hour")
            page.dashboard.to_verify_data_on_dashboard("GENERAL")
            page.dashboard.to_verify_data_on_dashboard("Crew Orders")
            page.dashboard.to_verify_data_on_dashboard("Sailor Orders")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("data_in_dashboard")
            raise Exception(exp)

    @pytestrail.case(6036249)
    def test_04_verify_delivery_toggle_button(self, page, web_driver):
        """
        To verify delivery toggle button on dashboard
        :param page:
        :param web_driver:
        """
        try:
            status = page.dashboard.get_toggle_button_status()
            if status == "false":
                page.dashboard.perform_action_on_toggle_button()
                status = page.dashboard.get_toggle_button_status()
                assert status == "true", "toggle button is not operational"
                page.dashboard.perform_action_on_toggle_button()
                status = page.dashboard.get_toggle_button_status()
                assert status == "false", "toggle button is not operational"

            else:
                page.dashboard.perform_action_on_toggle_button()
                status = page.dashboard.get_toggle_button_status()
                assert status == "false", "toggle button is not operational"
                page.dashboard.perform_action_on_toggle_button()
                status = page.dashboard.get_toggle_button_status()
                assert status == "true", "toggle button is not operational"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("delivery_toggle")
            raise Exception(exp)

    @pytestrail.case(6036303)
    def test_05_switch_venue_from_venue_manager(self, page, web_driver):
        """
        To verify user is able to switch venues from venue manager
        :param page:
        :param web_driver:
        """
        try:
            page.dashboard.click_on_venue_change()
            page.venue.select_venue("Ship Eats - Aquatic Club")
            assert page.dashboard.get_venue_visible_on_dashboard() == "Ship Eats - Aquatic Club", "venue change successful"
            page.dashboard.click_on_venue_change()
            page.venue.select_venue("Ship Eats - Bell Box")
            assert page.dashboard.get_venue_visible_on_dashboard() == "Ship Eats - Bell Box", "venue change successful"

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("switch_venue")
            raise Exception(exp)

    @pytestrail.case(6036301)
    def test_06_check_for_menu_items_in_selected_venue(self, page, web_driver):
        """
        To check for menu items in selected voyage
        :param page:
        :param web_driver:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_expand_cta()
            page.menu.verify_filter_function("Gluten Free")
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_filter_function("Vegetarian")
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_filter_function("Vegan")
            menu_items = page.menu.menu_item_list()
            assert len(menu_items) > 0, "No menu items available in selected venue"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("menu_items_for_selected_venue")
            raise Exception(exp)

    @pytestrail.case(6036262)
    def test_07_check_for_staff_for_selected_venue(self, page, web_driver):
        """
        To verify the staff details for selected venue
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Staff")
            page.staff.verify_elements_in_staff_tab()
            selected_venue = page.dashboard.get_venue_visible_on_dashboard()
            if page.staff.no_records_found():
                logger.info(msg=f"no records found for the selected venue {selected_venue}")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("staff_details")
            raise Exception(exp)

    @pytestrail.case(6036260)
    def test_08_to_verify_venue_details_of_selected_venue(self, page, web_driver):
        """
        To verify the venue details for selected venue
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Settings")
            page.settings.click_on_venue_details()
            page.settings.verify_columns_in_venue_details_tab()
            selected_venue = page.dashboard.get_venue_visible_on_dashboard()
            if page.settings.no_data_found():
                logger.info(msg=f"no data found for the selected venue {selected_venue}")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venue_details")
            raise Exception(exp)

    @pytestrail.case(6036256)
    def test_09_to_verify_preorder_breakfast_details_of_selected_venue(self, page, web_driver):
        """
        To verify preorder breakfast setting tab
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.settings.click_on_preorder_breakfast()
            page.settings.to_verify_preorder_breakfast_settings_for_current_sailing()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("preorder_breakfast")
            raise Exception(exp)

    @pytestrail.case(6036250)
    def test_10_to_verify_operation_hours_and_meal_period(self, page, web_driver):
        """
        To verify user is able to see meal period and operational hours
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.settings.click_on_operational_hour_meal_period()
            if page.settings.is_meal_period_and_capacity():
                pytest.skip(msg="No meal period available")
            page.settings.to_verify_user_is_able_to_see_operational_hour_and_meal_period()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("operational_hour_meal_period")
            raise Exception(exp)

    @pytestrail.case(6036264)
    def test_11_to_verify_current_day_orders_as_per_their_status(self, page, web_driver):
        """
        To verify user is able to see current day orders as per their status
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.to_verify_all_elements_in_order_details()
            page.orders.to_click_on_tab_in_orders_page("active")
            if not page.orders.no_records_found():
                page.orders.to_verify_orders_in_order_details_page("active")
            page.orders.to_click_on_tab_in_orders_page("delivered")
            if not page.orders.no_records_found():
                page.orders.to_verify_orders_in_order_details_page("delivered")
            page.orders.to_click_on_tab_in_orders_page("cancelled")
            if not page.orders.no_records_found():
                page.orders.to_verify_orders_in_order_details_page("cancelled")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_as_per_status")
            raise Exception(exp)

    @pytestrail.case(6036275)
    def test_12_to_verify_sales_report(self, page, web_driver):
        """
        To verify user is able to see sales report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_reports_and_metrics()
            page.reports.verif_elements_on_sales_and_reports()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sales_report")
            raise Exception(exp)

    @pytestrail.case(6036276)
    def test_13_to_verify_order_status_report(self, page, web_driver):
        """
        To verify user is able to see order status report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.verify_elements_on_order_status_report()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sales_report")
            raise Exception(exp)

    @pytestrail.case(63931784)
    def test_14_to_create_preorder_breakfast_with_existing_template(self, page, web_driver):
        """
        To verify user is able to create preorder breakfast with existing template
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Settings")
            page.settings.click_on_preorder_breakfast()
            page.settings.to_create_preorder_breakfast_using_template_for_current_date()
            page.settings.to_create_preorder_breakfast_using_template_for_future_voyage()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("preorder_breakfast_with_template")
            raise Exception(exp)

    @pytestrail.case(6036257)
    def test_15_preorder_breakfast_filter_by_date(self, page, web_driver):
        """
        To verify user is able to apply filter for preorder with date
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.settings.filter_pre_order_breakfast_with_date()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("pre_order_filter_with_date")
            raise Exception(exp)

    @pytestrail.case(6036252)
    def test_16_operational_hours_and_meal_period_filter_by_date(self, page, web_driver):
        """
        To verify user is able to apply filter for operational hors and meal period by date
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.settings.click_on_operational_hour_meal_period()
            page.settings.filter_for_operational_hours_and_meal_period_by_date()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("operational_hours_and_meal_period_filter_with_date")
            raise Exception(exp)

    @pytestrail.case(6036304)
    def test_17_to_very_user_is_able_set_as_default(self, page, web_driver, creds):
        """
        To verify user is able to set default venue
        :param page:
        :param web_driver:
        :param creds:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Dashboard")
            page.dashboard.click_on_venue_change()
            page.venue.select_venue_and_set_as_default("Ship Eats - Bell Box")
            page.dashboard.logout()
            page.login.verify_with_valid_login(username=creds.venuemanager.login.username,
                                               password=creds.venuemanager.login.password)
            assert page.dashboard.get_venue_visible_on_dashboard() == "Ship Eats - Bell Box", "default venu set " \
                                                                                              "successfulyl "
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("default_venue_set")
            raise Exception(exp)

    @pytestrail.case(6036302)
    def test_18_to_very_filter_by_menu_type(self, page, web_driver):
        """
        To verify user is able to set default venue
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Dashboard")
            page.dashboard.click_on_venue_change()
            page.venue.select_venue_and_set_as_default("Ship Eats - Bell Box")
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_filter_function("Gluten Free")
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_filter_function("Vegetarian")
            page.dashboard.click_on_hamburger_menu_tab("Menu")
            page.menu.verify_filter_function("Vegan")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter_menu_items")
            raise Exception(exp)

    @pytestrail.case(6036267)
    def test_19_to_very_order_filter_by_type(self, page, web_driver):
        """
        To verify user is able to filter by type
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.click_on_filter_by_type("Pre-Order Breakfast")
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.click_on_filter_by_type("Crew Orders")
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.click_on_filter_by_type("Sailor Orders")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_filter_by_type")
            raise Exception(exp)

    @pytestrail.case(6036265)
    def test_20_to_very_order_filter_by_date(self, page, web_driver):
        """
        To verify user is able to filter by date
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.to_verify_filter_order_by_date()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_filter_by_date")
            raise Exception(exp)

    @pytestrail.case(6036266)
    def test_21_to_very_order_filter_by_voyage(self, page, web_driver):
        """
        To verify user is able to filter by voyage
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.to_verify_order_filter_by_voyage()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_filter_by_voyage")
            raise Exception(exp)

    @pytestrail.case(6036286)
    def test_22_export_sales_report(self, page, web_driver):
        """
        To verify user is able to export sales report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_reports_and_metrics()
            page.reports.click_sales_status_tab()
            if not page.reports.no_records_found():
                page.reports.click_download()
                page.reports.click_sales_pdf()
                page.reports.verify_pdf("ReportAndMetricsReport")
                page.reports.click_download()
                page.reports.click_sales_excel()
                page.reports.verify_excel("ReportAndMetricsReport")
            else:
                logger.info("no records found to download sales report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sales_excel_pdf_download_error")
            raise Exception(exp)

    @pytestrail.case(6036287)
    def test_23_export_order_status_report(self, page, web_driver):
        """
        To verify user is able to export sales report
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_reports_and_metrics()
            page.reports.click_order_status_tab()
            if not page.reports.no_records_found():
                page.reports.click_download()
                page.reports.click_order_status_pdf()
                page.reports.verify_pdf("ReportAndMetricsReport")
                page.reports.click_download()
                page.reports.click_order_status_excel()
                page.reports.verify_excel("ReportAndMetricsReport")
            else:
                logger.info("no records found to download order status report")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_excel_pdf_download_error")
            raise Exception(exp)

    @pytestrail.case(6036283)
    def test_24_filter_sales_current_meal_period(self, page, web_driver):
        """
        To verify user is able to filter for sales current meal period
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_reports_and_metrics()  #remove after execution
            page.reports.click_sales_status_tab()
            page.reports.filter_sales_and_order_with_current_meal_period()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sales_report_filter")
            raise Exception(exp)

    @pytestrail.case(6036284)
    def test_25_filter_orders_current_meal_period(self, page, web_driver):
        """
        To verify user is able to filter for orders current meal period
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.click_order_status_tab()
            page.reports.filter_sales_and_order_with_current_meal_period()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("order_report_filter")
            raise Exception(exp)

    @pytestrail.case(6036281)
    def test_26_custom_sales_report_filter(self, page, web_driver):
        """
        To verify user is able to apply custom filter from reports and matrix
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.click_sales_status_tab()
            page.reports.verify_custom_sales_report_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("custom_sales_report_filter")
            raise Exception(exp)

    @pytestrail.case(6036282)
    def test_27_custom_order_status_report_filter(self, page, web_driver):
        """
        To verify user is able to apply custom filter from reports and matrix for order status
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.click_order_status_tab()
            page.reports.verify_orders_custom_report_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("custom_order_report_filter")
            raise Exception(exp)

    @pytestrail.case(6036280)
    def test_28_filter_by_voyages(self, page, web_driver):
        """
        To verify user is able to apply custom filter for future voyage
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.reports.filter_sales_and_orders_by_voyage()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sales_and_order_report_filter_by_voyage")
            raise Exception(exp)

    @pytestrail.case(2917012)
    def test_29_search_orders_from_global_search(self, page, web_driver):
        """
        To verify user is able to search orders from global search or not
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu_tab("Orders")
            page.orders.to_click_on_tab_in_orders_page("active")
            page.orders.search_for_order()
            page.orders.to_click_on_tab_in_orders_page("delivered")
            page.orders.search_for_order()
            page.orders.to_click_on_tab_in_orders_page("cancelled")
            page.orders.search_for_order()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Orders_global_search")
            raise Exception(exp)

    @pytestrail.case(6036300)
    def test_30_order_cancellation_graph(self, page, web_driver):
        """
        To verify user is able to check cancellations metrics bar graph
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_reports_and_metrics()
            page.reports.verify_cancellation_status_report()

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Orders_global_search")
            raise Exception(exp)

    @pytestrail.case(6036244)
    def test_31_logout_from_venue_manager(self, page, web_driver):
        """
        logout from web app
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.logout()
            assert 'Venue Manager' == page.login.verify_login_page_header(), 'failed to logout from venue manager'
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("logout")
            raise Exception(exp)

    @pytestrail.case(6036243)
    def test_32_verify_remember_me_option_on_login_page(self, page, web_driver):
        """
        Verify is able to see remember me option on logon page
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.login.verify_user_name_and_password_after_logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("username_password")
            raise Exception(exp)