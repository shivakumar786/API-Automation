__author__ = 'saloni.pattnaik'

from virgin_utils import *


class CrewAppLogin(General):
    """
    Page Class For Login To Table Management
    """
    def __init__(self, web_driver):
        """
        To Initialize the locators of login page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "calls_popup": "//*[@text='Allow']",
            "record_audio_popup": "//*[@text='While using the app']",
            "next_button": "//*[@text='Next']",
            "login_logo": "//*[@class='android.widget.Image']",
            "username": "//*[@class='android.widget.EditText']",
            "password": "//*[@class='android.widget.EditText']",
            "create_pin": "//*[@text='Create PIN']",
            "enter_pin": "//*[@resource-id='KeyboardKey-1']",
            "enter_button": "//*[@resource-id='KeyboardKey-ENTER']",
            "dashboard_header": "//*[@text='Dashboard']",
            "hamburger_menu": "//*[@resource-id='android:id/content']//*[@class='android.widget.Button']",
            "modules": "(//*[@resource-id='android:id/content']//*["
                       "@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*["
                       "@class='android.view.View'])[2]//*[@class='android.view.View']",
            "click_tm": "//*[@resource-id='android:id/content']//*["
                        "@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']",
            "click_logout": "//*[@class='android.view.View']//*[@text='Logout']",
            "logout": "//*[@text='LOGOUT']",
            "hamburger_menu_icon": "//*[@resource-id='button-main-menu']",
            "error_message": "//*[@class='android.widget.Image']/following-sibling::android.view.View/android.view.View[2]",
            "invalid_error_message": "//*[contains(@text,'Invalid credentials')]",
        })

    def verify_logout(self):
        """
        To verify logged out from table management application
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_logo, locator_type='xpath'):
            logo = self.webDriver.get_text(element=self.locators.login_logo, locator_type='xpath')
            if logo == "vv":
                return True
            else:
                return False

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')

    def verify_crew_dashboard(self):
        """
        Function to verify crew app dashboard
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.dashboard_header, locator_type="xpath",
                                                      time_out=120)
        dashboard_header = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_header,
                                                                       locator_type="xpath")
        if not dashboard_header:
            raise Exception("Not successfully landed on crew dashboard")

    def click_logout(self):
        """
        To click on logout button
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.click_logout, locator_type='xpath'):
            self.webDriver.click(element=self.locators.click_logout, locator_type='xpath')
        else:
            self.webDriver.scroll_mobile(534, 1514, 459, 155)
            self.webDriver.scroll_mobile(534, 1514, 459, 155)
            self.webDriver.click(element=self.locators.click_logout, locator_type='xpath')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')

    def open_table_management(self):
        """
        To open table management application
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        if len(self.webDriver.get_elements(element=self.locators.modules, locator_type='xpath')) != 4:
            return False
        else:
            return True

    def allow_call_popup(self):
        """
        To allow the calls pop-up
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.calls_popup, locator_type='xpath',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.calls_popup, locator_type='xpath'):
            self.webDriver.click(element=self.locators.calls_popup, locator_type='xpath')
            try:
                self.webDriver.get_web_element(element=self.locators.calls_popup, locator_type='xpath').click()
            except (Exception, ValueError):
                self.webDriver.get_web_element(element=self.locators.record_audio_popup, locator_type='xpath').click()
        else:
            logger.info('Allow Calls pop up not displayed')

    def verify_select_ship(self):
        """
        To verify select ship option
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.login_logo, locator_type='xpath',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.login_logo, locator_type='xpath'):
            logo = self.webDriver.get_text(element=self.locators.login_logo, locator_type='xpath')
            if logo == "vv":
                self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.username, locator_type='xpath',
                                                              time_out=120)
                return True
            else:
                return False

    def sign_in(self, username, password):
        """
        To sign in into the TM application
        :param username:
        :param password:
        """
        self.webDriver.clear_text(element=self.locators.username, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.submit()
        self.webDriver.explicit_visibility_of_element(element=self.locators.password, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.clear_text(element=self.locators.password, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.submit()

    def verify_create_pin_page(self):
        """
        To verify user land on create pin page
        :return:
        """
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.create_pin, locator_type='xpath'):
            for pins in range(1, 3):
                for pin in range(0, 4):
                    self.webDriver.click(element=self.locators.enter_pin, locator_type='xpath')
                    pin += 1
                self.webDriver.click(element=self.locators.enter_button, locator_type='xpath')
                pins += 1
            return True
        else:
            return False

    def verify_invalid_login(self, username, password):
        """
        Function to login crew app with invalid user credential
        :param username:
        :param password:
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.username, locator_type='xpath'):
            self.webDriver.explicit_visibility_of_element(element=self.locators.username, locator_type='xpath',
                                                          time_out=120)
        self.webDriver.set_text(element=self.locators.username, locator_type='xpath', text=username)
        self.webDriver.submit()
        self.webDriver.explicit_visibility_of_element(element=self.locators.password, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.set_text(element=self.locators.password, locator_type='xpath', text=password)
        self.webDriver.submit()
        if self.webDriver.is_element_display_on_screen(element=self.locators.error_message, locator_type="xpath"):
            error_message = self.webDriver.is_element_display_on_screen(element=self.locators.error_message,
                                                                        locator_type="xpath")
        else:
            error_message = self.webDriver.is_element_display_on_screen(element=self.locators.invalid_error_message,
                                                                        locator_type="xpath")
        assert error_message, "Error message not displayed while login with sailor credential"

    def wait_for_select_ship_page(self):
        """
        Function to wait for select ship page and click on next button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.next_button, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.username, locator_type='xpath',
                                                      time_out=60)