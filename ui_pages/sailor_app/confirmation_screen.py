__author__ = 'vanshika.arora'

from virgin_utils import *


class Booking_confirmation(General):
    """
    Page class for booking confirmation page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "view_in_my_sailor_log_cta": "//button[text()='View in my Sailor’s Log']",

        })

    def click_view_in_my_sailor_log(self):
        """
        To click veiw in my sailor log cta on booking confirmation screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.view_in_my_sailor_log_cta, locator_type='xpath')
