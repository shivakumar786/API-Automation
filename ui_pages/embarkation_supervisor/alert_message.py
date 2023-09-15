__author__ = 'prahlad.sharma'

from virgin_utils import *


class Alertmessage(General):
    """
    Page Class for alert and message page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of alert and message page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "alert_tab": "//li/button[contains(text(),'ALERTS')]",
            "message_tab": "//li/button[contains(text(),'MESSAGES')]",
            "new_message_button": "//span[contains(text(),'NEW MESSAGE')]",
            "new_alert_button": "//span[contains(text(),'NEW ALERT')]",
            "add_passenger": "//span[contains(text(),'Add Passengers')]",
            "add_passenger_header": "//div[@class='title is-4 has-text-left']//span[contains(text(),'Add Passenger')]",
            "search_textbox": "//input[@name='search']",
            "add_button": "//span[contains(text(),'ADD')]",
            "cancel_button": "//button[contains(@class,'button is-primary-outline')]//span[contains(text(),'CANCEL')]",
            "search_button": "//span[contains(text(),'SEARCH')]",
            "checkbox": "//td/span[@class='checkbox is-pulled-left ']/span/img",
            "passenger_name": "//td/span[@class='checkbox is-pulled-left checked']/label/span",
            "table_passenger_name": "//td[contains(text(),'%s')]",
            "total_columns": "//div[@class='TabContent active']//tr[1]//td"
        })

    def blank_list(self):
        """
        Verification of blank list
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_records, locator_type='xpath'):
            return True
        else:
            return False

    def click_new_alert(self):
        """
        Function to click on new alert button
        """
        self.webDriver.click(element=self.locators.new_alert_button, locator_type='xpath')

    def click_new_message(self):
        """
        Function to click on new message button
        """
        self.webDriver.click(element=self.locators.new_message_button, locator_type='xpath')

    def click_alert_tab(self):
        """
        Function to click on alert tab
        """
        self.webDriver.click(element=self.locators.alert_tab, locator_type='xpath')

    def click_message_tab(self):
        """
        Function to click on message tab
        """
        self.webDriver.click(element=self.locators.message_tab, locator_type='xpath')

    def click_add_passenger(self):
        """
        Function to click on add passenger
        """
        self.webDriver.click(element=self.locators.add_passenger, locator_type='xpath')

    def click_add_button(self):
        """
        Function to click on add passenger
        """
        self.webDriver.click(element=self.locators.add_button, locator_type='xpath')

    def search_passengers(self, search_parameter):
        """
        Function to search the passenger
        :param search_parameter:
        """
        self.webDriver.set_text(element=self.locators.search_textbox, locator_type='xpath', text=search_parameter)
        self.webDriver.click(element=self.locators.search_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_checkbox_on_passenger_search_and_get_passenger_name(self):
        """
        Function is used to tick the check box
        """
        index = None
        passenger_name = None
        all_checkbox = self.webDriver.get_elements(element=self.locators.checkbox, locator_type='xpath')
        if len(all_checkbox) > 0:
            for check in all_checkbox:
                index = all_checkbox.index(check)
                check.click()
                break

        all_passenger = self.webDriver.get_elements(element=self.locators.passenger_name, locator_type='xpath')
        for passenger in all_passenger:
            if all_passenger.index(passenger) == index:
                passenger_name = passenger.text
                break
        self.webDriver.allure_attach_jpeg('check_box_selected')
        return passenger_name

    def verify_added_passenger(self, passenger_name):
        """
        Function to verify the passenger name
        :param passenger_name:
        """
        self.webDriver.scroll_complete_page()
        display_passenger = self.webDriver.get_text(element=self.locators.table_passenger_name % passenger_name,
                                                    locator_type='xpath')

        self.webDriver.allure_attach_jpeg('passenger_in_details_page')

        if display_passenger == passenger_name:
            logger.debug("Passenger added in list")
        else:
            raise Exception("Passenger is not added in list")
