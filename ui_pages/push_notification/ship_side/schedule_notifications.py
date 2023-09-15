__author__ = 'saloni.pattnaik'

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