__author__ = 'prahlad.sharma'

from virgin_utils import *


class Guest_details(General):
    """
    Page class for Guest_details screen of Gangway app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        self.locators = self.dict_to_ns({
            "down_arrow": "com.decurtis.dxp.gangway:id/arrow",
            "more_option": "//android.widget.ImageView[@content-desc='More options']",
            "create_alert": "//*[@text='Create Alert']",
            "create_message": "//*[@text='Create Message']",
            "alert_type_dd": "//*[@text='Alert Type']/../following-sibling::*[@class='android.widget.FrameLayout']",
            "department_dd": "//*[@text='Department']/../following-sibling::*[@class='android.widget.FrameLayout']",
            "select_value_dd": "//*[@class='android.widget.ListView']/*[@text='%s']",
            "description": "com.decurtis.dxp.gangway:id/description",
            "create": "com.decurtis.dxp.gangway:id/create",
            "cancel": "com.decurtis.dxp.gangway:id/cancel",
            "tabs": "//*[@class='androidx.appcompat.app.ActionBar$Tab']",
            "alert_message": "com.decurtis.dxp.gangway:id/alert_message",
            "alert_header": "//*[@text='Deny Onboard']",
            "no_records": "//*[@text='No Record(s) Available']",
            "message_body": "com.decurtis.dxp.gangway:id/message_body",
            "history_event_type": "com.decurtis.dxp.gangway:id/event_type",
            "additional_info": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='Additional Info']",
            "checkin_time": "com.decurtis.dxp.gangway:id/check_in_time",
            "onboard_time": "com.decurtis.dxp.gangway:id/onboard_time",
            "conflict_resolve_between": "com.decurtis.dxp.gangway:id/conflict_resolved_between",
            "sailor_image": "com.decurtis.dxp.gangway:id/person_photo",
            "zoom_image": "com.decurtis.dxp.gangway:id/zoom_image",
            "history": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='History']",
            "onboard_on_details": "com.decurtis.dxp.gangway:id/on_board",
            "ashore_on_details": "com.decurtis.dxp.gangway:id/ashore",
            "alert_icon": "com.decurtis.dxp.gangway:id/alert",
            "message_icon": "com.decurtis.dxp.gangway:id/message",
            "click_ok": "android:id/button1",
            "guest_details": "//*[@resource-id='com.decurtis.dxp.gangway:id/toolbar']//*[@class='android.widget.TextView']",
            "visitor_details": "//*[@text='Visitor Details']",
            "retake_image": "com.decurtis.dxp.gangway:id/retake",
            "allow": "com.android.packageinstaller:id/permission_allow_button",
            "while_using_app": "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            "image_capture": "com.decurtis.dxp.gangway:id/capture",
            "save_captured_image": "com.decurtis.dxp.gangway:id/crop_image_menu_crop",
            "boarding_status": "com.decurtis.dxp.gangway:id/boarding_status",
            "dob_key": "com.decurtis.dxp.gangway:id/label_date_of_birth",
            "embark_date_key": "com.decurtis.dxp.gangway:id/label_embark_date",
            "debark_date_key": "com.decurtis.dxp.gangway:id/label_debark_date",
            "checkintime_key": "com.decurtis.dxp.gangway:id/label_check_in_time",
            "onboard_time_key": "com.decurtis.dxp.gangway:id/label_onboard_time",
            "sepcial_needs_key": "com.decurtis.dxp.gangway:id/label_special_needs",
            "conflict_key": "com.decurtis.dxp.gangway:id/label_conflict_resolved_between",
            "all_tab": "androidx.appcompat.app.ActionBar$Tab",
            "alert_tab": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='%s']",
            "allow_button": "//*[@text='Allow']",
            "recent_arrow": "com.decurtis.dxp.gangway:id/arrow",
        })

    def click_on_down_arrow(self):
        """
        Function to click on down arrow
        """
        self.webDriver.click(element=self.locators.down_arrow, locator_type='id')

    def click_on_create_alert(self):
        """
        Function to click create alert
        """
        self.webDriver.click(element=self.locators.more_option, locator_type='xpath')
        self.webDriver.click(element=self.locators.create_alert, locator_type='xpath')

    def click_on_create_message(self):
        """
        Function to click create message
        """
        self.webDriver.click(element=self.locators.more_option, locator_type='xpath')
        self.webDriver.click(element=self.locators.create_message, locator_type='xpath')

    def fill_alert_and_save(self, alert_type, department, description):
        """
        Fill the alert info and save
        :param alert_type:
        :param department:
        :param description:
        """
        self.webDriver.click(element=self.locators.alert_type_dd, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_value_dd % alert_type, locator_type='xpath')
        self.webDriver.click(element=self.locators.department_dd, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_value_dd % department, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.description, locator_type='id', text=description)
        self.webDriver.mobile_native_back()
        self.webDriver.click(element=self.locators.create, locator_type='id')

    def fill_message_and_save(self, description):
        """
        Fill the message info and save
        :param description:
        """
        self.webDriver.set_text(element=self.locators.description, locator_type='id', text=description)
        self.webDriver.mobile_native_back()
        self.webDriver.click(element=self.locators.create, locator_type='id')

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

    def verify_created_alert_message(self, description, tabs, type):
        """
        Function to verify the alert and message
        :param description:
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
                all_alerts = self.webDriver.get_elements(element=self.locators.alert_message, locator_type='id')
            else:
                all_alerts = self.webDriver.get_elements(element=self.locators.message_body, locator_type='id')
            for alert in all_alerts:
                if alert.text == description:
                    return
                else:
                    count = int(count) - 1

    def verify_event_type(self, event_name, count):
        """
        Function to verify the event type in History
        :param event_name:
        :param count:
        """
        display_count = 0
        flag = True
        while flag:
            heading = self.get_alert_heading_in_history()
            if heading == event_name:
                display_count = display_count + 1
                self.webDriver.scroll_mobile(196, 1161, 199, 939)
                new_name = self.get_alert_heading_in_history()
                if new_name == heading:
                    flag = False
                    break
                else:
                    self.webDriver.scroll_mobile(196, 1161, 199, 939)
            else:
                self.webDriver.scroll_mobile(196, 1161, 199, 939)
                new_name = self.get_alert_heading_in_history()
                if new_name == heading:
                    flag = False
                    break
        assert count == display_count, f'For {event_name} event desired count is :{count} and available count is ' \
                                       f'{display_count}!!'

    def get_alert_heading_in_history(self):
        """
        Function to get the alert heading in History
        """
        heading = ''
        event_type = self.webDriver.get_elements(element=self.locators.history_event_type, locator_type='id')
        for event in event_type:
            heading = event.text
        return heading

    def click_additional_info(self):
        """
        Function to click on additional info
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.down_arrow, locator_type='id'):
            self.webDriver.click(element=self.locators.down_arrow, locator_type='id')
        self.webDriver.click(element=self.locators.history, locator_type='xpath')
        self.webDriver.click(element=self.locators.additional_info, locator_type='xpath')

    def verify_checkin_time_available(self):
        """
        To verify checkin time is available
        :return:
        """
        self.webDriver.scroll_mobile(769, 1174, 782, 888)
        checkin_time = self.webDriver.get_text(element=self.locators.checkin_time, locator_type='id')
        boarding_status_value = self.webDriver.get_text(element=self.locators.boarding_status, locator_type='id')

        if boarding_status_value.split('|')[0] == 'Not Checked-in':
            if checkin_time == 'N/A':
                logger.info(f"Check-in time Should be N/A in this case because Guest in not Checked in ")
            else:
                self.webDriver.allure_attach_jpeg("Check-in-time")
                raise Exception ("Check in time should be available but here its missing")
        elif boarding_status_value.find('Onboard') or boarding_status_value.find('Ashore'):
            self.webDriver.allure_attach_jpeg("Check-in-time")
            logger.info(f"Check-in time is available")
        else:
            logger.info(f"Check-in time is available and time is {checkin_time}")

    def verify_NA_availability(self):
        """
        To verify NA should be available
        :return:
        """
        self.webDriver.scroll_mobile(769, 1174, 782, 888)
        checkin_time = self.webDriver.get_text(element=self.locators.checkin_time, locator_type='id')
        onbaord_time = self.webDriver.get_text(element=self.locators.onboard_time, locator_type='id')
        conflict_resolve = self.webDriver.get_text(element=self.locators.conflict_resolve_between, locator_type='id')

        if checkin_time == 'N/A' or onbaord_time == 'N/A' or conflict_resolve == 'N/A':
            logger.info(f"NA is displayed when data is not available {checkin_time} ")
        else:
            self.webDriver.allure_attach_jpeg("NA_unavailable")
            raise Exception("NA not display")

    def verify_fields_on_additional_info_tab(self):
        """
        To verify the fields on additional tabs
        :return:
        """
        self.webDriver.wait_for(3)
        dob = self.webDriver.is_element_display_on_screen(element=self.locators.dob_key, locator_type='id')
        embark_date = self.webDriver.is_element_display_on_screen(element=self.locators.embark_date_key,
                                                                  locator_type='id')
        debark_date = self.webDriver.is_element_display_on_screen(element=self.locators.debark_date_key,
                                                                  locator_type='id')
        checkintime = self.webDriver.is_element_display_on_screen(element=self.locators.checkintime_key,
                                                                  locator_type='id')
        self.webDriver.allure_attach_jpeg("additional_info_1")
        self.webDriver.scroll_mobile(575, 1208, 532, 955)
        onboard_time = self.webDriver.is_element_display_on_screen(element=self.locators.onboard_time_key,
                                                                   locator_type='id')
        special_needs = self.webDriver.is_element_display_on_screen(element=self.locators.sepcial_needs_key,
                                                                    locator_type='id')
        conflict_key = self.webDriver.is_element_display_on_screen(element=self.locators.conflict_key,
                                                                   locator_type='id')
        if dob and embark_date and debark_date and checkintime and onboard_time and special_needs and conflict_key:
            logger.info("All the required field available in Additional Info tab")
        else:
            self.webDriver.allure_attach_jpeg("additional_info_error")
            raise Exception("Required field not available")

    def verify_fields_on_additional_info_tab_vv(self):
        """
        To verify the fields on additional tabs for vv
        :return:
        """
        self.webDriver.wait_for(3)
        dob = self.webDriver.is_element_display_on_screen(element=self.locators.dob_key, locator_type='id')
        embark_date = self.webDriver.is_element_display_on_screen(element=self.locators.embark_date_key,
                                                                  locator_type='id')
        debark_date = self.webDriver.is_element_display_on_screen(element=self.locators.debark_date_key,
                                                                  locator_type='id')
        checkintime = self.webDriver.is_element_display_on_screen(element=self.locators.checkintime_key,
                                                                  locator_type='id')
        self.webDriver.allure_attach_jpeg("additional_info_1")
        self.webDriver.click(element=self.locators.recent_arrow, locator_type='id')
        self.webDriver.scroll_mobile(1440, 2194, 1440, 1615)
        onboard_time = self.webDriver.is_element_display_on_screen(element=self.locators.onboard_time_key,
                                                                   locator_type='id')
        special_needs = self.webDriver.is_element_display_on_screen(element=self.locators.sepcial_needs_key,
                                                                    locator_type='id')
        conflict_key = self.webDriver.is_element_display_on_screen(element=self.locators.conflict_key,
                                                                   locator_type='id')
        if dob and embark_date and debark_date and checkintime and onboard_time and special_needs and conflict_key:
            logger.info("All the required field available in Additional Info tab")
        else:
            self.webDriver.allure_attach_jpeg("additional_info_error")
            raise Exception("Required field not available")

    def verify_fields_on_additional_info_tab_vv(self):
        """
        To verify the fields on additional tabs for vv
        :return:
        """
        self.webDriver.wait_for(3)
        dob = self.webDriver.is_element_display_on_screen(element=self.locators.dob_key, locator_type='id')
        embark_date = self.webDriver.is_element_display_on_screen(element=self.locators.embark_date_key,
                                                                  locator_type='id')
        debark_date = self.webDriver.is_element_display_on_screen(element=self.locators.debark_date_key,
                                                                  locator_type='id')
        checkintime = self.webDriver.is_element_display_on_screen(element=self.locators.checkintime_key,
                                                                  locator_type='id')
        self.webDriver.allure_attach_jpeg("additional_info_1")
        self.webDriver.click(element=self.locators.recent_arrow, locator_type='id')
        self.webDriver.scroll_mobile(1440, 2194, 1440, 1615)
        onboard_time = self.webDriver.is_element_display_on_screen(element=self.locators.onboard_time_key,
                                                                   locator_type='id')
        special_needs = self.webDriver.is_element_display_on_screen(element=self.locators.sepcial_needs_key,
                                                                    locator_type='id')
        conflict_key = self.webDriver.is_element_display_on_screen(element=self.locators.conflict_key,
                                                                   locator_type='id')
        if dob and embark_date and debark_date and checkintime and onboard_time and special_needs and conflict_key:
            logger.info("All the required field available in Additional Info tab")
        else:
            self.webDriver.allure_attach_jpeg("additional_info_error")
            raise Exception("Required field not available")


    def click_sailor_image(self):
        """
        Function to click on sailor image
        :return:
        """
        self.webDriver.click(element=self.locators.sailor_image, locator_type='id')

    def verify_zoom_image_availability(self):
        """
        Function to check the image zoom or not
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.zoom_image, locator_type='id', time_out=10)
        if self.webDriver.is_element_display_on_screen(element=self.locators.zoom_image, locator_type='id'):
            self.webDriver.screen_shot("zoomed_image")
            pass
        else:
            self.webDriver.screen_shot("error_zoomed_image")
            raise Exception("image not zoomed and giving error")

    def click_onboard_on_details(self):
        """
        Function to click on on-board button on details page
        """
        self.webDriver.click(element=self.locators.onboard_on_details, locator_type='xpath')

    def verify_alert_icon_detail_page(self):
        """
        Verify the alert icon on guest detail page
        """
        elements = self.webDriver.is_element_display_on_screen(element=self.locators.alert_icon, locator_type='id')
        if elements:
            return self.webDriver.get_text(element=self.locators.alert_icon, locator_type='id')
        else:
            self.webDriver.screen_shot("alert_icon_details_page_error")
            raise Exception("Alert Icon is not visible on Guest detail page")

    def verify_message_icon_detail_page(self):
        """
        Verify the alert icon on guest detail page
        """
        elements = self.webDriver.is_element_display_on_screen(element=self.locators.message_icon, locator_type='id')
        if elements:
            return self.webDriver.get_text(element=self.locators.message_icon, locator_type='id')
        else:
            raise Exception("Message Icon is not visible on Guest detail page")

    def verify_acknowledge_message(self):
        """
        Verify the Acknowledgment message
        """
        elements = self.webDriver.is_element_display_on_screen(element=self.locators.message_icon, locator_type='id')
        if elements:
            raise Exception("Message Icon is visible when we already acknowledge the message")

    def click_crew_ok(self):
        """
        Click on OK when we create
        """
        self.webDriver.click(element=self.locators.click_ok, locator_type='id')

    def availability_of_details_page(self):
        """
        Check the availability of Details Page
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.guest_details, locator_type='xpath'):
            self.webDriver.screen_shot("Details_page")
            pass
        else:
            self.webDriver.screen_shot("Details_page_image")
            raise Exception("Guest Details page not open and giving error")

    def availability_of_visitor_details_page(self):
        """
        Check the availability of Visitor Details Page
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_details, locator_type='xpath'):
            self.webDriver.screen_shot("Details_page")
            pass
        else:
            self.webDriver.screen_shot("Details_page_image")
            raise Exception("Visitor Details page not open and giving error")

    def retake_image_functionality(self):
        """
        Function to check the image functionality
        :return:
        """
        self.webDriver.screen_shot("before_image_capture")
        self.webDriver.click(element=self.locators.retake_image, locator_type='id')
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.while_using_app, locator_type='id'):
            self.webDriver.click(element=self.locators.while_using_app, locator_type='id')
            self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_button, locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.image_capture, locator_type='id')
        self.webDriver.click(element=self.locators.save_captured_image, locator_type='id')
        self.webDriver.wait_for(5)
        self.webDriver.screen_shot("after_image_capture")

    def verify_alert_tab_selected(self):
        """
        Function to check the Tab value in Details page
        :return:
        """
        tab_heading = ''
        all_tabs = self.webDriver.get_elements(element=self.locators.all_tab, locator_type='class')
        for tab in all_tabs:
            tab_heading = tab.tag_name
            if 'Alert' in tab_heading:
                break
        if self.webDriver.get_attribute(element=self.locators.alert_tab % tab_heading, locator_type='xpath',
                                        attribute_name='selected') and int(tab_heading.split(' ')[1].split('(')[1]
                                                                                              .split(')')[0]) > 0:
            logger.info("Alert tab is selected by default")
        else:
            raise Exception("Alert tab is not highlighted after open the details page")
