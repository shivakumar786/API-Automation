__author__ = 'Krishna'

from virgin_utils import *


class Login(General):
    """
    page class for login to ars admin web application
    """

    def __init__(self, web_driver):
        """
        initiate locators
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "login_page": "//*[text()='ARS Crew']",
            "username": "username",
            "password": "password",
            "login_btn": "//*[text()='LOGIN']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "vv_logo": "//*[@src='/activityReservationCrew/static/media/vv-Logo.f4d2d1ca.svg']"
        })

    def verify_ars_login_page(self):
        """
        verify ars login page
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.login_page, locator_type="xpath")

    def verify_vv_logo_is_displayed_on_login_screen(self):
        """
        To verify vv logo on login screen
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.vv_logo, locator_type='xpath', time_out=120)
        status = self.webDriver.is_element_display_on_screen(element=self.locators.vv_logo, locator_type="xpath")
        assert status, "VV logo is not displayed on login screen"

    def login_into_ars_admin_web_app(self, user_name, password):
        """
        login to ars application
        :params: user_name:
        :params: password:
        """
        self.webDriver.set_text(element=self.locators.username, locator_type='name', text=user_name)
        self.webDriver.set_text(element=self.locators.password, locator_type='name', text=password)
        self.webDriver.click(element=self.locators.login_btn, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)