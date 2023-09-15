__author__ = 'mohit.raghav'

from virgin_utils import *


class Discover(General):
    """
    Page class for Discover page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "lineup_events": "//div[@class='EventCard__name']",
            'loading': '//img[@alt="loading..."]',
            "back_button": "//*[@resource-id='back-btn']",
            "loader": "//*[@text='loading...']",
            "search_in_discover": "//div[@class='SearchBar__placeholder']",
            "search_input": "//input[@id='SearchInput']",
            "search_result": "//div[text()='Razzle Dazzle Restaurant']",
            "search_bar": "//div[@class='SearchBar__placeholder']",
            'close_discover_search': "//*[@resource-id='back-close-btn']",
            "open_lineup": "//*[@id='DiscoveryMenuItem-0']//span",
            'current_date_lineup': "//div[@class='LineupPager__dayItems-item__wrapper LineupPager__dayItems-item__wrapper--active']",
            'dates_available': "//div[@class='LineupPager__dayItems-item__wrapper']",
            "event_title": "//h1[contains(@class,'PageTitle')]",
            "click_love_btn": "//button[@id='LikeBtn']",
            'add_to_agenda_btn': "//*[@id='bookButton']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            'ship_spaces_btn': "//span[text()='Ship spaces']",
            "open_shore_things": "//*[@id='DiscoveryMenuItem-2']/span",
            'spa_header': "//div[@class='ActivityDetailsHeroWithStatus__title']"
            })

    def verify_availability_of_lineup_events(self):
        """
        Function to verify availability of lineup events
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_complete_page_top()
        get_all_lineup_events = self.webDriver.get_elements(element=self.locators.lineup_events, locator_type='xpath')
        assert len(get_all_lineup_events) > 0, "No lineup event is available"

    def click_back_button(self):
        """
        Function to click back button on ship spaces screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def verify_availability_of_search_bar(self):
        """
        Function to verify that search bar is available on discover screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_in_discover, locator_type='xpath'):
            logger.debug("Search bar is not available on discover screen")
        else:
            raise Exception("Search bar is not available on discover screen")

    def search_keyword(self):
        """
        Function to search keyword in search bar
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.click(element=self.locators.search_bar, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.search_input, locator_type='xpath', text="Razzle Dazzle")
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')

    def verify_search_results(self):
        """
        Function to verify search results
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.search_result,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_result, locator_type='xpath'):
            logger.info("Search results are available in discover search")
        else:
            raise Exception("Search results are not available in discover search")

    def close_discover_search(self):
        """
        Function to close discover search results
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.close_discover_search,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.close_discover_search, locator_type='xpath')

    def open_lineup(self):
        """
        To open lineup section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.open_lineup,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.open_lineup, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.open_lineup, locator_type='xpath')

    def select_and_open_lineup_event(self, test_data):
        """
        To select and open lineup event
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_for(3)
        available_lineup_events = self.webDriver.get_elements(element=self.locators.lineup_events, locator_type='xpath')
        test_data['lineup_available'] = True
        if len(available_lineup_events) == 0:
            dates = []
            current_date = int(self.webDriver.get_text(element=self.locators.current_date_lineup, locator_type='xpath'))
            dates_on_page = self.webDriver.get_elements(element=self.locators.dates_available,
                                                        locator_type='xpath')
            for day in dates_on_page:
                date = int(day.text)
                if date > current_date:
                    day.click()
                    self.webDriver.wait_for(3)
                    available_lineup_events = self.webDriver.get_elements(element=self.locators.lineup_events,
                                                                          locator_type='xpath')
                    test_data['lineup_available'] = True
                    break
            else:
                test_data['lineup_available'] = False
        for event in available_lineup_events:
            test_data['booked_lineup_name'] = event.text
            self.webDriver.wait_for(2)
            self.webDriver.scroll(pixel_x=event.location['x'], pixel_y=event.location['y'])
            event.click()
            break

    def add_to_love_list(self, test_data):
        """
        To add event to love list
        :param test_data:
        :return:
        """
        test_data['love_list_events'] = []
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.event_title, locator_type='xpath')
        event_title = self.webDriver.get_text(element=self.locators.event_title, locator_type='xpath')
        test_data['love_list_events'].append(event_title)
        self.webDriver.click(element=self.locators.click_love_btn, locator_type='xpath')

    def book_lineup(self):
        """
        Function to click Add to Agenda btn on details of a bookable event
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.add_to_agenda_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.add_to_agenda_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_button, locator_type='xpath')
        
    def open_ship_spaces(self):
        """
        To open ship spaces section
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ship_spaces_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_spaces_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.ship_spaces_btn,
                                                               locator_type='xpath')

    def open_shore_things(self):
        """
        To open shore things section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.open_shore_things, locator_type='xpath')
        self.webDriver.click(element=self.locators.open_shore_things, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.open_shore_things,
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