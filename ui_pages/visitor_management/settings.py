__author__ = 'prahlad.sharma'

from virgin_utils import *


class Settings(General):
    """
    Page class for Setting Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "setting_page_title": "//div[@class='column title']//span[contains(text(),'Settings')]",
            "change_ship": "//span[contains(text(),'CHANGE SHIP')]",
            "ship_name": "//div[@class='has-text-centered' and contains(text(),'%s')]",
            "chip_ship_popup_header": "//span[contains(text(),'Change Ship')]",
            "change_button": "//button[contains(@class,'button is-primary is-fullwidth')]//span[contains(text(),"
                             "'CHANGE')]",
            "cancel": "//button/span[contains(text(),'CANCEL')]",
        })

    def verify_setting_page_title(self):
        """
        Function to verify page title
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.setting_page_title, locator_type='xpath'
                                                          )
        self.webDriver.allure_attach_jpeg('setting_page_title')
        screen_title = self.webDriver.get_text(element=self.locators.setting_page_title, locator_type='xpath')
        if screen_title == "Settings":
            logger.debug("User is landed on Setting page")
        else:
            raise Exception("User is not landed on Setting page")

    def click_change_ship_button(self):
        """
        Function to click on Change Ship Button
        """
        self.webDriver.click(element=self.locators.change_ship, locator_type='xpath')
        screen_title = self.webDriver.get_text(element=self.locators.chip_ship_popup_header, locator_type='xpath')
        if screen_title == "Change Ship":
            self.webDriver.allure_attach_jpeg('pending_approval')
            logger.debug("User is landed on Change Ship Popup")
        else:
            raise Exception("User is not landed on Change Ship popup")

    def select_ship_from_list(self, ship_name_to_select):
        """
        Function to select the ship
        :param ship_name_to_select:
        """
        self.webDriver.get_text(element=self.locators.ship_name % ship_name_to_select, locator_type='xpath')

    def click_change(self):
        """
        Function to click on Change button
        """
        self.webDriver.click(element=self.locators.change_button, locator_type='xpath')

    def click_cancel(self):
        """
        Function to click on Cancel button
        """
        self.webDriver.click(element=self.locators.cancel, locator_type='xpath')
