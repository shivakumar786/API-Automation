
from virgin_utils import *


class MociLogin:
    """
    Page Class For Login To moci App
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver
        """
        self.webDriver = web_driver
        self.locators = General.dict_to_ns({
            "login_logo": "//div[@class='login__form__inputs__form-control']",
            "username": "Username",
            "password": "Password",
            "login": "login",
            "invalid_error": "//div[contains(text(),'Invalid User name or Password')]",
            "logout_my_id": "//a[contains(text(),'Logout')]",
            "loader": "//div[@class='app-loader-wrap app-overlays']"
        })

    def verification_of_moci_login_page(self):
        """
        To check the availability of login page
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_logo, locator_type='xpath'):
            logger.debug("User is land on Login page of MOCI")
        else:
            raise Exception("User is not on Login page of MOCI")

    def login_into_moci(self, username, password):
        """
        To login into moci
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.username, locator_type='id', action_type='clear')
        self.webDriver.set_text(element=self.locators.username, locator_type='id', text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type='id', action_type='clear')
        self.webDriver.set_text(element=self.locators.password, locator_type='id', text=password)
        self.webDriver.click(element=self.locators.login, locator_type='id')

    def verification_of_invalid_user_login_error_toast(self):
        """
        To check the login error display after enter the invalid credentials
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=15)
        toast = self.webDriver.get_text(element=self.locators.invalid_error, locator_type='xpath')
        if toast != "Invalid User name or Password. Please verify and try again.":
            raise Exception("correct message is not display when username or password is wrong")

    def verification_of_moci_login_error_toast_with_guest(self):
        """
        To check the login error display after enter the invalid credentials
        """
        toast = self.webDriver.get_text(element=self.locators.invalid_error, locator_type='xpath')
        if toast != "Invalid User name or Password. Please verify and try again.":
            raise Exception("correct message is not display when username or password is wrong")

    def moci_logout_available(self):
        """
        Check the availability of Logout from my ID button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.logout_my_id, locator_type='xpath',
                                                      time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.logout_my_id, locator_type='xpath'):
            self.webDriver.allure_attach_jpeg('logout_successful')
            logger.debug("Crew get logout successfully")
        else:
            raise Exception("Crew is not logged-out from MOCI")
