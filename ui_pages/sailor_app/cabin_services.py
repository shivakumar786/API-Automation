__author__ = 'vanshika.arora'

from virgin_utils import *


class Cabin_Services(General):
    """
    Page class for Cabin Services page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "cabin_services": "//span[text()='Cabin services']",
            "make_your_cabin": "//div[text()='Making your cabin... ']",
            "cabin_services_content": "//p[@class='PageParagraph SplashScreen__description']/span"
        })

    def verify_make_your_cabin_header(self):
        """
        Verify header of services section
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.cabin_services, locator_type='xpath'):
            logger.debug("User has landed on Cabin services screen")
        else:
            raise Exception("User has not landed on Cabin services screen")

    def verify_cabin_services_content(self):
        """
        To verify text in cabin servicees page
        :return:
        """
        cabin_services_content = self.webDriver.get_text(element=self.locators.lineup_day_And_date, locator_type='xpath')
        if cabin_services_content == "Once you're on board, come back here for all your cabin wants and needs.":
            logger.debug("Correct content is displayed on Cabin Services screen")
        else:
            raise Exception("Incorrect content is displayed on Cabin Services screen")

