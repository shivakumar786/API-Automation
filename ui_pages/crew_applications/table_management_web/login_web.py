__author__ = 'bhanu.pratap'

from virgin_utils import *
from selenium.webdriver.common.keys import Keys

class TableManagementShipLogin(General):
    """
    Page Class For Login To Table Management Web
    """
    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "login_logo": "//*[@src='/tableui/images/logo.VV.svg']",
            "username": "//input[@id='input-auth-email__input']",
            "password": "//input[@id='input-auth-password__input']",
            "click_logout": "//span[contains(text(),'Logout')]",
            "Upcoming": "//span[contains(text(),'Upcoming')]"
        })

    def verification_of_login_page(self):
        """
        To check the availability of login page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.login_logo, locator_type='xpath',
                                                      time_out=60)
        screen_status = self.webDriver.is_element_display_on_screen(element=self.locators.login_logo, locator_type="xpath")
        assert screen_status, "VV logo is not displayed on login screen"


    def login_into_table_management(self, username, password):
        """
        To login into table management ship
        :param username:
        :param password:
        """
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.key_chains().send_keys(Keys.ENTER).perform()
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.key_chains().send_keys(Keys.ENTER).perform()
        self.webDriver.wait_for(5)

    def verify_table_management_dashboard(self):
        """
        To verify successful login into table management ship
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.Upcoming, locator_type='xpath',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.Upcoming, locator_type='xpath'):
            text = self.webDriver.get_text(element=self.locators.Upcoming, locator_type='xpath')
            if text == "Upcoming":
                return True
            else:
                return False

    def click_logout(self):
        """
        To click on logout button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.click_logout, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.click_logout, locator_type='xpath')

    def verify_logout(self):
        """
        To verify logged out from table management application
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.login_logo, locator_type='xpath',
                                                      time_out=60)
        screen_status = self.webDriver.is_element_display_on_screen(element=self.locators.login_logo,
                                                                    locator_type="xpath")
        assert screen_status, "VV logo is not displayed on logout screen"