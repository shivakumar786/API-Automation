__author__ = 'Vanshika.Arora'

from virgin_utils import *


class CannedMessage(General):
    """
    Page Class for Canned Message in Support Queue
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Canned Message window
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "open_canned_message": "//button[@aria-label='add']/span/img",
            "add_canned_message": "//button[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-edgeEnd']",
            "canned_message_text": "//textarea[@id='standard-name']",
            "add_canned_message_button": "//span[(text()='ADD')]",
            "saved_canned_message": "//p[contains(text(),'Canned Messages')]/ancestor::div/div/div/button/p",
            "search_canned_message": "//p[contains(text(),'Canned Messages')]/ancestor::div/div/div/button/p[text()='%s']",
            "send_message": "//button[@aria-label='send'] ",
            "delete_canned_message": "//p[contains(text(),'Canned Messages')]/ancestor::div/div/div/button/p[text()='%s']/parent::button/following-sibling::button/span/img"

        })

    def create_canned_message(self, test_data):
        """
        Function to create canned message
        :param test_data:
        :return:
        """
        now = datetime.now()
        test_data['canned_message'] = f'Canned message at {now}'
        self.webDriver.click(element=self.locators.open_canned_message, locator_type='xpath')
        self.webDriver.click(element=self.locators.add_canned_message, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.canned_message_text, locator_type='xpath',
                                text=test_data['canned_message'])
        self.webDriver.click(element=self.locators.add_canned_message_button, locator_type='xpath')

    def verify_canned_message(self, test_data):
        """
        Function to verify created canned message
        :param test_data:
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_canned_message % test_data['canned_message'], locator_type='xpath'):
            logger.debug('Canned message is saved')
        else:
            raise Exception('Canned message is not saved')


    def send_canned_message(self, message):
        """
        Function to send canned message
        :param message:
        :return:
        """
        self.webDriver.click(element=self.locators.search_canned_message % message, locator_type='xpath')
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')

    def delete_canned_message(self, message):
        """
        Function to delete canned message
        :param message:
        :return:
        """
        self.webDriver.click(element=self.locators.open_canned_message, locator_type='xpath')
        self.webDriver.click(element=self.locators.delete_canned_message % message, locator_type='xpath')

