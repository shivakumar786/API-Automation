__author__ = 'mohit.raghav'

import random

from virgin_utils import *


class Eateries(General):
    """
    Page class for Eateries page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "eateries_header": "//h1[text()='Eateries']",
            'loading': '//img[@alt="loading..."]',
            "back_button": "//*[@resource-id='back-btn']",
            'bookable_slots': "//span[@class='timeslot-item']",
            'disabled_slots': "//span[@class='timeslot-item disable']",
            'second_sailor_select': "//div[@id='user_avatar_1']",
            'next_btn': "//button[@id='nextButton']",
            'select_slot': "//div[text()='{}']",
            'already_selected_slot': "//div[@class='time-item selected']",
            'restro_list': "//div[@class='list-item-container']",
            'summary_check_box': "//label[@class='form-control-checkbox']",
            'slots_available': "//div[@class='time-item']"
        })

    def click_back_button(self):
        """
        Function to click back button on eateries screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def verify_eateries_header(self):
        """
        Function to verify availbility of eateries header on the screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.eateries_header, locator_type='xpath'):
            logger.debug("Eateries header is available on restaurant listing screen")
        else:
            raise Exception("Eateries header is not available on restaurant listing screen")

    def verify_availability_of_default_slots(self):
        """
        Verify defaults slots are available
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.eateries_header, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.restro_list, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.disabled_slots, locator_type='xpath'):
            logger.info("Default slots are available but are disabled for booking")
        elif self.webDriver.is_element_display_on_screen(element=self.locators.bookable_slots, locator_type='xpath'):
            logger.info("Default slots are available and are enabled for booking")

    def verify_availability_of_bookable_slots(self, test_data):
        """
        Function to verify availability of bookable slots
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.bookable_slots, locator_type='xpath')
        no_of_bookable_slots = len(self.webDriver.get_elements(element=self.locators.bookable_slots,
                                                               locator_type='xpath'))
        if no_of_bookable_slots > 0:
            test_data['bookable_dining_slots'] = True
            logger.info("Bookable dining slots are available")
        else:
            test_data['bookable_dining_slots'] = False

    def book_dining(self):
        """
        Function to book dining
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.bookable_slots, locator_type='xpath')
        bookable_slots = self.webDriver.get_elements(element=self.locators.bookable_slots, locator_type='xpath')
        slot = random.choice(bookable_slots)
        slot_time = slot.text
        self.webDriver.scroll(pixel_x=slot.location['x'], pixel_y=slot.location['y'])
        slot.click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.second_sailor_select,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.second_sailor_select, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.already_selected_slot,
                                                           locator_type='xpath'):
            self.webDriver.click(element=self.locators.select_slot.format(slot_time), locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.next_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_btn, locator_type='xpath')

    def book_dining_at_restaurant_closing_time(self):
        """
        Function to book dining at restaurant closing time
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.bookable_slots, locator_type='xpath')
        bookable_slots = self.webDriver.get_elements(element=self.locators.bookable_slots, locator_type='xpath')
        slot = random.choice(bookable_slots)
        slot_time = slot.text
        self.webDriver.scroll(pixel_x=slot.location['x'], pixel_y=slot.location['y'])
        slot.click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.second_sailor_select,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.second_sailor_select, locator_type='xpath')
        self.webDriver.wait_for(2)
        last_slot = self.webDriver.get_elements(element=self.locators.slots_available, locator_type='xpath')[-1]
        last_slot.click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.next_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_btn, locator_type='xpath')