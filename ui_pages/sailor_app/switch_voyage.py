__author__ = 'vanshika.arora'

from virgin_utils import *


class switch_Voyage(General):
    """
    Page class for switch voyage screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "voyage_selection": "//h1[text()='Voyage selection']",
            "voyage_image": "//div[@class='img-bd']",
            "voyage_title": "//div[@class='title']",
            "port_names": "//div[@class='port-names']",
            "ship_name": "//div[@class='ship-name']",
            "connect_booking": "//button[@id='connectBookingButton']",
            })

    def verify_switch_voyage_page_landing(self):
        """
        Function to verify that user has landed on switch voyage screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_selection,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on switch voyage screen")
        else:
            raise Exception("Sailor has not landed on switch voyage screen")

    def verify_availability_of_voyage_image(self):
        """
        Function to verify availability of voyage image
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_image, locator_type='xpath'):
            logger.debug("Voyage image is available on switch voyage screen")
        else:
            raise Exception("Voyage image is not available on switch voyage screen")

    def verify_voyage_name(self, test_data):
        """
        Function to verify voyage name
        :param test_data
        :return:
        """
        voyage_name = self.webDriver.get_text(element=self.locators.voyage_title, locator_type='xpath')
        port_names = self.webDriver.get_text(element=self.locators.port_names, locator_type='xpath')
        self.webDriver.click(element=self.locators.voyage_image, locator_type='xpath')
        assert voyage_name == test_data['homepage_voyage_name'], "Correct voyage name is not shown in switch voyage screen"
        assert port_names == test_data['homepage_port_names'], "Correct ports name is not shown in switch voyage screen"

    def click_connect_booking(self):
        """
        Function to click connect booking button
        :return:
        """
        self.webDriver.click(element=self.locators.connect_booking, locator_type='xpath')