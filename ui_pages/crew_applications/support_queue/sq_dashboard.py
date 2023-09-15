__author__ = 'aatir.fayyaz'

from virgin_utils import *


class SupportQueue(General):
    """
    Page class for Support Queue page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "support_queue_header": "//*[@text='Support Queue']",
            "dashboard_header": "//*[@text='Dashboard']",
            "search_button": "//*[@class='android.widget.Button'][1]",
            "search_by_name_cabin": "//*[@class='android.widget.EditText'][1]",
            "close_search_button": "//*[@text='menu']",
            "notification_tab": "//button[@class='MuiButtonBase-root MuiIconButton-root jss295 MuiIconButton-edgeEnd']",
            "filter_icon": "//*[@class='android.widget.Button'][contains(@text,'logo')]",
            "filter_header_title": "//*[@class='android.widget.TextView'][contains(@text,'Apply Filter')]",
            "new_request_button": "//*[contains(@text,'NEW')]",
            "in_progress_request_button": "//*[contains(@text,'IN PROGRESS')]",
            "in_progress_sailor": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "resolved_request_button": "//*[contains(@text,'RESOLVED')]",
            "open_resolved_chat": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "new_chat_button": "//*[@class='android.widget.Image'][@text='logo'][@index='3']",
            "search_sailor": "//button[@class='MuiButtonBase-root MuiIconButton-root jss294 MuiIconButton-colorPrimary MuiIconButton-edgeEnd']",
            "resolved_message": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "resolved_close_button": "//*[@class='android.widget.Button'][@text='menu'][@index='0']",
        })

    def verify_support_queue_header(self):
        """
        verify support queue header on top left corner of support queue after login
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.support_queue_header, locator_type='xpath',
                                                      time_out=120)
        application_name = self.webDriver.get_text(element=self.locators.support_queue_header, locator_type='xpath')
        if application_name == 'Support Queue':
            logger.debug("Support queue header is available on top left corner")
        else:
            self.webDriver.allure_attach_jpeg('support_queue_header_on_top_left_corner')
            raise Exception("Support queue header is not available on top left corner")

    def availability_of_new_chat_button(self):
        """
        availability of new chat button
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.new_chat_button, locator_type='xpath'):
            logger.debug("New chat button is available")
        else:
            self.webDriver.allure_attach_jpeg('availability_of_new_chat_button')
            raise Exception("New chat button is not available")

    def click_new_chat_button(self):
        """
        Click new chat button
        :return:
        """
        self.webDriver.click(element=self.locators.new_chat_button, locator_type='xpath')

    def verify_sailor_in_progress_section(self, sailor_name):
        """
        Function to verify in progress status of sailor after initiating chat
        :param sailor_name:
        :return:
        """
        sailor_fname = sailor_name[0].split()[0]
        self.webDriver.click(element=self.locators.search_button, locator_type="xpath")
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.search_by_name_cabin, locator_type="xpath", text=sailor_fname)
        self.webDriver.submit()
        self.webDriver.click(element=self.locators.in_progress_request_button, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.in_progress_sailor % sailor_fname,
                                                      locator_type='xpath', time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.in_progress_sailor % sailor_fname,
                                                       locator_type='xpath'):
            logger.debug("Sailor has correct in progress status")
            self.webDriver.click(element=self.locators.close_search_button, locator_type="xpath")
        else:
            self.webDriver.allure_attach_jpeg('verify_sailor_in_progress_section')
            raise Exception("Sailor does not have correct in progress status")

    def open_sailor_chat(self, sailor_name):
        """
        Click new chat button
        :param sailor_name:
        :return:
        """
        sailor_fname = sailor_name[0].split()[0]
        self.webDriver.click(element=self.locators.in_progress_request_button, locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(element=self.locators.in_progress_sailor % sailor_fname,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.in_progress_sailor % sailor_fname, locator_type="xpath")

    def verify_chat_mark_as_resolved(self, sailor_cabin, sailor_name):
        """
        Function to verify chat mark as resolved
        :param sailor_cabin:
        :param sailor_name:
        :return:
        """
        self.webDriver.click(element=self.locators.search_button, locator_type="xpath")
        self.webDriver.set_text(element=self.locators.search_by_name_cabin, locator_type="xpath", text=sailor_cabin)
        self.webDriver.submit()
        self.webDriver.click(element=self.locators.resolved_request_button, locator_type="xpath")
        if self.webDriver.is_element_display_on_screen(element=self.locators.open_resolved_chat % sailor_name[0],
                                                       locator_type='xpath'):
            logger.debug(f"Sailor {sailor_name[0]} is there in resolved request")
        else:
            self.webDriver.allure_attach_jpeg('verify_chat_mark_as_resolved')
            raise Exception(f"Sailor {sailor_name[0]} is not there in resolved request")

    def verify_history_of_resolved_request(self, test_data):
        """
        Function to verify history of resolved request
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.open_resolved_chat % test_data['sailor_name'][0],
                             locator_type="xpath")
        self.webDriver.explicit_visibility_of_element(
            element=self.locators.open_resolved_chat % 'Canned message', locator_type='xpath',
            time_out=60)
        if self.webDriver.is_element_display_on_screen(
                element=self.locators.resolved_message % 'Canned message', locator_type='xpath'):
            logger.debug("Previously sent message is visible in history of resolved request")
            self.webDriver.click(element=self.locators.resolved_close_button, locator_type="xpath")
        else:
            self.webDriver.allure_attach_jpeg('verify_history_of_resolved_request')
            raise Exception("Previously sent message is not visible in history of resolved request")

    def click_filter_icon(self):
        """
        Function to click on filter icon
        :return:
        """
        self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header_title, locator_type='xpath',
                                                      time_out=60)

    def back_to_filter(self):
        """
        Function to back to filter page
        :return:
        """
        self.webDriver.click(element=self.locators.close_search_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header_title, locator_type='xpath',
                                                      time_out=60)

    def back_to_crew_dashboard(self):
        """
        Function to back to Crew App Dashboard page
        :return:
        """
        self.webDriver.mobile_native_back()
        self.webDriver.explicit_visibility_of_element(element=self.locators.dashboard_header, locator_type='xpath',
                                                      time_out=120)

