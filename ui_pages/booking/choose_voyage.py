__author__ = 'sarvesh.singh'

from virgin_utils import *


class ChooseVoyage(General):
    """
    Page class for Choose Voyage Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "cross": "//*[@class='CookieBar__close js-CookieBar__close']",
            "accountButton": "//div[@id='booking-account']//div[@class='Popover']",
            "spinner": "Spinner",
            "signInToAccount": "//button[@class='btn btn-block btn-secondary']",
            "voyages": "//button[contains(text(),'Choose Voyage')]"
        })

    def open_account_dropdown(self):
        """
        To open account dropdown
        :return:
        """
        self.webDriver.click(element=self.locators['cross'], locator_type='xpath')
        self.webDriver.click(element=self.locators['accountButton'], locator_type='xpath')

    def click_sign_in_to_your_account(self):
        """
        To click on sign in to your account button
        :return:
        """
        self.webDriver.click(element=self.locators['signInToAccount'], locator_type='xpath')
        self.webDriver.wait_for(seconds=5)

    def go_to_account_page(self):
        """
        Navigate to account page
        :return:
        """
        self.webDriver.wait_for(seconds=30)
        self.open_account_dropdown()
        ss_path = os.path.abspath('/screen_shot/acc.png')
        ss_name = self.webDriver.screen_shot(file_name=ss_path)
        # allure.attach('screenshot', self.webDriver.driver.get_screenshot_as_png(), attachment_type=allure.attachment_type.PNG)
        allure.attach('screenshot', ss_path, attachment_type=allure.attachment_type.PNG)

        self.webDriver.wait_for(seconds=10)
        self.click_sign_in_to_your_account()

    def scroll_to_voyage(self):
        """
        Navigate to account page
        :return:
        """
        self.webDriver.scroll(pixel_x='0', pixel_y='400')

    def click_voyage(self):
        """
        To click on sign in to your account button
        :return:
        """
        voyages = self.webDriver.get_elements(element=self.locators['voyages'], locator_type='xpath')
        for _voyage in voyages:
            _voyage.click()
            self.webDriver.wait_for(seconds=5)
            break

    def choose_voyage(self):
        """

        :return:
        """
        self.scroll_to_voyage()
        self.click_voyage()
