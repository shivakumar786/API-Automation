from virgin_utils import *


class GuestFilter:
    """
    Page Class For Guest Filter Screen
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        :param web_driver:
        """
        self.webDriver = web_driver
        self.locators = General.dict_to_ns({
            "dropbox_ship_view": "//*[@class='Select-value-label']",
            "citizenship_dropbox": "//*[@id='countryOfCitizenship-sort']/span[2]",
            "all_check_box": "//*[@id='allLable']",
            "approved_check_box": "//*[@id='ALable']",
            "oci_not_started_check_box": "//*[@id='ONSLable']",
            "pending_check_box": "//*[@id='PLable']",
            "pending_overdue_check_box": "//*[@id='POLable']",
            "rejected_check_box": "//*[@id='ICM,ICMOLable']",
            "rejected_overdue_check_box": "//*[@id='ICMCNLable']",
            "update_button": "//*[@id='apply-filter']",
            "first_guest_tile": "//*[@id='guest-0']",
            "reservation_number_first_tile": "//*[@class='col-xs-12 party__title']",
            "approved_status": "//div[@class='bubble is-approved']"

        })

    def get_value_ship_dropbox(self):
        """
        Click on Ship Tile
        :return:
        """
        ship_name = self.webDriver.get_text(element=self.locators.dropbox_ship_view, locator_type='xpath')
        return ship_name

    def select_citizenship(self, citizenship):
        """
        Select Citizenship from DropBox
        :citizenship:
        """
        self.webDriver.click(element=self.locators.citizenship_dropbox, locator_type='xpath')

    def click_all_checkbox(self):
        """
        Select All Checkbox
        """
        self.webDriver.click(element=self.locators.all_check_box, locator_type='xpath')

    def click_approved_checkbox(self):
        """
        Click Approved Checkbox
        """
        self.webDriver.click(element=self.locators.approved_check_box, locator_type='xpath')

    def click_update_button(self):
        """
        Click Update Button
        """
        self.webDriver.click(element=self.locators.update_button, locator_type='xpath')

    def click_guest_first_tile(self):
        """
        Click Guest On First Tile
        """
        self.webDriver.click(element=self.locators.first_guest_tile, locator_type='xpath')

    def get_reservation_number_first_tile(self):
        """
        Get Reservation Number of first tile
        """
        res_number = self.webDriver.get_text(element=self.locators.reservation_number_first_tile, locator_type='xpath')
        return res_number

    def verify_guest_status(self):
        """
        Get guest Status.
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.approved_status, locator_type='xpath')
        return "Approved"