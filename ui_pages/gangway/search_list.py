__author__ = 'prahlad.sharma'

from virgin_utils import *


class Search_list(General):
    """
    Page class for Search list
    """
    def __init__(self, web_driver, config, test_data):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "back_button": "//android.widget.ImageButton[@content-desc='‎‏‎‎‎‎‎‏‎‏‏‏‎‎‎‎‎‏‎‎‏‎‎‎‎‏‏‏‏‏‎‏‏‎‏‏‎‎‎‎‏‏‏‏‏‏‏‎‏‏‏‏‏‎‏‎‎‏‏‎‏‎‎‎‎‎‏‏‏‎‏‎‎‎‎‎‏‏‎‏‏‎‎‏‎‏‎‏‏‏‏‏‎‎Navigate up‎‏‎‎‏‎']",
            "sailor_tab": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='Sailor']/android.widget.TextView",
            "crew_tab": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='Crew']/android.widget.TextView",
            "visitor_tab": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='Visitor']/android.widget.TextView",
            "ship_date_time": "com.decurtis.dxp.gangway:id/ship_date_and_time",
            "voyage_name": "com.decurtis.dxp.gangway:id/voyage_header_name",
            "voyage_number": "com.decurtis.dxp.gangway:id/voyage_number",
            "network_status_indicator": "com.decurtis.dxp.gangway:id/network_status_indicator",
            "network_name": "com.decurtis.dxp.gangway:id/network_name",
            "click_on_check_in_filter": "com.decurtis.dxp.gangway:id/check_in_filter",
            "grid_view": "com.decurtis.dxp.gangway:id/gridView",
            "list_view": "com.decurtis.dxp.gangway:id/listView",
            "search_list": "com.decurtis.dxp.gangway:id/search_list",
            "search_list_item": "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.decurtis.dxp.gangway:id/search_list']/android.view.ViewGroup",
            "no_result": "//*[@text='No Record(s) Available']",
            "spinner": "com.decurtis.dxp.gangway:id/progressBar1",
            "alert_icon": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.ImageView[1]",
            "name": "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.decurtis.dxp.gangway:id/search_list']/android.view.ViewGroup[%s]/android.widget.TextView[@resource-id='com.decurtis.dxp.gangway:id/name']",
            "ashore": "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.decurtis.dxp.gangway:id/check_in_state'']/android.view.ViewGroup[%s]//android.widget.RadioGroup/android.widget.RadioButton[@resource-id='com.decurtis.dxp.gangway:id/ashore']",
            "override_button": "com.decurtis.dxp.gangway:id/override",
            "mode_conflict_popup": "//*[@text='Mode Conflict']",
            "ashore_button_on_popup": "//*[@text='ASHORE']",
            "onboard_button_on_popup": "//*[@text='ONBOARD']",
            "cancel_button_on_popup": "//*[@text='CANCEL']",
            "guest_name": "com.decurtis.dxp.gangway:id/name",
            "alert_title": "com.decurtis.dxp.gangway:id/alert_action",
            "message_icon": "com.decurtis.dxp.gangway:id/message",
            "stateroom": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                         "/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup"
                         "/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager"
                         "/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView"
                         "/android.view.ViewGroup[1]/android.widget.TextView[5]",
            "crew_cabin": "com.decurtis.dxp.gangway:id/cabin",
            "onboard_first_guest": "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.decurtis.dxp.gangway:id/search_list']/android.view.ViewGroup[%s]/android.widget.TextView[@resource-id='com.decurtis.dxp.gangway:id/item_guest']",
            "alert_popup": "//*[@resource-id='android:id/content']",
            "click_on_cancel": "com.decurtis.dxp.gangway:id/cancel",
            "alert_override": "	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[%s]/android.view.ViewGroup/android.widget.Button[3]",
            "onboard_on_details": "com.decurtis.dxp.gangway:id/on_board",
            "ashore_on_details": "com.decurtis.dxp.gangway:id/ashore",
            "status_verification2": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[%s]/android.widget.TextView[8]",
            "status_verification1": "(//*[@resource-id='com.decurtis.dxp.gangway:id/check_in_state'])[%s]",
            "edit_alert": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[%s]/android.view.ViewGroup/android.widget.Button[1]",
            "alert_message": "com.decurtis.dxp.gangway:id/alert_message",
            "click_acknowledge": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[%s]/android.view.ViewGroup/android.widget.Button[2]",
            "verify_checked_ashore": "//android.widget.RadioButton[@resource-id='com.decurtis.dxp.gangway:id/ashore' and @checked='true']",
            "verify_checked_onboard": "//android.widget.RadioButton[@resource-id='com.decurtis.dxp.gangway:id/on_board' and @checked='true']",
            "guest_list": "com.decurtis.dxp.gangway:id/item_drill_down",
            "trackable": "com.decurtis.dxp.gangway:id/trackable_assignment",
            "rfid": "//*[@text='Unassigned']",
            "tabs": "//*[@class='androidx.appcompat.app.ActionBar$Tab']",
        })

    def click_on_onboard_guest(self):
        """
        Function to click on on-board button
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.click_onboard_on_details()
            override_list = self.webDriver.get_elements(element=self.locators.override_button, locator_type='id')
            count = len(override_list)

            if count != 0:
                for override in override_list:
                    override.click()
                    self.webDriver.wait_for(2)
                    override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                locator_type='id')
                    break
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def check_availability_of_search_result(self):
        """
        Function to check the availability of search result page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_result, locator_type='xpath')

    def click_crew(self):
        """
        Function to click on crew tab
        """
        self.webDriver.click(element=self.locators.crew_tab, locator_type='xpath')

    def click_visitor(self):
        """
        Function to click on crew tab
        """
        self.webDriver.click(element=self.locators.visitor_tab, locator_type='xpath')

    def click_sailor(self):
        """
        Function to click on crew tab
        """
        self.webDriver.click(element=self.locators.sailor_tab, locator_type='xpath')

    def click_on_onboard(self):
        """
        Function to click on on-board button
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.click_onboard_on_details()
            override_list = self.webDriver.get_elements(element=self.locators.override_button, locator_type='id')
            count = len(override_list)

            while count != 0:
                for override in override_list:
                    override.click()
                    count = count - 1
                    self.webDriver.wait_for(2)
                    override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                locator_type='id')
                    count = len(override_list)
                    break
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        return len(search_list)

    def click_onboard_visitor(self):
        """
        Function to onboard the Visitor
        :return:
        """
        if not self.click_onboard_on_details():
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            logger.info("visitor is rejected")
            return 0
        else:
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            return 1

    def click_ashore_visitor(self):
        """
        Function to Ashore the Visitor
        :return:
        """
        self.click_ashore_on_details()
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        return 1

    def click_back(self):
        """
        Function to click on back button
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def select_tab(self, tab_name):
        """
        Function to select the tab
        :param tab_name:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tabs, locator_type='xpath', time_out=120)
        all_tabs = self.webDriver.get_elements(element=self.locators.tabs, locator_type='xpath')
        for tab in all_tabs:
            if tab_name in tab.tag_name:
                tab.click()
                break
        return all_tabs

    def verify_rfid(self):
        """
        To verify rfid card
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.webDriver.wait_for(2)
            self.select_tab('Additional Info')
            self.webDriver.wait_for(2)
            self.webDriver.scroll_mobile(1400, 2300, 1445, 1585)
            self.webDriver.wait_for(2)
            card_status = self.webDriver.get_text(element=self.locators.trackable, locator_type='id')
            if card_status == "Assigned":
                return True
            else:
                self.click_back()
                continue

    def verify_card(self):
        """
        Function to verify card
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.webDriver.wait_for(2)
            self.select_tab('Additional Info')
            self.webDriver.wait_for(2)
            self.webDriver.scroll_mobile(1400, 2300, 1445, 1585)
            self.webDriver.explicit_visibility_of_element(element=self.locators.rfid, locator_type='xpath', time_out=2000)
            if self.webDriver.is_element_enabled(element=self.locators.trackable, locator_type='id'):
                self.click_back()
                self.click_back()
                return False
            else:
                self.click_back()
                self.click_back()
                return True

    def click_on_ashore_sailor(self):
        """
        debark sailor
        :return:
        """
        self.click_ashore_on_details()
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.ashore_button_on_popup,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.ashore_button_on_popup, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.alert_title, locator_type='id'):
            alert_type = self.webDriver.get_text(element=self.locators.alert_title, locator_type='id')
            if alert_type == 'CBP Hold' or alert_type == 'Deny Ashore':
                override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                            locator_type='id')
                count = len(override_list)
                while count != 0:
                    override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                locator_type='id')
                    for override in override_list:
                        override.click()
                        count = count - 1
                        self.webDriver.wait_for(2)
                        override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                    locator_type='id')
                        count = len(override_list)
                        break
        self.webDriver.wait_for(10)
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def click_on_ashore(self):
        """
        Function to click on Ashore button
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.click_ashore_on_details()
            self.webDriver.wait_for(3)
            if self.webDriver.is_element_display_on_screen(element=self.locators.ashore_button_on_popup,
                                                           locator_type='xpath'):
                self.webDriver.click(element=self.locators.ashore_button_on_popup, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.alert_title, locator_type='id'):
                alert_type = self.webDriver.get_text(element=self.locators.alert_title, locator_type='id')
                if alert_type == 'CBP Hold' or alert_type == 'Deny Ashore':
                    override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                locator_type='id')
                    count = len(override_list)
                    while count != 0:
                        override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                    locator_type='id')
                        for override in override_list:
                            override.click()
                            count = count - 1
                            self.webDriver.wait_for(2)
                            override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                                        locator_type='id')
                            count = len(override_list)
                            break
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        return len(search_list)

    def open_guest_details(self, guest_number):
        """
        Open the Guest details
        """
        guest_name_list = self.webDriver.get_elements(element=self.locators.guest_name, locator_type='id')
        for name in guest_name_list:
            if guest_number == guest_name_list.index(name)+1:
                name.click()
                break

    def open_visitor_details(self, visitor_name):
        """
        Open the Visitor details
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.guest_name, locator_type='id', time_out=60)
        flag = False
        while not flag:
            visitor_name_list = self.webDriver.get_elements(element=self.locators.guest_name, locator_type='id')
            for name in visitor_name_list:
                if visitor_name == name.text:
                    name.click()
                    flag = True
                    break
            else:
                self.webDriver.scroll_mobile(1554, 2240, 1559, 740)
                flag = False

    def click_onboard_on_details(self):
        """
        Function to click on on-board button on details page
        """
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.onboard_on_details, locator_type='id'):
            self.webDriver.click(element=self.locators.onboard_on_details, locator_type='id')
            return True
        else:
            return False

    def click_ashore_on_details(self):
        """
        Function to click on ashore button on details page
        """
        self.webDriver.click(element=self.locators.ashore_on_details, locator_type='id')

    def verify_alert_icon(self):
        """
        verify the alert icon
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.alert_icon, locator_type='xpath')

    def verify_message_icon(self):
        """
        verify the Message icon
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.message_icon, locator_type='id')

    def verify_after_onboard(self):
        """
        verify the after onboard
        """
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            status = self.webDriver.get_text(element=self.locators.status_verification1 % index, locator_type='xpath')
            if not bool(re.findall("Onboard", status)):
                status = self.webDriver.get_text(element=self.locators.status_verification2 % index,
                                                 locator_type='xpath')
                if not bool(re.findall("Onboard", status)):
                    raise Exception("After onboard guest are reset again ashore after search")
            else:
                logger.info("Onboard status found for the guest")
                break

    def verify_after_ashore(self):
        """
        Verify the after Ashore and again search
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_list_item, locator_type='xpath',
                                                      time_out=60)
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            self.webDriver.wait_for(5)
            if self.webDriver.is_element_display_on_screen(element=self.locators.verify_checked_ashore, locator_type='xpath'):
                logger.info("Record is Ashored")
                self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            else:
                self.webDriver.allure_attach_jpeg("Ashore is not checked")
                raise Exception("Ashore button is not checked after Ashore")

    def get_stateroom_no(self):
        """
        Get stateroom
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.stateroom, locator_type='xpath',
                                                      time_out=60)
        stateroom = self.webDriver.get_text(element=self.locators.stateroom, locator_type='xpath')
        if stateroom == 'GTY':
            logger.info("The state room is GTY")
            return stateroom
        else:
            return stateroom

    def get_crew_cabin(self):
        """
        Get Crew cabin no
        """
        return self.webDriver.get_text(element=self.locators.stateroom, locator_type='xpath')

    def click_on_override_alert(self):
        """
        Click on Override alert
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.alert_override % self.test_data['alert_count'], locator_type='xpath'):
            self.webDriver.click(element=self.locators.alert_override % self.test_data['alert_count'], locator_type='xpath')
        else:
            logger.error("Guest Alert Override option is not enable")

    def click_on_visitor(self):
        """
        Click first visitor
        """
        search_list = self.webDriver.get_elements(element=self.locators.search_list_item, locator_type='xpath')
        for search in search_list:
            index = search_list.index(search)
            index = index + 1
            self.open_guest_details(index)
            break

    def click_on_cancel_option(self, tabs, type):
        """
        Function to verify the alert and message
        :param tabs:
        :param type:
        """
        count = 0
        for tab in tabs:
            if type in tab.tag_name:
                count = tab.tag_name.split(' ')[1].replace('(', '').replace(')', '')
                break
        while int(count) > 0:
            if type == "Alerts":
                while int(count) > 1:
                    self.webDriver.scroll_mobile(1560, 2360, 1560, 1507)
                    count = int(count) - 1
                if self.webDriver.is_element_enabled(element=self.locators.edit_alert % count, locator_type='xpath'):
                    self.webDriver.click(element=self.locators.edit_alert % count, locator_type='xpath')
                    if self.webDriver.is_element_display_on_screen(element=self.locators.alert_popup, locator_type='xpath'):
                        self.webDriver.click(element=self.locators.click_on_cancel, locator_type='id')
                        count = int(count) - 1
                    else:
                        raise Exception("Edit Alert button is not visible!!!")
                else:
                    count = int(count) - 1
            else:
                while int(count) > 1:
                    self.webDriver.scroll_mobile(1560, 2360, 1560, 1507)
                    count = int(count) - 1
                if self.webDriver.is_element_display_on_screen(element=self.locators.click_acknowledge % count, locator_type='xpath'):
                    self.webDriver.click(element=self.locators.click_acknowledge % count, locator_type='xpath')
                    count = int(count) - 1
                else:
                    raise Exception("Massage Acknowledge button is not visible!!!")
        self.test_data['alert_count'] = count

    def click_on_first_guest_from_list(self):
        """
        Function to click on First guest from checked in, not Checked-in etc list
        :return:
        """
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.guest_list, locator_type='id'):
            self.webDriver.click(element=self.locators.guest_list, locator_type='id')
            return True
        else:
            return False

    def override_alert(self):
        """
        Function to Override the alert
        :return:
        """
        override_list = self.webDriver.get_elements(element=self.locators.override_button, locator_type='id')
        count = len(override_list)

        while count != 0:
            for override in override_list:
                override.click()
                count = count - 1
                self.webDriver.wait_for(2)
                override_list = self.webDriver.get_elements(element=self.locators.override_button,
                                                            locator_type='id')
                count = len(override_list)
                break

        return count
