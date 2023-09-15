__author__ = 'Krishna'

from virgin_utils import *


class StopSell(General):
    """
    To Initiate elements from add slots tab
    """
    def __init__(self, web_driver):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "stop": "//*[text()='STOP']"
        })

    def click_on_stop_cta(self):
        """
        click on stop cta on stop sell page
        """
        self.webDriver.click(element=self.locators.stop, locator_type="xpath")
