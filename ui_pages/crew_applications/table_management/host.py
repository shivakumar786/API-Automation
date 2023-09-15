__author__ = 'saloni.pattnaik'

from virgin_utils import *


class TableManagementHost(General):
    """
    Page Class For host To Table Management
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of host page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "host": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Host']",
            "record_audio_popup": ".//android.widget.Button[@text='While using the app']",
            "loader": "//*[@text='loading...']",
            "venue_dropdown": "//*[@resource-id='dropdown-venues-selected']",
            "venues": "//*[@resource-id='dropdown-venues']//*[@class='android.widget.ListView']//*[@class='android.view.View']",
            "tables": "//*[contains(@resource-id,'table-drag-container-table-layout-reservations')]",
            "bookable_venue": "//*[@resource-id='dropdown-venues']//*[@class='android.widget.ListView']//*[@class='android.view.View']//*[@text='%s']",
            "search_button": "//*[@resource-id='reservation-button-header-search-page']",
            "sailor": "//*[@class='android.widget.EditText']",
            "first_sailor": "//*[contains(@resource-id,'search-button-result-item-0')]",
            "reservation": "//*[@content-desc='RESERVATION']",
            "walk_in": "//*[@content-desc='WALK-IN']",
            "time_table": "//*[@text='TIME AND TABLES']",
            "done_button": "//*[@resource-id='reservation-button-submit']",
            "confirm_message": "//*[@text='android.widget.TextView']",
            "venue_list_dropdown": "//*[@resource-id='venues-list-selected']",
            "venue_list": "(//*[@class='android.widget.ListView'])[2]//*[@class='android.view.View']",
            "venue": "((//*[@class='android.widget.ListView'])[2]//*[@class='android.view.View'])[%s]",
            "hamburger_menu_icon": "//*[@resource-id='button-main-menu']",
            "confirm_popup": "//*[@resource-id='new-popup-button-close']",
            "edit_icon": "//*[@resource-id='guest-sidebar-button-redirect']",
            "revoke_btn": "//*[@resource-id='reservation-header-button-show-popup-confirm']",
            "plus_icon": "//*[@resource-id='guest-sidebar-button-chenge-anon-guest-2']",
            "delete_icon": "//*[@resource-id='guest-sidebar-button-delete']",
            "delete": "//*[@text='REVOKE']",
            "confirm": "//*[@text='CONFIRM']",
            "wait_list": "(//*[@class='android.widget.ListView']//*[@class='android.view.View'])[5]",
            "waitlist_toggle": "//*[@text='VQ']",
            "total_bookings": "//*[contains(@resource-id, 'guest-card')]",
            "cabin_no": "((//*[contains(@resource-id, 'guest-card')])[%s]//*[@class='android.widget.TextView'])[4]",
            "party_count": "//*[@class='android.view.View']//*[@text='2']",
            "wait_time_slot": "//*[@text='15 m']",
            "special_req_icon": "(//*[@resource-id='overflow-menu-button-undefined'])",
            "special_res_req_icon": "//*[@resource-id='overflow-menu-button-undefined']",
            "dietary": "(//*[@text='Dietary'])",
            "allergen": "(//*[@text='Allergen'])",
            "wheelchair": "(//*[@text='Wheelchair'])",
            "req_drop_down": "//*[@resource-id='preferences-dropdown-selected']",
            "req": "//*[@resource-id='dropdown-item-preferences-dropdown-0']",
            "main_sailor": "//*[@text='MAIN SAILOR']",
            "main_crew": "//*[@text='CREW']",
            "table_no": "(//*[contains(@resource-id, 'guest-card-button')])[%s]",
            "seat_party": "//*[@text='SEAT PARTY']",
            "release_party": "//*[@text='RELEASE PARTY']",
            "dot_icon": "//*[@text='Actions']",
            "unseat": "(//*[@text='Unseat Party'])[1]",
            "move_to_table": "(//*[@text='Move to another table'])[2]",
            "revoke_msg": "//*[@text='Reservation has been revoked']",
            "delete_msg": "//*[@text='Party has been deleted from waitlist']",
            "special_req": "(//*[@text='Coeliac'])[2]",
            "vq_popup": "//*[@text='No active sessions for this voyage']",
            "vq_close": "//*[@resource-id='button-close']",
            "move_party_btn": "//*[@text='MOVE PARTY']",
            "move_party_message": "//*[@text='Seated party successfully moved']",
            "back_btn": "//*[@resource-id='guest-sidebar-back-button']//*[@class='android.widget.Image']",
            "sailor_seat": "//*[contains(@resource-id, 'guest-card')]",
            "sailor_cabin": "((//*[contains(@resource-id, 'guest-card')])[%s])//*[@class='android.widget.TextView'][4]",
            "release_party_btn": "//*[@text='RELEASE PARTY']",
            "popup_release": "//*[@text='RELEASE']",
            "release_msg": "//*[@text='Party successfully released']",
            "time_slot": "//*[@resource-id='switcher-button-undefined-2']",
            "hamburger_menu": "//*[@resource-id='android:id/content']//*[@class='android.widget.Button']",
            "resevation_icon": "//*[contains(@resource-id,'guest-actions-button')]",
            "sailor_info": "//*[@resource-id='reservations_guest-reservations_guest-info']",
            "back_button_reservation": "//*[@resource-id='reservation-list_header_button-back']",
            "refresh_icon": "//*[@text='icon-resresh']",
            "bookings_reservation": "//*[contains(@resource-id,'reservations-manager__reservations-list-table-row')]",
            "venue_close_popup": "//*[@text='Venue is closed for this time!']",
            "clean_table": "//*[contains(@resource-id,'[%s]')]",
            "clean_icon": "(//*[contains(@resource-id,'table-table-drag-source-table-layout-reservations-[%s]')]//*[@class='android.widget.Image'])[2]",
            "action_dropdown": "//*[@text='ACTIONS']",
            "mark_clean": "//*[@text='MARK AS CLEAN']",
            "need_cleaning": "//*[@text='Need cleaning']",
            "table_back_button": "//*[@resource-id='table-sidebar-back-button']//*[@class='android.widget.Image']",
            "all_tables": "//*[contains(@resource-id,'table-table-drag-source-table-layout-reservations-')]",
            "table": "(//*[contains(@resource-id,'table-table-drag-source-table-layout-reservations-')])[%s]",
            "booked_cabin_numbers": "((//*[contains(@resource-id, 'guest-card')])[%s]//*[@class='android.widget.TextView'])[4]",
            "background": "//*[contains(@text,'floorplan')]",
            "background_dropdown": "//*[@resource-id='host-reservation-table-layout-dropdown-checkboxes-selected']",
            "gender": "//*[contains(@text,'•')]",
            "host_back_button": "//*[@resource-id='guest-sidebar-back-button']//*[@class='android.widget.Image']",
            "add": "//*[@text='ADD SAILOR']",
            "second_sailor": "(//*[contains(@resource-id,'guest-card')])[2]",
            "set_main_sailor": "//*[@text='SET AS MAIN SAILOR']",
            "error": "//*[@text='Something went wrong']",
            "close": "//*[@resource-id='button-close']",
            "crew": "//*[@text='Search For Crew']",
            "floor_plan": "//*[contains(@text,'floorplan')]",
            "ok": "//*[@text='OK']",
            "sp_req": "(//*[@text='Coeliac'])[4]",
            "res_sp_req": "(//*[@text='Wheelchair'])[4]",
            "delete_req": "//*[@resource-id='preferences-dropdown']/..//*[@class='android.widget.Button']",
            "reservation_back": "//android.view.View[@content-desc='reservations']/android.widget.Image"
        })

    def add_special_request(self):
        """
        To add special requests
        :return:
        """
        self.webDriver.wait_for(2)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_req_icon, locator_type='xpath'):
            raise Exception("Special request option is not available")
        else:
            self.webDriver.click(element=self.locators.special_req_icon, locator_type='xpath')
            self.webDriver.click(element=self.locators.dietary, locator_type='xpath')
            self.webDriver.click(element=self.locators.req_drop_down, locator_type='xpath')
            self.webDriver.click(element=self.locators.req, locator_type='xpath')
            self.webDriver.click(element=self.locators.main_sailor, locator_type='xpath')
            if not self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
                self.webDriver.click(element=self.locators.sp_req, locator_type='xpath')
                self.webDriver.click(element=self.locators.delete_req, locator_type='xpath')
                self.webDriver.click(element=self.locators.special_req_icon, locator_type='xpath')
                self.webDriver.click(element=self.locators.dietary, locator_type='xpath')
                self.webDriver.click(element=self.locators.req_drop_down, locator_type='xpath')
                self.webDriver.click(element=self.locators.req, locator_type='xpath')
                self.webDriver.click(element=self.locators.main_sailor, locator_type='xpath')
            else:
                return True

    def click_crew_confirm(self):
        """
        To click revoke confirm
        :return:
        """
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.revoke_msg, locator_type='xpath', time_out=180)
        if self.webDriver.is_element_display_on_screen(element=self.locators.revoke_msg, locator_type='xpath'):
            return True
        else:
            return False

    def click_delete_crew_icon(self):
        """
        To click on delete vq icon
        :return:
        """
        self.webDriver.click(element=self.locators.delete_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete, locator_type='xpath', time_out=180)

    def verify_crew_edit_vq(self):
        """
        To verify edit bookings
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.special_req, locator_type='xpath', time_out=180)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_req, locator_type='xpath'):
            return False
        else:
            return True

    def verify_crew_revoke_dining(self):
        """
        To verify dining booking after revoke dining
        :return:
        """
        booked_crew = self.webDriver.get_elements(element=self.locators.sailor_seat, locator_type='xpath')
        if len(booked_crew) != 0:
            for sailor in range(1, len(booked_crew)):
                if self.webDriver.get_text(element=self.locators.booked_cabin_numbers % sailor, locator_type='xpath') == "Test":
                    raise Exception("crew hasn't revoked")
                else:
                    continue
        else:
            self.webDriver.allure_attach_jpeg("Booking_revoked")

    def add_crew_special_request(self):
        """
        To add special requests
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.special_req_icon, locator_type='xpath', time_out=180)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_req_icon, locator_type='xpath'):
            raise Exception("Special request option is not available")
        else:
            self.webDriver.click(element=self.locators.special_req_icon, locator_type='xpath')
            self.webDriver.click(element=self.locators.dietary, locator_type='xpath')
            self.webDriver.click(element=self.locators.req_drop_down, locator_type='xpath')
            self.webDriver.click(element=self.locators.req, locator_type='xpath')
            self.webDriver.click(element=self.locators.main_crew, locator_type='xpath')

    def search_crew(self, cabin):
        """
        To search crew for booking
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_button, locator_type='xpath'):
            self.webDriver.click(element=self.locators.reservation_back, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.search_button, locator_type='xpath',
                                                          time_out=120)
            self.webDriver.click(element=self.locators.search_button, locator_type='xpath')
            self.webDriver.click(element=self.locators.crew, locator_type='xpath')
            self.webDriver.set_text(element=self.locators.sailor, locator_type='xpath', text=cabin)
            self.webDriver.explicit_visibility_of_element(element=self.locators.first_sailor, locator_type='xpath',
                                                          time_out=180)
            self.webDriver.click(element=self.locators.first_sailor, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.reservation, locator_type='xpath',
                                                          time_out=180)
        else:
            self.webDriver.explicit_visibility_of_element(element=self.locators.search_button, locator_type='xpath', time_out=120)
            self.webDriver.click(element=self.locators.search_button, locator_type='xpath')
            self.webDriver.click(element=self.locators.crew, locator_type='xpath')
            self.webDriver.set_text(element=self.locators.sailor, locator_type='xpath', text=cabin)
            self.webDriver.explicit_visibility_of_element(element=self.locators.first_sailor, locator_type='xpath', time_out=180)
            self.webDriver.click(element=self.locators.first_sailor, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.reservation, locator_type='xpath', time_out=180)

    def go_back(self):
        """
        To go back to dashboard of host page
        :return:
        """
        self.webDriver.click(element=self.locators.close, locator_type='xpath')

    def set_main_sailor_verify(self):
        """
        To verify main sailor
        :return:
        """
        self.webDriver.click(element=self.locators.second_sailor, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.set_main_sailor, locator_type='xpath',
                                                      time_out=200)
        self.webDriver.click(element=self.locators.set_main_sailor, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.error, locator_type='xpath'):
            return False
        else:
            return True

    def click_on_second_sailor(self):
        """
        To select second sailor
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.second_sailor, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.second_sailor, locator_type='xpath')

    def add_another_sailor(self, cabin):
        """
        To add another sailor
        :param cabin:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.add, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.add, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.sailor, locator_type='xpath', text=cabin)
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_sailor, locator_type='xpath',
                                                      time_out=200)
        self.webDriver.click(element=self.locators.first_sailor, locator_type='xpath')

    def click_side_bar_arrow(self):
        """
        To click side arrow
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.host_back_button, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.host_back_button, locator_type='xpath')

    def verify_sailor_gender(self):
        """
        To verify gender of a sailor
        :return:
        """
        sailor_gender = self.webDriver.get_text(element=self.locators.gender, locator_type='xpath')
        gender = sailor_gender.split('•')[0]
        if "(X)" in gender:
            self.webDriver.click(element=self.locators.host_back_button, locator_type='xpath')
            return True
        else:
            self.webDriver.click(element=self.locators.host_back_button, locator_type='xpath')
            return False

    def verify_background_plan(self):
        """
        To verify venue background
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.background_dropdown, locator_type='xpath', time_out=30)
        if self.webDriver.is_element_display_on_screen(element=self.locators.background, locator_type='xpath'):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.floor_plan, locator_type='xpath'):
                raise Exception("Floor plan for venue is not displaying")
            else:
                return True
        else:
            return False

    def verify_revoke_dining(self, cabin_number):
        """
        To verify dining booking after revoke dining
        :param cabin_number:
        :return:
        """
        booked_sailors = self.webDriver.get_elements(element=self.locators.sailor_seat, locator_type='xpath')
        if len(booked_sailors) != 0:
            for sailor in range(1, len(booked_sailors)):
                if self.webDriver.get_text(element=self.locators.booked_cabin_numbers % sailor, locator_type='xpath') == cabin_number:
                    raise Exception("sailor hasn't revoked")
                else:
                    continue
        else:
            self.webDriver.allure_attach_jpeg("Booking_revoked")

    def click_table_back_button(self):
        """
        To click back button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.table_back_button, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.table_back_button, locator_type='xpath')

    def mark_as_clean(self):
        """
        Mark table clean
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.need_cleaning, locator_type='xpath'):
            self.webDriver.click(element=self.locators.action_dropdown, locator_type='xpath')
            self.webDriver.click(element=self.locators.mark_clean, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.need_cleaning, locator_type='xpath'):
            return False
        else:
            return True

    def verify_clean_table(self, test_data):
        """
        To verify drop icon on clean table
        :param test_data:
        :return:
        """
        tables = self.webDriver.get_elements(element=self.locators.all_tables, locator_type='xpath')
        for table_no in range(1, len(tables)):
            self.webDriver.click(element=self.locators.table % table_no, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.need_cleaning, locator_type='xpath'):
                return True
            else:
                continue

    def click_clean_table(self, test_data):
        """
        To click on clean table
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.action_dropdown, locator_type='xpath', time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.action_dropdown, locator_type='xpath'):
            return True
        else:
            return False

    def verify_reservation_tab(self, cabin_number):
        """
        To search sailor booking in reservation tab
        :param cabin_number:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sailor_info, locator_type='xpath', time_out=30)
        info = self.webDriver.get_web_element(element=self.locators.sailor_info, locator_type='xpath')
        reservations = self.webDriver.get_elements(element=self.locators.bookings_reservation, locator_type='xpath')
        if len(reservations) == 0:
            self.webDriver.click(element=self.locators.refresh_icon, locator_type='xpath')
            self.webDriver.wait_for(10)
            info = self.webDriver.get_web_element(element=self.locators.sailor_info, locator_type='xpath')
            reservations = self.webDriver.get_elements(element=self.locators.bookings_reservation, locator_type='xpath')
        information = (info.text).split('•')
        if cabin_number not in information:
            return False
        else:
            self.webDriver.explicit_visibility_of_element(element=self.locators.back_button_reservation, locator_type='xpath', time_out=120)
            self.webDriver.click(element=self.locators.back_button_reservation, locator_type='xpath')
            return len(reservations)

    def click_action_button(self):
        """
        To go to reservation tab
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.resevation_icon, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.resevation_icon, locator_type='xpath')

    def click_back_button(self):
        """
        To click back button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.back_btn, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type='xpath', time_out=120)

    def release_party(self):
        """
        To release party
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.release_party_btn, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.release_party_btn, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.popup_release, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.popup_release, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.release_msg, locator_type='xpath',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.release_msg, locator_type='xpath'):
            self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
            return True
        else:
            return False

    def go_to_seat_party_tab(self, test_data):
        """
        To go back to seat party tab
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.back_btn, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
        seats = self.webDriver.get_elements(element=self.locators.sailor_seat, locator_type='xpath')
        for seat in range(1, len(seats)+1):
            cabin_no = self.webDriver.get_web_element(element=self.locators.sailor_cabin % seat, locator_type='xpath')
            if cabin_no.text == test_data['searched_sailor_stateroom_1']:
                cabin_no.click()

    def move_party(self, test_data):
        """
        To move party to another table
        :param test_data:
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.move_party_btn, locator_type='xpath'):
            test_data['table_no'] = self.webDriver.get_text(element=self.locators.table_no % 2, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.table_no % 2, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.ok, locator_type='xpath'):
                self.webDriver.click(element=self.locators.ok, locator_type='xpath')
                self.webDriver.click(element=self.locators.move_party_btn, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.move_party_message,
                                                              locator_type='xpath', time_out=30)
                if self.webDriver.is_element_display_on_screen(element=self.locators.move_party_message,
                                                               locator_type='xpath'):
                    return True
            else:
                self.webDriver.click(element=self.locators.move_party_btn, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.move_party_message, locator_type='xpath', time_out=30)
                if self.webDriver.is_element_display_on_screen(element=self.locators.move_party_message, locator_type='xpath'):
                    return True
                else:
                    return False
        else:
            raise Exception("Move party button not displaying")

    def click_vq_done(self):
        """
        To click on save
        :return:
        """
        self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.venue_close_popup, locator_type='xpath'):
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.vq_close, locator_type='xpath')
            return False
        else:
            self.webDriver.wait_for(5)
            return True

    def verify_vq(self, test_data):
        """
        To verify vq booking done or not
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.walk_in, locator_type='xpath', time_out= 120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.walk_in, locator_type='xpath'):
            return True
        else:
            self.select_sailor(test_data['searched_sailor_stateroom'])
            self.webDriver.explicit_visibility_of_element(element=self.locators.walk_in, locator_type='xpath', time_out= 120)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.walk_in, locator_type='xpath'):
                return False
            else:
                return True

    def unseat_party(self):
        """
        To unseat party
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.dot_icon, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.dot_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.unseat, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.table_no % 1, locator_type='xpath', time_out=180)
        if self.webDriver.is_element_display_on_screen(element=self.locators.table_no % 1, locator_type='xpath'):
            return True
        else:
            return False

    def move_to_table(self, test_data):
        """
        To move party to another table
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.dot_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.move_to_table, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.table_no % 2, locator_type='xpath', time_out=180)
        if self.webDriver.is_element_display_on_screen(element=self.locators.table_no % 2, locator_type='xpath'):
            test_data['seat_table_number'] = self.webDriver.get_text(element=self.locators.table_no % 2, locator_type='xpath')
            return True
        else:
            return False

    def seat_party(self):
        """
        To seat party
        :return:
        """
        self.webDriver.wait_for(10)
        if self.webDriver.is_element_enabled(element=self.locators.seat_party, locator_type='xpath'):
            self.webDriver.wait_for(5)
            self.webDriver.click(element=self.locators.seat_party, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.ok, locator_type='xpath'):
                self.webDriver.click(element=self.locators.ok, locator_type='xpath')
            else:
                self.webDriver.explicit_visibility_of_element(element=self.locators.release_party, locator_type='xpath', time_out=120)
                if self.webDriver.is_element_enabled(element=self.locators.release_party, locator_type='xpath'):
                    return True
                else:
                    return False

    def select_table(self):
        """
        To select table
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.table_no % 1, locator_type='xpath', time_out=180)
        self.webDriver.scroll_mobile(476, 1228, 488, 1050)
        self.webDriver.click(element=self.locators.table_no % 1, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.ok, locator_type='xpath'):
            self.webDriver.click(element=self.locators.ok, locator_type='xpath')

    def add_res_special_request(self):
        """
        To add reservation special request
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_res_req_icon, locator_type='xpath'):
            raise Exception("Special request option is not available")
        else:
            self.webDriver.click(element=self.locators.special_res_req_icon, locator_type='xpath')
            self.webDriver.click(element=self.locators.allergen, locator_type='xpath')
            self.webDriver.click(element=self.locators.req_drop_down, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.req, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.main_sailor, locator_type='xpath')
            self.webDriver.click(element=self.locators.special_req_icon, locator_type='xpath')
            self.webDriver.click(element=self.locators.wheelchair, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.main_sailor, locator_type='xpath')
            if not self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
                self.webDriver.click(element=self.locators.res_sp_req, locator_type='xpath')
                self.webDriver.click(element=self.locators.delete_req, locator_type='xpath')
                self.webDriver.click(element=self.locators.special_req_icon, locator_type='xpath')
                self.webDriver.click(element=self.locators.wheelchair, locator_type='xpath')
                self.webDriver.wait_for(2)
                self.webDriver.click(element=self.locators.main_sailor, locator_type='xpath')
            else:
                return True

    def verify_count(self):
        """
        To verify count increased or not
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.party_count, locator_type='xpath', time_out=200)
        party_member = self.webDriver.get_text(element=self.locators.party_count, locator_type='xpath')
        if party_member == "2":
            return True
        else:
            return False

    def select_sailor(self, cabin_no):
        """
        To select sailor from booking list
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.reservation, locator_type='xpath'):
            self.webDriver.explicit_visibility_of_element(element=self.locators.total_bookings, locator_type='xpath', time_out=200)
            bookings = self.webDriver.get_elements(element=self.locators.total_bookings, locator_type='xpath')
            for booking in range(0, len(bookings)):
                cabin = self.webDriver.get_text(element=self.locators.cabin_no % (booking+1), locator_type='xpath')
                if cabin == cabin_no:
                    self.webDriver.click(element=self.locators.cabin_no % (booking+1), locator_type='xpath')
                    break
                else:
                    continue
        else:
            pass

    def click_wait_list(self):
        """
        To click on waitlist tab
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.wait_list, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.wait_list, locator_type='xpath')
        if not self.webDriver.is_element_enabled(element=self.locators.waitlist_toggle, locator_type='xpath'):
            self.webDriver.click(element=self.locators.waitlist_toggle, locator_type='xpath')
            if self.webDriver.is_element_enabled(element=self.locators.waitlist_toggle, locator_type='xpath'):
                return True
            else:
                return False
        else:
            self.webDriver.click(element=self.locators.waitlist_toggle, locator_type='xpath')
            if self.webDriver.is_element_enabled(element=self.locators.waitlist_toggle, locator_type='xpath'):
                return True
            else:
                return False

    def click_confirm(self):
        """
        To click revoke confirm
        :return:
        """
        self.webDriver.click(element=self.locators.confirm, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete_msg, locator_type='xpath',time_out=180)
        if self.webDriver.is_element_display_on_screen(element=self.locators.delete_msg, locator_type='xpath'):
            return True
        else:
            return False

    def click_revoke(self):
        """
        To click revoke
        :return:
        """
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.revoke_msg, locator_type='xpath',time_out=180)
        if self.webDriver.is_element_display_on_screen(element=self.locators.revoke_msg, locator_type='xpath'):
            return True
        else:
            return False

    def click_delete_icon(self):
        """
        To click on delete icon
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete_icon, locator_type='xpath', time_out=180)
        self.webDriver.click(element=self.locators.delete_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete, locator_type='xpath', time_out=180)

    def click_delete_vq_icon(self):
        """
        To click on delete vq icon
        :return:
        """
        self.webDriver.click(element=self.locators.delete_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.confirm, locator_type='xpath', time_out=200)

    def edit_time_slot(self):
        """
        To edit time slot
        :return:
        """
        self.webDriver.click(element=self.locators.time_table, locator_type='xpath')
        self.webDriver.wait_for(20)

    def add_sailor(self):
        """
        To add sailor into existing booking
        :return:
        """
        self.webDriver.click(element=self.locators.plus_icon, locator_type='xpath')

    def click_edit_icon(self):
        """
        To click on edit icon
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.edit_icon, locator_type='xpath', time_out=180)
        self.webDriver.click(element=self.locators.edit_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.revoke_btn, locator_type='xpath', time_out=180)

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu_icon, locator_type='xpath')

    def select_reservation_venue(self):
        """
        To select venue from dropdown
        :return:
        """
        venues = self.webDriver.get_elements(element=self.locators.venue_list, locator_type='xpath')
        for venuee in range(1, len(venues)):
            self.webDriver.click(element=self.locators.venue % venuee, locator_type='xpath')
            self.webDriver.wait_for(10)
            if self.webDriver.is_element_display_on_screen(element=self.locators.time_slot, locator_type='xpath'):
                self.webDriver.click(element=self.locators.time_slot, locator_type='xpath')
                break
            else:
                continue

    def select_wait_time_slot(self, test_data):
        """
        To select wait time slot
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.time_table, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.vq_popup, locator_type='xpath'):
            self.webDriver.explicit_visibility_of_element(element=self.locators.wait_time_slot, locator_type='xpath',
                                                          time_out=180)
            self.webDriver.click(element=self.locators.wait_time_slot, locator_type='xpath')
            return True
        else:
            self.webDriver.click(element=self.locators.vq_close, locator_type='xpath')
            return False

    def select_time_slot(self):
        """
        To select timeslot from slot tables
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_table, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.time_table, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_slot, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.time_slot, locator_type='xpath')
        if self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
            return True
        else:
            self.webDriver.click(element=self.locators.venue_list_dropdown, locator_type='xpath')
            self.select_reservation_venue()
            return False

    def select_time_slots(self):
        """
        To select timeslot from slots tables
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_slot, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.time_slot, locator_type='xpath')
        if self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
            return True
        else:
            self.webDriver.click(element=self.locators.venue_list_dropdown, locator_type='xpath')
            self.select_reservation_venue()
            return False

    def select_time_slots(self):
        """
        To select timeslots from slot tables
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_slot, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.time_slot, locator_type='xpath')
        if self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
            return True
        else:
            self.webDriver.click(element=self.locators.venue_list_dropdown, locator_type='xpath')
            self.select_reservation_venue()
            return False

    def click_done(self):
        """
        To click done button
        :return:
        """
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_enabled(element=self.locators.done_button, locator_type='xpath'):
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.confirm_popup, locator_type='xpath'):
                self.webDriver.click(element=self.locators.confirm_popup, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.total_bookings, locator_type='xpath', time_out=200)
                if not self.webDriver.is_element_display_on_screen(element=self.locators.total_bookings, locator_type='xpath'):
                    return False
                else:
                    return True
            else:
                self.webDriver.explicit_visibility_of_element(element=self.locators.total_bookings, locator_type='xpath', time_out=200)
                if not self.webDriver.is_element_display_on_screen(element=self.locators.total_bookings, locator_type='xpath'):
                    return False
                else:
                    return True
        else:
            raise Exception("done button not getting enabled")

    def verify_edit_vq(self):
        """
        To verify edit bookings
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.walk_in, locator_type='xpath', time_out=180)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_req, locator_type='xpath'):
            return False
        else:
            return True

    def verify_edit_res_vq(self):
        """
        To verify edit bookings
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.explicit_visibility_of_element(element=self.locators.walk_in, locator_type='xpath', time_out=180)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.special_req, locator_type='xpath'):
            return False
        else:
            return True

    def click_reservation(self):
        """
        To click reservation button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.reservation, locator_type='xpath',time_out=30)
        self.webDriver.click(element=self.locators.reservation, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_table, locator_type='xpath', time_out=180)

    def click_walkin(self):
        """
        To click walk in button
        :return:
        """
        self.webDriver.click(element=self.locators.walk_in, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.time_table, locator_type='xpath', time_out=180)

    def search_sailor(self, cabin):
        """
        To search sailor for booking
        :param cabin:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_button, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.search_button, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.sailor, locator_type='xpath', text=cabin)
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_sailor, locator_type='xpath', time_out=180)
        self.webDriver.click(element=self.locators.first_sailor, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.reservation, locator_type='xpath', time_out=180)

    def select_venue(self, venue):
        """
        To select any venue from venue drop down
        :param venue:
        :return:
        """
        venues = ["Extra Virgin", "Gunbae", "Pink Agave", "Razzle Dazzle Restaurant", "The Test Kitchen", "The Wake"]
        for i in range(len(venue)):
            venues_list = self.webDriver.get_elements(element=self.locators.venues, locator_type='xpath')
            for venue in venues_list:
                if venue.text in venues:
                    self.webDriver.click(element=self.locators.bookable_venue % venue.text, locator_type='xpath')
                    self.webDriver.explicit_visibility_of_element(element=self.locators.tables, locator_type='xpath', time_out=120)
                    if len(self.webDriver.get_elements(element=self.locators.tables, locator_type='xpath')) > 10:
                        break
                    else:
                        self.click_venue_drop_down()
                        self.webDriver.scroll_mobile(574, 253, 579, 722)
                        continue
            break

    def click_venue_drop_down(self):
        """
        To click venue drop down
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.venue_dropdown, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.venue_dropdown, locator_type='xpath')
        self.webDriver.wait_for(2)

    def verify_venue_list(self, venues):
        """
        To verify venue list
        :return:
        """
        venue = ["Extra Virgin", "Gunbae", "Pink Agave", "Razzle Dazzle Restaurant", "The Test Kitchen", "The Wake"]
        for restaurant in venue:
            if restaurant in venues:
                return True
            else:
                return False

    def get_venue_list(self):
        """
        To get all venue lists
        :return:
        """
        venues = []
        self.webDriver.click(element=self.locators.venue_dropdown, locator_type='xpath')
        for i in range(14):
            venues_list = self.webDriver.get_elements(element=self.locators.venues, locator_type='xpath')
            self.webDriver.scroll_mobile(579, 722, 568, 210)
            for venue in venues_list:
                venues.append(venue.text)
        return venues

    def verify_host_module(self):
        """
        To verify user land on host module
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.venue_dropdown, locator_type='xpath'):
            return True
        else:
            return False

    def open_host_module(self):
        """
        To open table management host module
        :return:
        """
        self.webDriver.click(element=self.locators.host, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.record_audio_popup, locator_type='xpath', time_out=120)
        self.webDriver.get_web_element(element=self.locators.record_audio_popup, locator_type='xpath').click()
        self.webDriver.explicit_visibility_of_element(element=self.locators.venue_dropdown, locator_type='xpath',time_out=180)