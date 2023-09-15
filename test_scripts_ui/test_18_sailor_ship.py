__author__ = 'mohit.raghav'

from virgin_utils import *
from ui_pages.sailor_app_ship.login import Login
from ui_pages.sailor_app_ship.Home import Home
from ui_pages.sailor_app_ship.me import Me_tab
from ui_pages.sailor_app_ship.setting_screen import Setting_screen
from ui_pages.sailor_app_ship.apihit import Apihit
from ui_pages.sailor_app_ship.notifications import Notifications
from ui_pages.sailor_app_ship.eateries import Eateries
from ui_pages.sailor_app_ship.ports import Ports
from ui_pages.sailor_app_ship.discover import Discover
from ui_pages.sailor_app_ship.ship_spaces import Ship_spaces
from ui_pages.sailor_app_ship.beauty_and_body import Beauty_and_body
from ui_pages.sailor_app_ship.wallet import Wallet
from ui_pages.sailor_app_ship.cabin_services import Cabin_services
from ui_pages.sailor_app_ship.summary import Summary
from ui_pages.sailor_app_ship.events_my_agenda import Events_my_agenda
from ui_pages.sailor_app_ship.shipeats import Ship_eats
from ui_pages.sailor_app_ship.services import Services
from ui_pages.sailor_app_ship.help_and_support import HelpAndSupport

@pytest.mark.SAILOR_SHIP_UI
@pytest.mark.run(order=18)

