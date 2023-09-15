__author__ = 'saloni.pattnaik'

from virgin_utils import *


class PushNotificationLogin(General):
    """
    Page Class for Push Notification Login page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Login page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h5[contains(text(),'Push Notifications')]",
            "username": "//input[@id='filled-basic-username']",
            "password": "//input[@id='filled-basic-password']",
            "remember_me": "//span[@class='MuiIconButton-label']",
            "login_button": "//span[contains(text(),'SIGN IN')]",
            "dashboard": "//h6[contains(text(),'Push Notifications')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
        })

    def verification_of_login_page(self):
        """
        To check the availability of login page
        """
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "Push Notifications":
            logger.debug("User is land on Login page of Push Notification")
        else:
            raise Exception("user is not on Login page of Push Notification")

    def login_into_push_notification(self, username, password):
        """
        To login into Push Notification
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.username, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.remember_me, locator_type='xpath')
        self.webDriver.click(element=self.locators.login_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        return self.webDriver.is_element_display_on_screen(element=self.locators.dashboard, locator_type='xpath')

