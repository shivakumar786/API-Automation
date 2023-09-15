__author__ = 'saloni.pattaik'

import pytest

from ui_pages.crew_applications.table_management.admin import TableManagementAdmin
from ui_pages.crew_applications.table_management.report import TableManagementReport
from ui_pages.crew_applications.apihit.apihit import Apihit
from ui_pages.crew_applications.table_management.host import TableManagementHost
from ui_pages.crew_applications.table_management.reservation import TableManagementReservation
from virgin_utils import *
from ui_pages.crew_applications.login.login import CrewAppLogin


@pytest.mark.TABLE_MANAGEMENT
@pytest.mark.run(order=16)
class TestTableManagementApk:
    """
    Test Suite to test Table management APK
    """
    @pytestrail.case(37797589)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, db_core, creds):
        """
        Launch the Crew app and login into table management application
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param test_data:
        :param db_core:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'login', CrewAppLogin(web_driver))
            setattr(page, 'admin', TableManagementAdmin(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'host', TableManagementHost(web_driver))
            setattr(page, 'reservation', TableManagementReservation(web_driver))
            setattr(page, 'report', TableManagementReport(web_driver))
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_sailor_details(flag=True)
            page.apihit.get_crew_details(flag=True)
            page.apihit.get_gender_x_sailor_details(flag=True)
            page.login.allow_call_popup()
            if page.login.verify_select_ship():
                web_driver.allure_attach_jpeg("availability_of_virgin_select_ship_page")
            else:
                raise Exception("Invalid select ship page")
            page.login.sign_in(username='vertical-qas', password='4BWm2tz')
            if page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("error message not coming for wrong credentials")
            page.login.sign_in(username='vertical-qa', password='4BWm2tz4Xz')
            if not page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("login unsuccessful")
                raise Exception("Error in login")
            if not page.login.open_table_management():
                raise Exception("No modules are available")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(37800921)
    def test_02_verify_availability_of_venues(self, web_driver, page, test_data):
        """
        To verify all availability of all venues
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.open_host_module()
            if not page.host.verify_host_module():
                web_driver.allure_attach_jpeg("invalid_host_page_error")
                raise Exception("user not landed on host page")
            test_data['venues'] = page.host.get_venue_list()
            if not page.host.verify_venue_list(venues=test_data['venues']):
                raise Exception("venue list not matching")
            page.host.click_venue_drop_down()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venues_error")
            raise Exception(exp)

    @pytestrail.case(6139372)
    def test_03_verify_venue_background(self, web_driver, page, test_data):
        """
        To verify background of venue is displaying or not
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.click_venue_drop_down()
            page.host.select_venue(test_data)
            if not page.host.verify_background_plan():
                web_driver.allure_attach_jpeg("background_layout_error")
                raise Exception("Background option is not displaying")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venues_background_option_error")
            raise Exception(exp)

    @pytestrail.case(67901514)
    def test_04_verify_gender_x_icon(self, web_driver, page, test_data):
        """
        To verify gender x icon
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data["x_sailor_data"]:
                pytest.skip("no gender x data available")
            else:
                page.host.search_sailor(test_data['x_searched_sailor_name'])
                if not page.host.verify_sailor_gender():
                    web_driver.allure_attach_jpeg("gender_error")
                    raise Exception("gender x not coming for sailor")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("gender_x_error")
            raise Exception(exp)

    @pytestrail.case(43052502)
    def test_05_switch_to_main_sailor(self, web_driver, page, test_data):
        """
        To switch to main sailor
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.search_sailor(test_data['searched_sailor_stateroom_1'])
            page.host.click_reservation()
            page.host.add_another_sailor(test_data['searched_sailor_stateroom_2'])
            page.host.click_on_second_sailor()
            if not page.host.set_main_sailor_verify():
                raise Exception("Error message is displaying while switching main sailor")
            page.host.go_back()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("main_sailor_error")
            raise Exception(exp)

    @pytestrail.case(63441793)
    def test_06_book_dining_for_crew(self, web_driver, page, test_data):
        """
        To book dining for crew member
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.search_crew(test_data['searched_crew_stateroom_1'])
            page.host.click_reservation()
            if not page.host.select_time_slot():
                page.host.select_time_slots()
            if not page.host.click_done():
                web_driver.allure_attach_jpeg("booking_error")
                raise Exception("Booking failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("booking_error")
            raise Exception(exp)

    @pytestrail.case(70057197)
    def test_07_edit_crew_booking(self, web_driver, page, test_data):
        """
        To edit crew booking
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.host.click_edit_icon()
            page.host.add_crew_special_request()
            if not page.host.click_vq_done():
                test_data['venue_slot'] = 0
                web_driver.allure_attach_jpeg("venue_page")
                pytest.skip("venue is closed")
            else:
                if not page.host.verify_crew_edit_vq():
                    raise Exception("crew edit failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew_edit_error")
            raise Exception(exp)

    @pytestrail.case(63441790)
    def test_08_delete_crew_booking(self, web_driver, page, test_data):
        """
        To delete crew booking
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.host.click_delete_crew_icon()
            if not page.host.click_crew_confirm():
                web_driver.allure_attach_jpeg("crew_revoke_page")
                raise Exception("crew revoke failed")
            page.host.verify_crew_revoke_dining()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew_delete_error")
            raise Exception(exp)

    @pytestrail.case(6139366)
    def test_09_book_dining(self, web_driver, page, test_data):
        """
        To book dining
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.search_sailor(test_data['searched_sailor_stateroom_1'])
            page.host.click_reservation()
            if not page.host.select_time_slot():
                page.host.select_time_slots()
            if not page.host.click_done():
                web_driver.allure_attach_jpeg("booking_error")
                raise Exception("Booking failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("booking_error")
            raise Exception(exp)

    @pytestrail.case(64604586)
    def test_10_search_dining_in_reservation(self, web_driver, page, test_data):
        """
        To search dining in reservation tab
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.select_sailor(test_data['searched_sailor_stateroom_1'])
            page.host.click_action_button()
            if page.host.verify_reservation_tab(test_data['searched_sailor_stateroom_1']) == 0:
                web_driver.allure_attach_jpeg("reservation_tab_page")
                raise Exception("Sailor not displaying in reservation tab")
            else:
                page.reservation.click_hamburger_menu()
                page.reservation.open_host_page()
                page.host.select_sailor(test_data['searched_sailor_stateroom_1'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("reservation_error")
            raise Exception(exp)

    @pytestrail.case(37798430)
    def test_11_edit_dining(self, web_driver, page, test_data):
        """
        To edit booked dining
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.click_edit_icon()
            page.host.add_sailor()
            page.host.click_done()
            if not page.host.verify_count():
                web_driver.allure_attach_jpeg("dining_edit_page")
                raise Exception("dining edit failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("edit_booking_error")
            raise Exception(exp)

    @pytestrail.case(60364886)
    def test_12_cancel_dining(self, web_driver, page, test_data):
        """
        To cancel booked dining
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.click_delete_icon()
            if not page.host.click_revoke():
                raise Exception("revoke booking failed")
            page.host.verify_revoke_dining(test_data['searched_sailor_stateroom_1'])
            web_driver.allure_attach_jpeg("revoked_sailor")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cancel_booking_error")
            raise Exception(exp)

    @pytestrail.case(63441784)
    def test_13_enable_wait_list(self, web_driver, page):
        """
        To enable waitlist
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.host.click_wait_list():
                web_driver.allure_attach_jpeg("waitlist_toggle_page")
                raise Exception("waitlist not enabled")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("waitlist_enable_error")
            raise Exception(exp)

    @pytestrail.case(6139367)
    def test_14_book_wait_list(self, web_driver, page, test_data):
        """
        To book wait list
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.host.search_sailor(test_data['searched_sailor_stateroom_1'])
            page.host.click_walkin()
            test_data['wait_slot'] = page.host.select_wait_time_slot(test_data)
            if not test_data['wait_slot']:
                web_driver.allure_attach_jpeg("wait_slot_page")
                pytest.skip("slots not available")
            else:
                if not page.host.click_vq_done():
                    test_data['venue_slot'] = 0
                    pytest.skip("venue is closed")
                else:
                    test_data['venue_slot'] = 1
                    if not page.host.verify_vq(test_data):
                        web_driver.allure_attach_jpeg("vq_page")
                        raise Exception("Wait list booking failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("waitlist_book_error")
            raise Exception(exp)

    @pytestrail.case(37798431)
    def test_15_edit_wait_list(self, web_driver, page, test_data):
        """
        To edit waitlist
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.click_edit_icon()
                page.host.add_special_request()
                if not page.host.click_vq_done():
                    test_data['venue_slot'] = 0
                    web_driver.allure_attach_jpeg("venue_page")
                    pytest.skip("venue is closed")
                else:
                    if not page.host.verify_edit_vq():
                        raise Exception("wait list edit failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("waitlist_edit_error")
            raise Exception(exp)

    @pytestrail.case(63424445)
    def test_16_edit_reservation_wait_list(self, web_driver, page, test_data):
        """
        To edit waitlist by adding special request for reservation
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.click_edit_icon()
                page.host.add_res_special_request()
                if not page.host.click_vq_done():
                    test_data['venue_slot'] = 0
                    web_driver.allure_attach_jpeg("venue_page")
                    pytest.skip("venue is closed")
                else:
                    if not page.host.verify_edit_res_vq():
                        raise Exception("wait list edit failed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("waitlist_edit_error")
            raise Exception(exp)

    @pytestrail.case(37799299)
    def test_17_delete_wait_list(self, web_driver, page, test_data):
        """
        To delete waitlist
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.click_delete_vq_icon()
                if not page.host.click_confirm():
                    web_driver.allure_attach_jpeg("vq_revoke_page")
                    raise Exception("Waitlist revoke failed")
                page.host.verify_revoke_dining(test_data['searched_sailor_stateroom_1'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("waitlist_delete_error")
            raise Exception(exp)

    @pytestrail.case(62660628)
    def test_18_seat_party(self, web_driver, page, test_data):
        """
        To seat party
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.search_sailor(test_data['searched_sailor_stateroom_1'])
                page.host.click_walkin()
                page.host.select_wait_time_slot(test_data)
                if test_data['wait_slot'] == 0:
                    pytest.skip("slots not available")
                else:
                    if not page.host.click_vq_done():
                        pytest.skip("venue is closed")
                page.host.select_table()
                if not page.host.seat_party():
                    web_driver.allure_attach_jpeg("seat_party_page")
                    raise Exception("party not seated")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("seat_party_error")
            raise Exception(exp)

    @pytestrail.case(41557128)
    def test_19_unseat_party(self, web_driver, page, test_data):
        """
        To verify unseat party
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                if not page.host.unseat_party():
                    web_driver.allure_attach_jpeg("unseat_page")
                    raise Exception("unseat party error")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("unseat_error")
            raise Exception(exp)

    @pytestrail.case(63436886)
    def test_20_move_to_another_table(self, web_driver, page, test_data):
        """
        To verify move to another table functionality
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.select_table()
                if not page.host.seat_party():
                    raise Exception("party not seated")
                else:
                    if not page.host.move_to_table(test_data):
                        web_driver.allure_attach_jpeg("table_error")
                        raise Exception("tables not displaying for move")
                    else:
                        if not page.host.move_party(test_data):
                            raise Exception("Party not moved")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("move_party_error")
            raise Exception(exp)

    @pytestrail.case(41557126)
    def test_21_release_party(self, web_driver, page, test_data):
        """
        To verify release party functionality
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.go_to_seat_party_tab(test_data)
                if not page.host.release_party():
                    web_driver.allure_attach_jpeg("release_page")
                    raise Exception("Party not get released")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("release_party_error")
            raise Exception(exp)

    @pytestrail.case(41556807)
    def test_22_clean_table(self, web_driver, page, test_data):
        """
        To verify clean table after release table
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                pytest.skip("slots not available")
            elif test_data['venue_slot'] == 0:
                pytest.skip("venue is closed")
            else:
                page.host.verify_clean_table(test_data)
                if not page.host.click_clean_table(test_data):
                    web_driver.allure_attach_jpeg("action_page")
                    raise Exception("Action dropdown is not visible")
                else:
                    if not page.host.mark_as_clean():
                        raise Exception("Table is not cleaned")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("clean_table_error")
            raise Exception(exp)

    @pytestrail.case(6139374)
    def test_23_verify_admin_module(self, web_driver, page, test_data):
        """
        To verify admin module
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not test_data['wait_slot']:
                page.host.click_back_button()
                page.admin.open_admin_page()
                page.admin.verify_admin_module()
            elif test_data['venue_slot'] == 0:
                page.host.click_back_button()
                page.admin.open_admin_page()
                page.admin.verify_admin_module()
            else:
                page.host.click_table_back_button()
                page.admin.open_admin_page()
                page.admin.verify_admin_module()
                web_driver.allure_attach_jpeg("admin_page")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("admin_module_error")
            raise Exception(exp)

    @pytestrail.case(41556470)
    def test_24_verify_current_tab(self, web_driver, page, test_data):
        """
        To verify current tab in admin module
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_current_tab()
            if not page.admin.verify_current_tab(test_data):
                web_driver.allure_attach_jpeg("current_page")
                raise Exception("current voyage is not displaying in current tab")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("current_tab_error")
            raise Exception(exp)

    @pytestrail.case(41556471)
    def test_25_verify_completed_tab(self, web_driver, page, test_data):
        """
        To verify completed tab in admin module
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_completed_tab()
            page.admin.verify_completed_tab()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("completed_tab_error")
            raise Exception(exp)

    @pytestrail.case(41556474)
    def test_26_verify_preset_applied(self, web_driver, page, test_data):
        """
        To verify preset applied for all voyages
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_upcoming_tab()
            if not page.admin.verify_applied_preset():
                web_driver.allure_attach_jpeg("reset_page")
                raise Exception("preset not been applied for upcoming voyage")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("applied_preset_error")
            raise Exception(exp)

    @pytestrail.case(64605401)
    def test_27_add_table_capacity(self, web_driver, page, test_data):
        """
        To verify table capacity
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_upcoming_voyage()
            page.admin.click_edit()
            page.admin.click_tables()
            if not page.admin.add_tables():
                web_driver.allure_attach_jpeg("capacity_page")
                raise Exception("unable to add table capacity")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("table_capacity_error")
            raise Exception(exp)

    @pytestrail.case(64605404)
    def test_28_add_sailor_booking_slot(self, web_driver, page, test_data):
        """
        To remove slot for sailor booking
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.click_sailor_booking()
            if not page.admin.remove_slots():
                raise Exception("unable to add table capacity")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_slot_error")
            raise Exception(exp)

    @pytestrail.case(64605403)
    def test_29_add_host_booking_slot(self, web_driver, page, test_data):
        """
        To remove slot for host booking
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.click_host_booking()
            if not page.admin.add_slots():
                raise Exception("unable to add table capacity")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("host_slot_error")
            raise Exception(exp)

    @pytestrail.case(64605402)
    def test_30_add_layout(self, web_driver, page, test_data):
        """
        To add layout
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.click_layout()
            page.admin.add_new_layout()
            if not page.admin.verify_layout():
                web_driver.allure_attach_jpeg("layout_page")
                raise Exception("unable to add new layout")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("layout_error")
            raise Exception(exp)

    @pytestrail.case(68315329)
    def test_31_add_table_in_layout(self, web_driver, page, test_data):
        """
        To add table in layout
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not page.admin.add_table():
                raise Exception("unable to add new table in new layout")
            page.admin.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("add_table_error")
            raise Exception(exp)

    @pytestrail.case(65111306)
    def test_32_add_new_preset(self, web_driver, page, test_data):
        """
        To add new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.click_back_button()
            page.admin.open_manage_preset()
            page.admin.new_preset(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("add_preset_error")
            raise Exception(exp)

    @pytestrail.case(65111307)
    def test_33_rename_new_preset(self, web_driver, page, test_data):
        """
        To rename new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.click_three_dot_preset(test_data['preset_name'])
            page.admin.rename_new_preset(test_data)
            if page.admin.verify_rename_preset(test_data['preset_rename']):
                logger.info("preset rename done")
            else:
                raise Exception("preset rename error")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("rename_preset_error")
            raise Exception(exp)

    @pytestrail.case(64605406)
    def test_34_delete_new_preset(self, web_driver, page, test_data):
        """
        To delete new preset
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.delete_new_preset()
            if not page.admin.verify_delete_preset(test_data['preset_rename']):
                web_driver.allure_attach_jpeg("delete preset error")
                raise Exception("Preset not deleted")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_preset_error")
            raise Exception(exp)

    @pytestrail.case(65464602)
    def test_35_link_table(self, web_driver, page, test_data):
        """
        To verify link table
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_current_tab()
            page.admin.click_edit_option()
            page.admin.link_table(test_data)
            page.admin.click_back_button()
            page.admin.click_back_button()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("link_error")
            raise Exception(exp)

    @pytestrail.case(66543747)
    def test_36_manifest_report(self, web_driver, page, test_data):
        """
        To verify manifest report
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.admin.open_report_page()
            if not page.reservation.verify_dining_menifest():
                web_driver.allure_attach_jpeg("manifest_page")
                raise Exception("Menifest report is not coming")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("menifest_error")
            raise Exception(exp)

    @pytestrail.case(68347928)
    def test_37_recap_report(self, web_driver, page, test_data):
        """
        To verify recap report
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not page.reservation.verify_recap():
                web_driver.allure_attach_jpeg("recap_page")
                raise Exception("Recap report is not coming")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("recap_error")
            raise Exception(exp)

    @pytestrail.case(68347929)
    def test_38_special_request_report(self, web_driver, page, test_data):
        """
        To verify special request report
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not page.reservation.verify_special_request():
                web_driver.allure_attach_jpeg("special_request_page")
                raise Exception("special request report is not coming")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("special_request_error")
            raise Exception(exp)

    @pytestrail.case(68347930)
    def test_39_without_reservation_report(self, web_driver, page, test_data):
        """
        To verify sailor without reservation report
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not page.reservation.verify_without_reservation():
                raise Exception("without reservation report is not coming")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("without_reservation_error")
            raise Exception(exp)

    @pytestrail.case(68347931)
    def test_40_turn_time_report(self, web_driver, page, test_data):
        """
        To verify avg turn time per table top report
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            if not page.reservation.verify_avg_turntime_request():
                raise Exception("avg turn time is not coming")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("avg_turn_time_error")
            raise Exception(exp)

    @pytestrail.case(41557127)
    def test_41_verify_reservation_module(self, web_driver, page):
        """
        To verify reservation module
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.reservation.hamburger_menus()
            page.reservation.click_reservation_tab()
            if not page.reservation.verify_voyage_dropdown():
                web_driver.allure_attach_jpeg("reservation_error")
                raise Exception("reservation drop down is not displaying")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("voyage_dropdow_error")
            raise Exception(exp)

    @pytestrail.case(6139373)
    def test_42_verify_cancel_reservation(self, web_driver, page, test_data):
        """
        To verify cancel reservation
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            all_bookings = page.reservation.verify_reservation_list()
            if len(all_bookings) == 0:
                web_driver.allure_attach_jpeg("no_bookings")
                raise Exception("No booking details displaying under reservation tab")
            else:
                if page.reservation.verify_cancel_bookings(all_bookings):
                    web_driver.allure_attach_jpeg("cancel_bookings")
                else:
                    raise Exception("Cancel booking status is not coming")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cancel_reservation_error")
            raise Exception(exp)

    @pytestrail.case(65111308)
    def test_44_verify_voyage_setting_reservation(self, web_driver, page, test_data):
        """
        To verify voyage settings in reservation
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.reservation.verify_voyage_setting()
            if not page.reservation.verify_setting():
                raise Exception("Page not redirect to settings page")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("voyage_setting_error")
            raise Exception(exp)

    @pytestrail.case(41557134)
    def test_45_verify_voyage_autoassignment(self, web_driver, page, test_data):
        """
        To verify auto assignment
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            page.reservation.click_hamburger_menu()
            page.reservation.open_host_page()
            if not page.host.verify_host_module():
                web_driver.allure_attach_jpeg("invalid_host_page_error")
                raise Exception("user not landed on host page")
            page.host.search_sailor(test_data['searched_sailor_stateroom_2'])
            page.host.click_reservation()
            if not page.host.select_time_slot():
                page.host.select_time_slot()
            if not page.host.click_done():
                web_driver.allure_attach_jpeg("booking_error")
                raise Exception("Booking failed")
            page.host.click_side_bar_arrow()
            page.host.click_hamburger_menu()
            page.reservation.click_reservation_tab()
            page.reservation.verify_autoassignment()

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("voyage_setting_error")
            raise Exception(exp)

    @pytestrail.case(43050384)
    def test_46_verify_venue_occupency(self, web_driver, page):
        """
        To verify venue occupency
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.reservation.verify_venue_occupency()
            if not page.reservation.verify_occupency():
                raise Exception("Venue occupency is not displaying for any venue")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("venue_occupency_error")
            raise Exception(exp)

    @pytestrail.case(54370866)
    def test_47_verify_sailor_names(self, web_driver, page):
        """
        To verify sailor name
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.reservation.verify_sailor():
                web_driver.allure_attach_jpeg("handsome_error")
                raise Exception("Sailor name is coming as handsome")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("handsome_error")
            raise Exception(exp)

    @pytestrail.case(43050383)
    def test_48_verify_filter(self, web_driver, page):
        """
        To verify filter
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.reservation.click_filter()
            sailor = page.reservation.verify_filter()
            if sailor == 0:
                web_driver.allure_attach_jpeg("filter_error")
                raise Exception("No sailor is displaying after applying filter")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("filter_error")
            raise Exception(exp)

    @pytestrail.case(43050386)
    def test_49_verify_sources(self, web_driver, page):
        """
        To verify sources
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.reservation.verify_sources():
                raise Exception("Sources are not cming for any reservation")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("source_error")
            raise Exception(exp)

    @pytestrail.case(61409290)
    def test_50_verify_logout_from_table_management(self, web_driver, page):
        """
        To verify logout functionality from table management
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.reservation.hamburger_menu()
            page.login.click_logout()
            if not page.login.verify_logout():
                web_driver.allure_attach_jpeg("logout_page")
                raise Exception("not logged out")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("logout_error")
            raise Exception(exp)