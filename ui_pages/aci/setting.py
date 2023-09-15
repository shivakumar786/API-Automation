__author__ = 'sarvesh.singh'

from virgin_utils import *


class Setting(General):
    """
    Page class for setting screen of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "setting_title": "//*[@text='Settings']",
                "change_ship": "//*[@text='CHANGE SHIP']",
                "next_button": "//*[@text='NEXT']",
                "running_at": "com.decurtis.dxp.aci:id/spinner",
                "hotel_mode": "//*[contains(@text,'Airport')]",
                "save_button": "//*[@text='SAVE']",
            })
        else:
            self.locators = self.dict_to_ns({
                "setting_title": "//*[@text='Settings']",
                "change_ship": "//*[@text='CHANGE SHIP']",
                "next_button": "//*[@text='NEXT']",
                "running_at": "com.decurtis.dxp.aci.dclnp:id/spinner",
                "hotel_mode": "//*[contains(@text,'Airport')]",
                "save_button": "//*[@text='SAVE']",
            })

    def switch_mode(self):
        """
        To switch mode
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.running_at, locator_type='id', time_out=30)
        self.webDriver.click(element=self.locators.running_at, locator_type='id')
        self.webDriver.click(element=self.locators.hotel_mode, locator_type='xpath')
        self.webDriver.click(element=self.locators.save_button, locator_type='xpath')

    def check_availability_of_setting_page(self):
        """
        Function to check the availability of setting page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.setting_title, locator_type='xpath',
                                                      time_out=300)
        return self.webDriver.is_element_display_on_screen(element=self.locators.setting_title, locator_type='xpath')

    def click_on_next(self):
        """
        Function to click on Next button on Setting page
        """
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
