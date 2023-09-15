_author_ = 'sudhansh.arora'

from virgin_utils import *


class Selection(General):
    """
    Page Class For Selecting venue in  delivery_manager
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of host page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "hamburger_menu": "(//*[@class='android.widget.Button'])[1]",
            "delivery_manager": "//*[@class='android.view.View']//*[@text='DELIVERY MANAGER']",
            "SE_Aquatic": "//*[@class='android.view.View']//*[@text='Ship Eats - Aquatic Club']",
            "SE_Athletic": "//*[@class='android.view.View']//*[@text='Ship Eats - Athletic Club']",
            "SE_Bell_Box": "//*[@class='android.view.View']//*[@index='3']",
            "SE_GT": "//*[@class='android.view.View']//*[@text='Ship Eats - Gym & Tonic']",
            "SE_RR": "//*[@class='android.view.View']//*[@text='Ship Eats - Richard's Rooftop']",
            "SE_Shake": "//*[@class='android.view.View']//*[@text='Ship Eats - Shake for Champagne']",
            "SE_Sun_club": "//*[@class='android.view.View']//*[@text='Ship Eats - Sun Club Bar']",
            "apply": "//*[@class='android.widget.Button']",
            "android_sidebar": "//*[@resource-id='AUTOTEST_sidebar_profile']",
            "verification":"//*[@resource-id='AUTOTEST_crewdashboard-itineraries-card3_button-button']",
            "location_popup": "//*[@text='While using the app']"
        })

    def select_athletic(self):
        """
        To open Venue
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_Athletic,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Athletic, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')

        else:
            raise Exception("Couldn't select this venue")

    def select_bell_box(self):
        """
        To open bell box Venue
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_Bell_Box, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.SE_Bell_Box, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.apply, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("nothing is selected")

    def select_GT(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_GT,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_GT, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_RR(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_RR,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_RR, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_shake(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_Shake,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Shake, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_sun_club(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_Sun_club,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Sun_club, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")

    def select_aquatic(self):
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivery_manager,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.SE_Aquatic,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.SE_Aquatic, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("Couldn't select this venue")