__author__ = 'HT'

from virgin_utils import *


class CrewDashboard(General):
    """
    Page Class For crew dashboard
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of crew dashboard
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "calls_popup": "//*[@text='Allow']",
            "record_audio_popup": "//*[@text='While Using The App']",
            "on_duty_toggle": "com.decurtis.crew.embark:id/action_bar_root",
            "dashboard_header": "//*[@text='Dashboard']",
            "ahoy_crew_name": "//*[contains(@text,'AHOY!')]",
            "hamburger_menu": "//*[contains(@resource-id, 'hamburger-button')]",
            "line_up": "//*[@text='LINE UP']",
            "spaces": "//*[contains(@text,'Spaces')]",
            "view_venues": "//*[@text='VIEW VENUES']",
            "next_button": "//*[@text='Next']",
            "sailor_faq": "//*[@text='Sailor FAQ']",
            "help_center": "//*[@text='Help Center']",
            "sailor_faq_header": "//*[@text='Sailor’s FAQ']",
            "circles": "//*[@text='Circles']",
            "back_button": "//*[@resource-id='AUTOTEST__inquiries__backbutton']",
            "sailor_pin_reset": "//*[@text='SAILOR PIN RESET']",
            "pin_reset_header": "//*[@text='Sailor PIN Reset']",
            "search_sailor_icon": "(//*[@class='android.widget.Image'])[1]",
            "search_sailor_cabin": "//*[@class='android.widget.EditText']",
            "select_sailor": "//*[@text='%s']",
            "click_on_sailor_pin_reset": "//*[@text='RESET SAILOR PIN']",
            "change_my_pin_cta": "//*[@text='CHANGE MY PIN']",
            "enter_pin": "//*[@resource-id='KeyboardKey-1']",
            "enter_next_btn": "//*[@resource-id='KeyboardKey-ENTER']",
            "enter_confirm_pin": "//android.view.View[@content-desc='Sailor FAQ']/android.view.View",
            "click_logout": "//*[@class='android.view.View']//*[@text='Logout']",
            "logout": "//*[@text='LOGOUT']",
            "scroll_to_table_management": "//*[@text='TABLE MANAGEMENT']",
            "sync_in_progress_dashboard": "//*[@text='Sync In Progress']",
            "syn_in_progress_reset_pin": "//*[@text='Sync in Progress']",
            "settings": "//*[@text='Settings']",
            "near_by": "//*[@text='Nearby']",
            "nearby_toggle": "//*[@class='android.widget.Image']",
            "settings_back_btn": "//*[@resource-id='BackButton']",
            "dashboard_module": "//*[contains(@text,'%s')]",
            "pin_reset_success": "//*[contains(@text,'Success')]",
            "login_logo": "//*[@class='android.widget.Image']",
            "username": "//*[@class='android.widget.EditText']",
            "module_header": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "open_greeter_module": "//*[contains(@text,'ARS Greeter')]"
        })

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')

    def open_crew_app_module(self, module_name, module_heading):
        """
        To open Crew App Module from Hamburger Menu and also verify Module Header
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % module_name,
                                                           locator_type="xpath"):
            for i in range(10):
                self.webDriver.scroll_mobile(534, 1514, 459, 155)
                if self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % module_name,
                                                               locator_type="xpath"):
                    self.webDriver.click(element=self.locators.dashboard_module % module_name, locator_type='xpath')
                    break
                else:
                    raise Exception('Crew App Module not found in Hamburger Menu')
        else:
            self.webDriver.click(element=self.locators.dashboard_module % module_name, locator_type='xpath')
        self.webDriver.wait_for(10)
        if module_name != "GREETER":
            self.webDriver.explicit_visibility_of_element(element=self.locators.module_header % module_heading,
                                                          locator_type="xpath", time_out=120)
            logger.debug('Crew App Module from Hamburger Menu opened successfully')

    def verify_dashboard_ui_elements(self):
        """
        Function to verify the UI elements of crew dashboard
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.dashboard_header, locator_type="xpath",
                                                      time_out=120)
        dashboard_header = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_header,
                                                                       locator_type="xpath")
        if not dashboard_header:
            raise Exception("Not successfully landed on crew dashboard")

        toggle_button = self.webDriver.is_element_display_on_screen(element=self.locators.on_duty_toggle,
                                                                    locator_type="id")
        if not toggle_button:
            raise Exception("Toggle Button is not displayed on crew app dashboard")

        self.webDriver.explicit_visibility_of_element(element=self.locators.ahoy_crew_name, locator_type="xpath",
                                                      time_out=120)

        ahoy_crew_name = self.webDriver.is_element_display_on_screen(element=self.locators.ahoy_crew_name,
                                                                     locator_type="xpath")
        if not ahoy_crew_name:
            raise Exception("Ahoy! crew name is not displayed on crew app dashboard")

        line_up = self.webDriver.is_element_display_on_screen(element=self.locators.line_up,
                                                              locator_type="xpath")
        if not line_up:
            raise Exception("Line Up is not displayed on crew app dashboard")

        self.webDriver.scroll_mobile(x_press=0, y_press=2030, x_move=879, y_move=0)
        spaces = self.webDriver.is_element_display_on_screen(element=self.locators.spaces,
                                                             locator_type="xpath")
        if not spaces:
            raise Exception("Spaces is not displayed on crew app dashboard")

        view_venues = self.webDriver.is_element_display_on_screen(element=self.locators.view_venues,
                                                                  locator_type="xpath")
        if not view_venues:
            raise Exception("view venues is not displayed on crew app dashboard")
        self.webDriver.move_to_element(element=self.locators.sailor_faq, locator_type="xpath")

        sailor_faq = self.webDriver.is_element_display_on_screen(element=self.locators.sailor_faq, locator_type="xpath")
        if not sailor_faq:
            raise Exception("Sailor faq is not displayed on crew app dashboard")
        help_center = self.webDriver.is_element_display_on_screen(element=self.locators.help_center,
                                                                  locator_type="xpath")
        if not help_center:
            raise Exception("Help center is not displayed on crew app dashboard")

    def open_and_verify_frequently_asked_questions(self):
        """
        Function to verify frequently asked questions
        :return:
        """
        self.webDriver.click(element=self.locators.sailor_faq, locator_type="xpath")
        faq_header = self.webDriver.is_element_display_on_screen(element=self.locators.sailor_faq_header,
                                                                 locator_type="xpath")
        assert faq_header, "Failed to open faq page"
        self.webDriver.click(element=self.locators.circles, locator_type="xpath")
        circle_header = self.webDriver.is_element_display_on_screen(element=self.locators.circles,
                                                                    locator_type="xpath")
        assert circle_header, "Failed to load circle header"
        self.webDriver.click(element=self.locators.back_button, locator_type="xpath")
        self.webDriver.click(element=self.locators.back_button, locator_type="xpath")

        self.webDriver.click(element=self.locators.help_center, locator_type="xpath")
        help_center_header = self.webDriver.is_element_display_on_screen(element=self.locators.help_center,
                                                                         locator_type="xpath")
        assert help_center_header, "Failed to open help center from crew dashboard"

    def verify_create_pin_page(self):
        """
        To verify user land on create pin page
        :return:
        """
        for pin in range(0, 4):
            self.webDriver.click(element=self.locators.enter_pin, locator_type='xpath')

    def reset_sailor_pin(self, sailor_name, cabin_number):
        """
        Function to reset sailor pin
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type="xpath")
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.click(element=self.locators.sailor_pin_reset, locator_type="xpath")
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.record_audio_popup, locator_type="xpath"):
            self.webDriver.click(element=self.locators.record_audio_popup, locator_type="xpath")
        reset_pin_header = self.webDriver.is_element_display_on_screen(element=self.locators.pin_reset_header,
                                                                       locator_type="xpath")
        assert reset_pin_header, "failed to verify sailor pin reset header"
        if self.webDriver.is_element_display_on_screen(element=self.locators.syn_in_progress_reset_pin,
                                                       locator_type="xpath"):
            self.webDriver.explicit_invisibility_of_element(element=self.locators.syn_in_progress_reset_pin,
                                                            locator_type="xpath", time_out=300)
        self.webDriver.click(element=self.locators.search_sailor_icon, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.search_sailor_cabin, locator_type="xpath", text=cabin_number)
        self.webDriver.click(element=self.locators.select_sailor % sailor_name, locator_type="xpath")
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.click(element=self.locators.click_on_sailor_pin_reset, locator_type="xpath")
        self.webDriver.click(element=self.locators.change_my_pin_cta, locator_type="xpath")
        self.verify_create_pin_page()
        self.webDriver.click(element=self.locators.enter_next_btn, locator_type="xpath")
        self.webDriver.click(element=self.locators.enter_confirm_pin, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.pin_reset_success,
                                                                        locator_type="xpath", time_out=20)
        pin_reset_success = self.webDriver.is_element_display_on_screen(element=self.locators.pin_reset_success,
                                                                        locator_type="xpath")
        assert pin_reset_success, "sailor pin reset is not successful"
        self.webDriver.click(element=self.locators.enter_confirm_pin, locator_type="xpath")
        self.webDriver.click(element=self.locators.logout, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.next_button, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.username, locator_type='xpath',
                                                      time_out=60)

    def verify_toggle_button_in_settings(self):
        """
        Function to verify toggle button in jenkins page
        :return:
        """
        self.webDriver.click(element=self.locators.settings, locator_type="xpath")
        near_by = self.webDriver.is_element_display_on_screen(element=self.locators.near_by, locator_type="xpath")
        assert near_by, "near by name not displayed on settings screen"
        near_by_toggle = self.webDriver.is_element_display_on_screen(element=self.locators.nearby_toggle,
                                                                     locator_type="xpath")
        assert near_by_toggle, "near by toggle button not displayed on screen"
        self.webDriver.click(element=self.locators.settings_back_btn, locator_type="xpath")

    def verify_runner_is_able_to_access_defined_functionality(self):
        """
        Function to verify runner is able to access defined functionality
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type="xpath")
        self.webDriver.wait_for(1)
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "HOUSEKEEPING",
                                                             locator_type="xpath")
        assert module, "Runner is not able to see defined module"

    def verify_crew_are_manager_is_able_to_access_defined_functionality(self):
        """
        Function to verify crew area manager is able to access defined functionality
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type="xpath")
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "Contacts",
                                                             locator_type="xpath")
        assert module, "contacts module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "Chat",
                                                             locator_type="xpath")
        assert module, "chat module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "Notifications",
                                                             locator_type="xpath")
        assert module, "Notifications module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "DELIVERY MANAGER",
            locator_type="xpath")
        assert module, "DELIVERY MANAGER module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "SERVER",
                                                             locator_type="xpath")
        assert module, "SERVER module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "VIRTUAL QUEUES",
                                                             locator_type="xpath")
        assert module, "VIRTUAL QUEUES module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "GREETER",
                                                             locator_type="xpath")
        assert module, "GREETER module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "TABLE MANAGEMENT",
            locator_type="xpath")
        assert module, "TABLE MANAGEMENT module is not displayed in left hamburger menu"
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "SAILOR PIN RESET",
            locator_type="xpath")
        assert module, "SAILOR PIN RESET module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "CREW PORTAL",
                                                             locator_type="xpath")
        assert module, "CREW PORTAL module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "INCIDENT MANAGEMENT",
            locator_type="xpath")
        assert module, "INCIDENT MANAGEMENT module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "TRACKABLE MANAGEMENT",
            locator_type="xpath")
        assert module, "TRACKABLE MANAGEMENT module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "HELP CENTER",
                                                             locator_type="xpath")
        assert module, "HELP CENTER module is not displayed in left hamburger menu"

    def verify_delivery_manager_is_able_to_access_defied_functionalities(self):
        """
        Function to verify delivery manager is able to access defined functionalities
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type="xpath")
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "DELIVERY MANAGER",
            locator_type="xpath")
        assert module, "DELIVERY MANAGER module is not displayed in left hamburger menu"
        module = self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_module % "SERVER",
                                                             locator_type="xpath")
        assert module, "SERVER module is not displayed in left hamburger menu"

    def verify_box_office_manager_is_able_to_access_defied_functionalities(self):
        """
        Function to verify box office manager is able to access defined functionalities
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type="xpath")
        module = self.webDriver.is_element_display_on_screen(
            element=self.locators.dashboard_module % "Support Queue",
            locator_type="xpath")
        assert module, "Support Queue module is not displayed in left hamburger menu"

    def click_on_greeter_module(self):
        """
        This function is to open greeter module from submodule showing under Greeter
        :return:
        """
        self.webDriver.click(element=self.locators.open_greeter_module, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.record_audio_popup, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.record_audio_popup, locator_type="xpath")
