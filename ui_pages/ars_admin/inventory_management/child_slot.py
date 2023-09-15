__author__ = 'Krishna'

import time

from virgin_utils import *


class ChildSlot(General):
    """
    To initiate page class elements and function from child slot details page
    """

    def __init__(self, web_driver, test_data):

        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "three_dotted_menu": "//*[@id='MoreOption__div']",
            "move_slot_cta": "//*[text()='Move Slot']",
            "stop_sell": "//*[text()='Stop Sell']",
            "cancel_slot": "//*[text()='Cancel Slot']",
            "success_notification": "//*[@class='notification is-success']",
            "failed_notification": "//*[@class='notification is-danger']",
            "vendor_name": "//*[text()='Vendor']/../div[@class='text']",
            "transaction_type": "//*[text()='Transaction Type']/../div[@class='text']",
            "meeting_start_time": "//*[text()='Meeting Start Time']/../div[@class='text']",
            "meeting_end_time": "//*[text()='Meeting End Time']/../div[@class='text']",
            "meeting_location": "//*[text()='Activity Location']/../div[@class='text']",
            "total_available_capacity": "//*[text()='Total Available Capacity']/../div[@class='text']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "re_open_canceled_slot": "//*[text()='Reinstate Cancelled Slot']",
            "ok_button": "//*[text()='Ok']",
            "add_slot": "//button[text()='ADD SLOT']",
            "edit_location_time_icon": "//div[text()='Location & Time']/ancestor::div/div[@class='button btn-clr']",
            "booking_closing_time": "//div[text()='Booking Close Time']/following-sibling::div/div",
            "cancel_edit_location": "(//*[text()='Edit Location & Time']/../../../../footer//*[text()='CANCEL'])[3]",
            "edit_capacity_icon": "//div[text()='Capacity']/ancestor::div/div[@class='button btn-clr']",
            "get_booking_count": "//p[text()='Booking Count']/following-sibling::p",
            "cancel_edit_capacity": "(//button[text()='CANCEL'])[3]",
            "back_button": "//a[@class='back-button']",
            "organiser_title": "//div[text()='Organizer']",
            "save_hold_capacity": "//*[text()='Hold Capacity']/../div[@class='text']",
            "save_slot_capacity": "//*[text()='Slot Capacity']/../div[@class='text']",
            "edit_activity_duration_hour": "//div[text()='Activity Duration *']/following-sibling::div[1]/div[1]//input",
            "edit_activity_duration_min": "//div[text()='Activity Duration *']/following-sibling::div[1]/div[2]//input",
            "meeting_start_time_hour": "//div[text()='Meeting Start Time']/following-sibling::div[1]/div[1]//input",
            "meeting_start_time_min": "//div[text()='Meeting Start Time']/following-sibling::div[1]/div[2]//input",
            "meeting_end_time_hour": "//div[text()='Meeting End Time']/following-sibling::div[1]/div[1]//input",
            "meeting_end_time_min": "//div[text()='Meeting End Time']/following-sibling::div[1]/div[2]//input",
            "update_location_time": "(//button[text()='UPDATE'])[8]",
            "edit_total_capacity": "//input[@name='totalCapacity']",
            "hold_capacity": "//input[@name='holdCapacity']",
            "update_capacity": "(//button[text()='UPDATE'])[2]",
            "meeting_location_shore_side": "(//div[text()='Meeting Location'])[2]/following-sibling::div//span[text()='Shore Side']",
            "ineditable_booking_closing_hour": "(//div[text()='Booking Close Time']/following-sibling::div/div/p[@class='is-size-6'][1])[1]",

        })

    def click_on_three_dotted_menu_and_move_slot(self):
        """
        Click on three dotted menu on slot details page to move slot
        """
        self.webDriver.click(element=self.locators.three_dotted_menu, locator_type="xpath")
        self.webDriver.click(element=self.locators.move_slot_cta, locator_type="xpath")

    def verify_success_message(self):
        """
        verify success message after moving slot
        """
        return self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")

    def click_on_three_dotted_menu_and_stop_sell(self):
        """
        Click on three dotted menu on slot details page to stop sell
        """
        self.webDriver.click(element=self.locators.three_dotted_menu, locator_type="xpath")

        try:
            self.webDriver.click(element=self.locators.stop_sell, locator_type="xpath")
            if "Slot is already marked as Stop Sell." == self.webDriver.get_text(self.locators.failed_notification,
                                                                                 locator_type="xpath"):
                self.test_data['isStopSell'] = False
        except Exception:
            self.test_data['isStopSell'] = True

    def click_on_three_dotted_menu_and_cancel_slot(self):
        """
        Click on three dotted menu on slot details page to cancel slot
        """
        self.webDriver.click(element=self.locators.three_dotted_menu, locator_type="xpath")
        time.sleep(3)
        self.webDriver.click(element=self.locators.cancel_slot, locator_type="xpath")

    def click_on_three_dotted_menu_and_re_initiate_cancelled_slot(self):
        """
        click o three dotted menu and re initiate or reopen cancelled slot
        :return:
        """
        self.webDriver.click(element=self.locators.three_dotted_menu, locator_type="xpath")
        time.sleep(3)
        self.webDriver.click(element=self.locators.re_open_canceled_slot, locator_type="xpath")
        self.webDriver.click(element=self.locators.ok_button, locator_type="xpath")

    def copy_child_activity_details(self):
        """
        to get the parent activity details
        """
        self.test_data['child'] = dict()
        self.test_data['child']['vendorName'] = self.webDriver.get_text(element=self.locators.vendor_name,
                                                                    locator_type="xpath")
        self.test_data['child']['transactionType'] = self.webDriver.get_text(element=self.locators.transaction_type,
                                                                         locator_type="xpath")
        self.test_data['child']['meetingStartTime'] = self.webDriver.get_text(element=self.locators.meeting_start_time,
                                                                          locator_type="xpath")
        self.test_data['child']['meetingLocation'] = self.webDriver.get_text(element=self.locators.meeting_location,
                                                                         locator_type="xpath")
        self.test_data['child']['totalAvailableCapacity'] = \
            self.webDriver.get_text(element=self.locators.total_available_capacity, locator_type="xpath")

    def failed_notification(self):
        """
        verify if stop sell is already on opened slot
        """
        return self.webDriver.get_text(element=self.locators.failed_notification, locator_type="xpath")

    def verify_three_dotted_menu_not_present(self):
        """
        To verify that three dotted menu should not be present
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.three_dotted_menu, locator_type='xpath'):
            logger.debug("Three dotted menu is not present on child slot page")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Three dotted menu is present on child slot page")

    def verify_add_slot_button_not_enabled(self):
        """
        To verify that three dotted menu should not be present
        :return:
        """
        if not self.webDriver.is_element_enabled(element=self.locators.add_slot, locator_type='xpath'):
            logger.debug("Add slot button is not enabled on child slot page")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Add slot button is enabled on child slot page")

    def verify_booking_closing_time_not_editable(self):
        """
        To verify booking closing time is not editable
        :return:
        """
        self.webDriver.scroll_till_element(self.locators.organiser_title, 'xpath')
        self.webDriver.click(element=self.locators.edit_location_time_icon, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.ineditable_booking_closing_hour, locator_type='xpath'):
            logger.debug("booking closing time is not enabled on child slot page")
            self.webDriver.click(element=self.locators.cancel_edit_location, locator_type="xpath")
        else:
            self.webDriver.click(element=self.locators.cancel_edit_location, locator_type="xpath")
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Add slot button is enabled on child slot page")

    def verify_booking_count(self):
        """
        Verifu booking count in child slot capacity edit
        :return:
        """
        self.webDriver.click(element=self.locators.edit_capacity_icon, locator_type='xpath')
        booking_count = int(self.webDriver.get_text(element=self.locators.get_booking_count, locator_type="xpath"))
        checkin_count = int(self.test_data['checkedIn'].split('/')[1])
        assert booking_count == checkin_count, 'booking count is matching with checkedin count'
        self.webDriver.click(element=self.locators.cancel_edit_capacity, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button and go to parent activity from child activity
        :return:
        """
        self.webDriver.click(element=self.locators.back_button, locator_type="xpath")

    def verify_add_slot_button_not_present(self):
        """
        To verify that three dotted menu should not be present
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.add_slot, locator_type='xpath'):
            logger.debug("Add slot button is not present on child slot page")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Add slot button is present on child slot page")

    def verify_activity_details_after_edit(self):
        """
        Function to verify activity details after editing
        :return:
        """
        assert self.webDriver.get_text(element=self.locators.save_slot_capacity,locator_type="xpath") != self.test_data['slotCapacity'], 'Slot capacity not matching after edit'
        assert self.webDriver.get_text(element=self.locators.save_hold_capacity,locator_type="xpath") != self.test_data['holdCapacity'], 'Hold capacity not matching after edit'

    def edit_location_and_time(self):
        """
        To edit location and time  of an activity
        :return:
        """
        self.webDriver.click(element=self.locators.edit_location_time_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.meeting_location_shore_side, locator_type='xpath')
        meeting_start_time_hour = self.webDriver.get_web_element(element=self.locators.meeting_start_time_hour, locator_type='xpath').get_attribute('value')
        meeting_start_time_min = self.webDriver.get_web_element(element=self.locators.meeting_start_time_min,locator_type='xpath').get_attribute('value')
        meeting_start_time_hour = int(meeting_start_time_hour) + 1
        meeting_start_time_min = int(meeting_start_time_min) + 5
        self.test_data['childMeetingStartTime'] = f"{meeting_start_time_hour * 60 + meeting_start_time_min} Min before"
        self.webDriver.clear_text(element=self.locators.meeting_start_time_hour, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.meeting_start_time_hour, locator_type='xpath', text=meeting_start_time_hour)
        self.webDriver.clear_text(element=self.locators.meeting_start_time_min, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.meeting_start_time_min, locator_type='xpath', text=meeting_start_time_min)
        self.webDriver.clear_text(element=self.locators.meeting_end_time_hour, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.meeting_end_time_hour, locator_type='xpath', text="1")
        self.webDriver.clear_text(element=self.locators.meeting_end_time_min, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.meeting_end_time_min, locator_type='xpath', text="1")

        self.webDriver.clear_text(element=self.locators.edit_activity_duration_hour, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.edit_activity_duration_hour, locator_type='xpath', text="1")
        self.webDriver.clear_text(element=self.locators.edit_activity_duration_min, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.edit_activity_duration_min, locator_type='xpath', text="9")

        self.webDriver.click(element=self.locators.update_location_time, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def edit_capacity(self):
        """
        Function to edit capacity of an activity
        :return:
        """
        self.test_data['holdCapacity'] = generate_random_number(low=5, high=60,include_all=True)
        self.test_data['slotCapacity'] = four_digit_random_number()
        self.webDriver.click(element=self.locators.edit_capacity_icon, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.edit_total_capacity, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.edit_total_capacity, locator_type='xpath', text=self.test_data['slotCapacity'])
        self.webDriver.clear_text(element=self.locators.hold_capacity, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.hold_capacity, locator_type='xpath', text=self.test_data['holdCapacity'])
        self.webDriver.click(element=self.locators.update_capacity, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
