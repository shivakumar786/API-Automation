__author__ = 'prahlad.sharma'

from virgin_utils import *


class Rts(General):
    """
    Page class for rts page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "click_next_cta": "//*[@id='com.virginvoyages.guest.integration:id/action_bar_root']",
            "seaworthy_in_seconds": "//div[@class='sub-title']",
            "Lets_go_text":"//h1[@class='PageTitle']/div",
            "why_do_i_need_to_do_this": "//div[@class='info']",
            "step_3_payment_method": "//div[@class='steps']/div[3]",
            "step_2_travel_documents": "//div[@class='steps']/div[2]",
            "start_travel_docs": "//h1[text()='Travel documents']/following-sibling::div[@class='start']",
            "payment_method_title": "//h1[text()='Payment method']",
            "start": "//h1[text()='Payment method']/following-sibling::div[@class='start']",
            "pregnancy_question_step": "//div[@class='steps']/div[4]",
            "pregnancy_title": "//h1[text()='Pregnancy']",
            "open_pregnancy_question": "//h1[text()='Pregnancy']/following-sibling::div[@class='start']",
            "open_voyage_contract": "//div[@class='steps']/div[%s]",
            "voyage_contract_title": "//h1[text()='Voyage contract']",
            "start_voyage_contract": "//h1[text()='Voyage contract']/following-sibling::div[@class='start']",
            "emergency_contact_title": "//h1[text()='Emergency contact']",
            "start_emergency_contact": "//h1[text()='Emergency contact']/following-sibling::div[@class='start']",
            "step_aboard_title": "//h1[text()='Step aboard']",
            "start_step_aboard_task": "//h1[text()='Step aboard']/following-sibling::div[@class='start']",
            "back_button": "//button[@id='back-btn']",
            "payment_edit_button": "//h1[text()='Payment method']/div[@class='start']"
        })

    def verify_availability_of_rts_opening_text(self):
        """
        Function to verify availability of rts opening text
        """
        lets_go_text = self.webDriver.get_text(element=self.locators.Lets_go_text, locator_type='xpath')
        seaworthy_in_seconds_text = self.webDriver.get_text(element=self.locators.seaworthy_in_seconds, locator_type='xpath')
        assert lets_go_text == "Let’s go!","Correct text is available on rts opening screen, hence user has landed on rts screen"
        assert seaworthy_in_seconds_text == "SEAWORTHY IN SECONDS","Correct text is available on rts opening screen, hence user has landed on rts screen"

    def click_start_rts(self):
        """
        Function to click next cta to start the rts
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.click_next_cta, locator_type='xpath')

    def open_payment_method_step(self):
        """
        Function to open payment method
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.step_3_payment_method, locator_type='xpath')

    def open_travel_document_step(self):
        """
        Function to open payment method
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.step_2_travel_documents, locator_type='xpath')

    def start_travel_documents(self):
        """
        Function to open travel documents
        """
        self.webDriver.click(element=self.locators.start_travel_docs, locator_type='xpath')

    def verify_availability_of_payment_method(self):
        """
        Function to verify that user has landed on payment method screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_method_title, locator_type='xpath'):
            logger.debug("Payment method title is available on screen")
        else:
            raise Exception("Payment method title is not available on screen")

    def click_start_button(self):
        """
        Function to click start button
        """
        self.webDriver.click(element=self.locators.start, locator_type='xpath')

    def click_payment_edit_button(self):
        """
        Function to click edit button
        """
        self.webDriver.click(element=self.locators.payment_edit_button, locator_type='xpath')

    def open_security_photo_flow(self):
        """
        Open security photo flow
        :return:
        """
        self.webDriver.click(element=self.locators.click_next_cta, locator_type='xpath')

    def open_pregnancy_question_step(self):
        """
        Function to open pregnancy questions in rts
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.pregnancy_question_step, locator_type='xpath')

    def verify_availabilty_of_pregnancy_title(self):
        """
        Function to verify pregnancy header available on screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.pregnancy_title, locator_type='xpath'):
            logger.debug("Pregnancy title is available on screen")
        else:
            raise Exception("Pregnancy title is not available on screen")

    def open_pregnancy_questions(self):
        """
        Function to open pregnancy question
        """
        self.webDriver.click(element=self.locators.open_pregnancy_question, locator_type='xpath')

    def open_voyage_contract(self, gender):
        """
        Function to open voyage contract in rts
        :param gender:
        :return:
        """
        if gender == "Female" or gender == "Another Gender":
            self.webDriver.click(element=self.locators.open_voyage_contract % '5', locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.open_voyage_contract % '4', locator_type='xpath')

    def verify_availabilty_of_voyage_contract_title(self):
        """
        Function to verify availability of voyage contract title
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_contract_title, locator_type='xpath'):
            logger.debug("Voyage contract title is available on screen")
        else:
            raise Exception("Voyage contract title is not available on screen")

    def start_voyage_contract(self):
        """
        Function to open voyage contract
        """
        self.webDriver.click(element=self.locators.start_voyage_contract, locator_type='xpath')

    def open_emergency_contact(self, gender):
        """
        Function to open emergency contact in rts
        :param gender:
        :return:
        """
        if gender == "Female" or gender == "Another Gender":
            self.webDriver.click(element=self.locators.open_voyage_contract % '6', locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.open_voyage_contract % '5', locator_type='xpath')

    def verify_availabilty_of_emergency_contact_title(self):
        """
        Function to verify emergency contact title available on the screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.emergency_contact_title, locator_type='xpath'):
            logger.debug("Emergency contact title is available on screen")
        else:
            raise Exception("Emergency contact title is not available on screen")

    def start_emergency_contact(self):
        """
        Function to open emergency contact
        """
        self.webDriver.click(element=self.locators.start_emergency_contact, locator_type='xpath')

    def open_step_aboard_flow(self, gender):
        """
        Function to open step aboard flow
        """
        if gender == "Female" or gender == "Another Gender":
            self.webDriver.click(element=self.locators.open_voyage_contract % '7', locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.open_voyage_contract % '6', locator_type='xpath')

    def verify_availabilty_of_step_aboard_title(self):
        """
        Function to verify availability of step aboard title
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.step_aboard_title, locator_type='xpath'):
            logger.debug("Emergency contact title is available on screen")
        else:
            raise Exception("Emergency contact title is not available on screen")

    def start_step_aboard_task(self):
        """
        Function to open emergency contact
        """
        self.webDriver.click(element=self.locators.start_step_aboard_task, locator_type='xpath')

    def click_back_button(self):
        """
        Function to click back button
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')







