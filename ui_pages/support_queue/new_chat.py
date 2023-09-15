__author__ = 'Vanshika.Arora'

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
            "searched_sailor_name": "//p[text()=\"Sailor's Name / Cabin Number\"]/parent::div/div//button[1]/div[1]/span",
            "search_sailor": "//p[(text()=\"Sailor's Name / Cabin Number\")]/following-sibling::div/form/div/div/input",
            "search_icon": "//p[(text()=\"Sailor's Name / Cabin Number\")]/following-sibling::div/form/div/div/div/button/span/img",
            "click_searched_sailor": "//div[@id='customized-dialog-title']/following-sibling::div/div/div/button/div/span[text()='%s']",
            "user_not_available": "//h6[text()='This user is not available for chat']",
            "get_all_sailors": "//div[@data-testid='testing-usertype-cabin']/preceding-sibling::div/span",
            "click_on_sailor": "//div[@data-testid='testing-usertype-cabin']/preceding-sibling::div/span[contains(text(),'%s')]",
            "click_ok": "//button/span[text()='Ok']",
            "sailor_name": "//h6[text()='Sailor Details']/following-sibling::div//h5",
            "loader": "//div[@id='Spinner']"

        })

    def search_sailor(self, search_item):
        """
        Search sailor with name or cabin number
        :param search_item:
        """
        self.webDriver.set_text(element=self.locators.search_sailor, locator_type='xpath', text=search_item)
        self.webDriver.click(element=self.locators.search_icon, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_searched_sailor(self, test_data):
        """
        Function to click on searched sailor
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(5)
        get_all_sailors = self.webDriver.get_elements(element=self.locators.get_all_sailors, locator_type='xpath')
        sailors_in_cabin= []
        for sailor in get_all_sailors:
            sailors_in_cabin.append(sailor.text)
        for sailors in sailors_in_cabin:
            if sailors != '':
                test_data['sailor_name'] = sailors.lstrip()
                self.webDriver.click(self.locators.click_on_sailor % test_data['sailor_name'], locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=120)
                if self.webDriver.is_element_display_on_screen(element=self.locators.user_not_available,
                                                               locator_type='xpath'):
                    self.webDriver.click(element=self.locators.click_ok, locator_type='xpath')
                    self.webDriver.wait_for(2)
                else:
                    get_sailor_name = self.webDriver.get_text(element=self.locators.sailor_name, locator_type='xpath')
                    if get_sailor_name == test_data['sailor_name']:
                        logger.debug("Correct sailor name is displayed in sailor details in left side")
                        return
                    else:
                        self.webDriver.allure_attach_jpeg('verify_sailor_name_in_sailor_details')
                        raise Exception("Correct sailor name is not displayed in sailor details in left side")


    def save_sailor_name(self, test_data):
        """
        Function to save the sailor name with whom chat is initiated
        :param test_data:
        :return:
        """
        test_data['sailors_name'] = self.webDriver.get_text(element=self.locators.searched_sailor_name,
                                                           locator_type='xpath')

