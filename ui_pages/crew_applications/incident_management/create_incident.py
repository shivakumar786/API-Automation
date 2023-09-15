__author__ = 'aatir.fayyaz'


from virgin_utils import *
from selenium.webdriver.common.keys import Keys


class CreateIncident(General):
    """
    Page Class for Create Incident page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Create Incident page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "mandatory": "//*[@class='android.view.View'][contains(@text,'Incident Category')]",
            "please_document": "//*[@class='android.widget.TextView'][contains(@text,'Please document at least')]",
            "stateroom": "//*[@resource-id='stateroom']",
            "select_sailor": "//*[@class='android.widget.TextView'][@text='✓']",
            "get_sailor_name": "//*[@text='%s']/preceding-sibling::android.widget.TextView",
            "parent_incident": "//*[@resource-id='incidentParentType']",
            "select_parent_incident": "//*[@class='android.widget.TextView'][@text='Cabin']",
            "incident_category": "//*[@resource-id='incidentCategories']",
            "select_incident_category": "//*[@class='android.widget.TextView'][@text='Cabin Flood']",
            "department": "//*[@class='android.widget.TextView'][@text='Housekeeping']",
            "assign_to_member": "//*[@resource-id='assignedToTeamMember']",
            "select_assign_to_member": "//*[@class='android.widget.TextView'][@text='%s']",
            "description": "//*[@resource-id='description']",
            "follow_up_notes": "//*[@resource-id='followUpNotes']",
            "resolution_details": "//*[@resource-id='resolutionDetails']",
            "AIMS": "//*[@resource-id='externalRefId']",
            "sla": "//*[@resource-id='incidentSLAs']",
            "select_sla": "//*[@class='android.widget.TextView'][@text='00:30 hrs']",
            "priority_slider": "//*[@name='priority']",
            "priority_value": "//*[@class='android.widget.Button'][contains(@text,'Priority')]",
            "check_sla": "//div[@id='incidentSLAs']/div/div[1]/div[1]",
            "sla_value": "//*[@class='android.widget.TextView'][@text='00:30 hrs']",
            "severity_slider": "//*[@name='severity']",
            "severity_value": "//*[@class='android.widget.Button'][contains(@text,'Severity')]",
            "upload_photo": "//*[@class='android.widget.Image'][@text='logo'][@index='0']",
            "camera_roll": "//*[@class='android.widget.Button'][@content-desc='Camera roll']",
            "allow_popup": "//*[@class='android.widget.TextView'][contains(@text,'Allow VV Crew App')]",
            "allow": "//*[@class='android.widget.Button'][@text='Allow']",
            "use_photo": "//*[@class='android.widget.TextView'][@text='pic.jpeg']",
            "verify_photo": "//*[@resource-id='img-preview']",
            "create_button": "//*[@text='CREATE']",
            "update_button": "//*[@text='UPDATE']",
            "indication_text": "//*[@class='android.view.View'][@text='%s']",
            "from_element": "//*[@name='priority'][@value='3']",
            "to_element": "//*[@name='priority'][@value='5']",
            "priority_bar": "//*[@name='priority']",
            "severity_bar": "//*[@name='severity']",
            "upload_profile": "//*[@name='severity']"
        })

    def check_mandatory_fields(self):
        """
        Function to verify the Star(*) mark on the mandatory fields
        :return:
        """
        self.webDriver.wait_for(5)
        mandatory = []
        statement = self.webDriver.get_text(element=self.locators.please_document, locator_type='xpath')
        assert statement == 'Please document at least “Place” or “Cabin / Sailor Name” below', \
            'Mandatory field text not shown'
        mandatory.append(self.webDriver.get_text(element=self.locators.mandatory, locator_type='xpath'))
        for field in mandatory:
            if '*' not in field:
                raise Exception('No star(*) mark on the mandatory fields')

    def department_auto_display(self, cabin_number, test_data):
        """
        Function to fill the incident details and verify Department Auto displayed after choosing parent incident and
        incident category
        :param cabin_number:
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.stateroom, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.stateroom, locator_type='xpath', text=cabin_number)
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(400, 500, 400, 470)
        test_data['sailor'] = self.webDriver.get_text(element=self.locators.get_sailor_name % cabin_number,
                                                      locator_type='xpath')
        self.webDriver.click(element=self.locators.select_sailor, locator_type='xpath')
        self.webDriver.scroll_mobile(400, 1200, 360, 100)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.parent_incident, locator_type='xpath'):
            self.webDriver.scroll_mobile(400, 1200, 360, 800)
        self.webDriver.click(element=self.locators.parent_incident, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.select_parent_incident,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(400, 500, 360, 200)
        self.webDriver.click(element=self.locators.select_parent_incident, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.incident_category,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(400, 1200, 360, 700)
        self.webDriver.click(element=self.locators.incident_category, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.select_incident_category,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(90, 500, 90, 200)
            self.webDriver.click(element=self.locators.incident_category, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_incident_category, locator_type='xpath')
        department_value = self.webDriver.get_text(element=self.locators.department, locator_type='xpath')
        if len(department_value) <= 0:
            raise Exception("Department is not pre-filled")

    def verify_assign_to_crew(self, crew):
        """
        Function to assign incident to crew
        :param crew:
        :return:
        """
        self.webDriver.scroll_mobile(90, 1170, 90, 1000)
        self.webDriver.click(element=self.locators.assign_to_member, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.select_assign_to_member % crew,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(90, 1200, 90, 800)
            self.webDriver.click(element=self.locators.assign_to_member, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_assign_to_member % crew, locator_type='xpath')
        member = self.webDriver.get_text(element=self.locators.select_assign_to_member % crew, locator_type='xpath')
        if member != crew:
            raise Exception("Not able to assign to crew")

    def fill_incident(self, test_data):
        """
        Function to fill the incident details
        :param test_data:
        :return:
        """
        test_data['AIMS'] = []
        self.webDriver.click(element=self.locators.description, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.description, locator_type='xpath',
                                text="Description of Incident")
        self.webDriver.scroll_mobile(90, 700, 90, 400)
        self.webDriver.click(element=self.locators.follow_up_notes, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.follow_up_notes, locator_type='xpath',
                                text="Notes of Incident")
        self.webDriver.scroll_mobile(90, 700, 90, 400)
        self.webDriver.click(element=self.locators.resolution_details, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.resolution_details, locator_type='xpath',
                                text="Resolution of Incident")
        self.webDriver.click(element=self.locators.AIMS, locator_type='xpath')
        test_data['AIMS'] = generate_random_alpha_numeric_string(5)
        self.webDriver.set_text(element=self.locators.AIMS, locator_type='xpath', text=test_data['AIMS'])
        self.webDriver.scroll_mobile(90, 700, 90, 400)

    def high_low_text(self):
        """
        To verify that Priority and Severity High to Low text is visible
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.indication_text % 'High',
                                                           locator_type='xpath'):
            raise Exception('High indication text not found')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.indication_text % 'Low',
                                                           locator_type='xpath'):
            raise Exception('Low indication text not found')

    def set_lowest_sla(self):
        """
        Function to set the lowest sla
        :return:
        """
        self.webDriver.click(element=self.locators.sla, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_sla, locator_type='xpath')
        self.webDriver.wait_for(3)
        sla = self.webDriver.get_text(element=self.locators.sla_value, locator_type='xpath')
        assert sla == '00:30 hrs', "Lowest SLA is not assigned"

    def set_priority(self, test_data):
        """
        Function to slide the priority
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        slide = self.webDriver.get_web_element(element=self.locators.priority_bar, locator_type='xpath')
        value = int(slide.get_attribute('value'))
        if value == 5:
            slide.send_keys(Keys.LEFT)
            if int(slide.get_attribute('value')) != value - 1:
                raise Exception("Priority not Decreased")
            else:
                test_data['priority'] = value - 1
                return value - 1
        else:
            slide.send_keys(Keys.RIGHT)
            if int(slide.get_attribute('value')) != value + 1:
                raise Exception("Priority not Increased")
            else:
                test_data['priority'] = value + 1
                return value + 1

    def set_severity(self, test_data):
        """
        Function to slide the severity
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        slide = self.webDriver.get_web_element(element=self.locators.severity_bar, locator_type='xpath')
        value = int(slide.get_attribute('value'))
        if value == 3:
            slide.send_keys(Keys.LEFT)
            if int(slide.get_attribute('value')) != value - 1:
                raise Exception("Severity not Decreased")
            else:
                test_data['severity'] = value - 1
                return value - 1
        else:
            slide.send_keys(Keys.RIGHT)
            if int(slide.get_attribute('value')) != value + 1:
                raise Exception("Severity not Increased")
            else:
                test_data['severity'] = value + 1
                return value + 1

    def check_sla_value(self, test_data):
        """
        Function to check that sla changes as per priority
        :param test_data:
        :return:
        """
        test_data['sla'] = self.webDriver.get_text(element=self.locators.check_sla, locator_type='xpath')
        assert test_data['sla'] != '00:30 hrs', "SLA is not updated"

    def upload_photo(self):
        """
        Function to upload photo
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.scroll_mobile(400, 700, 360, 250)
        self.webDriver.click(element=self.locators.upload_photo, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.explicit_visibility_of_element(element=self.locators.camera_roll, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.camera_roll, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_popup, locator_type="xpath"):
            self.webDriver.click(element=self.locators.allow, locator_type='xpath')
        self.webDriver.click(element=self.locators.use_photo, locator_type="xpath")

    def verify_upload_photo(self):
        """
        Function to upload photo
        :return:
        """
        self.webDriver.wait_for(3)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.verify_photo, locator_type="xpath"):
            raise Exception('Photo not uploaded successfully')

    def click_create(self):
        """
        Function to save the Incident
        :return:
        """
        self.webDriver.scroll_mobile(90, 650, 90, 250)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.create_button, locator_type="xpath"):
            self.webDriver.scroll_mobile(90, 250, 90, 650)
            self.webDriver.scroll_mobile(90, 650, 90, 250)
        self.webDriver.click(element=self.locators.create_button, locator_type='xpath')

    def click_update(self):
        """
        Function to update the Incident
        :return:
        """
        self.webDriver.scroll_mobile(90, 650, 90, 20)
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.update_button, locator_type="xpath"):
            self.webDriver.scroll_mobile(90, 250, 90, 650)
            self.webDriver.scroll_mobile(90, 650, 90, 250)
        self.webDriver.click(element=self.locators.update_button, locator_type='xpath')
        self.webDriver.wait_for(5)

