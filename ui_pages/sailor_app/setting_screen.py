__author__ = 'prahlad.sharma'

from virgin_utils import *


class Setting_screen(General):
    """
    Page class for Setting Screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//*[@text='loading...']",
            "setting_screen_header": "//*[@text='Voyage Settings']",
            "camera_icon": "//*[@id='photoCameraButton']",
            "logout": "//*[@text='Logout']",
            "confirm_logout": "//*[@text='Yes, log out']",
            "notification_and_privacy": "//div[text()='Notifications & privacy']",
            "reminders": "//input[@id='reminderSetting']",
            "back_button": "//button[@class='BackButton']",
            "emergency_contact": "//div[text()='Emergency contact']",
            "voyage_settings": "//h1[text()='Voyage Settings']",
            "sailings_documents": "//div[@id='sailingDocumentsItem']",
            "profile_and_setting": "//h1[text()='Profile & Settings']",
            "personal_information": "//div[@id=personalInformationItem']",
            "contact_details": "//div[@id='contactDetailsItem']",
            "login_details": "/div[@id=loginDetailsItem']",
            "payment_methods": "//div[@id='paymentMethodsItem']",
            "communcation_pref":"//div[@id='communicationPreferencesItem']",
            "terms_and_conditions": "//div[@id=termsAndConditionsItem']",
            "gender": "//span[@id='genderInput']",
            "preferred_name": "//input[@id='preferredNameInput']",
            "gender_female": "//*[@text='Female']",
            "gender_male": "//*[@text='Male']",
            "personal_info_header": "//h1[text='Personal information']",
            "next_cta": "//button[@id='okButton']",
            "save_button": "//button[@id='saveButton']",
            "int_code": "//input[@id='intCodeInput']",
            "select_us_code": "//div[text='United States (+1)']",
            "update_country": "//input[@id='countryCode']",
            "select_country_us": "//div[text='United States']",
            "street": "//input[@id=streetInput']",
            "no": "//input[@id='noInput']",
            "city": "//input[@id='cityInput']",
            "state": "//input[@id='stateCode']",
            "select_state_arizona": "//div[text()='Arizona']",
            "zipcode": "//input[@id='zipCodeInput']",
            "change_email_button": "//div[@id='changeYourEmailItem]",
            "new_email": "//input[@id='newEmailInput']",
            "re_enter_new_email": "//input[@id=repeatNewEmailInput']",
            "email_updated_header": "//h1[text()='Email: updated']",
            "account_landing_button": "//button[@id='accountLandingBtn']",
            "current_password": "//input[@id='currentPasswordInput']",
            "new_password": "//input[@id='newPasswordInput']",
            "re_enter_new_password": "//input[@id='repeatNewPasswordInput']",
            "password_updated_header": "//h1[text()='Password: updated']",
            "payment_method": "//div[@id='paymentMethodsItem']",
            "communication_preferences": "//div[@id='communicationPreferencesItem']",
            "switch_voyage": "//button[@id='switchVoyageButton']",

        })

    def verify_setting_screen_landing(self):
        """
        Function to verify that user has landed on settings screen
        :return :
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_settings,
                                                       locator_type='xpath'):
            logger.info("Voyage Settings title is available on the screen ")
        else:
            raise Exception("Voyage Settings title is not available on the screen")

    def verify_availability_of_notifications_and_privacy(self):
        """
        Function to verify availability of notifications and privacy
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.notification_and_privacy,
                                                       locator_type='xpath'):
            logger.info("Notification and privacy section is available on the screen ")
        else:
            raise Exception("Notification and privacy section is not available on the screen")

    def verify_availability_of_emergency_contact(self):
        """
        Function to verify availability of emergency contacts
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.emergency_contact,
                                                       locator_type='xpath'):
            logger.info("Emergency contacts section is available on the screen ")
        else:
            raise Exception("Emergency contacts section is not available on the screen")

    def verify_availability_of_sailing_documents(self):
        """
        Function to verify availability of emergency contacts
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailings_documents,
                                                       locator_type='xpath'):
            logger.info("Sailing documents section is available on the screen ")
        else:
            raise Exception("Sailing documents section is not available on the screen")

    def open_notification_and_privacy(self):
        """
        Function to open notification and privacy
        :return:
        """
        self.webDriver.click(element=self.locators.notification_and_privacy, locator_type='xpath')

    def click_switch_voyage(self):
        """
        Function to open switch voyage section
        :return:
        """
        self.webDriver.click(element=self.locators.switch_voyage, locator_type='xpath')

    def open_terms_and_conditions(self):
        """
        Function to open terms and conditions
        :return:
        """
        self.webDriver.click(element=self.locators.terms_and_conditions, locator_type='xpath')

    def turn_reminders_off(self):
        """
        Function to turn reminders off
        :return:
        """
        self.webDriver.click(element=self.locators.reminders, locator_type='xpath')

    def turn_reminders_on(self):
        """
        Function to turn reminders on
        :return:
        """
        self.webDriver.click(element=self.locators.reminders, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def open_login_details(self):
        """
        Function to open login details
        :return:
        """
        self.webDriver.click(element=self.locators.login_details, locator_type='xpath')

    def update_email(self, guest_data):
        """
        Function to update the email of a sailor
        :param guest_data:
        :return:
        """
        self.webDriver.click(element=self.locators.change_email_button, locator_type='xpath')
        guest_data[0]['Email'] = guest_data[0]['Email'][2:]
        self.webDriver.set_text(element=self.locators.new_email, locator_type='xpath', text=guest_data[0]['Email'])
        self.webDriver.set_text(element=self.locators.re_enter_new_email, locator_type='xpath', text=guest_data[0]['Email'])

    def update_password(self):
        """
        Function to update password
        :return:
        """
        self.webDriver.set_text(element=self.locators.current_password, locator_type='xpath', text='Voyages@9876')
        self.webDriver.set_text(element=self.locators.new_password, locator_type='xpath',
                                text='Yellow*99')
        self.webDriver.set_text(element=self.locators.re_enter_new_password, locator_type='xpath',
                                text='Yellow*99')

    def verify_reminder_off(self):
        """
        Function to verify reminder off
        :return:
        """
        if self.webDriver.is_element_enabled(element=self.locators.new_booking, locator_type='xpath'):
            raise Exception("Reminders are enabled after disabled by sailor")
        else:
            logger.debug("Reminders are disabled after disabled by sailor")

    def verify_reminder_on(self):
        """
        Function to verify reminder off
        :return:
        """
        if self.webDriver.is_element_enabled(element=self.locators.new_booking, locator_type='xpath'):
            logger.debug("Reminders are enabled after enabled by sailor")
        else:
            raise Exception("Reminders are disabled after enabled by sailor")

    def open_emergency_contact(self):
        """
        Function to open emergency contact
        :return:
        """
        self.webDriver.click(element=self.locators.emergency_contact, locator_type='xpath')

    def open_payment_method(self):
        """
        Function to open payment method
        :return:
        """
        self.webDriver.click(element=self.locators.payment_method, locator_type='xpath')

    def open_communication_preferences(self):
        """
        Function to open communication preferences
        :return:
        """
        self.webDriver.click(element=self.locators.payment_method, locator_type='xpath')

    def verify_sailor_landed_on_personal_info_section(self):
        """
        To verify that sailor has landed on personal info section
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.personal_info_header,
                                                       locator_type='xpath'):
            logger.info("Personal info section is available on the screen ")
        else:
            raise Exception("Personal info section is not available on the screen")

    def verify_availability_of_profile_settings_title(self):
        """
        Function to verify availability of profile settings title
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.profile_and_setting,
                                                       locator_type='xpath'):
            logger.info("Sailing documents section is available on the screen ")
        else:
            raise Exception("Sailing documents section is not available on the screen")

    def verify_availability_of_personal_information(self):
        """
        Function to verify availability of personal information
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.personal_information,
                                                       locator_type='xpath'):
            logger.info("Personal information section is available on the screen ")
        else:
            raise Exception("Personal information section is not available on the screen")

    def verify_availability_of_contact_details(self):
        """
        Function to verify availability of contact details
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.contact_details,
                                                       locator_type='xpath'):
            logger.info("Contact details section is available on the screen ")
        else:
            raise Exception("Contact details section is not available on the screen")

    def verify_availability_of_login_details(self):
        """
        Function to verify availability of login details
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_details,
                                                       locator_type='xpath'):
            logger.info("Login details section is available on the screen ")
        else:
            raise Exception("Login details section is not available on the screen")

    def verify_availability_of_payment_methods(self):
        """
        Function to verify availability of payment methods
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_method,
                                                       locator_type='xpath'):
            logger.info("Payment methods section is available on the screen ")
        else:
            raise Exception("Payment methods section is not available on the screen")

    def verify_availability_of_communication_preferences(self):
        """
        Function to verify availability of communication preference
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.communcation_pref,
                                                       locator_type='xpath'):
            logger.info("Communication_preferences section is available on the screen ")
        else:
            raise Exception("Communication_preferences section is not available on the screen")

    def verify_availability_of_terms_and_conditions(self):
        """
        Function to verify availability of terms and conditions
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.communcation_pref,
                                                       locator_type='xpath'):
            logger.info("Terms and conditions section is available on the screen ")
        else:
            raise Exception("Terms and conditions section is not available on the screen")

    def open_personal_info(self):
        """
        Function to open personal info section
        :return:
        """
        self.webDriver.click(element=self.locators.personal_information, locator_type='xpath')

    def update_personal_info(self, test_data):
        """
        Function to get and update personal info
        :param test_data:
        :return:
        """
        gender = self.webDriver.get_text(element=self.locators.gender, locator_type='xpath')
        preferred_name = self.webDriver.get_text(element=self.locators.preferred_name, locator_type='xpath')
        test_data['preferred_name'] = preferred_name[0:2]
        self.webDriver.set_text(element=self.locators.preferred_name, locator_type='xpath', text=preferred_name)
        if gender == "Male":
            self.webDriver.click(element=self.locators.gender_female, locator_type='xpath')
            test_data['sailor_gender'] = "Female"
        elif gender == "Another Gender":
            self.webDriver.click(element=self.locators.gender_male, locator_type='xpath')
            test_data['sailor_gender'] = "Male"
        else:
            self.webDriver.click(element=self.locators.gender_male, locator_type='xpath')
            test_data['sailor_gender'] = "Male"

    def click_next_cta(self):
        """
        Function to click next/ok button
        :return:
        """
        self.webDriver.click(element=self.locators.next_cta, locator_type='xpath')

    def click_save_button(self):
        """
        Function to click save button
        :return:
        """
        self.webDriver.click(element=self.locators.save_button, locator_type='xpath')

    def verify_email_updated_confirmation_screen(self):
        """
        Function to verify Email updated screen available
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.email_updated_header,
                                                       locator_type='xpath'):
            logger.info("Email updated title is available on the screen ")
        else:
            raise Exception("Email updated title is not available on the screen")

    def verify_password_updated_confirmation_screen(self):
        """
        Function to verify Email updated screen available
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.password_updated_header,
                                                       locator_type='xpath'):
            logger.info("Email updated title is available on the screen ")
        else:
            raise Exception("Email updated title is not available on the screen")

    def click_done_button(self):
        """
        Function to click done button
        :return:
        """
        self.webDriver.click(element=self.locators.account_landing_button, locator_type='xpath')

    def verify_updated_personal_info(self, test_data):
        """
        Function to verify updated personal info
        :param test_data:
        :return:
        """
        gender = self.webDriver.get_text(element=self.locators.gender, locator_type='xpath')
        preferred_name = self.webDriver.get_text(element=self.locators.preferred_name, locator_type='xpath')
        assert gender == test_data['sailor_gender'], "Correct gender is not shown after updting personal info"
        assert preferred_name == test_data['preferred_name'], "Correct preferrred is not shown after updting personal info"

    def open_contact_details_section(self):
        """
        Function to open contact details section
        :return:
        """
        self.webDriver.click(element=self.locators.contact_details, locator_type='xpath')

    def update_contact_details(self):
        """
        Function to update contact details
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.int_code, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_us_code, locator_type='xpath')
        self.webDriver.click(element=self.locators.update_country, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_country_us, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.street, locator_type='xpath', text="365/242")
        self.webDriver.set_text(element=self.locators.no, locator_type='xpath', text="5")
        self.webDriver.set_text(element=self.locators.city, locator_type='xpath', text="Tucson")
        self.webDriver.click(element=self.locators.state, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_state_arizona, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.zipcode, locator_type='xpath', text="80245")

    def verify_updated_contact_detais(self):
        """
        Function to verify updated contact
        :return:
        """
        int_code = self.webDriver.get_text(element=self.locators.int_code, locator_type='xpath')
        country = self.webDriver.get_text(element=self.locators.update_country, locator_type='xpath')
        street = self.webDriver.get_text(element=self.locators.street, locator_type='xpath')
        no = self.webDriver.get_text(element=self.locators.no, locator_type='xpath')
        city =self.webDriver.get_text(element=self.locators.city, locator_type='xpath')
        state =self.webDriver.get_text(element=self.locators.state, locator_type='xpath')
        zipcode = self.webDriver.get_text(element=self.locators.zipcode, locator_type='xpath')
        assert int_code == "1", "Correct international code is not shown after updating contact details"
        assert country == "United States", "Correct country is not shown after updating contact details"
        assert street == "365/242", "Correct street is not shown after updating contact details"
        assert no == "5", "Correct no is not shown after updating contact details"
        assert city == "Tucson", "Correct city is not shown after updating contact details"
        assert state == "Arizona", "Correct state is not shown after updating contact details"
        assert zipcode == "80245", "Correct zipcode is not shown after updating contact details"

    def logout(self):
        """
        Function to Logout from app
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.camera_icon, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.scroll(pixel_x=0, pixel_y=1200)
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')
        self.webDriver.click(element=self.locators.confirm_logout, locator_type='xpath')
