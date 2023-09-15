__author__ = 'sudhansh.arora'

from virgin_utils import *


class SelectVenue(General):
    """
    Page Class For Selecting venue in  Server
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of host page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "hamburger_menu": "//*[contains(@resource-id, 'hamburger-button')]",
            "server": "//*[@resource-id='AUTOTEST__sidebar__simple__Server']//*[@text='SERVER']",
            "SE_Aquatic": "//*[@class='android.view.View']//*[@text='Ship Eats - Aquatic Club']",
            "SE_Athletic": "//*[@class='android.view.View']//*[@text='Ship Eats - Athletic Club']",
            "SE_Bell_Box": "//*[@class='android.view.View']//*[@index='3']",
            "SE_GT": "//*[@class='android.view.View']//*[@text='Ship Eats - Gym & Tonic']",
            "SE_RR": "//*[@class='android.view.View']//*[@text='Ship Eats - Richard's Rooftop']",
            "SE_Shake": "//*[@class='android.view.View']//*[@text='Ship Eats - Shake for Champagne']",
            "SE_Sun_club": "//*[@class='android.view.View']//*[@text='Ship Eats - Sun Club Bar']",
            "apply": "//*[@class='android.widget.Button']",
            "android_sidebar": "//*[@resource-id='AUTOTEST__sidebar__profile']",
            "verification":"//*[@resource-id='AUTOTEST__crew__dashboard-itineraries-card__3__button-button']",
            "location_popup": "//*[@text='While using the app']"
        })

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath'):
            return True
        else:
            raise Exception("Something Wrong Happend")


    def select_server(self):
        """
        To open Server module
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath'):
            self.webDriver.click(element=self.locators.server, locator_type='xpath')
            self.webDriver.wait_for(20)
        else:
            raise Exception("couldn't select server")

    def select_athletic(self):
        """
        To open Venue
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Athletic, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')

        else:
            raise Exception("Couldn't select this venue")

    def select_bell_box(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        self.webDriver.is_element_display_on_screen(element=self.locators.SE_Bell_Box, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.location_popup, locator_type='xpath'):
            self.webDriver.click(element=self.locators.location_popup, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_GT(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_GT, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_RR(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_RR, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_shake(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Shake, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_sun_club(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Sun_club, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_aquatic(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.wait_for(10)
        self.webDriver.is_element_display_on_screen(element=self.locators.android_sidebar, locator_type='xpath')
        self.webDriver.click(element=self.locators.server, locator_type='xpath')
        self.webDriver.wait_for(20)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Aquatic, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def click_logout(self):
        """
        To click on logout button
        :return:
        """
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.click(element=self.locators.click_logout, locator_type='xpath')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')

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