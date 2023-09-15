__author__ = 'vanshika.arora'

from virgin_utils import *


class Pregnancy(General):
    """
    Page class for pregnancy page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "yes": "//label[@id='yesPregnantButton']",
            "weeks": "//input[@id='weeksInput']",
            "next_btn": "//button[@id='submit']",
            "safe_to_travel_header": "//h1[text()='Safe to travel']",
            "we_will_be_in_touch": "//h1[text()='Hey Mama']",
            "ok_btn": "//button[@id='okButton']"
        })

    def select_yes(self):
        """
        Function to select yes for pregnancy question
        """
        self.webDriver.click(element=self.locators.yes, locator_type='xpath')

    def verify_safe_to_travel_screen(self):
        """
        Function to verify availability of safe to travel screen when pregnancy weeks are less than or equal to 22
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.safe_to_travel_header,
                                                       locator_type='xpath'):
            logger.debug("Safe to travel title is available on screen")
        else:
            raise Exception("Safe to travel title is not available on screen")

    def verify_we_will_be_in_touch_screen(self):
        """
        Function to verify we will be in touch screen when pregnancy weeks are greater than 22
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.we_will_be_in_touch,
                                                       locator_type='xpath'):
            logger.debug("We will be in touch text is available on screen")
        else:
            raise Exception("We will be in touch text not available on screen")

    def enter_no_of_weeks(self):
        """
        Function to enter no of weeks the sailor is pregnant
        :return:
        """
        weeks = random.randint(0,42)
        self.webDriver.set_text(element=self.locators.weeks, locator_type='xpath',text=weeks)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.next_btn, locator_type='xpath')
        if weeks<=22:
            self.verify_safe_to_travel_screen()
        else:
            self.verify_we_will_be_in_touch_screen()

    def click_ok_button(self):
        """
        Function to click ok button
        """
        self.webDriver.click(element=self.locators.ok_btn, locator_type='xpath')
