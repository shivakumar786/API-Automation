__author__ = 'prahlad.sharma'

from virgin_utils import *


class Dashboard(General):
    """
    Page Class for Incident Management Dashboard page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Dashboard page
        :param web_driver:
        :param test_data:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "dashboard_title": "//div[@class='incidentscreen-title']",
            "create_incident": "//button[@class='button is-primary is-fullwidth is-large ']/span[text()='CREATE']",
            "tab": "//a[contains(text(),'%s')]",
            "left_navigation": "//div[@id='dashboardBtn']/div/span[text()='%s']",
            "no_data": "//span[text()='No Incidents to Display']",
            "filter_icon": "//div[@class='incident-filters']//img[@class='SVGContainer ']",
            "get_active_tab": "//li[@class='is-active']",
            "search_textbox": "searchfield",
            "search_button": "//div[@class='search-icon']/img",
            "close_button": "//div[@class='close-icon']/img",
            "search_result": "//div[@class='incident-search-card']",
            "sort": "//span[text()='%s']",
            "incident_creation_time": "//span[text()='VIR #']/../../following-sibling::div/span",
            "incident_vir_value": "//span[text()='VIR #']/../following-sibling::span",
            "severity_status": "//span[text()='Severity:']/../following-sibling::span[@class='incidentdetails-statusvalue']",
            "priority_status": "//span[text()='Priority:']/../following-sibling::span[@class='incidentdetails-statusvalue']",
            "progress_bar_resolved_count": "//*[text()=' Incident Resolved']/../../div/span[1]",
            "progress_bar_total_count": "//*[text()=' Incident Resolved']/../../div/span[2]",
            "closed_count": "//*[contains(text(), 'CLOSED')]",
            "all_incident_count": "//*[contains(text(), 'ALL INCIDENTS')]"

        })

    def verify_dashboard_page(self):
        """
        Verify user is able to open the Dashboard page after login
        :return:
        """
        self.webDriver.allure_attach_jpeg('just_land_dashboard')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_title, locator_type='xpath'):
            logger.debug("User land on Dashboard page")
        else:
            raise Exception("User not land on Dashboard page")

    def open_tab(self, tab_name):
        """
        Function to open the specified tab
        :param tab_name:
        :return:
        """
        self.webDriver.click(element=self.locators.tab % tab_name, locator_type='xpath')

    def click_create_incident_button(self):
        """
        Function to click on create button
        :return:
        """
        self.webDriver.click(element=self.locators.create_incident, locator_type='xpath')

    def check_availability_of_incident(self):
        """
        Function to check the incident available or not
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_data, locator_type='xpath'):
            return False
        else:
            return True

    def get_active_tab_value(self):
        """
        Function to get the active tab value
        :return:
        """
        return self.webDriver.get_text(element=self.locators.get_active_tab, locator_type='xpath')

    def open_assigned_tab(self):
        """
        Function to open the assigned tab
        :return:
        """
        all_list = self.webDriver.get_elements(element=self.locators.tab % 'ASSIGNED', locator_type='xpath')
        for status in all_list:
            status.click()
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)

    def search_incident(self, value):
        """
        Function to search the Incident
        :param value:
        :return:
        """
        self.webDriver.set_text(element=self.locators.search_textbox, locator_type='name', text=value)
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_result, locator_type='xpath',
                                                      time_out=10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_result, locator_type='xpath'):
            return False
        else:
            return True

    def click_close_icon(self):
        """
        Function to click on Close icon
        :return:
        """
        self.webDriver.click(element=self.locators.close_button, locator_type='xpath')

    def click_filter(self):
        """
        Function to click on filter icon
        :return:
        """
        self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
        self.webDriver.wait_for(2)

    def sort_by(self, value):
        """
        Function to perform sort by
        :param value:
        :return:
        """
        self.click_filter()
        self.webDriver.click(element=self.locators.sort % value, locator_type='xpath')
        self.webDriver.click(element=self.locators.sort % 'apply', locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=90)

    def verify_severity_on_details(self):
        """
        Function to check the sorting
        :return:
        """
        return int(self.webDriver.get_text(element=self.locators.severity_status, locator_type='xpath'))

    def verify_priority_on_details(self):
        """
        Function to check the priority
        :return:
        """
        return int(self.webDriver.get_text(element=self.locators.priority_status, locator_type='xpath'))

    def get_vir_value(self):
        """
        Function to get the vir value
        :return:
        """
        all_list = self.webDriver.get_elements(element=self.locators.incident_vir_value, locator_type='xpath')
        for status in all_list:
            self.test_data['vir_value'] = status.text
            break

    def get_progress_bar_resolved_count(self):
        """
        To get the progress bar resolved count
        :return:
        """
        count = self.webDriver.get_text(element=self.locators.progress_bar_resolved_count, locator_type="xpath")
        return count

    def get_progress_bar_total_count(self):
        """
        To get total count from progress bar
        :return:
        """
        progress_bar_count = self.webDriver.get_text(element=self.locators.progress_bar_total_count, locator_type="xpath")
        count = ""
        for closed_count in progress_bar_count:
            if closed_count.isdigit():
                count = count + closed_count
        return count

    def closed_count(self):
        """
        To get total closed count
        :return:
        """
        closed_incident = self.webDriver.get_text(element=self.locators.closed_count, locator_type="xpath")
        count = ""
        for closed_count in closed_incident:
            if closed_count.isdigit():
                count = count+closed_count
        return count

    def all_incident_count(self):
        """
        To get all incident count
        :return:
        """
        all_incident = self.webDriver.get_text(element=self.locators.all_incident_count, locator_type="xpath")
        count = ""
        for closed_count in all_incident:
            if closed_count.isdigit():
                count = count + closed_count
        return count
