__author__ = 'Saloni.pattnaik'

import time

from selenium.webdriver.common.keys import Keys

from virgin_utils import *
from datetime import date


class ArsBookings(General):
    """
    ARS Admin Booking Page
    """

    def __init__(self, web_driver):
        """
        initiate booking elements
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "booking_page_header": "//p[@class='pageTitle']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "booking_date": "//div[@class='row ']//div[@class='col col-10'][1]//span",
            "booking_detail_arrow": "(//span[text()='%s'])[%s]/../..//button[@type='button']",
            "view_slot_details": "//button[text()='View Slot Details']",
            "new_booking": "//button[text()=' New Booking']",
            "add_sailor": "//button[text()='Add Sailor']",
            "search_sailor": "//input[@placeholder='Search Sailor']",
            "search_crew": "//input[@placeholder='Search Crew']",
            "sailor_checkbox": "(//span[@class='tick']//img[@class='SVGContainer '])[2]",
            "next": "//*[text()='Next']",
            "book_button": "//button[text()='Book']",
            "paid_by_radio_button": "//div[@class='check ']",
            "pay_and_book_button": "//button[text()='Pay And Book']",
            "page_loader": "//img[@alt='Loader']",
            "booking_confirm_status": "//span[text()='%s']/../..//div[3]//span",
            "booking_details_arrow": "//span[text()='%s']/../..//div[3]//span[text()='CONFIRMED']/../..//button",
            "cancel_header": "//div[text()='Cancel Booking']",
            "cancel_button": "//button[text()='Cancel Booking']",
            "cancel_booking": "//button[@class='button is-primary ']",
            "booking_status": "//p[text()='Booking Status']/..//p[2]",
            "filter": "//div[@class='sortIcon']//img[@class='SVGContainer ']",
            "ent_non_inventory_radio_button": "//span[text()='%s']/../../div[@class='check ']",
            "apply": "//button[text()='APPLY']",
            "activity_list": "//div[@class='row ']",
            "activity_type": "//div[@class='row ']//div//span[text()='%s']",
            "shore_activity_type": "(//div[@class='row ']//div//span[text()='Shore Thing'])[1]",
            "three_dot_filter": "//div[@class='dropdown-trigger']//img[@class='SVGContainer ']",
            "type_checkbox": "//label[text()='Type']/..//img[@class='SVGContainer ']",
            "checkin_status": "//*[@class='sailor-detail']//div[@class='column is-full']//div[5]",
            "sailor_name": "(//*[text()='Yes']/../..//span[@class='text-left is-size-9'])[1]",
            "cancel_sailor": "//div[@class='ButtonsContainer__div']//button[text()='Cancel']",
            "cancel_second": "//button[text()='Cancel']",
            "accept_cancel": "//*[text()='Yes']",
            "shore_thing_check_box": "//*[@id='PA']/../div",
            "clear_all": "//*[text()='CLEAR ALL']",
            "booking-time": "//span[text()='%s']/../..//button[@type='button']/preceding-sibling::div[1]",
            "booking_checkbox": "//span[text()='%s']/../..//div[3]//span[text()='CONFIRMED']/../../div//img["
                                "@class='SVGContainer ']",
            "notification_icon": "//img[@class='SVGContainer arrow-size']",
            "message_title": "//label[text()='Message Title']/../input",
            "message": "//label[text()='Message']/../textarea[@name='message']",
            "send_button": "//button[text()='Send']",
            "success_notification": "//div[@class='notification is-success']",
            "booking_checkin_status": "//span[text()='%s']/../..//div[3]//span[text("
                                      ")='CONFIRMED']/../../button//preceding-sibling::div[1]/span",
            "action_dropdown": "//div[@class='ActionDropdownContainer__div']/img",
            "mark_arrived": "//a[text()='Mark Arrived']",
            "cancel_condition": "//button[text()='Ok']",
            "slot_cancel_date": "(//span[text()='%s'])/../..//button[@type='button']",
            "three_dot_icon": "(//div[@class='dropdown-trigger'])[2]",
            "cancel_slot": "//button[text()='Cancel Slot']",
            "slot_time": "//div[@class='container header-container']//div[@class='column is-size-6']",
            "cancel_slot_button": "(//button[text()='Cancel Slot'])[2]",
            "conflict_mark": "//div[@class='column is-full is-pulled-right']//*",
            "search_booked_sailor": "//input[@class='NavSearchFieldTextBox']",
            "booked_sailor_count": "//div[@class='row row-border']",
            "booked_sailor_name": "(//div[@class='row row-border'])[%s]//span",
            "booked_dropdown": "(//div[@class='row row-border'])[%s]//span/../..//button//img",
            "booked_activity_count": "//div[@class='row booking-row-bottom']",
            "activity_status": "(//div[@class='row booking-row-bottom'])[%s]//div[5]",
            "dropdown": "(//div[@class='row booking-row-bottom'])[%s]//button//img",
            "no_records_found": "//*[text()='No Records Found']",
            "select_sailor": "(//*[text()='Please select the sailor paying for this "
                             "booking']/../../following-sibling::div)[1]",
            "click_on_sailor_checkbox": "(//*[text()='%s'])[2]",
            "sort_by_date": "//span[text()='Date']",
            "slot_drop_down": "//button[@type='button']/img",
            "booking_search": "//input[@class='BookingSearchFieldTextBox']",
            "search_icon": "search-icon",
            "no_results_found_for_search": "//*[contains(text(),'No Result found for')]",
            "is_confirmed": "//*[contains(text(),'CONFIRMED')]",
            "confirmed_checkbox": "//*[contains(text(),'CONFIRMED')]/../../..//span/span/img",
            "cancel_searched_booking": "//*[text()='Discard']/../*[text()='Cancel Booking']",
            "cancel_booking_actions": "//*[text()='Cancel Booking']",
            "activity_name": "//*[@name='activityCode']/../../../div/div/div/div[1]",
            "select_slot": "(//*[text()='%s']/../../div)[5]",
            "edit_booking": "//*[text()='Edit Booking']",
            "edit_discount": "discountAmount",
            "edit_notes": "//*[text()='Notes']/preceding-sibling::input",
            "edit_update": "//*[text()='UPDATE']",
            "verify_edited": "//*[text()='edit_notes']",
            "cancellation_reason": "//*[text()='Cancellation Reason']/../div/div/div[2]/div",
            "custom_reason": "customReason",
            "limit_error_message": "//*[text()='Max limit of 250 characters reached']",
            "discard_cancellation": "//*[text()='Discard']",
            "crew_checkbox": "//*[text()='%s']/../../../../div/span[@role='button']",
            "add_crew": "//*[text()='Add Crew']",
            "company_account": "//*[text()='Company Account']",
            "select_account_to_pay": "//*[text()='Prepaid - Spa']"
        })

    def wait_for_loader_to_complete(self):
        """
        Wait for loader to complete
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_booking_page_header(self):
        """
        To Verify user is successfully landing on ARS bookings page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        return self.webDriver.get_text(element=self.locators.booking_page_header, locator_type='xpath')

    def get_activity_list(self):
        """
        To get vendor list form activity booking  main page
        """
        activities = self.webDriver.get_elements(element=self.locators.activity_name, locator_type="xpath")
        activity_list = []
        for activity in activities:
            if activity.text not in ("Activity ID", ''):
                activity_list.append(activity.text)
        return set(activity_list)

    def click_on_selected_activity(self, activity):
        """
        function to open activity slot for booking
        :return:
        """
        self.webDriver.click(element=self.locators.select_slot % activity, locator_type="xpath")

    def edit_confirmed_booking(self):
        """
        Function to edit the confirmed booking
        :return:
        """
        self.webDriver.click(element=self.locators.edit_booking, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.set_text(element=self.locators.edit_discount, locator_type="name", text=0)
        self.webDriver.set_text(element=self.locators.edit_notes, locator_type="xpath", text="edit_notes")
        self.webDriver.click(element=self.locators.edit_update, locator_type="xpath")
        self.wait_for_loader_to_complete()
        status = self.webDriver.is_element_display_on_screen(element=self.locators.verify_edited, locator_type="xpath")
        assert status, "Failed to edit the confirmed booking"

    def verify_character_limit_in_custom_reason(self):
        """
        To verify character limit in custom message
        :return:
        """
        custom_reason = "A while back I needed to count the amount of letters that a piece of text in an email template had " \
                        "(to avoid passing any character limits). Unfortunately, I could not think of a quick way to do so " \
                        "on my macbook and I therefore turned to the InternetThere "
        self.cancel_booking()
        self.accept_cancel_condition()
        cancellation_element = self.webDriver.get_web_element(element=self.locators.cancellation_reason,
                                                              locator_type='xpath')
        size = cancellation_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_option_by_offset(cancellation_element, x, y, "Other")
        self.webDriver.set_text(element=self.locators.custom_reason, locator_type="name", text=custom_reason)
        error_message = self.webDriver.is_element_display_on_screen(element=self.locators.limit_error_message,
                                                                    locator_type="xpath")
        assert error_message, "Error message not displayed when more than 250 characters entered in custom reason filed"
        self.webDriver.click(element=self.locators.discard_cancellation, locator_type="xpath")
        self.wait_for_loader_to_complete()

    def check_for_any_existing_confirmed_booking(self, cabin):
        """
        Function to cancel the existing booking before proceeding to book any slot
        :return:
        """
        status = self.webDriver.is_element_display_on_screen(element=self.locators.booking_search, locator_type="xpath")
        if status:
            self.webDriver.set_text(element=self.locators.booking_search, locator_type="xpath", text=cabin)
            self.webDriver.click(element=self.locators.search_icon, locator_type="id")
            if not self.webDriver.is_element_display_on_screen(element=self.locators.no_results_found_for_search,
                                                               locator_type="xpath"):
                if self.webDriver.is_element_display_on_screen(element=self.locators.is_confirmed,
                                                               locator_type="xpath"):
                    elements = self.webDriver.get_elements(element=self.locators.confirmed_checkbox,
                                                           locator_type="xpath")
                    for slot_checkbox in elements:
                        slot_checkbox.click()
                    self.webDriver.click(element=self.locators.action_dropdown, locator_type="xpath")
                    self.webDriver.click(element=self.locators.cancel_booking_actions, locator_type="xpath")
                    self.wait_for_loader_to_complete()

    def sort_slots_by_date(self, activity_type):
        """
        To verify user is able to sort the activity slot
        :return:
        """
        if activity_type == "'Ent - Inventoried":
            self.webDriver.click(element=self.locators.sort_by_date, locator_type="xpath")
            if not self.webDriver.is_element_display_on_screen(element=self.locators.loader, locator_type='xpath'):
                self.webDriver.click(element=self.locators.sort_by_date, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
        else:
            self.webDriver.click(element=self.locators.sort_by_date, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                           time_out=60)

    def view_slot_details(self):
        """
        To click view slot details
        """
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.view_slot_details, locator_type='xpath')
        self.wait_for_loader_to_complete()

    def click_new_booking(self):
        """
        click new booking
        """
        if self.webDriver.is_element_enabled(element=self.locators.new_booking, locator_type='xpath'):
            self.webDriver.click(element=self.locators.new_booking, locator_type='xpath')
            return True
        else:
            self.webDriver.navigate_back()
            self.wait_for_loader_to_complete()
            return False

    def is_new_booking_cta_enabled(self):
        """
        This is to verify the new booking cta enabled or disabled
        :return:
        """
        return self.webDriver.is_element_enabled(element=self.locators.new_booking, locator_type='xpath')

    def add_sailor_for_booking(self, stateroom, test_data, deduct_from):
        """
        Add sailor to booking activity
        :param test_data:
        :param stateroom:
        :param deduct_from:
        :return:
        """
        self.webDriver.click(element=self.locators.add_sailor, locator_type='xpath')
        self.webDriver.get_web_element(element=self.locators.search_sailor, locator_type='xpath').send_keys(Keys.ENTER)
        self.webDriver.set_text(element=self.locators.search_sailor, locator_type='xpath', text=stateroom)
        self.webDriver.get_web_element(element=self.locators.search_sailor, locator_type='xpath').send_keys(Keys.ENTER)
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.sailor_name, locator_type='xpath')
        test_data['searched_sailor_name'] = self.webDriver.get_text(element=self.locators.sailor_name,
                                                                    locator_type='xpath')
        self.webDriver.click(element=self.locators.next, locator_type='xpath')
        self.wait_for_loader_to_complete()
        if len(self.webDriver.get_elements(element=self.locators.conflict_mark, locator_type='xpath')) is not 0:
            self.webDriver.click(element=self.locators.cancel_sailor, locator_type='xpath')
            self.webDriver.click(element=self.locators.cancel_second, locator_type="xpath")
            self.webDriver.click(element=self.locators.accept_cancel, locator_type="xpath")
            test_data['booking_success'] = False
        else:
            if self.webDriver.is_element_enabled(element=self.locators.next, locator_type='xpath'):
                self.webDriver.click(element=self.locators.next, locator_type='xpath')
                self.webDriver.click(element=self.locators.book_button, locator_type='xpath')
                sailor_name = self.webDriver.get_text(element=self.locators.select_sailor, locator_type="xpath")
                if deduct_from == "sailor":
                    self.webDriver.click(element=self.locators.click_on_sailor_checkbox % sailor_name,
                                         locator_type="xpath")
                else:
                    self.webDriver.click(element=self.locators.company_account, locator_type="xpath")
                    self.webDriver.click(element=self.locators.select_account_to_pay, locator_type="xpath")
                self.webDriver.click(element=self.locators.pay_and_book_button, locator_type="xpath")
                if not self.webDriver.is_element_display_on_screen(element=self.locators.success_notification,
                                                                   locator_type='xpath'):
                    test_data['booking_success'] = False
                    self.wait_for_loader_to_complete()
                else:
                    test_data['booking_success'] = True
                    self.wait_for_loader_to_complete()

    def add_crew_for_booking(self, crew_name, test_data, deduct_from):
        """
        Add crew to book activity
        :param deduct_from:
        :param test_data:
        :param crew_name:
        :return:
        """
        self.webDriver.click(element=self.locators.add_crew, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.get_web_element(element=self.locators.search_crew, locator_type='xpath').send_keys(Keys.ENTER)
        self.webDriver.set_text(element=self.locators.search_crew, locator_type='xpath', text=crew_name)
        self.webDriver.get_web_element(element=self.locators.search_crew, locator_type='xpath').send_keys(Keys.ENTER)
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.crew_checkbox % crew_name, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.next, locator_type='xpath')
        if len(self.webDriver.get_elements(element=self.locators.conflict_mark, locator_type='xpath')) is not 0:
            self.webDriver.click(element=self.locators.cancel_sailor, locator_type='xpath')
            self.webDriver.click(element=self.locators.cancel_second, locator_type="xpath")
            self.webDriver.click(element=self.locators.accept_cancel, locator_type="xpath")
            test_data['booking_success'] = False
        else:
            if self.webDriver.is_element_enabled(element=self.locators.next, locator_type='xpath'):
                self.webDriver.click(element=self.locators.next, locator_type='xpath')
                self.webDriver.click(element=self.locators.book_button, locator_type='xpath')
                if deduct_from == "crew":
                    self.webDriver.click(element=self.locators.click_on_sailor_checkbox % crew_name,
                                         locator_type="xpath")
                else:
                    self.webDriver.click(element=self.locators.company_account, locator_type="xpath")
                    self.webDriver.click(element=self.locators.select_account_to_pay, locator_type="xpath")
                self.webDriver.click(element=self.locators.pay_and_book_button, locator_type="xpath")
                if not self.webDriver.is_element_display_on_screen(element=self.locators.success_notification,
                                                                   locator_type='xpath'):
                    test_data['booking_success'] = False
                    self.wait_for_loader_to_complete()
                    raise Exception("Activity booking for crew is not successful")
                else:
                    test_data['booking_success'] = True
                    self.wait_for_loader_to_complete()

    def cancel_booked_activity(self, stateroom, test_data):
        """
        To cancel booked activity of sailor
        :param stateroom:
        :param test_data:
        """
        self.webDriver.get_web_element(element=self.locators.search_booked_sailor, locator_type='xpath').send_keys(
            Keys.ENTER)
        self.webDriver.set_text(element=self.locators.search_booked_sailor, locator_type='xpath', text=stateroom)
        self.webDriver.get_web_element(element=self.locators.search_booked_sailor, locator_type='xpath').send_keys(
            Keys.ENTER)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        sailor_counts = self.webDriver.get_elements(element=self.locators.booked_sailor_count, locator_type='xpath')
        for sailor in range(1, len(sailor_counts)):
            if self.webDriver.get_text(element=self.locators.booked_sailor_name % sailor, locator_type='xpath') == \
                    test_data['searched_sailor_name']:
                self.webDriver.click(element=self.locators.booked_dropdown % sailor, locator_type='xpath')
                self.webDriver.wait_for(5)
                booked_activities = self.webDriver.get_elements(element=self.locators.booked_activity_count,
                                                                locator_type='xpath')
                for activity in range(1, len(booked_activities) + 1):
                    if self.webDriver.get_text(element=self.locators.activity_status % activity,
                                               locator_type='xpath') == "CONFIRMED":
                        self.webDriver.click(element=self.locators.dropdown % activity, locator_type='xpath')
                        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,
                                                                        locator_type='xpath', time_out=60)
                        self.cancel_booking()
                        if self.accept_cancel_condition() is False:
                            self.click_cancel_button()
                            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,
                                                                            locator_type='xpath', time_out=60)
                            self.webDriver.navigate_back()
                            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,
                                                                            locator_type='xpath', time_out=60)
                            self.webDriver.navigate_back()
                            break
                        else:
                            self.click_cancel_button()
                            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,
                                                                            locator_type='xpath', time_out=60)
                            self.webDriver.navigate_back()
                            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,
                                                                            locator_type='xpath', time_out=60)
                            self.webDriver.navigate_back()
                            break

    def verify_confirmation_status(self, sailor_name):
        """
        Verify booking confirmation status
        :param sailor_name:
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        statuses = self.webDriver.get_elements(element=self.locators.booking_confirm_status % sailor_name,
                                               locator_type='xpath')
        for status in statuses:
            if status.text == "CONFIRMED":
                return True
            else:
                continue

    def booking_details_page(self, sailor_or_name):
        """
        To open booking details page
        :param sailor_or_name:
        """
        statuses = self.webDriver.get_elements(element=self.locators.booking_confirm_status % sailor_or_name,
                                               locator_type='xpath')
        for status in statuses:
            if status.text == "CONFIRMED":
                self.webDriver.click(element=self.locators.booking_details_arrow % sailor_or_name, locator_type='xpath')
                break
            else:
                continue
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def cancel_booking(self):
        """
        To cancel booking
        """
        self.webDriver.click(element=self.locators.cancel_button, locator_type='xpath')

    def accept_cancel_condition(self):
        """
        To accept cancel condition
        :return:
        """
        time.sleep(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.cancel_condition, locator_type='xpath'):
            self.webDriver.click(element=self.locators.cancel_condition, locator_type='xpath')
        else:
            return False

    def click_cancel_button(self):
        """
        To click cancel booking button
        """
        self.webDriver.click(element=self.locators.cancel_booking, locator_type='xpath')

    def verify_cancel_header(self):
        """
        To verify the header of cancel tab
        :return:
        """
        return self.webDriver.get_text(element=self.locators.cancel_header, locator_type='xpath')

    def get_booking_status(self):
        """
        To get the booking status
        :return:
        """
        return self.webDriver.get_text(element=self.locators.booking_status, locator_type='xpath')

    def loaded_disappear(self):
        """
        Wait till loader disappear
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def navigate_back(self):
        """
        Click on tab back button
        :return:
        """
        self.webDriver.navigate_back()
        self.wait_for_loader_to_complete()

    def verify_loader(self):
        """
        Verify loader after page scroll
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.page_loader, locator_type='xpath')

    def click_filter_icon(self):
        """
        click on filter icon on booking page
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.click(element=self.locators.clear_all, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def select_activity_in_filter(self, activity):
        """
        apply filter by selecting activity
        :param activity:
        """
        self.webDriver.click(element=self.locators.ent_non_inventory_radio_button % activity, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_3_dotted_filter(self):
        """
        Verify activity type and length
        """
        self.webDriver.click(element=self.locators.three_dot_filter, locator_type='xpath')

    def apply_type_filter(self):
        """
        Apply activity type filter
        """
        self.webDriver.click(element=self.locators.type_checkbox, locator_type='xpath')

    def filter_for_shore_things(self):
        """
        filter for shore things
        """
        self.click_filter_icon()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.shore_thing_check_box, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.apply, locator_type="xpath")
        self.wait_for_loader_to_complete()

    def get_shore_activity_type(self):
        """
        get shore activity type
        """
        return self.webDriver.get_text(element=self.locators.shore_activity_type, locator_type="xpath")

    def select_booking_checkbox(self, sailor_name):
        """
        Select checkbox with confirmed status
        :param sailor_name:
        :return:
        """
        statuses = self.webDriver.get_elements(element=self.locators.booking_confirm_status % sailor_name,
                                               locator_type='xpath')
        for status in statuses:
            if status.text == "CONFIRMED":
                self.webDriver.click(element=self.locators.booking_checkbox % sailor_name, locator_type='xpath')
                break
            else:
                continue

    def send_notification(self, sailor_name):
        """
        Send notification to sailor
        :param sailor_name:
        :return:
        """
        self.webDriver.click(element=self.locators.notification_icon, locator_type='xpath')
        self.webDriver.get_web_element(element=self.locators.message_title, locator_type='xpath').send_keys(Keys.ENTER)
        self.webDriver.set_text(element=self.locators.message_title, locator_type='xpath',
                                text='Notify to ' + sailor_name)
        self.webDriver.get_web_element(element=self.locators.message, locator_type='xpath').send_keys(
            Keys.ENTER)
        self.webDriver.set_text(element=self.locators.message, locator_type='xpath',
                                text=sailor_name + ' Booking Confirmed')
        self.webDriver.click(element=self.locators.send_button, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.success_notification,
                                                       locator_type='xpath'):
            return True
        else:
            return False

    def get_check_in_status(self, sailor_name):
        """
        Select checkbox with confirmed status
        :param sailor_name:
        :return:
        """
        statuses = self.webDriver.get_elements(element=self.locators.booking_confirm_status % sailor_name,
                                               locator_type='xpath')
        for status in statuses:
            if status.text == "CONFIRMED":
                return self.webDriver.get_text(element=self.locators.booking_checkin_status % sailor_name,
                                               locator_type='xpath')
            else:
                continue

    def change_check_in_status(self):
        """
        Select checkbox with confirmed status
        :return:
        """
        self.webDriver.click(element=self.locators.action_dropdown, locator_type='xpath')
        self.webDriver.click(element=self.locators.mark_arrived, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.success_notification,
                                                       locator_type='xpath'):
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            return True
        else:
            return False

    def cancel_slot(self, book_date):
        """
        To click arrow of booking detail
        :param book_date:
        """
        self.webDriver.scroll_complete_page_top()
        while not self.webDriver.is_element_display_on_screen(element=self.locators.slot_cancel_date % book_date,
                                                              locator_type='xpath'):
            self.webDriver.scroll(0, 10000)
        return self.webDriver.get_elements(element=self.locators.slot_cancel_date % book_date, locator_type='xpath')

    def new_booking_availability(self):
        """
        To verify new booking button available or not
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.new_booking, locator_type='xpath'):
            return True
        else:
            self.webDriver.navigate_back()
            return False

    def get_slot_time(self):
        """
        To get the slot time
        :return:
        """
        slot = self.webDriver.get_text(element=self.locators.slot_time, locator_type='xpath')
        slot_time = slot.split('| ')
        return slot_time

    def click_cancel_slot(self):
        """
        To cancel slot
        :return:
        """
        self.webDriver.click(element=self.locators.three_dot_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.cancel_slot, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.click(element=self.locators.cancel_slot_button, locator_type='xpath')
        assert self.verify_success_message() == "Slot successfully cancelled", "Failed to cancel slot from booking management"

    def is_no_records_found(self):
        """
        Check if no records found is displayed
        """
        record_status = self.webDriver.is_element_display_on_screen(element=self.locators.no_records_found,
                                                                    locator_type="xpath")
        return record_status

    def verify_success_message(self):
        """
        Verify success message
        """
        return self.webDriver.get_text(element=self.locators.success_notification, locator_type='xpath')
