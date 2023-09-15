__author__ = 'prahlad.sharma'

from virgin_utils import *


class Rockstar(General):
    """
    Page class for rockstar page
    """
    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//*[@text='loading...']",
            "rockstar_header": "//div[text()='You're a RockStar']",
            "rockstar_intro_message": "//div[@class='Rockstar__intro-message']",
            "richards_rooftop":"//span[text()='Richard's Rooftop access']",
            "in_room_bar": "//span[text()='Curated in-room bar, on us']",
            "early_booking_access": "//span[text()='Early booking/Priority access']",
            "rockstar_agents": "//span[text()='RockStar Agents']",
            "back": "back-btn",
        })

    def verify_availability_of_rockstar_header(self):
        """
        Function to verify_availability_of_rocktar_header
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_header, locator_type='xpath'):
            logger.debug("Rockstar header is available on rockstar page")
        else:
            raise Exception("Rockstar header is not available on rockstar page")

    def verify_availability_of_introductory_message(self):
        """
        Function to verify_availability_of_rocktar_header
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_intro_message, locator_type='xpath'):
            logger.debug("Rockstar intro message is available on rockstar page")
        else:
            raise Exception("Rockstar intro message is not available on rockstar page")

    def verify_availability_of_richards_rooftop(self):
        """
        Function to verify availability of Richards rooftop
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.richards_rooftop,
                                                       locator_type='xpath'):
            logger.debug("Richards rooftop is available on rockstar page")
        else:
            raise Exception("Richards rooftop is not available on rockstar page")

    def verify_availability_of_in_room_bar(self):
        """
        Function to verify availability of in room bar
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.in_room_bar,
                                                       locator_type='xpath'):
            logger.debug("In room bar is available on rockstar page")
        else:
            raise Exception("In room bar is not available on rockstar page")

    def verify_availability_of_early_booking_access(self):
        """
        Function to verify availability of early booking access
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.early_booking_access,
                                                       locator_type='xpath'):
            logger.debug("Early booking access is available on rockstar page")
        else:
            raise Exception("Early booking access is not available on rockstar page")

    def verify_availability_of_rockstar_agents(self):
        """
        Function to verify availability of rockstar agents
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_agents,
                                                       locator_type='xpath'):
            logger.debug("Rockstar agent is available on rockstar page")
        else:
            raise Exception("Rockstar agent is not available on rockstar page")

    def click_back(self):
        """
        Function to click back button
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')