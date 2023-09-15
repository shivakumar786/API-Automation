__author__ = 'HT'

from virgin_utils import *


class Menu(General):
    """
    Page Class for Venue Manager venue selection
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "menu": "//div[@class='col-md-12 order-list menu-list']/div/div/div",
            "expand_all": "//*[text()='Expand All']",
            "filter_by_type": "//*[text()='All']",
            "filter_by": "//*[@class='multiselect-container dropdown-menu']/li",
            "all": "//*[@class='multiselect-container dropdown-menu']/li[1]",
            "selected_filter": "(//*[text()='%s'])[2]",
        })

    def menu_item_list(self):
        """
        Get available menu items in list
        """
        return self.webDriver.get_elements(element=self.locators.menu, locator_type="xpath")

    def currently_selected_filter(self, filter_name):
        """
        get the filter selected in the menu items
        """
        return self.webDriver.get_text(element=self.locators.selected_filter % filter_name, locator_type="xpath")

    def verify_filter_function(self, filter_type):
        """
        Function to filter by all, pre orders, sailor orders, crew orders
        """
        self.webDriver.click(element=self.locators.filter_by_type, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        elements = self.webDriver.get_elements(element=self.locators.filter_by, locator_type="xpath")
        for type in elements:
            filter_by = type.text
            if filter_type == "All" and filter_by == "All":
                break
            elif filter_type == "Gluten Free" and filter_by == "Gluten Free":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Gluten Free", "failed to select filter"
                break
            elif filter_type == "Vegetarian" and filter_by == "Vegetarian":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Vegetarian", "failed to select filter"
                break
            elif filter_type == "Vegan" and filter_by == "Vegan":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Vegan", "failed to select filter"
                break
        else:
            raise Exception("Filter drop down not showing any names in list")

    def verify_expand_cta(self):
        """
        function to verify expand cta is enabled or not
        """
        cta_status = self.webDriver.is_element_enabled(element=self.locators.expand_all, locator_type="xpath")
        assert cta_status == True, "expand all cta is not enabled"