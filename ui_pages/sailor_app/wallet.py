__author__ = 'prahlad.sharma'

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
            "wallet_next_cta": "//button[@id=myWalletButton']",
        })

    def click_wallet_next_cta(self):
        """
        Function to open my wallet
        :return:
        """
        self.webDriver.click(element=self.locators.wallet_next_cta, locator_type='xpath')