__author__ = 'HT'

from selenium.webdriver.common.keys import Keys
import string
from virgin_utils import *


class ArsSettings(General):
    """
    ARS Admin Settings Page
    """

    def __init__(self, web_driver):
        """
        initiate settings page elements
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "settings_page_header": "(//*[text()='Settings'])[3]",
            "settings_dropdown": "//*[@id='settingOption']/div/div/div",
            "ship_board_radio_btn": "//*[text()='Shipboard']",
            "shore_side_radio_btn": "//*[text()='Shore Side']",
            "edit_cta": "//*[text()='EDIT']",
            "delete_cta": "//*[text()='DELETE']",
            "template_notification": "//*[text()='Notification Templates']",
            "new_template_notification": "//*[text()='New Notification Template']",
            "meeting_location": "//*[text()='Activity/Meeting Location']",
            "new_meeting_location": "//*[text()='New Activity/Meeting Location']",
            "loader": "//div[@id='Spinner']",
            "message_title": "//*[text()='Message Title']/../input",
            "message": "//*[text()='Message']/../textarea",
            "url": "//*[text()='URL']/../input",
            "create": "//*[text()='Create']",
            "update": "//*[text()='Update']",
            "get_updated_message": "//*[text()='Message: ']/../span",
            "get_notification_title": "//*[text()='Title: ']/../span",
            "success_notification": "//div[@class='notification is-success']",
            "new_location_name": "//*[text()='Activity Location Name']/../input",
            "newly_created_location_name": "//*[text()='Name: ']/../span"
        })

    def click_on_meeting_location(self):
        """
        function to select meeting location from dropdown
        :return:
        """
        self.webDriver.click(element=self.locators.settings_dropdown, locator_type="xpath")
        self.webDriver.click(element=self.locators.meeting_location, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=180)
    def click_on_notification_template(self):
        """
        function to select notification template from dropdown
        :return:
        """
        self.webDriver.click(element=self.locators.settings_dropdown, locator_type="xpath")
        self.webDriver.click(element=self.locators.template_notification, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=180)

    def verify_settings_page_elements(self):
        """
        To Verify user is successfully verified all the elements on settings screen
        """
        header_name = self.webDriver.get_text(element=self.locators.settings_page_header, locator_type="xpath")
        assert header_name == "Settings", "Settings page header is not visible on screen"
        status = self.webDriver.is_element_display_on_screen(element=self.locators.new_template_notification,
                                                             locator_type="xpath")
        assert status, "new notification template cta is not visible on screen"
        self.click_on_meeting_location()
        status = self.webDriver.is_element_display_on_screen(element=self.locators.new_meeting_location,
                                                             locator_type="xpath")
        assert status, "new meeting location cta is not visible on screen"
        ship_toggle = self.webDriver.is_element_display_on_screen(element=self.locators.ship_board_radio_btn,
                                                                  locator_type="xpath")
        assert ship_toggle, "ship side toggle button is not visible on screen"
        shore_toggle = self.webDriver.is_element_display_on_screen(element=self.locators.shore_side_radio_btn,
                                                                   locator_type="xpath")
        assert shore_toggle, "shore side toggle button is not visible on screen"
        self.click_on_notification_template()

    def create_new_notification_template(self):
        """
        function to create new notification template from settings page
        :return:
        """
        self.webDriver.click(element=self.locators.new_template_notification, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.set_text(element=self.locators.message_title, locator_type="xpath", text="AAAAAANewNT")
        message = "new notification template created from UI automation for testing"
        self.webDriver.set_text(element=self.locators.message, locator_type="xpath", text=message)
        url = "https://application-integration.ship.virginvoyages.com/activityReservationCrew/settings"
        self.webDriver.set_text(element=self.locators.url, locator_type="xpath", text=url)
        self.webDriver.click(element=self.locators.create, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        create_notification_title = self.webDriver.get_text(element=self.locators.get_notification_title,
                                                            locator_type="xpath")
        assert create_notification_title == "AAAAAANewNT", "newly created notification does not exist in list"

    def edit_newly_created_notification_template(self):
        """
        Function to edit newly created notification template
        :return:
        """
        self.webDriver.click(element=self.locators.edit_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        letters = string.ascii_lowercase
        updated_message = ''.join(random.choice(letters) for i in range(10))
        self.webDriver.clear_text(element=self.locators.message, locator_type="xpath", action_type="clear")
        self.webDriver.set_text(element=self.locators.message, locator_type="xpath", text=updated_message)
        self.webDriver.click(element=self.locators.update, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        updated_message = self.webDriver.get_text(element=self.locators.get_updated_message, locator_type="xpath")
        assert updated_message == updated_message, "Failed to Edit the notification template"

    def delete_created_notification_template(self):
        """
        function to delete the newly created notification template
        :return:
        """
        self.webDriver.click(element=self.locators.delete_cta, locator_type="xpath")
        success_message = self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")
        assert success_message == "Notification Template deleted successfully", "Notificatio template does not " \
                                                                                "deleted succesfullyy "
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def create_new_meeting_location(self):
        """
        Function to create new meeting location from settings page
        :return:
        """
        self.click_on_meeting_location()
        self.webDriver.click(element=self.locators.new_meeting_location, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.set_text(element=self.locators.new_location_name, locator_type="xpath",
                                text="AAA_new_meeting_location")
        self.webDriver.click(element=self.locators.create, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        new_location = self.webDriver.get_text(element=self.locators.newly_created_location_name, locator_type="xpath")
        assert new_location == "AAA_new_meeting_location", "new location not created successfully"

    def edit_newly_created_meeting_location(self):
        """
        Function to edit newly created meeting location
        :return:
        """
        self.webDriver.click(element=self.locators.edit_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        letters = string.ascii_lowercase
        location = ''.join(random.choice(letters) for i in range(10))
        updated_location_name = f"aaaaaa_{location}"
        self.webDriver.clear_text(element=self.locators.new_location_name, locator_type="xpath", action_type="clear")
        self.webDriver.set_text(element=self.locators.new_location_name, locator_type="xpath",
                                text=updated_location_name)
        self.webDriver.click(element=self.locators.update, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        new_location = self.webDriver.get_text(element=self.locators.newly_created_location_name, locator_type="xpath")
        assert new_location == updated_location_name, "new location not updated successfully"

    def delete_newly_created_meeting_location(self):
        """
        Function to delete newly created meeting location
        :return:
        """
        self.webDriver.click(element=self.locators.delete_cta, locator_type="xpath")
        success_message = self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")
        assert success_message == "Activity/Meeting Location deleted successfully", "Meeting Location does not " \
                                                                                    "deleted succesfullyy "
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
