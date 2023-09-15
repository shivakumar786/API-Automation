__author__ = 'sarvesh.singh'

from virgin_utils import *


class Login(General):
    """
    Page class for Login page of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "loader": "//*[@text='loading...']",
                "user_name": "//*[@text='Username']/../following-sibling::*[@class='android.widget.EditText']",
                "password": "//*[@text='Password']/../following-sibling::*[@class='android.widget.EditText']",
                "sign_in": "//*[@text='SIGN IN']",
                "login_error": "com.decurtis.dxp.aci:id/error",
                "setting_up_data": "//*[@text='Setting up the data']",
                "progress_bar": "//*[@id='progress_bg']",
                "progress": "//*[@resource-id='com.decurtis.dxp.aci:id/progress']",
                "progress_bar_horizontal": "//*[@resource-id='com.decurtis.dxp.aci:id/progress_horizontal']",
                "change_ship": "//*[@text='CHANGE SHIP']",
                "next_button": "//*[@text='NEXT']",
                "connect": "com.decurtis.dxp.aci:id/connect",
                "ok_button": "android:id/button1",
                "all_ships": "com.decurtis.dxp.aci:id/ship_image",
                "select_ship_available": "com.decurtis.dxp.aci:id/label_select_location",
                "ship_name": "com.decurtis.dxp.aci:id/ship_name",
                "connect_button": "com.decurtis.dxp.aci:id/connect",
                "spinner": "com.decurtis.dxp.aci:id/progress"
            })
        else:
            self.locators = self.dict_to_ns({
                "loader": "//*[@text='loading...']",
                "user_name": "//*[@text='Username']/../following-sibling::*[@class='android.widget.EditText']",
                "password": "//*[@text='Password']/../following-sibling::*[@class='android.widget.EditText']",
                "sign_in": "//*[@text='SIGN IN']",
                "login_error": "com.decurtis.dxp.aci:id/error",
                "setting_up_data": "//*[@text='Setting up the data']",
                "progress_bar": "//*[@id='progress_bg']",
                "progress": "//*[@resource-id='com.decurtis.dxp.aci:id/progress']",
                "progress_bar_horizontal": "//*[@resource-id='com.decurtis.dxp.aci:id/progress_horizontal']",
                "change_ship": "//*[@text='CHANGE SHIP']",
                "next_button": "//*[@text='NEXT']",
                "select_ship": "com.decurtis.dxp.aci.dclnp:id/ship_name",
                "connect": "com.decurtis.dxp.aci.dclnp:id/connect",
                "ok_button": "android:id/button1",
                "all_ships": "com.decurtis.dxp.aci.dclnp:id/ship_image",
                "select_ship_available": "com.decurtis.dxp.aci.dclnp:id/label_select_location",
                "ship_name": "com.decurtis.dxp.aci.dclnp:id/ship_name",
                "connect_button": "com.decurtis.dxp.aci.dclnp:id/connect",
                "spinner": "com.decurtis.dxp.aci.dclnp:id/progress"
            })

    def check_availability_of_login_page(self):
        """
        Availability of login page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sign_in, locator_type='xpath',
                                                      time_out=30)
        return self.webDriver.is_element_display_on_screen(element=self.locators.sign_in, locator_type='xpath')

    def sign_in(self, username, password):
        """
        Function to sign in into aci
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.user_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.user_name, locator_type='xpath', text=username)
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.click(element=self.locators.sign_in, locator_type='xpath')
        self.webDriver.wait_for(10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_error, locator_type='id'):
            raise Exception(f"ACI login is not working with username:{username} and password :{password}")
        else:
            self.webDriver.explicit_invisibility_of_element(element=self.locators.setting_up_data,
                                                            locator_type='xpath',
                                                            time_out=2000)
            self.webDriver.wait_for(20)

    def select_ship_name(self, ship_name):
        """
        Function to select the ship
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.select_ship_available, locator_type='id'):
            all_ships = self.webDriver.get_elements(element=self.locators.ship_name, locator_type='id')
            for ship in all_ships:
                if ship.text == ship_name:
                    ship.click()
                    break
            self.webDriver.allure_attach_jpeg('select_ship')
            self.webDriver.click(element=self.locators.connect_button, locator_type='id')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                            time_out=30)
        else:
            raise Exception("Select ship page is not available")
