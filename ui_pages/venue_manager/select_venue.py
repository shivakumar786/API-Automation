__author__ = 'HT'

from virgin_utils import *


class SelectVenue(General):
    """
    Page Class for Venue Manager venue selection
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "qsr_venues": "(//*[text()='QSR'])[1]",
            "bell_box_venue": "(//*[text()='Bell Box'])[1]",
            "qsr_venue": "//*[text()='%s']",
            "continue_btn": "btn-select-venue",
            "set_default": "//*[contains(text(),'Set as default')]"
        })

    def click_on_qsr_tab(self):
        """
        Get venue manager login page header
        """
        self.webDriver.click(element=self.locators.qsr_venues, locator_type="xpath")

    def select_venue(self, venue_name):
        """
        To select venue
        :param venue_name:
        """
        self.webDriver.click(element=self.locators.qsr_venue % venue_name, locator_type="xpath")
        self.webDriver.click(element=self.locators.continue_btn, locator_type="id")

    def select_venue_and_set_as_default(self, venue_name):
        """
        to verify user is able to select set as default button
        :return:
        """
        self.webDriver.click(element=self.locators.qsr_venue % venue_name, locator_type="xpath")
        self.webDriver.click(element=self.locators.set_default, locator_type="xpath")
        self.webDriver.click(element=self.locators.continue_btn, locator_type="id")
