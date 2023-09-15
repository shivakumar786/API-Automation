__author__ = 'HT'

from virgin_utils import *


class VenueManagerLogin(General):
    """
    Page Class for Venue Manager Login page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "login_page_header": "//*[text()='Venue Manager']",
            "user_id": "userName",
            "password": "passWord",
            "login_button": "btn-login",
            "error_message": "//*[text()='Invalid username or password']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "login_remember": "//*[text()=' Remember me ']"
        })

    def verify_login_page_header(self):
        """
        Get venue manager login page header
        """
        return self.webDriver.get_text(element=self.locators.login_page_header, locator_type='xpath')

    def verify_with_invalid_login(self, username):
        """
        Verify with invalid login user using sailor credential
        """
        self.webDriver.clear_text(element=self.locators.user_id, locator_type="id", action_type="clear")
        self.webDriver.set_text(element=self.locators.user_id, locator_type="id", text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type="id", action_type="clear")
        self.webDriver.set_text(element=self.locators.password, locator_type="id", text="Voyages@9876")
        self.webDriver.click(element=self.locators.login_button, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def get_error_message(self):
        """
        get error message after invalid login user
        """
        return self.webDriver.get_text(element=self.locators.error_message, locator_type="xpath")

    def verify_with_valid_login(self, username, password):
        """
        Verify with invalid login user using sailor credential
        """
        self.webDriver.clear_text(element=self.locators.user_id, locator_type="id", action_type="clear")
        self.webDriver.set_text(element=self.locators.user_id, locator_type="id", text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type="id", action_type="clear")
        self.webDriver.set_text(element=self.locators.password, locator_type="id", text=password)
        self.webDriver.click(element=self.locators.login_button, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=120)

    def verify_user_name_and_password_after_logout(self):
        """
        To verify user is able to see saved username and password after logout
        :return:
        """
        self.webDriver.click(element=self.locators.login_remember, locator_type="xpath")
        status = self.webDriver.is_element_enabled(element=self.locators.login_remember, locator_type="xpath")
        if not status:
            raise Exception("remember me element on login page is disabled")

