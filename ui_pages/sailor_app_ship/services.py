__author__ = 'mohit.raghav'

from virgin_utils import *


class Services(General):
    """
    Page class for Services page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'ship_eats_delivery_btn': "//label[@id='foodBtn']",
            'cabin_services_btn': "//label[@id='cabinBtn']",
            'help_and_support': "//label[@id='supportBtn']",
            'services_header': "//h3[text()='Services']",
            'header_text': "//h1[text()='Hey Sailor, tell us how we can help you.']"
            })

    def verify_services_page(self):
        """
        to verify services page is getting displayed
        :param page:
        :param web_driver:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.services_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.header_text, locator_type='xpath'):
            logger.info("Services page is visible")
        else:
            raise Exception("Services page is not visible")

    def verify_cabin_services_btn_availability(self):
        """
        to verify cabin services button availability
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.services_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.cabin_services_btn,
                                                       locator_type='xpath'):
            logger.info("Cabin services btn is available on services page")
        else:
            raise Exception("Cabin services btn is not available on services page")

    def click_cabin_services_btn(self):
        """
        function to click on cabin services btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cabin_services_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.cabin_services_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.cabin_services_btn,
                                                               locator_type='xpath')

    def verify_help_and_support_btn_availability(self):
        """
        to verify help and support button availability
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.services_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.help_and_support,
                                                       locator_type='xpath'):
            logger.info("Help and support btn is available on services page")
        else:
            raise Exception("Help and support btn is not available on services page")

    def click_help_and_support_btn(self):
        """
        function to click on help and support btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.help_and_support,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.help_and_support, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.help_and_support,
                                                               locator_type='xpath')

    def verify_shipEats_delivery_btn_availability(self):
        """
        to verify ship eats delivery button availability
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.services_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_eats_delivery_btn,
                                                       locator_type='xpath'):
            logger.info("Ship eats delivery btn is available on services page")
        else:
            raise Exception("Ship eats delivery btn is not available on services page")

    def click_shipEats_delivery_btn(self):
        """
        function to click on ship eats delivery btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ship_eats_delivery_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_eats_delivery_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.ship_eats_delivery_btn,
                                                               locator_type='xpath')