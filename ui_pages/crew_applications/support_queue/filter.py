__author__ = 'aatir.fayyaz'

from selenium.webdriver.common.keys import Keys

from virgin_utils import *


class Filter(General):
    """
    Page Class for Filter in Support Queue
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Filter window
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "request_button": "//*[contains(@text,'%s')]",
            "filter_header_title": "//*[@class='android.widget.Button'][contains(@text,'logo')]",
            "day_filter": "//*[@class='android.widget.TextView'][@text='%s']",
            "date_range": "//*[@class='android.widget.RadioButton'][@text='Date Range']",
            "calender_button": "//*[@class='android.widget.Button'][contains(@text,'change date')]",
            "select_date": "//*[@class='android.widget.Button'][@text='%s']",
            "decks_and_cabins": "//*[@class='android.widget.Button'][contains(@text,'Decks & Cabins')]",
            "select_all_cabins": "//*[@class='android.widget.TextView'][contains(@text,'Select All Cabins')]",
            "cabins": "//*[@class='android.widget.TextView']",
            "get_cabins": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "Done_button": "//*[@class='android.widget.Button'][contains(@text,'DONE')]",
            "apply_filter": "//*[@class='android.widget.Button'][contains(@text,'APPLY')]",
            "clear_all": "//*[@class='android.widget.Button'][@text='CLEAR ALL']",
            "multiple_filter": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "verify_filter": "//*[@class='android.widget.Image'][contains(@text,'vip')]",
        })

    def apply_filter_for_day(self, day, test_data):
        """
        Function to apply filter for day
        :param test_data:
        :param day:
        :return:
        """
        if day == "Date Range":
            if test_data['firstDay'][-2:] < '10':
                select_day = test_data['firstDay'][-1:]
            else:
                select_day = test_data['firstDay'][-2:]
            self.webDriver.click(element=self.locators.day_filter % day, locator_type='xpath')
            self.webDriver.click(element=self.locators.calender_button, locator_type="xpath")
            try:
                self.webDriver.click(element=self.locators.select_date % select_day, locator_type="xpath")
            except(Exception, ValueError)as exp:
                self.webDriver.submit()
                self.webDriver.click(element=self.locators.select_date % select_day, locator_type="xpath")
            self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.day_filter % day, locator_type='xpath')
            self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')

    def apply_filter_for_deck_cabin(self, test_data):
        """
        Apply filter and get list for cabin using decks and cabins filter cta
        :param test_data:
        :return:
        """
        test_data['cabins'] = []
        self.webDriver.click(element=self.locators.day_filter % 'All', locator_type="xpath")
        self.webDriver.click(element=self.locators.decks_and_cabins, locator_type="xpath")
        self.webDriver.click(element=self.locators.select_all_cabins, locator_type="xpath")
        for i in range(2):
            cabins = self.webDriver.get_elements(element=self.locators.cabins, locator_type='xpath')
            for cabin in cabins[4:]:
                if cabin.get_attribute('text') not in test_data['cabins']:
                    test_data['cabins'].append(cabin.get_attribute('text'))
            self.webDriver.scroll_mobile(300, 1197, 300, 283)
        self.webDriver.click(element=self.locators.Done_button, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_filter, locator_type="xpath")

    def verify_deck_cabin_filters(self, test_data):
        """
        Function to verify decks & cabins filter
        :param test_data:
        :return:
        """
        request_list = ['NEW', 'IN PROGRESS', 'RESOLVED']
        for request in request_list:
            self.webDriver.click(element=self.locators.request_button % request, locator_type='xpath')
            sailors = self.webDriver.get_elements(element=self.locators.cabins, locator_type='xpath')
            for sailor in sailors:
                if 'Cabin' in sailor.get_attribute('text') and sailor.get_attribute('text')[7:] not in \
                        test_data['cabins']:
                    raise Exception('filter is not working')

    def clear_filter_applied_for_deck_cabin(self):
        """
        function to clear applied filter for deck and cabin
        :return:
        """
        self.webDriver.click(element=self.locators.decks_and_cabins, locator_type="xpath")
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.Done_button, locator_type="xpath")
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.apply_filter, locator_type="xpath")
        self.webDriver.wait_for(2)

    def vip_filters(self):
        """
        Function to apply vip filters
        :return:
        """
        vip = ['VIP1', 'VIP2', 'VIP3', 'VIP4', 'VIP5', 'VIP6']
        for person in vip:
            self.webDriver.click(element=self.locators.multiple_filter % person, locator_type='xpath')

    def filter_by_owner(self):
        """
        Function to apply Filter by Owner
        :return:
        """
        self.webDriver.click(element=self.locators.multiple_filter % 'Owned by me', locator_type='xpath')
        self.webDriver.click(element=self.locators.multiple_filter % 'No Owner', locator_type='xpath')

    def sort_by_filter(self):
        """
        Function to apply Sort by Filter
        :return:
        """
        sort_by_list = ['Create time', 'Responded time', 'Guest type']
        sort_by = random.choice(sort_by_list)
        self.webDriver.click(element=self.locators.multiple_filter % sort_by, locator_type='xpath')

    def apply_filters(self):
        """
        Function to apply all Filters
        :return:
        """
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.wait_for(2)

    def verify_filters(self):
        """
        Function to verify Filter results
        :return:
        """
        request_list = ['NEW', 'IN PROGRESS', 'RESOLVED']
        for request in request_list:
            self.webDriver.click(element=self.locators.request_button % request, locator_type='xpath')
            sailors = self.webDriver.get_elements(element=self.locators.verify_filter, locator_type='xpath')
            for sailor in sailors:
                if not sailor.get_attribute('text') == 'vip':
                    raise Exception('filter is not working')

    def clear_all_filters(self):
        """
        Function to clear all filters
        :return:
        """
        vip = ['VIP1', 'VIP2', 'VIP3', 'VIP4', 'VIP5', 'VIP6']
        for i in vip:
            self.webDriver.click(element=self.locators.multiple_filter % i, locator_type='xpath')
        self.webDriver.click(element=self.locators.multiple_filter % 'Owned by me', locator_type='xpath')
        self.webDriver.click(element=self.locators.multiple_filter % 'No Owner', locator_type='xpath')
        self.webDriver.click(element=self.locators.multiple_filter % 'Create time', locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.wait_for(2)