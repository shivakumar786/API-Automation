__author__ = 'saloni.pattnaik'

from selenium.webdriver.common.keys import Keys
from virgin_utils import *


class DistributionList(General):
    """
    Page Class for Push Notification distribution list page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of distribution list page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "(//*[text()='Distribution Lists'])[2]",
            "loader": "//*[@class='LoaderContainer__div']//img",
            "create_distribution_button": "//button//span[text()='CREATE NEW DISTRIBUTION LIST']",
            "distribution_list_box": "//div[@id='customized-dialog-title']//h6",
            "recipients": "//div[@data-cy='recipients-dropdown']//input[@type='text']",
            "select_cabin_button": "//span[text()='Select Cabins']",
            "all_checkbox": "//input[@name='checkedCabins']/..",
            "deck_list": "//div[@class='decks-listing']/div",
            "deck": "//div[@class='decks-listing']/div[%s]",
            "all_cabin_checkbox": "//input[@name='All']",
            "ok_button": "//span[text()='OK']",
            "view_list_checkbox": "//input[@type='checkbox']",
            "added_cabins_count": "//div//h6[text()='Total Selected']//span",
            "list_name": "//input[@id='filled-basic-name']",
            "type": "//div[@id='demo-select-filled-type']",
            "create_button": "//button//span[text()='CREATE']",
            "search_bar": "//input[@placeholder='Search by keyword']",
            "distribution_list": "//div[@class='MuiCardContent-root']//mark",
            "view_details_button": "(//div[@class='MuiCardContent-root']//mark)[%s]/../../../../..//span[text()='VIEW DETAILS']",
            "total_recipients": "//h6[text()='Total Recipients']//span",
            "sailor": "//input[@aria-activedescendant='mui-43615-option-0']",
            "close": "//button[@aria-label='close']",
        })

    def wait_for_loader_to_complete(self):
        """
        Function to wait for page loading to complete
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_header(self):
        """
        To verify page header of distribution list
        """
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "Distribution Lists":
            logger.debug("User is land on distribution page of Push Notification")
        else:
            raise Exception("user is not on distribution page of Push Notification")

    def create_new_distribution_list(self, test_data):
        """
        To create new distribution list
        :param test_data:
        """
        self.webDriver.click(element=self.locators.create_distribution_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        if self.webDriver.is_element_display_on_screen(element=self.locators.distribution_list_box, locator_type='xpath'):
            if self.webDriver.get_text(element=self.locators.distribution_list_box, locator_type='xpath') == "Create New Distribution List":
                self.webDriver.set_text(element=self.locators.recipients, locator_type='xpath', text='sailor')
                self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ARROW_DOWN)
                self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ENTER)
                self.webDriver.click(element=self.locators.select_cabin_button, locator_type='xpath')
                self.webDriver.click(element=self.locators.ok_button, locator_type='xpath')
                total_cabin_count = self.get_cabin_list_count()
                name = self.create_random_distribution_list_name(3)
                test_data['distribution_list_name'] = "Dist_list_auto_" + name
                self.webDriver.set_text(element=self.locators.list_name, locator_type='xpath',
                                        text=test_data['distribution_list_name'])
                self.webDriver.move_to_element_and_double_click(element=self.locators.type, locator_type='xpath')
                self.webDriver.click(element=self.locators.create_button, locator_type='xpath')
                self.wait_for_loader_to_complete()
                return total_cabin_count
            else:
                raise Exception("new distribution dialog box is not displaying")

    def verify_created_distribution_list(self, test_data):
        """
        To verify created distribution list is coming in distribution list or not
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.search_bar, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.search_bar, locator_type='xpath',
                                text=test_data['distribution_list_name'])
        self.webDriver.get_web_element(element=self.locators.search_bar, locator_type='xpath').send_keys(Keys.ENTER)
        self.wait_for_loader_to_complete()
        distribution_list = self.webDriver.get_elements(element=self.locators.distribution_list, locator_type='xpath')
        for name in distribution_list:
            if name.text == test_data['distribution_list_name']:
                return True
            else:
                return False

    def verify_cabin_count(self, test_data):
        """
        To verify added cabin count is matching or not
        :param test_data:
        :return:
        """
        distribution_list = self.webDriver.get_elements(element=self.locators.distribution_list, locator_type='xpath')
        for name in range(0, len(distribution_list)):
            if distribution_list[name].text == test_data['distribution_list_name']:
                self.webDriver.click(element=self.locators.view_details_button % (name+1), locator_type='xpath')
                self.wait_for_loader_to_complete()
                recipient = self.webDriver.get_text(element=self.locators.total_recipients, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.close, locator_type='xpath', time_out=60)
                self.webDriver.click(element=self.locators.close, locator_type='xpath')
                return recipient

    def get_deck_list_count(self):
        """
        To get the count of deck list
        :return:
        """
        return self.webDriver.get_elements(element=self.locators.deck_list, locator_type='xpath')

    def create_random_distribution_list_name(self, length):
        """
        To generate random distribution list name
        :param length:
        :return:
        """
        name = ''.join((random.choice(string.ascii_letters) for x in range(length)))
        return name

    def get_cabin_list_count(self):
        """
        To get the cabin list count after adding cabins
        :return:
        """
        self.webDriver.click(element=self.locators.view_list_checkbox, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.scroll_till_element(element=self.locators.added_cabins_count, locator_type='xpath')
        return self.webDriver.get_text(element=self.locators.added_cabins_count, locator_type='xpath')

