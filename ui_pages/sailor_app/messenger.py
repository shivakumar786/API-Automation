__author__ = 'vanshika.arora'

from virgin_utils import *


class Messenger(General):
    """
    Page class for Messenger page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "notification_header": "//h2[text()='Notifications']",
            "notification_title": "//div[@class='NotificationsCard__title']",
            "notification_body": "//div[@class='NotificationsCard__body']",
            "no_unread_notification": "//div[@class='NotificationsCard__unread-message']",
            "notification_center_header": "//div[@class='NotificationsCenter__header']",
            "notification_settings_button": "//button[@id='notificationsSettingsButton']",
            "cross_icon":"//button[@id='back-close-btn']",
            "contacts": "//button[@id='aFriendButton']",
            "reminders": "//div[@class='react-toggle-track']",
            "notification_card": "//div[@class='NotificationsCard']",

        })

    def verify_user_landed_on_messenger_screen(self):
        """
        Function to verify that user has landed on guides page
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.notification_header, locator_type='xpath'):
            logger.debug("User has landed on messenger screen")
        else:
            raise Exception("User has not landed on messenger screen")

    def verify_default_notification_text(self):
        """
        Function to verify default notification text
        """
        notification_title = self.webDriver.get_text(element=self.locators.notification_title, locator_type='xpath')
        notification_body = self.webDriver.get_text(element=self.locators.notification_body, locator_type='xpath')
        no_unread_text = self.webDriver.get_text(element=self.locators.no_unread_notification, locator_type='xpath')
        assert notification_title == "Ahoy there!","Incorrect notification title is shown"
        assert notification_body == "Here's where you can stay up to date on all your relevant notifications and reminders.", "Incorrect notification body is shown"
        assert no_unread_text == "No unread notifications", "Incorrect unread notification text shown"

    def click_notification_card(self):
        """
        Function to click notification card in order to open notification settings
        """
        self.webDriver.click(element=self.locators.notification_body, locator_type='xpath')

    def verify_user_landed_on_notification_listing_screen(self):
        """
        Function to verify user landed on notification listing screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.notification_center_header, locator_type='xpath'):
            logger.debug("User has landed on notification center")
        else:
            raise Exception("User has not landed on notification center")

    def open_notification_settings(self):
        """
        Function to open notification settings
        """
        self.webDriver.click(element=self.locators.notification_settings_button, locator_type='xpath')

    def click_cross_icon(self):
        """
        Function to open cross icon
        """
        self.webDriver.click(element=self.locators.cross_icon, locator_type='xpath')

    def open_contacts(self):
        """
        Function to open contacts
        """
        self.webDriver.click(element=self.locators.contacts, locator_type='xpath')

    def turn_reminders_off(self):
        """
        Function to turn reminders off
        :return:
        """
        self.webDriver.click(element=self.locators.reminders, locator_type='xpath')

    def turn_reminders_on(self):
        """
        Function to turn reminders on
        :return:
        """
        self.webDriver.click(element=self.locators.reminders, locator_type='xpath')






