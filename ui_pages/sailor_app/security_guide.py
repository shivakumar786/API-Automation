__author__ = 'vanshika.arora'

from virgin_utils import *


class security_Guide(General):
    """
    Page class for security guide
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "security_guide": "//h1[text()='Security Guide']",
            "downloadable_document_volume": "//div[@class='DownloadableDocument__volume']",
            "download_button": "//div[@id='downloadButton']",
            "back_button": "//button[@id='back-btn']"
            })

    def verify_security_guide_page_landing(self):
        """
        Function to verify that user has landed on security guide screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.security_guide,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on security guide screen")
        else:
            raise Exception("Sailor has not landed on security guide screen")

    def content_available_in_security_guide(self):
        """
        Function to verify that content is available in security guide
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.downloadable_document_volume,
                                                       locator_type='xpath'):
            logger.info("Content is available in security guide screen")
        else:
            raise Exception("Content is not available in security guide screen")

    def download_security_guide(self):
        """
        Function to download security guide
        :return:
        """
        self.webDriver.click(element=self.locators.download_button, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button
        :return:
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')




