__author__ = 'vanshika.arora'

from virgin_utils import *


class Health_form(General):
    """
    Page class for health form page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "health_form_introduction_header": "//h1[@class='PageTitle']",
            "start_health_form": "//button[@id='DHCGo']",
            "question_1_yes": "//div[text()='Question 1']/following-sibling::div/div/div/label/span[text()='No']",
            "question_2_yes": "//div[text()='Question 2']/following-sibling::div/div/div/label/span[text()='No']",
            "question_3_yes": "//div[text()='Question 3']/following-sibling::div/div/div/label/span[text()='No']",
            "question_4_yes" : "//div[text()='Question 4']/following-sibling::div/div/div/label/span[text()='No']",
            "question_5_yes": "//div[text()='Question 5']/following-sibling::div/div/div/label/span[text()='No']",
            "ps_yes": "//div[text()='P.S.']/following-sibling::div/div/div/label/span[text()='No']",
            "question_test_update_yes": "//div[text()='Question Test Update K']/following-sibling::div/div/div/label/span[text()='No']",
            "final_question_yes": "//div[text()='Final Question']/following-sibling::div/div/div/label/span[text()='No']",
            "test_title_five_yes": "//div[text()='Test Title - Five']/following-sibling::div/div/div/label/span[text()='No']",
            "open_cabin_mates": "//div[@class='tit']",
            "select_cabin_mate": "//div[@class='Guest0']/div[@class='name']",
            "error_modal_text": "//h2[text()='Unfortunately, we were not able to approve your health form so we'll need to follow up.']",
            "modal_close_button": "//span[@id='modal-close-button']",
            "error_modal_ok_button": "//button[@id='HealthCheckFailModalOkButton']",
            "question_1_no": "//div[text()='Question 1']/following-sibling::div/div/div/label/span[text()='Yes']",
            "question_2_no": "//div[text()='Question 2']/following-sibling::div/div/div/label/span[text()='Yes']",
            "question_3_no": "//div[text()='Question 3']/following-sibling::div/div/div/label/span[text()='Yes']",
            "question_4_no": "//div[text()='Question 4']/following-sibling::div/div/div/label/span[text()='Yes']",
            "question_5_no": "//div[text()='Question 5']/following-sibling::div/div/div/label/span[text()='Yes']",
            "ps_no": "//div[text()='P.S.']/following-sibling::div/div/div/label/span[text()='Yes']",
            "question_test_update_no": "//div[text()='Question Test Update K']/following-sibling::div/div/div/label/span[text()='Yes']",
            "final_question_no": "//div[text()='Final Question']/following-sibling::div/div/div/label/span[text()='Yes']",
            "test_title_five_no": "//div[text()='Test Title - Five']/following-sibling::div/div/div/label/span[text()='Yes']",
            "pre_departure_health_check_header": "//h1[text()='Pre-departure health check']",
            "health_form_failed_text": "//div[@class='PageDescription']/p[1]",
            "call_soon_text": "//div[@class='PageDescription']/p[2]",
            "health_check_reopen_button": "//button[@id='HealthCheckIsGoodClose']"


        })

    def verify_user_landed_on_health_form_introduction_page(self):
        """
        Function to verify that user has landed on guides page
        """
        health_form_introduction_title = self.webDriver.is_element_enabled(element=self.locators.health_form_introduction_header, locator_type='id')
        assert health_form_introduction_title == 'Let us know you’re fit to sail', "User has landed on health form introduction page"

    def start_health_form(self):
        """
        Function to start health form
        """
        self.webDriver.click(element=self.locators.start_health_form, locator_type='xpath')

    def fill_health_form_with_incorrect_answers(self):
        """
        Function to fill health_form_with_incorrect_answers
        """
        self.webDriver.click(element=self.locators.question_1_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_2_yes, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_2_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_3_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_4_yes, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_4_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_5_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.final_question_yes, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.final_question_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.ps_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_test_update_yes, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_test_update_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.test_title_five_yes, locator_type='xpath')
        self.webDriver.click(element=self.locators.open_cabin_mates, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_cabin_mate, locator_type='xpath')

    def verify_error_modal_text(self):
        """
        Function to verify error modal text
        """
        error_modal_close_button = self.webDriver.is_element_display_on_screen(element=self.locators.modal_close_button, locator_type='xpath')
        error_modal_text = self.webDriver.is_element_display_on_screen(element=self.locators.error_modal_text,
                                                                               locator_type='xpath')
        assert error_modal_close_button ==  True , "Error modal close button is available on the screen"
        assert error_modal_text == True, "Correct error modal text is displayed on the screen"

    def click_ok_button_on_error_modal(self):
        """
        Function to click okay button on error modal
        """
        self.webDriver.click(element=self.locators.error_modal_ok_button, locator_type='xpath')

    def fill_health_form_with_correct_answers(self):
        """
        Function to fill health form with correct details
        """
        self.webDriver.click(element=self.locators.question_1_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_2_no, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_2_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_3_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_4_no, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_4_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_5_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.final_question_no, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.final_question_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.ps_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.question_test_update_no, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.question_test_update_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.test_title_five_no, locator_type='xpath')
        self.webDriver.click(element=self.locators.open_cabin_mates, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_cabin_mate, locator_type='xpath')

    def verify_health_form_rejected_page(self):
        """
        Function to verify that user landed on helath form failed page
        """
        pre_departure_health_check_header = self.webDriver.is_element_display_on_screen(element=self.locators.pre_departure_health_check_header,
                                                                               locator_type='xpath')
        health_form_failed_text = self.webDriver.get_text(element=self.locators.health_form_failed_text,locator_type='xpath')
        call_soon_text = self.webDriver.get_text(element=self.locators.call_soon_text,locator_type='xpath')
        assert pre_departure_health_check_header == True, "User has not landed on pre departure health check page"
        assert health_form_failed_text == "We weren't able to approve your health form, so we'll need to follow up with you.", "Correct health form failed text is not displayed on screen"
        assert  call_soon_text == "Depending on what's going on, we’ll give you a call soon to discuss or chat with you at the port.", "Correct call you soon text is not displayed on screen"
        self.webDriver.click(element=self.locators.health_check_reopen_button, locator_type='xpath')