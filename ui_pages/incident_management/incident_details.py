__author__ = 'prahlad.sharma'

from virgin_utils import *


class IncidentDetails(General):
    """
    Page Class for Incident Management details page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of details page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "details_page_header": "//span[text()='Incident Details']",
            "AOMS_data": "//span/span[text()='AIMS#']/../following-sibling::span[@class='tag-value-data']",
            "incident_location": "//div[@class='incident-card-location']",
            "incident_category": "incident-card-category",
            "back": "//span[@class='clickable page-title-main']",
            "edit_icon": "//span[text()='Work History']/../following-sibling::span/span/img[@class='SVGContainer ']",
            "cancel": "//*[text()='Assign']/../*[text()='Cancel']",
            "three_dot_icon": "//span[@class='incidentdetails-iconmargin show-pointer']",
            "incident_status": "//span[@class='incidentdetails-progressstatus']",
            "reassign": "//span[text()='Assign']",
            "close": "//span[text()='Closed Resolved']",
            "department_dropdown":"(//*[text()='Department']/..//div[@class='react-select__indicator "
                                  "react-select__dropdown-indicator css-tlfecz-indicatorContainer'])[2]",
            "department": "//div[@id='departments']//input",
            "assign_to": "(//*[text()='Assigned To']/..//div[@class='react-select__indicator "
                         "react-select__dropdown-indicator css-tlfecz-indicatorContainer'])[2]",
            "crew_notes": "(//input[@name='resolutionDetails'])[3]",
            "reassign_button": "//button[text()='Assign']",
            "close_confirmation": "//div[text()='Please submit your comments for this incident/issue to update status']",
            "close_notes": "attendedByNotes",
            "submit_button": "//button[text()='Submit']",
            "close_message": "//div[@class='incidentdetails-finished']/center[contains(text(),'This issue has been "
                             "marked Closed-Resolved ')]"

        })

    def verify_incident_details_page(self):
        """
        Verify user is able to open the Dashboard page after login
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.details_page_header, locator_type='xpath'):
            logger.debug("User land on Incident Details page")
        else:
            raise Exception("User land on Incident Details page")

    def match_AOMS(self):
        """
        Function to verify AOMS number
        :return:
        """
        if self.test_data["AIMS#"] == self.webDriver.get_text(element=self.locators.AOMS_data, locator_type='xpath'):
            logger.debug("AIMS# number is matching")
        else:
            raise Exception(f"AOMS number is not matching {self.test_data['AIMS#']}")

    def match_cabin_number(self):
        """
        Function to verify cabin number for which Incident is created
        :return:
        """
        if f"Cabin {self.test_data['searched_sailor_stateroom']}" == self.webDriver.get_text(
                element=self.locators.incident_location, locator_type='xpath'):
            logger.debug("AIMS# number is matching")
        else:
            raise Exception(f"AIMS# number is not matching {self.test_data['AIMS#']}")

    def go_back(self):
        """
        Function to go back
        :return:
        """
        self.webDriver.click(element=self.locators.back, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_edit_icon(self):
        """
        Function to click on edit icon
        :return:
        """
        self.webDriver.click(element=self.locators.edit_icon, locator_type='xpath')

    def get_incident_status(self):
        """
        Function to get the incident status
        :return:
        """
        return self.webDriver.get_text(element=self.locators.incident_status, locator_type='xpath')

    def open_3_dot_menu(self):
        """
        Function to click the 3 dot menu
        :return:
        """
        self.webDriver.click(element=self.locators.three_dot_icon, locator_type='xpath')

    def click_reassign_button(self):
        """
        Function to open reassign
        :return:
        """
        self.open_3_dot_menu()
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.reassign, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def reassign_incident(self):
        """
        Function to fill the data in reassign incident
        :return:
        """
        try:
            self.webDriver.select_dynamic_dropdown_data_using_action_keys(element=self.locators.assign_to,
                                                                          locator_type='xpath')
            self.webDriver.set_text(element=self.locators.crew_notes, locator_type='xpath', text="Assign to crew")
            self.webDriver.click(element=self.locators.reassign_button, locator_type='xpath')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            return True
        except(Exception, ValueError)as exp:
            self.webDriver.click(element=self.locators.cancel, locator_type="xpath")
            return False

    def close_incident(self):
        """
        Function to close the Incident
        :return:
        """
        self.open_3_dot_menu()
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.close, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.close_confirmation, locator_type='xpath'):
            self.webDriver.click(element=self.locators.submit_button, locator_type='xpath')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            if self.webDriver.is_element_display_on_screen(element=self.locators.close_message, locator_type='xpath'):
                self.webDriver.allure_attach_jpeg('close_incident')
                logger.debug("Incident is closed and green message bar display")
            else:
                raise Exception("Incident not closed")
        else:
            raise Exception("close Notes popup not open")
