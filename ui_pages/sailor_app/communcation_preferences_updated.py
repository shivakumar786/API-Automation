__author__ = 'vanshika.arora'

from virgin_utils import *


class communication_Preferences_Updated(General):
    """
    Page class for communication preferences updated screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "communication_preferences_updated_header": "//h1[text()='Communication Preferences: updated']",
            "loader": "//div[@class='loader-wrapper']",
            "next_cta": "//button[@id='btn-cnfirmation']",
            })

    def verify_communication_preferences_updated_title(self):
        """
        Function to verify communication preferences updated header
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.communication_preferences_updated_header,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on communication preferences screen")
        else:
            raise Exception("Sailor has not landed on communication preferences screen")

    def click_next_cta(self):
        """
        Function to click done button
        :return:
        """
        self.webDriver.click(element=self.locators.next_cta, locator_type='xpath')
