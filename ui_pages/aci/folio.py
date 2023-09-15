__author__ = 'sarvesh.singh'

from virgin_utils import *


class Folio(General):
    """
    Page class for folio screen of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "folio": "//*[@text='FOLIO']",
                "payment_status": "//*[@text='Payment Information']/following-sibling::android.widget.TextView",
                "cash": "//*[@text='Cash']",
                "cash_checkbox": "//*[@text='Cash letter given to Sailor']",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "payment": "//*[@text='Payment Information']",
            })
        else:
            self.locators = self.dict_to_ns({
                "folio": "//*[@text='PAYMENT']",
                "payment_status": "//*[@text='Payment Information']/following-sibling::android.widget.TextView",
                "cash": "//*[@text='Cash']",
                "cash_checkbox": "//*[@text='Refer Guest to Navigator App']",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "payment": "//*[@text='Payment Information']",
            })

    def click_folio_tab(self):
        """
        Func to click on folio tab
        :return:
        """
        self.webDriver.click(element=self.locators.folio, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_folio_tab_enabled(self):
        """
        Func to check if folio tab is enabled
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.folio, locator_type='xpath'):
            return self.webDriver.get_web_element(element=self.locators.folio, locator_type='xpath').get_attribute(
                "selected")
        else:
            return 'false'

    def click_save_proceed(self):
        """
        Func to click on save and proceed
        :return:
        """
        self.webDriver.click(element=self.locators.save_proceed, locator_type='xpath')
        self.webDriver.wait_for(2)

    def get_payment_status(self):
        """
        Func to get the payment status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.payment_status, locator_type='xpath').text

    def get_payment_checked_status(self):
        """
        Func to get the payment checked status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.cash_checkbox, locator_type='xpath').get_attribute(
            "checked")

    def update_payment_information(self):
        """
        Func to update payment information
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.cash, locator_type='xpath'):
            self.webDriver.click(element=self.locators.payment, locator_type='xpath')
        if self.get_payment_status() == 'Pending':
            self.webDriver.click(element=self.locators.cash, locator_type='xpath')
            if self.get_payment_checked_status() == 'false':
                self.webDriver.click(element=self.locators.cash_checkbox, locator_type='xpath')
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            self.webDriver.wait_for(1)
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

