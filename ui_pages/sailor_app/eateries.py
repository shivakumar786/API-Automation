__author__ = 'vanshika.arora'

from virgin_utils import *


class Eateries(General):
    """
    Page class for Login page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "default_slot1": "//span[text()='6:00pm']",
            "default_slot2": "//span[text()='6:30pm']",
            "default_slot3": "//span[text()='7:00pm']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            "eateries_header": "//h1[text()='Eateries']",
            "back_button": "//button[@id='back-btn']",
            "open_restaurant_details": "//div[@class='list-item__content']/h2[text()='Razzle Dazzle Restaurant']",
            "repeat_restaurant_error": "//div[text()='Repeat restaurant bookings']",
            "all_venues": "//div[@class='ShipSpacesLanding__PageContainer_list']/div",
            "get_venue_name": "//div[@class='ShipSpacesLanding__PageContainer_list']/div[%s]/div/div/h2",
        })

    def verify_eateries_header(self):
        """
        Function to verify availbility of eateries header on the screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.eateries_header, locator_type='xpath'):
            logger.debug("Eateries header is available on restaurant listing screen")
        else:
            raise Exception("Eateries header is not available on restaurant listing screen")

    def verify_availability_of_default_slots(self):
        """
        To verify that default slots are available on restaurant listing screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.default_slot1, locator_type='xpath'):
            logger.debug("6pm slot is available on restaurant listing screen")
        else:
            raise Exception("6pm slot is not available on restaurant listing screen")

        if self.webDriver.is_element_display_on_screen(element=self.locators.default_slot2, locator_type='xpath'):
            logger.debug("6:30pm slot is available on restaurant listing screen")
        else:
            raise Exception("6:30pm slot is not available on restaurant listing screen")

        if self.webDriver.is_element_display_on_screen(element=self.locators.default_slot3, locator_type='xpath'):
            logger.debug("7pm slot is available on restaurant listing screen")
        else:
            raise Exception("7pm slot is not available on restaurant listing screen")

    def book_dining(self):
        """
        Function to book dining
        :return:
        """
        self.webDriver.click(element=self.locators.default_slot1, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def click_default_slot(self):
        """
        Function to book dining
        :return:
        """
        self.webDriver.click(element=self.locators.default_slot1, locator_type='xpath')

    def verify_repeat_restaurant_conflict_screen(self):
        """
        Function to verify repeat restaurant conflict screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.repeat_restaurant_error, locator_type='xpath'):
            logger.debug("Repeat restaurant conflict is available on screen")
        else:
            raise Exception("Repeat restaurant conflict is not available on screen")

    def click_back_button(self):
        """
        Function to click back button on eateries screen
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def open_restaurant_details_page(self):
        """
        Function to open restaurant details page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.open_restaurant_details, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.open_restaurant_details, locator_type='xpath')

    def verify_user_landed_on_restaurant_details_page(self):
        """
        Function to verify that user has landed on restaurant details page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.restaurant_name_header,
                                                      locator_type='xpath'
                                                      , time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.restaurant_name_header, locator_type='xpath'):
            logger.debug("User has landed on restaurant details page")
        else:
            raise Exception("User has not landed on restaurant details page")

    def navigate_away_from_conflict_screen(self):
        """
        Function to naviagte away from screen
        """
        self.webDriver.mobile_native_back()

    def verify_no_duplicate_venue_available(self):
        """
        Function to verify that no duplicate restaurants are available
        """
        get_all_venues = self.webDriver.get_elements(element=self.locators.all_venues, locator_type='xpath')
        venue_list=[]
        for i in range(1, len(get_all_venues)+1):
            venue_name = self.webDriver.get_text(element=self.locators.get_venue_name % i, locator_type='xpath')
            if venue_name not in venue_list:
                venue_list.append(venue_name)
            else:
                raise Exception(f"Repeated venues are available for {venue_name}")



