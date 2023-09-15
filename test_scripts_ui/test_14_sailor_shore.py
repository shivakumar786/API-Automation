__author__ = 'vanshika.arora'

from virgin_utils import *
from ui_pages.sailor_app.login import Login
from ui_pages.sailor_app.Home import Home
from ui_pages.sailor_app.rts import Rts
from ui_pages.sailor_app.pregnancy import Pregnancy
from ui_pages.sailor_app.voyage_contract import Voyage_contract
from ui_pages.sailor_app.emergency_contact import Emergency_contact
from ui_pages.sailor_app.step_aboard import Step_aboard
from ui_pages.sailor_app.voyage_well import Voyage_well
from ui_pages.sailor_app.me import Me_tab
from ui_pages.sailor_app.discover import Discover
from ui_pages.sailor_app.setting_screen import Setting_screen
from ui_pages.sailor_app.confirmation_screen import Booking_confirmation
from ui_pages.sailor_app.event_detail import Event_detail
from ui_pages.sailor_app.summary import Summary
from ui_pages.sailor_app.apihit import Apihit
from ui_pages.sailor_app.ship import Ship
from ui_pages.sailor_app.eateries import Eateries
from ui_pages.sailor_app.ports import Ports
from ui_pages.sailor_app.payment_methods import Payment_methods
from ui_pages.sailor_app.payment import Payment
from ui_pages.sailor_app.shipeats import Ship_eats
from ui_pages.sailor_app.services import Services
from ui_pages.sailor_app.beauty_and_body import Beauty_and_body
from ui_pages.sailor_app.redemption_spa import Redemption_spa
from ui_pages.sailor_app.communication_preferences import communication_Preferences
from ui_pages.sailor_app.communcation_preferences_updated import communication_Preferences_Updated
from ui_pages.sailor_app.terms_and_conditions import terms_And_Conditions
from ui_pages.sailor_app.security_guide import security_Guide
from ui_pages.sailor_app.privacy_policy import privacy_Policy
from ui_pages.sailor_app.mobile_terms import mobile_Terms
from ui_pages.sailor_app.cookie_policy import cookie_Policy
from ui_pages.sailor_app.switch_voyage import switch_Voyage
from ui_pages.sailor_app.connect_booking import connect_Booking
from ui_pages.sailor_app.wallet import Wallet
from ui_pages.sailor_app.restaurant_details import Restaurant_details
from ui_pages.sailor_app.rockstar import Rockstar
from ui_pages.sailor_app.guides import Guides
from ui_pages.sailor_app.messenger import Messenger
from ui_pages.sailor_app.health_form import Health_form
from ui_pages.sailor_app.contacts import Contacts
from ui_pages.sailor_app.travel_docs import Travel_docs
from ui_pages.sailor_app.post_voyage import Post_voyage


