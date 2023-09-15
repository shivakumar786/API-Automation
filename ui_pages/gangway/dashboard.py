__author__ = 'prahlad.sharma'

from virgin_utils import *


class Dashboard(General):
    """
    Page class for Dashboard screen of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.config = config
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "navigation_drawer": "//android.widget.ImageButton[@content-desc='Open navigation drawer']",
            "search_icon": "//android.widget.TextView[@content-desc='Search for Sailor / Crew / Visitor']",
            "dcl_search_icon": "com.decurtis.dxp.gangway:id/action_search",
            "search_textbox_id": "com.decurtis.dxp.gangway:id/search_src_text",
            "sailor_not_checkedin_id": "com.decurtis.dxp.gangway:id/guest_not_checked_in",
            "gangway_dashboard": "//*[@text='Dashboard']",
            "dashboard_tab": "//*[@text='Dashboard']",
            "setting_tab": "//*[@text='Settings']",
            "signout_tab": "//*[@text='Sign Out']",
            "ship_itinerary": "//*[@text='Ship Itinerary']",
            "page_header": "//*[@class='android.widget.TextView' and @text='%s']",
            "gangway_history": "//*[@text='Gangway History']",
            "sign_out_confirmation": "//*[@text='SIGN OUT']",
            "cancel_confirmation": "//*[@text='CANCEL']",
            "active_voyage_name": "android:id/text1",
            "click_checkin_sailors": "com.decurtis.dxp.gangway:id/guest_checked_in",
            "click_first_sailor": "com.decurtis.dxp.gangway:id/person_name",
            "click_onboard_sailors_list": "com.decurtis.dxp.gangway:id/guest_onboard",
            "spinner": "com.decurtis.dxp.gangway:id/progress",
            "total_embarking_today": "com.decurtis.dxp.gangway:id/guest_total_embarking_today",
            "total_leaving_today": "com.decurtis.dxp.gangway:id/guest_total_leaving_today",
            "checkout": "com.decurtis.dxp.gangway:id/guest_checked_out",
            "not_checked_in_onboard": "com.decurtis.dxp.gangway:id/onboard_needs_review",
            "embark_today": "//*[@text='Total Embarking Today']",
            "embarkation_close_tab": "com.decurtis.dxp.gangway:id/cancel",
            "emb_today_counts": "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/"
                                "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/"
                                "android.widget.TextView[2]",
            "not_checked_in_onboard_counts": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                             "android.widget.FrameLayout/android.widget.LinearLayout/"
                                             "android.widget.FrameLayout/android.view.ViewGroup"
                                             "/androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/"
                                             "android.widget.LinearLayout/android.widget.FrameLayout/"
                                             "android.view.ViewGroup/android.widget.FrameLayout[2]"
                                             "/android.widget.ScrollView/android.widget.LinearLayout"
                                             "/android.view.ViewGroup[2]/android.widget.FrameLayout[8]/"
                                             "android.widget.TextView[2]",
            "back_to_dashboard": "//*[@class='android.widget.ImageButton']",
            "check_out_counts": "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout"
                                "/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout"
                                "/android.view.ViewGroup/androidx.drawerlayout.widget.DrawerLayout"
                                "/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout"
                                "/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.ScrollView"
                                "/android.widget.LinearLayout/android.view.ViewGroup[2]/android.widget.FrameLayout[7]"
                                "/android.widget.TextView[2]",
            "verify_tab_name": "//*[@class='android.widget.TextView']",
            "click_search_option": "com.decurtis.dxp.gangway:id/action_search",
            "text_box_for_search": "com.decurtis.dxp.gangway:id/search_src_text",
            "visitor_expected_today": "com.decurtis.dxp.gangway:id/visitor_expected_today",
            "hamburger_icon": "//android.widget.ImageButton[@content-desc='Open navigation drawer']",
            "view_more_guest": "com.decurtis.dxp.gangway:id/guest_view_more_less",
            "view_more": "com.decurtis.dxp.gangway:id/guest_view_more_less",
            "network_name": "com.decurtis.dxp.gangway:id/network_name",
            "document_count": "com.decurtis.dxp.gangway:id/pending_documents",
            "barcode_scan_icon": "com.decurtis.dxp.gangway:id/action_barcode_scan",
            "allow": "com.android.packageinstaller:id/permission_allow_button",
            "search_suggestion_cabin": "com.decurtis.dxp.gangway:id/cabin",
            "visitor_onboard": "com.decurtis.dxp.gangway:id/visitor_onboard",
            "mode_on_dashboard": "com.decurtis.dxp.gangway:id/gangway_mode"
        })

    def check_availability_of_dashboard_page(self):
        """
        Function to check the availability of dashboard page
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.gangway_dashboard, locator_type='xpath',
                                                      time_out=60)
        return self.webDriver.is_element_display_on_screen(element=self.locators.gangway_dashboard,
                                                           locator_type='xpath')

    def check_availability_of_document_count(self):
        """
        Function to check the availability of dashboard page
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.document_count,
                                                           locator_type='id')

    def wait_till_online_the_app(self):
        """
        Function to check the app should come Online
        :return:
        """
        flag = False
        count = 1
        while not flag and count <= 40:
            if self.webDriver.get_text(element=self.locators.network_name, locator_type='id') == 'Online':
                flag = True
            else:
                self.webDriver.wait_for(2)
                count = count + 1

    def click_on_navigation_drawer(self):
        """
        Function to click on navigation dashboard
        """
        self.webDriver.click(element=self.locators.navigation_drawer, locator_type='xpath')

    def click_on_barcode_icon(self):
        """
        Function to click on navigation dashboard
        """
        self.webDriver.click(element=self.locators.barcode_scan_icon, locator_type='id')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow, locator_type='id'):
            self.webDriver.click(element=self.locators.allow, locator_type='id')

    def sign_out(self):
        """
        Function to sign out
        """
        self.webDriver.click(element=self.locators.signout_tab, locator_type='xpath')
        self.webDriver.click(element=self.locators.sign_out_confirmation, locator_type='xpath')

    def sign_out_cancel(self):
        """
        Function to cancel the sign-out process
        :return:
        """
        self.webDriver.click(element=self.locators.signout_tab, locator_type='xpath')
        self.webDriver.click(element=self.locators.cancel_confirmation, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.cancel_confirmation, locator_type='xpath'):
            self.webDriver.allure_attach_jpeg("error_logout")
            raise Exception("After click on cancel button, popup still display on screen")

    def search(self, search_name):
        """
        Function for search the guest, crew, visitor
        :param search_name:
        """
        if self.config.platform == 'DCL' and self.config.envMasked == 'LATEST':
            self.webDriver.click(element=self.locators.dcl_search_icon, locator_type='id')
        else:
            self.webDriver.click(element=self.locators.search_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.search_textbox_id, locator_type='id')
        self.webDriver.set_text(element=self.locators.search_textbox_id, locator_type='id', text=search_name)
        self.webDriver.submit()

    def search_suggestion(self, search_name):
        """
        Check the search suggestion
        :param search_name:
        """
        if self.config.platform == 'DCL' and self.config.envMasked == 'LATEST':
            self.webDriver.click(element=self.locators.dcl_search_icon, locator_type='id')
        else:
            self.webDriver.click(element=self.locators.search_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.search_textbox_id, locator_type='id')
        self.webDriver.set_text(element=self.locators.search_textbox_id, locator_type='id', text=search_name)
        self.webDriver.wait_for(5)
        cabin_number = self.webDriver.get_elements(element=self.locators.search_suggestion_cabin, locator_type='id')
        if len(cabin_number) == 0:
            self.webDriver.allure_attach_jpeg("cabin_Number_error")
            raise Exception("Cabin Number not display after search the guest")

    def get_active_voyage_name(self, voyage_name):
        """
        To get the selected active voyage name
        :param voyage_name:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.spinner, locator_type='id',
                                                        time_out=20)
        self.webDriver.explicit_visibility_of_element(element=self.locators.active_voyage_name, locator_type='id',
                                                      time_out=60)
        selected_voyage_name = self.webDriver.get_text(element=self.locators.active_voyage_name, locator_type='id')
        if selected_voyage_name.split()[0] == voyage_name.split()[0] and selected_voyage_name.split()[1] == \
                voyage_name.split()[1]:
            logger.debug(f"{selected_voyage_name} Selected Voyage name is matching with backend response")
        else:
            raise Exception(f"{selected_voyage_name} Selected Voyage name is not matching with backend {voyage_name} "
                            f"voyage name ")

    def open_check_in_sailors_list(self):
        """
        To open list of checked in sailors
        :return:
        """
        self.webDriver.click(element=self.locators.click_checkin_sailors, locator_type='id')

    def open_details_of_first_sailor(self):
        """
        To open details of first sailor
        :return:
        """
        self.webDriver.click(element=self.locators.click_first_sailor, locator_type='id')

    def open_onboard_sailors_list(self):
        """
        To open onboard sailors list
        :return:
        """
        self.webDriver.click(element=self.locators.click_onboard_sailors_list, locator_type='id')

    def more_option_for_guest(self):
        """
        To Open More option on guest
        """
        self.webDriver.click(element=self.locators.view_more_guest, locator_type='id')

    def total_embarking_today(self):
        """
        To Open the Today Embark Guest list
        :return:
        """
        content = self.webDriver.get_text(element=self.locators.embark_today, locator_type='xpath')
        if content == 'Total Embarking Today':
            self.webDriver.click(element=self.locators.total_embarking_today, locator_type='id')

    def check_embarking_today_counts(self):
        """
        To verify the counts
        """

        emb_count = int(self.webDriver.get_text(element=self.locators.emb_today_counts, locator_type='xpath'))
        if emb_count == 0 or emb_count > 0:
            logger.info("Today's Embarkation counts is right")
        else:
            raise Exception("Counts are not visible")

    def close_tab(self):
        """
        Close the Embarking today tab.
        """
        self.webDriver.click(element=self.locators.embarkation_close_tab, locator_type='id')

    def total_leaving_today_tab(self):
        """
        open total leave today guest tab
        """
        self.webDriver.click(element=self.locators.total_leaving_today, locator_type='id')
        self.webDriver.explicit_visibility_of_element(element=self.locators.verify_tab_name, locator_type='xpath',
                                                      time_out=60)
        verify_tab = self.webDriver.get_text(element=self.locators.verify_tab_name, locator_type='xpath')
        return verify_tab

    def not_checked_in_counts(self):
        """
        Verify the Not checked-in counts
        """
        not_checked_in_counts = int(
            self.webDriver.get_text(element=self.locators.not_checked_in_onboard_counts, locator_type='xpath'))
        if not_checked_in_counts == 0 or not_checked_in_counts > 0:
            logger.info("Not Checked-in Onboard guest counts is visible")
        else:
            raise Exception("Not Checked-in Onboard guest counts is not visible")

    def not_checked_in_onboard_tab(self):
        """
        To Verify the Not checked-in guest tab
        """
        self.webDriver.click(element=self.locators.not_checked_in_onboard, locator_type='id')
        return self.webDriver.get_text(element=self.locators.verify_tab_name, locator_type='xpath')

    def return_back_dashboard(self):
        """"
        Back to Dashboard
        """
        self.webDriver.click(element=self.locators.back_to_dashboard, locator_type='xpath')

    def check_out_count(self):
        """
        Verify the check out counts
        """
        check_out_counts = int(self.webDriver.get_text(element=self.locators.check_out_counts, locator_type='xpath'))
        if check_out_counts == 0 or check_out_counts > 0:
            logger.info("Check out guest counts is visible")
        else:
            raise Exception("Check out guest counts is not visible")

    def check_out_guest_tab(self):
        """
        To verify the Checkout Guest Tab
        """
        self.webDriver.click(element=self.locators.checkout, locator_type='id')
        return self.webDriver.get_text(element=self.locators.verify_tab_name, locator_type='xpath')

    def chick_on_search_option(self):
        """
        Click on search option
        """
        self.webDriver.click(element=self.locators.click_search_option, locator_type='id')

    def text_box_for_search(self, reservation_no):
        """
        Write text for search
        """
        self.webDriver.click(element=self.locators.text_box_for_search, locator_type='id')
        self.webDriver.set_text(element=self.locators.text_box_for_search, locator_type='id', text=reservation_no)

    def expected_today_visitor(self):
        """
        Verify the Expected today visitor
        """
        self.webDriver.scroll_mobile(441, 1001, 459, 511)
        return self.webDriver.is_element_display_on_screen(element=self.locators.visitor_expected_today,
                                                           locator_type='id')

    def open_expected_today_visitor(self):
        """
        Verify the open expected today
        """
        self.webDriver.click(element=self.locators.visitor_expected_today, locator_type='id')

    def click_on_hamburger_icon(self):
        """
        Click on Hamburger menu
        """
        self.webDriver.click(element=self.locators.hamburger_icon, locator_type='xpath')

    def check_in_guest_tab(self):
        """
        Click on guest tab
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.click_checkin_sailors, locator_type='id'):
            self.webDriver.click(element=self.locators.click_checkin_sailors, locator_type='id')

    def check_more_view(self):
        """
        click ok on alert not created pop-up
        """
        self.webDriver.click(element=self.locators.view_more, locator_type='id')

    def open_onboard_visitor(self):
        """
        click on open onboard visitor
        """
        self.webDriver.click(element=self.locators.visitor_onboard, locator_type='id')

    def click_and_verify_ship_itinerary(self):
        """
        Click on Ship Itinerary
        """
        self.webDriver.click(element=self.locators.ship_itinerary, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.page_header % 'Ship Itinerary', locator_type='xpath'):
            self.webDriver.screen_shot("error_ship_itinerary")
            raise Exception("Ship Itinerary page not load on screen")

    def click_and_verify_gangway_history(self):
        """
        Click and verify the Gangway History
        """
        self.webDriver.click(element=self.locators.gangway_history, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.page_header % 'Gangway History', locator_type='xpath'):
            self.webDriver.screen_shot("error_gangway_history")
            raise Exception("gangway history page not load on screen")

    def click_and_verify_setting_page(self):
        """
        Click on verify the setting page
        """
        self.webDriver.click(element=self.locators.setting_tab, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.page_header % 'Settings', locator_type='xpath'):
            self.webDriver.screen_shot("error_settings")
            raise Exception("Settings page not load on screen")

    def open_not_checked_in(self):
        """
        Open the Not Checked-in Guest list
        """
        self.webDriver.click(element=self.locators.sailor_not_checkedin_id, locator_type='id')

    def get_mode_on_dashboard(self):
        """
        Function to check the mode name on Dashboard
        :return:
        """
        return self.webDriver.get_text(element=self.locators.mode_on_dashboard, locator_type='id')

