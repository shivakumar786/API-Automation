__author__ = 'vanshika.arora'

from virgin_utils import *


class Login(General):
    """
    Page Class for Support Queue Login page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h5[contains(text(),'Support Queue')]",
            "username": "//label[contains(text(),'User ID')]/following-sibling::div/input",
            "password": "//label[contains(text(),'Password')]/following-sibling::div/input",
            "remember_me": "//span[contains(text(),'Remember me')]",
            "login_button": "//span[contains(text(),'LOGIN')]",
            "invalid_login_toast": "//p[@id='component-error-text']"
        })

    def verification_of_login_page(self):
        """
        To check the availability of login page
        """
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "Support Queue":
            logger.debug("User is land on Login page of Support Queue")
        else:
            raise Exception("user is not on Login page of Support Queue")

    def login_into_support_queue(self, username, password):
        """
        To login into support queue
        :param username:
        :param password:
        """
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.remember_me, locator_type='xpath')
        self.webDriver.click(element=self.locators.login_button, locator_type='xpath')

    def verify_invalid_login_toast(self):
        """
        Function to verify invalid login toast
        :return:
        """
        toast = self.webDriver.get_text(element=self.locators.invalid_login_toast, locator_type='xpath')
        if toast == "Sorry, you are not authorized to access this app. Please contact your administrator.":
            logger.debug("correct error message is displayed when username or password is wrong")
        elif toast == "Incorrect Username or Password":
            logger.debug("correct error message is displayed when username or password is wrong")
        else:
            self.webDriver.allure_attach_jpeg('error_invalid_toast')
            raise Exception("correct message is not displayed when username or password is wrong")