class TestSailorShip:
    """
    Test Suite to test Sailor Ship application
    """

    @pytestrail.case(69419974)
    def test_01_launch_app_and_navigate_to_signin_page(self, page, config, web_driver, test_data, rest_shore,
                                                       guest_data, rest_ship, db_iam, couch, db_core, creds):
        """
        Launch the Sailor Ship app and navigate to sign-in page
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param rest_shore:
        :param test_data:
        :param db_iam:
        :param db_core:
        :param guest_data:
        :param couch:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'apihit', Apihit(config, test_data, rest_shore, guest_data, rest_ship, db_iam,
                                           couch, db_core, creds))
            setattr(page, 'home', Home(web_driver))
            setattr(page, 'me', Me_tab(web_driver))
            setattr(page, 'setting', Setting_screen(web_driver))
            setattr(page, 'beauty_and_body', Beauty_and_body(web_driver))
            setattr(page, 'discover', Discover(web_driver))
            setattr(page, 'eateries', Eateries(web_driver))
            setattr(page, 'ports', Ports(web_driver))
            setattr(page, 'ship', Ship_spaces(web_driver))
            setattr(page, 'wallet', Wallet(web_driver))
            setattr(page, 'cabin', Cabin_services(web_driver))
            setattr(page, 'ship_eats', Ship_eats(web_driver))
            setattr(page, 'notification', Notifications(web_driver))
            setattr(page, 'summary', Summary(web_driver))
            setattr(page, 'event_detail', Events_my_agenda(web_driver))
            setattr(page, 'services', Services(web_driver))
            setattr(page, 'help', HelpAndSupport(web_driver))
            page.login.wait_till_first_screen()
            page.apihit.checkin_onboard_guest(config, test_data, rest_shore, guest_data, rest_ship,
                                              db_iam, couch, db_core, creds)
            page.login.verification_of_initial_pages()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('launch_app_and_navigate_to_login_page')
            raise Exception(exp)

    @pytestrail.case(67653896)
    def test_02_signin_with_email(self, page, web_driver, guest_data):
        """
        Test case to Login into sailor app ship
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            page.login.fill_signin_details(guest_data[0]['email'], 'Voyages@9876')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('signin_with_email')
            raise Exception(exp)

    @pytestrail.case(6036309)
    def test_03_verify_oncruise_dashboard(self, page, web_driver, test_data):
        """
        To verify oncruise dashboard
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.verify_availability_of_dashboard_quick_links()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_oncruise_dashboard')
            raise Exception(exp)

    @pytestrail.case(69666756)
    def test_04_turn_off_notifications(self, page, web_driver, test_data):
        """
        Turn off notification to avoid random pop-ups on screen
        :param page:
        :param test_data:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.click_on_setting_icon()
            page.setting.open_notifications_and_privacy()
            page.notification.disable_reminders()
            page.ports.click_back_button()
            page.home.open_homepage_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('turn_off_notifications')
            raise Exception(exp)

    @pytestrail.case(69419419)
    def test_05_logout_from_sailor_app(self, page, web_driver, test_data):
        """
        Go to Account page
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('logout_from_sailor_app')
            raise Exception(exp)

    @pytestrail.case(67652283)
    def test_06_verify_sign_up_with_email_flow(self, page, web_driver, guest_data, test_data):
        """
        Test cases to Signup into Sailor app ship
        :param page:
        :param web_driver:
        :param guest_data:
        :param test_data:
        :return:
        """
        try:
            page.login.open_signup_page()
            page.login.open_signup_with_email()
            page.apihit.generate_sigup_email_id(test_data)
            page.login.fill_signup_details(guest_data, test_data)
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_sign_up_with_email_flow')
            raise Exception(exp)

    @pytestrail.case(67663546)
    def test_07_signup_with_google(self, page, web_driver, test_data):
        """
        Test case to to verify user is able to signup with google
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.login.open_signup_page()
            page.login.open_signup_with_google()
            page.login.signup_with_google(test_data)
            if not test_data['Google_ac_available']:
                pytest.skip("Skipping this TC as required google account is not added on device")
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signup_with_google')
            raise Exception(exp)

    @pytestrail.case(69666788)
    def test_08_signin_with_google_into_sailor_app(self, page, web_driver, test_data):
        """
        Function to signin with google into sailor app
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['Google_ac_available']:
                pytest.skip("Skipping this TC as required google account is not added on device")
            page.login.open_signin_page()
            page.login.open_signin_with_google()
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signin_with_google')
            raise Exception(exp)

    @pytestrail.case(67652728)
    def test_09_signup_with_facebook(self, page, web_driver):
        """
        Test case to verify that user is able to signup with facebook
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.login.open_signup_page()
            page.login.open_signup_with_facebook()
            page.login.signup_with_facebook()
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('signup_with_facebook')
            raise Exception(exp)

    @pytestrail.case(69666789)
    def test_10_signin_with_facebook(self, page, web_driver):
        """
        Function to sign-in with facebook into sailor app
        :param page:
        :param web_driver:
        :return :
        """
        try:
            page.login.open_signin_page()
            page.login.open_signin_with_facebook()
            page.login.signup_with_facebook()
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signin_with_facebook')
            raise Exception(exp)

    @pytestrail.case(60498731)
    def test_11_verify_signin_with_shipboard(self, page, web_driver, guest_data, test_data):
        """
        Verify signin with shipboard functionality
        :param page:
        :param web_driver:
        :param guest_data:
        :param test_data:
        :return:
        """
        try:
            page.login.open_signin_page()
            page.login.open_signin_with_shipboard()
            page.login.fill_shipboard_details(guest_data[0]['LastName'], guest_data[0]['birthDate'],
                                              test_data['shipside_guests'][0]['cabin_no'])
            page.home.verify_oncruise_ship_time()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signin_with_shipboard')
            raise Exception(exp)

    @pytestrail.case(67982558)
    def test_12_verify_book_dining_quicklink(self, page, web_driver):
        """
        Function to verify book dining quicklink on dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_oncruise_ship_time()
            page.home.click_book_dining_quicklink()
            try:
                page.eateries.verify_eateries_header()
            except(Exception, ValueError) as exp:
                page.eateries.click_back_button()
                web_driver.allure_attach_jpeg('no_dining_page')
                raise Exception(exp)
            page.eateries.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_dining_quicklink')
            raise Exception(exp)

    @pytestrail.case(67982559)
    def test_13_verify_book_a_shore_thing_quicklink(self, page, web_driver):
        """
        Function to verify book a shore thing quicklink on dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_book_a_shore_thing_quicklink()
            try:
                page.ports.verify_shore_things_page()
            except(Exception, ValueError) as exp:
                page.ports.click_back_button()
                web_driver.allure_attach_jpeg('no_shore_thing_page')
                raise Exception(exp)
            page.ports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_a_shore_thing_quicklink')
            raise Exception(exp)

    @pytestrail.case(67983944)
    def test_14_verify_browse_the_lineup_quicklink(self, page, web_driver):
        """
        Function to verify browse the event lineup quicklink on dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_browse_the_event_lineup_quicklink()
            try:
                page.discover.verify_availability_of_lineup_events()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_lineup_available')
                raise Exception(exp)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_browse_the_event_lineup_quicklink')
            raise Exception(exp)

    @pytestrail.case(67985861)
    def test_15_verify_book_a_spa_treatment_quicklink(self, page, web_driver):
        """
        Function to verify book a spa treatment quicklink on dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_book_a_spa_treatment_quicklink()
            try:
                page.beauty_and_body.verify_availability_of_beauty_and_body_header()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_spa_treatment_page')
                raise Exception(exp)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_a_spa_treatment_quicklink')
            raise Exception(exp)

    @pytestrail.case(67982320)
    def test_16_verify_add_your_friends_quickink(self, page, web_driver):
        """
        To verify add your friends quicklink on homepage
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_add_your_friends_quicklink()
            try:
                page.home.verify_share_pop_up()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_share_popup')
                raise Exception(exp)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_add_your_friends_quickink')
            raise Exception(exp)

    @pytestrail.case(67987307)
    def test_17_verify_view_the_ship_venues_quicklink(self, page, web_driver):
        """
        Function to verify view ship venue quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_view_the_ship_venues()
            try:
                page.ship.verify_ship_spaces_header()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_ship_spaces_page')
                raise Exception(exp)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_view_the_ship_venues_quicklink')
            raise Exception(exp)

    @pytestrail.case(70112467)
    def test_18_verify_view_your_agenda_quicklink(self, page, web_driver):
        """
        Function to verify view your agenda quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_view_your_agenda()
            try:
                page.me.check_availability_of_myagenda()
                page.home.open_homepage_tab()
            except(Exception, ValueError) as exp:
                page.home.open_homepage_tab()
                web_driver.allure_attach_jpeg('No_my_agenda_page')
                raise Exception(exp)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_view_your_agenda_quicklink')
            raise Exception(exp)

    @pytestrail.case(70112468)
    def test_19_verify_view_your_wallet_quicklink(self, page, web_driver):
        """
        Function to verify view your wallet quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_view_your_wallet()
            try:
                page.wallet.verify_wallet_balance_page()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                page.home.open_homepage_tab()
                web_driver.allure_attach_jpeg('No_my_wallet_page')
                raise Exception(exp)
            page.discover.click_back_button()
            page.home.open_homepage_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_view_your_wallet_quicklink')
            raise Exception(exp)

    @pytestrail.case(70112469)
    def test_20_verify_cabin_house_keeping_quicklink(self, page, web_driver):
        """
        Function to verify cabin housekeeping quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_cabin_house_keeping()
            try:
                page.cabin.verify_cabin_services_page()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_cabin_services_page')
                raise Exception(exp)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_cabin_house_keeping_quicklink')
            raise Exception(exp)

    @pytestrail.case(70112470)
    def test_21_verify_shipEats_delivery_quicklink(self, page, web_driver):
        """
        Function to verify ship eats delivery quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_oncruise_ship_time()
            page.home.click_ship_eats_delivery()
            try:
                page.ship_eats.verify_ship_eats_page()
            except(Exception, ValueError) as exp:
                page.discover.click_back_button()
                web_driver.allure_attach_jpeg('No_ship_eats_page')
                raise Exception(exp)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_cabin_house_keeping_quicklink')
            raise Exception(exp)

    @pytestrail.case(12150702)
    def test_22_verify_discover_search(self, page, web_driver):
        """
        Function to verify discover search
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.verify_availability_of_search_bar()
            page.discover.search_keyword()
            page.discover.verify_search_results()
            page.discover.close_discover_search()
            page.home.open_homepage_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_discover_search')
            raise Exception(exp)

    @pytestrail.case([11572036, 11572039])
    def test_23_verify_lineup_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_lineup()
            page.discover.select_and_open_lineup_event(test_data)
            if test_data['lineup_available']:
                page.discover.add_to_love_list(test_data)
                page.discover.book_lineup()
                page.summary.verify_summary_screen()
                page.summary.save_event_details(test_data)
                page.summary.click_confirm_button(test_data)
                page.summary.verify_booking_confirmation_screen(test_data)
                page.summary.click_view_in_sailor_log()
            else:
                pytest.skip("Skipping this TC as no lineup is available for booking")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lineup_booking')
            raise Exception(exp)

    @pytestrail.case(11572040)
    def test_24_verify_booked_lineup_in_my_agenda_of_me_section(self, page, web_driver, test_data):
        """
        To verify that booked lineup is available in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['lineup_available']:
                pytest.skip("Skipping this TC as no lineup is available for booking")
            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_title(test_data)
            page.event_detail.verify_booked_event_schedule_and_location(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_lineup_in_my_agenda_of_me_section')
            raise Exception(exp)

    @pytestrail.case(11572037)
    def test_25_edit_lineup(self, page, web_driver, test_data):
        """
        To verify that user is able to edit lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['lineup_available']:
                pytest.skip("Skipping this TC as no lineup is available for booking")
            event = 'lineup'
            page.event_detail.click_edit_booking_details(test_data, event)
            if not test_data[f'{event}_editing']:
                page.discover.click_back_button()
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_lineup')
            raise Exception(exp)

    @pytestrail.case(11572041)
    def test_26_verify_edited_lineup(self, page, web_driver, test_data):
        """
        To verify edited lineup details
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if not test_data['lineup_available']:
                pytest.skip("Skipping this TC as no lineup is available for booking")
            elif not test_data['lineup_editing']:
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_edited_lineup')
            raise Exception(exp)

    @pytestrail.case(11572038)
    def test_27_cancel_lineup(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['lineup_available']:
                pytest.skip("Skipping this TC as no lineup is available for booking")
            elif not test_data['lineup_editing']:
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen()
            page.event_detail.click_done()
            page.me.check_availability_of_myagenda()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_lineup')
            raise Exception(exp)

    @pytestrail.case(11572042)
    def test_28_verify_cancelled_lineup_not_available_in_my_agenda(self, page, web_driver, test_data):
        """
        To verify that cancelled lineup is unavailable in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.verify_unavailability_of_canceled_lineup(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_cancelled_lineup_not_available_in_my_agenda')
            raise Exception(exp)

    @pytestrail.case(6036291)
    def test_29_default_slots_available_on_eateries_listing_page(self, page, web_driver, test_data):
        """
        To verify that default slots are available on restaurant listing page
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship_spaces()
            page.ship.open_eateries()
            page.eateries.verify_availability_of_default_slots()
            page.eateries.verify_availability_of_bookable_slots(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('default_slots_available_on_restaurant_listing_page')
            raise Exception(exp)

    @pytestrail.case([6036292, 54370814])
    def test_30_book_dining(self, page, web_driver, test_data):
        """
        To verify that user is able to book dining
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_dining_slots']:
                pytest.skip('Skipping this TC as no dining slot is available for booking')
            page.eateries.book_dining()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('book_dining')
            raise Exception(exp)

    @pytestrail.case(70473079)
    def test_31_verify_booked_dining_in_my_agenda_of_me_section(self, page, web_driver, test_data):
        """
        To verify that booked dining is available in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_dining_slots']:
                pytest.skip('Skipping this TC as no dining slot is available for booking')
            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_title(test_data)
            page.event_detail.verify_booked_event_schedule_and_location(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_dining_in_my_agenda_of_me_section')
            raise Exception(exp)

    @pytestrail.case(6036293)
    def test_32_edit_dining_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit dining
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_dining_slots']:
                pytest.skip('Skipping this TC as no dining slot is available for booking')
            event = "dining"
            page.event_detail.click_edit_booking_details(test_data, event)
            if not test_data[f'{event}_editing']:
                page.discover.click_back_button()
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_dining_and_verify')
            raise Exception(exp)

    @pytestrail.case(6036294)
    def test_33_cancel_dining(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel dining
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_dining_slots']:
                pytest.skip('Skipping this TC as no dining slot is available for booking')
            elif not test_data['dining_editing']:
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen()
            page.event_detail.click_done()
            page.me.check_availability_of_myagenda()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_dining')
            raise Exception(exp)

    @pytestrail.case(54370816)
    def test_34_book_dining_at_restaurant_closing_time(self, page, web_driver, test_data):
        """
        To verify that user is able to book dining at restaurant closing time
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship_spaces()
            page.ship.open_eateries()
            page.eateries.verify_availability_of_default_slots()
            page.eateries.verify_availability_of_bookable_slots(test_data)
            if not test_data['bookable_dining_slots']:
                pytest.skip('Skipping this TC as no dining slot is available for booking')
            page.eateries.book_dining_at_restaurant_closing_time()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('book_dining_at_restaurant_closing_time')
            raise Exception(exp)

    @pytestrail.case(6036296)
    def test_35_verify_excursion_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book excursion
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_shore_things()
            page.ports.check_excursion(test_data)
            if not test_data['bookable_excursion_available']:
                page.discover.click_back_button()
                time.sleep(5)
                page.discover.click_back_button()
                pytest.skip('Skipping this TC as no excursion available for booking')
            page.discover.add_to_love_list(test_data)
            page.ports.book_excursion()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            if not test_data['active_folio']:
                page.home.open_homepage_tab()
                raise Exception("Not able to book excursion due to inactive folio")
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_excursion_booking')
            raise Exception(exp)

    @pytestrail.case(6036297)
    def test_36_verify_booked_excursion_in_my_agenda_of_me_section(self, page, web_driver, test_data):
        """
        To verify that booked excursion is available in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_excursion_available']:
                pytest.skip('Skipping this TC as no excursion available for booking')
            elif not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_title(test_data)
            page.event_detail.verify_booked_event_schedule_and_location(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_excursion_in_my_agenda_of_me_section')
            raise Exception(exp)

    @pytestrail.case(6036298)
    def test_37_edit_excursion_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit excursion
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_excursion_available']:
                pytest.skip('Skipping this TC as no excursion available for booking')
            elif not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            event = "excursion"
            page.event_detail.click_edit_booking_details(test_data, event)
            if not test_data[f'{event}_editing']:
                page.discover.click_back_button()
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_excursion_and_verify')
            raise Exception(exp)

    @pytestrail.case(6036299)
    def test_38_cancel_excursion(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel excursion
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['bookable_excursion_available']:
                pytest.skip('Skipping this TC as no excursion available for booking')
            elif not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            elif not test_data['excursion_editing']:
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen()
            page.event_detail.click_done()
            page.me.check_availability_of_myagenda()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_excursion')
            raise Exception(exp)

    @pytestrail.case(70571091)
    def test_39_verify_spa_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            page.home.open_discover_tab()
            page.discover.open_ship_spaces()
            page.ship.open_beauty_and_body()
            page.beauty_and_body.open_redemption_spa()
            page.discover.add_spa_to_love_List(test_data)
            page.beauty_and_body.open_acupuncture()
            page.beauty_and_body.book_resurrection_acupuncture(test_data)
            if not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")
            page.summary.verify_summary_screen()
            page.summary.save_event_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_spa_booking')
            raise Exception(exp)

    @pytestrail.case(70572312)
    def test_40_verify_booked_spa_in_my_agenda_of_me_section(self, page, web_driver, test_data):
        """
        To verify that booked spa is available in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            elif not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")

            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_title(test_data)
            page.event_detail.verify_booked_event_schedule_and_location(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_spa_in_my_agenda_of_me_section')
            raise Exception(exp)

    @pytestrail.case(70571092)
    def test_41_edit_booked_spa_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit booked spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            elif not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")

            event = "spa"
            page.event_detail.click_edit_booking_details(test_data, event)
            if not test_data[f'{event}_editing']:
                page.discover.click_back_button()
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.edit_spa_booking()
            page.summary.verify_summary_screen()
            page.summary.save_edited_spa_details(test_data)
            page.summary.click_confirm_button(test_data)
            page.summary.verify_booking_confirmation_screen(test_data)
            page.summary.click_view_in_sailor_log()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_booked_event_guest_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_booked_spa_and_verify')
            raise Exception(exp)

    @pytestrail.case(70571093)
    def test_42_cancel_booked_spa(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel booked spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['active_folio']:
                pytest.skip('Skipping this TC as sailor has inactive folio')
            elif not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")
            elif not test_data['spa_editing']:
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen()
            page.event_detail.click_done()
            page.me.check_availability_of_myagenda()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_booked_spa')
            raise Exception(exp)

    @pytestrail.case(6036313)
    def test_43_verify_lovelist(self, page, web_driver, test_data):
        """
        To verify that marked events should be available in lovelist
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.open_lovelist()
            page.me.verify_events_available_in_lovelist(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lovelist')
            raise Exception(exp)

    @pytestrail.case(6036314)
    def test_44_verify_availability_of_all_voyage_settings(self, page, web_driver, test_data):
        """
         Verify availability of all sections in voyage settings
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.click_on_setting_icon()
            page.setting.verify_landing_on_setting_screen()
            page.setting.verify_availability_of_the_band_and_pin()
            page.setting.verify_availability_of_notifications_and_privacy()
            page.setting.verify_availability_of_emergency_contact()
            page.setting.verify_availability_of_sailing_documents()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_voyage_settings')
            raise Exception(exp)

    @pytestrail.case(70949670)
    def test_45_verify_availability_of_all_profile_and_settings(self, page, web_driver):
        """
         Verify availability of all sections in profile and settings
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.verify_availability_of_profile_settings_header()
            page.setting.verify_availability_of_personal_information()
            page.setting.verify_availability_of_contact_details()
            page.setting.verify_availability_of_login_details()
            page.setting.verify_availability_of_payment_methods()
            page.setting.verify_availability_of_communication_preferences()
            page.setting.verify_availability_of_terms_and_conditions()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_availability_of_all_profile_settings')
            raise Exception(exp)

    @pytestrail.case(6036315)
    def test_46_verify_switch_voyage_and_payment_methods_disabled(self, page, web_driver):
        """
        Verify switch voyage and payment methods button are disabled
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.verify_availability_of_profile_settings_header()
            page.setting.verify_payments_methods_disabled()
            page.setting.verify_switch_voyage_button_disabled()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_switch_voyage_and_payment_methods_disabled')
            raise Exception(exp)

    @pytestrail.case(11572051)
    def test_47_raise_request_for_cabin_services(self, page, web_driver, test_data):
        """
         Verify sailor is able to raise cabin services request
        :param page:
        :param web_driver:
        :poram test_data:
        :return:
        """
        try:
            page.home.open_services_tab()
            page.services.verify_services_page()
            page.services.verify_cabin_services_btn_availability()
            page.services.click_cabin_services_btn()
            page.cabin.verify_cabin_services_page()
            page.cabin.request_cabin_service(test_data)
            page.cabin.verify_requested_cabin_service(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('raise_request_for_cabin_services')
            raise Exception(exp)

    @pytestrail.case(11572052)
    def test_48_cancel_request_for_cabin_services(self, page, web_driver, test_data):
        """
         Verify sailor is able to cancel the raised cabin services request
        :param page:
        :param web_driver:
        :poram test_data:
        :return:
        """
        try:
            page.cabin.cancel_raised_cabin_service_request(test_data)
            page.cabin.verify_cancelled_cabin_service_request(test_data)
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_request_for_cabin_services')
            raise Exception(exp)

    @pytestrail.case(6036312)
    def test_49_open_help_and_support_questions(self, page, web_driver):
        """
         Verify sailor is able to open help and support questions
        :param page:
        :param web_driver:
        :poram test_data:
        :return:
        """
        try:
            page.home.open_services_tab()
            page.services.verify_services_page()
            page.services.verify_help_and_support_btn_availability()
            page.services.click_help_and_support_btn()
            page.help.verify_help_and_support_questions()
            page.discover.click_back_button()
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_request_for_cabin_services')
            raise Exception(exp)

    @pytestrail.case(11572049)
    def test_50_send_msg_from_help_and_support(self, page, web_driver):
        """
        Verify sailor is able to send message to support team from help and support
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.services.verify_services_page()
            page.services.verify_help_and_support_btn_availability()
            page.services.click_help_and_support_btn()
            page.help.click_chat_button()
            page.help.verify_chat_window()
            page.help.send_message()
            page.discover.click_back_button()
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('send_msg_from_help_and_support')
            raise Exception(exp)

    @pytestrail.case(6036311)
    def test_51_verify_oncruise_page_card_details(self, page, web_driver):
        """
        To verify on-cruise card details
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_oncruise_ship_time()
            page.home.verify_homepage_cards()
            page.home.open_card_details_page()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_oncruise_page_card_details')
            raise Exception(exp)

    @pytestrail.case(64875824)
    def test_52_enable_biometric_for_sailor(self, page, web_driver, test_data):
        """
        Enable biometric login for sailor if disabled
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.click_on_setting_icon()
            page.setting.verify_landing_on_setting_screen()
            page.setting.verify_availability_of_login_details()
            page.setting.open_login_details()
            page.setting.enable_biometric_login()
            page.discover.click_back_button()
            page.discover.click_back_button()
        except Exception as exp:
            web_driver.allure_attach_jpeg('verify_oncruise_page_card_details')
            raise Exception(exp)

    @pytestrail.case(11968502)
    def test_53_verify_transactions_in_my_wallet(self, web_driver, page, test_data):
        """
         Verify transactions in my wallet
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.open_my_wallet()
            page.me.verify_transactions_in_wallet(test_data)
            page.discover.click_back_button()
        except Exception as exp:
            web_driver.allure_attach_jpeg('verify_transactions_in_my_wallet')
            raise Exception(exp)

    @pytestrail.case(68480262)
    def test_54_verify_tap_rockstar_symbol_for_vip_sailor(self, page, web_driver, test_data):
        """
        Verify user should be able to tap on rockstar symbol and open rockstar cabin details page
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_me_tab(test_data)
            page.me.check_vip_sailor(test_data)
            if not test_data['is_vip_sailor']:
                pytest.skip("Skipping this TC as user is not a vip sailor")
            page.me.click_rockstar_symbol()
            page.me.verify_rockstar_benefits()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_tap_rockstar_symbol_for_vip_sailor')
            raise Exception(exp)

    @pytestrail.case(6036310)
    def test_55_verify_watch_safety_drill_video(self, page, web_driver, test_data):
        """
        Verify user is able to watch safety drill video
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_oncruise_ship_time()
            page.home.click_watch_muster_drill(test_data)
            if test_data['muster_drill_available']:
                page.home.verify_availability_of_muster_drill_video()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_watch_safety_drill_video')
            raise Exception(exp)

    @pytestrail.case(1710)
    def test_56_verify_no_rts_option_for_onboarded_sailor(self, page, web_driver):
        """
        Verify no rts option is available for onboarded sailor
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_oncruise_ship_time()
            page.home.verify_no_rts_on_homepage()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_no_rts_option_for_onboarded_sailor')
            raise Exception(exp)

    @pytestrail.case(11572044)
    def test_57_order_ship_eats_in_services(self, page, web_driver, test_data):
        """
        Verify sailor is able to order ship eats in services
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_services_tab()
            page.services.verify_services_page()
            page.services.verify_shipEats_delivery_btn_availability()
            page.services.click_shipEats_delivery_btn()
            page.ship_eats.verify_ship_eats_page()
            page.ship_eats.add_items_to_basket(test_data)
            if not test_data['items_available']:
                pytest.skip("Skipping this TC as no items available to order.")
            page.ship_eats.place_order()
            page.ship_eats.verify_order_confirmation_screen()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('order_ship_eats_in_services')
            raise Exception(exp)

    @pytestrail.case(11572046)
    def test_58_verify_order_in_recent_orders(self, page, web_driver, test_data):
        """
        Verify order placed should be available in recent orders
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['items_available']:
                pytest.skip("Skipping this TC as no items available to order.")
            page.ship_eats.click_recent_orders()
            page.ship_eats.verify_recent_order(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_order_in_recent_orders')
            raise Exception(exp)

    @pytestrail.case(11572047)
    def test_59_cancel_the_shipEats_order(self, page, web_driver, test_data):
        """
        Verify user is able to cancel ship eats order
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['items_available']:
                pytest.skip("Skipping this TC as no items available to order.")
            page.ship_eats.cancel_order()
            page.ship_eats.confirm_cancellation_page()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_the_shipEats_order')
            raise Exception(exp)

    @pytestrail.case(64876609)
    def test_60_order_preorder_breakfast_without_allergies(self, page, web_driver, test_data):
        """
        To order preorder breakfast with allergies
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.ship_eats.verify_ship_eats_page()
            page.ship_eats.click_pre_order_breakfast()
            page.ship_eats.select_time_slot(test_data)
            if not test_data['slots_available']:
                pytest.skip("Skipping this TC as no slots available to order.")
            page.ship_eats.add_items_to_basket(test_data)
            if not test_data['items_available']:
                pytest.skip("Skipping this TC as no items available to order.")
            page.ship_eats.place_order()
            page.ship_eats.verify_order_confirmation_screen()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('order_ship_eats_in_services')
            raise Exception(exp)

    @pytestrail.case([64876608, 64875826])
    def test_61_edit_items_in_preorder_breakfast(self, page, web_driver, test_data):
        """
        To edit items in pre-order breakfast
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['items_available']:
                pytest.skip("Skipping this TC as no items available to order.")
            elif not test_data['slots_available']:
                pytest.skip("Skipping this TC as no slots available to order.")
            page.ship_eats.click_recent_orders()
            page.ship_eats.click_edit_pre_order_btn()
            page.ship_eats.edit_order()
            page.ship_eats.click_update_order()
            page.ship_eats.verify_preorder_update_confirmation_screen()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_items_in_preorder_breakfast')
            raise Exception(exp)



