__author__ = 'Krishna'

from virgin_utils import *


class NewBooking(General):
    """
    To Initiate elements from new booking page
    """
    def __init__(self, web_driver, test_data):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "spa_activity_price": "//*[text()='Ticket Price']/following-sibling::p",
            "add_sailor_cta": "//*[text()='Add Sailor']",
            "book_cta": "//*[text()='Book']",
            "booking_details_cta": "//*[@class='row booking-row-bottom']/button",
            "price_on_booking_details": "//*[text()='%s']",
            "loader": "//div[@class='LoaderContainer__div']//img",
        })

    def get_spa_activity_price(self):
        """
        get spa activity price from booking details page
        """
        self.test_data['spaSlotPrice'] = self.webDriver.get_text(element=self.locators.spa_activity_price, locator_type="xpath")

    def click_on_add_sailor(self):
        """
        click on add sailor cta to book activity
        """
        self.webDriver.click(element=self.locators.add_sailor_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def click_on_book_cta(self):
        """
        click on book cta from new booking page
        """
        self.webDriver.click(element=self.locators.book_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def click_on_booking_details(self):
        """
        click on the spa booking details
        """
        self.webDriver.click(element=self.locators.booking_details_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=120)

    def get_price_on_booking_details(self, spa_price):
        """
        get price on booking details page
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.price_on_booking_details % spa_price, locator_type="xpath")