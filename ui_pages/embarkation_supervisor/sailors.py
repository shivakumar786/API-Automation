__author__ = 'prahlad.sharma'

from virgin_utils import *


class Sailorscrew(General):
    """
    Page Class for Sailor and Crew page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "sailor_arrow": "//tr[%s]//td[6]//button[1]//img[1]",
            "sailor_details_header": "//span[contains(text(),'Sailor Details')]",
            "crew_details_header": "//span[contains(text(),'Crew Details')]",
            "sailor_name": "//p[@class='is-size-5']",
            "citizenship_name": "//span[contains(text(),'Citizenship')]/../following-sibling::p",
            "reservation_number": "//span[contains(text(),'Reservation')]/../following-sibling::p",
            "cabin_number": "//span[contains(text(),'Cabin')]/../following-sibling::p",
            "checked_in_status": "//span[contains(text(),'Checked-In Status')]/../following-sibling::p",
            "boarding_slot": "//span[contains(text(),'Boarding Slot')]/../following-sibling::p",
            "filter": "//div[@class='filters']//img[contains(@class,'SVGContainer')]",
            "crew_filter": "//div[@class='filters crewFilter']//img[contains(@class,'SVGContainer')]",
            "reservation_party": "//span[contains(text(),'Include Reservation Party')]",
            "availability_of_reservation_number": "//tr[1]//td[2]",
            "checkbox": "//div[@class='ProfileContainer is-pulled-left']/span/span/img",
            "action": "//span[contains(text(),'Actions')]",
            "create_alert_option": "//a[@name='CREATE_ALERT']",
            "create_message_option": "//a[@name='CREATE_MESSAGE']",
            "change_embark_slot": "//a[@name='CHANGE_BOARDING_GROUP']",
            "table_row": "//div[@class='HeaderTableContainer__div']/div/table[@class='table is-hoverable is-fullwidth -table']/tbody/tr",
            "boarding_time_class": "//div[@class='HeaderTableContainer__div']/div/table[@class='table is-hoverable is-fullwidth -table']/tbody/tr[%s]/td[1]/span//div",
            "boarding_time": "//div[@class='HeaderTableContainer__div']/div/table[@class='table is-hoverable is-fullwidth -table']/tbody/tr[%s]/td[1]/span",
            "boarding_time_radio": "//div[@class='HeaderTableContainer__div']/div/table[@class='table is-hoverable is-fullwidth -table']/tbody/tr[%s]/td[1]/span/label",
            "update": "//button[contains(text(),'Update')]",
            "cancel": "//span[contains(text(),'CANCEL')]"

        })

    def view_first_sailor(self):
        """
        Function to view the sailor details
        """
        self.webDriver.click(element=self.locators.sailor_arrow % 1, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.sailor_details_header,
                                                          locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def view_first_crew(self):
        """
        Function to view the crew details
        """
        self.webDriver.click(element=self.locators.sailor_arrow % 1, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.crew_details_header,
                                                          locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_sailor_name(self):
        """
        Get the sailor name on details page
        """
        return self.webDriver.get_text(element=self.locators.sailor_name, locator_type='xpath')

    def get_sailor_citizenship(self):
        """
        Get the sailor citizenship on details page
        """
        return self.webDriver.get_text(element=self.locators.citizenship_name, locator_type='xpath')

    def get_crew_checked_in_status(self):
        """
        Get the crew checked in status on details page
        """
        return self.webDriver.get_text(element=self.locators.checked_in_status, locator_type='xpath')

    def click_filter_option(self):
        """
        Function to click on filter option
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_crew_filter_option(self):
        """
        Function to click on filter option
        """
        self.webDriver.click(element=self.locators.crew_filter, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_include_reservation_party(self):
        """
        To click on Include Reservation party check box
        """
        self.webDriver.click(element=self.locators.reservation_party, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def verify_list_in_reservation_party_level(self):
        """
        Function to check the Sailor list should be in Reservation Party level
        """
        value = self.webDriver.get_text(element=self.locators.availability_of_reservation_number, locator_type='xpath')
        if value == '':
            self.webDriver.allure_attach_jpeg('reservation_party')
            return True
        else:
            self.webDriver.allure_attach_jpeg('error_reservation_party')
            return False

    def click_checkbox(self):
        """
        Function is used to tick the check box
        """
        all_checkbox = self.webDriver.get_elements(element=self.locators.checkbox, locator_type='xpath')
        for check in all_checkbox:
            if len(all_checkbox) > 4:
                check.click()
                if all_checkbox.index(check) >= 3:
                    break
            else:
                check.click()
        self.webDriver.allure_attach_jpeg('check_box_selected')

    def click_action(self):
        """
        Function to click on action button
        """
        self.webDriver.click(element=self.locators.action, locator_type='xpath')

    def click_create_alert(self):
        """
        Function to click create alert
        """
        self.webDriver.click(element=self.locators.create_alert_option, locator_type='xpath')

    def click_create_message(self):
        """
        Function to click on create message
        """
        self.webDriver.click(element=self.locators.create_message_option, locator_type='xpath')

    def click_change_embark_slot(self):
        """
        Function to click on change embark slot
        """
        self.webDriver.click(element=self.locators.change_embark_slot, locator_type='xpath')

    def select_boarding_time(self):
        """
        Function to check select the boarding time
        """
        index = None
        boarding_time = None
        row_count = self.webDriver.get_elements(element=self.locators.table_row, locator_type='xpath')
        for boarding in row_count:
            index = row_count.index(boarding) + 1
            if not self.webDriver.get_web_element(element=self.locators.boarding_time_class % index,
                                                  locator_type='xpath').get_attribute("class") == 'check  disabled':
                boarding_time = self.webDriver.get_text(element=self.locators.boarding_time % index,
                                                        locator_type='xpath')
                if boarding_time != 'Board Anytime':
                    break

        self.webDriver.click(element=self.locators.boarding_time_radio % index, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('boarding_time_selection')
        return boarding_time

    def click_update_button(self):
        """
        Function to click on update button
        """
        self.webDriver.click(element=self.locators.update, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def get_boarding_time_on_details(self):
        """
        Get the boarding time on details
        """
        return self.webDriver.get_text(element=self.locators.boarding_slot, locator_type='xpath')
