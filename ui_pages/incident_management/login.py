__author__ = 'prahlad.sharma'

from virgin_utils import *


class Login(General):
    """
    page class for login to Incident Management web application
    """

    def __init__(self, web_driver):
        """
        initiate locators
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "login_page": "//*[text()='Incident Management (Admin)']",
            "username": "username",
            "password": "password",
            "login_btn": "//*[text()='Login']"
        })

    def verify_login_page(self):
        """
        verify Incident Management login page
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.login_page, locator_type="xpath")

    def login_into_incident_management_web_app(self, user_name, password):
        """
        login to ars application
        :params: user_name:
        :params: password:
        """
        self.webDriver.set_text(element=self.locators.username, locator_type='name', text=user_name)
        self.webDriver.set_text(element=self.locators.password, locator_type='name', text=password)
        self.webDriver.click(element=self.locators.login_btn, locator_type="xpath")