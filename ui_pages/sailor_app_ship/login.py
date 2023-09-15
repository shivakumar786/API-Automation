__author__ = 'mohit.raghav'

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
            "first_screen": "//*[@text='Swipe to get started']",
            "second_screen": "//*[@text='1']",
            "third_screen": "//*[@text='2']",
            "forth_screen": "//*[@text='3']",
            "sign_in": "//*[@text='Sign in']",
            "sign_in_with_email": "//*[@text='Sign in with email']",
            "email_id": "//*[@id='emailInput']",
            "login_mail_btn": "//*[@id='loginMailButton']",
            "password": "//*[@id='currentPasswordInput']",
            'loading': '//img[@alt="loading..."]',
            "incorrect_creds_screen": """//div[contains(text(),"It looks like either the email or password you've entered is incorrect.")]""",
            "popup_no": "//*[@text='NO, THANKS']",
            "loader": "//*[@text='loading...']",
            'allow_access': ".//*[@text='Allow']",
            'sign_in_with_shipboard': '//*[@id="SignInShipboard"]',
            'lastname_shipboard': '//*[@id="lastNameInput"]',
            'cabin_no_shipbaord': '//*[@id="cabinNumberInput"]',
            'month_dob_shipboard': '//*[@id="month_dateOfBirthPicker"]',
            'day_dob_shipboard': "//*[@id='dayInput']",
            'year_dob_shipboard': "//*[@id='yearInput']",
            'month_index': "//*[@text='{}']",
            'shipboard_login_btn': "//*[@id='loginShipboardButton']",
            "sign_up": "//*[@text='Sign up']",
            "sign_up_with_email": "//*[@text='Sign up with email']",
            "connect_booking_button": "//button[@id='connectBookingButton']",
            "book_voyage_button": "//button[@id='bookVoyageButton']",
            "go_on_setting_after_signup": "//*[@class='VoyageUserAvatar__image']",
            "first_name": "//*[@id='firstNameInput']",
            "last_name": "//*[@id='lastNameInput']",
            "preferred_name": "//*[@id='preferredNameInput']",
            "sign_up_password": "//*[@id='passwordInput']",
            "email_next_button": "//*[@id='registerMailButton']",
            "name_next_button": "//*[@id='registerNameButton']",
            "preferred_next_button": "//*[@id='registerPrefNameButton']",
            "password_next_button": "//*[@id='registerPasswordButton']",
            "dob_next_button": "//*[@id='registerAgeButton']",
            "month_input": "//span[@id='month_register-date-of-birth']",
            "date_text": "//*[@text='%s']",
            "day_text": "//input[@id='dayInput']",
            "year_text": "//input[@id='yearInput']",
            "strike_a_pose": "//h1[text()='Strike a pose']",
            "skip_photo": "//*[@id='skipStrikePose']",
            "google_icon": "//a[@id='registerWithGoogle']",
            "google_choose_account_header": "//*[@text='Choose an account']",
            "select_google_account": "//*[@text='Test Signup']",
            "google_header": "//*[@text='Google']",
            'add_google_account_button': "//*[@text='Add another account']",
            "next_button": "android.widget.Button",
            "google_email_input": "//*[@text()='Email or phone']",
            "google_password_input": "password",
            "facebook_header": "//*[@content-desc='facebook']",
            "facebook_email_input": "//*[@resource-id='m_login_email']",
            "facebook_password_input": "//*[@resource-id='m_login_password']",
            "facebook_login_button": "//*[@text='Log In']",
            "signin_google_icon": "//a[@id='signInWithGoogle']",
            "facebook_icon": "//a[@id='registerWithFB']",
            "continue_login_fb": "//*[@text='Continue']",
            "go_to_settings_after_signup_fb": "//*[@class='VoyageUserAvatar']",
            "facebook_signin_icon": "//a[@id='signInWithFB']",
            'back_btn': "//*[@resource-id='back-btn']",
            "permission_skip": "//*[@text='Skip']"
        })

    def wait_till_first_screen(self):
        """
        To check the availability of first screen
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_screen, locator_type='xpath',
                                                      time_out=40)
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
        self.webDriver.click(element=self.locators.sign_in, locator_type='xpath')

    def open_signin_with_email(self):
        """
        Function to click on Sing in with Email
        :return:
        """
        self.webDriver.click(element=self.locators.sign_in_with_email, locator_type='xpath')

    def fill_signin_details(self, username, password):
        """
        To fill signin details
        :param username:
        :param password:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.set_text(element=self.locators.email_id, locator_type='xpath', text=username)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.password, locator_type='xpath',
                                                      time_out=40)
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.driver.hide_keyboard()
        self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.incorrect_creds_screen, locator_type='xpath'):
            self.webDriver.driver.hide_keyboard()
            self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
            self.webDriver.clear_text(element=self.locators.password, locator_type='xpath', action_type='action')
            self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text='Voyages@9899')
            self.webDriver.driver.hide_keyboard()
            self.webDriver.click(element=self.locators.login_mail_btn, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        if self.webDriver.is_element_display_on_screen(element=self.locators.popup_no, locator_type='xpath'):
            self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.popup_no, locator_type='xpath'):
                self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.allow_access,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access, locator_type='xpath'):
                self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')

    def open_signin_with_shipboard(self):
        """
        Function to click on Sign in with Shipboard
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.sign_in_with_shipboard, locator_type='xpath')

    def fill_shipboard_details(self, lastname, dob, cabin_number):
        """
        To fill sign in with shipboard details
        :param lastname:
        :param dob:
        :param cabin_number:
        :return:
        """
        split_dob = dob.split("-")
        year = split_dob[0]
        month_name = datetime.strptime(split_dob[1], "%m").strftime("%b")
        date = split_dob[2]
        self.webDriver.explicit_visibility_of_element(element=self.locators.lastname_shipboard, locator_type='xpath',
                                                      time_out=40)
        self.webDriver.set_text(element=self.locators.lastname_shipboard, locator_type='xpath', text=lastname)
        self.webDriver.set_text(element=self.locators.cabin_no_shipbaord, locator_type='xpath', text=cabin_number)
        self.webDriver.set_text(element=self.locators.year_dob_shipboard, locator_type='xpath', text=year)
        self.webDriver.set_text(element=self.locators.day_dob_shipboard, locator_type='xpath', text=date)
        self.webDriver.click(element=self.locators.month_dob_shipboard, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.month_index.format(month_name), locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.shipboard_login_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')

    def open_signup_page(self):
        """
        To open signup page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_up, locator_type='xpath')

    def open_signup_with_email(self):
        """
        To open signup woth email
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up_with_email, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.sign_up_with_email, locator_type='xpath')

    def fill_signup_details(self, guest_data, test_data):
        """
        Function to fill the details in signup flow
        :param guest_data:
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.email_id, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.email_id, locator_type='xpath', text=test_data['signup_email_id'])
        self.webDriver.click(element=self.locators.email_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.first_name, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.set_text(element=self.locators.first_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.set_text(element=self.locators.last_name, locator_type='xpath', text=guest_data[0]['LastName'])
        self.webDriver.click(element=self.locators.name_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.preferred_name, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.preferred_name, locator_type='xpath',
                                text=guest_data[0]['FirstName'])
        self.webDriver.click(element=self.locators.preferred_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_up_password, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.sign_up_password, locator_type='xpath', text="Yellow*99")
        self.webDriver.click(element=self.locators.password_next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.month_input, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.month_input, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'May', locator_type='xpath')
        date_s = guest_data[0]['birthDate'].split('-')[2]
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.set_text(element=self.locators.day_text, locator_type='xpath',
                                text=date_s)
        year_s = guest_data[0]['birthDate'].split('-')[0]
        self.webDriver.set_text(element=self.locators.year_text, locator_type='xpath',
                                text=year_s)
        self.webDriver.click(element=self.locators.dob_next_button, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.popup_no, locator_type='xpath'):
            self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.permission_skip, locator_type='xpath'):
            self.webDriver.click(element=self.locators.permission_skip, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.strike_a_pose, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.skip_photo, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')

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
        self.webDriver.explicit_visibility_of_element(element=self.locators.connect_booking_button, locator_type='xpath'
                                                      , time_out=30)
        if self.webDriver.is_element_display_on_screen(element=self.locators.book_voyage_button, locator_type='xpath'):
            logger.debug("Book voyage button is available on screen")
        else:
            raise Exception("Book voyage button is not available on screen")

    def go_to_settings_after_signup(self):
        """
        Function to go to settings after signup
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.connect_booking_button, locator_type='xpath'
                                                      , time_out=30)
        self.webDriver.click(element=self.locators.go_to_settings_after_signup_fb, locator_type='xpath')

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

    def signup_with_google(self, test_data):
        """
        Function to signup with google
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.google_choose_account_header,
                                                      locator_type='xpath', time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.select_google_account,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.select_google_account, locator_type='xpath')
            test_data['Google_ac_available'] = True
        else:
            test_data['Google_ac_available'] = False
            self.webDriver.mobile_native_back()
            self.webDriver.wait_for(2)
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.back_btn, locator_type='xpath')
            self.webDriver.click(element=self.locators.back_btn, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.back_btn, locator_type='xpath')
            return False
        
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.popup_no, locator_type='xpath'):
            self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')

    def open_signup_with_facebook(self):
        """
        Function to open signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.facebook_icon, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.facebook_icon, locator_type='xpath')

    def signup_with_facebook(self):
        """
        Function to signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.continue_login_fb,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.continue_login_fb, locator_type='xpath')
        else:
            self.webDriver.explicit_visibility_of_element(element=self.locators.facebook_header, locator_type='xpath'
                                                          , time_out=90)
            self.webDriver.clear_text(element=self.locators.facebook_email_input, locator_type='xpath', action_type='clear')
            self.webDriver.set_text(element=self.locators.facebook_email_input, locator_type='xpath',
                                    text='bjqldzcduh_1658997952@tfbnw.net')
            self.webDriver.clear_text(element=self.locators.facebook_password_input, locator_type='xpath', action_type='clear')
            self.webDriver.set_text(element=self.locators.facebook_password_input, locator_type='xpath',
                                    text='Yellow*99')
            self.webDriver.click(element=self.locators.facebook_login_button, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.facebook_login_button,
                                                                   locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.continue_login_fb,
                                                           locator_type='xpath'):
                self.webDriver.click(element=self.locators.continue_login_fb, locator_type='xpath')
        self.webDriver.wait_for(15)
        if self.webDriver.is_element_display_on_screen(element=self.locators.popup_no, locator_type='xpath'):
            self.webDriver.click(element=self.locators.popup_no, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')

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

    def open_signin_with_facebook(self):
        """
        Function to open signup with facebook
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.facebook_signin_icon, locator_type='xpath')