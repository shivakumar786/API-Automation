__author__ = 'HT'

from virgin_utils import *


class Staff(General):
    """
    Page Class for Venue Manager venue selection
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager staff page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "on_duty_staff": "onDutyStaff",
            "off_duty_staff": "offDutyStaff",
            "all_staff": "allStaff",
            "search_button": "orderSearchButton",
            "search_box_name": "txtSearchBox",
            "no_records_found": "//*[text()='No record found.']"
        })

    def verify_elements_in_staff_tab(self):
        """
        Get venue manager login page header
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.all_staff, locator_type="id"):
            raise Exception("All tab not displayed")

        if not self.webDriver.is_element_display_on_screen(element=self.locators.on_duty_staff, locator_type="id"):
            raise Exception("on duty tab not displayed")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.off_duty_staff, locator_type="id"):
            raise Exception("off duty tab not displayed")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_button, locator_type="id"):
            raise Exception("search button not displayed on UI")
        place_holder = self.webDriver.get_attribute(element=self.locators.search_box_name, locator_type="id",
                                                    attribute_name="placeholder")

        assert place_holder == "Search By Name", "place holder name not matching with expected"

    def no_records_found(self):
        """
        Check for no records found message
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_records_found, locator_type="xpath")
