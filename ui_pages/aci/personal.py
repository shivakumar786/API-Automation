__author__ = 'sarvesh.singh'

from virgin_utils import *


class Personal(General):
    """
    Page class for personl screen of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "personal": "//*[@text='PERSONAL']",
                "address_status": "//*[@text='Address']/following-sibling::android.widget.TextView",
                "emergency_status": "//*[@text='Emergency Contact']/following-sibling::android.widget.TextView",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "country": "//*[@text='Country of Residence']/../following-sibling::android.widget.EditText",
                "country_select": "//*[@text='United States']",
                "emergency_name": "//*[@text='Name']/../following-sibling::android.widget.EditText",
                "emergency_relation": "//*[@text='- Select -']",
                "emergency_relation_select": "//*[@text='Friend']",
                "emergency_country_code": "//*[@text='Emergency Contact']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.EditText",
                "emergenyc_country_code_select": "//*[@text='United States (+ 1)']",
                "emergency_contact": "//*[@text='Emergency Contact']/following-sibling::android.widget.TextView",
                "emergency_email": "//*[@text='Email']/../following-sibling::android.widget.EditText",
                "address_line": "//*[@text='Address Line 1']/../following-sibling::android.widget.EditText",
                "zipcode": "//*[@text='Zip Code']/../following-sibling::android.widget.EditText",
                "city": "//*[@text='City']/../following-sibling::android.widget.EditText",
                "country_code": "//*[@text='Country Code']/../following-sibling::android.widget.EditText",
                "emer_contact_no": "//*[@resource-id='com.decurtis.dxp.aci:id/section_emergency_contact']//*[@text='Contact No.']/../following-sibling::android.widget.EditText",
                "add_contact_no": "//*[@resource-id='com.decurtis.dxp.aci:id/address_section']//*[@text='Phone Number']/../following-sibling::android.widget.EditText",
                "country_name": "//*[@text='Country']/../following-sibling::android.widget.EditText",
                "emergency_contacts": "//*[@text='Emergency Contact']/../following-sibling::android.widget.EditText",
                "legal": "//*[@text='Additional Details']/following-sibling::*[@resource-id='com.decurtis.dxp.aci:id/status']",
            })
        else:
            self.locators = self.dict_to_ns({
                "personal": "//*[@text='PERSONAL']",
                "address_status": "//*[@text='Address']/following-sibling::android.widget.TextView",
                "emergency_status": "//*[@text='Emergency Contact']/following-sibling::android.widget.TextView",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "country": "//*[@text='Country of Residence']/../following-sibling::android.widget.EditText",
                "country_select": "//*[@text='United States']",
                "emergency_name": "//*[@text='Name']/../following-sibling::android.widget.EditText",
                "emergency_relation": "//*[@text='Relation']/../following-sibling::android.widget.EditText",
                "emergency_country_code": "//*[@text='Emergency Contact']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.EditText",
                "emergenyc_country_code_select": "//*[@text='United States (+ 1)']",
                "emergency_contact": "//*[@text='Emergency Contact']/following-sibling::android.widget.TextView",
                "emergency_email": "//*[@text='Email']/../following-sibling::android.widget.EditText",
                "address_line": "//*[@text='Address Line 1']/../following-sibling::android.widget.EditText",
                "zipcode": "//*[@text='Zip Code']/../following-sibling::android.widget.EditText",
                "city": "//*[@text='City']/../following-sibling::android.widget.EditText",
                "country_code": "//*[@text='Country Code']/../following-sibling::android.widget.EditText",
                "emer_contact_no": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/section_emergency_contact']//*[@text='Phone Number']/../following-sibling::android.widget.EditText",
                "add_contact_no": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/address_section']//*[@text='Phone Number']/../following-sibling::android.widget.EditText",
                "country_name": "//*[@text='Country']/../following-sibling::android.widget.EditText",
                "emergency_contacts": "//*[@text='Emergency Contact']/../following-sibling::android.widget.EditText",
                "legal": "//*[@text='Additional Details']/following-sibling::*[@resource-id='com.decurtis.dxp.aci.dclnp:id/status']",
                "legal_guardian": "com.decurtis.dxp.aci.dclnp:id/legal_guardian",
                "click_yes": "com.decurtis.dxp.aci.dclnp:id/yes",
            })

    def click_personal_tab(self):
        """
        Func to click on personal tab
        :return:
        """
        self.webDriver.click(element=self.locators.personal, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_personal_tab_enabled(self):
        """
        Func to check if personal tab is enabled
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.personal, locator_type='xpath'):
            return "false"
        else:
            return self.webDriver.get_web_element(element=self.locators.personal, locator_type='xpath').get_attribute(
                "selected")

    def get_address_status(self):
        """
        Func to get the address status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.address_status, locator_type='xpath').text

    def get_emergency_status(self):
        """
        Func to get the emergency contact status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.emergency_status, locator_type='xpath').text

    def update_address(self):
        """
        Func to update address
        :return:
        """
        self.webDriver.scroll_mobile(x_press=648, y_press=369, x_move=637, y_move=1143)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.address_line, locator_type='xpath'):
            self.webDriver.click(element=self.locators.address_status, locator_type='xpath')
        if len(self.webDriver.get_web_element(element=self.locators.address_line, locator_type='xpath').text) == 0:
            self.webDriver.click(element=self.locators.address_line, locator_type='xpath')
            self.webDriver.set_text(element=self.locators.address_line, locator_type='xpath', text='Automation 123')
            self.webDriver.driver.hide_keyboard()
        if len(self.webDriver.get_web_element(element=self.locators.zipcode, locator_type='xpath').text) == 0:
            self.webDriver.click(element=self.locators.zipcode, locator_type='xpath')
            self.webDriver.driver.hide_keyboard()
            self.webDriver.set_text(element=self.locators.zipcode, locator_type='xpath', text='208027')
        if len(self.webDriver.get_web_element(element=self.locators.country_name, locator_type='xpath').text) == 0:
            if self.config.platform != 'DCL':
                self.webDriver.set_text(element=self.locators.country_name, locator_type='xpath', text='United States')
            else:
                self.webDriver.click(element=self.locators.country_name, locator_type='xpath')
                self.webDriver.set_text(element=self.locators.country_name, locator_type='xpath',
                                        text='UNITED STATES OF AMERICA')
                self.webDriver.driver.hide_keyboard()
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if len(self.webDriver.get_web_element(element=self.locators.city, locator_type='xpath').text) == 0:
            self.webDriver.click(element=self.locators.city, locator_type='xpath')
            self.webDriver.set_text(element=self.locators.city, locator_type='xpath', text='New York')
            self.webDriver.driver.hide_keyboard()
        if len(self.webDriver.get_web_element(element=self.locators.country_code, locator_type='xpath').text) == 0:
            if self.config.platform != 'DCL':
                self.webDriver.set_text(element=self.locators.country_code, locator_type='xpath', text='United States (+ 1)')
            else:
                self.webDriver.set_text(element=self.locators.country_code, locator_type='xpath',
                                        text='+1')
        if len(self.webDriver.get_web_element(element=self.locators.add_contact_no, locator_type='xpath').text) == 0:
            self.webDriver.set_text(element=self.locators.add_contact_no, locator_type='xpath', text='1234567890')
        else:
            self.webDriver.click(element=self.locators.add_contact_no, locator_type='xpath')
            self.webDriver.driver.hide_keyboard()
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if self.config.platform != 'DCL':
            if len(self.webDriver.get_web_element(element=self.locators.country, locator_type='xpath').text) == 0:
                self.webDriver.set_text(element=self.locators.country, locator_type='xpath', text='United States')

    def update_emergency_contact(self):
        """
        Func to update emergency contact
        :return:
        """
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.emergency_name, locator_type='xpath'):
            self.webDriver.click(element=self.locators.emergency_contact, locator_type='xpath')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

        if self.get_emergency_status() == 'Pending':
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            if self.webDriver.get_text(element=self.locators.emergency_name, locator_type='xpath') == '':
                self.webDriver.set_text(element=self.locators.emergency_name, locator_type='xpath', text='Jack')
            if self.webDriver.get_text(element=self.locators.emergency_relation, locator_type='xpath') == '- Select -' or self.webDriver.get_text(element=self.locators.emergency_relation, locator_type='xpath') == '':
                if self.config.platform == 'DCL':
                    self.webDriver.set_text(element=self.locators.emergency_relation, locator_type='xpath', text="SPOUSE")
                else:
                    self.webDriver.click(element=self.locators.emergency_relation, locator_type='xpath')
                    self.webDriver.click(element=self.locators.emergency_relation_select, locator_type='xpath')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            if self.webDriver.get_text(element=self.locators.emergency_country_code, locator_type='xpath') == '':
                if self.config.platform != 'DCL':
                    self.webDriver.set_text(element=self.locators.emergency_country_code, locator_type='xpath',
                                            text='United States (+ 1)')
                else:
                    self.webDriver.set_text(element=self.locators.emergency_country_code, locator_type='xpath',
                                            text='UNITED STATES OF AMERICA (+ 1)')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            if self.webDriver.get_web_element(element=self.locators.emer_contact_no, locator_type='xpath').text == '':
                self.webDriver.set_text(element=self.locators.emer_contact_no, locator_type='xpath',
                                        text='7898767898')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

    def click_save_proceed(self):
        """
        Func to click on save and proceed
        :return:
        """
        self.webDriver.click(element=self.locators.save_proceed, locator_type='xpath')
        self.webDriver.wait_for(2)

    def scroll_top(self):
        """
        Func to scroll to top of page
        :return:
        """
        self.webDriver.scroll_mobile(x_press=637, y_press=366, x_move=653, y_move=1141)

    def additional(self):
        """
        Add additional question
        """
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if self.webDriver.is_element_display_on_screen(element=self.locators.legal, locator_type='xpath'):
            if self.webDriver.get_web_element(element=self.locators.legal, locator_type='xpath').text == 'Pending':
                if not self.webDriver.is_element_display_on_screen(element=self.locators.legal_guardian,
                                                                   locator_type='id'):
                    self.webDriver.click(element=self.locators.legal, locator_type='id')
                self.webDriver.click(element=self.locators.click_yes, locator_type='id')
