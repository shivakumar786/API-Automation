__author__ = 'HT'

from virgin_utils import *


class VenueManagerDashboard(General):
    """
    Page Class for Venue Manager Dashboard
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "homepage_header": "//*[@id='dashboardContainer']//div[contains(text(),'Dashboard')]",
            "today": "todayCount",
            "last_hour": "lastHour",
            "custom": "customTabHeader",
            "delivery": "//*[@class='food-delivery']/span",
            "settings": "settings",
            "staff": "staff",
            "order": "reports",
            "report_and_matrix": "reportsandmetrics",
            "menu": "menuItems",
            "dashboard": "dashboard",
            "tabs": "//span[text()='%s']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "today_header": "//*[contains(text(),'%s')]",
            "today_tab_elements": "(//*[contains(text(), '{}')]/..//*[contains(text(),'%s')])[1]",
            "no_order_found": "//*[text()='No record found.']",
            "delivery_toggle_status": "foodDeliveryHidden",
            "toggle_button": "foodDelivery",
            "logout_icon":"userImage",
            "logout_button": "logOutBtn",
            "change":"//*[contains(text(),'Change')]",
            "dashboard_venue":"//*[@id='sideMenu']/div[1]",
            "reports_metrics": "reportsandmetrics"

        })

    def verify_homepage_header(self):
        """
        Get venue manager login page header
        """
        return self.webDriver.get_text(element=self.locators.homepage_header, locator_type='xpath')

    def verify_elements_on_dashboard(self):
        """
        To verify the element's availability on dashboard
        """
        status = self.webDriver.is_element_display_on_screen(element=self.locators.today, locator_type="id")
        if not status:
            raise Exception("today tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.last_hour, locator_type="id")
        if not status:
            raise Exception("last hour tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.custom, locator_type="id")
        if not status:
            raise Exception("last custom tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.delivery, locator_type="xpath")
        if not status:
            raise Exception("last delivery toggle is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.settings, locator_type="id")
        if not status:
            raise Exception("last settings tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.staff, locator_type="id")
        if not status:
            raise Exception("last staff tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.order, locator_type="id")
        if not status:
            raise Exception("last order tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.report_and_matrix, locator_type="id")
        if not status:
            raise Exception("last report_and_matrix tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.menu, locator_type="id")
        if not status:
            raise Exception("last menu tab is not displayed on screen")
        status = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard, locator_type="id")
        if not status:
            raise Exception("last dashboard tab is not displayed on screen")

    def verify_today_data_in_today_tab(self, element_in_today_tab):
        """
        To verify data available in today tab from dashboard
        :param element_in_today_tab:
        """
        general_data = ['Average Processing Time', 'Current Wait Time', 'Average Orders Per Server',
                        'Average Items Per Server']
        sailor_crew_orders_list = ['Pending', 'Prepared', 'Out for Delivery', 'Delivered', 'Delivered within time',
                                   'Delivered 15 mins early', 'Delivered 15 mins late', 'Canceled',
                                   'Partially Canceled']
        self.click_on_element_on_dashboard("today")
        if element_in_today_tab == 'GENERAL':
            loc = self.locators.today_tab_elements.format(element_in_today_tab)
            for element in general_data:
                status = self.webDriver.is_element_display_on_screen(element=loc % element, locator_type="xpath")
                if not status:
                    raise Exception(f"element {element} not found in {element_in_today_tab}")
        elif element_in_today_tab == "Crew Orders":
            loc = self.locators.today_tab_elements.format(element_in_today_tab)
            for element in sailor_crew_orders_list:
                status = self.webDriver.is_element_display_on_screen(element=loc % element, locator_type="xpath")
                if not status:
                    raise Exception(f"element {element} not found in {element_in_today_tab}")
        else:
            for element in sailor_crew_orders_list:
                loc = self.locators.today_tab_elements.format(element_in_today_tab)
                status = self.webDriver.is_element_display_on_screen(element=loc % element, locator_type="xpath")
                if not status:
                    raise Exception(f"element {element} not found in {element_in_today_tab}")

    def no_records_found(self):
        """
        No records found
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_order_found, locator_type="xpath")

    def element_availability_in_today_tab(self, element):
        """
        to check general, crew order, sailor order element in today tab
        :param element:
        """
        status = self.webDriver.is_element_display_on_screen(element=self.locators.today_header % element, locator_type="xpath")
        if status:
            return self.webDriver.get_text(element=self.locators.today_header % element, locator_type="xpath")
        else:
            return ''

    def click_on_hamburger_menu_tab(self, tab_name):
        """
        Click o any tab from hamburger menu
        :param tab_name:
        """
        self.webDriver.click(element=self.locators.tabs % tab_name, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_on_element_on_dashboard(self, tab_name):
        """
        To click on dashboard element today, last hour, custom
        :param tab_name:
        """
        if tab_name == 'today':
            self.webDriver.click(element=self.locators.today, locator_type='id')
        elif tab_name == 'last hour':
            self.webDriver.click(element=self.locators.last_hour, locator_type='id')
        else:
            self.webDriver.click(element=self.locators.custom, locator_type='id')

    def to_verify_data_on_dashboard(self, tab):
        """
        to verify data in today, last hour tabs
        :param tab:
        """
        if not self.no_records_found():
            element = self.element_availability_in_today_tab(element=tab)
            if element != '':
                if tab == 'GENERAL':
                    assert element == 'GENERAL', 'General element data not displayed'
                elif tab == 'Crew Orders':
                    assert element == 'CREW ORDERS', 'crew orders element data not displayed'
                else:
                    assert element == 'SAILOR ORDERS', 'sailor orders element data not displayed'

    def get_toggle_button_status(self):
        """
        To verify toggle button operation on dashboard
        """
        return self.webDriver.get_attribute(element=self.locators.delivery_toggle_status, locator_type="id", attribute_name="value")

    def perform_action_on_toggle_button(self):
        """
        click on toggle button
        """
        self.webDriver.click(element=self.locators.toggle_button, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def logout(self):
        """
        logout from venue manager
        """
        self.webDriver.click(element=self.locators.logout_icon, locator_type="id")
        self.webDriver.click(element=self.locators.logout_button, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_on_venue_change(self):
        """
        To click on venue change button
        """
        self.webDriver.click(element=self.locators.change, locator_type="xpath")

    def get_venue_visible_on_dashboard(self):
        """
        Venue selected on dashboard
        """
        return self.webDriver.get_text(element=self.locators.dashboard_venue, locator_type="xpath")

    def click_on_reports_and_metrics(self):
        """
        click o reports and metrics
        :return:
        """
        self.webDriver.click(self.locators.reports_metrics, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)