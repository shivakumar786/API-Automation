__author__ = 'sarvesh.singh'

from virgin_utils import *


class Payment(General):
    """
    Page class for Payment Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = {
            "fullPay": "//button[@class='btn btn-secondary paymentOptionSelect']",
            "paymentIframe": "paymentIframe",
            "fullName": "//*[@id='ccFullName']",
            "cardNumber": "//*[@id='ccCardNumber']",
            "expMonth": "//*[@id='ccExpMonth']",
            "expYear": "//*[@id='ccExpYear']",
            "cvv": "//*[@id='ccCVV']",
            "street": "//*[@id='billingAddressStreet']",
            "city": "//*[@id='billingAddressCity']",
            "state": "//*[@id='billingAddressState']",
            "zipCode": "//*[@id='billingAddressZipCode']",
            "agreeTerms": "//label[@id='chkTermsAndConditions-label']",
            "payContinue": "//*[@id='submitHppPaymentForm']",
        }

    def select_full_pay(self):
        """

        :return:
        """
        self.webDriver.click(element=self.locators['fullPay'], locator_type='xpath')
        self.webDriver.wait_for(seconds=20)

    def fill_payment_details(self):
        """

        :return:
        """
        self.webDriver.switch_to_iframe(frame_reference=self.locators['paymentIframe'])
        self.webDriver.set_text(element=self.locators['fullName'], locator_type='xpath',
                                text=f'{generate_first_name()} {generate_last_name()}')
        self.webDriver.set_text(element=self.locators['cardNumber'], locator_type='xpath', text='4111 1111 1111 1111')
        self.webDriver.select_by_text(element=self.locators['expMonth'], locator_type='xpath', text='JAN')
        self.webDriver.select_by_text(element=self.locators['expYear'], locator_type='xpath', text='2023')
        self.webDriver.set_text(element=self.locators['cvv'], locator_type='xpath', text='123')
        self.webDriver.set_text(element=self.locators['street'], locator_type='xpath', text='42 baker street')
        self.webDriver.set_text(element=self.locators['city'], locator_type='xpath', text='Jaipur')
        self.webDriver.select_by_text(element=self.locators['state'], locator_type='xpath', text='Andhra Pradesh')
        self.webDriver.set_text(element=self.locators['zipCode'], locator_type='xpath', text='321001')
        self.webDriver.switch_to_default_content()
        self.webDriver.scroll_complete_page()
        self.webDriver.switch_to_iframe(frame_reference=self.locators['paymentIframe'])
        self.webDriver.click(element=self.locators['agreeTerms'], locator_type='xpath')
        self.webDriver.click(element=self.locators['payContinue'], locator_type='xpath')
        self.webDriver.wait_for(seconds=10)
