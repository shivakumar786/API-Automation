__author__ = 'sarvesh.singh'

import time

from virgin_utils import *


class Health(General):
    """
    Page class for health screen of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform == 'DCL':
            self.locators = self.dict_to_ns({
                "health": "//*[@text='HEALTH']",
                "voyage_well_checkbox": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/terms_and_conditions']",
                "save_button": "//*[@text='SAVE']",
                "voyage_well_status": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/status'][1]",
                "health_question_status": "//*[@text='Health Questions']/following-sibling::android.widget.TextView",
                "additional_health_protocols": "//*[@text='Additional Health Protocols']"
                                               "/following-sibling::android.widget.TextView",
                "additional_health_protocols_save": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/additional_health_test_message']"
                                                    "/following-sibling::android.widget.Button",
                "health_questions_scroll": "//*[@text='Health Questions']",
                "all_health_questions": "com.decurtis.dxp.aci.dclnp:id/common_questions_container",
                "pregnancy_questions_present": "//*[@text='Will you be more than 24 weeks pregnant by the end of your cruise?']",
                "pregnancy_questions_yes": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/pregnancy_answer_yes']",
                "thermal_pass": "//*[@text='Pass']",
                "thermal_pass_status": "//*[@text='Thermal Check']/following-sibling::android.widget.TextView",
                "thermal_pass_save": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/thermal_check_message']"
                                     "/following-sibling::android.widget.Button",
                "additional_health_check": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/test_completed']",
                "save_proceed": "//*[@text='AGREE & PROCEED']",
                "yes": "//*[@text='Yes']",
                "health_questions_no": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/no']",
                "remove_party": "com.decurtis.dxp.aci:id/edit_party"
            })
        else:
            self.locators = self.dict_to_ns({
                "health": "//*[@text='HEALTH']",
                "voyage_well_checkbox": "//*[@resource-id='com.decurtis.dxp.aci:id/terms_and_conditions']",
                "save_button": "//*[@text='SAVE']",
                "select_yes": "com.decurtis.dxp.aci:id/fully_vaccinated_yes",
                "vaccine_type": "//*[@text='Covishield']",
                "vaccine_name_select": "android:id/text1",
                "vaccination_date": "//*[@text='Final Vaccination Date']/../following-sibling::android.widget.EditText",
                "booster": "com.decurtis.dxp.aci:id/received_vaccination_booster",
                "health_question_status": "//*[@text='Health Questions']/following-sibling::android.widget.TextView",
                "additional_health_protocols": "//*[@text='Additional Health Protocols']"
                                               "/following-sibling::android.widget.TextView",
                "additional_health_protocols_save": "//*[@resource-id='com.decurtis.dxp.aci:id/additional_health_test_message']"
                                                    "/following-sibling::android.widget.Button",
                "additional_health_check": "//*[@resource-id='com.decurtis.dxp.aci:id/test_completed']",
                "voyage_well": "//*[@text='Voyage Well Acknowledgment Form']",
                "vaccination": "//*[@text='Vaccination Declaration']",
                "additional": "//*[@text='Additional Health Protocols']",
                "questions": "//*[@text='Health Questions']",
                "yes": "//*[@text='Yes']",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "all_health_questions": "com.decurtis.dxp.aci:id/question",
                "health_questions_no": "//*[@resource-id='com.decurtis.dxp.aci:id/no']",
                "pregnancy_questions_present": "//*[@text='Will you be more than 24 weeks pregnant by the end of your cruise?']",
                "pregnancy_questions_yes": "//*[@resource-id='com.decurtis.dxp.aci:id/pregnancy_answer_yes']",
                "remove_party": "com.decurtis.dxp.aci.dclnp:id/edit_party"
            })

    def click_health_tab(self):
        """
        Func to click on health tab
        :return:
        """
        self.webDriver.click(element=self.locators.health, locator_type='xpath')
        self.webDriver.wait_for(5)

    def check_health_tab_enabled(self):
        """
        Func to check if health tab is enabled
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.health, locator_type='xpath'):
            return self.webDriver.get_web_element(element=self.locators.health, locator_type='xpath').get_attribute(
                "selected")
        else:
            return "false"

    def check_voyage_well_selected(self):
        """
        Func to get the voyage well current status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.voyage_well_checkbox,
                                              locator_type='xpath').get_attribute("checked")

    def get_voyage_well_status(self):
        """
        Func to get the voyage well status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.voyage_well_status, locator_type='xpath').text

    def get_health_questions_status(self):
        """
        Func to get the voyage well status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.health_question_status, locator_type='xpath').text

    def get_thermal_pass_status(self):
        """
        Func to get the thermal pass status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.thermal_pass_status, locator_type='xpath').text

    def get_additional_health_protocol_status(self):
        """
        Func to get the additional health protocal status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.additional_health_protocols,
                                              locator_type='xpath').text

    def accept_voyage_well_terms(self):
        """
        Func to accept voyage well terms
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_well_checkbox, locator_type='xpath'):
            self.webDriver.click(element=self.locators.voyage_well, locator_type='xpath')
        if self.check_voyage_well_selected() == 'false':
            self.webDriver.click(element=self.locators.voyage_well_checkbox, locator_type='xpath')
            if self.check_voyage_well_selected() == 'false':
                raise Exception('Voyage well terms and conditions did not get accepted !!')
            self.webDriver.click(element=self.locators.save_button, locator_type='xpath')
            time.sleep(2)
        self.webDriver.scroll_mobile(x_press=18, y_press=1141, x_move=15, y_move=671)

    def accept_health_questions(self):
        """
        Func to accept health check questions
        :return:
        """
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.wait_for(2)
        # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        questions = self.webDriver.get_elements(element=self.locators.health_questions_no, locator_type='xpath')
        for _question in questions:
            _question.click()
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.wait_for(2)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.wait_for(2)
        # self.webDriver.click(element=self.locators.save_button, locator_type='xpath')

    def pass_thermal_check(self):
        """
        Func to pass thermal check
        :return:
        """
        if self.get_thermal_pass_status() == 'Pending':
            self.webDriver.click(element=self.locators.thermal_pass, locator_type='xpath')
            self.webDriver.click(element=self.locators.thermal_pass_save, locator_type='xpath')

    def pass_additional_health_protocol(self):
        """
        Func to pass additional health protocol
        :return:
        """
        self.webDriver.wait_for(2)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.wait_for(2)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.additional_health_check, locator_type='xpath'):
            self.webDriver.click(element=self.locators.additional, locator_type='xpath')
        if self.get_additional_health_protocol_status() == 'Pending':
            self.webDriver.click(element=self.locators.additional_health_check, locator_type='xpath')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            self.webDriver.click(element=self.locators.additional_health_protocols_save, locator_type='xpath')

    def click_save_proceed(self):
        """
        Func to click on save and proceed
        :return:
        """
        self.webDriver.click(element=self.locators.save_proceed, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.yes, locator_type='xpath'):
            self.webDriver.click(element=self.locators.yes, locator_type='xpath')

    def scroll_top(self):
        """
        Func to scroll to top of page
        :return:
        """
        self.webDriver.scroll_mobile(x_press=792, y_press=495, x_move=792, y_move=1099)
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.remove_party, locator_type='xpath'):
            pass
        else:
            self.webDriver.scroll_mobile(x_press=792, y_press=495, x_move=792, y_move=1099)

    def perform_health(self):
        """
        Func to perform health step in ACI
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.yes, locator_type='xpath'):
            self.webDriver.click(element=self.locators.questions, locator_type='xpath')
        if self.config.platform == 'VIRGIN':
            if self.get_health_questions_status() == 'Pending':
                self.accept_health_questions()
            else:
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
                self.webDriver.wait_for(2)
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
                self.webDriver.wait_for(2)
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
                self.webDriver.wait_for(2)
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        else:
            if self.get_health_questions_status() == 'Pending':
                self.accept_health_questions()
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            else:
                self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

    def vaccination_details(self):
        """
        Vaccination Declaration
        """
        #vaccine details
        self.webDriver.scroll_mobile(x_press=18, y_press=1141, x_move=15, y_move=671)
        if self.webDriver.is_element_display_on_screen(element=self.locators.select_yes,
                                                       locator_type='id'):
            self.webDriver.click(element=self.locators.select_yes, locator_type='id')
        else:
            self.webDriver.click(element=self.locators.vaccination, locator_type='xpath')
            self.webDriver.click(element=self.locators.select_yes, locator_type='id')

        if self.webDriver.get_web_element(element=self.locators.vaccine_name_select,
                                                       locator_type='id').text == "- Select -":
            self.webDriver.click(element=self.locators.vaccine_name_select,
                                           locator_type='id')
            self.webDriver.click(element=self.locators.vaccine_type, locator_type='xpath')
        self.webDriver.scroll_mobile(x_press=18, y_press=1141, x_move=15, y_move=671)
        self.webDriver.set_text(element=self.locators.vaccination_date, locator_type='xpath', text="01/13/2022")
        self.webDriver.scroll_mobile(x_press=18, y_press=1141, x_move=15, y_move=671)
        self.webDriver.click(element=self.locators.booster, locator_type='id')
        self.webDriver.scroll_mobile(x_press=18, y_press=1141, x_move=15, y_move=671)
        self.webDriver.click(element=self.locators.save_button, locator_type='xpath')