@pytest.mark.SAILOR_SHORE_UI
@pytest.mark.run(order=14)
class TestSailorApp:
    """
    Test Suite to test Sailor application
    """

    @pytestrail.case(57013902)
    def test_01_launch_app_and_navigate_to_login_page(self, page, config, web_driver, rest_shore, test_data, guest_data ,request, v_guest_data):
        """
        Launch the Sailor app
        :param web_driver:
        :param page:
        :param config:
        :param rest_shore:
        :param test_data:
        :param request:
        :param v_guest_data:
        :return:
        """
        setattr(page, 'login', Login(web_driver))
        setattr(page, 'home', Home(web_driver))
        setattr(page, 'rts', Rts(web_driver))
        setattr(page, 'rockstar', Rockstar(web_driver))
        setattr(page, 'voyage_contract', Voyage_contract(web_driver))
        setattr(page, 'emergency_contact', Emergency_contact(web_driver))
        setattr(page, 'pregnancy', Pregnancy(web_driver))
        setattr(page, 'step_aboard', Step_aboard(web_driver))
        setattr(page, 'voyage_well', Voyage_well(web_driver))
        setattr(page, 'me', Me_tab(web_driver))
        setattr(page, 'discover', Discover(web_driver))
        setattr(page, 'setting', Setting_screen(web_driver))
        setattr(page, 'confirmation_screen', Booking_confirmation(web_driver))
        setattr(page, 'event_detail', Event_detail(web_driver))
        setattr(page, 'summary', Summary(web_driver))
        setattr(page, 'ship', Ship(web_driver))
        setattr(page, 'eateries', Eateries(web_driver))
        setattr(page, 'ports', Ports(web_driver))
        setattr(page, 'payment', Payment(web_driver))
        setattr(page, 'payment_methods', Payment_methods(web_driver))
        setattr(page, 'shipeats', Ship_eats(web_driver))
        setattr(page, 'services', Services(web_driver))
        setattr(page, 'redemption_spa', Redemption_spa(web_driver))
        setattr(page, 'beauty_and_body', Beauty_and_body(web_driver))
        setattr(page, 'apihit', Apihit(config, rest_shore, test_data))
        setattr(page, 'preferences', communication_Preferences(web_driver))
        setattr(page, 'preferences_updated', communication_Preferences_Updated(web_driver))
        setattr(page, 'terms_and_conditions', terms_And_Conditions(web_driver))
        setattr(page, 'security_guide', security_Guide(web_driver))
        setattr(page, 'privacy_policy', privacy_Policy(web_driver))
        setattr(page, 'mobile_terms', mobile_Terms(web_driver))
        setattr(page, 'cookie_policy', cookie_Policy(web_driver))
        setattr(page, 'switch_voyage', switch_Voyage(web_driver))
        setattr(page, 'connect_booking', connect_Booking(web_driver))
        setattr(page, 'wallet', Wallet(web_driver))
        setattr(page, 'restaurant_details', Restaurant_details(web_driver))
        setattr(page, 'guides', Guides(web_driver))
        setattr(page, 'messenger', Messenger(web_driver))
        setattr(page, 'health_form', Health_form(web_driver))
        setattr(page, 'contacts', Contacts(web_driver))
        setattr(page, 'travel_docs', Travel_docs(web_driver))
        setattr(page, 'post_voyage', Post_voyage(web_driver))
        page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data, country="USA")
        page.login.wait_till_first_screen()
        page.login.verification_of_initial_pages()

    @pytestrail.case(57012747)
    def test_02_check_sign_up_with_email_flow(self, page, web_driver, guest_data):
        """
        Test cases to Signup into Sailor app
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        page.login.open_signup_page()
        page.login.open_signup_with_email()
        contexts = web_driver.get_contexts()
        web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page.login.fill_signup_details(guest_data)
        page.login.verify_availability_of_connect_booking_button()
        page.login.verify_availability_of_book_voyage_button()
        page.login.go_to_settings_after_signup()
        page.setting.logout()

    @pytestrail.case(1665)
    def test_03_signup_with_google(self, page, web_driver):
        """
        Test case to to verify user is able to signup with google
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.login.open_signup_page()
            page.login.open_signup_with_google()
            page.login.signup_with_google()
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signup_with_google')
            raise Exception(exp)

    @pytestrail.case(1668)
    def test_04_signup_with_facebook(self, page, web_driver):
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
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('signup_with_facebook')
            raise Exception(exp)

    @pytestrail.case(1659)
    def test_05_signin_with_google_into_sailor_app(self, page, web_driver):
        """
        Function to signin with google into sailor app
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.login.open_signin_page()
            page.login.open_signin_with_google()
            # page.login.signup_with_google()
            page.login.verify_availability_of_connect_booking_button()
            page.login.verify_availability_of_book_voyage_button()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_signin_with_google')
            raise Exception(exp)

    @pytestrail.case(1657)
    def test_06_signin_with_facebook_into_sailor_app(self, page, web_driver):
        """
        Function to signin with facebook into sailor app
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

    @pytestrail.case(1666)
    def test_07_signin_with_email_into_sailor_app(self, page, web_driver, guest_data):
        """
        Test case to Login into sailor app
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        page.login.open_signin_page()
        page.login.open_signin_with_email()
        contexts = web_driver.get_contexts()
        web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page.login.fill_signin_details(guest_data[0]['Email'], 'Voyages@9876')

    @pytestrail.case(1662)
    def test_08_verify_precruise_dashboard(self, page, web_driver, test_data):
        """
        To verify precruise dashboard
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.apihit.get_token(side='shore')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_next_voyage(test_data)
            page.home.verify_precruise_text()
            page.home.verify_availability_of_precruise_task()
            page.home.save_homepage_voyage_data(test_data)
            page.home.verify_no_of_days_on_homepage(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_precruise_dashboard')
            raise Exception(exp)

    @pytestrail.case(68400492)
    def test_09_verify_number_of_steps_available_in_rts(self, page, web_driver, guest_data, test_data):
        """
        Function to verify number of steps available in rts as per gender
        :param page:
        :param web_driver:
        :param guest_data:
        :param test_data:
        :return:
        """
        try:
            page.home.verify_precruise_text()
            page.home.verify_number_of_steps_in_rts(guest_data, test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_number_of_steps_available_in_rts')
            raise Exception(exp)

    @pytestrail.case(70024539)
    def test_10_verify_user_is_able_to_access_homepage_cards(self, page, web_driver):
        """
        Function to verify that user is able to access homepage cards
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.verify_precruise_text()
            page.home.open_and_verify_homepage_card()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(64875721)
    def test_11_complete_rts_travel_documents(self, page, web_driver, guest_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            nationality='United States'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_passport_scan_screen_available()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.travel_docs.verify_correct_details_available_after_scanning_passport(nationality)
            page.travel_docs.fill_correct_sailor_details(guest_data, nationality)
            page.travel_docs.click_done_cta()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(507110)
    def test_12_complete_rts_payment_method(self, page, web_driver, guest_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_payment_method_step()
            page.rts.verify_availability_of_payment_method()
            page.rts.click_start_button()
            page.payment_methods.verify_payment_method_title_question()
            page.payment_methods.select_credit_card()
            page.payment.verify_enter_card_details_page_available()
            page.payment.fill_payment_card_details(guest_data)
            page.payment.verify_card_saved(guest_data)
            page.payment.click_card_payment_confirm_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(68400493)
    def test_13_complete_rts_pregnancy_question(self, page, web_driver, guest_data):
        """
        Function to click pregnancy question
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            if guest_data[0]['GenderCode'] == "Female" or guest_data[0]['GenderCode'] == "Another Gender":
                page.rts.open_pregnancy_question_step()
                page.rts.verify_availabilty_of_pregnancy_title()
                page.rts.open_pregnancy_questions()
                page.pregnancy.select_yes()
                page.pregnancy.enter_no_of_weeks()
                page.pregnancy.click_ok_button()
            else:
                pytest.skip("Pregnancy questions step is not available for male sailors")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_pregnancy_question')
            raise Exception(exp)

    @pytestrail.case(1670)
    def test_14_complete_rts_voyage_contract(self, page, web_driver, guest_data):
        """
        Function to complete voyage contract step in rts
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.rts.open_voyage_contract(guest_data[0]['GenderCode'])
            page.rts.verify_availabilty_of_voyage_contract_title()
            page.rts.start_voyage_contract()
            page.voyage_contract.verify_voyage_contract_page_available()
            page.voyage_contract.click_next_cta_to_open_voyage_contract()
            page.voyage_contract.sign_on_behalf_of_sailormate()
            page.voyage_contract.click_submit_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_voyage_contract')
            raise Exception(exp)

    @pytestrail.case(1658)
    def test_15_complete_rts_emergency_contact(self, page, web_driver, guest_data):
        """
        Function to complete emergency contact
        """
        try:
            page.rts.open_emergency_contact(guest_data[0]['GenderCode'])
            page.rts.verify_availabilty_of_emergency_contact_title()
            page.rts.start_emergency_contact()
            page.emergency_contact.enter_emergency_contact_name()
            page.emergency_contact.select_emergency_contact_relationship()
            page.emergency_contact.enter_emergency_contact_number()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_emergency_contact')
            raise Exception(exp)

    @pytestrail.case(1660)
    def test_16_complete_rts_step_aboard_flow(self, page, web_driver, guest_data, test_data):
        """
        Function to complete rts step aboard flow
        :param page:
        :param web_driver:
        :param guest_data:
        :param test_data:
        :return:
        """
        try:
            page.rts.open_step_aboard_flow(guest_data[0]['GenderCode'])
            page.rts.verify_availabilty_of_step_aboard_title()
            page.rts.start_step_aboard_task()
            page.step_aboard.verify_user_landed_on_embarkation_flight_question()
            page.step_aboard.select_yes_for_embarkation_flight()
            page.step_aboard.fill_inbound_flight_details()
            if guest_data[0]['isVIP']:
                page.step_aboard.verify_arrive_in_style_page()
                page.step_aboard.select_no_for_book_a_driver()
                page.step_aboard.verify_availability_of_rock_up_page()
                page.step_aboard.select_arrival_time_slot(test_data)
                page.step_aboard.select_no_for_debarkation_flight()
            else:
                page.step_aboard.verify_correct_flight_details_availeble()
                page.step_aboard.select_arrival_time_slot(test_data)
                page.step_aboard.verify_correct_flight_details_availeble()
                page.step_aboard.verify_embarkation_slot(test_data)
                page.step_aboard.click_parking_button()
                page.step_aboard.select_sailor_mate()
                page.step_aboard.select_no_for_debarkation_flight()
                page.rts.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_step_aboard_flow')
            raise Exception(exp)

    @pytestrail.case(6036305)
    def test_17_complete_health_form(self, page, web_driver, test_data):
        """
        Function to complete health form
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            today_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime("%Y-%m-%d")
            next_embark_date = datetime.strptime(test_data['next_embarkDate'], "%m/%d/%Y").strftime("%Y-%m-%d")
            if today_date == next_embark_date:
                page.home.open_homepage_tab()
                page.home.verify_precruise_text()
                page.home.open_health_form()
                page.health_form.verify_user_landed_on_health_form_introduction_page()
                page.health_form.start_health_form()
                page.health_form.fill_health_form_with_incorrect_answers()
                page.health_form.verify_error_modal_text()
                page.health_form.click_ok_button_on_error_modal()
                page.health_form.open_health_form()
                page.health_form.verify_health_form_rejected_page()
                page.health_form.fill_health_form_with_correct_answers()
            else:
                pytest.skip("Health form can be completed only on embarkation day")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_embarkation_slot_on_homepage')
            raise Exception(exp)

    @pytestrail.case(63449592)
    def test_18_verify_embarkation_slot_on_homepage(self, page, web_driver, test_data):
        """
        Function to verify correct embarkation slot available on homepage
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.verify_correct_embarkation_slot_shown_on_homepage(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_embarkation_slot_on_homepage')
            raise Exception(exp)

    @pytestrail.case(69553593)
    def test_19_verify_rockstar_spaces_available_for_vip_sailor(self, page, web_driver, guest_data):
        """
        Function to verify that vip sailor is able to access rockstar spaces
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_view_the_ship_spaces_quicklink()
            page.ship.verify_ship_spaces_header()
            if guest_data[0]['isVIP']:
                page.ship.verify_availability_of_rockstar_space_for_vip_sailor()
                page.ship.open_rockstar_space()
            else:
                page.ship.verify_unavailability_of_rockstar_space_for_non_vip_sailors()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_rockstar_spaces_available_for_vip_sailor')
            raise Exception(exp)

    @pytestrail.case(69553295)
    def test_20_verify_vip_sailor_is_able_to_access_rockstar_page(self, page, web_driver, guest_data):
        """
        Function to verify that vip sailor is able to access rockstar page
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            if guest_data[0]['isVIP']:
                page.home.open_me_tab()
                page.me.verify_availability_of_vip_avatar()
                page.me.click_vip_avatar()
                page.rockstar.verify_availability_of_rockstar_header()
                page.rockstar.verify_availability_of_introductory_message()
                page.rockstar.verify_availability_of_richards_rooftop()
                page.rockstar.verify_availability_of_in_room_bar()
                page.rockstar.verify_availability_of_early_booking_access()
                page.rockstar.verify_availability_of_rockstar_agents()
                page.rockstar.click_back()
            else:
                pytest.skip("Rockstar page is not available for non-vip sailors")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_vip_sailor_is_able_to_access_rockstar_page')
            raise Exception(exp)

    @pytestrail.case(68400494)
    def test_21_sign_voyage_well_form(self, page, web_driver, test_data):
        """
        Function to sign voyage well form
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.open_sign_voyage_well_form_task()
            page.voyage_well.verify_voyage_well_form_about_page()
            page.voyage_well.open_voyage_well_form()
            page.voyage_well.select_vaccination_status()
            page.voyage_well.enter_vaccination_name()
            page.voyage_well.select_vaccination_date_and_submit()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('sign_voyage_well_form')
            raise Exception(exp)

    @pytestrail.case(67652274)
    def test_22_verify_view_the_ship_spaces_quickink(self, page, web_driver):
        """
        To verify view the ship spaces quicklink on homepage
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_view_the_ship_spaces_quicklink()
            page.ship.verify_ship_spaces_header()
            page.ship.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_view_the_ship_spaces_quickink')
            raise Exception(exp)

    @pytestrail.case(67652275)
    def test_23_verify_view_your_agenda_quicklink(self, page, web_driver):
        """
        Function to verify view your agenda quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_view_your_agenda_quicklink()
            page.me.check_availability_of_myagenda()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_view_your_agenda_quicklink')
            raise Exception(exp)

    @pytestrail.case(67652277)
    def test_24_verify_book_dining_quicklink(self, page, web_driver):
        """
        Function to verify book dining quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_book_dining_quicklink()
            page.eateries.verify_eateries_header()
            page.eateries.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_dining_quicklink')
            raise Exception(exp)

    @pytestrail.case(68305272)
    def test_25_verify_book_a_shore_thing_quicklink(self, page, web_driver):
        """
        Function to verify book a shore thing quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_book_a_shore_thing_quicklink()
            page.ports.verify_availability_of_book_a_shore_thing_button()
            page.ports.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_a_shore_thing_quicklink')
            raise Exception(exp)

    @pytestrail.case(67652280)
    def test_26_verify_browse_the_event_lineup_quicklink(self, page, web_driver):
        """
        Function to verify browse the event lineup quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_browse_the_event_lineup_quicklink()
            page.discover.verify_availability_of_lineup_events()
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_browse_the_event_lineup_quicklink')
            raise Exception(exp)

    @pytestrail.case(67652279)
    def test_27_verify_book_a_spa_treatment_quicklink(self, page, web_driver):
        """
        Function to verify book a spa treatment quicklink
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_homepage_tab()
            page.home.verify_precruise_text()
            page.home.click_book_a_spa_treatment_quicklink()
            page.beauty_and_body.verify_availability_of_beauty_and_body_header()
            page.discover.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_book_a_spa_treatment_quicklink')
            raise Exception(exp)

    @pytestrail.case(12150694)
    def test_28_verify_discover_search(self, page, web_driver):
        """
        Function to verify discover search
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.home.verify_availability_of_search_bar()
            page.home.search_keyword()
            page.home.verify_search_results()
            page.home.open_and_verify_search_results()
            page.home.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_spa_page')
            raise Exception(exp)

    @pytestrail.case(11572032)
    def test_29_verify_lineup_availabiity(self, page, web_driver):
        """
        To verify that bookable lineup events should be avilable
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_lineup()
            page.discover.verify_availability_of_lineup_events()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lineup_availabiity')
            raise Exception(exp)

    @pytestrail.case(70024540)
    def test_30_verify_user_is_able_to_access_port_card_in_lineup(self, page, web_driver, test_data):
        """
        Function to verify user is able to access port card in lineup
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.discover.get_and_open_port_card(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_user_is_able_to_access_port_card_in_lineup')
            raise Exception(exp)

    @pytestrail.case(11572029)
    def test_31_verify_lineup_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:

            page.discover.select_and_open_lineup_event(test_data)
            page.discover.favourite_event(test_data)
            page.discover.book_lineup()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lineup_booking')
            raise Exception(exp)

    @pytestrail.case(11572033)
    def test_32_verify_lineup_booked_available_in_me_section(self, page, web_driver, test_data):
        """
        To verify that booked lineup is available in me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.check_availability_of_myagenda()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_event_name_on_event_detail_screen(test_data)
            page.event_detail.verify_number_of_guests_in_booking(2)
            page.event_detail.verify_event_day_and_date(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lineup_booked_available_in_me_section')
            raise Exception(exp)

    @pytestrail.case(11572030)
    def test_33_edit_lineup_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.click_edit_booking_details()
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.verify_user_navigated_to_correct_day(test_data)
            page.me.click_booked_event(test_data)
            page.event_detail.verify_number_of_guests_in_booking(1)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_lineup_and_verify')
            raise Exception(exp)

    @pytestrail.case(11572031)
    def test_34_cancel_lineup_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen_for_one_person()
            page.event_detail.click_done()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_lineup_and_verify')
            raise Exception(exp)

    @pytestrail.case(6036285)
    def test_35_default_slots_available_on_restaurant_listing_page(self, page, web_driver):
        """
        To verify that default slots are available on restaurant listing page
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship()
            page.ship.open_eateries()
            page.eateries.verify_availability_of_default_slots()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('default_slots_available_on_restaurant_listing_page')
            raise Exception(exp)

    @pytestrail.case(6036288)
    def test_36_book_dining(self, page, web_driver, test_data):
        """
        To verify that user is able to book dining
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.eateries.book_dining()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('book_dining')
            raise Exception(exp)

    @pytestrail.case(6036306)
    def test_37_verify_booked_dining_is_available_in_my_agenda(self, page, web_driver, test_data):
        """
        To verify that booked dining is available in my agenda
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.check_availability_of_myagenda()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_event_name_on_event_detail_screen(test_data)
            page.event_detail.verify_number_of_guests_in_booking(2)
            page.event_detail.verify_event_day_and_date(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_dining_is_available_in_my_agenda')
            raise Exception(exp)

    @pytestrail.case(6036289)
    def test_38_edit_dining_and_verify(self, page, web_driver, test_data):
        """
        To edit dining and verify
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.click_edit_booking_details()
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_number_of_guests_in_booking(1)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_dining_and_verify')
            raise Exception(exp)

    @pytestrail.case(6036290)
    def test_39_cancel_dining_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen_for_one_person()
            page.event_detail.click_done()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_dining_and_verify')
            raise Exception(exp)

    @pytestrail.case(63587280)
    def test_40_verify_that_restaurants_should_not_be_duplicate(self, page, web_driver):
        """
        Function to verify that restaurants should not be duplicate
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship()
            page.ship.open_eateries()
            page.eateries.verify_no_duplicate_venue_available()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('restaurants_should_not_be_duplicate')
            raise Exception(exp)

    @pytestrail.case(69005964)
    def test_41_book_dining_from_restaurant_details_page(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.eateries.open_restaurant_details_page()
            page.restaurant_details.verify_user_landed_on_restaurant_details_page()
            page.discover.favourite_event(test_data)
            page.restaurant_details.click_find_a_table()
            page.restaurant_details.select_booking_details()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
            page.confirmation_screen.click_view_in_my_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_dining_and_verify')
            raise Exception(exp)

    @pytestrail.case(69005980)
    def test_42_verify_that_user_gets_conflict_while_booking_same_restuarant_two_times(self, page, web_driver, test_data):
        """
        Function to verify that user gets conflict while booking same restuarant two time
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship()
            page.ship.open_eateries()
            page.eateries.verify_availability_of_default_slots()
            page.eateries.click_default_slot()
            page.eateries.verify_repeat_restaurant_conflict_screen()
            page.eateries.navigate_away_from_conflict_screen()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('book_dining')
            raise Exception(exp)

    @pytestrail.case(69006044)
    def test_43_verify_excursion_filter(self, page, web_driver, test_data):
        """
        Function to verify excursion filter
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ports()
            page.ports.click_book_excursion()
            page.ports.open_port_guide()
            page.ports.get_events_categories_available(test_data)
            page.ports.apply_filter_and_verify(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_excursion_filter')
            raise Exception(exp)

    @pytestrail.case(507111)
    def test_44_verify_excursion_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ports()
            page.ports.click_book_excursion()
            page.ports.select_and_open_excursion_event(test_data)
            page.discover.favourite_event(test_data)
            page.ports.book_excursion()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_pay_with_existing_card()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_excursion_booking')
            raise Exception(exp)

    @pytestrail.case(507112)
    def test_45_verify_excursion_booked_available_in_me_section(self, page, web_driver, test_data):
        """
        To verify that booked lineup is available in me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.check_availability_of_myagenda()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_event_name_on_event_detail_screen(test_data)
            page.event_detail.verify_number_of_guests_in_booking(2)
            page.event_detail.verify_event_day_and_date(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_excursion_booked_available_in_me_section')
            raise Exception(exp)

    @pytestrail.case(507113)
    def test_46_edit_excursion_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.click_edit_booking_details()
            page.event_detail.edit_booking()
            page.summary.verify_summary_screen()
            page.summary.save_details_on_summary_screen(test_data)
            page.summary.click_confirm_button()
            page.confirmation_screen.click_view_in_my_sailor_log()
            page.me.click_booked_event(test_data)
            page.event_detail.verify_number_of_guests_in_booking(1)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_excursion_and_verify')
            raise Exception(exp)

    @pytestrail.case(507114)
    def test_47_cancel_excursion_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.event_detail.cancel_booking()
            page.event_detail.verify_cancelled_screen_for_one_person()
            page.event_detail.click_done()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('cancel_excursion_and_verify')
            raise Exception(exp)

    @pytestrail.case(64599863)
    def test_48_verify_spa_page(self, page, web_driver, test_data):
        """
        To verify that user is able to book lineup
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_ship()
            page.ship.open_beauty_and_body()
            page.beauty_and_body.open_redemption_spa()
            page.eateries.verify_no_duplicate_venue_available()
            page.redemption_spa.open_resurrection_accupuncture()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_spa_page')
            raise Exception(exp)

    @pytestrail.case(70422465)
    def test_49_verify_spa_booking(self, page, web_driver, test_data):
        """
        To verify that user is able to book spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
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
            page.summary.click_confirm_button()
            page.summary.verify_booking_confirmation_screen()
            page.summary.click_view_in_sailor_log()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_spa_booking')
            raise Exception(exp)

    @pytestrail.case(71593732)
    def test_50_verify_booked_spa_in_my_agenda_of_me_section(self, page, web_driver, test_data):
        """
        To verify that booked spa is available in my agenda of me section
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")
            page.me.check_availability_of_myagenda()
            page.me.verify_landing_on_booked_date(test_data)
            page.me.click_booked_spa_event(test_data)
            page.event_detail.verify_booked_event_title(test_data)
            page.event_detail.verify_booked_event_schedule_and_location(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_booked_spa_in_my_agenda_of_me_section')
            raise Exception(exp)

    @pytestrail.case(70422467)
    def test_51_edit_booked_spa_and_verify(self, page, web_driver, test_data):
        """
        To verify that user is able to edit booked spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['spa_slots_availability']:
                pytest.skip("Skipping this TC as no spa slots available for booking")
            event = "spa"
            page.event_detail.click_edit_booking_details(test_data, event)
            if not test_data[f'{event}_editing']:
                page.discover.click_back_button()
                pytest.skip("Skipping this TC as Sailor can’t amend a booking so close to to the start time")
            page.event_detail.edit_spa_booking()
            page.summary.verify_summary_screen()
            page.summary.save_edited_spa_details(test_data)
            page.summary.click_confirm_button()
            page.summary.verify_booking_confirmation_screen()
            page.summary.click_view_in_sailor_log()
            page.me.click_booked_spa_event(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('edit_booked_spa_and_verify')
            raise Exception(exp)

    @pytestrail.case(70422468)
    def test_52_cancel_booked_spa(self, page, web_driver, test_data):
        """
        To verify that user is able to cancel booked spa
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            if not test_data['spa_slots_availability']:
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
    @pytestrail.case(70024541)
    def test_53_verify_user_is_able_to_access_guides_from_lineup(self, page, web_driver):
        """
        Function to verify that user is able to access guides
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_discover_tab()
            page.discover.open_guides()
            page.guides.verify_user_landed_on_guides_page()
            page.guides.open_and_verify_guides()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_user_is_able_to_access_guides')
            raise Exception(exp)

    @pytestrail.case(70024732)
    def test_54_verify_default_notification(self, page, web_driver):
        """
        Verify that default notification is available in messenger
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_messenger_tab()
            page.messenger.verify_user_landed_on_messenger_screen()
            page.messenger.verify_default_notification_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_default_notification')
            raise Exception(exp)

    @pytestrail.case(70024795)
    def test_55_update_notification_settings_from_messenger(self, page, web_driver):
        """
        Update notification settings from messenger
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.messenger.click_notification_card()
            page.messenger.verify_user_landed_on_notification_listing_screen()
            page.messenger.open_notification_settings()
            page.messenger.turn_reminders_off()
            page.setting.click_back_button()
            page.messenger.open_notification_settings()
            page.setting.verify_reminder_off()
            page.messenger.turn_reminder_on()
            page.setting.click_back_button()
            page.messenger.open_notification_settings()
            page.messenger.verify_reminder_on()
            page.setting.click_back_button()
            page.messenger.click_cross_icon()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_default_notification')
            raise Exception(exp)

    @pytestrail.case(70024538)
    def test_56_view_cabin_mates_profile(self, page, web_driver, guest_data):
        """
        Verify that user is able to view cabin mates profile
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.messenger.verify_user_landed_on_messenger_screen()
            page.messenger.open_contacts()
            page.contacts.open_cabin_mates_profile()
            page.contacts.verify_cabin_mate_name(guest_data)
            page.contacts.allow_cabin_mate_to_see_what_primary_sailor_is_attending()
            page.contacts.click_back_button()
            page.contacts.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_default_notification')
            raise Exception(exp)

    @pytestrail.case(63449422)
    def test_57_verify_wallet_of_primary_sailor(self, page, web_driver, test_data):
        """
        Function to verify wallet for primary sailor
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab()
            page.me.open_my_wallet()
            page.wallet.click_wallet_next_cta()
            page.rts.verify_availability_of_payment_method()
            page.rts.click_payment_edit_button()
            page.payment.verify_card_details()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_wallet_of_primary_sailor')
            raise Exception(exp)

    @pytestrail.case(24938090)
    def test_58_delete_credit_card(self, page, web_driver, test_data):
        """
        Function to delete card
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.payment.verify_availability_of_payment_method_header()
            page.payment.delete_card()
            page.payment_methods.verify_payment_method_title_question()
            page.payment_methods.select_credit_card()
            page.payment.verify_enter_card_details_page_available()
            page.payment.click_back()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('delete_credit_card')
            raise Exception(exp)

    @pytestrail.case(63498835)
    def test_59_verify_no_of_days_in_my_agenda(self, page, web_driver, test_data):
        """
        Function to verify no of days in my agenda
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.me.check_availability_of_myagenda()
            page.me.get_days_and_dates_of_voyage(test_data)
            page.me.get_and_verify_days_available_in_my_agenda(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_no_of_days_in_my_agenda')
            raise Exception(exp)

    @pytestrail.case(11777725)
    def test_60_booking_procedure_available_in_shipeats(self, page, web_driver):
        """
        To verify that ship eats booking procedure is available in shipeats
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.open_services_tab()
            page.services.verify_services_header()
            page.services.open_ship_eats()
            page.shipeats.verify_shipeats_header()
            page.shipeats.verify_shipeats_steps_header()
            page.shipeats.click_back()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('booking_procedure_available_in_shipeats')
            raise Exception(exp)

    @pytestrail.case(11777726)
    def test_61_verify_cabin_services_screen(self, page, web_driver):
        """
        To verify cabin services screen
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.services.verify_services_header()
            page.services.open_cabin_services()
            page.shipeats.verify_cabin_services_header()
            page.shipeats.verify_cabin_services_content()
            page.shipeats.click_back()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_cabin_services_screen')
            raise Exception(exp)

    @pytestrail.case(65977839)
    def test_62_verify_help_and_support_screen(self, page, web_driver):
        """
        To verify help and support screen
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.services.verify_services_header()
            page.services.open_help_and_support()
            page.help_and_support.verify_availability_of_search_bar()
            page.help_and_support.verify_help_and_support_question_categories()
            page.help_and_support.verify_availability_of_email_and_call_buttons()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_help_and_support_screen')
            raise Exception(exp)

    @pytestrail.case(66799540)
    def test_63_verify_search_in_help_and_support(self, page, web_driver):
        """
        To verify that user is able to search keyword in help and support
        :return:
        """
        try:
            page.help_and_support.search_keyword()
            page.help_and_support.verify_availability_of_search_results()
            page.help_and_support.open_questions_in_search_results()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_search_in_help_and_support')
            raise Exception(exp)

    @pytestrail.case(1676)
    def test_64_verify_lovelist(self, page, web_driver, test_data):
        """
        To verify that user is able add bookable events to lovelist
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.home.open_me_tab()
            page.me.open_lovelist()
            page.me.verify_events_available_in_lovelist()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_lovelist')
            raise Exception(exp)

    @pytestrail.case(1656)
    def test_65_verify_the_rts_security_photo_flow(self, page, web_driver):
        """
        Test case to complete security photo in rts
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.home.click_checkin_and_get_ready_to_sail()
            page.rts.open_security_photo_flow()
            page.rts.start_security_photo_flow()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_the_rts_security_photo_flow')
            raise Exception(exp)

    @pytestrail.case(1667)
    def test_66_verify_availability_of_all_voyage_settings(self, page, web_driver):
        """
        Verify that all voyage settings are available
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.me.click_on_setting_icon()
            page.setting.verify_setting_screen_landing()
            page.setting.verify_availability_of_notifications_and_privacy()
            page.setting.verify_availability_of_emergency_contact()
            page.setting.verify_availability_of_sailing_documents()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_voyage_settings')
            raise Exception(exp)

    @pytestrail.case(67433674)
    def test_67_verify_reminders(self, page, web_driver):
        """
        To verify reminders
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.me.click_on_setting_icon()
            page.setting.open_notification_and_privacy()
            page.setting.turn_reminders_off()
            page.setting.click_back_button()
            page.setting.open_notification_and_privacy()
            page.setting.verify_reminder_off()
            page.settings.turn_reminder_on()
            page.setting.click_back_button()
            page.setting.open_notification_and_privacy()
            page.setting.verify_reminder_on()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_reminders')
            raise Exception(exp)

    @pytestrail.case(67433675)
    def test_68_verify_emergency_contact(self, page, web_driver):
        """
        To verify emergency contact
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.open_emergency_contact()
            page.rts.verify_availabilty_of_emergency_contact_title()
            page.rts.start_emergency_contact()
            page.emergency_contact.enter_emergency_contact_name()
            page.emergency_contact.select_emergency_contact_relationship()
            page.emergency_contact.enter_emergency_contact_number()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_emergency_contact')
            raise Exception(exp)

    @pytestrail.case(6036307)
    def test_69_verify_availability_of_all_profile_setting(self, page, web_driver):
        """
        Function to verify availability of profile settings section
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.verify_availability_of_profile_settings_title()
            page.setting.verify_availability_of_personal_information()
            page.setting.verify_availability_of_contact_details()
            page.setting.verify_availability_of_login_details()
            page.setting.verify_availability_of_payment_methods()
            page.setting.verify_availability_of_communication_preferences()
            page.setting.verify_availability_of_terms_and_conditions()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_availability_of_all_profile_setting')
            raise Exception(exp)

    @pytestrail.case(26958507)
    def test_70_update_personal_information(self, page, web_driver, test_data):
        """
        Function to update and verify personal information
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.setting.open_personal_info()
            page.setting.verify_sailor_landed_on_personal_info_section()
            page.setting.update_personal_info(test_data)
            page.setting.click_next_cta()
            page.setting.open_personal_info()
            page.setting.verify_updated_personal_info(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('update_personal_information')
            raise Exception(exp)

    @pytestrail.case(1812)
    def test_71_update_contact_details(self, page, web_driver):
        """
        Testcase to update and verify contact details
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.settings.open_contact_details_section()
            page.setting.update_contact_details()
            page.setting.click_next_cta()
            page.setting.open_contact_details_section()
            page.setting.verify_updated_contact_detais()
            page.setting.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('update_contact_details')
            raise Exception(exp)

    @pytestrail.case(67433676)
    def test_72_update_and_verify_email(self, page, web_driver, guest_data):
        """
        To update and verify email
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.open_login_details()
            page.setting.update_email(guest_data)
            page.setting.click_next_cta()
            page.setting.verify_email_updated_confirmation_screen()
            page.setting.click_done_button()
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(guest_data[0]['Email'], 'Yellow*99')
            page.home.verify_precruise_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('update_and_verify_email')
            raise Exception(exp)

    @pytestrail.case(67433677)
    def test_73_update_password(self, page, web_driver, guest_data):
        """
        To update and verify password details
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.setting.open_login_details()
            page.setting.update_password()
            page.setting.click_save_button()
            page.setting.verify_password_updated_confirmation_screen()
            page.setting.click_done_button()
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(guest_data[0]['Email'], 'Voyages@9876')
            page.home.verify_precruise_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('update_password')
            raise Exception(exp)

    @pytestrail.case(67433678)
    def test_74_add_payment_method(self, page, web_driver, guest_data):
        """
        Function to add payment method in settings
        :param page:
        :param web_driver:
        :param guest_data:
        :return:
        """
        try:
            page.setting.open_payment_methods()
            page.payment.click_addcard_button()
            page.payment.fill_payment_card_details(guest_data)
            page.payment.verify_card_saved(guest_data)
            page.payment.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('add_payment_method')
            raise Exception(exp)

    @pytestrail.case(67433679)
    def test_75_verify_communication_preferences(self, page, web_driver):
        """
        Function to verify communication preferences
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.open_communication_preferences()
            page.preferences.verify_communication_preferences_page_landing()
            page.preferences.check_all_communication_preferences()
            page.preferences.click_submit_button()
            page.preferences_updated.verify_communication_preferences_updated_title()
            page.preferences_updated.click_next_cta()
            page.setting.open_communication_preferences()
            page.preferences.verify_communication_preferences_checked()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_communication_preferences')
            raise Exception(exp)

    @pytestrail.case(67433680)
    def test_76_verify_security_and_guide(self, page, web_driver):
        """
        Function to verify security guide
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.setting.open_terms_and_conditions()
            page.terms_and_conditions.verify_terms_and_conditions_page_landing()
            page.terms_and_conditions.open_security_guide()
            page.security_guide.verify_security_guide_page_landing()
            page.security_guide.content_available_in_security_guide()
            page.security_guide.download_security_guide()
            page.security_guide.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_security_and_guide')
            raise Exception(exp)

    @pytestrail.case(67433681)
    def test_77_verify_mobile_terms_and_conditions(self, page, web_driver):
        """
        Function to verify mobile terms and conditions
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.terms_and_conditions.verify_terms_and_conditions_page_landing()
            page.terms_and_conditions.open_mobile_terms_and_conditions()
            page.mobile_terms.verify_mobile_terms_and_conditions_page_landing()
            page.mobile_terms.content_available_in_mobile_terms_and_conditions()
            page.mobile_terms.download_mobile_terms_and_conditions()
            page.mobile_terms.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_mobile_terms_and_conditions')
            raise Exception(exp)

    @pytestrail.case(67433682)
    def test_78_verify_privacy_policy(self, page, web_driver):
        """
        Function to verify privacy policy
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.terms_and_conditions.verify_terms_and_conditions_page_landing()
            page.terms_and_conditions.open_privacy_policy()
            page.privacy_policy.verify_privacy_policy_landing()
            page.privacy_policy.content_available_in_privacy_policy()
            page.privacy_policy.download_privacy_policy()
            page.privacy_policy.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_privacy_policy')
            raise Exception(exp)

    @pytestrail.case(67433683)
    def test_79_verify_cookie_policy(self, page, web_driver):
        """
        Function to verify cookie policy
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.terms_and_conditions.verify_terms_and_conditions_page_landing()
            page.terms_and_conditions.open_cookie_policy()
            page.cookie_policy.verify_cookie_policy_landing()
            page.privacy_policy.content_available_in_cookie_policy()
            page.privacy_policy.download_cookie_policy()
            page.privacy_policy.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_cookie_policy')
            raise Exception(exp)

    @pytestrail.case(67433684)
    def test_80_verify_switch_voyage(self, page, web_driver, test_data):
        """
        Function to verify switch voyage
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.settings.click_switch_voyage()
            page.switch_voyage.verify_switch_voyage_page_landing()
            page.switch_voyage.verify_availability_of_voyage_image()
            page.switch_voyage.verify_voyage_name(test_data)
            page.home.verify_precruise_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_switch_voyage')
            raise Exception(exp)

    @pytestrail.case(1672)
    def test_81_verify_connect_booking(self, page, web_driver, config, rest_shore, guest_data, request, test_data):
        """
        Function to verify connect booking
        :param page:
        :param web_driver:
        :param config:
        :param rest_shore:
        :param guest_data:
        :param request:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request)
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.settings.click_switch_voyage()
            page.switch_voyage.verify_switch_voyage_page_landing()
            page.switch_voyage.click_connect_booking()
            page.connect_booking.verify_connect_booking_screen_available()
            page.connect_booking.connect_the_booking(guest_data, test_data)
            page.home.verify_precruise_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_switch_voyage')
            raise Exception(exp)

    @pytestrail.case(1669)
    def test_82_logout_from_sailor_app(self, page):
        """
        Go to Account page
        :param page:
        :return:
        """
        page.home.open_me_tab()
        page.me.click_on_setting_icon()
        page.setting.logout()

    @pytestrail.case(67809277)
    def test_83_verify_post_voyage_screen_for_sailor_having_past_voyage(self, page, web_driver):
        """
        Function to verify that post voyage screen is available for sailor having past voyage
        :param page:
        :param web_driver:
        """
        try:
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details('christinestevens_749083@mailinator.com', 'Voyages@9876')
            page.home.verify_post_voyage_screen()
            page.home.verify_global_navigation_menu_disabled_on_post_voyage_screen()
            page.home.click_switch_voyage()
            page.login.go_to_settings_after_signup()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('verify_post_voyage_screen')
            raise Exception(exp)

    @pytestrail.case(63455176)
    def test_84_complete_rts_travel_documents_for_indian_sailor(self, page, web_driver, request, guest_data, config, rest_shore, v_guest_data, test_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param request:
        :param guest_data:
        :param config:
        :param rest_shore:
        :param v_guest_data:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data,
                                           country="India")
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(guest_data[0]['Email'], 'Voyages@9876')
            page.home.verify_precruise_text()
            nationality = 'India'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_available_primary_documents_option()
            page.travel_docs.select_passport()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_available_documents_option()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.travel_docs.verify_correct_details_available_after_scanning_passport()
            page.travel_docs.fill_correct_sailor_details()
            page.travel_docs.user_landed_on_visa_scan_screen()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_visa_image()
            page.travel_docs.fill_correct_visa_details(guest_data)
            page.post_voyage.fill_post_voyage_details()
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(71595223)
    def test_85_complete_rts_travel_documents_for_indian_sailor_with_green_card(self, page, web_driver, request, guest_data, config,
                                                                rest_shore, v_guest_data, test_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param request:
        :param guest_data:
        :param config:
        :param rest_shore:
        :param v_guest_data:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data,
                                           country="India")
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(v_guest_data[0]['Email'], 'Voyages@9876')
            nationality = 'India'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_available_primary_documents_option()
            page.travel_docs.select_green_card()
            page.green_card.verify_green_card_scan_screen()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.green_card.verify_correct_details_available_after_scanning_passport(nationality)
            page.green_card.fill_correct_sailor_details(guest_data, nationality)
            page.travel_docs.click_done_cta()
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(1663)
    def test_86_complete_rts_travel_documents_for_schengen_sailor_with_passport(self, page, web_driver, request, guest_data, config,
                                                                rest_shore, v_guest_data, test_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param request:
        :param guest_data:
        :param config:
        :param rest_shore:
        :param v_guest_data:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data,
                                           country="Italy")
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(v_guest_data[0]['Email'], 'Voyages@9876')
            page.home.verify_precruise_text()
            nationality = 'Italy'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_passport_scan_screen_available()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.travel_docs.verify_correct_details_available_after_scanning_passport(nationality)
            page.travel_docs.fill_correct_sailor_details(guest_data, nationality)
            page.travel_docs.click_done_cta()
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(71595224)
    def test_77_complete_rts_travel_documents_for_schenegen_sailor_with_green_card(self, page, web_driver, request,
                                                                                guest_data, config,
                                                                                rest_shore, v_guest_data, test_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param request:
        :param guest_data:
        :param config:
        :param rest_shore:
        :param v_guest_data:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data,
                                           country="India")
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(v_guest_data[0]['Email'], 'Voyages@9876')
            page.home.verify_precruise_text()
            nationality = 'Italy'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_available_primary_documents_option()
            page.travel_docs.select_green_card()
            page.green_card.verify_green_card_scan_screen()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.green_card.verify_correct_details_available_after_scanning_green_card(nationality)
            page.green_card.fill_correct_sailor_details_for_green_card(guest_data, nationality)
            page.travel_docs.click_done_cta()
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

    @pytestrail.case(71595225)
    def test_88_complete_rts_travel_documents_for_uk_sailor(self, page, web_driver, request, guest_data, config,
                                                                rest_shore, v_guest_data, test_data):
        """
        Function to complete rts step 3 payment method
        :param page:
        :param web_driver:
        :param request:
        :param guest_data:
        :param config:
        :param rest_shore:
        :param v_guest_data:
        :param test_data:
        :return:
        """
        try:
            page.apihit.create_reservation(config, test_data, rest_shore, guest_data, request, v_guest_data,
                                           country="UK")
            page.login.open_signin_page()
            page.login.open_signin_with_email()
            contexts = web_driver.get_contexts()
            web_driver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            page.login.fill_signin_details(v_guest_data[0]['Email'], 'Voyages@9876')
            page.home.verify_precruise_text()
            page.home.open_rts()
            nationality = 'United Kingdom'
            page.home.verify_precruise_text()
            page.home.open_rts()
            page.rts.open_travel_document_step()
            page.rts.start_travel_documents()
            page.travel_docs.verify_natioanality_on_travel_docs_introduction_page(nationality)
            page.travel_docs.click_next_button()
            page.travel_docs.verify_passport_scan_screen_available()
            page.travel_docs.click_scan_document_button()
            page.travel_docs.give_permission_to_use_camera()
            page.travel_docs.click_upload_document()
            page.travel_docs.allow_to_access_media()
            page.travel_docs.select_image()
            page.travel_docs.verify_correct_details_available_after_scanning_passport(nationality)
            page.travel_docs.fill_correct_sailor_details(guest_data, nationality)
            page.travel_docs.click_done_cta()
            page.home.open_me_tab()
            page.me.click_on_setting_icon()
            page.setting.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('complete_rts_payment_method')
            raise Exception(exp)

