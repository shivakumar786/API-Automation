from virgin_utils import *


class MociDashboard:
    """
    Page Class for MOCI Dashboard page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Dashboard page
        :param web_driver:
        :param test_data:
        """
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = General.dict_to_ns({
            "app_title": "//*[@class='app-title' and text()='Moderate Online Check-In']",
            "search_textbox": "header-search",
            "ship_view": "ship-mode",
            "voyage_view": "voyage-mode",
            "reports": "//*[text()='Reports']",
            "history": "//*[text()='History']",
            "user_avatar": "nav-user",
            "logout": "logout",
            "show_more": "view-all",
            "logo": "(//div[@class='logo'])[1]",
            "search_magnifier": "//*[@class='search-btn cursor false']",
            "invalid_rearch": "//*[@class='col-xs-2 text-right number-of-results' and text()='0' and text()='Result']",
            "ship_search_textbox": "ship-search",
            "ship_tile": "//*[text()='Scarlet Lady']",
            "ship_seach_search_maginifier": "//*[@class='search-btn cursor']",
            "get_y_axis_mode": "//div[@class='y-axis-data']",
            "crew_name": "//div[@class='user-initials']",
            "show_me": "view-all",
            "get_voyages": "//div[@class = 'all ships-list']",
            "total_voyages": "//div[@class = 'text-right upcoming-voyages']/span"
        })

    def verification_of_moci_dashboard(self):
        """
        To check the availability of dashboard page
        """
        self.webDriver.allure_attach_jpeg('just_land_dashboard')
        self.webDriver.explicit_visibility_of_element(element=self.locators.ship_view, locator_type='id',
                                                      time_out=120)
        screen_title = self.webDriver.get_text(element=self.locators.app_title, locator_type='xpath')
        if screen_title == "Moderate Online Check-In":
            self.webDriver.allure_attach_jpeg('moci_dashboard')
            logger.debug("User is landed on Dashboard page after login")
            return True
        else:
            raise Exception("User is not landed on Dashboard page after login or login is not successful")

    def click_ship_view(self):
        """
        Click on Ship view
        :return:
        """
        self.webDriver.click(element=self.locators.ship_view, locator_type='id')
        self.webDriver.allure_attach_jpeg('click_ship')

    def click_voyage_view(self):
        """
        Click on Voyage view
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.voyage_view, locator_type='id', time_out=20)
        self.webDriver.click(element=self.locators.voyage_view, locator_type='id')
        self.webDriver.allure_attach_jpeg('click_voyage')

    def get_selected_view(self):
        """
        Function to get the selected view
        :return:
        """
        active = self.webDriver.get_attribute(element=self.locators.voyage_view,
                                              locator_type='id',
                                              attribute_name='class')
        if "active" in active:
            return "voyage"
        else:
            return "ship"

    def click_reports(self):
        """
        Click on Reports
        :return:
        """
        self.webDriver.click(element=self.locators.reports, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('click_report')

    def click_history(self):
        """
        Click on History
        :return:
        """
        self.webDriver.click(element=self.locators.history, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('click_history')

    def click_logo(self):
        """
        Click on logo
        :return:
        """
        self.webDriver.click(element=self.locators.logo, locator_type='xpath')

    def click_show_more(self):
        """
        Click on Show more of Voyages
        :return:
        """
        self.webDriver.click(element=self.locators.show_more, locator_type='id')
        self.webDriver.allure_attach_jpeg('click_reports')

    def search(self, search_value):
        """
        Function to search with Res# / Last Name / First Name / Middle Name
        :return:
        """
        self.webDriver.set_text(element=self.locators.search_textbox, locator_type='id', text=search_value)
        self.webDriver.click(element=self.locators.search_magnifier, locator_type='xpath')

    def click_user_avatar(self):
        """
        click on Logged in user avatar icon
        """
        self.webDriver.click(element=self.locators.user_avatar, locator_type='id')
        self.webDriver.allure_attach_jpeg('click_avatar')

    def click_logout(self):
        """
        click on logout option after open avatar
        """
        self.webDriver.click(element=self.locators.logout, locator_type='id')

    def validate_invalid_data(self, invalid_data):
        """
        Search with Invalid data
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.invalid_rearch, locator_type='xpath')

    def search_ship(self, search_value):
        """
        Function to search with Ships in Ship Search
        :return:
        """
        self.webDriver.set_text(element=self.locators.ship_search_textbox, locator_type='id', text=search_value)
        self.webDriver.click(element=self.locators.ship_seach_search_maginifier, locator_type='xpath')

    def click_ship_tile(self):
        """
        Click on Ship Tile
        :return:
        """
        self.webDriver.click(element=self.locators.ship_tile, locator_type='xpath')

    def verify_ship_mode(self):
        """
        verify ship mode
        """
        text = self.webDriver.get_text(element=self.locators.get_y_axis_mode, locator_type='xpath')
        assert text == "Ships", "Not landing on ship mode !!"

    def verify_voyage_mode(self):
        """
        verify voyages mode
        """
        text = self.webDriver.get_text(element=self.locators.get_y_axis_mode, locator_type='xpath')
        assert text == "Voyages", "Not landing on voyage mode !!"

    def verify_crew_name(self):
        """
        To verify the crew name
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.crew_name, locator_type='xpath'):
            raise Exception("Crew name is not visible !!")
        else:
            name = self.webDriver.get_text(element=self.locators.crew_name, locator_type='xpath')
        return name

    def verify_availability_show_me(self):
        """
        verify availability of show me button
        """
        self.webDriver.scroll_till_element(element=self.locators.show_me, locator_type='id')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.show_me, locator_type='id'):
            raise Exception("Show me button not available")
        count = []
        while True:
            if self.webDriver.is_element_display_on_screen(element=self.locators.show_me, locator_type='id'):
                self.webDriver.scroll_till_element(element=self.locators.show_me, locator_type='id')
                self.webDriver.click(element=self.locators.show_me, locator_type='id')
            else:
                res = self.webDriver.get_web_element(element=self.locators.get_voyages, locator_type='xpath')
                result = res.text.split("\n")
                for _data in result:
                    if "Lady" in _data:
                        count.append(_data)
                return count

    def total_voyages(self):
        """
        get total voyages
        """
        total = self.webDriver.get_elements(element=self.locators.total_voyages, locator_type='xpath')
        return total[0].text