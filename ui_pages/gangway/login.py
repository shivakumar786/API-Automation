__author__ = 'prahlad.sharma'

from virgin_utils import *


class Login(General):
    """
    Page class for Login page of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        self.locators = self.dict_to_ns({
            "loader": "//*[@text='loading...']",
            "user_name": "//*[@text='Username']/../following-sibling::*[@class='android.widget.EditText']",
            "password": "//*[@text='Password']/../following-sibling::*[@class='android.widget.EditText']",
            "sign_in": "//*[@text='SIGN IN']",
            "login_error": "com.decurtis.dxp.gangway:id/error",
            "setting_up_data": "//*[@text='Setting up the data']",
            "progress_bar": "//*[@id='progress_bg']",
            "progress": "//*[@resource-id='com.decurtis.dxp.gangway:id/progress']",
            "progress_bar_horizontal": "//*[@resource-id='com.decurtis.dxp.gangway:id/progress_horizontal']",
            "change_ship": "//*[@text='CHANGE SHIP']",
            "next_button": "//*[@text='NEXT']",
            "all_ships": "com.decurtis.dxp.gangway:id/ship_image",
            "connect_button": "com.decurtis.dxp.gangway:id/connect",
            "select_ship_available": "com.decurtis.dxp.gangway:id/label_select_location",
            "spinner": "com.decurtis.dxp.gangway:id/progress",
            "invalid_login_toast": "com.decurtis.dxp.gangway:id/error",
            "ship_name": "com.decurtis.dxp.gangway:id/ship_name"
        })

    def check_availability_of_login_page(self):
        """
        Availability of login page
        """
        self.webDriver.wait_for(5)
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_in, locator_type='xpath',
                                                      time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.sign_in, locator_type='xpath')

    def sign_in(self, username, password):
        """
        Function to sing in into gangway
        :param username:
        :param password:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.user_name, locator_type='xpath', time_out= 120)
        self.webDriver.clear_text(element=self.locators.user_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.user_name, locator_type='xpath', text=username)
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.sign_in, locator_type='xpath')
        self.webDriver.wait_for(10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_error, locator_type='id'):
            raise Exception(f"Gangway login is not working with username:{username} and password :{password}")
        else:
            self.webDriver.explicit_invisibility_of_element(element=self.locators.setting_up_data,
                                                            locator_type='xpath',
                                                            time_out=2000)

    def invalid_sign_in(self, username, password):
        """
        Function to sing in into gangway
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.user_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.user_name, locator_type='xpath', text=username)
        self.webDriver.clear_text(element=self.locators.password, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.sign_in, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.setting_up_data,
                                                        locator_type='xpath',
                                                        time_out=1000)

    def verification_of_invalid_login_toast(self):
        """
        to verify invalid login toast
        :return:
        """
        screen_title = self.webDriver.get_text(element=self.locators.invalid_login_toast, locator_type='id')
        if screen_title == "Incorrect Username or Password.":
            self.webDriver.allure_attach_jpeg('invalid_toast')
            logger.debug("correct message is display when username or password is wrong")
        else:
            self.webDriver.allure_attach_jpeg('error_invalid_toast')
            raise Exception("correct message is not display when username or password is wrong")

    def verification_of_error_message_to_enter_username_or_password(self):
        """
        TO verify error message to enter username or password
        :return:
        """
        screen_title = self.webDriver.get_text(element=self.locators.invalid_login_toast, locator_type='id')
        if screen_title == "Please enter Username and Password.":
            self.webDriver.allure_attach_jpeg('verification_of_error_message_to_enter_username_or_password')
            logger.debug("correct message is displayed when only username or password is entered")
        else:
            self.webDriver.allure_attach_jpeg('verification_of_error_message_to_enter_username_or_password')
            raise Exception("correct message is not displayed when only username or password is entered")

    def select_ship(self, ship_name):
        """
        To select the Ship from Ship Page
        :param ship_name:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.all_ships, locator_type='id',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.select_ship_available, locator_type='id'):
            all_ships = self.webDriver.get_elements(element=self.locators.ship_name, locator_type='id')
            for ship in all_ships:
                if ship.text == ship_name or ship.text == 'Dream':
                    ship.click()
                    break
            self.webDriver.allure_attach_jpeg('select_ship')
            self.webDriver.click(element=self.locators.connect_button, locator_type='id')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                            time_out=30)
        else:
            raise Exception("Select ship page is not available")
