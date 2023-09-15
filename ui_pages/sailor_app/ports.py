__author__ = 'vanshika.arora'

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
            "click_book_excursion": "//button[@id='ShowPortexcursions-0']",
            "all_events": "//div[@class='EventCard__name']",
            "click_book_button": "//button[@id='mainButton']",
            "select_second_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            "add_card_and_pay": "//button[@id='ExcursionsPaymentSummary__confirmButton']",
            "back_button": "//button[@id='back-btn']",
            "event_category": "//div[@class='EventCard__category']",
            "select_filter": "//span[text()='%s']",
            "remove_filter": "//button[@id='ResetInlineFilter']",
        })

    def click_book_excursion(self):
        """
        Function to click Book excursions button
        :return:
        """
        self.webDriver.click(element=self.locators.click_book_excursion, locator_type='xpath')

    def select_and_open_excursion_event(self, test_data):
        """
        To select and open lineup event
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        get_all_events = self.webDriver.get_elements(
            element=self.locators.all_events, locator_type='xpath')
        for i in get_all_events:
            test_data['booked_excursion_name'] = i.text
            # contexts = self.webDriver.get_contexts()
            # self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            # self.webDriver.scroll_mobile(x_press=696, y_press=778, x_move=673, y_move=1551)
            # contexts = self.webDriver.get_contexts()
            # self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            i.click()
            break

    def book_excursion(self):
        """
        Function to click book button on details of a bookable event
        :return:
        """
        self.webDriver.click(element=self.locators.click_book_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_second_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def verify_availability_of_book_a_shore_thing_button(self):
        """
        Function to verify that book a shore thing button is available on the screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.click_book_excursion, locator_type='xpath'):
            logger.debug("Book a shore thing button is available on screen, hence user has landed on ports listing screen")
        else:
            raise Exception("Book a shore thing button is not available on screen, hence user has not landed on ports listing screen")

    def click_back_button(self):
        """
        Function to click back button on ports listing screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_events_categories_available(self, test_data):
        """
        Function to get categories of available events
        :param test_data:
        :return:
        """
        test_data['excursion_available_categories'] = []
        excursion_categories = []
        event_category = self.webDriver.get_elements(element=self.locators.event_category, locator_type='xpath')
        for category in event_category:
            category_name = category.text.split(',')
            for i in category_name:
                if i not in excursion_categories:
                    excursion_categories.append(i)
        for i in excursion_categories:
            test_data['excursion_available_categories'].append(str(i).replace(' ', ''))

    def apply_filter_and_verify(self, test_data):
        """
        Function to apply filter and verify
        :param test_data:
        :return:
        """
        flag = 0
        for cat in test_data['excursion_available_categories']:
            while self.webDriver.is_element_display_on_screen(element=self.locators.select_filter % cat.strip().capitalize(),
                                                               locator_type='xpath'):
                contexts = self.webDriver.get_contexts()
                self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
                self.webDriver.scroll_mobile(1117, 1025, 150, 1112)
                flag += 1
                if flag == 3:
                    break
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            self.webDriver.click(element=self.locators.select_filter % cat.strip().capitalize(), locator_type='xpath')
            event_category = self.webDriver.get_elements(element=self.locators.event_category, locator_type='xpath')
            for category in event_category:
                category_name = category.text.split(',')
                category_list=[]
                for i in category_name:
                    category_list.append(str(i).replace(' ',''))
                if cat in category_list:
                    logger.debug("Events are available for selected filters")
                else:
                    raise Exception("Events are not available for selected filter")
            self.webDriver.click(element=self.locators.remove_filter, locator_type='xpath')
