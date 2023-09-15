__author__ = 'aatir.fayyaz'

from virgin_utils import *


class Filters(General):
    """
    Page class for Filters page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "filter_heading": "//*[@class='android.widget.TextView'][@text='Filter & Sort Incident']",
            "status": "//*[@class='android.widget.TextView'][contains(@text,'Select Status')]",
            "select_status": "//*[@class='android.view.View'][@text='%s']",
            "apply_filter": "//*[@text='Apply']",
            "sort": "//*[@class='android.view.View'][@text='%s']",
            "filter_result": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "back_to_incidents": "//*[@class='android.widget.Button'][contains(@text,'menu')]",
            "back_to_im_dashboard": "//*[@class='android.widget.Button'][contains(@text,'menu')]",
        })

    def closed_resolved_unresolved_status(self, test_data):
        """
        To get closed resolved/un-resolved incident count
        :param test_data:
        :return:
        """
        filter_list = []
        test_data['closed'] = []
        self.webDriver.click(element=self.locators.filter_by_status, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_status % 'Closed/Resolved', locator_type='xpath')
        self.webDriver.click(element=self.locators.select_status % 'Closed/Un-resolved', locator_type='xpath')
        self.webDriver.scroll_mobile(360, 600, 360, 300)
        self.webDriver.scroll_mobile(360, 600, 360, 300)
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        for i in range(10):
            filter_list.append(self.webDriver.get_text(element=self.locators.filter_result % 'Details of Incident',
                                                       locator_type='xpath'))
            self.webDriver.scroll_mobile(300, 1200, 300, 150)
        self.webDriver.click(element=self.locators.back_to_incidents, locator_type='xpath')
        self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
        for block in filter_list:
            for incident in block:
                if incident not in test_data['closed']:
                    test_data['closed'].append(incident)

    def sort_incident(self):
        """
        Function to perform sort by
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(300, 1200, 300, 150)
        self.webDriver.click(element=self.locators.sort % 'Sort by Creation Date', locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')

    def verify_sort_incident(self, value):
        """
        Function to verify sort by filter
        :param value:
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(300, 1000, 300, 800)
        self.webDriver.scroll_mobile(300, 800, 300, 1200)
        for i in range(10):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_result % f'Cabin {value}',
                                                               locator_type='xpath'):
                self.webDriver.scroll_mobile(300, 1200, 300, 150)
                continue
            self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
            self.webDriver.wait_for(5)
            break
        else:
            raise Exception('Sorting is not working as expected')
