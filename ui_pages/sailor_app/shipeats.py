__author__ = 'vanshika.arora'

from virgin_utils import *


class Ship_eats(General):
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
            "ship_eats_header": "//h1[text(0='ShipEats Delivery']",
            "content_header": "//div[@class='ShipEat__content_header']",
            "content_subheader": "//div[@class='ShipEat__content_subHeader']",
            "back_button": "//button[@class='BackButton']",

        })

    def verify_shipeats_header(self):
        """
        Verify that user has landed on ship eats screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_eats_header, locator_type='xpath'):
            logger.debug("User has landed on Shipeats screen")
        else:
            raise Exception("User has not landed on Shipeats Screen")

    def verify_shipeats_steps_header(self):
        """
        Function to open ship eats
        :return:
        """
        steps_header = ['Order the best bites and bevs', 'Delivered right to you', ' Breakfast in bed, but also…']
        j=0
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        get_all_steps_header = self.webDriver.get_elements(
            element=self.locators.content_header, locator_type='xpath')
        for i in get_all_steps_header:
            assert steps_header[j] == i.text, "Steps Header are not matching"
            j += 1

