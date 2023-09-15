__author__ = 'prahlad.sharma'

from virgin_utils import *


class Setting(General):
    """
    Page class for setting screen of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.config = config
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "setting_title": "//*[@text='Settings']",
            "change_ship": "//*[@text='CHANGE SHIP']",
            "next_button": "//*[@text='NEXT']",
            "both_direction_mode": "com.decurtis.dxp.gangway:id/both_mode",
            "save_button": "com.decurtis.dxp.gangway:id/next",
            "onboard": "com.decurtis.dxp.gangway:id/embark_mode",
            "ashore": "com.decurtis.dxp.gangway:id/debark_mode"

        })

    def check_availability_of_setting_page(self):
        """
        Function to check the availability of setting page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.setting_title, locator_type='xpath',
                                                      time_out=600)
        return self.webDriver.is_element_display_on_screen(element=self.locators.setting_title, locator_type='xpath')

    def click_on_next(self):
        """
        Function to click on Next button on Setting page
        """
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def click_both_direction_mode(self):
        """
        Function to click on both direction mode
        """
        self.webDriver.click(element=self.locators.both_direction_mode, locator_type='id')

    def click_on_save(self):
        """
        Function to click on Save button on Setting page
        """
        self.webDriver.click(element=self.locators.save_button, locator_type='id')

    def check_availability_of_gangway_mode(self):
        """
        Function to check the availability of gangway mode
        :return:
        """
        if (self.webDriver.is_element_display_on_screen(element=self.locators.onboard, locator_type='id') and
            self.webDriver.is_element_display_on_screen(element=self.locators.ashore, locator_type='id') and
            self.webDriver.is_element_display_on_screen(element=self.locators.both_direction_mode, locator_type='id')):
            logger.info("all modes are available")
        else:
            self.webDriver.allure_attach_jpeg("setting_more_error")
            raise Exception("all Modes are not display")

    def click_onboard_direction_mode(self):
        """
        Function to click on Onboard direction mode
        """
        self.webDriver.click(element=self.locators.onboard, locator_type='id')

    def click_ashore_direction_mode(self):
        """
        Function to click on Ashore direction mode
        """
        self.webDriver.click(element=self.locators.ashore, locator_type='id')

