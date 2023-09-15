__author__ = 'prahlad.sharma'

from virgin_utils import *
import datetime


class Boarding_slots(General):
    """
    Page Class for Sailor and Crew page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Boarding slots page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "table": "//tbody/tr",
            "header_name": "//thead/tr/th",
            "boarding_slot_header": "//div[@class='title']//span[contains(text(),'Boarding Slots')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "checkbox": "//span[@class='tick']/img[@class='SVGContainer ']",
            "column_value": "//tr[%s]//td[%s]",
            "column_values": "//tbody/tr/td[%s]",
            "click_boarding_slot": "//*[text()='%s']",
            "action_dd": "//span[contains(text(),'Actions')]",
            "add_slot": "ADD_SLOT",
            "slot_start_time": "endTime",
            "slot_end_time": "//div[@class='Timepicker timekeeper-cl']/input[@class='has-value']",
            "slot_end_time_icon": "//img[@class='SVGContainer calendar-icon']",
            "hour_selection": "//div[@class='react-timekeeper__clock-hours css-av1tj5']/span",
            "minutes_selection": "//div[@class='react-timekeeper__clock-minutes css-av1tj5']/span",
            "select_PM": "//button[contains(.,'PM')]",
            "select_AM": "//button[contains(.,'AM')]",
            "capacity": "capacity",
            "boardingNumber": "boardingNumber",
            "Add": "//button[contains(.,'Add')]",
            "value_from_particular_row_and_column": "//tbody/tr[%s]/td[%d]",
            "change_capacity": "CHANGE_CAPACITY",
            "capacity_update": "ageTo",
            "update": "//span[text()='Update']",
            'disable_slot': "DISABLE",
            "disable_button": "//button[text()='DISABLE']",
            "enable_slot": "ENABLE",
            "enable_button": "//button[text()='ENABLE']",
            "move_slot": "MOVE",
            "ahead_dd": "//span[text()='ahead']/../../following-sibling::div//*[@class='react-select__indicator "
                        "react-select__dropdown-indicator css-tlfecz-indicatorContainer']//*[local-name()='svg']",
            "move_button": "//span[text()='Move']",
            "mark_active": "//a[@name='MARK_ACTIVE']",
            "mark_inactive": "//a[@name='MARK_IN_ACTIVE']",
            "remove_slot": "REMOVE",
            "remove_button": "//button[text()='REMOVE']",
        })

    def verify_boarding_slot_page(self):
        """
        Function to verify boarding slot page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.boarding_slot_header,
                                                      locator_type='xpath',
                                                      time_out=60)
        screen_title = self.webDriver.get_text(element=self.locators.boarding_slot_header, locator_type='xpath')
        if screen_title == "Boarding Slots":
            logger.debug("User has opened boarding slot page of Embarkation Supervisor")
        else:
            raise Exception("User is not on boarding slot page of Embarkation Supervisor")

    def availability_of_boarding_data(self):
        """
        :return:
        """
        rows = self.webDriver.get_elements(element=self.locators.table, locator_type='xpath')
        if len(rows) > 0:
            logger.debug(f"Boarding slots available on page and count is: {len(rows)}")
        else:
            raise Exception("Boarding list is blank")

    def set_column_name(self, test_data):
        """
        Function to set the column name
        :param test_data:
        """
        column_number = 0
        total_column = self.webDriver.get_elements(element=self.locators.header_name, locator_type='xpath')
        for column in total_column:
            column_number = column_number + 1
            test_data[f"{column.text}_position"] = column_number

    def check_if_slot_can_be_added(self, test_data):
        """
         Function to check slot can be added or not
         :param test_data:
         :return:
         """
        rows = len(self.webDriver.get_elements(element=self.locators.checkbox, locator_type='xpath'))
        last_slot_value = self.webDriver.get_text(element=self.locators.column_value % (rows-1, 1),
                                                  locator_type='xpath')
        last_slot_assigned = int(
            self.webDriver.get_text(element=self.locators.column_value % (rows-1, test_data['Assigned_position']),
                                    locator_type='xpath'))
        slot_end_time = last_slot_value.split('-')[1]
        slot_end_hour = int(slot_end_time[0:2])
        slot_end_minute = int(slot_end_time[3:5])
        if slot_end_hour == 11 and slot_end_minute >= 45:
            if last_slot_assigned == 0:
                self.webDriver.click(element=self.locators.click_boarding_slot % last_slot_value,
                                     locator_type='xpath')
                self.click_action_dropdown()
                self.webDriver.click(element=self.locators.remove_slot, locator_type='name')
                self.webDriver.click(element=self.locators.remove_button, locator_type='xpath')
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                return True
            else:
                return False
        elif slot_end_hour == 11 and slot_end_minute >= 45:
            if last_slot_assigned > 0:
                return False
        else:
            return True


    def click_action_dropdown(self):
        """
        Click on Action drop down
        :return:
        """
        self.webDriver.click(element=self.locators.action_dd, locator_type='xpath')
        self.webDriver.wait_for(1)

    def add_new_slot(self, test_data):
        """
        Click on add Slot
        :param test_data:
        :return:
        """
        count = 1
        self.webDriver.click(element=self.locators.add_slot, locator_type='name')
        start_slot_time = self.webDriver.get_value_from_textbox(element=self.locators.slot_start_time,
                                                                locator_type='name')
        datetime_object = datetime.datetime.strptime(start_slot_time, '%I:%M%p')
        now_plus_15m = datetime_object + datetime.timedelta(minutes=15)
        new_time = str(now_plus_15m.strftime("%I:%M%p"))
        end_time = str(int(new_time.split(':')[0]))
        minute = str(int(new_time.split(':')[1][0:2]))
        self.webDriver.click(element=self.locators.Add, locator_type='xpath')
        self.webDriver.click(element=self.locators.slot_end_time_icon, locator_type='xpath')
        hours_count = self.webDriver.get_elements(element=self.locators.hour_selection, locator_type='xpath')
        self.webDriver.wait_for(1)
        for hour in hours_count:
            if hour.text == end_time:
                self.webDriver.move_to_element_and_click_without_type(hour)
                break
        self.webDriver.wait_for(5)
        minutes_count = self.webDriver.get_elements(element=self.locators.minutes_selection, locator_type='xpath')
        for minutes in minutes_count:
            if minutes.text >= minute:
                self.webDriver.move_to_element_and_click_without_type(minutes)
                break
        if 'am' in start_slot_time.split(":")[1]:
            self.webDriver.click(element=self.locators.select_AM, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.select_PM, locator_type='xpath')
        slot_start_time = datetime_object.strftime('%I:%M:%S %p')
        slot_end_time = self.webDriver.get_value_from_textbox(element=self.locators.slot_end_time,
                                                              locator_type='xpath')
        datetime_object = datetime.datetime.strptime(slot_end_time, '%I:%M%p')
        slot_end_time = datetime_object.strftime('%I:%M:%S %p')
        self.webDriver.set_text(element=self.locators.capacity, locator_type='name', text='10')
        boarding_slot = f"{slot_start_time}-{slot_end_time}"
        self.webDriver.click(element=self.locators.Add, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg("added_slot")
        self.set_column_name(test_data)
        get_all_boarding_slots = self.webDriver.get_elements(
            element=self.locators.column_values % test_data['Boarding Slot_position'], locator_type='xpath')
        for slots in get_all_boarding_slots:
            if slots.text == boarding_slot:
                return self.webDriver.get_text(
                    element=self.locators.value_from_particular_row_and_column % (count, test_data['Boarding '
                                                                                                   'Slot_position']),
                    locator_type='xpath')
            count = count + 1

    def click_checkbox(self, test_data):
        """
        Function is used to tick the check box
        :param test_data:
        """
        all_checkbox = self.webDriver.get_elements(element=self.locators.checkbox, locator_type='xpath')
        for check in all_checkbox:
            test_data['boarding_slot_text'] = self.webDriver.get_text(
                element=self.locators.column_value % (1, test_data['Boarding Slot_position']),
                locator_type='xpath')
            check.click()
            break
        self.webDriver.allure_attach_jpeg('check_box_selected')

    def update_capacity(self, test_data):
        """
        Function to update the capacity
        :param test_data:
        :return:
        """
        self.webDriver.scroll_complete_page()
        count = 0
        self.webDriver.click(element=self.locators.click_boarding_slot % test_data["added_slot_value"],
                             locator_type='xpath')
        self.click_action_dropdown()
        self.webDriver.click(element=self.locators.change_capacity, locator_type='name')
        self.webDriver.set_text(element=self.locators.capacity_update, locator_type='name', text='20')
        self.webDriver.click(element=self.locators.update, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        get_all_boarding_slots = self.webDriver.get_elements(
            element=self.locators.column_values % test_data['Boarding Slot_position'], locator_type='xpath')
        for slots in get_all_boarding_slots:
            count = count + 1
            if slots.text == test_data["added_slot_value"]:
                break

        return self.webDriver.get_text(
            element=self.locators.value_from_particular_row_and_column % (count, test_data['Capacity_position']),
            locator_type='xpath')

    def enable_disable_slot(self, test_data, status):
        """
        Function to enable or disable the slot
        :param test_data:
        :param status:
        :return:
        """
        count = 0
        self.webDriver.click(element=self.locators.click_boarding_slot % test_data["added_slot_value"],
                             locator_type='xpath')
        self.click_action_dropdown()
        if status:
            self.webDriver.click(element=self.locators.enable_slot, locator_type='name')
            self.webDriver.click(element=self.locators.enable_button, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.disable_slot, locator_type='name')
            self.webDriver.click(element=self.locators.disable_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg("enable disable sot")
        get_all_boarding_slots = self.webDriver.get_elements(
            element=self.locators.column_values % test_data['Boarding Slot_position'], locator_type='xpath')
        for number in get_all_boarding_slots:
            count = count + 1
            if number.text == test_data["added_slot_value"]:
                break
        test_data['count'] = count
        return self.webDriver.get_text(
            element=self.locators.value_from_particular_row_and_column % (count, test_data['Enabled_position']),
            locator_type='xpath')

    def move_slot(self, test_data):
        """
        Function to move the slot
        :param test_data:
        """
        boarding_slot_values = []
        flag = 0
        rows = self.webDriver.get_elements(element=self.locators.table, locator_type='xpath')
        for i in range(2, len(rows)):
            slot_value = self.webDriver.get_text(element=self.locators.column_value % (i, test_data['Boarding Slot_position']),  locator_type='xpath')
            boarding_slot_values.append(slot_value)
        self.click_action_dropdown()
        self.webDriver.click(element=self.locators.move_slot, locator_type='name')
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.ahead_dd, locator_type='xpath',
                                                          text='ahead')
        self.webDriver.click(element=self.locators.move_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        moved_boarding_slot_values = []
        for i in range(2, len(rows)):
            moved_slot_value = self.webDriver.get_text(element=self.locators.column_value % (i, test_data['Boarding Slot_position']), locator_type='xpath')
            moved_boarding_slot_values.append(moved_slot_value)

        for i in range(0,len(rows)-2):
            slot_value = boarding_slot_values[i]
            start_time = slot_value.split("-")[0]
            end_time = slot_value.split("-")[1]
            start_datetime_object = datetime.datetime.strptime(start_time, '%I:%M:%S %p')
            end_datetime_object = datetime.datetime.strptime(end_time, '%I:%M:%S %p')
            start_plus_15m = start_datetime_object + datetime.timedelta(minutes=15)
            end_plus_15m = end_datetime_object + datetime.timedelta(minutes=15)
            moved_start_time = str(start_plus_15m.strftime('%I:%M:%S %p'))
            moved_end_time = str(end_plus_15m.strftime("%I:%M:%S %p"))
            moved_slot_value = f"{moved_start_time}-{moved_end_time}"
            if moved_boarding_slot_values[i] == moved_slot_value:
                flag = 0
            else:
                flag = 1

        if flag == 0:
            logger.debug("All boarding slots have been moved by 15 mins")
        else:
            raise Exception("All boarding slots are not moved by 15 mins")

        self.click_action_dropdown()
        self.webDriver.click(element=self.locators.move_slot, locator_type='name')
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.ahead_dd, locator_type='xpath',
                                                          text='behind')
        self.webDriver.click(element=self.locators.move_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def remove_slot(self, test_data):
        """
        Function to remove the slot
        :param test_data:
        :return:
        """
        flag = True

        self.webDriver.click(element=self.locators.click_boarding_slot % test_data["added_slot_value"],
                             locator_type='xpath')
        self.click_action_dropdown()
        self.webDriver.click(element=self.locators.remove_slot, locator_type='name')
        self.webDriver.click(element=self.locators.remove_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        get_all_boarding_slots = self.webDriver.get_elements(
            element=self.locators.column_values % test_data['Boarding Slot_position'], locator_type='xpath')
        for slots in get_all_boarding_slots:
            if slots.text == test_data["added_slot_value"]:
                flag = False
        return flag

    def active_boarding_slot(self):
        """
        Function to mark a boarding slot as active
        """
        self.webDriver.click(element=self.locators.action_dd, locator_type='xpath')
        self.webDriver.click(element=self.locators.mark_active, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('mark_active_boarding_slot')

    def inactive_boarding_slot(self):
        """
        Function to mark a boarding slot as inactive
        """
        self.webDriver.click(element=self.locators.action_dd, locator_type='xpath')
        self.webDriver.click(element=self.locators.mark_inactive, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('mark_inactive_boarding_slot')

    def verify_inactive_boarding_slot(self, test_data):
        """
        Function to verify inactive boarding slot
        """
        slot_inactive_text = self.webDriver.get_text(
            element=self.locators.column_value % (1, test_data['Boarding Status_position']),
            locator_type='xpath')
        assert slot_inactive_text == 'In-Active', "Slot is still active"
        self.webDriver.allure_attach_jpeg('Verify_inactive_slot')

    def verify_active_boarding_slot(self, test_data):
        """
        Function to verify active boarding slot
        """
        slot_inactive_text = self.webDriver.get_text(
            element=self.locators.column_value % (1, test_data['Boarding Status_position']),
            locator_type='xpath')
        assert slot_inactive_text == 'Active', "Slot is still In-active"
        self.webDriver.allure_attach_jpeg('Verify_active_slot')
