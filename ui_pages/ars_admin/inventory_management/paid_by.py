__author__ = 'Krishna'

from virgin_utils import *


class PaidBy(General):
    """
    To Initiate elements paid by page
    """

    def __init__(self, web_driver, test_data):
        """
        Initiate web_driver and elements of paid by page
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "paid_by_radio_button": "//div[@class='check ']",
            "pay_and_book_button": "//button[text()='Pay And Book']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "success_notification": "//div[@class='notification is-success']",
            "select_sailor": "(//*[text()='Please select the sailor paying for this booking']/../../following-sibling::div)[1]",
            "click_on_sailor_checkbox": "(//*[text()='%s'])[2]"
        })

    def select_sailor_to_pay_and_click_pay_and_book_cta(self):
        """
        get spa activity price while booking
        """
        sailor_name = self.webDriver.get_text(element=self.locators.select_sailor, locator_type="xpath")
        self.webDriver.click(element=self.locators.click_on_sailor_checkbox % sailor_name, locator_type="xpath")
        sailor_name = self.webDriver.click(element=self.locators.pay_and_book_button, locator_type="xpath")
        if self.webDriver.is_element_display_on_screen(element=self.locators.success_notification,
                                                       locator_type='xpath'):
            self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
            return True
        else:
            return False
