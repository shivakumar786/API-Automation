"""
* Copyright (c) 2019, DeCurtis Corporation. All rights reserved.
* DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
*    File name : vv-e2e-automation : test_13_moci.py
*    Author : Vishal Gupta
*    Creation Date: 21 April, 2023
"""
from virgin_utils import *


class Report:
    """
    Page Class For Repots To moci App
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver
        """
        self.webDriver = web_driver
        self.locators = General.dict_to_ns({
            "report_header": "//*[@class='heading report-heading' and text()='Reports']",
            "reports": "//div[text()='This report provides the statistics of sailor records approved and rejected by the Moderator.']",
            "select_date": "//*[text()='%s']",
            "date": "fromDate",
            "ship": "//div[@class='Select-placeholder']",
            "select_voyages": "//span[text()='Please Select']",
            "choose": "//label[text()=' All Voyages']",
            "apply": "apply",
            "moderation_report": "moderation-count",
            "moderation_report_header": "//*[text()='Report : Moderation by User']",
            "user": "//*[text()='User']",
            "user_box": "user-multiselectDropdown",
            "report1": "//*[text()='Sailor Records Moderation Status']",
            "report2": "//*[text()='Moderation by User']",
            "get_all_ship_names": "//div[@class='Select-menu-outer']",
            "click_ok": "//button[@id='popup-ok']",
            "click_cancel": "//button[@id='popup-cancel']",
            "pop_up_warning": "//div[@class='message']",
            "pop_up": "//div[@class='ReactModal__Content ReactModal__Content--after-open commonPopup router-prompt"
                      "-confirm-section']",
            "user_drop": "user-multiselectDropdown",
            "action": "action-multiselectDropdown",
            "ships": "ship-multiselectDropdown",
            "mod_form_date": "fromModerateCountDate",
            "mod_to_date": "toModerateCountDate",
            "dropdown_menu": "//ul[@class='multiselect-container dropdown-menu']",
            "sailedatefrom": "sailFromDateModerateCountReport",
            "sailedateto": "sailToDateModerateCountReport",
            "get_ship": "//div[@class='Select-menu-outer']",
            "filters": "//div[@class='col-xs-4']",
            "ids": "//input[@id='fromModerateCountDate']",
        })

    def verification_of_report_page(self):
        """
        To check the Reports page loaded or not
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.report_header, locator_type='xpath'):
            logger.debug("User is land on Report page of MOCI")
        else:
            raise Exception("User is not on Report page of MOCI")
        if self.webDriver.is_element_display_on_screen(element=self.locators.report1, locator_type='xpath'):
            logger.debug("User is land on Report page of MOCI and Sailor Records Moderation Status report is visible")
        else:
            raise Exception("User is land on Report page of MOCI and Sailor Records Moderation Status report is "
                            "not visible")
        if self.webDriver.is_element_display_on_screen(element=self.locators.report2, locator_type='xpath'):
            logger.debug("User is land on Report page of MOCI and Moderation by User report is visible")
        else:
            raise Exception("User is land on Report page of MOCI and Moderation by User report is not visible")

    def open_report(self):
        """
        lunch the report page.
        """
        self.webDriver.click(element=self.locators.reports, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship, locator_type='xpath')
        data = self.webDriver.get_elements(element=self.locators.get_all_ship_names, locator_type='xpath')[0].text
        if len(data) != 0:
            ships_name = data.split("\n")
            if 'Scarlet Lady' in ships_name:
                self.webDriver.enter_data_in_textbox_using_action(element=self.locators.ship, locator_type='xpath', text='Scarlet Lady')
            else:
                raise Exception("Scarlet Lady name is missing in Ship name")
        else:
            raise Exception("Ship name is not visible or not clickable")
        self.webDriver.click(element=self.locators.date, locator_type='id')
        day = str(date.today().day)
        self.webDriver.click(element=self.locators.select_date % day, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_voyages, locator_type='xpath')
        self.webDriver.click(element=self.locators.choose, locator_type='xpath')
        if self.webDriver.is_element_enabled(element=self.locators.apply, locator_type='id'):
            self.webDriver.click(element=self.locators.apply, locator_type='id')
            self.webDriver.explicit_visibility_of_element(element=self.locators.apply, locator_type='id', time_out=20)
            value = self.webDriver.get_text(element=self.locators.reports, locator_type='xpath')
            if value != 'This report provides the statistics of sailor records approved and rejected by the Moderator.':
                raise Exception("Report page is not opened")
                self.webDriver.allure_attach_jpeg('Report page is not opened or reports data is not visible!!')
            else:
                self.webDriver.allure_attach_jpeg('Report page is opened and data is visible!!')
        else:
            raise Exception("Ship name is not visible or not clickable")

    def moderate_by_user_report_is_visible(self):
        """
        Verify theModeration by user report is visible
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.moderation_report, locator_type='id'):
            report_name = self.webDriver.get_text(element=self.locators.moderation_report, locator_type='id')
            if "Moderation by User" in report_name and "This report provides the statistics of number of records " \
                                                       "approved, rejected and marked as Review Later by the " \
                                                       "Moderator over a period of time." in report_name:
                self.webDriver.click(element=self.locators.moderation_report, locator_type='id')
            else:
                logger.debug("Moderation by user Report name has been changed !!")
        else:
            raise Exception("Moderation by user Report is not visible on report section !!!")

    def open_moderate_by_user_reports(self):
        """
        Verify the reports has been open or not
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.moderation_report_header, locator_type='xpath'):
            raise Exception("After open the Moderation by user Report the header title does not matched. ")

    def clear_pop_up(self):
        """
        Click on Ok on Pop-Up, when we move to report section to another Tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.pop_up, locator_type='xpath'):
            if self.webDriver.is_element_enabled(element=self.locators.click_ok, locator_type='xpath') and \
                    self.webDriver.is_element_enabled(element=self.locators.click_cancel, locator_type='xpath'):
                self.webDriver.allure_attach_jpeg('Check Report move Pop-Up')
                self.webDriver.click(element=self.locators.click_ok, locator_type='xpath')
            else:
                self.webDriver.allure_attach_jpeg('Yes Button or Cancel button should we disabled !! ')
                raise Exception("report Pop-up Yes Button or Cancel button should we disabled !!")
        else:
            self.webDriver.allure_attach_jpeg('Pop-up is not visible when Move to another tab from report.')
            raise Exception("Pop-up is not visible when Move to another tab from report.")

    def moderate_by_user_report_fields(self):
        """
        Verify the Moderate by user report fields
        :return:
        """

        data = self.webDriver.get_inner_html(element=self.locators.ids, locator_type='id')
        for i, filter_name in enumerate(data):
            print(i,filter_name)
