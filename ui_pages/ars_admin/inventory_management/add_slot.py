__author__ = 'Krishna'

from virgin_utils import *


class AddSlots(General):
    """
    To Initiate elements from add slots tab
    """

    def __init__(self, web_driver, test_data):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "today_cta": "//*[text()='Today']",
            "ok_btn": "//*[@id='_dialog_wrapper']/div/button[text()='OK']",
            "sell_ist": "//*[@class='e-schedule-table e-content-table']/tbody/tr/td[@class='e-work-cells']",
            "available_slots": "(//*[@class='e-schedule-table e-content-table']/tbody/tr/td[@class='e-work-cells'])[{}]",
            "save": "//*[text()='SAVE']",
            "cancel": "//*[text()='CANCEL']",
            "slot_time": "StartTime",
            "loader": "//div[@class='LoaderContainer__div']//img",
        })

    def select_today_date_from_add_slots_tab(self):
        """
        select today's date from add slots tab
        """
        self.webDriver.click(element=self.locators.today_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def select_slot(self):
        """
        select slot to add
        """
        sell_list = self.webDriver.get_elements(element=self.locators.sell_ist, locator_type="xpath")
        for sell_count in range(1, len(sell_list)):
            try:
                self.webDriver.move_to_element_and_double_click(
                    element=self.locators.available_slots.format(sell_count),
                    locator_type="xpath")
                self.webDriver.explicit_visibility_of_element(element=self.locators.ok_btn, locator_type="xpath",
                                                              time_out=60)
                self.test_data['newSlotTime'] = self.webDriver.get_attribute(element=self.locators.slot_time,
                                                                             locator_type="id", attribute_name="value")
                self.webDriver.click(element=self.locators.ok_btn, locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
                self.webDriver.click(element=self.locators.save, locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            except Exception:
                continue
