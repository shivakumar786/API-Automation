__author__ = 'vanshika.arora'

from virgin_utils import *


class privacy_Policy(General):
    """
    Page class for privacy policy screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "privacy_policy": "//h1[text()='Privacy policy']",
            "downloadable_document_volume": "//div[@class='DownloadableDocument__volume']",
            "download_button": "//div[@id='downloadButton']",
            "back_button": "//button[@id='back-btn']"
        })

    def verify_privacy_policy_landing(self):
        """
        Function to verify that user has landed on privacy policy screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.privacy_policy,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on privacy policy screen")
        else:
            raise Exception("Sailor has not landed on privacy policy screen")

    def content_available_in_privacy_policy(self):
        """
        Function to verify that content is available in privacy policy
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.downloadable_document_volume,
                                                       locator_type='xpath'):
            logger.info("Content is available in privacy policy screen")
        else:
            raise Exception("Content is not available in privacy policy screen")

    def download_privacy_policy(self):
        """
        Function to download privacy policy
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
