__author__ = 'aatir.fayyaz'

from virgin_utils import *


class IncidentDetails(General):
    """
    Page Class for incident_management details page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of details page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "details_page_header": "//*[@class='android.view.View'][contains(@text,'Incident Detail')]",
            "back": "//*[@class='android.widget.Button'][@text='menu']",
            "priority_severity": "//*[@class='android.widget.TextView'][contains(@text,'Priority')]",
            "AIMS_data": "//*[@class='android.widget.TextView'][contains(@text,'AIMS')]",
            "incident_cabin": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "VIR_data": "//*[@class='android.widget.TextView'][contains(@text,'VIR')]",
            "sla_value": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "three_dot_icon": "//*[@class='android.widget.TextView']/following-sibling::android.widget.Button",
            "edit_icon": "//*[text()='Edit']",
            "closed_resolved": "//*[text()='Closed Resolved']",
            "confirmation_text": "//*[@class='modal-card-head']",
            "submit_button": "//*[@class='button is-primary']",
            "close_message": "//*[@class='incidentdetails-finished']",
            "reopen": "//*[text()='Reopen']",
            "im_header": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
        })

    def match_aims(self, aim):
        """
        Function to verify AIMS number
        :param aim:
        :return:
        """
        self.webDriver.wait_for(5)
        aims = self.webDriver.get_text(element=self.locators.AIMS_data, locator_type='xpath')
        if aim == aims[7:]:
            logger.debug("AIMS number is matching")
        else:
            raise Exception(f"AIMS number is not matching {aims}")

    def match_cabin_number(self, cabin):
        """
        Function to verify cabin number for which Incident is created
        :param cabin:
        :return:
        """
        cabin_number = self.webDriver.get_text(element=self.locators.incident_cabin % cabin, locator_type='xpath')
        if cabin == cabin_number[6:]:
            logger.debug("Cabin number is matching")
        else:
            raise Exception(f"Cabin number is not matching {cabin}")

    def get_vir_value(self, test_data):
        """
        Function to get the vir value
        :param test_data:
        :return:
        """
        all_list = self.webDriver.get_elements(element=self.locators.VIR_data, locator_type='xpath')
        for status in all_list:
            test_data['vir_value'] = status.text
            break

    def verify_sla(self):
        """
        Function to verify the sla time after creating incident
        :return:
        """
        sla = self.webDriver.get_text(element=self.locators.sla_value % 'Hrs', locator_type='xpath').split('|')[1]
        if sla not in ['04:00 Hrs', ' 3:59 Hrs', ' 3:58 Hrs', ' 3:57 Hrs', ' 3:56 Hrs']:
            raise Exception('SLA not matched')
        self.webDriver.click(element=self.locators.back, locator_type='xpath')
        self.webDriver.wait_for(5)

    def verify_severity_on_details(self, severity_value):
        """
        Function to check the sorting
        :param severity_value:
        :return:
        """
        severity = self.webDriver.get_text(element=self.locators.priority_severity, locator_type='xpath').split('|')[1]
        if not int(severity[-1]) == severity_value:
            raise Exception('severity not matched')

    def verify_priority_on_details(self, priority_value):
        """
        Function to check the priority
        :param priority_value:
        :return:
        """
        self.webDriver.wait_for(5)
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.scroll_mobile(300, 1000, 300, 800)
        self.webDriver.scroll_mobile(300, 800, 300, 1200)
        self.webDriver.explicit_visibility_of_element(element=self.locators.priority_severity, locator_type='xpath',
                                                      time_out=120)
        priority = self.webDriver.get_text(element=self.locators.priority_severity, locator_type='xpath').split('|')[0]
        if not int(priority[-1]) == priority_value:
            raise Exception('priority not matched')

    def back_to_im_dashboard(self):
        """
        Function to close the search result page
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger, locator_type='xpath')
        self.webDriver.click(element=self.locators.incident_management, locator_type='xpath')
        self.webDriver.wait_for(5)

    def open_3_dot_menu(self):
        """
        Function to click the 3 dot menu
        :return:
        """
        self.webDriver.click(element=self.locators.three_dot_icon, locator_type='xpath')

    def close_incident(self):
        """
        Function to close the Incident
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.closed_resolved, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.confirmation_text, locator_type='xpath'):
            self.webDriver.click(element=self.locators.submit_button, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.close_message, locator_type='xpath'):
                self.webDriver.allure_attach_jpeg('close_incident')
                logger.debug("Incident is closed and green message bar displayed")
                contexts = self.webDriver.get_contexts()
                self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            else:
                raise Exception("Incident not closed")
        else:
            raise Exception("close Notes popup not open")

    def reopen_closed_incident(self):
        """
        Function to Re-open the closed Incident
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.reopen, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.confirmation_text, locator_type='xpath'):
            self.webDriver.click(element=self.locators.submit_button, locator_type='xpath')
            self.webDriver.wait_for(3)
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            self.webDriver.click(element=self.locators.back, locator_type='xpath')
            self.webDriver.wait_for(5)
        else:
            raise Exception("Reopen Notes popup not open")

    def click_edit_icon(self):
        """
        Function to click on edit icon
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.edit_icon, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(300, 1200, 300, 100)
        self.webDriver.scroll_mobile(300, 1200, 300, 100)