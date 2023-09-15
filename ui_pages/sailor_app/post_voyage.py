__author__ = 'vanshika.arora'

from virgin_utils import *


class Post_voyage(General):
    """
    Page class for post voyage screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "street": "//input[@id='streetInput']",
            "no": "//input[@id='noInput']",
            "city": "//input[@id='cityInput']",
            "state": "//input[@id='state']",
            "zipcode": "//input[@id='zipCodeInput']",
            "select_text": "//[text()='%s']"
        })

    def fill_post_voyage_details(self):
        """
        Function to complete post voyage details
        """
        self.webDriver.set_text(element=self.locators.street, locator_type='xpath', text='Street')
        self.webDriver.set_text(element=self.locators.no, locator_type='xpath', text='104')
        self.webDriver.set_text(element=self.locators.city, locator_type='xpath', text='Tucson')
        self.webDriver.click(element=self.locators.state, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_text % 'Arizona', locator_type='xpath')
        self.webDriver.set_text(element=self.locators.zipcode, locator_type='xpath', text='80245')
