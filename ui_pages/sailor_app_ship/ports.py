__author__ = 'mohit.raghav'

from virgin_utils import *


class Ports(General):
    """
    Page class for ports page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "click_book_excursion": "//*[@text='Book a Shore Thing']",
            "shore_thing_active_btn": "//button[@class='CardSlider__btn CardSlider--PortButton__Left button button-small-primary']",
            "loader": "//*[@text='loading...']",
            'loading': '//img[@alt="loading..."]',
            "back_button": "//*[@resource-id='back-btn']",
            'back_btn': "//button[@id='back-btn']/span",
            'all_excursion': "//div[@class='EventCard__name']",
            "click_book_button": "//button[@id='mainButton']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            'time_slots': "//div[@class='time-item']",
            'exursion_page': "//div[@id='CountResult']",
            'ports_btn': "//li[@class='']",
            'active_port': "//li[@class='slick-active']//button[@class='CardSlider__paging-item button button-custom']"
        })

    def verify_shore_things_page(self):
        """
        Function to verify shore ports landing page
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.click_book_excursion,
                                                       locator_type='xpath'):
            logger.debug("User has landed on ports listing screen")
        else:
            raise Exception("User has not landed on ports listing screen")

    def click_back_button(self):
        """
        Function to click back button on ports listing screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def check_excursion(self, test_data):
        """
        Function to click Book excursions button
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ports_btn, locator_type='xpath')
        ports = self.webDriver.get_elements(element=self.locators.ports_btn, locator_type='xpath')
        active_port = self.webDriver.get_elements(element=self.locators.active_port, locator_type='xpath')
        ports.append(active_port)
        for port in ports:
            port.click()
            self.webDriver.wait_for(3)
            if self.webDriver.is_element_display_on_screen(element=self.locators.shore_thing_active_btn,
                                                           locator_type='xpath'):
                self.webDriver.click(element=self.locators.shore_thing_active_btn, locator_type='xpath')
                self.webDriver.wait_till_element_appear_on_screen(element=self.locators.exursion_page,
                                                                  locator_type='xpath')
                available_excursions = self.webDriver.get_elements(element=self.locators.all_excursion,
                                                                   locator_type='xpath')
                if len(available_excursions) != 0:
                    for event in available_excursions:
                        self.webDriver.scroll(pixel_x=event.location['x'], pixel_y=event.location['y'])
                        self.webDriver.wait_for(3)
                        event.click()
                        test_data['booked_excursion_name'] = event.text
                        test_data['bookable_excursion_available'] = True
                        break
                    break
                else:
                    self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
                    self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading,
                                                                           locator_type='xpath')
        else:
            test_data['bookable_excursion_available'] = False

    def select_and_open_excursion_event(self, test_data):
        """
        To select and open excursion event
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.exursion_page, locator_type='xpath')
        available_excursions = self.webDriver.get_elements(element=self.locators.all_excursion, locator_type='xpath')
        if len(available_excursions) != 0:
            for event in available_excursions:
                self.webDriver.scroll(pixel_x=event.location['x'], pixel_y=event.location['y'])
                self.webDriver.wait_for(3)
                event.click()
                test_data['booked_excursion_name'] = event.text
                test_data['bookable_excursion_available'] = True
                break
        else:
            self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ports_btn, locator_type='xpath')
            ports = self.webDriver.get_elements(element=self.locators.ports_btn, locator_type='xpath')
            for port in ports:
                port.click()
                self.webDriver.wait_for(3)
                if self.webDriver.is_element_display_on_screen(element=self.locators.shore_thing_active_btn,
                                                               locator_type='xpath'):
                    self.webDriver.click(element=self.locators.shore_thing_active_btn, locator_type='xpath')
                    self.webDriver.wait_till_element_appear_on_screen(element=self.locators.exursion_page,
                                                                      locator_type='xpath')
                    available_excursions = self.webDriver.get_elements(element=self.locators.all_excursion,
                                                                       locator_type='xpath')
                    if len(available_excursions) != 0:
                        for event in available_excursions:
                            self.webDriver.scroll(pixel_x=event.location['x'], pixel_y=event.location['y'])
                            self.webDriver.wait_for(3)
                            event.click()
                            test_data['booked_excursion_name'] = event.text
                            test_data['bookable_excursion_available'] = True
                            break
                        break
                    else:
                        self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
            else:
                test_data['bookable_excursion_available'] = False

    def book_excursion(self):
        """
        Function to click book button on details of a bookable event
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.click_book_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.click_book_button, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.select_second_sailor,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.time_slots, locator_type='xpath'):
            time_slots = self.webDriver.get_elements(element=self.locators.time_slots, locator_type='xpath')
            for slot in time_slots:
                slot.click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_button, locator_type='xpath')