__author__ = 'vanshika.arora'

from virgin_utils import *


class Ship(General):
    """
    Page class for Ship page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "eateries": "//div[@id='PromoCard_item_0']",
            "beauty_and_body": "//div[@id='PromoCard_item_5']",
            "default_slot1": "//span[@text='6:00pm']",
            "default_slot2": "//span[@text='6:30pm']",
            "default_slot3": "//span[@text='7:00pm']",
            "ship_spaces_header": "//h1[text()='Oh, the spaces you will go']",
            "back_button": "//button[@id='back-btn']",
            "rockstar_space": "//div[text()='Rockstar']",
            "space_header": "//h1[@class='ShipSpacesLanding__PageContainer_header']"
        })

    def open_eateries(self):
        """
        To open eateries
        :return:
        """
        self.webDriver.click(element=self.locators.eateries, locator_type='xpath')

    def open_beauty_and_body(self):
        """
        To open eateries
        :return:
        """
        self.webDriver.click(element=self.locators.beauty_and_body, locator_type='xpath')

    def verify_ship_spaces_header(self):
        """
        To verify that user has landed on ship spaces screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_spaces_header,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on ship spaces screen")
        else:
            raise Exception("Sailor has not landed on ship spaces screen")

    def click_back_button(self):
        """
        Function to click back button on ship spaces screen
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def verify_availability_of_rockstar_space_for_vip_sailor(self):
        """
        Function to verify availability of vip space
        """
        self.webDriver.scroll_complete_page()
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_space,
                                                       locator_type='xpath'):
            logger.info("Rockstar space is available on ship spaces screen")
        else:
            raise Exception("Rockstar space is not available on ship spaces screen")

    def verify_unavailability_of_rockstar_space_for_non_vip_sailors(self):
        """
        Function to verify unavailability of vip space
        """
        self.webDriver.scroll_complete_page()
        if not self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_space,
                                                       locator_type='xpath'):
            logger.info("Rockstar space is not available on ship spaces screen")
        else:
            raise Exception("Rockstar space is available on ship spaces screen")

    def open_rockstar_space(self):
        """
        Function to verify that vip sailor is able to open rockstar space
        """
        self.webDriver.click(element=self.locators.rockstar_space, locator_type='xpath')

    def verify_rockstar_space_header(self):
        """
        Function to verify that user has landed on rockstar space
        """
        get_header = self.webDriver.get_text(element=self.locators.space_header,locator_type='xpath')
        assert get_header == "Rockstar", "Correct header is not displayed on rockstar space"





