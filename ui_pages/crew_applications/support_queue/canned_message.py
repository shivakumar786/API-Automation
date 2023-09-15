__author__ = 'aatir.fayyaz'

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
            "open_canned_message": "//*[@class='android.widget.Button'][contains(@text,'add')][@index='1']",
            "add_canned_message": "//*[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-edgeEnd']",
            "canned_message_text": "//*[@resource-id='standard-name']",
            "add_canned_message_button": "//android.widget.Button[@text='ADD']",
            "search_canned_message": "//*[@class='android.widget.Button'][contains(@text,'%s')]",
            "send_message": "//*[@class='android.widget.Button'][contains(@text,'send')]",
            "delete_canned_message": "//*[@text='%s']/following-sibling::android.widget.Button[@text='logo']",
            "close_canned_message_button": "//*[@class='android.widget.Button'][@text='menu'][@index='1']"
        })

    def create_canned_message(self, test_data):
        """
        Function to create canned message
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(5)
        now = datetime.now()
        test_data['canned_message'] = f'Canned message at {now}'
        self.webDriver.click(element=self.locators.open_canned_message, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.decurtis.crew.embark')
        self.webDriver.click(element=self.locators.add_canned_message, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.canned_message_text, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.canned_message_text, locator_type='xpath',
                                text=test_data['canned_message'])
        self.webDriver.click(element=self.locators.add_canned_message_button, locator_type='xpath')

    def verify_canned_message(self, test_data):
        """
        Function to verify created canned message
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(2)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_canned_message % test_data['canned_message'],
                                                           locator_type='xpath'):
            for i in range(20):
                self.webDriver.scroll_mobile(300, 1150, 300, 960)
                if self.webDriver.is_element_display_on_screen(element=self.locators.search_canned_message % test_data['canned_message'],
                                                               locator_type='xpath'):
                    logger.debug('Canned message is saved')
                    break
            else:
                raise Exception('Canned message is not saved')

    def send_canned_message(self, message):
        """
        Function to send canned message
        :param message:
        :return:
        """
        self.webDriver.click(element=self.locators.search_canned_message % message, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.send_message, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')

    def delete_canned_message(self, message):
        """
        Function to delete canned message
        :param message:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.open_canned_message, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.click(element=self.locators.open_canned_message, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.delete_canned_message % message,
                                                           locator_type='xpath'):
            for i in range(20):
                self.webDriver.scroll_mobile(300, 1150, 300, 960)
                if self.webDriver.is_element_display_on_screen(element=self.locators.delete_canned_message % message,
                                                               locator_type='xpath'):
                    self.webDriver.click(element=self.locators.delete_canned_message % message, locator_type='xpath')
                    break
                else:
                    raise Exception('Canned message not deleted')
        else:
            self.webDriver.click(element=self.locators.delete_canned_message % message, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.close_canned_message_button,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.close_canned_message_button, locator_type='xpath')
        logger.debug('Canned message deleted successfully')

