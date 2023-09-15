__author__ = 'vanshika.arora'

from virgin_utils import *


class Contacts(General):
    """
    Page class for Messenger page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "cabin_mates": "//div[@class='MessengerContactList__matesRow_name']",
            "view_profile": "//*[@text='View profile']",
            "cabin_mates_name": "//div[@classs='MessengerContact__name']",
            "back_button": "back-btn",
            "allow_toggle_button": "//div[@class='react-toggle-track']"

        })


    def open_cabin_mates_profile(self):
        """
        Function to verify cabin mates profile
        """
        self.webDriver.click(element=self.locators.cabin_mates, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.view_profile, locator_type='xpath')

    def verify_cabin_mate_name(self, guest_data):
        """
        Function to verify cabin mates name
        """
        contexts = self.webDriver.get_contexts()
        sailor_mate_name = " ".join([guest_data[1]['FirstName'], guest_data[1]['LastName']])
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        cabin_mates_name = self.webDriver.get_text(element=self.locators.cabin_mates_name, locator_type='xpath')
        assert cabin_mates_name == sailor_mate_name, "Correct sailot mates name is shown in sailor app"

    def allow_cabin_mate_to_see_what_primary_sailor_is_attending(self):
        """
        Function to enable button to allow cabin mate to see what primary sailor is attending
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='id')

    def click_back_button(self):
        """
        Function to click back button
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='id')


