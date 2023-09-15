__author__ = 'vishal'

from virgin_utils import *


class Visitor_details(General):
    """
    Page class for Visitor_details screen of Gangway app
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "unassign_card_button": "com.decurtis.dxp.gangway:id/assign_card",
            "visitor_history": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='History'']/android.widget.TextView,",
            "Visitor_add_info": "//androidx.appcompat.app.ActionBar.Tab[@content-desc='Additional Info']/android.widget.TextView",
            "alert_icon": "com.decurtis.dxp.gangway:id/alert",
        })

    def verify_unassign_card_button(self):
        """
        Verify the visitor unassign verify the cards.
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.unassign_card_button, locator_type='id',
                                                      time_out=20)
        return self.webDriver.is_element_enabled(element=self.locators.unassign_card_button, locator_type='id')

