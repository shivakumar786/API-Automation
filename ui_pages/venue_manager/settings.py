__author__ = 'HT'

import time

from selenium.webdriver.common.keys import Keys

from virgin_utils import *


class Settings(General):
    """
    Page Class for Venue Manager venue selection
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager settings page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "venue_details": "venueDetails",
            "voyage_details": "voyage-details",
            "no_data_available": "//*[text()='NO DATA AVAILABLE.']",
            "venue_details_col": "//*[@id='orderStatusReport']/tbody/tr[1]/td",
            "pre_order_breakfast": "preOrderBreakFast",
            "filter_by_date": "voyage-itineraries",
            "filter_by_date_operational_hours": "custom-dropdown-style-filterdate",
            "edit_settings": "edit-preorders-settings",
            "pull_from_template": "pull-template",
            "availability_toggle": "Availability0",
            "toggle_btn_status": "AvailabilityHidden0",
            "add_new_time_slot": "//*[contains(text(),'Add New Time Slot')]",
            "from_time": "fromTime",
            "new_slot": "(//*[@id='fromTime'])[%s]",
            "to_time": "toTime",
            "ordinary_inventory": "(//*[@class='inventry-sxn']/input)[%s]",
            "order_period_start_date": "custom-dropdown-style-orderperiod-0",
            "order_period_end_date": "custom-dropdown-style-orderperiodend-0",
            "cut_off_date": "custom-dropdown-style-cutoffdate-0",
            "save": "save-preorders",
            "delete_delivery_slot": "//*[@class='minus-click do-nothing']",
            "delivery_time_slot": "//*[contains(text(),'Delivery Timeslots')]",
            "order_period": "//*[contains(text(),'Order Period')]",
            "edit_cut_off": "//*[contains(text(),'Edit Cutoff')]",
            "meal_period": "//*[text()='Operational Hours & Meal Period']",
            "meal_period_filter": "filterByDate",
            "operational_hours": "//*[@class='opr-hour-sxn']/div",
            "meal_period_capacity": "//*[@class='meal-period-main col-md-12']/div",
            "update": "btnUpdateMealPeriod",
            "voyage_filter_icon": "update-icon",
            "voyage_list": "listVoyage",
            "future_voyage": "(//*[@class='custom-options'])[4]",
            "date_elements": "//*[@id='filterByDate']/../div/div[@class='custom-options']",
            "voyage_drop_down": "custom-dropdown-style-preorder",
            "pull_template_btn": "pull-template",
            "template_list": "//*[@class='template-item']",
            "apply_template": "savePullfromTemplate",
            "error_popup": "//*[@id='errorException']/span[2]",
            "ok_btn": "//*[text()='OK']",
            "cancel": "close-it-template",
            "no_meal_period": "//*[text()='No Meal Period Available']"
        })

    def click_on_venue_details(self):
        """
        Click on venue details page
        :return:
        """
        self.webDriver.click(element=self.locators.venue_details, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def click_on_operational_hour_meal_period(self):
        """
        To click on operational hours and meal period
        :return:
        """
        self.webDriver.click(element=self.locators.meal_period, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def verify_columns_in_venue_details_tab(self):
        """
        Get venue manager login page header
        """
        col_length = len(self.webDriver.get_elements(element=self.locators.venue_details_col, locator_type="xpath"))
        assert col_length >= 4, "All columns are not displayed in venue details page"

    def no_data_found(self):
        """
        Check for no records found message
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_data_available,
                                                           locator_type="xpath")

    def click_on_preorder_breakfast(self):
        """
        To select current sailing from filer
        :return:
        """
        self.webDriver.click(element=self.locators.pre_order_breakfast, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def create_new_delivery_period(self):
        """
        This func is to create new delivery period time slot
        :return:
        """
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        availability_status = self.webDriver.get_attribute(element=self.locators.toggle_btn_status, locator_type="id",
                                                           attribute_name="value")
        if not availability_status:
            self.webDriver.click(element=self.locators.availability_toggle, locator_type="id")
        self.webDriver.click(element=self.locators.add_new_time_slot, locator_type="xpath")
        total_slots = len(self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        self.webDriver.click(element=self.locators.new_slot % total_slots, locator_type="xpath")
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
        self.webDriver.clear_text(element=self.locators.ordinary_inventory % total_slots, locator_type="xpath",
                                  action_type="clear")
        self.webDriver.set_text(element=self.locators.ordinary_inventory % total_slots, locator_type="xpath", text=10)
        self.webDriver.click(element=self.locators.order_period_start_date, locator_type="id")
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
        self.webDriver.click(element=self.locators.order_period_end_date, locator_type="id")
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
        self.webDriver.click(element=self.locators.cut_off_date, locator_type="id")
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
        self.webDriver.click(element=self.locators.save, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        total_slots_after_creating = len(
            self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        assert total_slots_after_creating == total_slots, "Delivery time slot not created successfully"
        self.webDriver.click(element=self.locators.delete_delivery_slot, locator_type="xpath")

    def to_verify_preorder_breakfast_settings_for_current_sailing(self):
        """
        This is to verify preorder breakfast for current sailing
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_details, locator_type="id"):
            raise Exception("current sailing voyage details are not showing up in preorder breakfast settings screen")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.edit_settings, locator_type="id"):
            raise Exception("current sailing edit settings is not showing up in preorder breakfast settings screen")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_by_date, locator_type="id"):
            raise Exception("filter by date drop down button is not showing up in preorder breakfast settings screen")
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.availability_toggle,
                                                           locator_type="id"):
            raise Exception("availability toggle button is not showing up in preorder breakfast settings screen")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.pull_from_template, locator_type="id"):
            raise Exception("pull from template button is not showing up in preorder breakfast settings screen")
        delivery_time_slot = self.webDriver.get_text(element=self.locators.delivery_time_slot, locator_type="xpath")
        assert delivery_time_slot == "Delivery Timeslots*", "delivery time slot is not showing up in preorder breakfast settings screen"
        order_period = self.webDriver.get_text(element=self.locators.order_period, locator_type="xpath")
        assert order_period == "Order Period*", "order period is not showing up in preorder breakfast settings screen"
        edit_cut_off = self.webDriver.get_text(element=self.locators.edit_cut_off, locator_type="xpath")
        assert edit_cut_off == "Edit Cutoff*", "edit cut off is not showing up in preorder breakfast settings screen"

    def to_verify_user_is_able_to_see_operational_hour_and_meal_period(self):
        """
        This is to verify user is able to see operational hour's and able to see meal period
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_details, locator_type="id"):
            raise Exception("current sailing voyage details are not showing up in preorder breakfast settings screen")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.meal_period_filter, locator_type="id"):
            raise Exception("meal period filter is not showing up in meal period tab")
        operational_hours = len(
            self.webDriver.get_elements(element=self.locators.operational_hours, locator_type="xpath"))
        assert operational_hours > 0, "Operational hours is not showing in settings meal period tab"
        meal_period_capacity = len(
            self.webDriver.get_elements(element=self.locators.meal_period_capacity, locator_type="xpath"))
        assert meal_period_capacity > 0, "Meal period is not showing up in meal period tab"
        if not self.webDriver.is_element_display_on_screen(element=self.locators.update, locator_type="id"):
            raise Exception("update button is not showing up in meal period tab in settings")

    def to_create_preorder_breakfast_using_template_for_current_date(self):
        """
        To create preorder breakfast using existing template
        :return:
        """
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        self.webDriver.click(element=self.locators.pull_template_btn, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        templates = self.webDriver.get_elements(element=self.locators.template_list, locator_type="xpath")
        for template in templates:
            template.click()
            break
        self.webDriver.click(element=self.locators.apply_template, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.ok_btn, locator_type='xpath'):
            self.webDriver.click(element=self.locators.ok_btn, locator_type='xpath')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            self.webDriver.click(element=self.locators.cancel, locator_type='id')
            pytest.skip(msg="Can not update Slot time which already have pre-order breakfast Booked.")
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        self.webDriver.click(element=self.locators.save, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        total_slots_after_creating = len(
            self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        assert total_slots_after_creating > 0, "current day preorder not created successfully"

    def to_create_preorder_breakfast_using_template_for_future_voyage(self):
        """
        To create preorder breakfast using existing template
        :return:
        """
        self.webDriver.click(element=self.locators.voyage_filter_icon, locator_type="id")
        self.webDriver.click(element=self.locators.voyage_drop_down, locator_type="id")
        self.webDriver.click(element=self.locators.future_voyage, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        self.webDriver.click(element=self.locators.filter_by_date, locator_type="id")
        dates = self.webDriver.get_elements(element=self.locators.date_elements, locator_type="xpath")
        for select_date in dates:
            element = select_date.text
            if element != '-Select-':
                select_date.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                break
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        self.webDriver.click(element=self.locators.pull_template_btn, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        templates = self.webDriver.get_elements(element=self.locators.template_list, locator_type="xpath")
        for template in templates:
            template.click()
            break
        self.webDriver.click(element=self.locators.apply_template, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.ok_btn, locator_type='xpath'):
            self.webDriver.click(element=self.locators.ok_btn, locator_type='xpath')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            self.webDriver.click(element=self.locators.cancel, locator_type='id')
            pytest.skip(msg="Can not update Slot time which already have pre-order breakfast Booked.")
        self.webDriver.click(element=self.locators.edit_settings, locator_type="id")
        self.webDriver.click(element=self.locators.save, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        total_slots_after_creating = len(
            self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        assert total_slots_after_creating > 0, "future voyage preorder not created successfully"

    def is_meal_period_and_capacity(self):
        """
        To check for any meal period and capacity available
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_meal_period, locator_type='xpath')

    def filter_pre_order_breakfast_with_date(self):
        """
        To filter for preorder breakfast with date
        :return:
        """
        self.webDriver.click(element=self.locators.filter_by_date, locator_type="id")
        dates = self.webDriver.get_elements(element=self.locators.date_elements, locator_type="xpath")
        for select_date in dates:
            element = select_date.text
            if element != '-Select-':
                select_date.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                break
        total_slots_after_creating = len(
            self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        if not total_slots_after_creating > 0:
            logger.info("no pre order breakfast slots for selected date")

    def filter_for_operational_hours_and_meal_period_by_date(self):
        """
        To filter for operational hours and meal period by date
        :return:
        """
        self.webDriver.click(element=self.locators.filter_by_date_operational_hours, locator_type="id")
        dates = self.webDriver.get_elements(element=self.locators.date_elements, locator_type="xpath")
        for select_date in dates:
            element = select_date.text
            if element != '-Select-':
                select_date.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                break
        total_slots_after_creating = len(
            self.webDriver.get_elements(element=self.locators.from_time, locator_type="id"))
        if not total_slots_after_creating > 0:
            logger.info("no pre order breakfast slots for selected date")