__author__ = 'prahlad.sharma'

from virgin_utils import *


class History(General):
    """
    Page class for History screen of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.config = config
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "filter_dropdown": "com.decurtis.dxp.gangway:id/person_type",
            "select_value_dd": "//*[@resource-id='android:id/text1' and @text='%s']",
            "guest_type": "com.decurtis.dxp.gangway:id/person_text",
            "search_box": "com.decurtis.dxp.gangway:id/search_src_text",
            "station_checkbox": "com.decurtis.dxp.gangway:id/myStationHistory"
        })

    def select_person_type(self, person_type):
        """
        Function to select the person type
        :param person_type:
        """
        self.webDriver.click(element=self.locators.filter_dropdown, locator_type='id')
        self.webDriver.click(element=self.locators.select_value_dd % person_type, locator_type='xpath')

    def verify_person_type_in_list(self, person_type):
        """
        Function to verify the person type
        """
        p_type = self.webDriver.get_text(element=self.locators.guest_type, locator_type='id')
        if p_type == person_type:
            logger.info("correct type of person display on screen")
        else:
            self.webDriver.allure_attach_jpeg("person_type_error")
            raise Exception(f"Wrong data display expected is: {person_type}")

    def verify_the_field_availability_for_history(self):
        """
        Function to verify the various fields on Ship Itinerary page
        """
        if (self.webDriver.is_element_display_on_screen(element=self.locators.filter_dropdown, locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.search_box, locator_type='id') and
                self.webDriver.is_element_display_on_screen(element=self.locators.station_checkbox, locator_type='id')
                and self.webDriver.is_element_display_on_screen(element=self.locators.guest_type, locator_type='id')):
            logger.info("correct fields display on screen")
        else:
            self.webDriver.allure_attach_jpeg("history_error")
            raise Exception("correct Fields not display on history page")

