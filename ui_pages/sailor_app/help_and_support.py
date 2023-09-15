__author__ = 'vanshika.arora'

from virgin_utils import *


class Help_and_Support(General):
    """
    Page class for Help And Support page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "help_and_support_header": "//h1[text()='Let us help you out...']",
            "help_and_support_search": "//div[@class='ServicesSupportLanding__search-bar']",
            "search_keyword_bar": "//input[@id='SearchInput']",
            "search_output": "//div[@class='MenuItem__title']",
            "total_search_output": "//div[@class='SupportSearch__title']",
            "before_you_sail": "//span[text()='Before You Sail']",
            "the_days_at_sea": "//span[text()='The Days at Sea']",
            "back_on_dry_land": "//span[text()='The Days at Sea']",
            "help_email_button": "//button[@id='HelpEmailBtn']",
            "help_call_button": "//button[@id='HelpCallBtn']",
            "search_title": "//div[@class='SupportSearch__title']",
            "search_menu_items": "//div[@class='MenuItem']",
            "result_page_title": "//h1[@class='PageTitle']/span",
        })

    def verify_help_and_support_header(self):
        """
        Verify header of Help And Support section
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.help_and_support_header, locator_type='xpath'):
            logger.debug("User has landed on Help And Support screen")
        else:
            raise Exception("User has not landed on Help And Support screen")

    def verify_availability_of_search_bar(self):
        """
        Verify availability of search bar in help and support
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.help_and_support_search,
                                                       locator_type='xpath'):
            logger.debug("User is able to see search bar in help and support")
        else:
            raise Exception("User is not able to see search bar in help and support")

    def search_keyword(self):
        """
        Search a keyword to get results in help and support search
        :return:
        """
        self.webDriver.click(element=self.locators.help_and_support_search, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.search_keyword_bar, locator_type='xpath', text='Water')

    def verify_availability_of_search_results(self):
        """
        To verify results are available after seraching keyword
        :return:
        """
        search_title = self.webDriver.get_text(element=self.locators.search_title, locator_type='xpath')
        no_of_results = int(search_title.split('(')[1][0:2])
        get_all_search_results = self.webDriver.get_elements(
            element=self.locators.search_menu_items, locator_type='xpath')
        assert no_of_results == get_all_search_results, "Correct serach results are not available"

    def verify_help_and_support_question_categories(self):
        """
        Verify questions categories available on help and support screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.before_you_sail,
                                                       locator_type='xpath'):
            logger.debug("User is able to see questions categories in help and support")
        else:
            raise Exception("User is not able to questions categories in help and support")

        if self.webDriver.is_element_display_on_screen(element=self.locators.the_days_at_sea,
                                                       locator_type='xpath'):
            logger.debug("User is able to see questions categories in help and support")
        else:
            raise Exception("User is not able to see questions categories in help and support")

        if self.webDriver.is_element_display_on_screen(element=self.locators.back_on_dry_land,
                                                       locator_type='xpath'):
            logger.debug("User is able to see questions categories in help and support")
        else:
            raise Exception("User is not able to see questions categories in help and support")

    def verify_availability_of_email_and_call_buttons(self):
        """
        To verify that email and call buttons are available on help and support screen
        :return:
        """
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        current_time = datetime_ist.strftime('%H:%M:%S')
        if "09:00:00" <= current_time <= "18:00:00":
            if self.webDriver.is_element_display_on_screen(element=self.locators.help_call_button,
                                                           locator_type='xpath'):
                logger.debug("User is able to see call button in help and support")
            else:
                raise Exception("User is not able to see call button in help and support")

        if self.webDriver.is_element_display_on_screen(element=self.locators.help_email_button,
                                                       locator_type='xpath'):
            logger.debug("User is able to see email button in help and support")
        else:
            raise Exception("User is not able to see email button in help and support")

    def open_questions_in_search_results(self):
        """
        Verify user is able to open
        :return:
        """
        get_all_search_results = self.webDriver.get_elements(
            element=self.locators.search_menu_items, locator_type='xpath')
        for result in get_all_search_results:
            result_question = result.text
            result.click()
            break
        result_page_title = self.webDriver.get_text(element=self.locators.result_page_title, locator_type='xpath')
        assert result_page_title == result_question, "User is not able open and view details of questions in search results"








