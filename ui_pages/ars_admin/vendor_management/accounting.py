__author__ = 'HT'

from selenium.webdriver.common.keys import Keys
from virgin_utils import *


class ArsAccounting(General):
    """
    ARS Admin Accounting Page
    """

    def __init__(self, web_driver):
        """
        initiate Accounting page elements
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "accounting_page_header": "(//*[text()='Accounting'])[2]",
            "loader": "//div[@id='Spinner']",
            "filter_icon": "//*[text()='Accounting']/../div/div",
            "actions": "//*[text()='Actions']",
            "edit": "//*[text()='Edit']",
            "activity_checkbox": "(//*[@class='Accounting_column']/span/label)[2]",
            "prepaid_refund": "//*[@name='_prepaid refund']",
            "booking": "//*[@name='_booking']",
            "full_refund": "//*[@name='_full refund']",
            "partial_refund": "//*[@name='_partial refund']",
            "update": "//*[text()='Update']",
            "success_notification": "//div[@class='notification is-success']",
        })

    def verify_accounting_tab_elements(self):
        """
        function to select meeting location from dropdown
        :return:
        """
        account_header = self.webDriver.get_text(element=self.locators.accounting_page_header, locator_type="xpath")
        assert account_header == "Accounting", "failed to access accounting tab"
        status = self.webDriver.is_element_display_on_screen(element=self.locators.filter_icon, locator_type="xpath")
        assert status, "Filer icon not displayed on accounting tab"
        status = self.webDriver.is_element_display_on_screen(element=self.locators.actions, locator_type="xpath")
        assert status, "actions drop down not displayed on accounting screen"

    def edit_quick_code_from_accounting_tab(self):
        """
        Function to edit charge ID from accounting tab
        :return:
        """
        self.webDriver.click(element=self.locators.activity_checkbox, locator_type="xpath")
        self.webDriver.click(element=self.locators.actions, locator_type="xpath")
        self.webDriver.click(element=self.locators.edit, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.prepaid_refund, locator_type="xpath", text="94004")
        self.webDriver.set_text(element=self.locators.booking, locator_type="xpath", text="94001")
        self.webDriver.set_text(element=self.locators.full_refund, locator_type="xpath", text="94001")
        self.webDriver.set_text(element=self.locators.partial_refund, locator_type="xpath", text="94005")
        self.webDriver.click(element=self.locators.update, locator_type="xpath")
        success_message = self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")
        assert success_message == "Quick code of activities updated successfully", "Quick code not updated successfully"
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
