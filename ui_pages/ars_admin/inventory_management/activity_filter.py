__author__ = 'Krishna'

from virgin_utils import *


class ActivityFilter(General):
    """
    To Initiate elements from activity filter tab
    """
    def __init__(self, web_driver, test_data):
        """
        Initiate web_driver and elements
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "shore_thing_check_box": "//*[@id='PA']/../div",
            "apply_btn": "//*[text()='APPLY']",
            "ent_inventoried": "//*[@id='IET']/../div",
            "ent_non_inventoried": "//*[@id='NET']/../div",
            "spa_events": "//*[@id='SPA']/../div",
            "clear_all": "//*[text()='CLEAR ALL']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "open_activities_filter": "//span[text()='Open']",
            "clear_filter": "//button[text()='CLEAR ALL']",
            "activity_slot_access_private": "//div[text()='Activity Slot "
                                            "Access']/parent::div/following-sibling::div//span[text()='Private']",
            "activity_access_private": "//div[text()='Activity Access']/parent::div/following-sibling::div//span["
                                       "text()='Private']",
        })

    def select_shore_thing(self):
        """
        select shore thing activities from filter
        """
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.click(element=self.locators.shore_thing_check_box, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=120)

    def filter_for_ent_inventoried_events(self):
        """
        filter for entertainment inventoried events
        """
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def filter_for_ent_non_inventoried_events(self):
        """
        filter for entertainment non inventoried events
        """
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_non_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=120)

    def filter_for_spa_activities(self):
        """
        filter for spa activities
        """
        self.webDriver.click(element=self.locators.clear_all, locator_type="xpath")
        self.webDriver.click(element=self.locators.spa_events, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def apply_filter_for_open_activities(self):
        """
        Apply filter for open activities
        :return:
        """
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.open_activities_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def filter_inventoried_activity_access_private(self):
        """
        To filter shore activity access private
        :return:
        """
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_access_private, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def filter_inventoried_activity_slot_access_private(self):
        """
        To filter inventoried activities with private access
        :return:
        """
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_slot_access_private, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def filter_non_inventoried_activity_access_private(self):
        """
        To filter shore activity access private
        :return:
        """
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_non_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_access_private, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def filter_non_inventoried_activity_slot_access_private(self):
        """
        To filter inventoried activities with private access
        :return:
        """
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_non_inventoried, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_slot_access_private, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)