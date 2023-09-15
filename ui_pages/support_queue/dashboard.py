__author__ = 'Vanshika.Arora'

from virgin_utils import *


class Dashboard(General):
    """
    Page Class for Support Queue Dashboard page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Dashboard page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "search": "//form/div/div/input",
            "support_queue_header": "//header/div/h6",
            "new_chat_button": "//button/span[text()='NEW CHAT']",
            "filter_icon": "//p[contains(text(),'Filters')]/following-sibling::button",
            "sailor_name": "//h6[text()='Sailor Details']/following-sibling::div//h5",
            "sailor_details": "//h6[contains(text(),'Sailor Details')]",
            "message": "//textarea[@id='message']",
            "open_canned_message": "//button[@aria-label='add']/span/img",
            "add_canned_message": "//button[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-edgeEnd']",
            "send_message": "//button[@aria-label='send']",
            "in_progress_sailor": "//div/p[text()='In Progress Request']/ancestor::div//span[contains(text(),'%s')]",
            "canned_message_text": "//textarea[1]",
            "add_canned_message_button": "//span[(text()='ADD')]",
            "saved_canned_message": "//p[contains(text(),'Ahoy Sailor')]/ancestor::div/div/button/p",
            "search_canned_message": "//p[contains(text(),'Ahoy Sailor')]/ancestor::div/div/button/p[text()='%s']",
            "sent_message": "//p[text()='%s']",
            "sailor_details_header": "//h6[text()='Sailor Details']",
            "clickable_hyperlink": "//a[text()='https://application-integration.ship.virginvoyages.com/supportQueue/']",
            "search_message_in_conversation": "//input[@placeholder='Search message in current conversation']",
            "searched_keyword": "//mark[text()='%s']",
            "click_menu_icon": "//header/following-sibling::div/div/div/div/div/button[@aria-label='menu']",
            "mark_as_resolved": "//span[normalize-space()='Mark as Resolved']",
            "yes_resolved": "//div[@role='presentation']//button/span[text()='YES']",
            "see_all_resolved_request": "//span[contains(text(),'See All')]",
            "resolved_chat": "//p[text()='Resolved Request']/parent::div/parent::div/parent::div//div[@role='region']//button//span",
            "resolved_message": "//p[text()='%s']",
            "user_avatar": "//h6[text()='Support Queue']/parent::div/button/div",
            "logout": "//span[text()='Logout']",
            "open_resolved_chat": "//p[text()='Resolved Request']/parent::div/parent::div/parent::div//div[@role='region']//button//span[contains(text(),'%s')]",
            "upload_photo": "cameraInput",
            "see_all_resolved_requests": "//p[text()='Resolved Request']/parent::div/parent::div/parent::div//div[@role='region']//button//span[contains(text(),'See All')]",
            "filter_header_title": "//h6[text()='Filter']",
            "resolved_request_list": "(//div[@role='region']/div/div)[3]",
            "search_by_name_cabin": "//*[@placeholder='Name / Cabin']",
            "close_button": "//*[@placeholder='Name / Cabin']/../div/button[@aria-label='To Clean']",
            "own_request": "//*[text()='OWN REQUEST']",
            "click_on_search": "//*[@aria-label = 'To Search']",
            "owned_by": "//*[text()='Owned by:']",
            })

    def verify_support_queue_header_on_top_right_corner(self):
        """
        verify support queue header on top right corner of support queue after login
        """
        application_name = self.webDriver.get_text(element=self.locators.support_queue_header, locator_type='xpath')
        if application_name == 'Support Queue':
            logger.debug("Support queue header is available on top left corner")
        else:
            self.webDriver.allure_attach_jpeg('support_queue_header_on_top_right_corner')
            raise Exception("Support queue header is not available on top left corner")

    def availability_of_search_option(self):
        """
        availability of search option
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.search, locator_type='xpath'):
            logger.debug("Search option available on Dashboard")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_search_option')
            raise Exception("Search option not available on Dashboard")

    def availability_of_new_chat_button(self):
        """
        availability of new chat button
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.new_chat_button, locator_type='xpath'):
            logger.debug("New chat button available on Dashboard")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_new_chat_button')
            raise Exception("New chat button not available on Dashboard")

    def availability_of_filter_icon(self):
        """
        availability of filter icon
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.filter_icon, locator_type='xpath'):
            logger.debug("Filter icon available on Dashboard")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_filter_icon')
            raise Exception("Filter icon not available on Dashboard")

    def click_new_chat_button(self):
        """
        Click new chat button
        :return:
        """
        self.webDriver.scroll_till_element(self.locators.filter_icon, 'xpath')
        self.webDriver.click(element=self.locators.new_chat_button, locator_type='xpath')

    def verify_sailor_name_in_sailor_details(self, sailor_name):
        """
        Function to verify sailor name in sailor details
        :param sailor_name:
        :return:
        """
        get_sailor_name = self.webDriver.get_text(element=self.locators.sailor_name, locator_type='xpath')
        if get_sailor_name == sailor_name:
            logger.debug("Correct sailor name is displayed in sailor details in left side")
        else:
            self.webDriver.allure_attach_jpeg('verify_sailor_name_in_sailor_details')
            raise Exception("Correct sailor name is not displayed in sailor details in left side")

    def verify_sailor_details_header_on_right_side(self):
        """
        Verify presence of sailor details header
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_details_header, locator_type='xpath'):
            logger.debug("sailor details header is available on right side Dashboard")
        else:
            self.webDriver.allure_attach_jpeg('verify_sailor_details_header_on_right_side')
            raise Exception("sailor details header is not available on right side Dashboard")

    def send_message(self, test_data):
        """
        Function to send message from support queue to a sailor
        :param test_data:
        :return:
        """
        now = datetime.now()
        test_data['sent_message'] = f'Message at {now}'
        self.webDriver.set_text(element=self.locators.message, locator_type='xpath', text=test_data['sent_message'])
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')

    def verify_sailor_in_progress_section(self, sailor_name):
        """
        Function to verify in progress status of sailor after initiating chat
        :param sailor_name:
        :return:
        """
        sailor_fname = sailor_name.split()[0]
        self.webDriver.set_text(element=self.locators.search_by_name_cabin,locator_type="xpath", text=sailor_fname)
        self.webDriver.click(element=self.locators.click_on_search, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.in_progress_sailor % sailor_fname, locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.in_progress_sailor % sailor_fname, locator_type='xpath'):
            logger.debug("Sailor has correct in progress status")
            self.webDriver.click(element=self.locators.close_button, locator_type="xpath")
        else:
            self.webDriver.allure_attach_jpeg('verify_sailor_in_progress_section')
            raise Exception("Sailor does not have correct in progress status")

    def verify_sent_message(self, message):
        """
        Function to verify sent message
        :param message:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sent_message % message,
                                                      locator_type='xpath',
                                                      time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.sent_message % message, locator_type='xpath'):
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
        self.webDriver.set_text(element=self.locators.upload_photo, locator_type="id",
                                text=visitor_image_path)
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')

    def send_hyperlink_to_sailor(self):
        """
        Function to send message from support queue to a sailor
        :return:
        """
        self.webDriver.set_text(element=self.locators.message, locator_type='xpath', text='https://application-integration.ship.virginvoyages.com/supportQueue/')
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')

    def verify_clickable_hyperlink(self):
        """
        Function to verify that hyperlink is clickable
        :return:
        """
        self.webDriver.click(element=self.locators.clickable_hyperlink, locator_type='xpath')
        application_name = self.webDriver.get_text(element=self.locators.support_queue_header, locator_type='xpath')
        if application_name == 'Support Queue':
            logger.debug("Support queue module has been opened by clickable hyperlink in conversation")
        else:
            raise Exception("Support queue module has not been opened by clickable hyperlink in conversation")
        window = self.webDriver.get_current_window()
        self.webDriver.switch_to_main_tab(window)

    def verify_search_chat_by_keyword(self, test_data):
        """
        search chat by keyword
        :param test_data:
        :return:
        """
        self.webDriver.set_text(element=self.locators.search_message_in_conversation, locator_type='xpath',
                                text=test_data['sent_message'])
        if self.webDriver.is_element_display_on_screen(element=self.locators.searched_keyword % test_data['sent_message'], locator_type='xpath'):
            self.webDriver.clear_text(element=self.locators.search_message_in_conversation, locator_type='xpath',
                                      action_type='clear')
            logger.debug("Searched keyword found in conversation")
        else:
            self.webDriver.allure_attach_jpeg('verify_search_chat_by_keyword')
            raise Exception("Searched keyword not found in conversation")

    def mark_chat_status_to_resolved(self):
        """
        Function to mark chat status to resolved
        :return:
        """
        self.webDriver.click(element=self.locators.click_menu_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.mark_as_resolved, locator_type='xpath')
        self.webDriver.click(element=self.locators.yes_resolved, locator_type='xpath')

    def verify_chat_mark_as_resolved(self, sailor_cabin, sailor_name):
        """
        Function to verify chat mark as resolved
        :param sailor_cabin:
        :param sailor_name:
        :return:
        """
        for retry in range(0, 5):
            self.webDriver.set_text(element=self.locators.search_by_name_cabin, locator_type="xpath", text=sailor_cabin)
            self.webDriver.click(element=self.locators.click_on_search, locator_type="xpath")
            if self.webDriver.is_element_display_on_screen(element=self.locators.open_resolved_chat % sailor_name,
                                                           locator_type='xpath'):
                logger.debug(f"Sailor {sailor_name} is there in resolved request")
                self.webDriver.click(element=self.locators.close_button, locator_type="xpath")
                break
            else:
                self.webDriver.click(element=self.locators.close_button, locator_type="xpath")
        else:
            self.webDriver.allure_attach_jpeg('verify_chat_mark_as_resolved')
            raise Exception(f"Sailor {sailor_name} is not there in resolved request")

    def verify_history_of_resolved_request(self, message):
        """
        Function to verify history of resolved request
        :param message:
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.resolved_message % message,
                                                       locator_type='xpath'):
            logger.debug("Previously sent message can be seen in history of resolved request")
        else:
            self.webDriver.allure_attach_jpeg('verify_history_of_resolved_request')
            raise Exception("Previously sent message can not be seen in history of resolved request")

    def logout(self):
        """
        Function to logout of support queue
        :return:
        """
        self.webDriver.click(element=self.locators.user_avatar, locator_type='xpath')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')

    def click_filter_icon(self):
        """
        Function to click on filter icon
        :return:
        """
        self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header_title,
                                                      locator_type='xpath',
                                                      time_out=60)

    def open_resolved_chat(self, sailor_name):
        """
        Function to open chat with status resolved
        :param sailor_name:
        :return:
        """
        self.webDriver.scroll_till_element(self.locators.resolved_request_list, 'xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.see_all_resolved_requests, locator_type='xpath'):
            self.webDriver.click(element=self.locators.see_all_resolved_requests, locator_type='xpath')
        sailor_fname = sailor_name.split()[0]
        self.webDriver.click(element=self.locators.open_resolved_chat % sailor_fname, locator_type='xpath')

    def own_the_request(self):
        """
        own the created request for self and verify
        :return:
        """
        self.webDriver.click(element=self.locators.own_request, locator_type="xpath")
        text = self.webDriver.get_text(element=self.locators.owned_by, locator_type="xpath")
        assert text == 'Owned by: me', "failed to own the request"
