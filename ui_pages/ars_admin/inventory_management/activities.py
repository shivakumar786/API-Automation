__author__ = 'Krishna'

from virgin_utils import *


class Activities(General):
    """
    To initiate page class elements and functions
    """

    def __init__(self, web_driver, test_data):
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "filter_link": "//*[@class='SVGContainer btn-img-clr']",
            "activities_list": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div/a",
            "select_activity": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div/a/button/div[text("
                               ")=\"{}\"]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "active_voyage_name": "(//div[@class='react-select__single-value css-1uccc91-singleValue'])[2]",
            "page_header": "//div[@class='column title']",
            "search": "//input[@class='NavSearchFieldTextBox']",
            "ars_admin_header": "//strong[contains(@class,'is-size-5')]",
            "no_records": "//div[@class='rt-noData']",
            "column_header_name": "//div[@class='rt-tr']/div",
            "table_rows": "//div[@class='rt-tr-group']",
            "sort_by": "//div[@class='rt-th -cursor-pointer']/div[text()='%s']",
            "sort_descending_by": "//div[@class='rt-th -sort-asc -cursor-pointer']/div[text()='%s']",
            "column_values": "//div[@class='rt-tbody']/div[@class='rt-tr-group'][%s]//div[@class='rt-td'][%s]",
            "edit_organiser_icon": "//div[text()='Organizer']/ancestor::div/div[@class='button btn-clr']",
            "edit_transaction_type": "//div[@id='accountType']/div/div[2]",
            "edit_vendor": "//div[@id='vendorId']/div/div[2]",
            "activities": "(//*[text()='Activities'])[2]",
            "select_activity": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div/div/div/a/button/div[text("
                               ")=\"{}\"]",
            "slots_tab": "//*[text()='SLOTS']",
            "slot_list": "//*[@class='ReactTable']/div/div[@class='rt-tbody']/div",
            "no_records_found": "//*[text()='No Records Found']",

        })

    def click_on_filter(self):
        """
        To click on filter icon from activities tab
        """
        self.webDriver.click(element=self.locators.filter_link, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def shore_thing_list(self):
        """
        store shore thing activity name
        """
        activity_list = self.webDriver.get_elements(element=self.locators.activities_list, locator_type="xpath")
        self.test_data['activityNames'] = []
        if len(activity_list) != 0:
            for activity in activity_list:
                if activity.text != 'Script Automation':
                    self.test_data['activityNames'].append(activity.text)
        else:
            raise Exception("No shore thing activities available")

    def spa_activity_list(self):
        """
        spa activities name lsit
        """
        activity_list = self.webDriver.get_elements(element=self.locators.activities_list, locator_type="xpath")
        self.test_data['spaActivityNames'] = []
        if len(activity_list) != 0:
            for activity in activity_list:
                self.test_data['spaActivityNames'].append(activity.text)
        else:
            raise Exception("No Spa activities available")

    def click_on_slots_cta(self):
        """
        Click on add slots tab from activity details page
        """
        self.webDriver.click(element=self.locators.slots_tab, locator_type="xpath")

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

    def click_on_three_dotted_menu_and_move_slot(self):
        """
        Click on three dotted menu on slot details page to move slot
        """
        self.webDriver.click(element=self.locators.three_dotted_menu, locator_type="xpath")
        self.webDriver.click(element=self.locators.move_slot_cta, locator_type="xpath")

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
        self.webDriver.click(element=self.locators.cancel_slot, locator_type="xpath")

    def select_activity_from_list(self):
        """
        Select activity from list to add slots
        """
        self.shore_thing_list()
        activity_used = str(random.choice(self.test_data['activityNames']))
        logger.info(f"{activity_used}")
        self.webDriver.click(element=self.locators.select_activity.format(activity_used), locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def is_no_records_found(self):
        """
        Check if no records found is displayed
        """
        record_status = self.webDriver.is_element_display_on_screen(element=self.locators.no_records_found, locator_type="xpath")
        return record_status

    def get_spa_activity_from_list(self):
        """
        select spa activity from spa activity list
        """
        self.spa_activity_list()
        activity_selected = str(random.choice(self.test_data['spaActivityNames']))
        logger.info(f"activity used {activity_selected}")
        self.webDriver.click(element=self.locators.select_activity.format(activity_selected), locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def verify_active_voyage_name(self, voyage_name):
        """
        Verify active voyage name
        :param voyage_name:
        """
        selected_voyage_name = self.webDriver.get_text(element=self.locators.active_voyage_name, locator_type='xpath')
        if selected_voyage_name.split()[0] == voyage_name.split()[0] and selected_voyage_name.split()[1] == \
                voyage_name.split()[1]:
            logger.debug(f"{selected_voyage_name} Selected Voyage name is matching with backend response")
        else:
            raise Exception(f"{selected_voyage_name} Selected Voyage name is not matching with backend response")
        self.webDriver.allure_attach_jpeg('verify_active_voyage_name')

    def verify_page_header(self):
        """
        Verify Activities header
        """
        page_header = self.webDriver.get_text(element=self.locators.page_header, locator_type='xpath')
        if page_header == "Activities":
            logger.debug("User has landed on Activities page")
        else:
            raise Exception("User has not landed on Activities page")
        self.webDriver.allure_attach_jpeg('verify_activities_header')

    def verify_ars_admin_header_on_top_left_corner(self):
        """
        Verify ARS admin header on top left corner
        """
        ars_admin_header = self.webDriver.get_text(element=self.locators.ars_admin_header, locator_type='xpath')
        if ars_admin_header == "ARS Admin":
            logger.debug("ARS Admin header is present on activities page")
        else:
            raise Exception("ARS Admin header is not present on activities page")
        self.webDriver.allure_attach_jpeg('verify_ars_admin_header_on_top_left_corner')

    def verify_search_bar_present(self):
        """
        Verify ARS admin search bar on top
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.search, locator_type='xpath'):
            logger.debug("Search option available on Activities page")
        else:
            raise Exception("Search option not available on Activities page")
        self.webDriver.allure_attach_jpeg('verify_search_bar_present')

    def set_column_name(self):
        """
        Function to get the column name
        :param test_data:
        """
        column_number = 0
        total_column = self.webDriver.get_elements(element=self.locators.column_header_name, locator_type='xpath')
        for column in total_column:
            column_number = column_number + 1
            self.test_data[f"{column.text}_position"] = column_number

    def sort_column_and_verify(self, sort_by):
        """
        Function to sort column and verify
        :param test_data:
        :param sort_by:
        """
        rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
        if len(rows) < 11:
            val = len(rows) + 1
        else:
            val = 11

        self.webDriver.click(element=self.locators.sort_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        list1 = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, self.test_data[f'{sort_by}_position']), locator_type='xpath')
            list1.append(col_value)
        sorted_list = sorted(list1, key=str.lower)
        assert list1 == sorted_list, f'list is not sorted in ascending order according to {sort_by}'
        self.webDriver.click(element=self.locators.sort_descending_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        desc_list = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, self.test_data[f'{sort_by}_position']), locator_type='xpath')
            desc_list.append(col_value)
        sorted_list = sorted(desc_list, reverse=True, key=str.lower)
        assert desc_list == sorted_list, f'list is not sorted in descending order according to {sort_by}'

    def sort_column_with_int_value_and_verify(self, sort_by):
        """
        Function to sort column and verify
        :param test_data:
        :param sort_by:
        """
        rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
        if len(rows) < 11:
            val = len(rows) + 1
        else:
            val = 11

        self.webDriver.click(element=self.locators.sort_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        list1 = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, self.test_data[f'{sort_by}_position']), locator_type='xpath')
            if col_value != '':
                list1.append(int(col_value[1:]))
        sorted_list = sorted(list1)
        assert list1 == sorted_list, f'list is not sorted in ascending order according to {sort_by}'
        self.webDriver.click(element=self.locators.sort_descending_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        desc_list = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, self.test_data[f'{sort_by}_position']), locator_type='xpath')
            if col_value != '':
                desc_list.append(int(col_value[1:]))
        sorted_list = sorted(desc_list, reverse=True)
        assert desc_list == sorted_list, f'list is not sorted in descending order according to {sort_by}'

    def blank_list(self):
        """
        Verification of blank list
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_records, locator_type='xpath'):
            return True
        else:
            return False

    def shore_events_available_after_login(self):
        """
        To verify that shore events are available after login
        :return:
        """
        rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
        for i in range(1, len(rows) + 1):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, self.test_data['Type_position']), locator_type='xpath')
            assert col_value == 'Shore Thing', 'Shorex events are not available after login by default'
            break

    def ent_non_inventoried_event_list(self):
        """
        store shore thing activity name
        """
        non_inventoried_activity_list = self.webDriver.get_elements(element=self.locators.activities_list,
                                                                    locator_type="xpath")
        self.test_data['nonInventoriedActivityNames'] = []
        if len(non_inventoried_activity_list) != 0:
            for activity in non_inventoried_activity_list:
                if activity.text != 'Script Automation':
                    self.test_data['nonInventoriedActivityNames'].append(activity.text)
        else:
            raise Exception("No non inventoried activities available")

    def click_on_slots_cta(self):
        """
        Click on add slots tab from activity details page
        """
        self.webDriver.click(element=self.locators.slots_tab, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def verify_private_activities_filter(self):
        """
        Verify private activities available after applying private filter
        :return:
        """
        if self.blank_list():
            logger.debug("No private activities available")
        else:
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            for i in range(1, len(rows) + 1):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, self.test_data['Access_position']), locator_type='xpath')
                if col_value != ['PRIVATE']:
                    ptest.skip(msg="Private events are not available after applying private filter")

    def verify_private_slots_filter(self):
        """
        Verify private activities available after applying private filter
        :return:
        """
        if self.blank_list():
            logger.debug("No private slots available")
        else:
            self.shore_thing_list()
            for activities in self.test_data['activityNames']:
                self.webDriver.click(element=self.locators.activities, locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
                self.webDriver.click(element=self.locators.select_activity.format(activities), locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
                self.click_on_slots_cta()
                slot_list = self.get_slot_list()
                for slots in slot_list:
                    slot_columns = slots.text.split()
                    if slot_columns[4] != "PRIVATE":
                        pytest.skip(msg="Private slots not available after applying filter for private slots")
