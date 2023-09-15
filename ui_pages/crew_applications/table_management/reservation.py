__author__ = 'saloni.pattnaik'

from virgin_utils import *


class TableManagementReservation(General):
    """
    Page Class For reservation To Table Management
    """
    def __init__(self, web_driver):
        """
        To Initialize the locators of reservation page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "reservation": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Reservations']",
            "hamburger_menu": "//*[@resource-id='reservation-list_header_button-hamburger']",
            "click_tm": "//*[@resource-id='android:id/content']//*["
                        "@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']",
            "host": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Host']",
            "venue_dropdown": "//*[@resource-id='dropdown-venues-selected']",
            "reports": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Reports']",
            "manifest_report": "//*[@text='DINING MANIFEST']",
            "recap_report": "//*[@text='RESERVATION RECAP']",
            "special_request": "//*[@text='SPECIAL REQUEST']",
            "without_reservation_request": "//*[@text='SAILORS WITHOUT RESERVATION']",
            "avg_turntime_request": "//*[@text='AVERAGE TURN TIME PER TABLE TOP SIZE']",
            "filter_popup": "//*[@text='Filter popup']",
            "apply": "//*[@text='APPLY']",
            "cabin_number": "//*[@text='Next']",
            "back_button": "//*[@class='android.widget.Button']",
            "special_request_col": "//*[@text='SPECIAL REQUEST']",
            "hamburger_icon": "(//*[@class='android.widget.Button'])[1]",
            "voyage_dropdown": "//*[@resource-id='main-filters_sailings-selected']",
            "all_voyages": "//*[contains(@resource-id,'dropdown-item-main-filters_sailings')]",
            "booking_list": "//*[contains(@resource-id,'reservations-manager__reservations-list-table-row')]",
            "status": "(//*[contains(@resource-id,'reservations-manager__reservations-list-table-row')])[%s]//*[contains(@resource-id,'reservations-table_cell_status')]",
            "action": "//*[@text='ACTIONS']",
            "setting": "//*[@text='Voyage settings']",
            "setting_page": "//*[@text='SETTINGS']",
            "admin_back_button": "//*[@resource-id='admin__sidebar__back']",
            "reservation_tab": "//*[@text='Reservations']",
            "autoassign": "//*[@text='Run autoassign']",
            "occupency": "//*[@text='Venue occupancy']",
            "close": "//*[@text='CLOSE']",
            "all_sailor": "//*[contains(@resource-id,'reservations-table_cell_reserved')]",
            "filter": "//*[@resource-id='reservation-list_header_button-admin-filter']",
            "apply_filter": "//*[@text='APPLY FILTERS']",
            "source": "//*[@resource-id='reservations-table_col-header_sources']",
            "hamburger_menus": "//*[@class='android.widget.Button']",
        })

    def hamburger_menus(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menus, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.hamburger_menus, locator_type='xpath')


    def verify_sources(self):
        """
        To verify sources
        :return:
        """
        self.webDriver.scroll_mobile(2401, 276, 1715, 282)
        self.webDriver.explicit_visibility_of_element(element=self.locators.source, locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.source, locator_type='xpath'):
            return True
        else:
            return False

    def verify_filter(self):
        """
        To verify filter
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.apply_filter, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.all_sailor, locator_type='xpath', time_out=120)
        all_sailor = self.webDriver.get_elements(element=self.locators.all_sailor, locator_type='xpath')
        return len(all_sailor)

    def click_filter(self):
        """
        To click on filter
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')

    def verify_sailor(self):
        """
        To verify sailor name
        :return:
        """
        all_sailor = self.webDriver.get_elements(element=self.locators.all_sailor, locator_type='xpath')
        for sailor in all_sailor:
            if sailor.text == "HANDSOME":
                return False
            else:
                return True

    def verify_occupency(self):
        """
        To verify occupency
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.close, locator_type='xpath'):
            self.webDriver.click(element=self.locators.close, locator_type='xpath')
            return True
        else:
            return False

    def verify_venue_occupency(self):
        """
        To verify venue occupency
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.action, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.action, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.occupency, locator_type='xpath'):
            self.webDriver.click(element=self.locators.occupency, locator_type='xpath')

    def verify_autoassignment(self):
        """
        To verify auto assignment
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.action, locator_type='xpath', time_out=200)
        self.webDriver.click(element=self.locators.action, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.autoassign, locator_type='xpath'):
            self.webDriver.click(element=self.locators.autoassign, locator_type='xpath')

    def click_reservation_tab(self):
        """
        To click reservation tab
        :return:
        """
        self.webDriver.scroll_mobile(540, 1492, 500, 390)
        self.webDriver.explicit_visibility_of_element(element=self.locators.click_tm, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.reservation, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.reservation, locator_type='xpath')

    def verify_setting(self):
        """
        To verify page of settings
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.setting_page, locator_type='xpath', time_out=120)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.setting_page, locator_type='xpath'):
            self.webDriver.click(element=self.locators.admin_back_button, locator_type='xpath')
            return False
        else:
            self.webDriver.click(element=self.locators.admin_back_button, locator_type='xpath')
            return True

    def verify_voyage_setting(self):
        """
        To verify voyage settings
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.action, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.action, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.setting, locator_type='xpath'):
            self.webDriver.click(element=self.locators.setting, locator_type='xpath')

    def verify_cancel_bookings(self, all_bookings):
        """
        To verify cancel booking
        :return:
        """
        for booking in range(1, len(all_bookings)):
            if self.webDriver.get_text(element=self.locators.status % booking, locator_type='xpath') != "Cancelled":
                continue
            else:
                return True

    def verify_reservation_list(self):
        """
        To verify reservation list
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.booking_list, locator_type='xpath', time_out=120)
        bookings = self.webDriver.get_elements(element=self.locators.booking_list, locator_type='xpath')
        return bookings

    def verify_voyage_dropdown(self):
        """
        To verify voyage dropdown
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.voyage_dropdown, locator_type='xpath',
                                                      time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_dropdown, locator_type='xpath'):
            self.webDriver.click(element=self.locators.voyage_dropdown, locator_type='xpath')
            if len(self.webDriver.get_elements(element=self.locators.all_voyages, locator_type='xpath')) > 1:
                self.webDriver.click(element=self.locators.voyage_dropdown, locator_type='xpath')
                return True
            else:
                return False
        else:
            return False

    def hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')

    def verify_avg_turntime_request(self):
        """
        To verify avg turntime request
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.avg_turntime_request, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.avg_turntime_request, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_popup, locator_type='xpath'):
            raise Exception("Filter popup is not displaying")
        else:
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_number, locator_type='xpath',
                                                          time_out=60)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_number,
                                                               locator_type='xpath'):
                return False
            else:
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return True

    def verify_without_reservation(self):
        """
        To verify without reservation
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.without_reservation_request, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.without_reservation_request, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_popup, locator_type='xpath'):
            raise Exception("Filter popup is not displaying")
        else:
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_number, locator_type='xpath',
                                                          time_out=120)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_number,
                                                               locator_type='xpath'):
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return False
            else:
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return True

    def verify_special_request(self):
        """
        To verify special request report
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.special_request, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.special_request, locator_type='xpath')
        self.webDriver.scroll_mobile(1800, 1388, 1777, 922)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_popup, locator_type='xpath'):
            raise Exception("Filter popup is not displaying")
        else:
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_number, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.scroll_mobile(1400, 680, 2150, 676)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.special_request_col,
                                                               locator_type='xpath'):
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return False
            else:
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return True

    def verify_recap(self):
        """
        To verify recap report
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.recap_report, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.recap_report, locator_type='xpath')
        self.webDriver.scroll_mobile(1800, 1388, 1777, 922)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_popup, locator_type='xpath'):
            raise Exception("Filter popup is not displaying")
        else:
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_number, locator_type='xpath', time_out=60)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_number, locator_type='xpath'):
                return False
            else:
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return True

    def verify_dining_menifest(self):
        """
        To verify menifest report
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.manifest_report, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.manifest_report, locator_type='xpath')
        self.webDriver.wait_for(4)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_popup, locator_type='xpath'):
            raise Exception("Filter popup is not displaying")
        else:
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_number, locator_type='xpath', time_out=60)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_number, locator_type='xpath'):
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return False
            else:
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                return True

    def open_report_page(self):
        """
        To open table management report module
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.click_tm, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        self.webDriver.click(element=self.locators.reports, locator_type='xpath')

    def open_host_page(self):
        """
        To open host page
        :return:
        """
        self.webDriver.scroll_mobile(540, 1492, 500, 390)
        self.webDriver.explicit_visibility_of_element(element=self.locators.click_tm, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.host, locator_type='xpath',
                                                      time_out=180)
        self.webDriver.click(element=self.locators.host, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.venue_dropdown, locator_type='xpath',
                                                      time_out=180)

    def click_hamburger_menu(self):
        """
        To click hamburger menu
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')

    def open_reservation_page(self):
        """
        To open table management reservation module
        :return:
        """
        self.webDriver.click(element=self.locators.reservation, locator_type='xpath')