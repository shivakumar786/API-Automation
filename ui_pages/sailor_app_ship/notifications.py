__author__ = 'mohit.raghav'

from virgin_utils import *


class Notifications(General):
    """
    Page class for Notifications page in settings
    """
    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'reminder_toggle_off': "//div[@class='react-toggle react-toggle--focus Toggle']",
            'reminder_toggle_on': "//div[@class='react-toggle react-toggle--checked react-toggle--focus Toggle']",
            'loading': '//img[@alt="loading..."]',
            'notification_header': "//*[text()='Notifications']",
            'reminder_toggle': "//input[@id='reminderSetting']//preceding-sibling::div[@class='react-toggle-thumb']"
            })

    def disable_reminders(self):
        """
        Function to disable the Reminders toggle button
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.reminder_toggle,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.reminder_toggle, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.reminder_toggle_off,
                                                       locator_type='xpath'):
            logger.info("Reminders are turned off for this sailor")
        elif self.webDriver.is_element_display_on_screen(element=self.locators.reminder_toggle_on,
                                                         locator_type='xpath'):
            self.webDriver.click(element=self.locators.reminder_toggle, locator_type='xpath')
