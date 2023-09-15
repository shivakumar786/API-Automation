__author__ = 'vanshika.arora'

from virgin_utils import *


class Payment_methods(General):
    """
    Page class for payment methods page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "payment_methods_title_question": "//div[@class='question']",
            "credit_card": "//label[@id='card']",
        })

    def verify_payment_method_title_question(self):
        """
        Function to verify payment method title question
        """
        title_question = self.webDriver.get_text(element=self.locators.payment_methods_title_question, locator_type='xpath')
        assert title_question == "How would you like to pay on board?","Payment method question title is incorrect"

    def select_credit_card(self):
        """
        Function to click Book excursions button
        :return:
        """
        self.webDriver.click(element=self.locators.credit_card, locator_type='xpath')
