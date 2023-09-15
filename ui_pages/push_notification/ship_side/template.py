__author__ = 'saloni.pattnaik'

from virgin_utils import *


class Template(General):
    """
    Page Class for Push Notification template page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of template page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h6[contains(text(),'Push Notifications')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "new_template_button": "//span[text()='CREATE NEW TEMPLATE']",
            "type": "//div[@id='demo-select-filled-type']",
            "category": "(//div[@id='demo-select-filled-category'])[2]",
            "name": "//input[@id='filled-basic-templateName']",
            "title": "//input[@id='filled-basic-templateTitle']",
            "text": "//textarea[@id='filled-basic-template']",
            "save": "//span[text()='SAVE']",
            "delete_template": "//*[text()='DELETE']",
            "del_text": "//h6[text()='%s']",
            "close_button": "//button[@aria-label='close']//span[@class='MuiIconButton-label']//*[name()='svg']"
        })

    def click_new_template_button(self):
        """
        To click on tabs from the dashboard
        """
        self.webDriver.click(element=self.locators.new_template_button, locator_type="xpath")

    def create_random_template_title(self, length):
        """
        To generate random notification title
        :param length:
        :return:
        """
        title = ''.join((random.choice(string.ascii_letters) for x in range(length)))
        return title

    def create_template(self, test_data):
        """
        create template
        :param test_data:
        :return:
        """
        self.webDriver.move_to_element_and_double_click(element=self.locators.type, locator_type="xpath")
        self.webDriver.move_to_element_and_double_click(element=self.locators.category, locator_type="xpath")
        random_text = self.create_random_template_title(3)
        self.webDriver.click(element=self.locators.name, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.name, locator_type="xpath", text="template name " + random_text)
        random_title = self.create_random_template_title(5)
        self.webDriver.click(element=self.locators.title, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.title, locator_type="xpath", text="template title " + random_title)
        test_data['templateTitle'] = "template title " + random_title
        random_text = self.create_random_template_title(5)
        self.webDriver.click(element=self.locators.text, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.text, locator_type="xpath",text="Automated template text " + random_text)
        self.webDriver.click(element=self.locators.save, locator_type="xpath")

    def delete_used_template_and_verify(self):
        """
        To verify user is not able to delete template which is currently used in scheduled notifications
        :return:
        """
        delete_text = "Request denied as this template is currently in use"
        self.webDriver.click(element=self.locators.delete_template, locator_type="xpath")
        if not delete_text == self.webDriver.get_text(element=self.locators.del_text % delete_text, locator_type='xpath'):
            raise Exception('User is able to delete the used templates')
        else:
            self.webDriver.click(element=self.locators.close_button, locator_type="xpath")