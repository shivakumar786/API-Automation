__author__ = 'Krishna'

from virgin_utils import *


class AddSailor(General):
    """
    To Initiate elements add sailor page
    """
    def __init__(self, web_driver, test_data):
        """
        Initiate web_driver and elements of add slots
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "sailor_search": "//input[@placeholder='Search Sailor']",
            "sailor_check_box": "(//span[@class='tick']//img[@class='SVGContainer '])[2]",
            "next": "//button[text()='Next']",
            "sailor_image": "//*[text(),\"Sailor already have a booking at this time which can not be overridden.\"]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "info_icon": "//div[@class='column is-full is-pulled-right']",
            "hard_conflict_warning": "//div[@class='column is-narrow is-vcentered']/following-sibling::div",
            "cancel": "(//button[text()='Cancel'])[2]",
        })

    def click_on_add_sailor(self):
        """
        click on add sailor cta to book activity
        """
        self.webDriver.click(element=self.locators.add_sailor_cta, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def search_for_sailor_and_click_on_next_cta(self, stateroom):
        """
        search for sailor
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sailor_search, locator_type="xpath", time_out=60)
        self.webDriver.enter_data_in_textbox_using_auto_complete(element=self.locators.sailor_search, locator_type= "xpath", text=stateroom)
        self.webDriver.click(element=self.locators.sailor_check_box, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        self.webDriver.click(element=self.locators.next, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        try:
            self.webDriver.click(element=self.locators.next, locator_type="xpath")
            self.test_data['isSpaBooked'] = True
        except Exception:
            self.test_data['isSpaBooked'] = False
            self.webDriver.click(element=self.locators.cancel, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def get_conflict_status(self):
        """
        get the conflict status
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.sailor_image, locator_type="xpath")

    def verify_hard_conflict(self):
        """
        Function to verify hard conflict when date and time for booking two spa activities is same
        :return:
        """
        self.webDriver.click(element=self.locators.info_icon, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath",
                                                        time_out=60)
        warning = self.webDriver.get_text(element=self.locators.hard_conflict_warning,locator_type="xpath")
        assert warning == "Sailor already have a booking at this time which can not be overridden."

    def search_for_sailor(self, stateroom):
        """
        search for sailor
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.sailor_search, locator_type="xpath",
                                                      time_out=60)
        self.webDriver.enter_data_in_textbox_using_auto_complete(element=self.locators.sailor_search,
                                                                 locator_type="xpath", text=stateroom)
        self.webDriver.click(element=self.locators.sailor_check_box, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        self.webDriver.click(element=self.locators.next, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)
        self.webDriver.explicit_invisibility_of_element(self.locators.loader, locator_type="xpath", time_out=60)

    def click_cancel_button(self):
        """
        Click cancel button
        :return:
        """
        self.webDriver.click(element=self.locators.cancel, locator_type="xpath")

