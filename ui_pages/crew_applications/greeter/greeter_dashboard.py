__author__ = 'HT'

from selenium.webdriver.common.keys import Keys

from virgin_utils import *


class GreeterDashboard(General):
    """
    Page Class For crew dashboard
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Greeter module
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({

            "logout": "//*[@text='LOGOUT']",
            "sync_in_progress_dashboard": "//*[@resource-id='searchButton']/following-sibling::android.widget.TextView",
            "settings": "//android.view.View[@resource-id='root']/android.widget.Button[@resource-id='settingsButton']",
            "refresh_button": "//android.view.View[@resource-id='root']/android.widget.Button[@resource-id='refreshButton']",
            "history_button": "//android.view.View[@resource-id='root']/android.widget.Button[@resource-id='historyButton']",
            "search_button": "//android.view.View[@resource-id='root']/android.widget.Button[@resource-id='searchButton']",
            "info_button": "//android.view.View[@resource-id='root']//android.view.View/android.widget.Button[@resource-id='infoButton']",
            "close_settings": "//android.view.View[@resource-id='root']//android.view.View/android.widget.Button[@resource-id='closeButton']",
            "switch_grid": "//android.view.View[@resource-id='switchGridView']",
            "switch_list": "//android.view.View[@resource-id='switchListView']",
            "images": "//*[@class='android.widget.Image']",
            "select_activity": "//android.view.View[@resource-id='root']//android.view.View[@resource-id='ARSActivityFilterSelectWrapper']",
            "cabin_search": "//android.view.View[@resource-id='root']//android.widget.EditText[@resource-id='TopBar_SearchField']",
            "cabin_search_btn": "//android.view.View[@resource-id='root']//android.widget.Button[@resource-id='searchButton-undefined']",
            "searched_sailor": "(//*[@resource-id='root']/android.view.View//android.widget.Image)[2]",
            "add_booking_cta": "//android.view.View/android.widget.Button[@resource-id='form-input-4313']",
            "non_inventoried": "//*[text()='Ent - Non Inventoried']",
            "selected_activity": "//*[@class='ActivityFilterActivitySelect__activities-list']/div[1]//div[@class='ActivityFilterActivitySlot__name']",
            "click_on_activity": "//*[text()='%s']",
            "save_button": "//*[text()='Save']",
            "statics": "//android.view.View/android.widget.Button[@resource-id='closeButton']/following-sibling::android.view.View[1]",
            "current_voyage": "//*[text()='Current voyage']",
            "checkin_count_ele": "//*[@class='GuestStatistics__stat-name']/span",
            "waver_signed": "//*[text()='Waver is not signed']",
            "total_element": "//*[text()='Total']",
            "search_field": "//*[@resource-id='root']//android.widget.EditText",
            "sailor_search_btn": "(//*[@resource-id='root']//android.widget.Button)[2]",
            "tap_on_sailor": "(//*[@resource-id='root']//android.view.View[3]//android.widget.Image)[1]",
            "add_booking_cta": "//*[text()='Add Booking']",
            "select_time_slot": "//*[text()='Select time slot']",
            "add_guests": "//*[text()='Add Guests']",
            "add_second_sailor": "//div[@class='GuestParty__party']/div[2]//button",
            "activity_type_list": "//*[text()='No Type Selected']",
            "ent_non_inventoried": "//*[@class='Select']//*[text()='Ent - Non Inventoried']",
            "click_on_activity": "//*[@class='ActivityFilterActivitySelect__activities-list']//*[text()='%s']",
            "click_on_select": "//*[text()='Select']",
            "book_now": "//*[text()='BOOK']",
            "booking_conflict": "//*[text()='Booking conflict']",
            "close_btn": "//*[@id='closeButton']",
            "check_in_sailor": "//*[@class='BookingCalendarEntry__details-wrapper']//button[text()='Check In']",
            "greet_sailor": "//*[@class='GuestPartyFooter']/div/button[@id='greetGuestsButton']",
            "back_button": "//android.view.View[@resource-id='root']/android.widget.Button[@resource-id='backButton']",
            "history_header": "//android.view.View[@resource-id='root']/android.view.View[1]",
            "sailor_list_in_history": "//android.view.View[@resource-id='root']/android.view.View[3]/android.view.View",
            "list_of_un_greet_elements":"//*[@resource-id='root']/android.view.View[3]//android.widget.Button",
            "un_greet_button": "(//*[@resource-id='root']/android.view.View[3]//android.widget.Button)[%s]",
            "checkin_again": "//*[@class='BookingCalendarEntry__details-wrapper']//*[text()='Check In']"
        })

    def sync_in_progress(self):
        """
        wait for sync in progress to complete
        :return:
        """
        is_present = self.webDriver.is_element_display_on_screen(element=self.locators.sync_in_progress_dashboard,
                                                                 locator_type='xpath')
        if is_present:
            self.webDriver.explicit_invisibility_of_element(element=self.locators.sync_in_progress_dashboard,
                                                            locator_type='xpath', time_out=300)

    def verify_greeter_dashboard_elements(self):
        """
        This function is to verify greeter dashboard elements
        :return:
        """
        self.sync_in_progress()
        settings = self.webDriver.is_element_display_on_screen(element=self.locators.settings, locator_type="xpath")
        if not settings:
            raise Exception("settings cta is not displayed on greeter dashboard")
        refresh_button = self.webDriver.is_element_display_on_screen(element=self.locators.refresh_button,
                                                                     locator_type="xpath")
        if not refresh_button:
            raise Exception("refresh cta is not displayed on greeter dashboard")
        history_button = self.webDriver.is_element_display_on_screen(element=self.locators.history_button,
                                                                     locator_type="xpath")
        if not history_button:
            raise Exception("history cta is not displayed on greeter dashboard")
        search_button = self.webDriver.is_element_display_on_screen(element=self.locators.search_button,
                                                                    locator_type="xpath")
        if not search_button:
            raise Exception("search cta is not displayed on greeter dashboard")

    def verify_settings_tab_elements(self):
        """
        To verify UI elements if settings screen
        :return:
        """
        self.webDriver.click(element=self.locators.settings, locator_type="xpath")
        info_button = self.webDriver.is_element_display_on_screen(element=self.locators.info_button,
                                                                  locator_type="xpath")
        if not info_button:
            raise Exception("info cta is not displayed on greeter dashboard")
        switch_grid = self.webDriver.is_element_display_on_screen(element=self.locators.switch_grid,
                                                                  locator_type="xpath")
        if not switch_grid:
            raise Exception("switch grid cta is not displayed on greeter dashboard")
        switch_list = self.webDriver.is_element_display_on_screen(element=self.locators.switch_grid,
                                                                  locator_type="xpath")
        if not switch_list:
            raise Exception("switch list cta is not displayed on greeter dashboard")
        elements = self.webDriver.get_elements(self.locators.images, locator_type="xpath")
        assert len(elements) > 10, "Elements are missing from greeter settings tab"

    def select_activity_from_drop_down(self):
        """
        Function to select activity from dropdown
        :return:
        """
        self.webDriver.click(element=self.locators.select_activity, locator_type="xpath")
        self.webDriver.click(element=self.locators.select_activity, locator_type="xpath")
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.non_inventoried, locator_type="xpath")

    def save_non_inventoried_activity(self):
        """
        function to save entertainment activity from list
        :return:
        """
        self.test_data['activityName'] = self.webDriver.get_text(element=self.locators.selected_activity,
                                                                 locator_type="xpath")
        self.webDriver.click(element=self.locators.click_on_activity % self.test_data['activityName'],
                             locator_type="xpath")
        self.webDriver.click(element=self.locators.save_button, locator_type="xpath")

    def verify_information_of_selected_activity(self):
        """
        Function to verify selected activity slot information
        :return:
        """
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.info_button, locator_type="xpath")
        statics = self.webDriver.is_element_display_on_screen(element=self.locators.statics, locator_type="xpath")
        assert statics, "activity info statics page not opened"
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='WEBVIEW_com.decurtis.crew.embark')
        current_voyage = self.webDriver.is_element_display_on_screen(element=self.locators.current_voyage, locator_type="xpath")
        assert current_voyage, "activity info current voyage details not available in statics page"
        checkin_count_ele = self.webDriver.is_element_display_on_screen(element=self.locators.checkin_count_ele,
                                                                     locator_type="xpath")
        assert checkin_count_ele, "activity info checkin count details not available in statics page"
        waver_signed = self.webDriver.is_element_display_on_screen(element=self.locators.waver_signed,
                                                                        locator_type="xpath")
        assert waver_signed, "activity info waver signed  details not available in statics page"
        total_element = self.webDriver.is_element_display_on_screen(element=self.locators.total_element,
                                                                   locator_type="xpath")
        assert total_element, "activity info total count details not available in statics page"
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.close_settings, locator_type="xpath")
        self.webDriver.click(element=self.locators.close_settings, locator_type="xpath")

    def book_activity_for_sailor_from_greeter(self):
        """
        Book activity for sailor from greeter application
        :return:
        """
        self.webDriver.click(element=self.locators.search_button, locator_type="xpath")
        cabin_number = self.test_data['searched_sailor_stateroom']
        self.webDriver.set_text(element=self.locators.search_field, locator_type="xpath", text=cabin_number)
        self.webDriver.click(element=self.locators.sailor_search_btn, locator_type="xpath")
        self.webDriver.click(element=self.locators.tap_on_sailor, locator_type="xpath")
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.add_booking_cta, locator_type="xpath")
        self.webDriver.click(element=self.locators.add_guests, locator_type="xpath")
        if self.webDriver.is_element_display_on_screen(element=self.locators.add_second_sailor, locator_type="xpath"):
            self.webDriver.click(element=self.locators.add_second_sailor, locator_type="xpath")
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.close_settings, locator_type="xpath")
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.select_time_slot, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_type_list, locator_type="xpath")
        self.webDriver.click(element=self.locators.ent_non_inventoried, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.click_on_activity % self.test_data['activityName'],
                             locator_type="xpath", time_out=120)
        self.webDriver.click(element=self.locators.click_on_activity % self.test_data['activityName'],
                             locator_type="xpath")
        self.webDriver.click(element=self.locators.click_on_select, locator_type="xpath")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.booking_conflict, locator_type="xpath"):
            self.webDriver.click(element=self.locators.book_now, locator_type="xpath")
            self.webDriver.explicit_visibility_of_element(element=self.locators.check_in_sailor, locator_type="xpath", time_out=120)
            if not self.webDriver.is_element_display_on_screen(element=self.locators.check_in_sailor, locator_type="xpath"):
                raise Exception("Failed to book entertainment activity")
            self.webDriver.click(element=self.locators.check_in_sailor, locator_type="xpath")
            self.webDriver.explicit_visibility_of_element(element=self.locators.greet_sailor, locator_type="xpath",
                                                          time_out=120)
            self.webDriver.click(element=self.locators.greet_sailor, locator_type="xpath")
            self.test_data['isBookingConflict']= False
            self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')

        else:
            self.test_data['isBookingConflict'] = True
            self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
            self.webDriver.click(element=self.locators.back_button, locator_type="xpath")
            self.webDriver.click(element=self.locators.close_settings, locator_type="xpath")
            logger.info("Booking already exists at this time")

    def verify_history_after_booking_and_checkin_from_greeter(self):
        """
        function to verify history after booking and greeting the sailor from greeter
        :return:
        """
        self.webDriver.click(element=self.locators.back_button, locator_type="xpath")
        self.webDriver.click(element=self.locators.history_button, locator_type="xpath")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.history_header, locator_type="xpath"):
            raise Exception("Failed to load checkin history page")

        sailor_list = self.webDriver.get_elements(element=self.locators.sailor_list_in_history, locator_type="xpath")
        if not self.test_data['isBookingConflict']:
            assert len(sailor_list) >= 1, "sailor are not showing up in history page"
            self.un_greet_greeted_sailor_from_history_page()
            self.webDriver.click(element=self.locators.back_button, locator_type="xpath")
        else:
            self.webDriver.click(element=self.locators.back_button, locator_type="xpath")

    def verify_booking_conflict(self):
        """
        Function to verify booking conflict message/error
        :return:
        """
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.tap_on_sailor, locator_type="xpath")
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.add_booking_cta, locator_type="xpath")
        self.webDriver.click(element=self.locators.add_guests, locator_type="xpath")
        if self.webDriver.is_element_display_on_screen(element=self.locators.add_second_sailor, locator_type="xpath"):
            self.webDriver.click(element=self.locators.add_second_sailor, locator_type="xpath")
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(), context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.close_settings, locator_type="xpath")
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.select_time_slot, locator_type="xpath")
        self.webDriver.click(element=self.locators.activity_type_list, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(
            element=self.locators.click_on_activity % self.test_data['activityName'],
            locator_type="xpath", time_out=120)
        self.webDriver.click(element=self.locators.ent_non_inventoried, locator_type="xpath")

        self.webDriver.click(element=self.locators.click_on_activity % self.test_data['activityName'],
                             locator_type="xpath")
        self.webDriver.click(element=self.locators.click_on_select, locator_type="xpath")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.booking_conflict,
                                                           locator_type="xpath"):
            raise Exception("conflict error message not displayed for sailor booking at sailor time and slot")

    def un_greet_greeted_sailor_from_history_page(self):
        """
        Function to un-greet greeted sailors for history page
        :return:
        """
        un_greet_element = self.webDriver.get_elements(element=self.locators.list_of_un_greet_elements, locator_type="xpath")
        for un_greet in range(1, len(un_greet_element)+1):
            self.webDriver.click(element=self.locators.un_greet_button % un_greet, locator_type="xpath")

    def checkin_again_from_sailor_details_page(self):
        """
        Function to check in the sailors who are unchecked from history page
        :return:
        """
        self.webDriver.click(element=self.locators.search_button, locator_type="xpath")
        self.webDriver.click(element=self.locators.tap_on_sailor, locator_type="xpath")
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        self.webDriver.set_context(contexts=self.webDriver.get_contexts(),
                                   context_name='WEBVIEW_com.decurtis.crew.embark')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.checkin_again, locator_type="xpath"):
            raise Exception("check In cta is not displayed after doing un check fro history page")
        self.webDriver.click(element=self.locators.checkin_again, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.greet_sailor, locator_type="xpath",
                                                      time_out=120)
        self.webDriver.click(element=self.locators.greet_sailor, locator_type="xpath")