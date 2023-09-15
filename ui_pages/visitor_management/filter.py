__author__ = 'prahlad.sharma'

from virgin_utils import *


class Filter(General):
    """
    Page class for Filter popup
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "start_date": "//span[contains(text(),'Start Date')]/../preceding-sibling::div/div["
                          "@class='react-datepicker__input-container']/input",
            "end_date": "//span[contains(text(),'End Date')]/../preceding-sibling::div/div["
                        "@class='react-datepicker__input-container']/input",
            "select_date": "//div[@class='react-datepicker__week']/div[text()='%s']",
            "month_dd": "//select[@class='react-datepicker__month-select']",
            "year_dd": "//select[@class='react-datepicker__year-select']",
            "start_date_calendar_icon": "//span[contains(text(),'Start Date')]/../following-sibling::img["
                                        "@class='SVGContainer calendar-icon']",
            "end_date_calendar_icon": "//span[contains(text(),'End Date')]/../following-sibling::img["
                                      "@class='SVGContainer calendar-icon']",
            "duration": "//button[contains(text(),'Duration')]",
            "boarding_type": "//button[contains(text(),'Boarding Type')]",
            "visit_status": "//button[contains(text(),'Visit Status')]",
            "visit_type": "//button[contains(text(),'Visitor Type')]",
            "visit_purpose": "//button[contains(text(),'Visit Purpose')]",
            "department": "//button[contains(text(),'Department')]",
            "reviewer": "//button[contains(text(),'Reviewer')]",
            "port": "//button[contains(text(),'Port')]",

            "general_boarding": "//label[contains(text(),'General Boarding')]",
            "early_boarding": "//label[contains(text(),'Early Boarding')]",

            "approval_pending": "//span[contains(text(),'Pending Approval')]",
            "approved": "//span[contains(text(),'Approved')]",
            "rejected": "//span[contains(text(),'Rejected')]",
            "cancel": "//button[contains(text(),'Cancel')]",
            "apply": "//button[contains(text(),'Apply')]",
            "sailor_apply": "//span[contains(text(),'Apply')]",

            "dynamic_filter_name": "//span[contains(text(),'%s')]",

            "sailor_check_in_status": "//button[contains(text(),'Check-in Status')]",
            "sailor_age_range": "//button[contains(text(),'Age Range')]",
            "sailor_checked_in_status": "//button[contains(text(),'Check-In Status')]",
            "sailor_boarding_status": "//button[contains(text(),'Boarding Status')]",
            "sailor_alert": "//button[contains(text(),'Alert')]",
            "sailor_special_assistance": "//button[contains(text(),'Special Assistance')]",
            "sailor_citizenship": "//button[contains(text(),'Citizenship')]",

            "checked_in_radio": "//input[@id='CHECKED_IN']/following-sibling::label",
            "not_checked_in_radio": "//label[contains(text(),'Not Checked-in')]",
            "Online_Check_in_complete": "//label[contains(text(),'Online Check-in complete')]",

            "country_name_path": "//span[contains(text(),'%s')]",
            "select_group": "//button[contains(text(),'Groups')]",
            "group_name": "//span[text()='%s']"

        })

    def click_duration(self):
        """
        Function to click on Duration filter
        """
        self.webDriver.click(element=self.locators.duration, locator_type='xpath')

    def select_start_date(self, s_date):
        """
        Function to select the start date
        :param s_date:
        """
        s_date = s_date.split("/")
        month = s_date[0]
        day = int(s_date[1])
        year = s_date[2]
        self.webDriver.click(element=self.locators.start_date_calendar_icon, locator_type='xpath')
        self.webDriver.wait_for(1)
        date_list = self.webDriver.get_elements(element=self.locators.select_date % str(day), locator_type='xpath')
        if len(date_list) <= 1:
            date_list[0].click()
        elif int(day) < 8 and len(date_list) > 1:
            date_list[0].click()
        else:
            date_list[1].click()

    def select_end_date(self, e_date):
        """
        Function to select the end date
        :param e_date:
        """
        e_date = e_date.split("/")
        month = e_date[0]
        day = int(e_date[1])
        year = e_date[2]
        self.webDriver.click(element=self.locators.end_date_calendar_icon, locator_type='xpath')
        self.webDriver.wait_for(1)
        date_list = self.webDriver.get_elements(element=self.locators.select_date % str(day), locator_type='xpath')
        if len(date_list) <= 1:
            date_list[0].click()
        elif int(day) < 8 and len(date_list) > 1:
            date_list[0].click()
        else:
            date_list[1].click()
        self.webDriver.allure_attach_jpeg('select_start_end_date')

    def select_assigned_group(self, test_data):
        """
        To select assigned group in filter
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.select_group, locator_type='xpath')
        self.webDriver.click(element=self.locators.group_name % test_data['report_data']['group'][-1], locator_type='xpath')

    def click_boarding_type(self):
        """
        Function to click on Boarding type filter
        """
        self.webDriver.click(element=self.locators.boarding_type, locator_type='xpath')

    def click_general_boarding(self):
        """
        Function to click on General Boarding type filter
        """
        self.webDriver.click(element=self.locators.general_boarding, locator_type='xpath')

    def click_early_boarding(self):
        """
        Function to click on early Boarding type filter
        """
        self.webDriver.click(element=self.locators.early_boarding, locator_type='xpath')

    def click_visit_status(self):
        """
        Function to click on Visit status filter
        """
        self.webDriver.click(element=self.locators.visit_status, locator_type='xpath')

    def click_approval_pending(self):
        """
        Function to click on approval pending
        """
        self.webDriver.click(element=self.locators.approval_pending, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('pending_approval')

    def click_approved(self):
        """
        Function to click on approval pending
        """
        self.webDriver.click(element=self.locators.approved, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('pending_approval')

    def select_department(self, department_name):
        """
        Function to click on select department
        :param department_name:
        """
        self.click_department()
        self.webDriver.click(element=self.locators.dynamic_filter_name % department_name, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('selected_department_approval')

    def select_port(self, port_name):
        """
        Function to click on select Ports
        :param port_name:
        """
        self.click_port()
        self.webDriver.click(element=self.locators.dynamic_filter_name % port_name, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('selected_port_approval')

    def click_approved(self):
        """
        Function to click on approved
        """
        self.webDriver.click(element=self.locators.approved, locator_type='xpath')

    def click_rejected(self):
        """
        Function to click on rejected
        """
        self.webDriver.click(element=self.locators.rejected, locator_type='xpath')

    def click_visit_type(self):
        """
        Function to click on visit type filter
        """
        self.webDriver.click(element=self.locators.visit_type, locator_type='xpath')

    def click_visit_purpose(self):
        """
        Function to click on visit purpose filter
        """
        self.webDriver.click(element=self.locators.visit_purpose, locator_type='xpath')

    def click_department(self):
        """
        Function to click on department filter
        """
        self.webDriver.click(element=self.locators.department, locator_type='xpath')

    def click_reviewer(self):
        """
        Function to click on reviewer filter
        """
        self.webDriver.click(element=self.locators.reviewer, locator_type='xpath')

    def click_port(self):
        """
        Function to click on port filter
        """
        self.webDriver.click(element=self.locators.port, locator_type='xpath')

    def click_apply(self):
        """
        Function to click on Apply button
        """
        self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('list_after_apply')

    def click_sailor_apply(self):
        """
        Function to click on Apply button at sailor filer popup
        """
        self.webDriver.click(element=self.locators.sailor_apply, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('list_after_apply_for_sailor')

    def click_cancel(self):
        """
        Function to click on cancel button
        """
        self.webDriver.click(element=self.locators.cancel, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def click_calendar_icon(self):
        """
        Function to click on cancel button
        """
        self.webDriver.click(element=self.locators.cancel, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def select_date(self):
        """
        Function to click on cancel button
        """
        self.webDriver.click(element=self.locators.cancel, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def click_citizenship(self):
        """
        Function to click on citizenship option
        """
        self.webDriver.click(element=self.locators.sailor_citizenship, locator_type='xpath')

    def select_country(self, country_name):
        """
        Function to select the country
        """
        self.webDriver.click(element=self.locators.country_name_path % country_name, locator_type='xpath')

    def click_checkin_status(self):
        """
        Function to click on checked in status option
        """
        self.webDriver.click(element=self.locators.sailor_checked_in_status, locator_type='xpath')

    def select_checked_in(self):
        """
        Function to select checked in radio
        """
        self.webDriver.click(element=self.locators.checked_in_radio, locator_type='xpath')

    def select_non_checked_in(self):
        """
        Function to select non checked in radio
        """
        self.webDriver.click(element=self.locators.not_checked_in_radio, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('not_checked_in_selected')
