__author__ = 'mohit.raghav'

from virgin_utils import *


class Wallet(General):
    """
    Page class for wallet page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "wallet_balance": "//div[text()='Amount Due']",
            'loading': '//img[@alt="loading..."]'
        })

    def verify_wallet_balance_page(self):
        """
        Function to verify wallet balance page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_complete_page_top()
        if self.webDriver.is_element_display_on_screen(element=self.locators.wallet_balance, locator_type='xpath'):
            logger.info("Wallet balance page is displayed on screen")
        else:
            raise Exception("Wallet balance page is not displayed on screen")
