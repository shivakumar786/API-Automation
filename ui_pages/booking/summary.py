__author__ = 'sarvesh.singh'

from virgin_utils import *


class Summary:
    """
    Page class for Summary Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        self.webDriver = web_driver
        self.locators = {
            "checkout": "//button[@id='PriceBreakdownCheckout']"
        }

    def checkout_summary(self):
        """
        To open account dropdown
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators['checkout'], locator_type='xpath')
        self.webDriver.wait_for(seconds=5)
