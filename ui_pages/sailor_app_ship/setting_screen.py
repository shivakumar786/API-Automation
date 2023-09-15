__author__ = 'mohit.raghav'

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
            "camera_icon": "//*[@id='photoCameraButton']",
            "logout": "//*[@text='Logout']",
            "confirm_logout": "//*[@text='Yes, log out']",
            "sign_in": "//*[@text='Sign in']",
            "notifications_and_privacy_btn": "//*[text()='Notifications & privacy']",
            "voyage_settings_header": "//h1[text()='Voyage Settings']",
            'the_band_and_pin': "//div[text()='The Band and PIN']",
            "notification_and_privacy": "//div[text()='Notifications & privacy']",
            "emergency_contact": "//div[text()='Emergency contact']",
            "sailings_documents": "//div[text()='Sailing documents']",
            'profile_and_settings_header': "//h1[text()='Profile & Settings']",
            'personal_information': "//div[text()='Personal information']",
            'contact_details': "//div[text()='Contact details']",
            'login_details': "//div[text()='Login details']",
            'communication_preferences': "//div[text()='Communication preferences']",
            'terms_and_conditions': "//div[text()='Terms and conditions']",
            'payment_methods': "//div[text()='Payment methods']",
            'disabled_section': "//div[@class='MenuItem disabled']",
            'switch_voyage_btn': "//button[@class='button button-outline is-disabled']",
            'login_details_header': "//h1[text()='Login Details']",
            'login_with_biometric': "//div[text()='Login with biometric ID']",
            'default_toggle_disabled': "//div[@class='react-toggle Toggle']",
            'default_toggle_enabled': "//div[@class='react-toggle react-toggle--checked Toggle']",
            'biometric_toggle_disabled': "//div[@class='react-toggle react-toggle--focus Toggle']",
            'biometric_toggle_enabled': "//div[@class='react-toggle react-toggle--checked react-toggle--focus Toggle']",
            'change_your_email': "//div[text()='Change your email']",
            'change_your_password': "//div[text()='Change your email']"
        })

    def logout(self):
        """
        Function to Logout from app
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.camera_icon, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.scroll_complete_page()
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')
        self.webDriver.click(element=self.locators.confirm_logout, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_in, locator_type='xpath'
                                                      , time_out=60)

    def open_notifications_and_privacy(self):
        """
        Function to open notifications and privacy screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.notifications_and_privacy_btn,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.notifications_and_privacy_btn,
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.notifications_and_privacy_btn, locator_type='xpath')

    def verify_landing_on_setting_screen(self):
        """
        Function to verify that user has landed on settings screen
        :return :
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.voyage_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_settings_header,
                                                       locator_type='xpath'):
            logger.info("Settings title is available on the screen ")
        else:
            raise Exception("Settings title is not available on the screen")

    def verify_availability_of_the_band_and_pin(self):
        """
        Function to verify the availability of the band and pin section in voyage settings
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.voyage_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.the_band_and_pin,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.the_band_and_pin, locator_type='xpath')
            logger.info("The Band and Pin section is available on the screen")
        else:
            raise Exception("The Band and Pin section is not available on the screen")

    def verify_availability_of_notifications_and_privacy(self):
        """
        Function to verify availability of notifications and privacy section in voyage settings
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.voyage_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.notification_and_privacy,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.notification_and_privacy, locator_type='xpath')
            logger.info("Notification and privacy section is available on the screen")
        else:
            raise Exception("Notification and privacy section is not available on the screen")

    def verify_availability_of_emergency_contact(self):
        """
        Function to verify availability of emergency contacts section in voyage settings
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.voyage_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.emergency_contact,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.emergency_contact, locator_type='xpath')
            logger.info("Emergency contacts section is available on the screen ")
        else:
            raise Exception("Emergency contacts section is not available on the screen")

    def verify_availability_of_sailing_documents(self):
        """
        Function to verify availability of emergency contacts section in voyage settings
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.voyage_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailings_documents,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.sailings_documents, locator_type='xpath')
            logger.info("Sailing documents section is available on the screen ")
        else:
            raise Exception("Sailing documents section is not available on the screen")
        
    def verify_availability_of_profile_settings_header(self):
        """
        Function to verify availability of profile settings header
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.profile_and_settings_header,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.profile_and_settings_header,
                                               locator_type='xpath')
            logger.info("Profile settings header is available on screen")
        else:
            raise Exception("Profile settings header is not available on screen")

    def verify_availability_of_personal_information(self):
        """
        Function to verify availability of personal information section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.personal_information,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.personal_information, locator_type='xpath')
            logger.info("Personal information section is available on the screen ")
        else:
            raise Exception("Personal information section is not available on the screen")

    def verify_availability_of_contact_details(self):
        """
        Function to verify availability of contact details
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.contact_details,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.contact_details, locator_type='xpath')
            logger.info("Contact details section is available on the screen")
        else:
            raise Exception("Contact details section is not available on the screen")

    def verify_availability_of_login_details(self):
        """
        Function to verify availability of login details
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_details,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.login_details, locator_type='xpath')
            logger.info("Login details section is available on the screen ")
        else:
            raise Exception("Login details section is not available on the screen")

    def verify_availability_of_payment_methods(self):
        """
        Function to verify availability of payment methods
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_methods,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.payment_methods, locator_type='xpath')
            logger.info("Payment methods section is available on the screen ")
        else:
            raise Exception("Payment methods section is not available on the screen")

    def verify_availability_of_communication_preferences(self):
        """
        Function to verify availability of communication preference
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.communication_preferences,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.communication_preferences, locator_type='xpath')
            logger.info("Communication_preferences section is available on the screen ")
        else:
            raise Exception("Communication_preferences section is not available on the screen")

    def verify_availability_of_terms_and_conditions(self):
        """
        Function to verify availability of terms and conditions
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.terms_and_conditions,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.terms_and_conditions, locator_type='xpath')
            logger.info("Terms and conditions section is available on the screen ")
        else:
            raise Exception("Terms and conditions section is not available on the screen")

    def verify_payments_methods_disabled(self):
        """
        Function to verify payment methods are disabled
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        disabled_section = self.webDriver.get_text(element=self.locators.disabled_section, locator_type='xpath')
        if disabled_section.split("\n")[0] == "Payment methods":
            logger.info("Payment methods section is disabled")
        else:
            raise Exception("Payment methods section is not disabled")

    def verify_switch_voyage_button_disabled(self):
        """
        Function to verify switch voyage button is disabled
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.profile_and_settings_header,
                                                          locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.switch_voyage_btn, locator_type='xpath')
        disabled_btn = self.webDriver.get_text(element=self.locators.switch_voyage_btn, locator_type='xpath')
        if disabled_btn == 'Switch Voyage':
            logger.info("Switch voyage btn is disabled")
        else:
            raise Exception("Switch voyage btn is not disabled")

    def open_login_details(self):
        """
        Function to open login details
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.login_details, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.login_details_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_details_header, locator_type='xpath'):
            logger.info("User has landed on the login details page")
        else:
            raise Exception("User has not landed on the login details page")

        if self.webDriver.is_element_display_on_screen(element=self.locators.change_your_email, locator_type='xpath'):
            logger.info("Change your email option is available")
        else:
            raise Exception("Change your email option is not available")

        if self.webDriver.is_element_display_on_screen(element=self.locators.change_your_password, locator_type='xpath'):
            logger.info("Change your password option is available")
        else:
            raise Exception("Change your password option is not available")
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_with_biometric,
                                                       locator_type='xpath'):
            logger.info("Biometric login option is getting displayed")
        else:
            raise Exception("Biometric login option is not getting displayed in login details page")

    def enable_biometric_login(self):
        """
        Function to enable biometric login for sailor
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.default_toggle_disabled,
                                                       locator_type='xpath'):
            logger.info("Biometric login is is disabled. Enabling now")
            self.webDriver.click(element=self.locators.default_toggle_disabled, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.biometric_toggle_enabled,
                                                           locator_type='xpath'):
                logger.info("Biometric login is enabled now")
            else:
                raise Exception("Biometric login is not getting enabled")
        elif self.webDriver.is_element_display_on_screen(element=self.locators.default_toggle_enabled,
                                                         locator_type='xpath'):
            logger.info("Biometric login is already enabled for sailor")
        else:
            raise Exception('Biometric toggle button is not getting displayed.')
