__author__ = 'sarvesh.singh'

from virgin_utils import *


class ChooseCabin(General):
    """
    Page class for Choose Cabin Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = {
            "cabin": "//*[@class='btn btn-secondary CabinCategoryCard__choose']"
        }

    def choose_cabin(self):
        """
        To open account dropdown
        :return:
        """
        cabins = self.webDriver.get_elements(element=self.locators['cabin'], locator_type='xpath')
        for _cabin in cabins:
            _cabin.click()
            self.webDriver.wait_for(seconds=5)
            break
