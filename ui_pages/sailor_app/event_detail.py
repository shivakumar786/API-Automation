__author__ = 'vanshika.arora'

from virgin_utils import *


class Event_detail(General):
    """
    Page class for event detail screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "verify_event_name": "//h1[@class='PageTitle withHypen']",
            "no_of_guests": "//div[@class='BookingDetailsSummary__guests']/img",
            "edit_booking_details": "//button[@id='editButton']",
            "remove_secondary_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            "confirm": "//button[@id='ExcursionsPaymentSummary__confirmButton']",
            "lineup_location": "//div[@class='BookingDetailsSummary__card-section']/div[2]",
            "lineup_description": "//div[@class='item descr']",
            "lineup_day_And_date": "//div[@class='BookingDetailsSummary__card-section']/div[1]",
            "cancel_booking": "//button[@id='cancelBtn']",
            "for_whole_group": "//button[@id='groupCancellationButton']",
            "cancelled": "//h1[@class='PageTitle withHypen']",
            "canceled_for_text": "//div[@class='CompletePageDescription']",
            "done": "//button[@id='CompletePage__doneButton']",
            "yes_cancel_for_one_person": "//button[@id='confirmCancellationButton']",
            "time_slots": "//span[@class='timeslot-item']",
            "time_slot_selected": "//div[@class='time-item selected']",
        })

    def save_lineup_description(self, test_data):
        """
        To save location of lineup
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        test_data['lineup_location'] = self.webDriver.get_text(element=self.locators.lineup_location, locator_type='xpath')
        test_data['lineup_description'] = self.webDriver.get_text(element=self.locators.lineup_description, locator_type='xpath')

    def verify_event_name_on_event_detail_screen(self, test_data):
        """
        To verify event name on event detail screen
        :param test_data:
        :return:
        """
        event_name = self.webDriver.get_text(element=self.locators.verify_event_name, locator_type='xpath')
        if event_name == test_data['summary_event_title']:
            logger.debug('Correct event name available on event detail screen')
        else:
            raise Exception('Incorrect event name is displayed')

    def verify_number_of_guests_in_booking(self, no_of_guests):
        """
        To verify number of guests in booked event
        :param no_of_guests:
        :return:
        """
        get_no_of_guests = self.webDriver.get_elements(
            element=self.locators.no_of_guests, locator_type='xpath')
        if len(get_no_of_guests) == no_of_guests:
            logger.debug(f"Event is booked for {no_of_guests} sailors")
        else:
            raise Exception("Incorrect number of guests displayed on booking detail screen")

    def verify_event_day_and_date(self, test_data):
        """
        To verify event day and date on event details screen
        :param test_data:
        :return:
        """
        lineup_schedule = self.webDriver.get_text(element=self.locators.lineup_day_And_date, locator_type='xpath')
        if (test_data['summary_event_schedule'].split(',')[1]).lstrip() == lineup_schedule.upper():
            logger.debug("Correct event schedule is displayed on event detail screen")
        else:
            raise Exception("Incorrect event details displayed on event details screen")

    def click_edit_booking_details(self):
        """
        To click edit booking details cta
        :return:
        """
        self.webDriver.click(element=self.locators.edit_booking_details, locator_type='xpath')

    def edit_booking(self):
        """
        To edit a booked event
        :return:
        """
        self.webDriver.click(element=self.locators.remove_secondary_sailor, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')

    def cancel_booking(self):
        """
        To cancel booking for whole group
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.cancel_booking, locator_type='xpath')
        self.webDriver.click(element=self.locators.yes_cancel_for_one_person, locator_type='xpath')

    def verify_cancelled_screen_for_one_person(self):
        """
        To verify cancelation for whole group
        :return:
        """
        canceled_text = self.webDriver.get_text(element=self.locators.cancelled, locator_type='xpath')
        cancelled_for_text = self.webDriver.get_text(element=self.locators.canceled_for_text, locator_type='xpath')
        assert canceled_text == 'Canceled', 'Canceled text is not available on cancelation screen'
        assert cancelled_for_text == 'Your spot has been canceled for', 'Event has not been cancled for group'

    def click_done(self):
        """
        To click done cta
        :return:
        """
        self.webDriver.click(element=self.locators.done, locator_type='xpath')

    def edit_spa_booking(self):
        """
        To edit the booked spa
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.time_slots, locator_type='xpath')
        time_slots = self.webDriver.get_elements(element=self.locators.time_slots, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.time_slot_selected, locator_type='xpath'):
            slot_selected = self.webDriver.get_text(element=self.locators.time_slot_selected, locator_type='xpath')
            for slot in time_slots:
                if slot.text != slot_selected:
                    slot.click()
                    break
        else:
            random.choice(time_slots).click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_button,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_button,
                                                               locator_type='xpath')

    def verify_booked_event_guest_count(self, test_data):
        """
        To verify booked event guest count
        :param test_data:
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booked_sailor_avatar,
                                                          locator_type='xpath')
        booked_guest_count = len(self.webDriver.get_elements(element=self.locators.booked_sailor_avatar,
                                                             locator_type='xpath'))
        if booked_guest_count == test_data['lineup_guest_count']:
            logger.info('Correct guest count is displayed on event detail screen')
        else:
            raise Exception('Incorrect guest count is displayed on event detail screen')


