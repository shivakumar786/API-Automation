__author__ = 'vanshika.arora'

from virgin_utils import *


class Restaurant_details(General):
    """
    Page class for Restaurant details page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "restaurant_name_header": "//div[text()='Razzle Dazzle Restaurant']",
            "find_a_table": "//button[@id='mainButton']",
            "select_time_slot": "//div[@id='timeslot_0']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
        })

    def verify_user_landed_on_restaurant_details_page(self):
        """
        Function to verify that user has landed on restaurant details page
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.restaurant_name_header,
                                                       locator_type='xpath'):
            logger.debug("User has landed on restaurant details page")
        else:
            raise Exception("User has not landed on restaurant details page")

    def click_find_a_table(self):
        """
        Function to click find a table button
        """
        self.webDriver.click(element=self.locators.find_a_table, locator_type='xpath')

    def select_booking_details(self):
        """
        Function to select booking details
        """
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_time_slot, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')