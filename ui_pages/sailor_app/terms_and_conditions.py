__author__ = 'vanshika.arora'

from virgin_utils import *


class terms_And_Conditions(General):
    """
    Page class for terms and conditions screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "terms_and_conditions": "//h1[text()='Terms & Conditions']",
            "security_guide": "//div[@id='securityGuideItem']",
            "mobile_terms_and_conditions": "//div[@id='mobileTermsConditionsItem']",
            "privacy_policy": "//div[@id='privacyPolicyItem']",
            "cookie_policy": "//div[@id='cookiePolicyItem']"
            })

    def verify_terms_and_conditions_page_landing(self):
        """
        Function to verify that user has landed on terms and conditions screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.terms_and_conditions,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on terms and conditions screen")
        else:
            raise Exception("Sailor has not landed on terms and conditions screen")

    def open_security_guide(self):
        """
        Function to open security guide
        :return:
        """
        self.webDriver.click(element=self.locators.mobile_terms_and_conditions, locator_type='xpath')

    def open_mobile_terms_and_conditions(self):
        """
        Function to open mobile terms and conditions screen
        :return:
        """
        self.webDriver.click(element=self.locators.security_guide, locator_type='xpath')

    def open_privacy_policy(self):
        """
        Function to open privacy policy screen
        :return:
        """
        self.webDriver.click(element=self.locators.privacy_policy, locator_type='xpath')

    def open_cookie_policy(self):
        """
        Function to open cookie policy screen
        :return:
        """
        self.webDriver.click(element=self.locators.cookie_policy, locator_type='xpath')



