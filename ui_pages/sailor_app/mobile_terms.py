__author__ = 'vanshika.arora'

from virgin_utils import *


class mobile_Terms(General):
    """
    Page class for mobile terms and conditions screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "mobile_terms_and_conditions": "//h1[text()='Mobile terms & conditions']",
            "downloadable_document_volume": "//div[@class='DownloadableDocument__volume']",
            "download_button": "//div[@id='downloadButton']",
            "back_button": "//button[@id='back-btn']"
            })

    def verify_mobile_terms_and_conditions_page_landing(self):
        """
        Function to verify that user has landed on mobile terms and conditions screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.mobile_terms_and_conditions,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on terms and conditions screen")
        else:
            raise Exception("Sailor has not landed on terms and conditions screen")

    def content_available_in_mobile_terms_and_conditions(self):
        """
        Function to verify that content is available in mobile terms and conditions
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.downloadable_document_volume,
                                                       locator_type='xpath'):
            logger.info("Content is available in mobile terms and conditions screen")
        else:
            raise Exception("Content is not available in mobile terms and conditions screen")

    def download_mobile_terms_and_conditions(self):
        """
        Function to download mobile terms and conditions
        :return:
        """
        self.webDriver.click(element=self.locators.download_button, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')