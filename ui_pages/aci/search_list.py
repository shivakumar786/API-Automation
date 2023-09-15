__author__ = 'sarvesh.singh'

from virgin_utils import *


class SearchList(General):
    """
    Page class for Search list
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "no_result": "//*[@text='No Record(s) Available']",
                "spinner": "com.decurtis.dxp.gangway:id/progressBar1",
                "search_page": "com.decurtis.dxp.aci:id/search_src_text",
                "search_results": "//*[@resource-id='com.decurtis.dxp.aci:id/item_guest']",
                "check_in": "//*[@resource-id='com.decurtis.dxp.aci:id/primary_action'][%s]",
                "check_in_page": "//*[@text='CHECK-IN']",
                "citizenship": "//*[@resource-id='com.decurtis.dxp.aci:id/gender_age_and_country_name'][%s]",
            })
        else:
            self.locators = self.dict_to_ns({
                "no_result": "//*[@text='No Record(s) Available']",
                "spinner": "com.decurtis.dxp.gangway.:id/progressBar1",
                "search_page": "com.decurtis.dxp.aci.dclnp:id/search_src_text",
                "search_results": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/item_guest']",
                "check_in": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/primary_action'][%s]",
                "check_in_page": "//*[@text='Check-in']",
                "citizenship": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/gender_age_and_country_name'][%s]",
            })

    def select_sailor(self):
        """
        To select sailor from search list
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_results, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.search_results, locator_type='xpath')

    def check_availability_of_search_result(self):
        """
        Function to check the availability of search result page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_result, locator_type='xpath')

    def check_availability_of_search_page(self):
        """
        Function to check the availability of search page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_page, locator_type='id',
                                                      time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.search_page,
                                                           locator_type='id')

    def get_search_results(self):
        """
        Func to get all available results
        :return:
        """
        return self.webDriver.get_elements(element=self.locators.search_results, locator_type='xpath')

    def click_check_in(self, index):
        """
        Function to click on check in button
        :param index
        """
        elements = self.webDriver.get_elements(element=self.locators.check_in % 1, locator_type='xpath')
        elements[index - 1].click()
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=60)

    def check_us_citizen(self):
        """
        Func to check is cabin has us citizen
        :return:
        """
        flag = False
        try:
            elements = self.webDriver.get_elements(element=self.locators.citizenship % 1, locator_type='xpath')
            for _element in elements:
                if _element.text.split('|')[1].strip() == 'United States':
                    flag = True
                else:
                    flag = False
                    break
            return flag
        except:
            return flag
