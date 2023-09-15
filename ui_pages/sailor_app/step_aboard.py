__author__ = 'vanshika.arora'

import random

from virgin_utils import *


class Step_aboard(General):
    """
    Page class for step aboard page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "embarkation_flight_question": "//div[@class='question']",
            "inbound_select_yes": "//label[@id='yesBtn']",
            "open_inbound_flight_list": "//input[@id='FlightForm-airlineSelect']",
            "select_inbound_flight_name": "//div[text()='1time']",
            "inbound_flight_number": "//input[@id='FlightForm-flightNumberInput']",
            "inbound_arrival_time": "//input[@id='FlightForm-arrivalTimeInput']",
            "select_inbound_hours": "//android.widget.RadialTimePickerView.RadialPickerTouchHelper[@content-desc='2']",
            "select_inbound_minutes": "//android.widget.RadialTimePickerView.RadialPickerTouchHelper[@content-desc='0']",
            "set_time": "//*[@text='SET']",
            "next_cta": "//button[@id='submit']",
            "select_arrival_time_slot": "//div[@class='FlightDetails__availableSlot'][1]",
            "get_arrival_time": "//div[@class='FlightDetails__availableSlot'][1]/label/span",
            "yes_parking_button": "//span[text()='Yes']",
            "sailormate": "//label[@class='form-control-checkbox']",
            "click_done_cta": "//button[@id='FlightDetails-whoIsArrivingSuccessButton']/span",
            "select_debarkation_not_flying_button": "//label[@id='notFlyingBtn']",
            "skip_email_or_call": "//button[@id='FlightDetails-skipButton']",
            "timer_header": "android:id/time_header",
            "selected_inbount_flight_name": "//div[@class='FlightCard']/div[3]/div[1]/div",
            "selected_inbount_flight_number": "//div[@class='FlightCard']/div[3]/div[2]/div",
            "selected_inbount_flight_time": "//div[@class='FlightCard']/div[3]/div[3]/div",
            "arrive_in_style_header": "//h1[@class='PageTitle']",
            "book_a_driver": "//div[@class='question']",
            "driver_not_needed": "//label[@id='notNeededBtn']",
            "enter_flight_detail_question": "//div[@class='question']",
            "get_selected_embarkation_slot": "//div[text()='Time']/following-sibling::div"
        })

    def verify_user_landed_on_embarkation_flight_question(self):
        """
        Function to verify that embarkation flight question should be available on screen
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.embarkation_flight_question, locator_type='xpath'
                                                      , time_out=60)
        embarkation_flight_question = self.webDriver.get_text(element=self.locators.embarkation_flight_question, locator_type='xpath')
        assert embarkation_flight_question == "Do you plan to fly in on the day of embarkation?","User has not landed on embarkation flight question"

    def select_yes_for_embarkation_flight(self):
        """
        Function to select yes for if user wants to fly in on embarkation day
        """
        self.webDriver.click(element=self.locators.inbound_select_yes, locator_type='xpath')

    def fill_inbound_flight_details(self):
        """
        Function to enter inbound flight details
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.enter_flight_detail_question,
                                                      locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.open_inbound_flight_list, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_inbound_flight_name, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.inbound_flight_number, locator_type='xpath', text="100")
        self.webDriver.click(element=self.locators.inbound_arrival_time, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.explicit_visibility_of_element(element=self.locators.timer_header, locator_type='id'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.select_inbound_hours, locator_type='xpath')
        self.webDriver.click(element=self.locators.select_inbound_minutes, locator_type='xpath')
        self.webDriver.click(element=self.locators.set_time, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.next_cta, locator_type='xpath')

    def select_arrival_time_slot(self, test_data):
        """
        Function to select and get arrival time slot
        """
        test_data['selected_arrival_time'] = self.webDriver.get_text(element=self.locators.get_arrival_time,
                                                                     locator_type='xpath')
        self.webDriver.click(element=self.locators.select_arrival_time_slot, locator_type='xpath')

    def click_parking_button(self):
        """
        Select yes for if user is planning to park at the port
        """
        self.webDriver.click(element=self.locators.yes_parking_button, locator_type='xpath')

    def skip_email_call(self):
        """
        Function to skip email or call
        """
        self.webDriver.click(element=self.locators.skip_email_or_call, locator_type='xpath')

    def select_sailor_mate(self):
        """
        Function to click sailormate checkbox
        """
        self.webDriver.click(element=self.locators.sailormate, locator_type='xpath')
        self.webDriver.click(element=self.locators.click_done_cta, locator_type='xpath')

    def select_no_for_debarkation_flight(self):
        """
        Function to select yes for if user wants to fly in on embarkation day
        """
        self.webDriver.click(element=self.locators.select_debarkation_not_flying_button, locator_type='xpath')

    def verify_correct_flight_details_availeble(self):
        """
        Function to verify availability of correct flight details
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.selected_inbount_flight_name, locator_type='xpath'
                                                      , time_out=60)
        flight_name = self.webDriver.get_text(element=self.locators.selected_inbount_flight_name, locator_type='xpath')
        flight_number = self.webDriver.get_text(element=self.locators.selected_inbount_flight_number, locator_type='xpath')
        flight_time = self.webDriver.get_text(element=self.locators.selected_inbount_flight_time, locator_type='xpath')
        assert flight_name == "1time", "Correct flight name is not shown on emarkation slot selection page"
        assert flight_number == "100", "Correct flight number is not shown on emarkation slot selection page"
        assert flight_time == "02:00am", "Correct flight time is not shown on emarkation slot selection page"

    def verify_arrive_in_style_page(self):
        """
        Function to verify arrive in style page
        """
        arrive_in_style_text = self.webDriver.get_text(element=self.locators.arrive_in_style_header,
                                                              locator_type='xpath')
        flight_name = self.webDriver.get_text(element=self.locators.selected_inbount_flight_name, locator_type='xpath')
        flight_number = self.webDriver.get_text(element=self.locators.selected_inbount_flight_number,
                                                locator_type='xpath')
        flight_time = self.webDriver.get_text(element=self.locators.selected_inbount_flight_time, locator_type='xpath')
        book_a_driver = self.webDriver.get_text(element=self.locators.book_a_driver, locator_type='xpath')
        assert flight_name == "1time", "Correct flight name is not shown on emarkation slot selection page"
        assert flight_number == "100", "Correct flight number is not shown on emarkation slot selection page"
        assert flight_time == "02:00am", "Correct flight time is not shown on emarkation slot selection page"
        assert arrive_in_style_text == "Arrive in style", "Correct arrive in style text is not available"
        assert book_a_driver == "Would you like to book a driver?", "Coorect book a driver question is available on arrive in style page"

    def verify_embarkation_slot(self, test_data):
        """
        FUnction to verify correct embarkation slot is displayed
        """
        get_embarkation_slot = self.webDriver.get_text(element=self.locators.get_selected_embarkation_slot, locator_type='xpath')
        assert get_embarkation_slot == test_data['selected_arrival_time'], "Correct embarkation slot is not shown"

    def select_no_for_book_a_driver(self):
        """
        Function to select for question Would you like to book a driver?
        """
        self.webDriver.click(element=self.locators.driver_not_needed, locator_type='xpath')

    def verify_availability_of_rock_up_page(self):
        """
        Function to verify availability of rock up page
        """
        rock_up_header = self.webDriver.get_text(element=self.locators.arrive_in_style_header,
                                                       locator_type='xpath')
        assert rock_up_header == "Rock-up from 1:30pm & 8:30pm","Rock up page is not available"
