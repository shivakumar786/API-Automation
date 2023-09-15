__author__ = 'aatir.fayyaz'

from virgin_utils import *


class ScheduleNotifications(General):
    """
    Page Class for Push Notification schedule notifications page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of schedule notifications page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h6[contains(text(),'Push Notifications')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "tabs": "//span[text()='%s']",
            "notification_count": "//div[@class='MuiCardContent-root']/h3",
            "schedule_count": "//h6[text()='Scheduled']/../..//div[@class='MuiCardContent-root']/h3 ",
            "send_now": "(// span[text() = 'SEND NOW'])[2]",
            "card": "//span[text()='%s']"
        })

    def click_on_tabs_from_dashboard(self, tab_name):
        """
        To click on tabs from the dashboard
        :param tab_name:
        """
        self.webDriver.scroll_complete_page_top()
        self.webDriver.click(element=self.locators.tabs % tab_name, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def wait_for_loader_to_complete(self):
        """
        Function to wait for page loading to complete
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=160)

    def send_now(self, tab_name):
        """
        To click on tabs from the dashboard
        :param tab_name:
        """
        self.webDriver.click(element=self.locators.tabs % tab_name, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.send_now, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.wait_for(2)

    def verify_notification_card(self, test_data):
        """
        To verify an indication on the scheduled notification card that the specific notification is
        recurring - weekly/daily
        :param test_data:
        """
        slab = test_data['recurring'] + " Recurring Notification"
        slab_low = test_data['recurring'].lower() + " Recurring Notification"
        self.webDriver.scroll_till_element(element=self.locators.card % slab_low, locator_type='xpath')
        notification_list = self.webDriver.get_elements(element=self.locators.card % slab_low, locator_type='xpath')
        for name in notification_list:
            if name.text == slab:
                return True
            else:
                raise Exception('Incorrect indication on the scheduled notification card')
