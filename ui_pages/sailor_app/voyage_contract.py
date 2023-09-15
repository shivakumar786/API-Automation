__author__ = 'vanshika.arora'

from virgin_utils import *


class Voyage_contract(General):
    """
    Page class for voyage contract page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "voyage_contract": "//h1[text()='Voyage contract']",
            "next_cta": "//button[@id='VCGo']",
            "sign_on_behalf_of": "//div[@class='tit']",
            "sailormate_checkbox": "//div[@class='checkbox']",
            "submit_button": "//button[@id='VoyageContractSubmit']",
            "guest_list": "//div[@class='GuestList']"
        })

    def verify_voyage_contract_page_available(self):
        """
        Function to select yes for pregnancy question
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_contract,
                                                       locator_type='xpath'):
            logger.debug("Voyage contract title is available on screen")
        else:
            raise Exception("Voyage contract title is not available on screen")

    def click_next_cta_to_open_voyage_contract(self):
        """
        Function to click next cta
        """
        self.webDriver.click(element=self.locators.next_cta, locator_type='xpath')

    def sign_on_behalf_of_sailormate(self):
        """
        Function to sign voyage contract on behalf of sailormate
        """
        self.webDriver.scroll_till_element(element=self.locators.guest_list, locator_type='xpath')
        self.webDriver.click(element=self.locators.sign_on_behalf_of, locator_type='xpath')
        self.webDriver.click(element=self.locators.sailormate_checkbox, locator_type='xpath')

    def click_submit_button(self):
        """
        Function to submit voyage contract
        """
        self.webDriver.click(element=self.locators.submit_button, locator_type='xpath')



