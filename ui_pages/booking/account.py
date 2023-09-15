__author__ = 'sarvesh.singh'

from virgin_utils import *


class Account(General):
    """
    Page class for Account Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = {
            "signup": "//a[contains(text(),'Sign Up')]",
            "signupWithEmail": "//button[@class='btn btn-block']",
            "firstName": "//input[@id='firstname']",
            "lastName": "//input[@id='lastname']",
            "email": "//input[@id='email']",
            "password": "//input[@id='password']",
            "month": "//*[@aria-label='Select Month']",
            "day": "//*[@aria-label='Select Day']",
            "year": "//*[@aria-label='Select Year']",
            "submitSignup": "//button[@class='btn btn-secondary']",
            "planVoyage": "//a[@class='btn btn-primary btn-lg SuperButton__section SuperButton__button']"
        }

    def click_signup(self):
        """
        To click on sign up button
        :return:
        """
        self.webDriver.click(element=self.locators['signup'], locator_type='xpath')

    def click_signup_with_email(self):
        """
        To click on sign up button
        :return:
        """
        self.webDriver.click(element=self.locators['signupWithEmail'], locator_type='xpath')

    def go_to_signup_page(self):
        """
        To click on sign up button
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.click_signup()
        self.click_signup_with_email()

    def fill_signup_details(self):
        """
        To click on sign up buttons
        :return:
        """
        self.webDriver.set_text(element=self.locators['firstName'], locator_type='xpath', text=generate_first_name())
        self.webDriver.set_text(element=self.locators['lastName'], locator_type='xpath', text=generate_last_name())
        self.webDriver.set_text(element=self.locators['email'], locator_type='xpath', text=generate_email_id())
        self.webDriver.set_text(element=self.locators['password'], locator_type='xpath', text='Yellow*99')
        self.webDriver.select_by_text(element=self.locators['month'], locator_type='xpath', text='JAN')
        self.webDriver.select_by_text(element=self.locators['day'], locator_type='xpath', text='03')
        self.webDriver.select_by_text(element=self.locators['year'], locator_type='xpath', text='1995')

    def submit_signup(self):
        """
        To click on sign up button
        :return:
        """
        self.webDriver.click(element=self.locators['submitSignup'], locator_type='xpath')
        self.webDriver.wait_for(seconds=5)

    def perform_signup(self):
        """

        :return:
        """
        self.fill_signup_details()
        self.webDriver.scroll(pixel_x='0', pixel_y='1200')
        self.submit_signup()

    def click_plan_voyage(self):
        """
        To click on sign up button
        :return:
        """
        self.webDriver.scroll(pixel_x='0', pixel_y='400')
        self.webDriver.click(element=self.locators['planVoyage'], locator_type='xpath')
        self.webDriver.wait_for(seconds=5)
