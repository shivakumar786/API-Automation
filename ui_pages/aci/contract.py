__author__ = 'sarvesh.singh'

from virgin_utils import *


class Contract(General):
    """
    Page class for contract screen of ACI app
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
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "contract_status": "//*[@text='Cruise Contract']/following-sibling::android.widget.TextView",
                "sign_at_status": "//*[@text='Sign at Terminal / Sign Again']",
                "sign_status": "//*[@text='Sign Automatically']",
                "check_box": "com.decurtis.dxp.aci:id/party_check_box",
                "sign_again": "com.decurtis.dxp.aci:id/sign_again",
                "contract_tab": "//*[@text='CONTRACT']",
                "confirmation_popup": "com.decurtis.dxp.aci:id/confirmation_title",
                "confirmation_check_box": "com.decurtis.dxp.aci:id/contact_confirmation_checkbox",
                "confirmation_yes": "com.decurtis.dxp.aci:id/contract_confirmation_yes_button"

            })
        else:
            self.locators = self.dict_to_ns({
                "save_proceed": "//*[@text='AGREE & PROCEED']",
                "contract_status": "//*[@text='Cruise Contract']/following-sibling::android.widget.TextView",
                "sign_at_status": "//*[@text='Sign at Terminal / Sign Again']",
                "sign_status": "//*[@text='Sign Automatically']",
                "check_box": "com.decurtis.dxp.aci.dclnp:id/party_check_box",
                "sign_again": "com.decurtis.dxp.aci.dclnp:id/sign_again",
                "contract_tab": "//*[@text='CONTRACT']",
                "confirmation_popup": "com.decurtis.dxp.aci.dclnp:id/confirmation_title",
                "confirmation_check_box": "com.decurtis.dxp.aci.dclnp:id/contact_confirmation_checkbox",
                "confirmation_yes": "com.decurtis.dxp.aci.dclnp:id/contract_confirmation_yes_button",
            })

    def click_contract_tab(self):
        """
        Func to click on contract tab
        :return:
        """
        self.webDriver.click(element=self.locators.contract_tab, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_contract_tab_enabled(self):
        """
        Func to check if contract tab is enabled
        :return:
        """
        try:
            return self.webDriver.get_web_element(element=self.locators.contract_tab, locator_type='xpath'). \
                get_attribute("selected")
        except:
            return 'false'

    def click_save_proceed(self):
        """
        Func to click on save and proceed
        :return:
        """
        self.webDriver.click(element=self.locators.save_proceed, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.confirmation_popup, locator_type='id'):
            self.webDriver.click(element=self.locators.confirmation_check_box, locator_type='id')
            self.webDriver.wait_for(1)
            self.webDriver.click(element=self.locators.confirmation_yes, locator_type='id')

    def get_contract_status(self):
        """
        Func to get the contract status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.contract_status, locator_type='xpath').text

    def get_sign_at_status(self):
        """
        Func to get the sign at status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.sign_at_status, locator_type='xpath').get_attribute(
            "checked")

    def get_sign_status(self):
        """
        Func to get the sign status
        :return:
        """
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if self.webDriver.is_element_display_on_screen(element=self.locators.sign_status, locator_type='xpath'):
            return self.webDriver.get_web_element(element=self.locators.sign_status, locator_type='xpath').get_attribute(
                "checked")

    def update_digital_contract(self, count):
        """
        Func to update digital contract
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.sign_again, locator_type='id'):
            self.webDriver.click(element=self.locators.contract_status, locator_type='xpath')

        if self.get_contract_status() == 'Pending':
            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            self.webDriver.click(element=self.locators.sign_again, locator_type='id')
            if count > 1:
                if self.webDriver.is_element_display_on_screen(element=self.locators.check_box, locator_type='id'):
                    if not self.webDriver.get_web_element(element=self.locators.check_box, locator_type='id').get_attribute(
                            "checked"):
                        self.webDriver.click(element=self.locators.check_box, locator_type='id')
                    else:
                        self.webDriver.click(element=self.locators.sign_status, locator_type='xpath')
                else:
                    if self.get_sign_status() == 'false':
                        self.webDriver.click(element=self.locators.sign_status, locator_type='xpath')
            else:
                self.webDriver.click(element=self.locators.sign_status, locator_type='xpath')
