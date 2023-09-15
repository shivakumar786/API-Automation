__author__ = 'Vanshika.Arora'

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
            "vip_filter": "//p[contains(text(),'Filter by loyalty level')]/parent::div//span[text()='%s']",
            "apply_filter": "//button/span[text()='APPLY']",
            "vip_img_src": "//div[@role='region']//img[@alt='vip']",
            "day_filter": "//span[text()='%s']",
            "filter_icon": "//p[contains(text(),'Filters')]/following-sibling::button",
            "filter_header_title": "//h6[text()='Filter']",
            "select_deck_cabin_search": "checkboxes-tags-demo",
            "select_cabin": "//*[text()='%s']",
            "select_all_decks": "//*[text()='Select All Decks']",
            "select_cta": "//*[text()='SELECT']",
            "decks_and_cabins": "//button/span[contains(text(),'DECKS & CABINS')]",
            "select_all_cabins": "//*[text()='Select All Cabins']",
            "calender_button": "//*[text()='From Date']/..//div/button",
            "select_date": "//*[@class='MuiPickersCalendar-week']/div//*[text()= '%s']",
            "calender_back_button": "//*[@class='MuiPickersCalendarHeader-switchHeader']/button",
        })

    def apply_vip_filters(self):
        """
        Function to apply all vip filters
        :return:
        """
        self.webDriver.click(element=self.locators.vip_filter % 'VIP1', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP2', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP3', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP4', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP5', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP6', locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.wait_for(2)

    def get_list_of_vip_filters(self, test_data):
        """
        Function to get list of vip filters
        :param test_data:
        :return:
        """
        test_data['loyalty_list'] = []
        vip_list = ['vip1', 'vip2', 'vip3', 'vip4', 'vip5', 'vip6']
        get_all_vip = []
        images = self.webDriver.get_elements(
            element=self.locators.vip_img_src, locator_type='xpath')
        for image in images:
            get_all_vip.append(image.get_attribute('src'))
        for i in vip_list:
            for j in get_all_vip:
                if i in j and i not in test_data['loyalty_list']:
                    test_data['loyalty_list'].append(i)

    def clear_filter(self):
        """
        Function to clear filter
        :return:
        """
        self.webDriver.click(element=self.locators.vip_filter % 'VIP1', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP2', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP3', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP4', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP5', locator_type='xpath')
        self.webDriver.click(element=self.locators.vip_filter % 'VIP6', locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')

    def apply_filter_and_verify(self, test_data, multiple_filter):
        """
        Function to apply filter and verify
        :param multiple_filter:
        :param test_data:
        :return:
        """
        if test_data['loyalty_list']:
            for i in range(len(test_data['loyalty_list'])):
                self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
                self.webDriver.click(element=self.locators.vip_filter % test_data['loyalty_list'][i].upper(), locator_type='xpath')
                self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
                images = self.webDriver.get_elements(element=self.locators.vip_img_src, locator_type='xpath')
                for image in images:
                    source = image.get_attribute('src')
                    if test_data['loyalty_list'][i] not in source:
                        raise Exception(f"Vips not available according to applied filter for {i}")
                self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header_title,
                                                              locator_type='xpath',
                                                              time_out=60)
                self.webDriver.click(element=self.locators.vip_filter % test_data['loyalty_list'][i].upper(),
                                     locator_type='xpath')
                if multiple_filter:
                    self.webDriver.click(element=self.locators.vip_filter % test_data['loyalty_list'][i].upper(),
                                         locator_type='xpath')
                    self.clear_filter_applied_for_deck()
                    element = self.webDriver.is_element_display_on_screen(element=self.locators.vip_img_src,
                                                                          locator_type="xpath")
                    assert element, "Failed to filter sailors with multiple filters options"
                    self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
                    self.webDriver.click(element=self.locators.vip_filter % test_data['loyalty_list'][i].upper(),
                                        locator_type='xpath')
                    self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
                else:
                    self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
                    element = self.webDriver.is_element_display_on_screen(element=self.locators.vip_img_src, locator_type="xpath")
                    assert element, "Failed to filter sailors with vip status"
        else:
            logger.debug('No Vips are available in support queue')

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
                self.webDriver.click(element=self.locators.calender_back_button, locator_type="xpath")
                self.webDriver.click(element=self.locators.select_date % select_day, locator_type="xpath")
            self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        else :
            self.webDriver.click(element=self.locators.day_filter % day, locator_type='xpath')
            self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')

    def apply_filter_for_cabin(self, cabin):
        """
        Apply filter for cabin using decks and cabins filter cta
        :return:
        """
        self.webDriver.click(element=self.locators.decks_and_cabins, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.select_deck_cabin_search, locator_type="id", text=cabin)
        self.webDriver.click(element=self.locators.select_deck_cabin_search, locator_type="id")
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ENTER).perform()
        self.webDriver.click(element=self.locators.select_cta, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_filter, locator_type="xpath")

    def clear_filter_applied_for_deck(self):
        """
        function to clear applied filter for deck and cabin
        :return:
        """
        self.webDriver.click(element=self.locators.decks_and_cabins, locator_type="xpath")
        self.webDriver.click(element=self.locators.select_all_decks, locator_type="xpath")
        self.webDriver.click(element=self.locators.select_cta, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_filter, locator_type="xpath")