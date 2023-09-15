__author__ = 'mohit.raghav'

from virgin_utils import *


class Ship_spaces(General):
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
            "ship_spaces_header": "//h1[text()='Oh, the spaces you will go']",
            'loading': '//img[@alt="loading..."]',
            'eateries_section': "//div[text()='Eateries']",
            'beauty_and_body_section': "//div[text()='Beauty & Body']"
        })

    def verify_ship_spaces_header(self):
        """
        To verify that user has landed on ship spaces screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_complete_page_top()
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_spaces_header,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on ship spaces screen")
        else:
            raise Exception("Sailor has not landed on ship spaces screen")

    def open_eateries(self):
        """
        Click on Eateries section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.eateries_section, locator_type='xpath')
        self.webDriver.click(element=self.locators.eateries_section, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.eateries_section,
                                                               locator_type='xpath')

    def open_beauty_and_body(self):
        """
        Click Beauty and Body
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.beauty_and_body_section,
                                                          locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.beauty_and_body_section, locator_type='xpath')
        self.webDriver.click(element=self.locators.beauty_and_body_section, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.beauty_and_body_section,
                                                               locator_type='xpath')