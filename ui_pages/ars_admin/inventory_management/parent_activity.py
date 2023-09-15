__author__ = 'Krishna'

from virgin_utils import *


class ParentActivity(General):
    """
    To initiate page class elements from parent activity details and slot list page
    """

    def __init__(self, web_driver, test_data):

        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "activities": "(//*[text()='Activities'])[2]",
            "filter_link": "//*[@class='SVGContainer btn-img-clr']",
            "activities_list": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div/a",
            "select_activity": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div/a/button/div[text("
                               ")=\"{}\"]",
            "slots_tab": "//*[text()='SLOTS']",
            "add_slots": "//*[text()='ADD SLOT']",
            "slot_list": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div",
            "selected_slot": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div[text("
                             ")='{}']/following-sibling::div[text()='{}']/../div/a",
            "vendor_name": "//*[text()='Vendor']/../div[@class='text']",
            "transaction_type": "//*[text()='Transaction Type']/../div[@class='text']",
            "meeting_start_time": "//*[text()='Meeting Start Time']/../div[@class='text']",
            "save_crew_price": "//*[text()='Crew Price']/parent::div",
            "save_selling_price": "//div[@class='column selling-price-margin ']",
            "save_hold_capacity": "//*[text()='Hold Capacity']/../div[@class='text']",
            "save_slot_capacity": "//*[text()='Slot Capacity']/../div[@class='text']",
            "meeting_end_time": "//*[text()='Meeting End Time']/../div[@class='text']",
            "meeting_location": "//*[text()='Activity Location']/../div[@class='text']",
            "activity_duration": "//*[text()='Activity Duration']/../div[@class='text']",
            "total_available_capacity": "//*[text()='Total Available Capacity']/../div[@class='text']",
            "is_waiver_required": "//*[text()='Is Waiver Required']/../div[@class='text']",
            "newly_created_slot": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div[contains(text(),"
                                  "'{}')]/following-sibling::div[contains(text(),'{}')]/../div/a ",
            "new_booking": "//*[text()='New Booking']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "activity_name": "//div[text()='Activity Name']/following-sibling::div",
            "activity_code": "//div[text()='Activity Code']/following-sibling::div",
            "account_type": "(//*[@id='accountType']/div/div/div)[1]",
            "edit_location_time_icon": "//div[text()='Location & Time']/ancestor::div/div[@class='button btn-clr']",
            "edit_organiser_icon": "//div[text()='Organizer']/ancestor::div/div[@class='button btn-clr']",
            "edit_other_info_icon": "//div[text()='Others Info']/ancestor::div/div[@class='button btn-clr']",
            "edit_transaction_type": "//div[@id='accountType']/div/div[2]",
            "edit_vendor": "(//*[@class='css-19bqh2r'])[2]",
            "update_organiser": "(//*[text()='Edit Organiser']/../../../../footer//*[text()='UPDATE'])[2]",
            "cancel_organiser":"(//*[text()='Edit Organiser']/../../../../footer//*[text()='CANCEL'])[3]",
            "organiser_title": "//div[text()='Organizer']",
            "edit_meeting_location": "(//div[text()='Meeting Location'])[2]/parent::div//div[@class='column'][3]//span[text()='Shore Side']",
            "edit_meeting_venue": "//label[text()='Venue']/parent::div/div/div/div[2]",
            "edit_activity_location": "//div[text()='Activity Location']/parent::div//span[text()='Shore Side']",
            "edit_activity_venue": "//div[text()='Activity Location']/parent::div//label[text()='Venue']/parent::div/div/div/div[2]",
            "update_location_time": "(//*[text()='Edit Location & Time']/../../../../footer//*[text()='UPDATE'])[2]",
            "edit_capacity_icon": "//div[text()='Capacity']/ancestor::div/div[@class='button btn-clr']",
            "edit_total_capacity": "//input[@name='totalCapacity']",
            "hold_capacity": "//input[@name='holdCapacity']",
            "update_capacity": "(//button[text()='UPDATE'])[2]",
            "crew_price": "(//input[@name='crewPrice'])[1]",
            "edit_pricing_icon": "//div[text()='Pricing']/ancestor::div/div[@class='button btn-clr']",
            "selling_price": "(//input[@name='price'])[2]",
            "update_pricing": "//*[text()='Edit Pricing']/../../../../footer//*[text()='UPDATE']",
            "meeting_location_shore_side": "(//div[text()='Meeting Location'])[2]/following-sibling::div//span[text()='Shore Side']",
            "edit_activity_duration_hour": "//div[text()='Activity Duration *']/following-sibling::div[1]/div[1]//input",
            "edit_activity_duration_min": "//div[text()='Activity Duration *']/following-sibling::div[1]/div[2]//input",
            "meeting_start_time_hour": "//div[text()='Meeting Start Time']/following-sibling::div[1]/div[1]//input",
            "meeting_start_time_min": "//div[text()='Meeting Start Time']/following-sibling::div[1]/div[2]//input",
            "meeting_end_time_hour": "//div[text()='Meeting End Time']/following-sibling::div[1]/div[1]//input",
            "meeting_end_time_min": "//div[text()='Meeting End Time']/following-sibling::div[1]/div[2]//input",
            "edit_conflict_resolution_time": "//*[@id='conflict_resolution_time_frame']/div/div/div",
            "edit_is_waiver_required": "//span[text()='Is Waiver Required']",
            "update_other_info": "//*[text()='Edit Others']/../../../../footer//*[text()='UPDATE']",
        })

    def click_on_slots_cta(self):
        """
        Click on add slots tab from activity details page
        """
        self.webDriver.click(element=self.locators.slots_tab, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def click_on_add_slots_cta(self):
        """
        Click on add_slots tab from slots list page
        """
        self.webDriver.click(element=self.locators.add_slots, locator_type="xpath")

    def get_slot_list(self):
        """
        get the slot available in the list
        """
        return self.webDriver.get_elements(element=self.locators.slot_list, locator_type="xpath")

    def verify_newly_crated_slot_date(self):
        """
        Verify newly created slots for any activity
        """
        new_slot_date = self.test_data['newSlotTime'].split()
        new_slot_time = twenty_four_hour_format_converter(self.test_data['newSlotTime'][-8:]).strip()
        time.sleep(5)
        slot_list = self.get_slot_list()
        for slots in slot_list:
            slot_columns = slots.text.split()
            if slot_columns[0][:5] == new_slot_date[0][:5]:
                logger.info(f"new slot date and time is {new_slot_date[0][:5]} : {new_slot_time}")
                break
        else:
            raise Exception(f"new slot date {new_slot_date[0][:5]} and time {new_slot_time} not matching")

    def copy_parent_activity_details(self):
        """
        to get the parent activity details
        """
        self.test_data['parent'] = dict()
        self.webDriver.scroll_till_element(element=self.locators.vendor_name, locator_type="xpath")
        self.test_data['parent']['vendorName'] = self.webDriver.get_text(element=self.locators.vendor_name,
                                                                         locator_type="xpath")
        self.webDriver.scroll_till_element(element=self.locators.transaction_type, locator_type="xpath")
        self.test_data['parent']['transactionType'] = self.webDriver.get_text(element=self.locators.transaction_type,
                                                                              locator_type="xpath")
        self.test_data['parent']['meetingStartTime'] = self.webDriver.get_text(element=self.locators.meeting_start_time,
                                                                               locator_type="xpath")
        self.test_data['parent']['meetingEndTime'] = self.webDriver.get_text(element=self.locators.meeting_end_time,
                                                                               locator_type="xpath")

        self.test_data['parent']['meetingLocation'] = self.webDriver.get_text(element=self.locators.meeting_location,
                                                                              locator_type="xpath")
        self.test_data['parent']['crewPrice'] = self.webDriver.get_text(element=self.locators.save_crew_price,
                                                                              locator_type="xpath")
        self.test_data['parent']['totalAvailableCapacity'] = \
            self.webDriver.get_text(element=self.locators.total_available_capacity, locator_type="xpath")
        self.test_data['parent']['isWaiverRequired'] = self.webDriver.get_text(element=self.locators.is_waiver_required,
                                                                              locator_type="xpath")

    def open_newly_created_slot(self):
        """
        open newly created slot from list
        """
        new_slot = self.test_data['newSlotTime'].split()
        new_slot_date = new_slot[0][:5]
        new_slot_time = twenty_four_hour_format_converter(self.test_data['newSlotTime'][-8:]).strip()
        self.webDriver.click(element=self.locators.newly_created_slot.format(new_slot_date, new_slot_time),
                             locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def check_for_upcoming_slots(self):
        """
        check for upcoming slots to move to next day
        """
        for activities in self.test_data['activityNames']:
            self.webDriver.click(element=self.locators.activities, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.copy_parent_activity_details()
            self.click_on_slots_cta()
            slot_list = self.get_slot_list()
            for slots in slot_list:
                slot_columns = slots.text.split()
                current_date = datetime.today().date().strftime("%m/%d/%Y")
                if slot_columns[0] > current_date and slot_columns[5] == 'OPEN':
                    self.test_data['cancelSlotTime'] = slot_columns[1]
                    self.test_data['checkedIn'] = slot_columns[7]
                    self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                         locator_type="xpath")
                    self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                    time_out=60)
                    self.test_data['isSlotAvailable'] = True
                    return
        else:
            self.test_data['isSlotAvailable'] = False
            pytest.skip(msg="no upcoming slots available to move")

    def check_for_upcoming_cancelled_slot(self):
        """
        check for upcoming slots to move to next day
        """
        for activities in self.test_data['activityNames']:
            self.webDriver.click(element=self.locators.activities, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.click_on_slots_cta()
            slot_list = self.get_slot_list()
            for slots in slot_list:
                slot_columns = slots.text.split()
                current_date = datetime.today().date().strftime("%m/%d/%Y")
                if slot_columns[0] > current_date and slot_columns[5] == 'Cancelled':
                    self.test_data['cancelSlotTime'] = slot_columns[1]
                    self.test_data['checkedIn'] = slot_columns[7]
                    self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                         locator_type="xpath")
                    self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                    time_out=60)
                    self.test_data['isCancelledSlotAvailable'] = True
                    return
        else:
            self.test_data['isCancelledSlotAvailable'] = False
            pytest.skip(msg="no upcoming slots available to move")

    def check_spa_slot_available_for_booking(self):
        """
        check for the available spa slots for booking
        """
        for activities in self.test_data['spaActivityNames']:
            self.webDriver.click(element=self.locators.activities, locator_type="xpath")
            self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.click_on_slots_cta()
            slot_list = self.get_slot_list()
            for slots in slot_list:
                slot_columns = slots.text.split()
                current_date = datetime.today().date().strftime("%m/%d/%Y")
                current_time = datetime.now().strftime("%H:%M")
                if slot_columns[0] > current_date and slot_columns[1] > current_time:
                    self.webDriver.click(
                        element=self.locators.newly_created_slot.format(slot_columns[0], slot_columns[1]),
                        locator_type="xpath")
                    self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                    time_out=60)
                    self.test_data['bookedSpaStartTime'] = slot_columns[1]
                    self.test_data['bookedSpaEndTime'] = slot_columns[3]
                    self.test_data['bookedSpaActivityName'] = activities
                    self.test_data['bookedSpaActivityDate'] = slot_columns[0]
                    self.test_data['isSapSlotAvailable'] = True
                    return
        else:
            self.test_data['isSapSlotAvailable'] = False

    def click_on_new_booking_cta(self):
        """
        Book for the selected spa activity slot
        """
        self.webDriver.click(element=self.locators.new_booking, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def check_for_cancelled_slot(self):
        """
        check for cancelled slot
        """
        self.click_on_slots_cta()
        slot_list = self.get_slot_list()
        for slots in slot_list:
            slot_columns = slots.text.split()
            if slot_columns[1] > self.test_data['cancelSlotTime'] and slot_columns[5] == 'Cancelled':
                break
        else:
            raise Exception("slot not cancelled successfully")

    def edit_organiser(self):
        """
        To edit organizer on main activity details screen
        :return:
        """
        self.webDriver.scroll_till_element(self.locators.organiser_title, 'xpath')
        self.webDriver.click(element=self.locators.edit_organiser_icon, locator_type='xpath')
        account_type = self.webDriver.get_text(element=self.locators.account_type, locator_type='xpath')
        if account_type == 'Pre Paid':
            self.webDriver.enter_data_in_textbox_using_action(element=self.locators.account_type, locator_type='xpath', text='Onboard')
            self.test_data['parent']['transactionType'] = 'Onboard'
        else:
            self.webDriver.enter_data_in_textbox_using_action(element=self.locators.account_type, locator_type='xpath',
                                                              text='Pre Paid')
            self.test_data['parent']['transactionType'] = 'Pre-Paid'
        self.webDriver.select_dynamic_dropdown_data_using_action_keys(element=self.locators.edit_vendor, locator_type='xpath')
        try:
            self.webDriver.click(element=self.locators.update_organiser, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        except Exception:
            self.webDriver.click(element=self.locators.cancel_organiser, locator_type="xpath")
        finally:
            self.test_data['vendorName'] = self.webDriver.get_text(element=self.locators.vendor_name, locator_type="xpath")

    def save_used_activity_data(self, test_data):
        """
        To save name and activity id of activity opened
        :param test_data:
        :return:
        """
        test_data['activity_name'] = self.webDriver.get_text(element=self.locators.activity_name, locator_type='xpath')
        test_data['activity_code'] = self.webDriver.get_text(element=self.locators.activity_code, locator_type='xpath')

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
        self.test_data['parent']['meetingStartTime'] = f"{meeting_start_time_hour * 60 + meeting_start_time_min} Min before"
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
        self.webDriver.set_text(element=self.locators.edit_activity_duration_hour, locator_type='xpath', text="2")
        self.webDriver.clear_text(element=self.locators.edit_activity_duration_min, locator_type='xpath',
                                  action_type='clear')
        self.webDriver.set_text(element=self.locators.edit_activity_duration_min, locator_type='xpath', text="2")

        self.webDriver.click(element=self.locators.update_location_time, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def edit_capacity(self):
        """
        Function to edit capacity of an activity
        :return:
        """
        self.webDriver.click(element=self.locators.edit_capacity_icon, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.edit_total_capacity, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.edit_total_capacity, locator_type='xpath', text="99999")
        self.webDriver.clear_text(element=self.locators.hold_capacity, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.hold_capacity, locator_type='xpath', text="50")
        self.webDriver.click(element=self.locators.update_capacity, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def edit_pricing(self):
        """
        Function to edit pricing of an activity
        :return:
        """
        self.webDriver.click(element=self.locators.edit_pricing_icon, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.selling_price, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.selling_price, locator_type='xpath', text="100")
        self.webDriver.click(element=self.locators.update_pricing, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def edit_other_info(self):
        """
        To edit other info on parent activity details page
        :return:
        """
        self.webDriver.click(element=self.locators.edit_other_info_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.edit_is_waiver_required, locator_type='xpath')
        self.webDriver.click(element=self.locators.update_other_info, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def verify_capacity_not_editable(self):
        """
        Function to verify that capacity is not editable
        :return:
        """
        self.webDriver.scroll_till_element(self.locators.organiser_title, 'xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.edit_capacity_icon,
                                                           locator_type='xpath'):
            logger.debug("Edit capacity icon is not present")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Edit capacity icon is present")

    def click_action_drop_down(self, option):
        """
        To click action drop down
        :param option:
        :return:
        """
        self.webDriver.scroll(0, 5000)
        element = self.webDriver.get_web_element(element=self.locators.action_drop_down, locator_type='xpath')
        size = element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_option_by_offset(element, x, y, option)

    def fill_complaint_details(self):
        """
        To fill complaint details
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        sailor_element = self.webDriver.get_web_element(element=self.locators.sailor_name, locator_type='xpath')
        size = sailor_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_by_offset(sailor_element, x, y)
        self.webDriver.click(element=self.locators.description, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def check_for_upcoming_slots_in_non_inventoried_activities(self):
        """
        check for upcoming slots to move to next day
        """
        for activities in self.test_data['nonInventoriedActivityNames']:
            self.webDriver.click(element=self.locators.activities, locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.click_on_slots_cta()
            slot_list = self.get_slot_list()
            for slots in slot_list:
                slot_columns = slots.text.split()
                current_date = datetime.today().date().strftime("%m/%d/%Y")
                if slot_columns[0] > current_date and slot_columns[5] == 'OPEN':
                    self.test_data['cancelSlotTime'] = slot_columns[1]
                    self.test_data['checkedIn'] = slot_columns[6]
                    self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                         locator_type="xpath")
                    self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                    time_out=60)
                    self.test_data['isSlotAvailable'] = True
                    return
                elif slot_columns[0] == current_date and slot_columns[1] > self.test_data['currentShipTime'] and \
                        slot_columns[5] == 'OPEN':
                    self.test_data['cancelSlotTime'] = slot_columns[1]
                    self.test_data['checkedIn'] = slot_columns[6]
                    self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                         locator_type="xpath")
                    self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                    time_out=60)
                    self.test_data['isSlotAvailable'] = True
                    return

        else:
            self.test_data['isSlotAvailable'] = False
            pytest.skip(msg="no upcoming slots available")

    def open_upcoming_child_slot(self):
        """
        Function to open available slot
        :return:
        """
        slot_list = self.get_slot_list()
        for slots in slot_list:
            slot_columns = slots.text.split()
            current_date = datetime.today().date().strftime("%m/%d/%Y")
            if slot_columns[0] > current_date and slot_columns[5] == 'OPEN':
                self.test_data['cancelSlotTime'] = slot_columns[1]
                self.test_data['checkedIn'] = slot_columns[6]
                self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                     locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                time_out=60)
                self.test_data['isSlotAvailable'] = True
                return
            elif slot_columns[0] == current_date and slot_columns[1] > self.test_data['currentShipTime'] and slot_columns[5] == 'OPEN':
                self.test_data['cancelSlotTime'] = slot_columns[1]
                self.test_data['checkedIn'] = slot_columns[6]
                self.webDriver.click(element=self.locators.selected_slot.format(slot_columns[0], slot_columns[5]),
                                     locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                time_out=60)
                self.test_data['isSlotAvailable'] = True
                return

    def verify_parent_activity_info(self):
        """
        To verify parent activity info is not changed
        :return:
        """
        assert self.test_data['parent']['totalAvailableCapacity'] != self.test_data['child']['totalAvailableCapacity'], \
            "Total available capacity is matching in both parent and child activity level "

    def find_spa_slot_booked_previously(self):
        """
        Function to find slot with same date and time as previosuly booked spa slot
        :return:
        """
        for activities in self.test_data['spaActivityNames']:
            self.webDriver.click(element=self.locators.activities, locator_type="xpath")
            self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            self.click_on_slots_cta()
            current_time = datetime.now().strftime("%H:%M")
            slot_list = self.get_slot_list()
            for slots in slot_list:
                slot_columns = slots.text.split()
                current_date = datetime.today().date().strftime("%m/%d/%Y")
                if slot_columns[0] > current_date:
                    if slot_columns[0] == self.test_data['bookedSpaActivityDate']:
                        if self.test_data['bookedSpaStartTime'] < slot_columns[1] < self.test_data['bookedSpaEndTime']:
                            self.webDriver.click(
                                element=self.locators.newly_created_slot.format(slot_columns[0], slot_columns[1]),
                                locator_type="xpath")
                            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                            time_out=60)
                            self.test_data['isSameSpaSlotAvailable'] = True
                            return
                        elif self.test_data['bookedSpaStartTime'] < slot_columns[3] < self.test_data['bookedSpaEndTime']:
                            self.webDriver.click(
                                element=self.locators.newly_created_slot.format(slot_columns[0], slot_columns[1]),
                                locator_type="xpath")
                            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                            time_out=60)
                            self.test_data['isSameSpaSlotAvailable'] = True
                            return
                    else:
                        self.test_data['isSameSpaSlotAvailable'] = False
                elif slot_columns[0] == current_date and slot_columns[1] > current_time:
                    if slot_columns[0] == self.test_data['bookedSpaActivityDate']:
                        if self.test_data['bookedSpaStartTime'] < slot_columns[1] < self.test_data['bookedSpaEndTime']:
                            self.webDriver.click(
                                element=self.locators.newly_created_slot.format(slot_columns[0], slot_columns[1]),
                                locator_type="xpath")
                            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                            time_out=60)
                            self.test_data['isSameSpaSlotAvailable'] = True
                            return
                        elif self.test_data['bookedSpaStartTime'] < slot_columns[3] < self.test_data['bookedSpaEndTime']:
                            self.webDriver.click(
                                element=self.locators.newly_created_slot.format(slot_columns[0], slot_columns[1]),
                                locator_type="xpath")
                            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                                            time_out=60)
                            self.test_data['isSameSpaSlotAvailable'] = True
                            return
                        else:
                            self.test_data['isSameSpaSlotAvailable'] = False
                            logger.debug("No similar spa slot available")
                else:
                    self.test_data['isSameSpaSlotAvailable'] = False

    def verify_activity_details_after_edit(self):
        """
        Function to verify activity details after editing
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.vendor_name, locator_type="xpath")
        assert self.webDriver.get_text(element=self.locators.vendor_name,locator_type="xpath") == self.test_data['vendorName'], 'Vendor name not matching after edit'
        self.webDriver.scroll_till_element(element=self.locators.transaction_type, locator_type="xpath")
        assert self.webDriver.get_text(element=self.locators.transaction_type,locator_type="xpath") == self.test_data['parent']['transactionType'], 'Transaction type not matching after edit'
        assert self.webDriver.get_text(element=self.locators.meeting_start_time,locator_type="xpath") == self.test_data['parent']['meetingStartTime'], 'Meeting start time not matching after edit'
        assert self.webDriver.get_text(element=self.locators.meeting_end_time, locator_type="xpath") == "61 Min before", 'Meeting end time not matching after edit'
        assert self.webDriver.get_text(element=self.locators.total_available_capacity, locator_type="xpath") == "99949", 'Total available capacity not matching after edit'
        assert self.webDriver.get_text(element=self.locators.save_slot_capacity,locator_type="xpath") == "99999", 'Slot capacity not matching after edit'
        assert self.webDriver.get_text(element=self.locators.save_hold_capacity,locator_type="xpath") == "50", 'Hold capacity not matching after edit'
        if self.test_data['parent']['isWaiverRequired'] == 'YES':
            assert self.webDriver.get_text(element=self.locators.is_waiver_required,locator_type="xpath") == 'NO'
        else:
            assert self.webDriver.get_text(element=self.locators.is_waiver_required, locator_type="xpath") == 'YES'
