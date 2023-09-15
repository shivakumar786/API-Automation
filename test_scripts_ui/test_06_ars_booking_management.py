__author__ = 'Saloni.pattnaik'

import pytest

from ui_pages.ars_admin.login.login import Login
from ui_pages.ars_admin.dashboard.dashboard import ArsDashboard
from ui_pages.ars_admin.bookings.booking import ArsBookings
from ui_pages.ars_admin.apihit.apihit import Apihit
from virgin_utils import *


@pytest.mark.BOOKING_MANAGEMENT_UI
@pytest.mark.run(order=6)
class TestArsBookingManagement:
    """
    Test ui suite to run Ars Booking Management
    """

    @pytestrail.case(6036356)
    def test_01_verify_crew_access_to_bookings_tab(self, page, web_driver, config, test_data, rest_ship, creds):
        """
        To verify crew should be able to access Bookings after login
        :param rest_ship:
        :param test_data:
        :param config:
        :param page:
        :param web_driver:
        """
        try:
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', ArsDashboard(web_driver, test_data))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'booking', ArsBookings(web_driver))
            web_driver.open_website(
                url=urljoin(config.ship.url.replace('/svc', ''), "/activityReservationCrew/login"))
            page.login.verify_vv_logo_is_displayed_on_login_screen()
            page.login.login_into_ars_admin_web_app(user_name=creds.verticalqa.username,
                                                    password=creds.verticalqa.password)
            page.apihit.get_ship_reservation_details()
            page.dashboard.click_on_bookings_tab_from_dashboard()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Failed to access bookings")
            raise Exception(exp)

    @pytestrail.case(6036358)
    def test_02_verify_bookings_page_ui(self, page, web_driver):
        """
        To verify ui of booking page
        :param page:
        :param web_driver:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            if page.booking.verify_booking_page_header() == "Bookings":
                logger.debug("Crew able to access ARS Bookings")
            else:
                raise Exception("Crew is not on ARS Booking page")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Failed to access bookings")
            raise Exception(exp)

    @pytestrail.case(40881791)
    def test_03_book_activity_for_sailor(self, page, web_driver, test_data):
        """
        To book activity on behalf of sailor
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.booking.click_filter_icon()
            page.booking.select_activity_in_filter('Ent - Non Inventoried')
            if page.booking.is_no_records_found():
                test_data['booking_success'] = False
                pytest.skip("ent non inventory activities are not available")
            page.booking.sort_slots_by_date(activity_type='Ent - Non Inventoried')
            activity_list = page.booking.get_activity_list()
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for booking or no checkin and onboarded sailors")
            for activity_slot in activity_list:
                page.booking.click_on_selected_activity(activity_slot)
                page.booking.wait_for_loader_to_complete()
                page.booking.check_for_any_existing_confirmed_booking(test_data['searched_sailor_stateroom'])
                page.booking.view_slot_details()
                if page.booking.click_new_booking():
                    page.booking.add_sailor_for_booking(test_data['searched_sailor_stateroom'], test_data, "sailor")
                    logger.debug("Booking confirmed")
                    break
                else:
                    page.dashboard.click_on_bookings_tab_from_dashboard()
                    continue
            else:
                pytest.skip("No activity slot is available for booking ")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Booking failed")
            raise Exception(exp)

    @pytestrail.case(2778236)
    def test_04_book_activity_for_crew(self, page, web_driver, test_data):
        """
        To book activity for crew
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            if test_data['booking_success']:
                page.booking.check_for_any_existing_confirmed_booking(test_data['activeCrew'])
                if page.booking.click_new_booking():
                    page.booking.add_crew_for_booking(test_data['activeCrew'], test_data, "crew")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew_booking_failed")
            raise Exception(exp)

    @pytestrail.case(2778232)
    def test_05_verify_booking_status(self, page, web_driver, test_data):
        """
        To verify the status of sailor booking
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if test_data['booking_success']:
                booking_status = page.booking.verify_confirmation_status(test_data['searched_sailor_name'])
                if not booking_status:
                    raise Exception("Booking failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Booking failed")
            raise Exception(exp)

    @pytestrail.case(2964727)
    def test_06_send_notification_against_booking(self, page, web_driver, test_data):
        """
        To send notification to sailor
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            if test_data['booking_success']:
                page.booking.select_booking_checkbox(test_data['searched_sailor_name'])
                if not page.booking.send_notification(test_data['searched_sailor_name']):
                    raise Exception("Notification not raised")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Notification sent failed")
            raise Exception(exp)

    @pytestrail.case(2778234)
    def test_07_change_booking_status_to_checked_in(self, page, web_driver, test_data):
        """
        To change the booked activity status from no show to checked-in
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            if test_data['booking_success']:
                previous_status = page.booking.get_check_in_status(test_data['searched_sailor_name'])
                if not page.booking.change_check_in_status():
                    raise Exception("No success message is displayed")
                new_status = page.booking.get_check_in_status(test_data['searched_sailor_name'])
                assert previous_status != new_status, "Status not updated"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("status not updated")
            raise Exception(exp)

    @pytestrail.case(2917005)
    def test_08_edit_booked_activity(self, page, web_driver, test_data):
        """
        To Verify user is able to edit the conformed booking
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            if test_data['booking_success']:
                page.booking.booking_details_page(test_data['searched_sailor_name'])
                page.booking.edit_confirmed_booking()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Edit_booking")

    @pytestrail.case(65458353)
    def test_09_custom_reason_for_cancellation(self, page, web_driver, test_data):
        """
        To verify custom reason max character acceptance
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            if test_data['booking_success']:
                page.booking.verify_character_limit_in_custom_reason()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("custom_cancellation_reason")
            raise Exception(exp)

    @pytestrail.case(25871025)
    def test_10_cancel_booked_activity(self, page, web_driver, test_data):
        """
        To cancel booked activity
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            if test_data['booking_success']:
                test_data['booking_status'] = page.booking.get_booking_status()
                page.booking.cancel_booking()
                page.booking.accept_cancel_condition()
                if page.booking.verify_cancel_header() == "Cancel Booking":
                    page.booking.click_cancel_button()
                    page.booking.loaded_disappear()
                    assert page.booking.get_booking_status() == "CANCELLED", "Cancel booking failed"
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Booking cancellation failed")
            raise Exception(exp)

    @pytestrail.case(2778233)
    def test_11_verify_booking_status(self, page, web_driver, test_data):
        """
        To verify the booking status
        :param test_data:
        :param web_driver:
        :param page:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and update")
            if test_data['booking_success']:
                test_data['cancel_booking_status'] = page.booking.get_booking_status()
                if test_data['booking_status'] == test_data['cancel_booking_status']:
                    raise Exception("Booking status not getting updated")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Booking status mismatch")
            raise Exception(exp)

    @pytestrail.case(6036359)
    def test_12_apply_filter(self, page, web_driver):
        """
        To verify apply filter in booking page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            page.booking.filter_for_shore_things()
            page.booking.click_3_dotted_filter()
            page.booking.apply_type_filter()
            activity_type = page.booking.get_shore_activity_type()
            if activity_type != "Shore Thing":
                raise Exception(f"failed to filter for shore things actual filter {activity_type}")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter not applied")
            raise Exception(exp)

    @pytestrail.case(41063557)
    def test_13_verify_loader(self, page, web_driver):
        """
        To verify loader at bottom of page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_dashboard_tab_from_dashboard()
            page.dashboard.click_on_bookings_tab_from_dashboard_to_verify_loader()
            if not page.booking.verify_loader():
                logger.debug("Loader not displayed while shifting tab")
            page.booking.loaded_disappear()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Loader failed!")
            raise Exception(exp)

    @pytestrail.case(6036357)
    def test_14_book_excursion(self, page, web_driver, test_data):
        """
        To verify booking of ent non inventory activity
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            page.booking.click_filter_icon()
            page.booking.select_activity_in_filter('Shore Thing')
            if page.booking.is_no_records_found():
                pytest.skip("ent non inventory activities are not available")
            page.booking.sort_slots_by_date(activity_type='Shore Thing')
            activity_list = page.booking.get_activity_list()
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for booking or no checkin and onboarded sailors")
            for activity_slot in activity_list:
                page.booking.click_on_selected_activity(activity_slot)
                page.booking.wait_for_loader_to_complete()
                page.booking.check_for_any_existing_confirmed_booking(test_data['searched_sailor_stateroom'])
                page.booking.view_slot_details()
                if page.booking.click_new_booking():
                    page.booking.add_sailor_for_booking(test_data['searched_sailor_stateroom'], test_data, "sailor")
                    logger.debug("Booking confirmed")
                    break
                else:
                    page.dashboard.click_on_bookings_tab_from_dashboard()
                    continue
            else:
                pytest.skip("No activity slot is available for booking ")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("shorex Booking failed")
            raise Exception(exp)

    @pytestrail.case(45960835)
    def test_15_book_ent_inventory_activity(self, page, web_driver, test_data):
        """
        To verify booking of ent inventory activity
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            page.booking.click_filter_icon()
            page.booking.select_activity_in_filter('Ent - Inventoried')
            if page.booking.is_no_records_found():
                pytest.skip("ent non inventory activities are not available")
            page.booking.sort_slots_by_date(activity_type='Ent - Inventoried')
            activity_list = page.booking.get_activity_list()
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for booking or no checkin and onboarded sailors")
            for activity_slot in activity_list:
                page.booking.click_on_selected_activity(activity_slot)
                page.booking.wait_for_loader_to_complete()
                page.booking.check_for_any_existing_confirmed_booking(test_data['searched_sailor_stateroom'])
                page.booking.view_slot_details()
                if page.booking.click_new_booking():
                    page.booking.add_sailor_for_booking(test_data['searched_sailor_stateroom'], test_data, "sailor")
                    logger.debug("Booking confirmed")
                    break
                else:
                    page.dashboard.click_on_bookings_tab_from_dashboard()
                    continue
            else:
                pytest.skip("No activity slot is available for booking ")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("ent_inventoried_Booking_failed")
            raise Exception(exp)

    @pytest.mark.skip(reason='DCP-119341')
    @pytestrail.case(2778238)
    def test_16_cancel_slot(self, page, web_driver, test_data):
        """
        To cancel the activity slot
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            page.booking.click_filter_icon()
            page.booking.select_activity_in_filter('Ent - Inventoried')
            if page.booking.is_no_records_found():
                pytest.skip("No entertainment activities slot to cancel")
            else:
                page.booking.sort_slots_by_date(activity_type='Ent - Inventoried')
                activity_list = page.booking.get_activity_list()
                page.booking.sort_slots_by_date(activity_type='Ent - Inventoried')
                for activity_slot in activity_list:
                    page.booking.click_on_selected_activity(activity_slot)
                    page.booking.view_slot_details()
                    if not page.booking.is_new_booking_cta_enabled():
                        test_data['NewBookingButton'] = 'Disabled'
                        page.dashboard.click_on_bookings_tab_from_dashboard()
                        continue
                    else:
                        page.booking.click_cancel_slot()
                        break
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Slot not cancelled")
            raise Exception(exp)

    @pytestrail.case(68679927)
    def test_17_book_activity_for_sailor_using_company_account(self, page, web_driver, test_data):
        """
        To book activity on behalf of sailor by company account
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_bookings_tab_from_dashboard()
            page.booking.click_filter_icon()
            page.booking.select_activity_in_filter('Ent - Non Inventoried')
            if page.booking.is_no_records_found():
                pytest.skip("ent non inventory activities are not available")
            page.booking.sort_slots_by_date(activity_type='Ent - Non Inventoried')
            activity_list = page.booking.get_activity_list()
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for booking or no checkin and onboarded sailors")
            for activity_slot in activity_list:
                page.booking.click_on_selected_activity(activity_slot)
                page.booking.wait_for_loader_to_complete()
                page.booking.check_for_any_existing_confirmed_booking(test_data['searched_sailor_stateroom'])
                page.booking.view_slot_details()
                if page.booking.click_new_booking():
                    page.booking.add_sailor_for_booking(test_data['searched_sailor_stateroom'], test_data, "company")
                    logger.debug("Booking confirmed")
                    break
                else:
                    page.dashboard.click_on_bookings_tab_from_dashboard()
                    continue
            else:
                pytest.skip("No activity slot is available for booking ")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("company_account_booking_for_sailor")
            raise Exception(exp)

    @pytestrail.case(68685448)
    def test_18_cancel_sailor_booking_done_by_company_account(self, page, web_driver, test_data):
        """
        To cancel booked activity for sailor with company account
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['sailor_data']:
                pytest.skip("activities are not available for book and cancel")
            elif test_data['booking_success']:
                page.booking.booking_details_page(test_data['searched_sailor_name'])
                test_data['booking_status'] = page.booking.get_booking_status()
                page.booking.cancel_booking()
                page.booking.accept_cancel_condition()
                if page.booking.verify_cancel_header() == "Cancel Booking":
                    page.booking.click_cancel_button()
                    page.booking.loaded_disappear()
                    assert page.booking.get_booking_status() == "CANCELLED", "Cancel booking failed"
                    page.booking.navigate_back()
            else:
                logger.info("sailor booking with company account not done to cancel")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_booking_not_cancelled")
            raise Exception(exp)

    @pytestrail.case(68686399)
    def test_19_book_activity_for_crew_using_company_account(self, page, web_driver, test_data):
        """
        To book activity for crew using company account
        :param test_data:
        :param page:
        :param web_driver:
        :return:
        """
        try:
            if test_data['booking_success']:
                page.booking.click_new_booking()
                page.booking.check_for_any_existing_confirmed_booking(test_data['activeCrew'])
                page.booking.add_crew_for_booking(test_data['activeCrew'], test_data, "company")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew_booking_failed")
            raise Exception(exp)

    @pytestrail.case(68687733)
    def test_20_cancel_crew_booking_done_by_company_account(self, page, web_driver, test_data):
        """
        To cancel booked activity for crew using company account
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if test_data['booking_success']:
                page.booking.booking_details_page(test_data['activeCrew'])
                test_data['booking_status'] = page.booking.get_booking_status()
                page.booking.cancel_booking()
                page.booking.accept_cancel_condition()
                if page.booking.verify_cancel_header() == "Cancel Booking":
                    page.booking.click_cancel_button()
                    page.booking.loaded_disappear()
                    assert page.booking.get_booking_status() == "CANCELLED", "Cancel booking failed"
                    page.booking.navigate_back()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew_booking_cancel")
            raise Exception(exp)
