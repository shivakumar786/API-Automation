__author__ = 'vanshika.arora'

import random

from virgin_utils import *


class Emergency_contact(General):
    """
    Page class for emergency contact page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "emergency_contact_name": "//input[@id='nameInput']",
            "click_next_cta": "//button[@id='submit']",
            "open_relationship_options": "//span[@id='relationshipInput']",
            "select_relation": "//*[@text='%s']",
            "int_code": "//input[@id='intInput']",
            "select_us_code": "//div[text()='United States (+1)']",
            "phone_number": "//input[@id='phoneNumberInput']"
        })

    def enter_emergency_contact_name(self):
        """
        Function to enter emergency contact name
        """
        first_name = generate_first_name()
        last_name = generate_last_name()
        emergency_contact_name = " ".join([first_name,last_name])
        self.webDriver.set_text(element=self.locators.emergency_contact_name, locator_type='xpath', text=emergency_contact_name)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.click_next_cta, locator_type='xpath')

    def select_emergency_contact_relationship(self):
        """
        Function to selct emergency contact relationship
        """
        relationships_available = ['Child', 'Friend', 'Parent', 'Spouse', 'Other Relative']
        self.webDriver.click(element=self.locators.open_relationship_options, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.select_relation % random.choice(relationships_available), locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.click_next_cta, locator_type='xpath')

    def enter_emergency_contact_number(self):
        """
        Function to enter emergency contact number
        """
        self.webDriver.click(element=self.locators.int_code, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_us_code, locator_type='xpath')
        phone_number = generate_phone_number(10)
        self.webDriver.set_text(element=self.locators.phone_number, locator_type='xpath',
                                text=phone_number)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.click_next_cta, locator_type='xpath')


