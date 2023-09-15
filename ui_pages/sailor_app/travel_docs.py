__author__ = 'vanshika.arora'

from virgin_utils import *


class Travel_docs(General):
    """
    Page class for travel documents page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "next": "//button[@id='next']",
            "scan_document": "//button[@id='takePhoto']",
            "while_using_the_app": "//*[@text='While using the app']",
            "upload_document": "//*[@class='android.widget.TextView'][1]",
            "access_media": "//*[@text='Allow']",
            "search_image": "//*[@class='android.widget.AutoCompleteTextView']",
            "open_gallery": "//*[@text='Gallery']",
            "select_image": "(//android.widget.FrameLayout[@content-desc='Button'])[1]/android.widget.FrameLayout[1]/android.widget.ImageView",
            "select_visa_image": "(//android.widget.FrameLayout[@content-desc='Button'])[2]/android.widget.FrameLayout[1]/android.widget.ImageView",
            "done": "//*[@text='Done']",
            "travel_documents_text": "//p[@class='PageParagraph']",
            "passport_header": "//h1[@class='PageTitle']",
            "error_modal_text": "//h2[text()='We had a problem uploading your document.']",
            "try_again": "//button[text()='Try again']",
            "first_name": "//input[@id='givenName']",
            "last_name": "//input[@id='surname']",
            "month_dob":"//span[@id='month_birthDate']",
            "day_dob": "//label[text()='Date of birth']/parent::div/div//input[@id='dayInput']",
            "year_dob": "//label[text()='Date of birth']/parent::div/div//input[@id='yearInput']",
            "gender": "//input[@id='gender']",
            "passport_number": "//input[@id='number']",
            "month_expiry_date": "//span[@id='month_expiryDate']",
            "day_expiry_date": "//label[text()='Expiry date']/parent::div/div//input[@id='dayInput']",
            "year_expiry_date": "//label[text()='Expiry date']/parent::div/div//input[@id='yearInput']",
            "country_of_issue": "//input[@id='issueCountryCode']",
            "date_text": "//*[@text='%s']",
            "month_of_issue": "//span[@id='month_issueDate']",
            "date_of_issue": "//label[text()='Date of issue']/parent::div/div//input[@id='dayInput']",
            "year_of_issue": "//label[text()='Date of issue']/parent::div/div//input[@id='yearInput']",
            "country_of_permanent_residence": "//input[@id='countryOfResidenceCode']",
            "done_cta": "//button[@id='submitFormButton']",
            "done_cta_final": "//div[@class='tdocs__warning-text']/following-sibling::button",
            "page_header": "//h1[@class='PageTitle']",
            "visa_expiry_month": "//span[@id='month_expiryDate']",
            "visa_expiry_date": "//label[text()='Expiry date']/parent::div/div//input[@id='dayInput']",
            "visa_expiry_year": "//label[text()='Expiry date']/parent::div/div//input[@id='yearInput']",
            "visa_month_of_issue": "//span[@id='month_issueDate']",
            "visa_date_of_issue": "//label[text()='Date of issue']/parent::div/div//input[@id='dayInput']",
            "visa_year_of_issue": "//label[text()='Date of issue']/parent::div/div//input[@id='yearInput']",
            "find_country": "//*[@text='Country of issue']",
            "visa_issue_country": "//input[@id='issueCountryCode']",
            "visa_enteries": "//input[@id='visaEntries']",
            "visa_type": "//input[@id='visaTypeCode']",
            "issued_for": "//input[@id='issuedFor']",
            "select_passport": "//label[@id='PBtn']/span",
            "select_greencard": "//label[@id'ARCBtn']/span",
            "good_to_go":"//button[text()='I checked! I'm good to go']"

        })

    def click_next_button(self):
        """
        Function to click next button
        """
        self.webDriver.click(element=self.locators.next, locator_type='xpath')

    def click_scan_document_button(self):
        """
        Function to click camera icon
        """
        self.webDriver.click(element=self.locators.scan_document, locator_type='xpath')

    def give_permission_to_use_camera(self):
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        if self.webDriver.is_element_display_on_screen(element=self.locators.while_using_the_app,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.while_using_the_app, locator_type='xpath')

    def click_upload_document(self):
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.upload_document, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.upload_document, locator_type='xpath')

    def allow_to_access_media(self):
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.access_media, locator_type='xpath')

    def select_image(self):
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.open_gallery, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_image, locator_type='xpath')
        self.webDriver.click(element=self.locators.done, locator_type='xpath')

    def verify_natioanality_on_travel_docs_introduction_page(self, nationality):
        """
        Function to verify correct nationality available on travel document introduction page
        :param nationality:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.travel_documents_text, locator_type='xpath'
                                                      , time_out=60)
        rts_text = self.webDriver.get_text(element=self.locators.travel_documents_text, locator_type='xpath')
        get_nationality = rts_text.split('is')[1].split(',')[0].lstrip()
        assert get_nationality == nationality,"Correct nationality is not shown on rts travel documents introduction screen"

    def verify_passport_scan_screen_available(self):
        """
        Function to verify availability of passport scan screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.passport_header, locator_type='xpath'
                                                     , time_out=60)
        page_title = self.webDriver.get_text(element=self.locators.passport_header, locator_type='xpath')
        assert page_title == 'Passport scan', " User has not landed on passport scan screen"

    def verify_correct_details_available_after_scanning_passport(self, nationality):
        """
        Function to verify that correct details are available after scanning passport
        :param nationality:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.error_modal_text,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.try_again, locator_type='xpath')
            self.click_scan_document_button()
            self.give_permission_to_use_camera()
            self.click_upload_document()
            self.allow_to_access_media()
            self.select_image()
            if self.webDriver.is_element_display_on_screen(element=self.locators.error_modal_text,
                                                           locator_type='xpath'):
                raise Exception("User is not able to upload documents by scanning")
        else:
            first_name = self.webDriver.get_web_element(element=self.locators.first_name, locator_type='xpath').get_attribute('value')
            last_name =  self.webDriver.get_web_element(element=self.locators.last_name, locator_type='xpath').get_attribute('value')
            birthday_month = self.webDriver.get_text(element=self.locators.month_dob, locator_type='xpath')
            birthday_date = self.webDriver.get_web_element(element=self.locators.day_dob, locator_type='xpath').get_attribute('value')
            birthday_year = self.webDriver.get_web_element(element=self.locators.year_dob, locator_type='xpath').get_attribute('value')
            passport_number = self.webDriver.get_web_element(element=self.locators.passport_number, locator_type='xpath').get_attribute('value')
            expiry_month = self.webDriver.get_text(element=self.locators.month_expiry_date, locator_type='xpath')
            expiry_date = self.webDriver.get_web_element(element=self.locators.day_expiry_date, locator_type='xpath').get_attribute('value')
            expiry_year = self.webDriver.get_web_element(element=self.locators.year_expiry_date, locator_type='xpath').get_attribute('value')
            country_of_issue = self.webDriver.get_web_element(element=self.locators.country_of_issue, locator_type='xpath').get_attribute('value')
            assert first_name == 'VINCENT',"Correct first name is not scanned"
            assert last_name == "MALONE","Correct last name is not scanned"
            assert birthday_month == "Dec", "Correct birthday month is not scanned"
            assert birthday_date == "24","Correct birthday date is not scanned"
            assert birthday_year == '1972',"Correct birthday year is not scanned"
            assert passport_number == "DM9325B20","Correct passport number is not scanned"
            assert expiry_month =="Jan","Correct expiry month is not scanned"
            assert expiry_date == "27","Correct expiry date is not scanned"
            assert expiry_year == "2023","Correct expiry year is not scanned"
            assert country_of_issue == nationality, "Correct country of issue is not scanned"

    def fill_correct_sailor_details(self, guest_data, nationality):
        """
        Function to fill correct sailor details
        :param guest_data:
        :param nationality:
        """
        self.webDriver.clear_text(element=self.locators.first_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.first_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.clear_text(element=self.locators.last_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.last_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.click(element=self.locators.month_expiry_date, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Dec', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.month_dob, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Dec', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.month_of_issue, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Dec', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.clear_text(element=self.locators.date_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.date_of_issue, locator_type='xpath',
                                text='27')
        self.webDriver.clear_text(element=self.locators.year_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.year_of_issue, locator_type='xpath',
                                text='2015')
        self.webDriver.click(element=self.locators.country_of_permanent_residence, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % nationality, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.done_cta, locator_type='xpath')

    def verify_availability_of_potential_passport_expiration_issue_and_proceed(self):
        """
        Function to verify availability of potential passport expiration issue screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page_title = self.webDriver.get_text(element=self.locators.page_header, locator_type='xpath')
        assert page_title == 'Potential passport expiration issue', "Potential passport expiration screen is not available"
        self.webDriver.click(element=self.locators.next, locator_type='xpath')

    def click_done_cta(self):
        """
        Function to click done cta
        """
        self.webDriver.click(element=self.locators.done_cta_final, locator_type='xpath')

    def user_landed_on_visa_scan_screen(self):
        """
        Function to verify that user has landed on us visa scan screen
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page_title = self.webDriver.get_text(element=self.locators.page_header, locator_type='xpath')
        assert page_title == 'United States Visa scan', " User has not landed on VISA scan screen"

    def select_visa_image(self):
        """
        Function to select visa image
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.open_gallery, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_visa_image, locator_type='xpath')
        self.webDriver.click(element=self.locators.done, locator_type='xpath')

    def verify_correct_visa_details_available_after_scanning(self):
        """
        Function to verify that correct visa details are available after scanning
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        visa_number = self.webDriver.get_web_element(element=self.locators.passport_number, locator_type='xpath').get_attribute('value')
        visa_expiry_month = self.webDriver.get_text(element=self.locators.visa_expiry_month, locator_type='xpath')
        visa_expiry_date = self.webDriver.get_web_element(element=self.locators.visa_expiry_date,
                                                    locator_type='xpath').get_attribute('value')
        visa_expiry_year = self.webDriver.get_web_element(element=self.locators.visa_expiry_year, locator_type='xpath').get_attribute(
            'value')
        country_of_issue = self.webDriver.get_web_element(element=self.locators.visa_issue_country, locator_type='xpath').get_attribute(
            'value')
        first_name = self.webDriver.get_web_element(element=self.locators.first_name,
                                                    locator_type='xpath').get_attribute('value')
        last_name = self.webDriver.get_web_element(element=self.locators.last_name, locator_type='xpath').get_attribute(
            'value')
        assert visa_number == 'Z2311715', "Correct visa number is not scanned"
        assert visa_expiry_month == 'Aug', " Correct expiry month is not scanned"
        assert visa_expiry_date =='12', "Correct visa expiry date is not scanned"
        assert visa_expiry_year == "2028", 'Correct Visa expiry year is not scanned'
        assert country_of_issue == "United States", "Correct Country of issue is not scanned"
        assert first_name == "HARSH RAJESHKUMAR","Correct first name is not scanned"
        assert last_name == 'MEHTA',"Correct Last name is not scanned"

    def fill_correct_visa_details(self, guest_data):
        """
        Function to fill correct visa details
        :param guest_data:
        """
        self.webDriver.clear_text(element=self.locators.visa_date_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.visa_date_of_issue, locator_type='xpath',
                                text='16')
        self.webDriver.clear_text(element=self.locators.visa_year_of_issue, locator_type='xpath', action_type='clear')

        self.webDriver.set_text(element=self.locators.visa_year_of_issue, locator_type='xpath',
                                text='2018')
        self.webDriver.click(element=self.locators.visa_month_of_issue, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Aug', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.visa_issue_country, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'United States', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.visa_enteries, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'Multiple', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.visa_type, locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.date_text % 'U-5 Crime Victims', locator_type='xpath')
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.clear_text(element=self.locators.first_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.first_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.clear_text(element=self.locators.last_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.last_name, locator_type='xpath', text=guest_data[0]['FirstName'])
        self.webDriver.clear_text(element=self.locators.issued_for, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.issued_for, locator_type='xpath', text='Travel')
        self.webDriver.click(element=self.locators.done_cta, locator_type='xpath')

    def verify_available_primary_documents_option(self):
        """
        Function to verify correct documents_option available as per citizenship
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        page_title = self.webDriver.get_text(element=self.locators.page_header, locator_type='xpath')
        assert page_title == 'Choose your Primary document', " User has not landed on primary document option screen"
        passport = self.webDriver.get_text(element=self.locators.select_passport, locator_type='xpath')
        green_card = self.webDriver.get_text(element=self.locators.select_greencard, locator_type='xpath')
        assert passport == 'Passport',"Passport is not available as option for primary document for Indian Sailor"
        assert green_card == "Green card", "Green card is not available as option for primary document for Indian Sailor"

    def select_passport(self):
        """
        Function to select passport as primary documwnt
        """
        self.webDriver.click(element=self.locators.select_passport, locator_type='xpath')

    def select_green_card(self):
        """
        Function to select green card as primary document
        """
        self.webDriver.click(element=self.locators.select_greencard, locator_type='xpath')


