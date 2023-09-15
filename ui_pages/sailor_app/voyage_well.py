__author__ = 'vanshika.arora'

from virgin_utils import *


class Voyage_well(General):
    """
    Page class for voyage well page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "voyage_well_header": "//h1[text()='Voyage Well form']",
            "open_voyage_well": "//button[@id='voyageWellEdit']",
            "vaccination_status_title": "//h3[text()='Vaccination Status']",
            "yes_vaccination_button": "//label[@id='notVaccinatedButton']",
            "select_vaccination_name": "//span[@id='vaccine_type']",
            "select_vaccine": "//*[@text='%s']",
            "final_vaccination_date": "//div[text()='Final vaccination date']",
            "open_month_of_vaccination": "//span[@id='month_dateOfVaccination']",
            "day_of_vaccination": "//input[@id='dayInput']",
            "year_of_vaccination": "//input[@id='yearInput']",
            "submit_form": "//button[@id='voyageWellContractSubmit']",
            "vaccinations": "android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[%s]/android.widget.TextView[1]"
        })

    def verify_voyage_well_form_about_page(self):
        """
        Verify user has landed on voyage well form about page
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_well_header,
                                                       locator_type='xpath'):
            logger.debug("Voyage well form about page is available on screen")
        else:
            raise Exception("Voyage well form about page not available on screen")

    def open_voyage_well_form(self):
        """
        Function to open voyage well form to click on downward error
        """
        self.webDriver.click(element=self.locators.open_voyage_well, locator_type='xpath')

    def select_vaccination_status(self):
        """
        Function to select vaccination status as yes
        """
        self.webDriver.scroll_till_element(element=self.locators.vaccination_status_title, locator_type='xpath')
        self.webDriver.click(element=self.locators.yes_vaccination_button, locator_type='xpath')

    def enter_vaccination_name(self):
        """
        Function to select vaccination name
        """
        vaccines_available = ['Astra Zeneca', 'COVAXIN', 'Covidshield', 'Covovax', 'Johnson & Johnson', 'Moderna', 'Novavax', 'Pfizer','Sinopharm','Sinovac']
        self.webDriver.click(element=self.locators.select_vaccination_name, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.select_vaccine % random.choice(vaccines_available),
                             locator_type='xpath')

    def select_vaccination_date_and_submit(self):
        """
        Function to select vaccination date
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.scroll_till_element(element=self.locators.final_vaccination_date, locator_type='xpath')
        self.webDriver.click(element=self.locators.open_month_of_vaccination, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.select_vaccine % 'May',locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.set_text(element=self.locators.day_of_vaccination, locator_type='xpath',text='21')
        self.webDriver.set_text(element=self.locators.year_of_vaccination, locator_type='xpath',text='2021')
        self.webDriver.driver.hide_keyboard()
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.submit_form, locator_type='xpath')

    def verify_vaccination_names_available_in_alphabetic_order(self):
        """
        Function to cerify that vaccination names are available in alphabetic order
        """
        vaccination_list=[]
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        get_all_vaccination_names = self.webDriver.get_elements(
            element=self.locators.vaccinations, locator_type='xpath')
        for i in get_all_vaccination_names:
            vaccination_list.append(i.text)



