__author__ = 'prahlad.sharma'



from virgin_utils import *
from selenium.webdriver.common.keys import Keys


class CreateIncident(General):
    """
    Page Class for Create Incident page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Create Incident page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "stateroom": "stateroom",
            "visibility_of_sailor": "//div[text()=' Sailors Impacted']",
            "sailor_img": "//div[@class='sailorprofile-img-container']/div/div",
            "close": "//*[text()='close']",
            "parent_incident_category": "//div[@id='incidentParentType']//input",
            "incident_category": "//div[@id='incidentCategories']//input",
            "department": "//div[@id='departments']//input",
            "department_value": "//div[@id='departments']//div[@class='react-select__single-value css-1uccc91-singleValue']",
            "assign_to_member": "//div[@id='assignedToTeamMember']//input",
            "description": "description",
            "notes": "followUpNotes",
            "crew_notes": "resolutionDetails",
            "AOMS": "externalRefId",
            "incident_reporter": "incidentReporter",
            "priority_bar": "priority",
            "severity_bar": "severity",
            "file_upload": "camera",
            "create_button": "//button[text()='CREATE']",
            "update_button": "//button[text()='UPDATE']",
            "cancel_button": "//button[text()='cancel']",
            "sla_value": "//div[@id='incidentSLAs']//div[@class='react-select__single-value css-1uccc91-singleValue']",
            "location": "locations"
        })

    def fill_incident(self, cabin_number):
        """
        Function to fill the incident details
        :return:
        """
        self.webDriver.set_text(element=self.locators.stateroom, locator_type='name', text=cabin_number)
        self.webDriver.explicit_visibility_of_element(element=self.locators.visibility_of_sailor, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.wait_for(5)
        sailor_count = self.webDriver.get_elements(element=self.locators.sailor_img, locator_type='xpath')
        for count, item in enumerate(sailor_count):
            if count >= 2:
                break
            else:
                self.webDriver.wait_for(5)
                item.click()

        if self.webDriver.is_element_display_on_screen(self.locators.close, locator_type="xpath"):
            self.webDriver.click(self.locators.close, locator_type="xpath")
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.parent_incident_category,
                                                          locator_type='xpath', text="cabin")
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.incident_category, locator_type='xpath',
                                                          text="Toilet Not Flushing")
        department_value = self.webDriver.get_text(element=self.locators.department_value, locator_type='xpath')
        if len(department_value) <= 0:
            raise Exception("Department is not pre-filled")
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.assign_to_member, locator_type='xpath',
                                                          text="david warner")
        self.webDriver.set_text(element=self.locators.description, locator_type='id', text="Details of Incident")
        self.webDriver.scroll_till_element(element=self.locators.notes, locator_type="id")
        self.webDriver.set_text(element=self.locators.notes, locator_type='id', text="Notes of the Incident")
        self.webDriver.set_text(element=self.locators.crew_notes, locator_type='id', text="Notes of the Incident by "
                                                                                          "Crew member")
        self.test_data["AIMS#"] = generate_random_alpha_numeric_string(5)
        self.webDriver.set_text(element=self.locators.AOMS, locator_type='id', text=self.test_data["AIMS#"])

    def set_highest_priority(self):
        """
        Function to set the highest priority
        :return:
        """
        slide = self.webDriver.get_web_element(element=self.locators.priority_bar, locator_type='name')
        value = int(slide.get_attribute('value'))
        if value != 5:
            for x in range(value, 5):
                slide.send_keys(Keys.RIGHT)

    def set_highest_severity(self):
        """
        Function to set the highest severity
        :return:
        """
        slide = self.webDriver.get_web_element(element=self.locators.severity_bar, locator_type='name')
        value = int(slide.get_attribute('value'))
        if value != 0:
            for x in range(value, 1, -1):
                slide.send_keys(Keys.LEFT)

    def priority_slider(self):
        """
        Function to slide the priority
        :return:
        """
        slide = self.webDriver.get_web_element(element=self.locators.priority_bar, locator_type='name')
        value = int(slide.get_attribute('value'))
        if value == 5:
            slide.send_keys(Keys.LEFT)
            if int(slide.get_attribute('value')) != value - 1:
                raise Exception("Priority not Decreased")
            else:
                return value - 1
        else:
            slide.send_keys(Keys.RIGHT)
            if int(slide.get_attribute('value')) != value + 1:
                raise Exception("Priority not Increased")
            else:
                return value + 1

    def severity_slider(self):
        """
        Function to slide the severity
        :return:
        """
        slide = self.webDriver.get_web_element(element=self.locators.severity_bar, locator_type='name')
        value = int(slide.get_attribute('value'))
        if value == 3:
            slide.send_keys(Keys.LEFT)
            if int(slide.get_attribute('value')) != value - 1:
                raise Exception("Severity not Decreased")
            else:
                return value - 1
        else:
            slide.send_keys(Keys.RIGHT)
            if int(slide.get_attribute('value')) != value + 1:
                raise Exception("Severity not Increased")
            else:
                return value + 1

    def click_save(self):
        """
        Function to save the Incident
        :return:
        """
        self.webDriver.click(element=self.locators.create_button, locator_type='xpath')

    def click_update(self):
        """
        Function to update the Incident
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.click(element=self.locators.update_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def check_sla_value(self):
        """
        Function to verify SLA changed as per priority
        :return:
        """
        sla = {1: "00:30 hrs", 2: "01:00 hrs", 3: "04:00 hrs", 4: "10:00 hrs", 5: "23:59 hrs"}
        value = self.priority_slider()
        sla_value = self.webDriver.get_text(element=self.locators.sla_value, locator_type='xpath')
        assert sla_value == sla[value], "Correct SLS is not updated"

    def select_incident_location(self):
        """
        Function to select incident location
        :return:
        """
        self.webDriver.click(element=self.locators.location, locator_type="id")
        self.webDriver.key_chains().send_keys(Keys.ENTER).perform()