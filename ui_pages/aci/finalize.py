__author__ = 'sarvesh.singh'

from virgin_utils import *


class Finalize(General):
    """
    Page class for finalize screen of ACI app
    """

    def __init__(self, web_driver, config, test_data):
        """
        To initialise the locators
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.config = config
        self.test_data = test_data
        if self.config.platform != 'DCL':
            self.locators = self.dict_to_ns({
                "finalize": "//*[@text='FINALIZE']",
                "check_in": "com.decurtis.dxp.aci:id/checkin_confirm_button",
                "done": "//*[@text='DONE']",
                "yes": "//*[@text='YES']",
                "anyway_checkin": "//*[@text='CHECK-IN ANYWAY']",
                "travel": "(//*[@class='androidx.appcompat.app.a$c'])[4]",
                "contract": "(//*[@class='androidx.appcompat.app.a$c'])[5]",
                "alert_popup": "com.decurtis.dxp.aci:id/alert",
                "manage_alert_button": "com.decurtis.dxp.aci:id/manage_alert",
                "delete_alert": "com.decurtis.dxp.aci:id/delete"
            })
        else:
            self.locators = self.dict_to_ns({
                "finalize": "//*[@content-desc='Check-In']/android.widget.TextView",
                "check_in": "com.decurtis.dxp.aci.dclnp:id/checkin_confirm_button",
                "done": "//*[@text='DONE']",
                "yes": "//*[@text='YES']",
                "anyway_checkin": "//*[@text='CHECK-IN ANYWAY']",
                "travel": "(//*[@class='androidx.appcompat.app.a$c'])[4]",
                "contract": "(//*[@class='androidx.appcompat.app.a$c'])[5]",
                "alert_popup": "com.decurtis.dxp.aci.dclnp:id/alert",
                "manage_alert_button": "com.decurtis.dxp.aci.dclnp:id/manage_alert",
                "delete_alert": "com.decurtis.dxp.aci.dclnp:id/delete",
                "person_image": "com.decurtis.dxp.aci.dclnp:id/person_image",
                "confirmation_popup": "android:id/button1"
            })

    def verify_express_checkin(self):
        """
        To verify express check in
        :return:
        """
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.anyway_checkin, locator_type='xpath'):
            self.webDriver.click(element=self.locators.anyway_checkin, locator_type='xpath')
            self.webDriver.click(element=self.locators.done, locator_type='xpath')
            self.webDriver.wait_for(2)
            return True
        else:
            return False

    def express_checkin(self):
        """
        To do express check in
        :return:
        """
        self.webDriver.click(element=self.locators.travel, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.yes, locator_type='xpath'):
            self.webDriver.click(element=self.locators.yes, locator_type='xpath')
            self.webDriver.click(element=self.locators.contract, locator_type='xpath')
            self.webDriver.click(element=self.locators.finalize, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.finalize, locator_type='xpath'):
                self.webDriver.click(element=self.locators.finalize, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.check_in, locator_type='id'):
                self.webDriver.click(element=self.locators.check_in, locator_type='id')

        else:
            self.webDriver.click(element=self.locators.contract, locator_type='xpath')
            self.webDriver.click(element=self.locators.finalize, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.finalize, locator_type='xpath'):
                self.webDriver.click(element=self.locators.finalize, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.check_in, locator_type='id'):
                self.webDriver.click(element=self.locators.check_in, locator_type='id')

    def click_finalize_tab(self):
        """
        Func to click on finalize tab
        :return:
        """
        self.webDriver.click(element=self.locators.finalize, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_finalize_tab_enabled(self):
        """
        Func to check if finalize tab is enabled
        :return:
        """
        try:
            return self.webDriver.get_web_element(element=self.locators.finalize, locator_type='xpath').get_attribute(
                "selected")
        except:
            return 'false'

    def click_check_in(self):
        """
        Func to click on check in
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.check_in, locator_type='id'):
            self.webDriver.click(element=self.locators.check_in, locator_type='id')

    def click_done(self):
        """
        Func to click on done
        :return:
        """
        self.webDriver.click(element=self.locators.done, locator_type='xpath')
        self.webDriver.wait_for(2)

    def check_availability_of_alert_popup(self):
        """
        Function to check the availability of alert popup
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.alert_popup, locator_type='id'):
            self.webDriver.click(element=self.locators.manage_alert_button, locator_type='id')
            self.delete_alert()
            return True
        else:
            return False

    def delete_alert(self):
        """
        Function to check the availability of alert popup
        :return:
        """
        guests = self.test_data['guest_count']
        counts = self.webDriver.get_elements(element=self.locators.person_image, locator_type='id')
        for count in counts:
            count.click()
            if self.webDriver.is_element_display_on_screen(element=self.locators.delete_alert, locator_type='id'):
                self.webDriver.click(element=self.locators.delete_alert, locator_type='id')
                self.webDriver.click(element=self.locators.confirmation_popup, locator_type='id')






