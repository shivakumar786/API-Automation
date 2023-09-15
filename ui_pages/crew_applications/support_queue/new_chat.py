__author__ = 'aatir.fayyaz'

from virgin_utils import *


class NewChat(General):
    """
    Page Class for New Chat in Support Queue
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of New chat window
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "search_sailor": "//*[@class='android.widget.EditText']",
            "get_all_sailors": "//*[@class='android.widget.TextView']",
            "click_on_sailor": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "user_not_available": "//*[@class='android.widget.TextView'][@text='This user is not available for chat']",
            "click_ok": "//*[@class='android.widget.Button'][@text='OK']",
            "sailor_name": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "message": "//*[@resource-id='message']",
            "send_message": "//*[@text='send']",
            "back_button": "//*[@class='android.widget.Button'][contains(@text,'menu')][@index='0']",
        })

    def search_sailor(self, search_item):
        """
        Search sailor with name or cabin number
        :param search_item:
        """
        self.webDriver.set_text(element=self.locators.search_sailor, locator_type='xpath', text=search_item)
        self.webDriver.submit()

    def click_searched_sailor(self, test_data):
        """
        Function to click on searched sailor
        :param test_data:
        :return:
        """
        test_data['sailor_name'] = []
        self.webDriver.wait_for(5)
        get_all_sailors = self.webDriver.get_elements(element=self.locators.get_all_sailors, locator_type='xpath')
        sailors_in_cabin = []
        for count, sailor in enumerate(get_all_sailors):
            if (count % 2) != 0 and len(sailor.text) != 0:
                sailors_in_cabin.append(sailor.text)
        for sailors in sailors_in_cabin:
            self.webDriver.click(self.locators.click_on_sailor % sailors, locator_type="xpath")
            self.webDriver.wait_for(3)
            if self.webDriver.is_element_display_on_screen(element=self.locators.user_not_available,
                                                           locator_type='xpath'):
                self.webDriver.click(element=self.locators.click_ok, locator_type='xpath')
                self.webDriver.wait_for(2)
            else:
                test_data['sailor_name'].append(sailors)
                break

    def send_message(self, test_data):
        """
        Function to send message from support queue to a sailor
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(5)
        now = datetime.now()
        test_data['sent_message'] = f'Message at {now}'
        self.webDriver.set_text(element=self.locators.message, locator_type='xpath',
                                text=test_data['sent_message'])
        self.webDriver.click(element=self.locators.send_message, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')