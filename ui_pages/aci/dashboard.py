__author__ = 'sarvesh.singh'

from virgin_utils import *


class Dashboard(General):
    """
    Page class for Dashboard screen of ACI app
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
                "navigation_drawer": "//android.widget.ImageButton[@content-desc='Open navigation drawer']",
                "search_icon": "//android.widget.TextView[@content-desc='Search for Sailor / Crew / Visitor']",
                "search_textbox_id": "com.decurtis.dxp.aci:id/search_src_text",
                "sailor_not_checkedin_id": "com.decurtis.dxp.gangway:id/guest_not_checked_in",
                "aci_dashboard": "//*[@text='ACI Dashboard']",
                "dashboard_tab": "//*[@text='Assisted Check-in Dashboard']",
                "setting_tab": "//*[@text='Settings']",
                "signout_tab": "//*[@text='Sign Out']",
                "sign_out_confirmation": "//*[@text='SIGN OUT']",
                "cancel_confirmation": "//*[@text='CANCEL']",
                "spinner": "com.decurtis.dxp.aci:id/progressBar1",
                "back": "//android.widget.ImageButton[@content-desc='‎‏‎‎‎‎‎‏‎‏‏‏‎‎‎‎‎‏‎‎‏‎‎‎‎‏‏‏‏‏‎‏‏‎‏‏‎‎‎‎‏‏‏‏‏‏‏‎‏‏‏‏‏‎‏‎‎‏‏‎‏‎‎‎‎‎‏‏‏‎‏‎‎‎‎‎‏‏‎‏‏‎‎‏‎‏‎‏‏‏‏‏‎‎Navigate up‎‏‎‎‏‎']",
                "hamburger_menu": "//*[@content-desc='Navigate up']",
                "hamburger_menu_1": "//*[@content-desc='Open navigation drawer']",
                "terminal": "//*[text()='Terminal']",
                "resort_airport": "//*[text()='Resort / Airport']",
                "save_button": "//*[text()='SAVE']",
                "signout": "com.decurtis.dxp.aci:id/sign_out",
                "voyage_dropdown": "android:id/text1",
                "three_dot_icon": "//*[@content-desc='More options']",
                "manage_alert": "//*[@text='Manage Alerts']",
                "create_alert": "//*[@text='CREATE ALERT']",
                "alert_type": "(//*[@resource-id='android:id/text1'])[1]",
                "department": "(//*[@resource-id='android:id/text1'])[2]",
                "description": "//*[@class='android.widget.EditText']",
                "msg_description": "(//*[@class='android.widget.EditText'])[2]",
                "create": "//*[@text='CREATE']",
                "alert_code": "(//*[@resource-id='android:id/text1'])[1]",
                "code_option": "(//*[@class='android.widget.CheckedTextView'])[2]",
                "start_date": "(//*[@resource-id='com.decurtis.dxp.aci:id/edit_text'])[2]",
                "start_time": "(//*[@resource-id='com.decurtis.dxp.aci:id/edit_text'])[3]",
                "ok": "//*[@text='OK']",
                "edit": "//*[@resource-id='com.decurtis.dxp.aci:id/edit']",
                "edited_alert": "//*[@text='automate_Test_alert_edit']/following-sibling::*[@resource-id='com.decurtis.dxp.aci:id/edit']",
                "save": "//*[@text='SAVE']",
                "alert_list": "//*[@resource-id='com.decurtis.dxp.aci:id/alert_message']",
                "delete": "//*[@text='DELETE']",
                "create_message": "//*[@text='Create Message']",
                "msg_tab": "//*[contains(@text,'MESSAGES')]",
                "acknowledge": "//*[@text='ACKNOWLEDGE']",
                "ship_itinerary": "//*[@text='Ship Itinerary']",
                "itinerary": "com.decurtis.dxp.aci:id/item_ship_itinerary",
                "msg_list": "com.decurtis.dxp.aci:id/message_body",
                "mode": "com.decurtis.dxp.aci:id/gangway_mode",
                "voyages": "//*[@class='android.widget.CheckedTextView']",
                "voyage": "(//*[@class='android.widget.CheckedTextView'])[2]",
            })
        else:
            self.locators = self.dict_to_ns({
                "navigation_drawer": "//android.widget.ImageButton[@content-desc='Open navigation drawer']",
                "search_icon": "//android.widget.TextView[@content-desc='Search for Guest / Crew / Visitor']",
                "search_textbox_id": "com.decurtis.dxp.aci.dclnp:id/search_src_text",
                "sailor_not_checkedin_id": "com.decurtis.dxp.gangway:id/guest_not_checked_in",
                "aci_dashboard": "//*[@text='ACI Dashboard']",
                "dashboard_tab": "//*[@text='Assisted Check-in Dashboard']",
                "setting_tab": "//*[@text='Settings']",
                "ship_itinerary": "//*[@text='Ship Itinerary']",
                "signout_tab": "//*[@text='Sign Out']",
                "sign_out_confirmation": "//*[@text='SIGN OUT']",
                "cancel_confirmation": "//*[@text='CANCEL']",
                "spinner": "com.decurtis.dxp.aci.dclnp:id/progressBar1",
                "back": "//android.widget.ImageButton["
                        "@content-desc"
                        "='‎‏‎‎‎‎‎‏‎‏‏‏‎‎‎‎‎‏‎‎‏‎‎‎‎‏‏‏‏‏‎‏‏‎‏‏‎‎‎‎‏‏‏‏‏‏‏‎‏‏‏‏‏‎‏‎‎‏‏‎‏‎‎‎‎‎‏‏‏‎‏‎‎‎‎‎‏‏‎‏‏‎‎‏‎‏‎‏‏‏‏‏‎‎Navigate up‎‏‎‎‏‎']",
                "hamburger_menu": "//*[@content-desc='Navigate up']",
                "hamburger_menu_1": "//*[@content-desc='Open navigation drawer']",
                "terminal": "//*[text()='Terminal']",
                "resort_airport": "//*[text()='Resort / Airport']",
                "save_button": "//*[text()='SAVE']",
                "signout": "com.decurtis.dxp.aci:id/sign_out",
                "voyage_dropdown": "android:id/text1",
                "three_dot_icon": "//*[@content-desc='More options']",
                "manage_alert": "//*[@text='Manage Alerts']",
                "create_alert": "//*[@text='CREATE ALERT']",
                "alert_code": "(//*[@resource-id='android:id/text1'])[1]",
                "code_option": "(//*[@class='android.widget.CheckedTextView'])[2]",
                "alert_type": "(//*[@resource-id='android:id/text1'])[2]",
                "department": "(//*[@resource-id='android:id/text1'])[3]",
                "description": "//*[@class='android.widget.EditText']",
                "msg_description": "(//*[@class='android.widget.EditText'])[2]",
                "create": "//*[@text='CREATE']",
                "start_date": "(//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/edit_text'])[2]",
                "start_time": "(//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/edit_text'])[3]",
                "ok": "//*[@text='OK']",
                "edit": "//*[@text='automate_Test_alert']/following-sibling::*[@resource-id='com.decurtis.dxp.aci.dclnp:id/edit']",
                "edited_alert": "//*[@text='automate_Test_alert_edit']/following-sibling::*[@resource-id='com.decurtis.dxp.aci.dclnp:id/edit']",
                "save": "//*[@text='SAVE']",
                "alert_list": "//*[@resource-id='com.decurtis.dxp.aci.dclnp:id/alert_message']",
                "delete": "//*[@text='DELETE']",
                "mode": "com.decurtis.dxp.aci.dclnp:id/gangway_mode",
                "voyages": "//*[@class='android.widget.CheckedTextView']",
                "voyage": "(//*[@class='android.widget.CheckedTextView'])[2]",
                "itinerary": "com.decurtis.dxp.aci.dclnp:id/item_ship_itinerary",
                "msg_list": "com.decurtis.dxp.aci.dclnp:id/message_body",
            })

    def verify_itinerary(self):
        """
        To verify itinerary
        :return:
        """
        return len(self.webDriver.get_elements(element=self.locators.itinerary, locator_type='id'))

    def click_on_ship_itinerary(self):
        """
        Function to click on ship itinerary on hamburger menu
        """
        self.webDriver.click(element=self.locators.ship_itinerary, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=60)

    def verify_voyage_in_hotel_mode(self):
        """
        To verify the voyages
        :return:
        """
        self.webDriver.click(element=self.locators.voyages, locator_type='xpath')
        if len(self.webDriver.get_elements(element=self.locators.voyages, locator_type='xpath')) == 1:
            return False
        else:
            self.webDriver.click(element=self.locators.voyage, locator_type='xpath')
            return True

    def verify_hotel_mode(self):
        """
        To verify hetel mode
        :return:
        """
        return self.webDriver.get_text(element=self.locators.mode, locator_type='id')

    def acknowledge_message(self):
        """
        To acknowledge message
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.acknowledge, locator_type='xpath',
                                                      time_out=30)
        acknowledgement = self.webDriver.get_elements(element=self.locators.acknowledge, locator_type='xpath')
        for msg in range(0, len(acknowledgement)):
            self.webDriver.click(element=self.locators.acknowledge, locator_type='xpath')
        return self.webDriver.is_element_display_on_screen(element=self.locators.acknowledge, locator_type='xpath')

    def verify_edit_msg(self):
        """
        To verify edit message
        :return:
        """
        msges = self.webDriver.get_elements(element=self.locators.msg_list, locator_type='id')
        for msg in msges:
            if msg.text == "automate_Test_message_edit":
                return True
            else:
                continue

    def edit_message(self):
        """
        To edit message
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.click(element=self.locators.edit, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.msg_description, locator_type='xpath', action_type='clear')
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.msg_description, locator_type='xpath',
                                text="automate_Test_message_edit")
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.start_time, locator_type='xpath')
        self.webDriver.click(element=self.locators.ok, locator_type='xpath')
        self.webDriver.click(element=self.locators.save, locator_type='xpath')

    def verify_message(self):
        """
        To verify message
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.msg_tab, locator_type='xpath',
                                                      time_out=30)
        self.webDriver.click(element=self.locators.msg_tab, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.edit, locator_type='xpath'):
            return False
        else:
            return True

    def create_message(self):
        """
        To create message for sailor
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.three_dot_icon, locator_type='xpath',
                                                      time_out=30)
        self.webDriver.click(element=self.locators.three_dot_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.create_message, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.msg_description, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.msg_description, locator_type='xpath',
                                text="automate_Test_message")
        self.webDriver.click(element=self.locators.start_time, locator_type='xpath')
        self.webDriver.click(element=self.locators.ok, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def verify_delete_alert(self):
        """
        To verify delete alert
        :return:
        """
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.alert_list, locator_type='xpath'):
            alerts = self.webDriver.get_elements(element=self.locators.alert_list, locator_type='xpath')
            for alert in alerts:
                if alert.text == "automate_Test_alert_edit":
                    return False
                else:
                    continue
            else:
                return True
        else:
            return True

    def delete_alert(self):
        """
        To delete alert
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')

    def verify_edit_alert(self):
        """
        To verify edit alert
        :return:
        """
        alerts = self.webDriver.get_elements(element=self.locators.alert_list, locator_type='xpath')
        for alert in alerts:
            if alert.text == "automate_Test_alert_edit":
                return True
            else:
                continue

    def edit_alert(self):
        """
        To edit alert
        :return:
        """
        self.webDriver.click(element=self.locators.edit, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.description, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.description, locator_type='xpath',
                                text="automate_Test_alert_edit")
        self.webDriver.click(element=self.locators.start_date, locator_type='xpath')
        self.webDriver.click(element=self.locators.ok, locator_type='xpath')
        self.webDriver.click(element=self.locators.save, locator_type='xpath')

    def verify_alert(self):
        """
        To verify alert
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.edit, locator_type='xpath'):
            return False
        else:
            return True

    def verify_edited_alert(self):
        """
        To verify alert
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.edited_alert, locator_type='xpath'):
            return False
        else:
            return True

    def create_alert_sailor(self):
        """
        To create alert for sailor
        :return:
        """
        self.webDriver.click(element=self.locators.alert_type, locator_type='xpath')
        self.webDriver.click(element=self.locators.code_option, locator_type='xpath')
        self.webDriver.click(element=self.locators.department, locator_type='xpath')
        self.webDriver.click(element=self.locators.code_option, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.description, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.description, locator_type='xpath', text="automate_Test_alert")
        self.webDriver.click(element=self.locators.start_date, locator_type='xpath')
        self.webDriver.click(element=self.locators.ok, locator_type='xpath')
        self.webDriver.scroll_mobile(x_press=676, y_press=963, x_move=661, y_move=857)
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def select_alert_code(self):
        """
        To create alert code
        :return:
        """
        self.webDriver.click(element=self.locators.alert_code, locator_type='xpath')
        self.webDriver.click(element=self.locators.code_option, locator_type='xpath')

    def create_alert_option(self):
        """
        To create alert option
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.three_dot_icon, locator_type='xpath',
                                                      time_out=30)
        self.webDriver.click(element=self.locators.three_dot_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.manage_alert, locator_type='xpath')
        self.webDriver.click(element=self.locators.create_alert, locator_type='xpath')

    def verify_search_icon(self):
        """
        To verify search icon
        :return:
        """
        self.webDriver.wait_for(2)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_icon, locator_type='xpath'):
            return False
        else:
            return True

    def verify_voyage_dropdown(self):
        """
        To verify voyage drop down
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_dropdown, locator_type='id'):
            raise Exception("Voyage dropdown is not displaying")

    def click_signout(self):
        """
        To click on signout button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.signout_tab, locator_type='xpath',
                                                      time_out= 30)
        self.webDriver.click(element=self.locators.signout_tab, locator_type='xpath')
        self.webDriver.click(element=self.locators.sign_out_confirmation, locator_type='xpath')

    def check_availability_of_dashboard_page(self):
        """
        Function to check the availability of dashboard page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.dashboard_tab, locator_type='xpath',
                                                      time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_tab,
                                                           locator_type='xpath')

    def click_on_navigation_drawer(self):
        """
        Function to click on navigation dashboard
        """
        self.webDriver.click(element=self.locators.navigation_drawer, locator_type='xpath')

    def sign_out(self):
        """
        Function to sign out
        """
        self.webDriver.click(element=self.locators.signout_tab, locator_type='xpath')
        self.webDriver.click(element=self.locators.sign_out_confirmation, locator_type='xpath')

    def search(self, text):
        """
        Function for search the guest, crew, visitor
        :param text:
        """

        self.webDriver.click(element=self.locators.search_icon, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.search_textbox_id, locator_type='id', text=text)
        self.webDriver.submit()
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=60)

    def navigate_back(self):
        """
        Function for navigating back
        """
        self.webDriver.click(element=self.locators.back, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_on_hamburger_menu(self):
        """
        Function for clicking on hamburger menu
        """
        try:
            self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
            self.webDriver.wait_for(2)
        except Exception:
            self.webDriver.click(element=self.locators.hamburger_menu_1, locator_type='xpath')
            self.webDriver.wait_for(2)

    def click_on_settings_page(self):
        """
        Function to click on setting on hamburger menu
        """
        self.webDriver.click(element=self.locators.setting_tab, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_on_terminal_dropdown(self):
        """
        Function for clicking on terminal on settings
        """
        self.webDriver.click(element=self.locators.terminal, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_on_resort_and_terminal_mode(self):
        """
        Function for clicking on resort and airport mode on settings
        """
        self.webDriver.click(element=self.locators.resort_airport, locator_type='xpath')
        self.webDriver.wait_for(2)

    def click_on_save(self):
        """
        Function for clicking on save button on settings
        """
        self.webDriver.click(element=self.locators.save_button, locator_type='xpath')
        self.webDriver.wait_for(2)
