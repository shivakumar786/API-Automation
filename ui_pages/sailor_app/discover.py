__author__ = 'vanshika.arora'

from virgin_utils import *


class Discover(General):
    """
    Page class for rts page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "click_next_cta": "//*[@id='action_bar_root']",
            "open_lineup": "//*[@id='DiscoveryMenuItem-0']/span",
            "open_ship": "//*[@id='DiscoveryMenuItem-1']/span",
            "open_ports": "//*[@id='DiscoveryMenuItem-2']/span",
            "open_guides": "//*[@id='DiscoveryMenuItem-3']/span",
            "lineup_events": "//div[@class='EventCard__name']",
            "click_book_button": "//button[@id='bookButton']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            "click_like_button": "//button[@id='LikeBtn']",
            "event_title": "//h1[@class='PageTitle withHypen']",
            "back_button": "//button[@class='BackButton']/span",
            "port_card": "//div[@class='PortCard__card']",
            "lineup_days": "//div[@class='LineupPager__dayItem']/div",
            "port_name": "//div[@class='PortCard__card__name']",
            "port_name_on_port_guide": "/div[@class='Hero']/div[2]/div",
            "back": "back-btn",
            "spa_header": "//div[@class='ActivityDetailsHeroWithStatus__title']",
            'ship_spaces_btn': "//span[text()='Ship spaces']",
        })

    def open_lineup(self):
        """
        To open lineup section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.open_lineup, locator_type='xpath')

    def open_ship(self):
        """
        To open lineup section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.open_ship, locator_type='xpath')

    def open_ports(self):
        """
        To open ports section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.open_ports, locator_type='xpath')

    def open_guides(self):
        """
        Function to open guides
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.open_guides, locator_type='xpath')

    def select_and_open_lineup_event(self, test_data):
        """
        To select and open lineup event
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        get_all_lineup_events = self.webDriver.get_elements(
            element=self.locators.lineup_events, locator_type='xpath')
        for i in get_all_lineup_events:
            test_data['booked_lineup_name'] = i.text
            i.click()
            break

    def favourite_event(self, test_data):
        """
        To favourite the event and add to love list
        :param test_data:
        :return:
        """
        test_data['favourite_events'] = []
        event_title = self.webDriver.get_text(element=self.locators.event_title, locator_type='xpath')
        test_data['favourite_events'].append(event_title)
        self.webDriver.click(element=self.locators.click_like_button, locator_type='xpath')

    def book_lineup(self):
        """
        Function to click book button on details of a bookable event
        :return:
        """
        self.webDriver.click(element=self.locators.click_book_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def verify_availability_of_lineup_events(self):
        """
        Function to verify availability of lineup events
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.lineup_events, locator_type='xpath',
                                                      time_out=60)
        get_all_lineup_events = self.webDriver.get_elements(
            element=self.locators.lineup_events, locator_type='xpath')
        assert len(get_all_lineup_events) > 0, "Lineup events are not available for booking"

    def click_back_button(self):
        """
        Function to click back button
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_and_open_port_card(self, test_data):
        """
        Function to get port name and open port card
        :param test_data:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.lineup_days, locator_type='xpath'
                                                      , time_out=60)
        get_all_lineup_days = self.webDriver.get_elements(
            element=self.locators.lineup_days, locator_type='xpath')
        for day in get_all_lineup_days:
            day.click()
            if self.webDriver.is_element_display_on_screen(element=self.locators.port_card,
                                                        locator_type='xpath'):
                self.webDriver.explicit_visibility_of_element(element=self.locators.port_name, locator_type='xpath'
                                                              , time_out=60)
                port_name = self.webDriver.get_text(element=self.locators.port_name, locator_type='xpath')
                self.webDriver.click(element=self.locators.port_name, locator_type='xpath')
                port_name_on_port_guide = self.webDriver.get_text(element=self.locators.port_name_on_port_guide, locator_type='xpath')
                assert port_name.upper() == port_name_on_port_guide,"User is not able to access port guide"
                self.webDriver.click(element=self.locators.back, locator_type='id')
            else:
                continue

    def open_ship_spaces(self):
        """
        To open ship spaces section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ship_spaces_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_spaces_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.ship_spaces_btn,
                                                               locator_type='xpath')

    def add_spa_to_love_List(self, test_data):
        """
        To add spa to love list
        :param test_data:
        :return:
        """
        if 'love_list_events' not in test_data:
            test_data['love_list_events'] = []
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.spa_header, locator_type='xpath')
        event_title = self.webDriver.get_text(element=self.locators.spa_header, locator_type='xpath')
        test_data['love_list_events'].append(event_title)
        self.webDriver.scroll_till_element(element=self.locators.click_love_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.click_love_btn, locator_type='xpath')




