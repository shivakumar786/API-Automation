__author__ = 'vanshika.arora'

from virgin_utils import *


class Services(General):
    """
    Page class for Login page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "ship_eats_delivery": "//span[text()='Ship Eats Delivery']",
            "services_header": "//h3[@class='ServicesModule__title-eyebrow']",
            "cabin_services": "//span[text()='Cabin services']",
            "make_your_cabin": "//div[@text='Making your cabin... ']",
            "help_and_support": "//span[@text='Help & support']",
        })

    def verify_services_header(self):
        """
        Verify header of services section
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.services_header, locator_type='xpath'):
            logger.debug("User has landed on services screen")
        else:
            raise Exception("User is not on Services Screen")

    def open_ship_eats(self):
        """
        Function to open ship eats
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.ship_eats_delivery, locator_type='xpath')

    def open_cabin_services(self):
        """
        Function to open cabin services
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.cabin_services, locator_type='xpath')

    def open_help_and_support(self):
        """
        Function to open Help And Support Page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.help_and_support, locator_type='xpath')
