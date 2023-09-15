__author__ = 'vanshika.arora'

from virgin_utils import *


class connect_Booking(General):
    """
    Page class for connect booking screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "connect_booking_header": "//h1[text()='Connect a booking']",
            "surname": "//input[@id='surnameInput']",
            "reservation_id": "//input[@id='bookingReferenceInput']",
            "month_of_birth": "//span[@id='month_dateOfBirth']",
            "date_of_birth": "//input[@id='dayInput']",
            "year_of_birth": "//input[@id='yearInput']",
            "find_my_booking": "//button[@id='findMyBookingButton']"
            })

    def verify_connect_booking_screen_available(self):
        """
        To verify that user is on connect a booking screen
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.connect_booking_header,
                                                       locator_type='xpath'):
            logger.info("Sailor has landed on connect booking screen")
        else:
            raise Exception("Sailor has not landed on connect booking screen")

    def connect_the_booking(self, guest_data, test_data):
        """
        Function to enter connect booking details
        :param guest_data:
        :param test_data:
        :return:
        """
        self.webDriver.set_text(element=self.locators.surname, locator_type='xpath', text=guest_data[0]['LastName'])
        self.webDriver.set_text(element=self.locators.reservation_id, locator_type='xpath', text=test_data['reservationNumber'])
        self.webDriver.set_text(element=self.locators.date_of_birth, locator_type='xpath', text=guest_data[0]['BirthDate'][8:10])
        self.webDriver.set_text(element=self.locators.month_of_birth, locator_type='xpath', text=guest_data[0]['BirthDate'][5:7])
        self.webDriver.set_text(element=self.locators.year_of_birth, locator_type='xpath', text=guest_data[0]['BirthDate'][0:4])
        self.webDriver.click(element=self.locators.find_my_booking, locator_type='xpath')


