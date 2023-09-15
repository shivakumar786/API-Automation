__author__ = 'Krishna'

from virgin_utils import *


class CancelSlot(General):
    """
    To Initiate elements from cancel Slot tab
    """
    def __init__(self, web_driver):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "cancel_slot": "//*[@class='ButtonsContainer__div']/button[text()='Cancel Slot']",
            "loader": "//div[@class='LoaderContainer__div']//img"
        })

    def click_on_cancel_cta(self):
        """
        click on cancel button on cancel slot page
        """
        self.webDriver.click(element=self.locators.cancel_slot, locator_type="xpath")