__author__ = 'saloni.pattnaik'

from virgin_utils import *
from selenium.webdriver.support.ui import Select


class BookVoyageSignIn(General):
    """
    Page Class for Book Voyage Sign in page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of sign in page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h1[contains(text(),'SIGN IN')]",
            "username": "//input[@name='email']",
            "password": "//input[@name='password']",
            "keep_me_logged_in": "SignIn_keepLoggedIn",
            "sign_in_button": "//button[@type='submit']",
            "signup": "//a[text()=' Sign Up']",
            "signup_with_email": "//button[text()='Sign up with Email']",
            "signup_header_title": "//*[text()=' SIGN UP']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "//input[@type='email']",
            "sailor_password": "password",
            "month": "//select[@aria-label=' Select Month']",
            "day": "//select[@aria-label=' Select Day']",
            "year": "//select[@aria-label=' Select Year']",
            "signup_button": "//button[text()='Sign up with Email']",
        })

    def sign_in(self, guest_data):
        """
        To verify sign in functionality
        :param guest_data:
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.username, locator_type='xpath')
        self.webDriver.click(element=self.locators.username, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=guest_data[0]['Email'])
        self.webDriver.click(element=self.locators.password, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text='Yellow*99')
        self.webDriver.click(element=self.locators.sign_in_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def signup_of_sailor(self, guest_data, count):
        """
        To enter all sailor information in required fields for signup
        :param guest_data:
        :return:
        """
        self.webDriver.set_text(element=self.locators.firstname, locator_type='id', text=guest_data[count]['FirstName'])
        self.webDriver.set_text(element=self.locators.lastname, locator_type='id', text=guest_data[count]['LastName'])
        self.webDriver.set_text(element=self.locators.email, locator_type='xpath', text=guest_data[count]['Email'])
        self.webDriver.set_text(element=self.locators.sailor_password, locator_type='id', text='Yellow*99')
        month = Select(self.webDriver.get_web_element(element=self.locators.month, locator_type='xpath'))
        day = Select(self.webDriver.get_web_element(element=self.locators.day, locator_type='xpath'))
        year = Select(self.webDriver.get_web_element(element=self.locators.year, locator_type='xpath'))
        month.select_by_index(random.randint(1, 11))
        day.select_by_index(random.randint(1, 29))
        year.select_by_index(random.randint(9, 20))
        self.webDriver.scroll(0, 1500)
        self.webDriver.click(element=self.locators.signup_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verification_of_signin_page(self):
        """
        To check the availability of sign in page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "SIGN IN":
            logger.debug("User is land on SignIn page of Book Voyage")
        else:
            raise Exception("user is not on SignIn page of Book Voyage")

    def click_signup_with_email(self):
        """
        To click signup with email button
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.signup, locator_type='xpath')
        self.webDriver.click(element=self.locators.signup_with_email, locator_type='xpath')

    def verification_of_signup_page(self):
        """
        To verify availability of signup page
        :return:
        """
        screen_title = self.webDriver.get_text(element=self.locators.signup_header_title, locator_type='xpath')
        if screen_title == "SIGN UP":
            logger.debug("User is land on SignUn page of Book Voyage")
        else:
            raise Exception("user is not on SignUn page of Book Voyage")
