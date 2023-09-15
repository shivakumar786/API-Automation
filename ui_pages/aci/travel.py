__author__ = 'sarvesh.singh'

from virgin_utils import *


class Travel(General):
    """
    Page class for travel screen of ACI app
    """

    def __init__(self, web_driver, config):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "travel": "//*[@text='TRAVEL']",
                "pre_status": "//*[@text='Pre Cruise Information']/following-sibling::android.widget.TextView",
                "not_flown": "//*[@text='Not flown in']",
                "post_status": "//*[@text='Post Cruise Information']/following-sibling::android.widget.TextView",
                "no": "//*[@text='No']",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "pre_cruise": "//*[@text='Pre Cruise Information']",
                "leave_usa": "com.decurtis.dxp.aci:id/leaving_usa",
                "land": "com.decurtis.dxp.aci:id/land",
                "remain_usa": "com.decurtis.dxp.aci:id/remain_in_usa",
                "hotel": "com.decurtis.dxp.aci:id/hotel",
                "private_residence": "com.decurtis.dxp.aci:id/private_residence",
                "other": "com.decurtis.dxp.aci:id/other",
                "hotel_name": "//*[@text='Hotel Name']/../following-sibling::android.widget.EditText",
                "address_line": "//*[@text='Address Line 1']/../following-sibling::android.widget.EditText",
                "remove_party": "com.decurtis.dxp.aci:id/edit_party",
                "cruise": "//*[@text='Cruise']",
            })
        else:
            self.locators = self.dict_to_ns({
                "travel": "//*[@text='TRAVEL']",
                "pre_status": "//*[@text='Pre Cruise Information']/following-sibling::android.widget.TextView",
                "not_flown": "//*[@text='Not flown in']",
                "post_status": "//*[@text='Post Cruise Information']/following-sibling::android.widget.TextView",
                "no": "//*[@text='No']",
                "save_proceed": "//*[@text='SAVE & PROCEED']",
                "pre_cruise": "//*[@text='Pre Cruise Information']",
                "cruise": "//*[@text='Cruise']",
                "terminal": "com.decurtis.dxp.aci.dclnp:id/car_parked_at_terminal",
                "other": "com.decurtis.dxp.aci,dclnp:id/other",
                "address_line": "//*[@text='Address Line 1']/../following-sibling::android.widget.EditText",
                "remove_party": "com.decurtis.dxp.aci.dclnp:id/edit_party"
            })

    def click_travel_tab(self):
        """
        Func to click on travel tab
        :return:
        """
        self.webDriver.click(element=self.locators.travel, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_travel_tab_enabled(self):
        """
        Func to check if travel tab is enabled
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.travel, locator_type='xpath'):
            return "false"
        else:
            return self.webDriver.get_web_element(element=self.locators.travel, locator_type='xpath').get_attribute(
                "selected")

    def click_save_proceed(self):
        """
        Func to click on save and proceed
        :return:
        """
        self.webDriver.click(element=self.locators.save_proceed, locator_type='xpath')
        self.webDriver.wait_for(2)

    def scroll_top(self):
        """
        Func to scroll to top of page
        :return:
        """
        self.webDriver.scroll_mobile(x_press=792, y_press=495, x_move=792, y_move=1099)
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.remove_party, locator_type='xpath'):
            pass
        else:
            self.webDriver.scroll_mobile(x_press=792, y_press=495, x_move=792, y_move=1099)

    def get_pre_status(self):
        """
        Func to get the pre cruise status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.pre_status, locator_type='xpath').text

    def get_post_status(self):
        """
        Func to get the post cruise status
        :return:
        """
        return self.webDriver.get_web_element(element=self.locators.post_status, locator_type='xpath').text

    def update_pre_cruise(self):
        """
        Func to update pre cruise information
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.not_flown, locator_type='xpath'):
            self.webDriver.click(element=self.locators.pre_cruise, locator_type='xpath')
        if self.get_pre_status() == 'Pending':
            self.webDriver.click(element=self.locators.not_flown, locator_type='xpath')
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

    def update_post_cruise(self):
        """
        Func to update post cruise information
        :return:
        """
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.cruise, locator_type='xpath'):
            self.webDriver.click(element=self.locators.post_status, locator_type='xpath')

        self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if self.get_post_status() == 'Pending':
            # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            # self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
            if self.config.platform == "DCL":
                self.webDriver.click(element=self.locators.cruise, locator_type='xpath')
                self.webDriver.click(element=self.locators.terminal, locator_type='id')
            else:
                if self.webDriver.is_element_display_on_screen(element=self.locators.remain_usa, locator_type='id'):
                    if self.webDriver.get_web_element(element=self.locators.remain_usa,
                                                      locator_type='id').get_attribute("checked") == 'true':
                        if self.webDriver.get_web_element(element=self.locators.hotel, locator_type='id').get_attribute(
                                "checked") == 'true':
                            if self.webDriver.get_web_element(element=self.locators.hotel_name,
                                                              locator_type='xpath').text != '':
                                data_is_there = True
                        elif self.webDriver.get_web_element(element=self.locators.private_residence,
                                                            locator_type='id').get_attribute("checked") == 'true':
                            if self.webDriver.get_web_element(element=self.locators.address_line,
                                                              locator_type='xpath').text != '':
                                data_is_there = True
                        elif self.webDriver.get_web_element(element=self.locators.other,
                                                            locator_type='id').get_attribute("checked") == 'true':
                            if self.webDriver.get_web_element(element=self.locators.address_line,
                                                              locator_type='xpath').text != '':
                                data_is_there = True
                else:
                    if self.webDriver.is_element_display_on_screen(element=self.locators.leave_usa, locator_type='id'):
                        if self.webDriver.get_web_element(element=self.locators.leave_usa,
                                                          locator_type='id').get_attribute("checked") == 'false':
                            self.webDriver.click(element=self.locators.leave_usa, locator_type='id')
                            self.webDriver.click(element=self.locators.land, locator_type='id')
                            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
                            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
                            self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)

        # if data_is_there:
        #     if self.webDriver.is_element_display_on_screen(element=self.locators.leave_usa, locator_type='id'):
        #         if self.webDriver.get_web_element(element=self.locators.leave_usa, locator_type='id').get_attribute(
        #                 "checked") == 'false':
        #             self.webDriver.click(element=self.locators.leave_usa, locator_type='id')
        #             self.webDriver.click(element=self.locators.land, locator_type='id')
        #             self.webDriver.scroll_mobile(x_press=18, y_press=932, x_move=13, y_move=609)
        if self.config.platform != "DCL":
            self.webDriver.click(element=self.locators.no, locator_type='xpath')