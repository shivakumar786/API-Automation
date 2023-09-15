from ui_pages.book_voyage.apihit import Apihit
from ui_pages.book_voyage.choose_voyage import ChooseVoyage
from ui_pages.book_voyage.signin import BookVoyageSignIn
from virgin_utils import *


@pytest.mark.Voyage_Booking_UI
@pytest.mark.run(order=12)
class TestVoyageBooking:
    """
    Test Suite to test Voyage booking
    """
    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(47468003)
    def test_01_launch_website_and_signup(self, web_driver, page, config, rest_ship, test_data, guest_data):
        """
        Test cases to Launch the book voyage website and signup with sailor details
        :param test_data:
        :param rest_ship:
        :param web_driver:
        :param page:
        :param config:
        :param guest_data:
        :return:
        """
        try:
            setattr(page, 'signin', BookVoyageSignIn(web_driver))
            setattr(page, 'choosevoyage', ChooseVoyage(web_driver, test_data))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data))
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_next_voyage(test_data)
            web_driver.open_website(url=urljoin(config.shore.url.replace('/svc', ''), "/book/accounts/signin"))
            page.signin.verification_of_signin_page()
            web_driver.allure_attach_jpeg("availability_of_signin_page")
            page.signin.click_signup_with_email()
            page.signin.verification_of_signup_page()
            page.signin.signup_of_sailor(guest_data, 0)
            pagetitle = page.choosevoyage.verify_sailor_details_page()
            assert pagetitle == "Ahoy", "Sailor is not on sailor details page"
            page.choosevoyage.logout()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Signup_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(955)
    def test_02_signup_and_verify_dashboard(self, web_driver, page, guest_data):
        """
        Test cases to signIn with sailor credentials and verify voyage dashboard
        :param guest_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.click_signin_account_button()
            page.signin.verification_of_signin_page()
            page.signin.sign_in(guest_data)
            page_title = page.choosevoyage.verify_sailor_details_page()
            assert page_title == "Ahoy", "Sailor is not on sailor details page"

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("SignIn_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(989)
    def test_03_verify_go_to_account_cta(self, web_driver, page):
        """
        Test cases to behavior of Go To Your Account CTA available on confirmation screen when sailor is logged in
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_go_to_account()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Go_to_your_account_cta_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(957)
    def test_04_select_plan_voyage_and_verify_select_voyage_page(self, web_driver, page, test_data):
        """
        Test cases to verify voyage list page
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.click_plan_voyage_button()
            if not page.choosevoyage.verify_voyage_list():
                page.choosevoyage.reduce_sailor_count()
                if not page.choosevoyage.verify_voyage_list():
                    test_data['VoyageAvailability'] = False
                    raise Exception("No voyages available for booking")
                else:
                    test_data['VoyageAvailability'] = True
            else:
                test_data['VoyageAvailability'] = True
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Voyage_error")
            raise Exception(exp)

    @pytestrail.case(973)
    def test_5_verify_accesible_cabins(self, web_driver, page):
        """
        Test cases to verify accesible cabins clickable or not
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.accesible_cabins()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("accesible_cabins_not_clickables")
            raise Exception(exp)

    @pytestrail.case(75940682)
    def test_6_verify_reset_all_button(self, web_driver, page):
        """
        To verify the the reset all button
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("reset_all")
            raise Exception(exp)

    @pytestrail.case(69691176)
    def test_7_verify_travel_party(self,  web_driver, page):
        """
        To verify the the travel party
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.travel_party()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Travel_party")
            raise Exception(exp)

    @pytestrail.case(73944245)
    def test_8_verify_defaul_sailor_per_night(self, web_driver, page):
        """
        To verify that default sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_sailor_per_night()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Sailor_per_night")
            raise Exception(exp)

    @pytestrail.case(1075)
    def test_9_verify_travel_date(self, web_driver, page):
        """
        To verify that default sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.apply_travel_date_filter()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Travel_date")
            raise Exception(exp)

    @pytestrail.case(69686486)
    def test_10_verify_destination_filter(self, web_driver, page):
        """
        To verify that destination filter
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_destination_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Destination_filter")
            raise Exception(exp)

    @pytestrail.case(69686485)
    def test_11_verify_togle_btw_itenary_pot(self, web_driver, page):
        """
        To verify that default sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_togle_ite_pot()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("toggle_btw_port")
            raise Exception(exp)

    @pytestrail.case(69926557)
    def test_12_verify_filter(self, web_driver, page):
        """
        To verify that default sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Verify_filter")
            raise Exception(exp)

    @pytestrail.case(70417669)
    def test_13_verify_weekend_filter(self,  web_driver, page):
        """
        To verify that weekend filter
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.weekend_filter()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("weeken_filter")
            raise Exception(exp)

    @pytestrail.case(70436176)
    def test_14_verify_the_cabins(self, web_driver, page):
        """
        To verify that cabins type
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.cabins_type()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cabins_type")
            raise Exception(exp)

    @pytestrail.case(70436007)
    def test_15_verify_price_per_cabin_sailor(self, web_driver, page):
        """
        To verify price per cabin , sailor, sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_filter()
            page.choosevoyage.verify_price()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Verify_price_per_sailor_cabin")
            raise Exception(exp)

    @pytestrail.case(70436177)
    def test_16_verify_ship_filter(self, web_driver, page):
        """
        To verify price per cabin , sailor, sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_filter()
            page.choosevoyage.verify_ship_filter()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Verify_ship_filter")
            raise Exception(exp)

    @pytestrail.case(70436178)
    def test_17_verify_departure_port_filter(self, web_driver, page):
        """
        To verify price per cabin , sailor, sailor per night
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_filter()
            page.choosevoyage.verify_departure_port()
            page.choosevoyage.reset_all()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Verify_dipature_port_filter")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(1002)
    def test_18_select_cabin(self, web_driver, page, test_data):
        """
        Test cases to verify user is able to see the month range filter on UI
        :param web_driver:
        :param test_data:
        :param page:
        :return:
        """
        try:
            if not test_data['VoyageAvailability']:
                raise Exception("No voyages available for booking")
            else:
                page.choosevoyage.select_choose_voyage()
                page.choosevoyage.select_cabin()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("select_cabin_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(1003)
    def test_19_verify_summary_page(self, web_driver, page):
        """
        Test cases to verify user is able land on summary page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.choosevoyage.verify_summary_page() != "SUMMARY":
                raise Exception("User is not landed on summary page")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("summary_page_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(983)
    def test_20_verify_edit_icon_summary_card(self, web_driver, page):
        """
        To verify the edit icon on summary page.
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.verify_itenary_edit_icon()
            page.choosevoyage.verify_cabin_edit_icon()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Summary_icon")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(958)
    def test_21_verify_persistent_header(self, web_driver, page):
        """
        To verify the persistent header summary details
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.verify_persistent_header()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("tell_me_more")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(982)
    def test_22_verify_total_voyage_and_cabin_count(self, web_driver, page):
        """
        Test cases to verify voyage total and cabin total on the summary page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            voyage_price = page.choosevoyage.get_voyage_count()
            total_cabin_price = page.choosevoyage.get_cabin_count()
            assert voyage_price == total_cabin_price, "voyage price and cabin prices are not matching"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("voyage_cabin_count_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(988)
    def test_23_verify_checkout_button(self, web_driver, page):
        """
        Test cases to verify checkout button
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.choosevoyage.verify_checkout():
                page.choosevoyage.click_checkout()
            else:
                raise Exception("Checkout option is not available in summary page")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("checkout_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(961)
    def test_24_verify_sailor_details_page(self, web_driver, page):
        """
        Test cases to verify sailor details page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.choosevoyage.verify_sailor_details():
                raise Exception("Sailor details fields are not available")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_details_page_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(972)
    def test_25_verify_price_after_choose_cabin_and_voyage(self, web_driver, page):
        """
        To verify the login functionality.
        """
        try:
            page.choosevoyage.verify_cabin_and_voyage_amount()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(956)
    def test_26_verify_tell_me_more(self, web_driver, page):
        """
        To verify the tell me more functionality
        :params web_driver:
        :params web_driver:
        """
        try:
            if not page.choosevoyage.verify_tell_me_more():
                raise Exception("Tell me button not available")
            page.choosevoyage.click_on_tell_me()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("tell_me_more")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(992)
    def test_27_verify_tell_me_flyout(self, web_driver, page):
        """
        To verify that user is able to click on accessible filter
        :params web_driver:
        :params page:
        """
        try:
            if not page.choosevoyage.verify_tell_me_more():
                raise Exception("Tell me button not available")
            page.choosevoyage.click_on_tell_me()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("tell_me_more")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(964)
    def test_28_verify_travel_insurance_amount(self, web_driver, page):
        """
        To verify travel insurance amount
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.verify_progress_bar_amoount()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(971)
    def test_29_verify_address_field_travel_insurance(self, web_driver, page):
        """
        To verify travel insurance field
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.travel_insurance_field()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(975)
    def test_30_change_country_travel_insurance(self, web_driver, page):
        """
        To verify travel insurance field
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.travel_insurance_field()
            page.choosevoyage.select_country("India")
            page.choosevoyage.select_state("Bihar")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(968)
    def test_31_verify_usa_sailor_field(self, web_driver, page, guest_data):
        """
        Test cases to verify USA sailor details
        :param web_driver:
        :param guest_data:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.click_gender()
            page.choosevoyage.select_citizenship("United States")
            page.choosevoyage.select_country_code(6, guest_data[0]['Phones'][0]['number'])
            page.choosevoyage.click_category()

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("usa_sailor_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(235)
    def test_32_verify_continue_button(self, web_driver, page):
        """
        Test cases to verify functionality of "Continue" button on sailor detail page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.click_continue_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("continue_button_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(995)
    def test_33_verify_persistent_header_on_payment_page(self, web_driver, page):
        """
        To verify the persistent header summary details
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.verify_persistent_header_on_payment()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Header_displayed")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(1000)
    def test_34_verify_price_on_payment_page(self, web_driver, page):
        """
        To verify the login functionality.
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_amount_on_payment()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(963)
    def test_35_verify_term_condition(self, web_driver, page):
        """
        To verify the term and condition.
        :params web_driver:
        :params page:
        """
        try:
            if not page.choosevoyage.get_term_and_condition():
                raise Exception("Term & Condition is not avaialable")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("term_and_condition")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(985)
    def test_36_verify_term_and_condition_checkbox(self, web_driver, page):
        """
        To verify the login functionality.
        :params web_driver:
        :params page:
        """
        try:
            page.choosevoyage.verify_check_box()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("insurance_amount")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(986)
    def test_37_verify_pay_and_continue_button(self, web_driver, page):
        """
        To verify the login functionality.
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_pay_continue_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("continue_button_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(1004)
    def test_39_click_pay_and_continue_button(self, web_driver, page, guest_data):
        """
        Test cases to verify The behavior of "Continue" button on payment page
        :param web_driver:
        :param page:
        :param guest_data:
        :return:
        """
        try:
            page.choosevoyage.fill_payment_page(guest_data, "United States")
            page.choosevoyage.click_pay_button()

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("pay_button_error")
            raise Exception(exp)

    @pytest.mark.USA
    @pytest.mark.INDIA
    @pytestrail.case(993)
    def test_39_verify_confirmation_page(self, web_driver, page):
        """
        Test cases to verify the details available on confirmation screen
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.choosevoyage.verify_confirmation_page() is None:
                raise Exception("Booking failed")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("booking_confirmation_error")
            raise Exception(exp)

    @pytestrail.case(1013)
    def test_40_verify_reservation_on_dashboard(self, web_driver, page):
        """
        To verify reservation details on dashboard.
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_res_details_dash()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("booking_reservation_details")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(65106042)
    def test_41_verify_and_purchage_bartab(self, web_driver, page, guest_data):
        """
        To verify the login functionality.
        :param web_driver:
        :param page:
        :param guest_data:
        :return:
        """
        try:
            page.choosevoyage.verify_and_purchage_bartab(guest_data, "United States")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("purchage_bartab")
            raise Exception(exp)

    @pytest.mark.USA
    @pytestrail.case(984)
    def test_42_verify_logout_from_my_account(self, web_driver, page):
        """
        To verify the login functionality.
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.choosevoyage.verify_logout_page()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("verify_logout")
            raise Exception(exp)
