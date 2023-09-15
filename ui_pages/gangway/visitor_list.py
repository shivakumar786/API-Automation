__author__ = 'vishal'

from virgin_utils import *


class Visitor_list(General):
    """
    Page class for Visitor_list screen of Gangway app
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "tittle_name": "//*[@class='android.widget.TextView']",
        })

    def tab_tittle_name(self):
        """
        verify the tab tittle name
        """
        return self.webDriver.get_text(element=self.locators.tittle_name, locator_type='xpath')
