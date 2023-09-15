from virgin_utils import *


class History:
    """
    Page Class For History page
    """

    def __init__(self, web_driver, test_data):
        """
        To initialise the locators
        :param web_driver
        :param test_data:
        """
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = General.dict_to_ns({
            "page_header": "//div[@class='col-xs-3 history-heading' and text()='History']",
        })

    def verification_of_history_page(self):
        """
        To check the History page loaded or not
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.page_header, locator_type='xpath'):
            logger.debug("User is land on History page of MOCI")
        else:
            raise Exception("User is not on History page of MOCI")
