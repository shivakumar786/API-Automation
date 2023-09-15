__author__ = 'prahlad.sharma'

from virgin_utils import *


class SupervisorLogin(General):
    """
    Page Class for Embarkation Supervisor Login page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h1[contains(text(),'EMBARKATION ADMIN')]",
            "username": "//input[@name='username']",
            "password": "//input[@name='password']",
            "remember_me": "//label[contains(text(),'Remember Me')]",
            "login_button": "//button[contains(text(),'LOGIN')]",
            "invalid_login_toast": "//div[@class='notification is-danger']"
        })

    def verification_of_login_page(self):
        """
        To check the availability of login page
        """
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "EMBARKATION ADMIN":
            logger.debug("User is land on Login page of Embarkation Supervisor")
        else:
            raise Exception("user is not on Login page of Embarkation Supervisor")

    def login_into_embarkation_supervisor(self, username, password):
        """
        To login into Embarkation Supervisor
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.username, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.remember_me, locator_type='xpath')
        self.webDriver.click(element=self.locators.login_button, locator_type='xpath')

    def verification_of_invalid_login_toast(self):
        """
        To check the availability of login page
        """
        screen_title = self.webDriver.get_text(element=self.locators.invalid_login_toast, locator_type='xpath')
        if screen_title == "Username or password is wrong":
            self.webDriver.allure_attach_jpeg('invalid_toast')
            logger.debug("correct message is display when username or password is wrong")
        else:
            self.webDriver.allure_attach_jpeg('error_invalid_toast')
            raise Exception("correct message is not display when username or password is wrong")
