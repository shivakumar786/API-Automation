__author__ = 'vanshika.arora'

from virgin_utils import *


class Summary(General):
    """
    Page class for summary screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "title_summary_Screen": "//h1[@class='PageTitle ExcursionsPaymentSummary__title']",
            "event_schedule": "//div[@class='BookingSummaryHeading__date']",
            "event_title": "//h2[@class='PageSubTitle']",
            "event_location": "//div[@class='Pad Pad__cornered_primary BookingSummaryPlace RemoveDashedBorder RemoveBackground']",
            "guest_number": "//div[@class='Attendees__img']",
            "confirm": "//button[@id='ExcursionsPaymentSummary__confirmButton']",
            "add_card_and_pay": "//button[@id='ExcursionsPaymentSummary__confirmButton']",
        })

    def verify_summary_screen(self):
        """
        To verify that sailor is on summary screen
        :return:
        """
        title = self.webDriver.get_text(element=self.locators.title_summary_Screen, locator_type='xpath')
        if title == "Summary":
            logger.debug('User has landed on summary screen')
        else:
            raise Exception('User has not landed on summary screen after clicking next')

    def save_details_on_summary_screen(self, test_data):
        """
        To save details on summary screen
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        test_data['summary_event_title'] = self.webDriver.get_text(element=self.locators.event_title, locator_type='xpath')
        test_data['summary_event_schedule'] = self.webDriver.get_text(element=self.locators.event_schedule, locator_type='xpath')
        test_data['summary_event_location'] = self.webDriver.get_text(element=self.locators.event_location, locator_type='xpath')
        test_data['summary_no_of_guests'] = len(self.webDriver.get_elements(element=self.locators.guest_number, locator_type='xpath'))

    def click_confirm_button(self):
        """
        To click confirm button on summary screen
        :return:
        """
        self.webDriver.click(element=self.locators.confirm, locator_type='xpath')

    def click_add_card_and_pay(self):
        """
        Function to click add card and pay button
        :return:
        """
        self.webDriver.click(element=self.locators.add_card_and_pay, locator_type='xpath')

    def click_pay_with_existing_card(self):
        """
        Function to click pay with existing card
        :return:
        """
        self.webDriver.click(element=self.locators.confirm, locator_type='xpath')

    def save_edited_spa_details(self, test_data):
        """
        To save event details
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        test_data['lineup_title'] = self.webDriver.get_text(element=self.locators.lineup_title,
                                                            locator_type='xpath')
        test_data['lineup_schedule'] = self.webDriver.get_text(element=self.locators.lineup_schedule,
                                                               locator_type='xpath')
        test_data['lineup_guest_count'] = len(self.webDriver.get_elements(element=self.locators.lineup_guest_count,
                                                                          locator_type='xpath'))

    def verify_booking_confirmation_screen(self):
        """
        To verify booking confirmation screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booking_confirmation,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.done_btn,
                                                       locator_type='xpath'):
            logger.info("Booking confirmation page is getting displayed")
        else:
            raise Exception("Booking confirmation page is not getting displayed")

