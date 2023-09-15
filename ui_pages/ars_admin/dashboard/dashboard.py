__author__ = 'Krishna'

from virgin_utils import *


class ArsDashboard(General):
    """
    ARS Admin Home Page
    """

    def __init__(self, web_driver, test_data):
        """
        initiate dashboard elements
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "activities": "(//*[text()='Activities'])[2]",
            "bookings": "(//div[text()='Bookings'])[2]",
            "logout_icon": "LogoutLogo",
            "logout_btn": "//*[text()='Logout']",
            "loader": "//div[@id='Spinner']",
            "voyage_list": "(//*[@id='selectedVoyageNumber'])[2]",
            "dashboard": "(// * [text() = 'Dashboard'])[2]",
            "vendor": "(//div[text()='Vendor'])[2]",
            "pending_approval": "//div[text()='Pending Approval']",
            "pending_approval_count": "//div[text()='Pending Approval']/ancestor::div[@class='columns']/div[@class='column']",
            "reject": "//button[text()='REJECT']",
            "reject_reason": "//div[@class='check ']",
            "reject_button": "//button[text()='Reject']",
            "success_notification": "//div[@class='notification is-success']",
            "settings": "(//*[text()='Settings'])[2]",
            "accounting": "//*[text()='Accounting']",
            "rejection_reason": "//*[text()='Rejection Reason']",
            "description": "(//*[@id='description']/div/div/div)[3]",
            "custom_description": "//*[@name='custom']"
        })

    def verify_ars_dashboard_page(self):
        """
        To Verify user is successfully landing on ARS Dashboard page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        return self.webDriver.get_title()

    def select_current_voyage(self):
        """
        select current voyage
        """
        debark_date = str(datetime.strptime(self.test_data['embarkDate'], '%m/%d/%Y')).split()[0]
        self.webDriver.enter_data_in_textbox_using_auto_complete(element=self.locators.voyage_list,
                                                                 locator_type="xpath", text=debark_date)

    def click_on_activities_tab_from_dashboard(self):
        """
        To click on activities tab from ars dashboard
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.activities, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_on_bookings_tab_from_dashboard(self):
        """
        To click bookings tab from ars dashboard
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.click(element=self.locators.bookings, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def logout_from_ars(self):
        """
        This is to logout from ars admin module
        """
        self.webDriver.click(element=self.locators.logout_icon, locator_type="id")
        self.webDriver.click(element=self.locators.logout_btn, locator_type="xpath")

    def click_on_dashboard_tab_from_dashboard(self):
        """
        To click on activities tab from ars dashboard
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.dashboard, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)

    def click_on_vendor_tab_from_dashboard(self):
        """
        To click vendor tab from ars dashboard
        """
        self.webDriver.click(element=self.locators.vendor, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def get_approval_count(self):
        """
        To get the count of approval pendings
        :return:
        """
        approval_count = self.webDriver.get_text(element=self.locators.pending_approval_count, locator_type="xpath")
        if int(approval_count) == 1:
            return 1
        else:
            return int(approval_count)

    def success_message(self):
        """
        This is to get the success message after complaint log, approve reject invoice
        """
        notification = self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")
        return notification

    def click_pending_approval(self):
        """
        To click on pending approval
        :return:
        """
        self.webDriver.click(element=self.locators.pending_approval, locator_type="xpath")

    def reject_approval(self):
        """
        To reject approval
        :return:
        """
        self.webDriver.click(element=self.locators.reject, locator_type="xpath")
        rejection_reason = self.webDriver.is_element_display_on_screen(element=self.locators.rejection_reason, locator_type="xpath")
        assert rejection_reason, "Rejecting reason page not displayed"
        description_element = self.webDriver.get_web_element(element=self.locators.description, locator_type='xpath')
        size = description_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_by_offset(description_element, x, y)
        if self.webDriver.is_element_display_on_screen(element=self.locators.custom_description, locator_type="xpath"):
            self.webDriver.set_text(element=self.locators.custom_description, locator_type="xpath", text="Reject Invoice")
        self.webDriver.click(element=self.locators.reject_button, locator_type="xpath")
        assert self.success_message() == "Activity Slot Rejected", "Failed to reject invoice from dashboard"
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def click_on_bookings_tab_from_dashboard_to_verify_loader(self):
        """
        To click bookings tab from ars dashboard
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.bookings, locator_type="xpath")
        self.webDriver.click(element=self.locators.bookings, locator_type="xpath")

    def click_on_settings_tab_from_dashboard(self):
        """
        To click on settings from ars dashboard
        """
        self.webDriver.click(element=self.locators.settings, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def clik_on_accounting_tab(self):
        """
        function to click on accounting tab
        :return:
        """
        self.webDriver.click(element=self.locators.accounting, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)