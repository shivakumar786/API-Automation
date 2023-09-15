__author__ = 'mohit.raghav'

import random

from virgin_utils import *


class HelpAndSupport(General):
    """
    Page class for help and support page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'categories': "//input[@type='checkbox']//following-sibling::span",
            "help_and_support_header": "//h1[text()='Let us help you out...']",
            'verify_questions_page_header': "//div[text()='{}']",
            'loading': '//img[@alt="loading..."]',
            'questions': "//div[@id='objectObjectItem']",
            'chat_btn': "//*[@resource-id='HelpChatBtn']",
            'chat_window_header': "//*[@text='Sailor Services']",
            'message_box': "//*[@resource-id='message']",
            'send_btn': "//*[@text='mic']",
            'verify_sent_msg': "//*[contains(@text,'Test Message')]"
        })

    def verify_help_and_support_questions(self):
        """
        Function to verify sailor services help and support questions
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.help_and_support_header,
                                                          locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.categories, locator_type='xpath')
        categories = self.webDriver.get_elements(element=self.locators.categories, locator_type='xpath')
        if len(categories) == 0:
            raise Exception("No categories found in help and support")
        else:
            chosen_category = random.choice(categories)
            self.webDriver.scroll(pixel_x=chosen_category.location['x'], pixel_y=chosen_category.location['y'])
            category_text = chosen_category.text
            chosen_category.click()
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.verify_questions_page_header.format(category_text),
                                                              locator_type='xpath')
            no_of_questions = self.webDriver.get_elements(element=self.locators.questions, locator_type='xpath')
            if no_of_questions == 0:
                raise Exception(f"No questions are visible for '{chosen_category.text}' category in Help and Support")

    def click_chat_button(self):
        """
        Function to open chat window
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.chat_btn, locator_type='xpath')
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.chat_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.chat_btn, locator_type='xpath')

    def verify_chat_window(self):
        """
        Function to verify chat window
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.chat_window_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.message_box, locator_type='xpath'):
            logger.info("Chat window is visible")
        else:
            raise Exception("Chat window is not visible")

    def send_message(self):
        """
        Function to send message to support team
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.message_box, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.message_box, locator_type='xpath', text='Test Message')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.send_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.send_btn, locator_type='xpath')
        self.webDriver.wait_for(2)

    def verify_sent_message(self):
        """
        Function to verify sent message in chat window
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.driver.hide_keyboard()
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.chat_window_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.verify_sent_msg, locator_type='xpath'):
            logger.info("Message has been sent successfully")
        else:
            raise Exception("Message has not been sent successfully")


