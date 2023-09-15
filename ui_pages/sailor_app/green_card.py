__author__ = 'vanshika.arora'

from virgin_utils import *


class Green_card(General):
    """
    Page class for green card screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header": "//h1[@class='PageTitle']",
            "gender": "//input[@id='gender']",
            "green_card_number": "//input[@id='number']",
            "country_of_issue": "//input[@id='issueCountryCode']",
            "month_expiry_date": "//span[@id='month_expiryDate']",
            "day_expiry_date": "//input[@id='dayInput']",
            "year_expiry_date": "//input[@id='yearInput']",
            "month_dob": "//span[@id='month_birthDate']",
            "day_dob": "//input[@id='dayInput']",
            "year_dob": "//input[@id='yearInput']",
            "first_name": "//input[@id='givenName']",
            "last_name": "//input[@id='surname']",

        })

    def verify_green_card_scan_screen(self):
        """
        Function to scan green card
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page_title = self.webDriver.get_text(element=self.locators.passport_header, locator_type='xpath')
        assert page_title == 'Green card scan', " User has not landed on passport scan screen"

    def verify_correct_details_available_after_scanning_green_card(self, nationality):
        """
        Function to verify that correct details are available after scanning green card
        :param nationality:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        first_name = self.webDriver.get_web_element(element=self.locators.first_name, locator_type='xpath').get_attribute('value')
        last_name =  self.webDriver.get_web_element(element=self.locators.last_name, locator_type='xpath').get_attribute('value')
        gender = self.webDriver.get_web_element(element=self.locators.gender,
                                                       locator_type='xpath').get_attribute('value')
        birthday_month = self.webDriver.get_text(element=self.locators.month_dob, locator_type='xpath')
        birthday_date = self.webDriver.get_web_element(element=self.locators.day_dob, locator_type='xpath').get_attribute('value')
        birthday_year = self.webDriver.get_web_element(element=self.locators.year_dob, locator_type='xpath').get_attribute('value')
        green_card_number = self.webDriver.get_web_element(element=self.locators.green_card_numberer, locator_type='xpath').get_attribute('value')
        expiry_month = self.webDriver.get_text(element=self.locators.month_expiry_date, locator_type='xpath')
        expiry_date = self.webDriver.get_web_element(element=self.locators.day_expiry_date, locator_type='xpath').get_attribute('value')
        expiry_year = self.webDriver.get_web_element(element=self.locators.year_expiry_date, locator_type='xpath').get_attribute('value')
        country_of_issue = self.webDriver.get_web_element(element=self.locators.country_of_issue, locator_type='xpath').get_attribute('value')
        assert first_name == 'VOID',"Correct first name is not scanned"
        assert last_name == "VOID","Correct last name is not scanned"
        assert gender == "Female","Correct gender is not scanned"
        assert birthday_month == "Jan", "Correct birthday month is not scanned"
        assert birthday_date == "1","Correct birthday date is not scanned"
        assert birthday_year == '2020',"Correct birthday year is not scanned"
        assert green_card_number == "000000039","Correct passport number is not scanned"
        assert expiry_month =="Jan","Correct expiry month is not scanned"
        assert expiry_date == "1","Correct expiry date is not scanned"
        assert expiry_year == "1980","Correct expiry year is not scanned"
        assert country_of_issue == nationality, "Correct country of issue is not scanned"

    def fill_correct_sailor_details_for_green_card(self, guest_data, nationality):
        """
        Function to fill correct sailor details
        :param guest_data:
        :param nationality:
        """
        self.webDriver.clear_text(element=self.locators.first_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.first_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.clear_text(element=self.locators.last_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.last_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.click(element=self.locators.month_dob, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'May', locator_type='xpath')
        date_s = guest_data[0]['BirthDate'].split('-')[2]
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.clear_text(element=self.locators.day_dob, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.day_dob, locator_type='xpath',
                                text=date_s)
        year_s = guest_data[0]['BirthDate'].split('-')[0]
        self.webDriver.clear_text(element=self.locators.year_dob, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.year_dob, locator_type='xpath',
                                text=year_s)

        self.webDriver.click(element=self.locators.month_of_issue, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Jan', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.clear_text(element=self.locators.date_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.date_of_issue, locator_type='xpath',
                                text='27')
        self.webDriver.clear_text(element=self.locators.year_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.year_of_issue, locator_type='xpath',
                                text='2015')
        self.webDriver.clear_text(element=self.locators.year_expiry_date, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.year_expiry_date, locator_type='xpath',
                                text='2025')
        self.webDriver.click(element=self.locators.country_of_permanent_residence, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % nationality, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.done_cta, locator_type='xpath')