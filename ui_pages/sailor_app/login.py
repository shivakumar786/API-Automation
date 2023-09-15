__author__ = 'prahlad.sharma'

from virgin_utils import *


class Login(General):
    """
    Page class for Login page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//*[@text='loading...']",
            "sign_in": "//*[@text='Sign in']",
            "sign_up": "//*[@text='Sign up']",
            "book_voyage": "//*[@text='Book a voyage']",
            "first_screen": "//*[@text='Swipe to get started']",
            "second_screen": "//*[@text='1']",
            "third_screen": "//*[@text='2']",
            "forth_screen": "//*[@text='3']",
            "sign_in_with_email": "//*[@text='Sign in with email']",
            "sign_up_with_email": "//*[@text='Sign up with email']",
            "sign_in_with_facebook": "//*[@id='signInWithFB']",
            "sign_in_with_google": "//*[@id='signInWithGoogle']",
            "forget_password": "//*[@id='forgottenDetailsBtn']",
            "email_id": "//*[@id='emailInput']",
            "first_name": "//*[@id='firstNameInput']",
            "last_name": "//*[@id='lastNameInput']",
            "preferred_name": "//*[@id='preferredNameInput']",
            "sign_up_password": "//*[@id='passwordInput']",
            "email_next_button": "//*[@id='registerMailButton']",
            "name_next_button": "//*[@id='registerNameButton']",
            "preferred_next_button": "//*[@id='registerPrefNameButton']",
            "password_next_button": "//*[@id='registerPasswordButton']",
            "dob_next_button": "//*[@id='registerAgeButton']",
            "login_mail_btn": "//*[@id='loginMailButton']",
            "password": "//*[@id='currentPasswordInput']",
            "popup_no": "//*[@text='NO, THANKS']",
            "popup_yes": "//*[@text='YES']",
            "skip_band": "//*[@text='Skip']",
            "month_input": "//span[@id='month_register-date-of-birth']",
            "year_text": "//input[@id='yearInput']",
            "day_text": "//input[@id='dayInput']",
            "date_text": "//*[@text='%s']",
            "cancel": "//*[@text='CANCEL']",
            "OK": "//*[@text='OK']",
            "skip_photo": "//*[@id='skipStrikePose']",
            "go_on_setting_after_signup": "//*[@class='android.widget.Image']",
            "google_icon": "//a[@id='registerWithGoogle']",
            "google_header": "//*[@text='Google']",
            "google_email_input": "identifierId",
            "next_button": "android.widget.Button",
            "google_password_input": "password",
            "connect_booking_button": "//button[@id='connectBookingButton']",
            "book_voyage_button": "//button[@id='bookVoyageButton']",
            "facebook_icon": "//a[@id='registerWithFB']",
            "facebook_header": "//div[text()='Log in to your Facebook account to connect to Virgin_Voyages']",
            "facebook_email_input": "//input[@id='m_login_email']",
            "facebook_password_input": "//input[@id='m_login_password']",
            "facebook_login_button": "//button[@name='login']",
            "signin_google_icon": "//a[@id='signInWithGoogle']",
            "facebook_signin_icon": "//a[@id='signInWithFB']",
            "previously_logged_in_to_facebook": "//div[contains(text(),'You previously logged in to Virgin_Voyages with Facebook.')]",
            "continue_login_fb":"//button[@value='Continue']",
            "google_choose_account_header": "//*[@text='Choose an account']",
            "select_google_account": "//*[@text='Joey Tribbiani']",
            "strike_a_pose": "//h1[text()='Strike a pose']",
        })

    def wait_till_first_screen(self):
        """
        To check the availability of first screen
        """
        # self.webDriver.wait_till_element_invisible(element=self.locators['loader'], locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_screen, locator_type='xpath'
                                                      , time_out=60)
        screen_title = self.webDriver.get_text(element=self.locators.first_screen, locator_type='xpath')
        if screen_title == "Swipe to get started":
            logger.debug("Desired text is available")
        else:
            raise Exception("Swipe to get started text is not available")

    def verification_of_initial_pages(self):
        """
        This function is used to check the initial 4 pages in Sailor app
        """
        self.webDriver.click(element=self.locators.first_screen, locator_type='xpath')
        self.webDriver.click(element=self.locators.second_screen, locator_type='xpath')
        self.webDriver.click(element=self.locators.third_screen, locator_type='xpath')
        self.webDriver.click(element=self.locators.forth_screen, locator_type='xpath')

    def open_signin_page(self):
        """
        To open account dropdown
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_in, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_in, locator_type='xpath')

    def open_signup_page(self):
        """
        To open account dropdown
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_up, locator_type='xpath')

    def open_signup_with_email(self):
        """
        To open account dropdown
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up_with_email, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_up_with_email, locator_type='xpath')

    def open_signin_with_email(self):
        """
        Function to click on Sing in with Email
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_in_with_email, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_in_with_email, locator_type='xpath')

    def fill_signup_details(self, guest_data):
        """
        Function to fill the details in signup flow
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.email_id, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.email_id, locator_type='xpath', text=guest_data[1]['Email'])
        self.webDriver.click(element=self.locators.email_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_name, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.first_name, locator_type='xpath', text=guest_data[1]['FirstName'])
        self.webDriver.set_text(element=self.locators.last_name, locator_type='xpath', text=guest_data[1]['LastName'])
        self.webDriver.click(element=self.locators.name_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.preferred_name, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.preferred_name, locator_type='xpath', text=guest_data[1]['FirstName'])
        self.webDriver.click(element=self.locators.preferred_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up_password, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.sign_up_password, locator_type='xpath', text="Yellow*99")
        self.webDriver.click(element=self.locators.password_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.month_input, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.month_input, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'May', locator_type='xpath')
        date_s = guest_data[0]['BirthDate'].split('-')[2]
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.set_text(element=self.locators.day_text, locator_type='xpath',
                                text=date_s)
        year_s = guest_data[0]['BirthDate'].split('-')[0]
        self.webDriver.set_text(element=self.locators.year_text, locator_type='xpath',
                                text=year_s)
        self.webDriver.click(element=self.locators.dob_next_button, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.popup_no, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.strike_a_pose, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.skip_photo, locator_type='xpath')

    def fill_signin_details(self, username, password):
        """
        To fill signin details
        :param username:
        :param password:
        :return:
        """
        self.webDriver.set_text(element=self.locators.email_id, locator_type='xpath', text=username)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.popup_no, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')

    def open_signup_with_google(self):
        """
        Function to open signin with google page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.google_icon, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.google_icon, locator_type='xpath')

    def open_signin_with_google(self):
        """
        Function to open signin with google page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.signin_google_icon, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.signin_google_icon, locator_type='xpath')

    def signup_with_google(self):
        """
        Function to signup with google
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.google_choose_account_header, locator_type='xpath'
                                                      , time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.google_choose_account_header,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.select_google_account, locator_type='xpath')
        else:
            self.webDriver.explicit_invisibility_of_element(element=self.locators.google_header, locator_type='xpath',
                                                           time_out=40)
            self.webDriver.set_text(element=self.locators.google_email_input, locator_type='id', text='Joey.tribbiani.6778@gmail.com')
            self.webDriver.driver.hide_keyboard()
            self.webDriver.click(element=self.locators.next_button, locator_type='class')
            self.webDriver.set_text(element=self.locators.google_password_input, locator_type='id',
                                    text='Yellow*99')
            self.webDriver.driver.hide_keyboard()
            self.webDriver.click(element=self.locators.next_button, locator_type='class')

    def verify_availability_of_connect_booking_button(self):
        """
        To verify availability of connect booking button after signup
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.connect_booking_button, locator_type='xpath'
                                                      , time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.connect_booking_button, locator_type='xpath'):
            logger.debug("Connect booking button is available after signup")
        else:
            raise Exception("Connect booking button is not available after signup")

    def verify_availability_of_book_voyage_button(self):
        """
        To verify availability of book voyage button after signup
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.book_voyage_button, locator_type='xpath'):
            logger.debug("Book voyage button is available on screen")
        else:
            raise Exception("Book voyage button is not available on screen")

    def open_signup_with_facebook(self):
        """
        Function to open signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.facebook_icon, locator_type='xpath')

    def open_signin_with_facebook(self):
        """
        Function to open signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.facebook_signin_icon, locator_type='xpath')

    def signup_with_facebook(self):
        """
        Function to signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_chrome')
        if self.webDriver.is_element_display_on_screen(element=self.locators.previously_logged_in_to_facebook,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.continue_login_fb, locator_type='xpath')
        else:
            self.webDriver.explicit_invisibility_of_element(element=self.locators.facebook_header, locator_type='xpath',
                                                            time_out=40)
            self.webDriver.set_text(element=self.locators.facebook_email_input, locator_type='id',
                                   text='bjqldzcduh_1658997952@tfbnw.net')
            self.webDriver.set_text(element=self.locators.facebook_password_input, locator_type='id',
                                    text='Test@1234')
            self.webDriver.click(element=self.locators.facebook_login_button, locator_type='class')

    def go_to_settings_after_signup(self):
        """
        Function to go to settings after signup
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.go_on_setting_after_signup, locator_type='xpath')
