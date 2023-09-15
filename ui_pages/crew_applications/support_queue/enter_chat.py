__author__ = 'aatir.fayyaz'

from virgin_utils import *


class EnterChat(General):
    """
    Page class to Enter into Chat
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "sent_message": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "message": "//*[@resource-id='message']",
            "send_message_button": "//*[@text='send']",
            "clickable_hyperlink": "//*[@class='android.widget.TextView']"
                            "[contains(@text,'https://application-integration.ship.virginvoyages.com/supportQueue/')]",
            "main_menu": "//*[@class='android.widget.Button'][3]",
            "mark_as_resolved": "//*[@text='Mark as Resolved']",
            "view_details": "//*[@text='View Sailor Details']",
            "own_request": "//*[@text='Own Request']",
            "owned_by": "//*[@class='android.widget.TextView'][@text='Owned by me']",
            "yes_resolved": "//*[@text='YES']",
            "back_button": "//*[@text='menu']",
            "close_canned_message_button": "//*[@class='android.widget.Button'][@text='menu'][@index='1']",
            "support_queue_header": "//*[@class='android.widget.TextView'][@text='Support Queue']",
            "search_button": "//*[@class='android.widget.Button'][@text=''][@index='2']",
            "back_from_search": "//*[@text='menu'][@index='0']",
            "search_message_in_conversation": "//input[@placeholder='Search message in current conversation']",
            "searched_keyword": "//*[@class='android.view.View'][contains(@text,'%s')]",
        })

    def verify_sent_message(self, canned_message):
        """
        Function to verify sent message
        :param canned_message:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sent_message % canned_message,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.sent_message % canned_message,
                                                       locator_type='xpath'):
            logger.debug("Message is sent successfully")
        else:
            self.webDriver.allure_attach_jpeg('verify_sent_message')
            raise Exception("Message has not been sent")

    def send_media_item_in_message(self):
        """
        Send Media Item in message
        :return:
        """
        visitor_image_path = GeneratePhoto(gender='M').select_random_image()
        self.webDriver.click(element=self.locators.message, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.message, locator_type="xpath", text=visitor_image_path)
        self.webDriver.click(element=self.locators.send_message_button, locator_type='xpath')

    def verify_search_chat_by_keyword(self, test_data):
        """
        search chat by keyword
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(3)
        self.webDriver.click(element=self.locators.search_button, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.set_text(element=self.locators.search_message_in_conversation, locator_type='xpath',
                                text=test_data['sent_message'])
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        if self.webDriver.is_element_display_on_screen(
                element=self.locators.searched_keyword % test_data['sent_message'],
                locator_type='xpath'):
            self.webDriver.click(element=self.locators.back_from_search, locator_type='xpath')
            logger.debug("Searched keyword found in conversation")
        else:
            self.webDriver.allure_attach_jpeg('verify_search_chat_by_keyword')
            raise Exception("Searched keyword not found in conversation")

    def own_the_request(self):
        """
        own the created request for self and verify
        :return:
        """
        self.webDriver.click(element=self.locators.main_menu, locator_type="xpath")
        self.webDriver.click(element=self.locators.own_request, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.owned_by,
                                                      locator_type='xpath', time_out=120)
        text = self.webDriver.get_text(element=self.locators.owned_by, locator_type="xpath")
        assert text == 'Owned by me', "failed to own the request"

    def send_hyperlink_to_sailor(self):
        """
        Function to send message from support queue to a sailor
        :return:
        """
        self.webDriver.click(element=self.locators.message, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.message, locator_type='xpath',
                                text='https://application-integration.ship.virginvoyages.com/supportQueue/')
        self.webDriver.click(element=self.locators.send_message_button, locator_type='xpath')

    def verify_clickable_hyperlink(self):
        """
        Function to verify that hyperlink is clickable
        :return:
        """
        self.webDriver.click(element=self.locators.clickable_hyperlink, locator_type='xpath')
        self.webDriver.wait_for(5)
        application_name = self.webDriver.get_text(element=self.locators.support_queue_header, locator_type='xpath')
        if application_name == 'Support Queue':
            logger.debug("Support queue module has been opened by clickable hyperlink in conversation")
        else:
            raise Exception("Support queue module has not been opened by clickable hyperlink in conversation")

    def mark_chat_status_to_resolved(self):
        """
        Function to mark chat status to resolved
        :return:
        """
        self.webDriver.click(element=self.locators.main_menu, locator_type='xpath')
        self.webDriver.click(element=self.locators.mark_as_resolved, locator_type='xpath')
        self.webDriver.click(element=self.locators.yes_resolved, locator_type='xpath')
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

