__author__ = 'vanshika.arora'

from virgin_utils import *


class Redemption_spa(General):
    """
    Page class for Beauty And body page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "acupunture": "//div[text()='Acupunture']",
            "resurrection_acupuncture": "//div[@id='resurrectionAcupunctureItem']"

        })

    def open_resurrection_accupuncture(self):
        """
        Function to open and view resurrection accupuncture
        :return:
        """
        self.webDriver.click(element=self.locators.acupunture, locator_type='xpath')
        self.webDriver.click(element=self.locators.resurrection_acupuncture, locator_type='xpath')
