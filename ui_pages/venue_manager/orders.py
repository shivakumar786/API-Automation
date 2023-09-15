__author__ = 'HT'

from virgin_utils import *


class VenueManagerOrders(General):
    """
    Page Class for Venue Manager Orders Page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "filter_by_type": "//*[text()='All']",
            "filter_by": "//*[@class='multiselect-container dropdown-menu']/li",
            "all": "//*[@class='multiselect-container dropdown-menu']/li[1]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "active_order_list": "//*[@id='orderStatusReport']/tbody/tr",
            "no_order_found": "//*[text()='No record found.']",
            "voyage_details": "voyage-details",
            "filter_type": "filterType",
            "filter_date": "filterDate",
            "active": "active",
            "delivered": "delivered",
            "cancelled": "canceled",
            "oder_search_button": "orderSearchButton",
            "available_orders": "//*[@class='orderStatusReport_Model']",
            "selected_filter": "(//*[text()='%s'])[2]",
            "filter_by_date_btn": "voyage-itineraries",
            "date_list": "(//*[contains(text(),'Day 2')])[2]",
            "get_selected_date_title": "//*[@id='filterByDate']/following-sibling::div/button",
            "voyage_filter_icon": "update-icon",
            "voyage_drop_down": "custom-dropdown-style",
            "future_voyage": "(//*[@class='custom-options'])[5]",
            "orders_list": "(//*[@id='orderStatusReport']/tbody/tr/td[3])[2]",
            "search_box": "txtSearchBox"

        })

    def currently_selected_filter(self, filter_name):
        """
        get the filter selected in the menu items
        """
        return self.webDriver.get_text(element=self.locators.selected_filter % filter_name, locator_type="xpath")

    def click_on_filter_by_type(self, filter_type):
        """
        Function to filter by all, preorders, sailor orders, crew orders
        :param filter_type:
        """
        self.webDriver.click(element=self.locators.filter_by_type, locator_type="xpath")
        elements = self.webDriver.get_elements(element=self.locators.filter_by, locator_type="xpath")
        for type in elements:
            filter_by = type.text
            if filter_type == "All" and filter_by == "All":
                break
            elif filter_type == "Orders" and filter_by == "Orders":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Orders", "failed to select filter"
                break
            elif filter_type == "Pre-Order Breakfast" and filter_by == "Pre-Order Breakfast":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Pre-Order Breakfast", "failed to select filter"
                break
            elif filter_type == "Crew Orders" and filter_by == "Crew Orders":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Crew Orders", "failed to select filter"
                break
            elif filter_type == "Sailor Orders" and filter_by == "Sailor Orders":
                self.webDriver.click(element=self.locators.all, locator_type="xpath")
                type.click()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                assert self.currently_selected_filter(filter_type) == "Sailor Orders", "failed to select filter"
                break
        else:
            raise Exception("Filter drop down not showing any names in list")

    def no_records_found(self):
        """
        No records found
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_order_found, locator_type="xpath")

    def to_verify_all_elements_in_order_details(self):
        """
        This function is to verify order details in orders tab
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_details, locator_type="id"):
            raise Exception("current sailing voyage details are not showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_type, locator_type="id"):
            raise Exception("filter by type is showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_date, locator_type="id"):
            raise Exception("filter by date is showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.active, locator_type="id"):
            raise Exception("active tab is showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.delivered, locator_type="id"):
            raise Exception("delivered tab is showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.cancelled, locator_type="id"):
            raise Exception("cancelled tab is showing up in order details page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.oder_search_button, locator_type="id"):
            raise Exception("oder search button is showing up in order details page")

    def to_verify_orders_in_order_details_page(self, tab_name):
        """
        This is to verify the order details in active delivered and cancelled tabs
        :param tab_name:
        :return:
        """
        if tab_name == "active":
            self.webDriver.allure_attach_jpeg("orders_in_active_tab")
        elif tab_name == "delivered":
            self.webDriver.allure_attach_jpeg("orders_in_delivered_tab")
        else:
            self.webDriver.allure_attach_jpeg("orders_in_cancelled_tab")

    def to_click_on_tab_in_orders_page(self, tab_name):
        """
        To verify and click on tab
        :param tab_name:
        :return:
        """
        if tab_name == "active":
            self.webDriver.click(element=self.locators.active, locator_type="id")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
        elif tab_name == "delivered":
            self.webDriver.click(element=self.locators.delivered, locator_type="id")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
        else:
            self.webDriver.click(element=self.locators.cancelled, locator_type="id")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)

    def to_verify_filter_order_by_date(self):
        """
        To verify order can be filtered by date filter option
        :return:
        """
        self.webDriver.click(element=self.locators.filter_by_date_btn, locator_type="id")
        self.webDriver.click(element=self.locators.date_list, locator_type="xpath")
        day_verification = self.webDriver.get_attribute(element=self.locators.get_selected_date_title,
                                                        locator_type="xpath", attribute_name="title")
        assert day_verification[:5] == "Day 2", "order by date filter is not working fine"

    def to_verify_order_filter_by_voyage(self):
        """
        To verify order filter by voyage
        :return:
        """
        self.webDriver.click(element=self.locators.voyage_filter_icon, locator_type="id")
        self.webDriver.click(element=self.locators.voyage_drop_down, locator_type="id")
        self.webDriver.click(element=self.locators.future_voyage, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        day_verification = self.webDriver.get_attribute(element=self.locators.get_selected_date_title,
                                                        locator_type="xpath", attribute_name="title")
        assert day_verification[:5] == "Day 1", "order by date filter is not working fine"

    def search_for_order(self):
        """
        search for orders from global search
        :return:
        """

        self.webDriver.clear_text(element=self.locators.search_box, locator_type="id", action_type="clear")
        no_records = self.no_records_found()
        if not no_records:
            order_id = self.webDriver.get_text(element=self.locators.orders_list, locator_type="xpath")
            self.webDriver.set_text(element=self.locators.search_box, locator_type="id", text=order_id)
            self.webDriver.click(element=self.locators.oder_search_button, locator_type="id")
            order_list = self.webDriver.get_elements(element=self.locators.active_order_list, locator_type="xpath")
            assert len(order_list) != 0, f"failed to search {order_id} from global search"