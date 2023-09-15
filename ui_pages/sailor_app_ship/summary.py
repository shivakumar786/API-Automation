__author__ = 'mohit.raghav'

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
            "summary_header": "//h1[text()='Summary']",
            'confirm_button': "//button[text()='Confirm']",
            'booking_confirmation': '//*[text()="You’re all booked in for"]',
            'view_in_sailor_log_btn': "//button[@id ='CompletePageLinkButton']",
            'done_btn': "//button[@id='CompletePage__doneButton']",
            'lineup_title': "//h1[@class='PageTitle withHypen']",
            'lineup_schedule': "//div[@class='BookingSummaryHeading__date']",
            'lineup_location': "//div[@class='Pad Pad__cornered_primary BookingSummaryPlace RemoveDashedBorder RemoveBackground']",
            'lineup_guest_count': "//div[@class='Attendees__img']",
            'summary_check_box': "//label[@class='form-control-checkbox']",
            'something_went_wrong': "//*[text()='#Awkward, something went wrong']",
            'ok_button': "//button[text()='OK']",
            'payment_header': "//div[text()='To Pay']"
        })

    def verify_summary_screen(self):
        """
        To verify that sailor is on summary screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.confirm_button, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.summary_header,
                                                       locator_type='xpath'):
            logger.info("Summary page is getting displayed")
        else:
            raise Exception("Summary page is not getting displayed")

    def click_confirm_button(self, test_data):
        """
        To click confirm button on summary screen
        :param test_data:
        :return:
        """
        self.webDriver.scroll_complete_page()
        if self.webDriver.is_element_display_on_screen(element=self.locators.summary_check_box,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.summary_check_box, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.confirm_button,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_header, locator_type='xpath'):
            test_data['paid_activity'] = True
        else:
            test_data['paid_activity'] = False
        self.webDriver.click(element=self.locators.confirm_button, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.confirm_button,
                                                               locator_type='xpath')

    def verify_booking_confirmation_screen(self, test_data):
        """
        To verify booking confirmation screen
        :param test_data:
        :return:
        """
        test_data['active_folio'] = True
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.something_went_wrong,
                                                       locator_type='xpath'):
            if test_data['paid_activity']:
                self.webDriver.click(element=self.locators.ok_button, locator_type='xpath')
                contexts = self.webDriver.get_contexts()
                self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
                self.webDriver.mobile_native_back()
                self.webDriver.mobile_native_back()
                test_data['active_folio'] = False
                return
            else:
                raise Exception("Getting Something went wrong page after clicking on confirm button")
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booking_confirmation,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.done_btn,
                                                       locator_type='xpath'):
            logger.info("Booking confirmation page is getting displayed")
        else:
            raise Exception("Booking confirmation page is not getting displayed")

    def click_view_in_sailor_log(self):
        """
        To click on View in my Sailor's log btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.view_in_sailor_log_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.view_in_sailor_log_btn,
                                                               locator_type='xpath')

    def save_event_details(self, test_data):
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
        if self.webDriver.is_element_display_on_screen(element=self.locators.lineup_location,
                                                       locator_type='xpath'):
            test_data['lineup_location'] = self.webDriver.get_text(element=self.locators.lineup_location,
                                                                   locator_type='xpath')
        test_data['lineup_guest_count'] = len(self.webDriver.get_elements(element=self.locators.lineup_guest_count,
                                                                          locator_type='xpath'))
        
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
