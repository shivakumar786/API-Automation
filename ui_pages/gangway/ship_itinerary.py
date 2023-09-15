__author__ = 'prahlad.sharma'

from virgin_utils import *


class Ship_Itinerary(General):
    """
    Page class for Ship Itinerary screen of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.config = config
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "day_box": "com.decurtis.dxp.gangway:id/constraint_layout_one",
            "day_number": "com.decurtis.dxp.gangway:id/day",
            "voyage_date": "com.decurtis.dxp.gangway:id/date",
            "voyage_location": "com.decurtis.dxp.gangway:id/label_port_name",
            "port_name": "com.decurtis.dxp.gangway:id/port_name"
        })

    def verify_the_field_availability_for_itinerary(self):
        """
        Function to verify the various fields on Ship Itinerary page
        """
        if (self.webDriver.is_element_display_on_screen(element=self.locators.day_box, locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.day_number, locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.voyage_date, locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.voyage_location,
                                                            locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.port_name, locator_type='id')):
            logger.info("correct fields display on screen")
        else:
            self.webDriver.allure_attach_jpeg("ship_itinerary_error")
            raise Exception("correct Fields not display on Ship Itinerary page")
