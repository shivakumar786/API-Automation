__author__ = 'sarvesh.singh'

import time

from virgin_utils import *


class Identification(General):
    """
    Page class for identification screen of ACI app
    """

    def __init__(self, web_driver, guest_data, test_data, rest_ship, couch, config):
        """
        To initialise the locators
        :param web_driver:
        :param guest_data:
        :param test_data:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.rest_ship = rest_ship
        self.couch = couch
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "identification": "//*[@content-desc='Identification']",
                "identification_tick_mark": "//*[@content-desc='Identification']/*[@class='android.widget.ImageView']",
                "photo": "com.decurtis.dxp.aci:id/securityPhoto",
                "verify_photo": "//*[@text='VERIFY PHOTO']",
                "dob_not_available": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/date_of_birth']",
                "capture": "//*[@text='CAPTURE']",
                "photo_status": "//*[@text='Photo']/following-sibling::android.widget.TextView",
                "passport_status": "//*[@text='Primary Document']/following-sibling::android.widget.TextView",
                "document_type_dropdown": "//*[@text='Primary Document']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "document_select": "//*[@text='Passport']",
                "given_name": "//*[@text='Given Name']/../following-sibling::android.widget.EditText",
                "sur_name": "//*[@text='Surname']/../following-sibling::android.widget.EditText",
                "gender_dropdown": "//*[@text='Gender']/../following-sibling::android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "gender_dropdown_select": "//*[@text='%s']",
                "passport_number": "//*[@text='Document Number']/../following-sibling::android.widget.EditText",
                "place_insurance": "//*[@text='Place of Issuance']/../following-sibling::android.widget.EditText",
                "place_insurance_select": "//*[@text='United States']",
                "expires_on": "//*[@text='Expires on']/../following-sibling::android.widget.EditText",
                "nationality": "//*[@text='Nationality']/../following-sibling::android.widget.EditText",
                "us_nationality": "//*[@text='United States']",
                "issued_on": "//*[@text='Issued on']/../following-sibling::android.widget.EditText",
                "click_allow_using_app": "//*[@text='While using the app']",
                "click_allow": "//*[@text='Allow']",
                "take_photo": "//*[@text='Take picture']",
                "click_ok": "//*[@text='OK']",
                "click_crop": "//*[@text='CROP']",
                "save_proceed": "com.decurtis.dxp.aci:id/save_and_proceed",
                "update": "//*[@text='UPDATE']",
                "options": "//*[text()='More Options']",
                "manage_alerts": "//*[text()='Manage Alerts']",
                "create_alert": "//*[text()='CREATE ALERT']",
                "select_alert": "//*[text()='- Select -']",
                "select_approved_minor": "//*[text()='APPROVED MINOR']",
                "click_create": "//*[text()='CREATE']",
                "click_edit": "//*[text()='EDIT']",
                "click_delete": "//*[text()='DELETE']",
                "select_birthday": "//*[text()='BIRTHDAY']",
                "delete_popup": "android:id/button1",
                "navigate_back": "//*[@content-desc='Navigate up']",
                "click_yes": "android:id/button1",
                "view_details": "com.decurtis.dxp.aci:id/message",
                "view_detail": "com.decurtis.dxp.aci:id/view_details",
                "verify_doc": "com.decurtis.dxp.aci:id/verify_document",
                "other_document": "//*[text()='Supporting Document']",
                "other_doc_status": "//*[@text='Supporting Document']/following-sibling::android.widget.TextView",
                "select_second_doc": "//*[text()='- Select -']",
                "select_visa": "//*[text()='Visa']",
                "select_visa_type": "//*[@text='Visa Type']/../following-sibling::android.widget.EditText",
                "get_name": "com.decurtis.dxp.aci:id/name",
                "get_dob": "com.decurtis.dxp.aci:id/date_of_birth",
                "get_gender": "com.decurtis.dxp.aci:id/age_and_gender",
                "select_dob": "//*[@text='Date of Birth']/../following-sibling::android.widget.EditText",
                "number_entries": "//*[@text='Number of Entries']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "check_in_button": "//*[@text='CHECK-IN']",
                "back_button": "//android.widget.ImageButton[@content-desc='‎‏‎‎‎‎‎‏‎‏‏‏‎‎‎‎‎‏‎‎‏‎‎‎‎‏‏‏‏‏‎‏‏‎‏‏‎‎‎‎‏‏‏‏‏‏‏‎‏‏‏‏‏‎‏‎‎‏‏‎‏‎‎‎‎‎‏‏‏‎‏‎‎‎‎‎‏‏‎‏‏‎‎‏‎‏‎‏‏‏‏‏‎‎Navigate up‎‏‎‎‏‎']",
                "select_visa_type_select": "//*[@text='H-1B Temporary Worker']",
                "citizenship": "//*[@resource-id='com.decurtis.dxp.aci:id/citizenship']",
                "photo_s": "//*[@text='%s']",
                "citizenship_photo": "com.decurtis.dxp.aci:id/citizenship",
                "total_guests": "com.decurtis.dxp.aci:id/guest_status",
                "edit_details": "//*[@text='EDIT DETAILS']",
                "edit_details_bottom": "//*[@text='EDIT GUEST DETAILS']",
            })
        else:
            self.locators = self.dict_to_ns({
                "identification": "//*[@text='IDENTIFICATION']",
                "identification_tick_mark": "//*[@content-desc='Identification']/*[@class='android.widget.ImageView']",
                "photo": "com.decurtis.dxp.aci.dclnp:id/securityPhoto",
                "verify_photo": "//*[@text='VERIFY PHOTO']",
                "dob_not_available": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/date_of_birth']",
                "edit_details": "//*[@text='EDIT DETAILS']",
                "edit_details_bottom": "//*[@text='EDIT GUEST DETAILS']",
                "capture": "//*[@text='TAKE PHOTO']",
                "photo_status": "//*[@text='Photo']/following-sibling::android.widget.TextView",
                "passport_status": "//*[@text='Primary Document']/following-sibling::android.widget.TextView",
                "document_type_dropdown": "//*[@text='Primary Document']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "document_select": "//*[@text='Passport']",
                "given_name": "//*[@text='Given Name']/../following-sibling::android.widget.EditText",
                "sur_name": "//*[@text='Last Name']/../following-sibling::android.widget.EditText",
                "gender_dropdown": "//*[@text='Gender']/../following-sibling::android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "gender_dropdown_select": "//*[@text='%s']",
                "passport_number": "//*[@text='Document Number']/../following-sibling::android.widget.EditText",
                "place_insurance": "//*[@text='Place of Issuance']/../following-sibling::android.widget.EditText",
                "expires_on": "//*[@text='Expires on']/../following-sibling::android.widget.EditText",
                "nationality": "//*[@text='Nationality']/../following-sibling::android.widget.EditText",
                "us_nationality": "//*[@text='UNITED STATES OF AMERICA']",
                "issued_on": "//*[@text='Issued on']/../following-sibling::android.widget.EditText",
                "click_allow_using_app": "//*[@text='While using the app']",
                "click_allow": "//*[@text='Allow']",
                "take_photo": "//*[@text='Take picture']",
                "click_ok": "//*[@text='OK']",
                "click_crop": "//*[@text='CROP']",
                "save_proceed": "com.decurtis.dxp.aci.dclnp:id/save_and_proceed",
                "update": "//*[@text='UPDATE']",
                "options": "//*[text()='More Options']",
                "manage_alerts": "//*[text()='Manage Alerts']",
                "create_alert": "//*[text()='CREATE ALERT']",
                "select_alert": "//*[text()='- Select -']",
                "select_approved_minor": "//*[text()='APPROVED MINOR']",
                "click_create": "//*[text()='CREATE']",
                "click_edit": "//*[text()='EDIT']",
                "click_delete": "//*[text()='DELETE']",
                "select_birthday": "//*[text()='BIRTHDAY']",
                "delete_popup": "android:id/button1",
                "navigate_back": "//*[@content-desc='Navigate up']",
                "click_yes": "android:id/button1",
                "view_details": "com.decurtis.dxp.aci.dclnp:id/message",
                "view_detail": "com.decurtis.dxp.aci.dclnp:id/view_details",
                "verify_doc": "com.decurtis.dxp.aci.dclnp:id/verify_document",
                "other_document": "//*[text()='Supporting Document']",
                "other_doc_status": "//*[@text='Supporting Document']/following-sibling::android.widget.TextView",
                "select_second_doc": "//*[text()='- Select -']",
                "select_visa": "//*[text()='Visa']",
                "select_visa_type": "//*[@text='Visa Type']/../following-sibling::android.widget.EditText",
                "get_name": "com.decurtis.dxp.aci.dclnp:id/name",
                "get_dob": "com.decurtis.dxp.aci.dclnp:id/date_of_birth",
                "get_gender": "com.decurtis.dxp.aci.dclnp:id/age_and_gender",
                "select_dob": "//*[@text='Date of Birth']/../following-sibling::android.widget.EditText",
                "number_entries": "//*[@text='Number of Entries']/../following-sibling::android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.Spinner/android.widget.TextView",
                "check_in_button": "//*[@text='CHECK-IN']",
                "back_button": "//android.widget.ImageButton[@content-desc='‎‏‎‎‎‎‎‏‎‏‏‏‎‎‎‎‎‏‎‎‏‎‎‎‎‏‏‏‏‏‎‏‏‎‏‏‎‎‎‎‏‏‏‏‏‏‏‎‏‏‏‏‏‎‏‎‎‏‏‎‏‎‎‎‎‎‏‏‏‎‏‎‎‎‎‎‏‏‎‏‏‎‎‏‎‏‎‏‏‏‏‏‎‎Navigate up‎‏‎‎‏‎']",
                "select_visa_type_select": "//*[@text='H-1B Temporary Worker']",
                "citizenship": "//*[@resource-id='com.decurtis.dxp.aci:id/citizenship']",
                "photo_s": "//*[@text='%s']",
                "citizenship_photo": "com.decurtis.dxp.aci.dclnp:id/citizenship",
                "capture_image": "com.decurtis.dxp.aci.dclnp:id/image_capture",
                "allow_camera": "com.android.packageinstaller:id/permission_allow_button",
                "camera_pop_up": "com.android.packageinstaller:id/desc_container",
                "click_passport_image": "com.decurtis.dxp.aci.dclnp:id/capture",
                "save_pass_image": "com.decurtis.dxp.aci.dclnp:id/crop_image_menu_crop",
                "total_guests": "com.decurtis.dxp.aci.dclnp:id/guest_status"
            })
        self.guest_data = guest_data

    def click_identification_tab(self):
        """
        Func to click on identification tab
        :return:
        """
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.identification, locator_type='xpath'):
            self.webDriver.click(element=self.locators.identification, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.click_yes, locator_type='id'):
                self.webDriver.click(element=self.locators.click_yes, locator_type='id')
            self.webDriver.explicit_visibility_of_element(element=self.locators.photo_status, locator_type='xpath', time_out=60)
            return True
        else:
            return False

    def check_identification_tab_enabled(self):
        """
        Func to check if identification tab is enabled
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.identification, locator_type='xpath'):
            return self.webDriver.get_web_element(element=self.locators.identification, locator_type='xpath').get_attribute(
                "selected")
        else:
            return "false"

    def check_identification_tab_tick_mark_selected(self):
        """
        Func to check if identification tab is enabled
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.identification_tick_mark, locator_type='xpath'):
            return self.webDriver.is_element_selected(element=self.locators.identification_tick_mark, locator_type='xpath').get_attribute(
                "selected")
        else:
            return "false"

    def check_us_guest(self):
        """
        Func to check if guest is of US
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.identification, locator_type='xpath').get_attribute(
            "selected")

    def get_security_photo_status(self):
        """
        Func to get the security photo status
        :return:
        """
        self.webDriver.wait_for(2)
        return self.webDriver.get_web_element(element=self.locators.photo_status, locator_type='xpath').text

    def check_verify_photo_displayed(self):
        """
        Func to check if the verify photo is displayed
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.verify_photo, locator_type='xpath')

    def check_photo_displayed(self):
        """
        Func to check if the retake photo is displayed
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.capture, locator_type='xpath'):
            return self.webDriver.is_element_enabled(element=self.locators.capture, locator_type='xpath')

    def get_passport_photo_status(self):
        """
        Func to get the passport photo status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.passport_status, locator_type='xpath').text

    def get_support_document_status(self):
        """
        Func to fet supporting document photo status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.other_doc_status, locator_type='xpath').text

    def update_photo(self):
        """
        Func to update the photo step
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.photo, locator_type='id'):
            self.open(self.get_security_photo_status())
            self.get_guest_details()
        else:
            self.get_guest_details()
        if self.get_security_photo_status() == 'Pending':
            if self.check_verify_photo_displayed():
                self.webDriver.click(element=self.locators.verify_photo, locator_type='xpath')
            elif self.check_photo_displayed():
                upload_guest_media_file(self.test_data, self.rest_ship, self.couch, self.config)
                time.sleep(10)
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
                if self.webDriver.is_element_display_on_screen(element=self.locators.click_yes, locator_type='id'):
                    self.webDriver.click(element=self.locators.click_yes, locator_type='id')
                    time.sleep(20)
                if self.webDriver.is_element_display_on_screen(element=self.locators.check_in_button, locator_type='xpath'):
                    self.webDriver.click(element=self.locators.check_in_button, locator_type='xpath')
                else:
                    self.webDriver.click(element=self.locators.click_edit, locator_type='xpath')
                self.click_identification_tab()
                if self.check_verify_photo_displayed():
                    self.webDriver.click(element=self.locators.verify_photo, locator_type='xpath')

    def update_passport(self):
        """
        Func to update the passport step
        :return:
        """
        self.webDriver.scroll_mobile(x_press=790, y_press=1166, x_move=785, y_move=808)
        self.webDriver.wait_for(2)
        if self.get_passport_photo_status() == 'Pending':
            if not self.webDriver.is_element_display_on_screen(element=self.locators.document_type_dropdown, locator_type='xpath'):
                self.open(self.get_passport_photo_status())
            if self.webDriver.get_web_element(element=self.locators.document_type_dropdown,
                                              locator_type='xpath').text == "- Select -":
                self.webDriver.click(element=self.locators.document_type_dropdown, locator_type='xpath')
                self.webDriver.click(element=self.locators.document_select, locator_type='xpath')
            # if self.config.platform == 'DCL':
            #     self.webDriver.scroll_mobile(x_press=534, y_press=1200, x_move=529, y_move=751)
            self.webDriver.scroll_mobile(x_press=534, y_press=1200, x_move=529, y_move=751)
            self.webDriver.wait_for(2)
            # self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
            # self.webDriver.wait_for(2)
            if self.config.platform != 'DCL':
                self.webDriver.scroll_mobile(x_press=1223, y_press=2230, x_move=1130, y_move=1022)
                if self.webDriver.is_element_display_on_screen(element=self.locators.view_detail, locator_type='id'):
                    self.webDriver.click(element=self.locators.view_detail, locator_type='id')
                    self.webDriver.click(element=self.locators.update, locator_type='xpath')
            else:
                if self.webDriver.is_element_display_on_screen(element=self.locators.view_details, locator_type='id'):
                    self.webDriver.click(element=self.locators.view_detail, locator_type='id')
                    self.webDriver.click(element=self.locators.update, locator_type='xpath')
            if self.config.platform != 'DCL':
                self.webDriver.scroll_mobile(x_press=1223, y_press=2230, x_move=1130, y_move=1022)
                if self.webDriver.is_element_display_on_screen(element=self.locators.verify_doc, locator_type='id'):
                    self.webDriver.click(element=self.locators.verify_doc, locator_type='id')
            else:
                if self.webDriver.is_element_display_on_screen(element=self.locators.verify_doc, locator_type='id'):
                    self.webDriver.click(element=self.locators.verify_doc, locator_type='id')
            self.webDriver.scroll_mobile(x_press=586, y_press=841, x_move=604, y_move=583)
            self.webDriver.wait_for(2)
            if len(self.webDriver.get_web_element(element=self.locators.given_name, locator_type='xpath').text) == 0:
                if self.config.platform == 'DCL':
                    self.capture_passport_image()
                self.webDriver.set_text(element=self.locators.given_name, locator_type='xpath',
                                        text=self.guest_data[0]['FirstName'])
                self.webDriver.set_text(element=self.locators.sur_name, locator_type='xpath',
                                        text=self.guest_data[0]['LastName'])
                self.webDriver.click(element=self.locators.gender_dropdown, locator_type='xpath')
                self.webDriver.click(element=self.locators.gender_dropdown_select % self.guest_data[0]['gender'].strip(), locator_type='xpath')
                self.webDriver.set_text(element=self.locators.select_dob, locator_type='xpath', text=self.guest_data[0]['dob'])
                self.webDriver.set_text(element=self.locators.passport_number, locator_type='xpath',
                                        text=self.guest_data[0]['Phones'][0]['number'])
                time.sleep(2)
                self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
                if self.config.platform == 'DCL':
                    self.webDriver.scroll_mobile(x_press=586, y_press=841, x_move=604, y_move=583)
                    self.webDriver.set_text(element=self.locators.place_insurance, locator_type='xpath', text='UNITED STATES OF AMERICA')
                else:
                    self.webDriver.set_text(element=self.locators.place_insurance, locator_type='xpath', text='United States')
                time.sleep(3)
                self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
                self.webDriver.scroll_mobile(x_press=586, y_press=841, x_move=604, y_move=583)
                self.webDriver.set_text(element=self.locators.expires_on, locator_type='xpath', text='11/13/2031')
                if self.config.platform != 'DCL':
                    self.webDriver.set_text(element=self.locators.issued_on, locator_type='xpath', text='11/13/2019')
                else:
                    if self.webDriver.is_element_display_on_screen(element=self.locators.view_details,
                                                                   locator_type='id'):
                        self.webDriver.click(element=self.locators.view_detail, locator_type='id')
                        self.webDriver.click(element=self.locators.update, locator_type='xpath')
            else:
                self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.other_doc_status, locator_type='xpath'):
            self.webDriver.explicit_visibility_of_element(element=self.locators.save_proceed, locator_type='id',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.save_proceed, locator_type='id')
        else:
            self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)

    def click_options(self):
        """
        Func to click on more options button on guest details page
        """
        self.webDriver.click(element=self.locators.options, locator_type='xpath')

    def click_manage_alerts(self):
        """
        Func to click on manage alerts button on guest details page
        """
        self.webDriver.click(element=self.locators.manage_alerts, locator_type='xpath')

    def click_create_alert(self):
        """
        Func to click on create alert button
        """
        self.webDriver.click(element=self.locators.create_alert, locator_type='xpath')

    def select_alert_type_from_dropdown(self):
        """
        Func to click on select alert drop down button
        """
        self.webDriver.click(element=self.locators.select_alert, locator_type='xpath')

    def select_approved_minor_alert_form_dropdown(self):
        """
        Func to click on select approved minor alert from drop down
        """
        self.webDriver.click(element=self.locators.select_approved_minor, locator_type='xpath')
        self.webDriver.scroll_mobile(x_press=1595, y_press=2400, x_move=1574, y_move=1332)

    def click_on_create_alert_button(self):
        """
        Func to click on create alert button
        """
        self.webDriver.click(element=self.locators.click_create, locator_type='xpath')

    def click_on_edit_alert(self):
        """
        Func to click on edit alert button
        """
        self.webDriver.click(element=self.locators.click_edit, locator_type='xpath')

    def select_birthday(self):
        """
        Func to click on birthday alert button
        """
        self.webDriver.click(element=self.locators.select_birthday, locator_type='xpath')
        self.webDriver.scroll_mobile(x_press=1595, y_press=2400, x_move=1574, y_move=1332)

    def click_on_delete_alert(self):
        """
        Func to click on delete alert button
        """
        self.webDriver.click(element=self.locators.click_delete, locator_type='xpath')
        self.webDriver.click(element=self.locators.delete_popup, locator_type='id')

    def navigate_back(self):
        """
        Func to navigate back
        """
        self.webDriver.click(element=self.locators.navigate_back, locator_type='xpath')

    def get_guest_details(self):
        """
        Get all the guest details
        """
        data = self.webDriver.get_web_element(element=self.locators.get_name, locator_type='id').text.split(',')
        self.guest_data[0]['LastName'] = data[0]
        self.guest_data[0]['FirstName'] = data[1]
        data = self.webDriver.get_web_element(element=self.locators.get_dob, locator_type='id').text.split(':')
        self.guest_data[0]['dob'] = data[1]
        data = self.webDriver.get_web_element(element=self.locators.get_gender, locator_type='id').text.split(',')
        self.guest_data[0]['gender'] = data[1]
        self.test_data['guest_detail'] = {"fname": self.guest_data[0]['FirstName'], "lname": self.guest_data[0]['LastName'],
                                          "dob": self.guest_data[0]['dob'], "gender": self.guest_data[0]['gender']}
        self.test_data['citizenshipCountryCode'] = self.webDriver.get_web_element(element=self.locators.citizenship_photo, locator_type='id').text

    def update_support_doc(self):
        """
        Update support document
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.other_doc_status, locator_type='xpath'):
            if self.get_support_document_status() == 'Pending':
                self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
                self.webDriver.wait_for(2)
                self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
                self.webDriver.wait_for(2)
                if self.webDriver.is_element_display_on_screen(element=self.locators.verify_doc, locator_type='id'):
                    self.webDriver.scroll_mobile(x_press=609, y_press=730, x_move=604, y_move=359)
                    self.webDriver.click(element=self.locators.verify_doc, locator_type='id')
                if self.webDriver.is_element_display_on_screen(element=self.locators.select_second_doc,
                                                               locator_type='xpath'):
                    self.webDriver.click(element=self.locators.select_second_doc, locator_type='xpath')
                    self.webDriver.click(element=self.locators.select_visa, locator_type='xpath')
                    self.webDriver.set_text(element=self.locators.given_name, locator_type='xpath',
                                            text=self.guest_data[0]['FirstName'])
                    self.webDriver.set_text(element=self.locators.sur_name, locator_type='xpath',
                                            text=self.guest_data[0]['LastName'])
                    self.webDriver.click(element=self.locators.select_visa_type, locator_type='xpath')
                    time.sleep(1)
                    self.webDriver.set_text(element=self.locators.select_visa_type, locator_type='xpath',
                                            text="H-1B Temporary Worker")
                    time.sleep(3)
                    self.webDriver.click(element=self.locators.select_visa_type_select, locator_type='xpath')
                    self.webDriver.set_text(element=self.locators.passport_number, locator_type='xpath',
                                            text=self.guest_data[0]['Phones'][0]['number'])
                    self.webDriver.set_text(element=self.locators.expires_on, locator_type='xpath', text='11/13/2031')
                    self.webDriver.click(element=self.locators.number_entries, locator_type='xpath')
                    self.webDriver.explicit_visibility_of_element(element=self.locators.save_proceed, locator_type='id',
                                                                  time_out=60)
                    self.webDriver.click(element=self.locators.save_proceed, locator_type='id')
            else:
                self.webDriver.explicit_visibility_of_element(element=self.locators.save_proceed, locator_type='id',
                                                              time_out=60)
                self.webDriver.click(element=self.locators.save_proceed, locator_type='id')
        self.webDriver.explicit_visibility_of_element(element=self.locators.save_proceed, locator_type='id',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.save_proceed, locator_type='id')

    def check_us_citizenship(self):
        """
        check us citizenship
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.us_nationality, locator_type='xpath')

    def open(self, status):
        """
        open photo
        """
        self.webDriver.click(element=self.locators.photo_s % status, locator_type='xpath')

    def capture_passport_image(self):
        """
        Click the passport image
        """
        self.webDriver.click(element=self.locators.capture_image, locator_type='id')
        if self.webDriver.is_element_display_on_screen(element=self.locators.camera_pop_up, locator_type='id'):
            self.webDriver.click(element=self.locators.allow_camera, locator_type='id')
            self.webDriver.click(element=self.locators.allow_camera, locator_type='id')
            self.webDriver.click(element=self.locators.click_passport_image, locator_type='id')
            self.webDriver.click(element=self.locators.save_pass_image, locator_type='id')
        else:
            self.webDriver.click(element=self.locators.click_passport_image, locator_type='id')
            self.webDriver.click(element=self.locators.save_pass_image, locator_type='id')

    def get_total_guests(self):
        """
        Function to get the total guests on Identification screen
        :return:
        """
        return len(self.webDriver.get_elements(element=self.locators.total_guests, locator_type='id'))

    def check_availability_of_dob_and_fill(self):
        """
        Function to check the availability of DOB value in Personal details
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.dob_not_available, locator_type='xpath'):
            logger.info("DOB is not available on screen, so we need to fill")
            if self.webDriver.is_element_display_on_screen(element=self.locators.edit_details, locator_type='xpath'):
                self.webDriver.click(element=self.locators.edit_details, locator_type='xpath')
            else:
                self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
                self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
                self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
                self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
                self.webDriver.scroll_mobile(x_press=511, y_press=1169, x_move=493, y_move=795)
                self.webDriver.click(element=self.locators.edit_details_bottom, locator_type='xpath')

        self.webDriver.set_text(element=self.locators.select_dob, locator_type='xpath', text='05/05/1987')
        self.webDriver.click(element=self.locators.update, locator_type='xpath')









