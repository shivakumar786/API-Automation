__author__ = 'prahlad.sharma'

from virgin_utils import *


class SelectShip(General):
    """
    Page class for Ship Selection Page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = General.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "header": "//span[contains(text(),'Select Ship')]",
            "all_ships": "//div[@class='column is-one-third false']//div//img",
            "all_ships_name": "//div[@class='column is-one-third false']//div//img/../following-sibling::div",
            "next_button": "//span[contains(text(),'NEXT')]",
            "ship_name": "//div[text()='%s']/preceding-sibling::div"
        })

    def select_ship(self, test_data):
        """
        To get the ship name
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.header, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_name % test_data['shipName'], locator_type='xpath')
        self.webDriver.allure_attach_jpeg('select_ship')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    # def select_ship(self):
    #     """
    #     To select the Ship from Ship Page
    #     """
    #     self.webDriver.click(element=self.locators.all_ships, locator_type='xpath')
    #     self.webDriver.allure_attach_jpeg('select_ship')
    #     self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def verify_ship_page_availability(self):
        """
        Function to verify ship page availability
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.all_ships, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('ship_page_available')
        return self.webDriver.is_element_display_on_screen(element=self.locators.all_ships, locator_type='xpath')
