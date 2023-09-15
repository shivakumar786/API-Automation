
from virgin_utils import *


class GuestList:
    """
    Page Class for MOCI Guest list after search
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Guest List page
        :param web_driver:
        :param test_data:
        """
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = General.dict_to_ns({
            "guest_count": "//div[@class='row guest-search-item']/div",
            "res_number": "(//div[@class='col-xs-2 v-m'])[%s]",
            "guest_name": "(//div[@class='col-xs-3 v-m text-uppercase'])[%s]",
            "guest_names": "(//div[@class='col-xs-3 v-m text-uppercase'])",
            "no_data": "//div[@class='no-data-available']",
            "personal_info": "//span[text()='Personal Information']",
            "MOCI_complete_check_box": "ALable",
            "filter_apply_button": "apply-filter",
            "MOCI_complete_total": "//span[@class='total-records']",
            "MOCI_pending_check_box": "PLable",
            "MOCI_overdue_pending_check_box": "POLable"
        })

    def get_total_guest_in_list(self):
        """
        Get the total number of guest in page
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_data, locator_type='xpath'):
            return 0
        else:
            total_guests = self.webDriver.get_elements(element=self.locators.guest_count, locator_type='xpath')
            self.test_data['total_guests'] = len(total_guests)
            return self.test_data['total_guests']

    def get_guest_name(self):
        """
        To get the guest name after search
        :return:
        """
        for count in range(self.test_data['total_guests']):
            self.test_data[f"name_{count + 1}"] = self.webDriver.get_text(
                element=self.locators.guest_name % (count + 1),
                locator_type='xpath')

    def verify_availability_of_guest_name(self, guest_name):
        """
        verify the guest name in list
        :return:
        """
        for count in range(self.test_data['total_guests']):
            name = self.webDriver.get_text(element=self.locators.guest_name % (count + 1), locator_type='xpath')
            if name == guest_name:
                logger.debug("guest name available in list")
                break
        else:
            raise Exception("Guest name is not available in list")

    def click_selected_guest_name(self, guest_name):
        """
        verify the guest name in list
        :return:
        """
        total_guests = self.webDriver.get_elements(element=self.locators.guest_names, locator_type='xpath')
        for guests in total_guests:
            if "Rejected" in guests.text and guests.text.split("\n")[0] == guest_name.split("\n")[0].upper():
                guests.click()
                break
            else:
                if guests.text.upper() == guest_name.upper():
                    guests.click()
                    break

    def verify_reservation_number(self):
        """
        To verify the reservation number after search
        :return:
        """
        for count in range(self.test_data['total_guests']):
            reservation = self.webDriver.get_text(element=self.locators.res_number % (count + 1), locator_type='xpath')
            if self.test_data['shore_reservationNumber'] == reservation:
                logger.debug("Correct reservation number display after search")
            else:
                raise Exception("Correct reservation not search or search not working")

    def open_guest_details(self, guest_number):
        """
        Function to open the guest details page
        :param guest_number:
        :return:
        """
        self.webDriver.click(element=self.locators.res_number % guest_number, locator_type='xpath')

    def get_primary_guest_name(self):
        """
        Get the primary guest name
        :return:
        """
        try:
            for primary in self.test_data['guest_details']['eCheckinGuestDetailsList']:
                if primary['reservationInfo']['isPrimaryGuest']:
                    self.test_data[
                        'primary_guest_name'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['middleName']} {primary['personalInfo']['lastName']}"
                    self.test_data[
                        'primary_guest_name_without_middle'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['lastName']}"
                    break
        except Exception:
            for primary in self.test_data['guest_details']['eCheckinGuestDetailsList']:
                if primary['reservationInfo']['isPrimaryGuest']:
                    self.test_data[
                        'primary_guest_name'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['lastName']}"
                    self.test_data[
                        'primary_guest_name_without_middle'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['lastName']}"
                    break

    def get_non_primary_guest_name(self):
        """
        Get the primary guest name
        :return:
        """
        try:
            for primary in self.test_data['guest_details']['eCheckinGuestDetailsList']:
                if not primary['reservationInfo']['isPrimaryGuest']:
                    self.test_data[
                        'non_primary_guest_name'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['middleName']} {primary['personalInfo']['lastName']}"
                    break
        except Exception:
            for primary in self.test_data['guest_details']['eCheckinGuestDetailsList']:
                if not primary['reservationInfo']['isPrimaryGuest']:
                    self.test_data[
                        'non_primary_guest_name'] = f"{primary['personalInfo']['firstName']} {primary['personalInfo']['lastName']}"
                    break