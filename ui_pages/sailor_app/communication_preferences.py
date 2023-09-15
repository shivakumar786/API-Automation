__author__ = 'vanshika.arora'

from virgin_utils import *


class communication_Preferences(General):
    """
    Page class for communication preferences screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "communication_preferences": "//h1[text()='Communication preferences']",
            "virgin_voyages_news": "//input[@id='menu_checkbox_no']",
            "partner_offers": "//input[@id='menu_checkbox_po']",
            "submit_button": "//button[@id='btn-submit']",
            })

    def verify_communication_preferences_page_landing(self):
        """
        Function to verify that user has landed on communcation preferences screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.communication_preferences,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on communication preferences screen")
        else:
            raise Exception("Sailor has not landed on communication preferences screen")

    def check_all_communication_preferences(self):
        """
        Function to check all communication preferences
        :return:
        """
        self.webDriver.click(element=self.locators.virgin_voyages_news, locator_type='xpath')
        self.webDriver.click(element=self.locators.partner_offers, locator_type='xpath')

    def click_submit_button(self):
        """
        Function to click submit button
        :return:
        """
        if self.webDriver.is_element_enabled(element=self.locators.submit_button, locator_type='id'):
            logger.debug("Communication preferences update button is enabled after updating preferences")
            self.webDriver.click(element=self.locators.submit_button, locator_type='xpath')
        else:
            logger.debug("Communication preferences update button is disabled after updating preferences")

    def verify_communication_preferences_checked(self):
        """
        Function to verify that communcation preferences are shown checked when checked by sailor
        :return:
        """




