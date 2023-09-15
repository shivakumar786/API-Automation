__author__ = 'vanshika.arora'

from virgin_utils import *


class Payment(General):
    """
    Page class for summary screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "full_name": "//input[@id='ccFullName']",
            "cc_number": "//input[@id='ccCardNumber']",
            "cc_month": "//input[@id='ccExpMonth']",
            "month_text": "//*[@text='%s']",
            "cc_expiry_date": "//input[@id='ccExpiryDate']",
            "cc_year": "//input[@id='ccMaxAllowedYear']",
            "year_text": "//*[@text='%s']",
            "cc_cvv": "//input[@id='ccCVV']",
            "billing_address_pincode": "billingAddressPinCode",
            "save_card": "//*[text()='Save card (overwrite any existing cards)']",
            "pay_and_continue": "submitHppPaymentForm",
            "add_card_button": "//button[@id='addCardButton']",
            "cc_Expiry_Date": "//input[@id='ccExpiryDate']",
            "forward_submit_arrow": "//div[@id='forward-submit-arrow']",
            "loader": "//div[@class='loader-wrapper']",
            "get_credit_card_number" : "//div[@class='CreditCardComponent__number-wrap']/div[2]",
            "get_credit_card_name": "//div[@class='CreditCardComponent__holder-name']",
            "get_credit_card_expiry_date": "//div[@class='CreditCardComponent__expiry']/div[2]",
            "back_button": "//button[@id='BackButton']",
            "payment_page_title": "//h1[text()='Your payment method']",
            "rts_payment_page_title": "//h1[text()='Payment method']",
            "enter_card_details_title": "//span[text()='Enter card details']",
            "card_payment_confirm_button": "//button[@id=cardPaymentConfirmButton']",
            "rts_cc_number": "//input[@id='cardNumberInput']",
            "rts_cc_name": "//input[@id='nameOnCardInput']",
            "rts_exp_date": "//input[@id='expDateInput']",
            "payment_method_header": "//h1[text()='Payment method']",
            "delete_card_button": "//button[@id='PaymentCardInfoDelete']",
            "confirm_delete_card_button": "//button[@id='PaymentCardModalSkip']",
            "click_back_button": "//span[text()='Enter card details']",
            "payment_iframe": "//iframe[@id='payment_iFrame']"
            })

    def verify_enter_card_details_page_available(self):
        """
        Function to verify that user has landed on enter card details page
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.payment_iframe, locator_type='xpath', time_out=60)
        self.webDriver.switch_to_iframe(self.webDriver.get_web_element(element=self.locators.payment_iframe, locator_type='xpath'))
        self.webDriver.explicit_visibility_of_element(element=self.locators.enter_card_details_title, locator_type='xpath'
                                                      , time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.enter_card_details_title, locator_type='xpath'):
            logger.debug("Enter card details title is available on screen")
        else:
            raise Exception("Enter card details title is not available on screen")

    def click_addcard_button(self):
        """
        Function to click add card button
        :return:
        """
        self.webDriver.click(element=self.locators.add_card_button, locator_type='xpath')

    def fill_card_and_pay_for_shore_things(self, test_data):
        """
        To fill payment card details
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.set_text(element=self.locators.full_name, locator_type='id', text='Vanshika Arora')
        self.webDriver.set_text(element=self.locators.cc_number, locator_type='id', text='4111111111111111')
        self.webDriver.set_text(element=self.locators.cc_Expiry_Date, locator_type='xpath', text='1225')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_text(element=self.locators.cc_cvv, locator_type='id', text='123')
        self.webDriver.set_text(element=self.locators.billing_address_pincode, locator_type='id', text='302021')
        self.webDriver.click(element=self.locators.save_card, locator_type='id')
        self.webDriver.click(element=self.locators.pay_and_continue, locator_type='id')

    def fill_payment_card_details(self, guest_data):
        """
        To fill payment card details
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.set_text(element=self.locators.cc_number, locator_type='xpath', text='4111111111111111')
        self.webDriver.set_text(element=self.locators.full_name, locator_type='xpath', text='Vanshika Arora')
        self.webDriver.click(element=self.locators.cc_month, locator_type='xpath')
        if self.webDriver.is_element_enabled(element=self.locators.forward_submit_arrow, locator_type='xpath'):
            logger.debug("User is able to click on forward submit arrow after entering all required card details")
            self.webDriver.click(element=self.locators.forward_submit_arrow, locator_type='xpath')
        else:
            raise Exception("Next button is not enabled after filling all required details")
        self.webDriver.set_text(element=self.locators.cc_cvv, locator_type='xpath', text='123')
        if self.webDriver.is_element_enabled(element=self.locators.forward_submit_arrow, locator_type='xpath'):
            logger.debug("User is able to click on forward submit arrow after entering all required card details")
            self.webDriver.set_text(element=self.locators.billing_address_pincode, locator_type='xpath', text='302021')
            self.webDriver.click(element=self.locators.forward_submit_arrow, locator_type='xpath')
        else:
            logger.debug("Reminders are disabled after disabled by sailor")
        self.webDriver.click(element=self.locators.forward_submit_arrow, locator_type='xpath')

    def verify_card_saved(self, guest_data):
        """
        Function to verify saved card
        :param guest_data:
        :return:
        """
        self.webDriver.wait_till_element_invisible(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.payment_page_title,
                                                          locator_type='xpath')
        card_number = self.webDriver.get_text(element=self.locators.get_credit_card_number, locator_type='xpath')
        cc_name = self.webDriver.get_text(element=self.locators.get_credit_card_name, locator_type='xpath')
        cc_exp_date = self.webDriver.get_text(element=self.locators.get_credit_card_expiry_date, locator_type='xpath')
        assert card_number =="411111******1111", "Correct card number is shown in saved card"
        assert cc_name == "Vanshika Arora", "Correct name is shown on saved cc"
        assert cc_exp_date == "12/25", "Correct expiry date is shown on credit card"

    def click_card_payment_confirm_button(self):
        """
        Function to click card payment confirmation button
        """
        self.webDriver.click(element=self.locators.card_payment_confirm_button, locator_type='id')

    def click_back_button(self):
        """
        Function to click back button
        :return:
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='id')

    def verify_card_details(self):
        """
        Function to verify card details
        :return:
        """
        self.webDriver.wait_till_element_invisible(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.rts_payment_page_title,
                                                          locator_type='xpath')
        card_number = self.webDriver.get_text(element=self.locators.rts_cc_number, locator_type='xpath')
        cc_name = self.webDriver.get_text(element=self.locators.rts_cc_name, locator_type='xpath')
        cc_exp_date = self.webDriver.get_text(element=self.locators.rts_exp_date, locator_type='xpath')
        assert card_number == "4111 11** **** 1111", "Correct card number is shown in saved card"
        assert cc_name == "Vanshika Arora", "Correct name is shown on saved cc"
        assert cc_exp_date == "12/25", "Correct expiry date is shown on credit card"

    def verify_availability_of_payment_method_header(self):
        """
        Function to verify availability of payment method header
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_method_header,
                                                       locator_type='xpath'):
            logger.debug("Enter card details title is available on screen")
        else:
            raise Exception("Enter card details title is not available on screen")

    def delete_card(self):
        """"
        Function to delete credit card
        :return:
        """
        self.webDriver.click(element=self.locators.delete_card_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.confirm_delete_card_button, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
