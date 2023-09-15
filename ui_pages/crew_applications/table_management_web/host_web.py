__author__ = 'bhanu.pratap'

from virgin_utils import *


class TableManagementHost(General):
    """
    Page Class For host To Table Management Web
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of host page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "host": "//span[contains(text(),'Host')]",
            "loader": "//*[@text='loading...']",
            "venue_dropdown": "//*[@id='dropdown-venues-selected']",
            "venues": "//ul[@class='dropdown__items']/li",
            "hamburger_menus": "//button[@id ='button-main-menu']",
            "bookable_venue": "//span[text()='%s']",
            "tables": "//*[contains(@id,'table-drag-container-table-layout-reservations')]",
            "background_dropdown": "//*[@id='host-reservation-table-layout-dropdown-checkboxes-selected']",
            "floor_plan": "//*[@class='tables__floorplan']"
        })

    def verify_host_module(self):
        """
        To verify user land on host module
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.venue_dropdown, locator_type='xpath'):
            return True
        else:
            return False

    def get_venue_list(self):
        """
        To get all venue lists
        :return:
        """
        venues = []
        self.webDriver.click(element=self.locators.venue_dropdown, locator_type='xpath')
        venues_list = self.webDriver.get_elements(element=self.locators.venues, locator_type='xpath')
        for venue in venues_list:
            venues.append(venue.text)
        return venues

    def verify_venue_list(self, venues):
        """
        To verify venue list
        :param venues:
        :return:
        """
        venue = ["Extra Virgin", "Gunbae", "Pink Agave", "Razzle Dazzle Restaurant", "The Test Kitchen", "The Wake"]
        for restaurant in venue:
            if restaurant in venues:
                return True
            else:
                return False

    def click_venue_drop_down(self):
        """
        To click venue drop down
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.venue_dropdown, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.venue_dropdown, locator_type='xpath')
        self.webDriver.wait_for(2)

    def select_venue(self, venue):
        """
        To select any venue from venue drop down
        :param venue:
        :return:
        """
        venues = ["Extra Virgin", "Gunbae", "Pink Agave", "Razzle Dazzle Restaurant", "The Test Kitchen", "The Wake"]
        for i in range(len(venue)):
            venues_list = self.webDriver.get_elements(element=self.locators.venues, locator_type='xpath')
            for venue in venues_list:
                if venue.text in venues:
                    self.webDriver.click(element=self.locators.bookable_venue % venue.text, locator_type='xpath')
                    self.webDriver.explicit_visibility_of_element(element=self.locators.tables, locator_type='xpath', time_out=120)
                    if len(self.webDriver.get_elements(element=self.locators.tables, locator_type='xpath')) > 10:
                        break
                    else:
                        self.click_venue_drop_down()
                        continue
            break

    def verify_background_plan(self):
        """
        To verify venue background
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.background_dropdown, locator_type='xpath',
                                                      time_out=120)
        self.webDriver.explicit_visibility_of_element(element=self.locators.floor_plan, locator_type='xpath',
                                                      time_out=120)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.floor_plan, locator_type='xpath'):
            raise Exception("Floor plan for venue is not displaying")
        else:
            return True