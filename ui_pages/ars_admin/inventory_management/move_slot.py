__author__ = 'Krishna'

from virgin_utils import *


class MoveSlot(General):
    """
    To Initiate elements from Move slot tab
    """

    def __init__(self, web_driver):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "date_picker": "//*[text()='Date']/following-sibling::span",
            "placeholder_time": "//*[@class='react-datepicker-time__input']/input[@placeholder='Time']",
            "override_all_move": "//*[contains(text(),'OVERRIDE ALL & MOVE')]",
            "move": "//*[contains(text(),'MOVE')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
        })

    def select_date_and_move_slot(self):
        """
        select date or time to move the slot
        """
        self.webDriver.click(element=self.locators.date_picker, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.placeholder_time,
                                                          locator_type="xpath", text=10)
        try:
            self.webDriver.click(element=self.locators.move, locator_type="xpath")
        except Exception:
            self.webDriver.click(element=self.locators.override_all_move, locator_type="xpath")
