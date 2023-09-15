__author__ = 'mohit.raghav'

from virgin_utils import *


class Events_my_agenda(General):
    """
    Page class for events in my agenda
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'booked_lineup_title': "//h1[@class='PageTitle withHypen']",
            'booked_lineup_details': "//div[@class='BookingDetailsSummary__data-location-label']",
            'booked_sailor_avatar': "//div[@class='BookingDetailsSummary__guests']//img",
            "edit_booking_details": "//button[@id='editButton']",
            "remove_secondary_sailor": "//div[@id='user_avatar_1']",
            "next_button": "//button[@id='nextButton']",
            "cancel_booking": "//button[@id='cancelBtn']",
            "confirm_cancel": "//button[@id='confirmCancellationButton']",
            'cancel_for_all': "//button[@id='groupCancellationButton']",
            "canceled_header": "//h1[text()='Canceled']",
            "canceled_text": "//div[@class='CompletePageDescription']",
            'done_btn': "//button[@id='CompletePage__doneButton']",
            'close_to_start_time_text': "//div[@class='WithoutCancellationModalContent']",
            'ok_btn': "//button[@id='withoutCancellationOkButton']",
            'time_slots': "//div[@class='time-item']",
            'time_slot_selected': "//div[@class='time-item selected']"
        })

    def verify_booked_event_title(self, test_data):
        """
        To verify booked event title in my agenda event details page
        :param test_data:
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booked_lineup_title,
                                                          locator_type='xpath')
        booked_lineup_title = self.webDriver.get_text(element=self.locators.booked_lineup_title, locator_type='xpath')
        if booked_lineup_title == test_data['lineup_title']:
            logger.info('Correct lineup title is displayed on event detail screen')
        else:
            raise Exception('Incorrect lineup title is displayed on event detail screen')

    def verify_booked_event_schedule_and_location(self, test_data):
        """
        To verify booked event schedule in my agenda event details page
        :param test_data:
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booked_lineup_details,
                                                          locator_type='xpath')
        booked_lineup_details = self.webDriver.get_elements(element=self.locators.booked_lineup_details,
                                                            locator_type='xpath')
        details = [detail.text for detail in booked_lineup_details]
        if details[1] == test_data['lineup_location']:
            logger.info("Correct lineup location is getting displayed.")
        else:
            raise Exception("Incorrect lineup location is getting displayed.")
        if details[0].lower() == test_data['lineup_schedule'].split(",")[0].lower():
            logger.info("Correct lineup schedule is getting displayed.")
        else:
            raise Exception("Incorrect lineup schedule is getting displayed.")

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

    def click_edit_booking_details(self, test_data, event):
        """
        To click edit booking details
        :param test_data:
        :param event:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.edit_booking_details,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.edit_booking_details, locator_type='xpath')
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.close_to_start_time_text,
                                                       locator_type='xpath'):
            logger.info("Sailor can’t amend a booking so close to to the start time.")
            test_data[f'{event}_editing'] = False
            self.webDriver.click(element=self.locators.ok_btn, locator_type='xpath')
            return
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.edit_booking_details,
                                                               locator_type='xpath')
        test_data[f'{event}_editing'] = True

    def edit_booking(self):
        """
        To edit booked linneup
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.remove_secondary_sailor,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.remove_secondary_sailor, locator_type='xpath')
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.next_button, locator_type='xpath'):
            self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.remove_secondary_sailor, locator_type='xpath')
            time_slots = self.webDriver.get_elements(element=self.locators.time_slots, locator_type='xpath')
            slot = random.choice(time_slots)
            slot.click()
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_button,
                                                              locator_type='xpath')
            self.webDriver.click(element=self.locators.next_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_button,
                                                               locator_type='xpath')

    def cancel_booking(self):
        """
        To cancel booking for whole group
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cancel_booking,
                                                          locator_type='xpath')
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.cancel_booking, locator_type='xpath')
        self.webDriver.wait_for(4)
        if self.webDriver.is_element_display_on_screen(element=self.locators.confirm_cancel,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.confirm_cancel, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.confirm_cancel,
                                                                   locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.cancel_for_all, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.cancel_for_all,
                                                                   locator_type='xpath')

    def verify_cancelled_screen(self):
        """
        To verify cancelation screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.canceled_header,
                                                          locator_type='xpath')
        canceled_text = self.webDriver.get_text(element=self.locators.canceled_text, locator_type='xpath')
        if canceled_text == 'Your spot has been canceled for' or 'Your group has been canceled for':
            logger.info("Event has been canceled")
        else:
            raise Exception("Event has not been canceled")

    def click_done(self):
        """
        To click Done btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.done_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.done_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.done_btn, locator_type='xpath')

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


