__author__ = 'sarvesh.singh'

from virgin_utils import *


class SailorDetails:
    """
    Page class for Account Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        self.webDriver = web_driver
        self.locators = {
            "genderMale": "//label[contains(text(),'Male')]",
            "citizenship": "//select[@id='primary_citizenShip']",
            "over18": "//label[@for='primary_over18']",
            "skipVoyageProtection": "//label[@for='primary_insurance_notOpted']",
            "continue": "//button[@id='SailorDetailsSubmit']"
        }

    def select_gender(self):
        """

        :return:
        """
        self.webDriver.click(element=self.locators['genderMale'], locator_type='xpath')

    def select_citizenship(self):
        """

        :return:
        """
        self.webDriver.select_by_text(element=self.locators['citizenship'], locator_type='xpath', text='United States')

    def agree_18_plus(self):
        """

        :return:
        """
        self.webDriver.click(element=self.locators['over18'], locator_type='xpath')

    def skip_voyage_protection(self):
        """

        :return:
        """
        self.webDriver.click(element=self.locators['skipVoyageProtection'], locator_type='xpath')

    def click_continue(self):
        """

        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators['continue'], locator_type='xpath')

    def fill_sailor_details(self):
        self.webDriver.scroll(pixel_x='0', pixel_y='600')
        self.select_gender()
        self.select_citizenship()
        self.agree_18_plus()
        self.skip_voyage_protection()
        self.click_continue()
        self.webDriver.wait_for(seconds=5)
