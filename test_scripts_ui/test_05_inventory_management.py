__author__ = 'Krishna'

import pytest

from ui_pages.ars_admin.login.login import Login
from ui_pages.ars_admin.dashboard.dashboard import ArsDashboard
from ui_pages.ars_admin.inventory_management.add_slot import AddSlots
from ui_pages.ars_admin.inventory_management.stop_sell import StopSell
from ui_pages.ars_admin.inventory_management.move_slot import MoveSlot
from ui_pages.ars_admin.inventory_management.cancel_slot import CancelSlot
from ui_pages.ars_admin.inventory_management.activities import Activities
from ui_pages.ars_admin.inventory_management.parent_activity import ParentActivity
from ui_pages.ars_admin.inventory_management.child_slot import ChildSlot
from ui_pages.ars_admin.inventory_management.activity_filter import ActivityFilter
from ui_pages.ars_admin.inventory_management.new_booking import NewBooking
from ui_pages.ars_admin.apihit.apihit import Apihit
from ui_pages.ars_admin.inventory_management.add_sailor import AddSailor
from ui_pages.ars_admin.inventory_management.paid_by import PaidBy
from virgin_utils import *
from ui_pages.ars_admin.bookings.booking import ArsBookings


@pytest.mark.INVENTORY_MANAGEMENT_UI
@pytest.mark.run(order=5)
class TestInventoryManagement:
    """
    Test ui suite to run Ars Inventory Management
    """

    @pytestrail.case(44671652)
    def test_01_verify_login_page(self, config, page, web_driver, test_data, rest_shore, creds):
        """
        Verify ARS login page
        :param rest_shore:
        :param config:
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', ArsDashboard(web_driver, test_data))
            setattr(page, 'activities', Activities(web_driver, test_data))
            setattr(page, 'activity_filter', ActivityFilter(web_driver, test_data))
            setattr(page, 'add_slot', AddSlots(web_driver, test_data))
            setattr(page, 'move_slot', MoveSlot(web_driver))
            setattr(page, 'stop_sell', StopSell(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data, creds))
            setattr(page, "parent_activity", ParentActivity(web_driver, test_data))
            setattr(page, "child_slot", ChildSlot(web_driver, test_data))
            setattr(page, 'new_booking', NewBooking(web_driver, test_data))
            setattr(page, 'add_sailor', AddSailor(web_driver, test_data))
            setattr(page, 'paid_by', PaidBy(web_driver, test_data))
            setattr(page, 'cancel_slot', CancelSlot(web_driver))
            setattr(page, 'booking', ArsBookings(web_driver))
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/activityReservationCrew/login"))
            page.apihit.get_ship_reservation_details()
            page.apihit.get_voyage_details()
            page.login.verify_vv_logo_is_displayed_on_login_screen()
            if page.login.verify_ars_login_page():
                logger.debug("Login page loaded successfully")
            else:
                web_driver.allure_attach_jpeg('login_page_not_loaded')
                raise Exception("Failed to load Login page successfully")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_login_page")
            raise Exception(exp)

    @pytestrail.case(44671653)
    def test_02_login_to_ars_web_application(self, page, web_driver, creds):
        """
        Login to ars admin module
        :param page:
        :param web_driver:
        """
        try:
            page.login.login_into_ars_admin_web_app(user_name=creds.verticalqa.username, password=creds.verticalqa.password)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_login_page")
            raise Exception(exp)

    @pytestrail.case(44671654)
    def test_03_verify_ars_dashboard(self, page, web_driver):
        """
        To verify user is able to successfully able to open ars dashboard
        :param page:
        :param web_driver:
        """
        try:
            if page.dashboard.verify_ars_dashboard_page() == "Activity Reservation Crew System":
                logger.debug("User successfully Landed on ARS Dashboard")
            else:
                web_driver.allure_attach_jpeg('dashboard_page')
                raise Exception("User Failed to Land on ARS Dashboard")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to verify dashboard")
            raise Exception(exp)

    @pytestrail.case(6036346)
    def test_04_access_activities_in_left_navigation_panel(self, page, web_driver):
        """
        Test case to access activities in left navigation panel
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to access activities in left navigation panel")
            raise Exception(exp)

    @pytestrail.case(6036347)
    def test_05_verify_ui_of_activities_screen(self, page, web_driver, test_data):
        """
        Test case to verify ui of activities screen
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.activities.verify_ars_admin_header_on_top_left_corner()
            page.activities.verify_search_bar_present()
            page.activities.verify_page_header()
            page.activities.verify_active_voyage_name(test_data['voyage_name_space'])
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to verify ui of activities screen")
            raise Exception(exp)

    @pytestrail.case(42629337)
    def test_06_shorex_events_are_displayed_after_login(self, page, web_driver):
        """
        To verify shorex events are displayed by default when crew re logins
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.activities.set_column_name()
            page.activities.shore_events_available_after_login()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed To verify shorex events are displayed by default when crew re logins")
            raise Exception(exp)

    @pytestrail.case(44680366)
    def test_07_filter_for_shore_things(self, page, web_driver):
        """
        To Verify user is able to filter the shore thing activities
        :params: page:
        :params: web_driver:
        """
        try:
            page.activities.click_on_filter()
            page.activity_filter.select_shore_thing()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to filter shore thing activities")
            raise Exception(exp)

    @pytestrail.case(6036352)
    def test_08_verify_user_able_to_add_slots(self, page, web_driver):
        """
        To Verify user is able to add slots to the existing activities or not
        :params: page:
        :params: web_driver:
        """
        try:
            page.activities.select_activity_from_list()
            page.parent_activity.copy_parent_activity_details()
            page.parent_activity.click_on_slots_cta()
            page.parent_activity.click_on_add_slots_cta()
            page.add_slot.select_today_date_from_add_slots_tab()
            page.add_slot.select_slot()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to add slots to existing activity")
            raise Exception(exp)

    @pytestrail.case(32281457)
    def test_09_newly_created_slot_date_and_time(self, page, web_driver):
        """
        To Verify user is able to add slots to the existing activities or not
        :params: page:
        :params: web_driver:
        """
        try:
            page.parent_activity.verify_newly_crated_slot_date()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("newly_created_slot")
            raise Exception(exp)

    @pytestrail.case(38813193)
    def test_10_verify_detail_on_main_page_and_new_slot_details_page(self, page, test_data, web_driver):
        """
        To Verify user is able to add slots to the existing activities or not
        :params: page:
        :params: web_driver:
        :params:test_data:
        """
        try:
            page.parent_activity.open_newly_created_slot()
            page.child_slot.copy_child_activity_details()
            assert test_data['parent']['vendorName'] == test_data['child']['vendorName'], "vendor name not matching"
            assert test_data['parent']['transactionType'] == test_data['child'][
                'transactionType'], "transaction type not " \
                                    "maching "
            assert test_data['parent']['meetingStartTime'] == test_data['child'][
                'meetingStartTime'], "meeting start time is " \
                                     "not matching "
            assert test_data['parent']['meetingLocation'] == test_data['child'][
                'meetingLocation'], "meting location is not " \
                                    "matching "
            assert test_data['parent']['totalAvailableCapacity'] == test_data['child'][
                'totalAvailableCapacity'], "Total " \
                                           "available capacity not matching"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("parent_child_details")
            raise Exception(exp)

    @pytestrail.case(42907527)
    def test_11_move_slot(self, page, web_driver, test_data):
        """
        To move slots to next day
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        current_date = datetime.today().date()
        if current_date == test_data['lastDay']:
            pytest.skip(msg="As Today is debarkation day slot cannot be moved")
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.shore_thing_list()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.click_on_three_dotted_menu_and_move_slot()
                page.move_slot.select_date_and_move_slot()
                assert "Moved Slot Successfully" == page.child_slot.verify_success_message(), "failed to move slot"
                test_data['activeSlot'] = False
            else:
                test_data['activeSlot'] = True
                pytest.skip(msg="no upcoming open slots to move")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to move slots")
            raise Exception(exp)

    @pytestrail.case(6036354)
    def test_12_modify_details_on_main_activity_detail_screen(self, page, web_driver):
        """
        To verify that crew should be able to modify details on main activity detail screen
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.select_activity_from_list()
            page.parent_activity.copy_parent_activity_details()
            page.parent_activity.edit_organiser()
            page.parent_activity.edit_location_and_time()
            page.parent_activity.edit_capacity()
            page.parent_activity.edit_other_info()
            page.parent_activity.verify_activity_details_after_edit()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg(
                "Failed to verify that crew should be able to modify details on main activity detail screen")
            raise Exception(exp)

    @pytestrail.case(41213577)
    def test_13_to_verify_parent_activity_details_by_modifying_details_in_child_slot(self, page, web_driver, test_data):
        """
        To verify activity(parent) details page by modifying details in slot(child) details page
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.select_activity_from_list()
            page.parent_activity.copy_parent_activity_details()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.edit_capacity()
                page.child_slot.verify_activity_details_after_edit()
                page.child_slot.copy_child_activity_details()
                page.child_slot.click_back_button()
                page.parent_activity.verify_parent_activity_info()
            else:
                pytest.skip(msg='No upcoming slots available to edit')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("child_activity_modification")
            raise Exception(exp)

    @pytestrail.case(41505639)
    def test_14_user_should_not_be_allowed_to_edit_booking_closing_time_in_child_slot(self, page, web_driver, test_data):
        """
        User should not be allowed to edit booking closing time in child slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.select_activity_from_list()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.verify_booking_closing_time_not_editable()
            else:
                pytest.skip(msg='No upcoming slots to edit booking close time')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg(
                "Failed to verify User should not be allowed to edit booking closing time in child slot")
            raise Exception(exp)

    @pytestrail.case(42907526)
    def test_15_stop_sell(self, page, web_driver, test_data):
        """
        To verify user is able to stop sell for slot
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.shore_thing_list()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.click_on_three_dotted_menu_and_stop_sell()
                if test_data['isStopSell']:
                    page.stop_sell.click_on_stop_cta()
                    assert "Stop Sell Update Successful" == page.child_slot.verify_success_message(), "Failed to stop sell"
            else:
                pytest.skip(msg="slot shell already stopped")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to stop sell")
            raise Exception(exp)

    @pytestrail.case(25872197)
    def test_16_cancel_slot(self, page, web_driver, test_data):
        """
        To verify user is able to cancel slot
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.shore_thing_list()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.click_on_three_dotted_menu_and_cancel_slot()
                page.cancel_slot.click_on_cancel_cta()
                assert "Slot successfully cancelled" == page.child_slot.verify_success_message(), "Failed to cancel slot"
            else:
                pytest.skip(msg='No upcoming slots available to cancel')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to cancel slots")
            raise Exception(exp)

    @pytestrail.case(32276623)
    def test_17_filter_ent_inventoried_and_non_inventoried_events(self, page, web_driver):
        """
        To verify user is able to filter ent inventoried and ent non inventoried events
        :params: page:
        :params: web_driver:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.filter_for_ent_inventoried_events()
            if page.activities.is_no_records_found():
                logger.info("No inventoried activities available")
            page.activities.click_on_filter()
            page.activity_filter.filter_for_ent_non_inventoried_events()
            if page.activities.is_no_records_found():
                logger.info("No non inventoried activities available")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("entertainment_activities")
            raise Exception(exp)

    @pytestrail.case(44798386)
    def test_18_filter_spa_activity(self, page, web_driver, test_data):
        """
        To verify availabilities of spa activities
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            current_date = datetime.today().date().strftime("%m/%d/%Y")
            if test_data['embarkDate'] != current_date:
                page.activities.click_on_filter()
                page.activity_filter.filter_for_spa_activities()
                test_data['embarkDay'] = False
                if page.activities.is_no_records_found():
                    logger.info("No Spa activities available to book")
            else:
                test_data['embarkDay'] = True
                pytest.skip(msg="no spa activities available on embark/debark day")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("spa_activities")
            raise Exception(exp)

    @pytestrail.case(40881795)
    def test_19_book_spa_activity(self, page, web_driver, test_data):
        """
        To verify booking flow of spa activity
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        if test_data['embarkDay']:
            test_data['isSapSlotAvailable'] = False
            pytest.skip(msg="no spa slots will be available on embark or debark day")
        else:
            test_data['isSapSlotAvailable'] = False
        try:
            current_date = datetime.today().date().strftime("%m/%d/%Y")
            if test_data['debarkDate'] != current_date:
                page.activities.get_spa_activity_from_list()
                page.parent_activity.check_spa_slot_available_for_booking()
                if test_data['isSapSlotAvailable']:
                    page.parent_activity.click_on_new_booking_cta()
                    page.new_booking.get_spa_activity_price()
                    page.new_booking.click_on_add_sailor()
                    page.add_sailor.search_for_sailor_and_click_on_next_cta(
                        stateroom=test_data['searched_sailor_stateroom'])
                    try:
                        page.new_booking.click_on_book_cta()
                        page.paid_by.select_sailor_to_pay_and_click_pay_and_book_cta()
                    except Exception:
                        pytest.skip(msg=f"spa not booked as {test_data['searched_sailor_stateroom']} already have "
                                        f"booking at this time")
                else:
                    test_data['isSpaBooked'] = False
                    pytest.skip(msg="no spa activities available to book")
            else:
                test_data['isSpaBooked'] = False
                pytest.skip(msg="no spa activities available on debarkation day")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("spa_activities")
            raise Exception(exp)

    @pytestrail.case(40885996)
    def test_20_verify_spa_activity_price_on_booking_details_page(self, page, web_driver, test_data):
        """
        To verify price of sap activity after booking
        :params: page:
        :params: web_driver:
        :params: test_data:
        """
        if test_data['embarkDay']:
            pytest.skip(msg="no spa slots will be available on embark or debark day")
        try:
            if test_data['isSpaBooked']:
                page.new_booking.click_on_booking_details()
                booking_price = page.new_booking.get_price_on_booking_details(test_data['spaSlotPrice'])
                assert booking_price, "booking price not matching on slot to booking details page"
            else:
                pytest.skip(msg="spa booking not done")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("slot_price")
            raise Exception(exp)

    @pytestrail.case(40881796)
    def test_21_hard_conflict_for_same_date_and_time_book_spa_activity(self, page, web_driver, test_data):
        """
        User should get Hard Conflict when the Crew tried to book a paid Spa slot in ARS for a Sailor having existing
        Paid Spa booking in ARS for the same date & time
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        if not test_data['isSapSlotAvailable'] and test_data['isSpaBooked']:
            pytest.skip(msg="no spa slots will be available on embark or debark day")
        try:
            current_date = datetime.today().date().strftime("%m/%d/%Y")
            if test_data['debarkDate'] != current_date:
                page.dashboard.click_on_activities_tab_from_dashboard()
                page.activities.get_spa_activity_from_list()
                page.parent_activity.find_spa_slot_booked_previously()
                if test_data['isSameSpaSlotAvailable']:
                    page.parent_activity.click_on_new_booking_cta()
                    page.new_booking.get_spa_activity_price()
                    page.new_booking.click_on_add_sailor()
                    page.add_sailor.search_for_sailor(
                        stateroom=test_data['searched_sailor_stateroom'])
                    page.add_sailor.verify_hard_conflict()
                    page.add_sailor.click_cancel_button()
            else:
                pytest.skip(msg="no spa activities available to book")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("spa_activities")
            raise Exception(exp)

    @pytestrail.case(6036349)
    def test_22_perform_sorting_on_activities_screen(self, page, web_driver):
        """
        To perform sorting on activities screen
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.select_shore_thing()
            if not page.activities.blank_list():
                page.activities.set_column_name()
                page.activities.sort_column_and_verify('Activity ID')
                page.activities.sort_column_and_verify('Activity Name')
                page.activities.sort_column_and_verify('Access')
                page.activities.sort_column_and_verify('Type')
                page.activities.sort_column_with_int_value_and_verify('Starting Price')
            else:
                pytest.skip('Data not available on activities screen')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to verify perform sorting on activities screen")
            raise Exception(exp)

    @pytestrail.case(42629338)
    def test_23_verify_booking_count_in_slot_capacity_edit_tab(self, page, web_driver, test_data):
        """
        Verify booking count in slot capacity edit tab
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.shore_thing_list()
            page.parent_activity.check_for_upcoming_slots()
            if test_data['isSlotAvailable']:
                page.child_slot.verify_booking_count()
            else:
                pytest.skip(msg="no upcoming open slots available")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to Verify booking count in slot capacity edit tab")
            raise Exception(exp)

    @pytestrail.case(41563642)
    def test_24_ent_non_inventoried_event_capacity_should_not_be_editable(self, page, web_driver, test_data):
        """
        Entertainment non inventoried events capacity should not be allowed to edit
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.filter_for_ent_non_inventoried_events()
            if page.activities.is_no_records_found():
                pytest.skip(msg="No non inventoried available")
            else:
                page.activities.ent_non_inventoried_event_list()
                page.parent_activity.check_for_upcoming_slots_in_non_inventoried_activities()
                if test_data['isSlotAvailable']:
                    page.parent_activity.verify_capacity_not_editable()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Entertainment non inventoried events capacity should not be allowed to edit")
            raise Exception(exp)

    @pytestrail.case(56944293)
    def test_25_to_verify_crew_is_able_to_reopen_cancelled_slot(self, page, web_driver, test_data):
        """
        To verify crew is able to reopen/initiate cancelled slot
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.click_on_filter()
            page.activity_filter.apply_filter_for_open_activities()
            page.activities.select_activity_from_list()
            page.parent_activity.check_for_upcoming_cancelled_slot()
            if test_data['isCancelledSlotAvailable']:
                page.child_slot.click_on_three_dotted_menu_and_re_initiate_cancelled_slot()
                assert page.child_slot.verify_success_message() == 'Slot successfully Reinstated', "Failed to re re initiate slot"
            else:
                pytest.skip(msg='No upcoming slots available to edit')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("child_activity_modification")
            raise Exception(exp)

    @pytestrail.case(41063555)
    def test_26_ars_manager_should_not_be_allowed_to_cancel_and_add_slots(self, page, web_driver, creds):
        """
        Ars crew should not be allowed to cancel slots
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.logout_from_ars()
            page.login.login_into_ars_admin_web_app(user_name=creds.inventory.arsmanager.username, password=creds.inventory.arsmanager.password)
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.select_activity_from_list()
            page.parent_activity.click_on_slots_cta()
            page.child_slot.verify_three_dotted_menu_not_present()
            page.child_slot.verify_add_slot_button_not_enabled()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to verify ars crew should not be allowed to cancel slots")
            raise Exception(exp)

    @pytestrail.case(41063556)
    def test_27_ars_crew_should_not_be_allowed_to_cancel_and_add_slots(self, page, web_driver, creds):
        """
        Ars manager should not be allowed to cancel slots
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.logout_from_ars()
            page.login.login_into_ars_admin_web_app(user_name=creds.inventory.arscrew.username, password=creds.inventory.arscrew.password)
            page.dashboard.click_on_activities_tab_from_dashboard()
            page.activities.select_activity_from_list()
            page.parent_activity.click_on_slots_cta()
            page.child_slot.verify_three_dotted_menu_not_present()
            page.child_slot.verify_add_slot_button_not_present()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("Failed to verify ars manager should not be allowed to cancel slots")
            raise Exception(exp)