__author__ = 'mohit.raghav'

from virgin_utils import *


class Cabin_services(General):
    """
    Page class for cabin services page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "cabin_services_header": "//*[text()='Cabin Services']",
            'loading': '//img[@alt="loading..."]',
            'available_cabin_services': "//input[@class='service-btn']//..",
            'yes_btn': "//label[@id='thanks']",
            'requested_cabin_services': "//input[@class='service-btn pending']//..",
            'cancel_request_btn': "//label[@id='cancel_request']"
            })

    def verify_cabin_services_page(self):
        """
        Function to verify cabin services page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_complete_page_top()
        if self.webDriver.is_element_display_on_screen(element=self.locators.cabin_services_header,
                                                       locator_type='xpath'):
            logger.info("Cabin services page is displayed on screen")
        else:
            raise Exception("Cabin services page is not displayed on screen")

    def request_cabin_service(self, test_data):
        """
        Function to request any cabin service
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cabin_services_header,
                                                          locator_type='xpath')
        available_services = self.webDriver.get_elements(element=self.locators.available_cabin_services,
                                                         locator_type='xpath')
        if len(available_services) == 0:
            raise Exception("No cabin services available to request")
        else:
            for service in available_services:
                if service.text == 'Fresh towels':
                    test_data['requested_cabin_service'] = service.text
                    service.click()
                    break
            else:
                raise Exception("Fresh towels cabin service is not available")
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.yes_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.yes_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.yes_btn, locator_type='xpath')

    def verify_requested_cabin_service(self, test_data):
        """
        Function to verify cabin service has been requested successfully
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cabin_services_header,
                                                          locator_type='xpath')
        requested_services = self.webDriver.get_elements(element=self.locators.requested_cabin_services,
                                                         locator_type='xpath')
        for service in requested_services:
            if test_data['requested_cabin_service'] == service.text:
                logger.info(f"Cabin service '{test_data['requested_cabin_service']}' has been requested successfully")
                break
        else:
            raise Exception(f"Cabin service '{test_data['requested_cabin_service']}' is not requested successfully")

    def cancel_raised_cabin_service_request(self, test_data):
        """
        Cancel the raised cabin service request
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cabin_services_header,
                                                          locator_type='xpath')
        requested_services = self.webDriver.get_elements(element=self.locators.requested_cabin_services,
                                                         locator_type='xpath')
        for service in requested_services:
            if test_data['requested_cabin_service'] == service.text:
                service.click()
                break
        else:
            raise Exception(f"No raised cabin service request found for '{test_data['requested_cabin_service']}'")
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cancel_request_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.cancel_request_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.cancel_request_btn,
                                                               locator_type='xpath')

    def verify_cancelled_cabin_service_request(self, test_data):
        """
        Function to verify the cabin requst has been cancelled
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cabin_services_header,
                                                          locator_type='xpath')
        requested_services = self.webDriver.get_elements(element=self.locators.requested_cabin_services,
                                                         locator_type='xpath')
        for service in requested_services:
            if test_data['requested_cabin_service'] == service.text:
                raise Exception(f"Cabin service '{test_data['requested_cabin_service']}' request is not cancelled")
        logger.info(f"Cabin service '{test_data['requested_cabin_service']}' request is cancelled successfully")