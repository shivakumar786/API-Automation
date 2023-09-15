__author__ = 'Saloni.pattnaik'

import time

from selenium.webdriver.common.keys import Keys
from virgin_utils import *


class Arsvendor(General):
    """
    ARS Admin Booking Page
    """

    def __init__(self, web_driver):
        """
        initiate booking elements
        :params: web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "vendor_page_header": "//span[text()='Vendor Activities']",
            "vendor_tab": "(//div[text()='Vendor'])[2]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "vendor_name": "//div[@class='rt-td'][1]",
            "vendor_balance_amount": "(//*[text()='{}']/../div[@class='rt-td'])[4]",
            "open_vendor": "(//*[text()='{}']/../div[@class='rt-td'])[5]",
            "activity_balance": "//tbody/tr/td[8]",
            "open_activity": "//*[text()='{}']/../td[9]",
            "slot_balance": "//*[text()='OPEN']/../td[9]",
            "select_slot": "(//*[text()='OPEN']/../td[1])[{}]",
            "actions_text_field": "(//div[@class='react-select-container css-2b097c-container'])[3]",
            "activity_list": "//div[@class='rt-tbody']//div[@class='rt-tr-group']",
            "slot_status": "//*[text()='OPEN']/../td[4]",
            "activity_filter": "//img[@class='SVGContainer btn-img-clr']",
            "active_radio_btn": "//span[text()='Active']/../..//div[@class='check ']",
            "apply": "//button[text()='APPLY']",
            "activity_arrow": "//div[@class='rt-td']//img[@class='SVGContainer ']",
            "vendor_status": "//div[text()='Vendor Status']/..//div[@class='column']",
            "back_button": "//a[@class='back-button']",
            "settle_all_accounts": "//button[text()='SETTLE ALL ACCOUNTS']",
            "activity_dropdown_arrow": "//div[@class='fa']",
            "activity_checkbox": "//span[@class='tick']//img[@class='SVGContainer ']",
            "action_drop_down": "(//div[@class='react-select__control css-yk16xz-control'])[3]",
            "complaint_count": "//button[@class='button complaintCount ']",
            "sailor_name": "(//*[@id='activityPersonBookingId']/div/div/div)[3]",
            "description": "(//*[@id='description']/div/div/div)[3]",
            "create": "//button[text()='CREATE']",
            "no_records_found":"//*[text()='No Records Found']",
            "send_for_approval": "//button[text()='SEND FOR APPROVAL']",
            "success_notification": "//div[@class='notification is-success']",
            "vendor_code": "//div[@class='card-header-title']/..//div[@class='column']",
            "vendor_list": "//div[@class='rt-td'][1]",
            "vendor_arrow": "//div[text()='%s']/..//div[5]",
            "adjust_amount": "//input[@name='amount']",
            "adjust": "//button[text()='ADJUST']",
            "amount_count": "//td[@class='rAlign']",
            "child_page_balance": "//*[text()='Total Balance']/../div[@class='column title']",
            "account_status": "//*[text()='Account Status']/../../../../div[@class='rt-tbody']//div[3]",
            "balance_amount": "//*[text()='Balance Amount']/../../../../div[@class='rt-tbody']//div[4]",
            "total_adjustment_amount": "//th[text()='Adjustment']/ancestor::div[@class='TableContainer__div "
                                       "card']//table[@class='table is-fullwidth is-hoverable']//td[7]",
            "total_balance_amount": "//th[text()='Balance Amount']/ancestor::div[@class='TableContainer__div "
                                    "card']//table[@class='table is-fullwidth is-hoverable']//td[8]",
            "total_adjustment": "//div[text()='Total Adjustment']/..//div[@class='column title']",
            "total_balance": "//div[text()='Total Balance']/..//div[@class='column title']",
            "action_to_log_complaint": "//*[text()='Select...']/..//input",
            "adjust_amount_for_rejected": "//*[text()='REJECTED']/../following-sibling::tr//*[text()='Select...']/..//input",
            "adjustment_reason": "//*[text()='Reason']/../div/div/div[2]/div",
            "header_name": "//div[@class='rt-tr']/div",
            "table_rows": "//div[@class='rt-tr-group']",
            "sort_by": "//div[@class='rt-th -cursor-pointer']/div[text()='%s']",
            "column_values": "//div[@class='rt-tbody']/div[@class='rt-tr-group'][%s]//div[@class='rt-td'][%s]",
            "sort_descending_by": "//div[@class='rt-th -sort-asc -cursor-pointer']/div[text()='%s']"
        })

    def verify_vendor_page_header(self):
        """
        To Verify user is successfully landing on ARS bookings page
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        return self.webDriver.get_text(element=self.locators.vendor_page_header, locator_type='xpath')

    def verify_activity_list(self):
        """
        To verify list of activity is coming or not
        :return:
        """
        return self.webDriver.get_elements(element=self.locators.activity_list, locator_type='xpath')

    def click_on_activity_filter(self):
        """
        To verify filter icon is clickable or not
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.click(element=self.locators.activity_filter, locator_type='xpath')

    def select_filter_option(self):
        """
        To select filter option
        :return:
        """
        self.webDriver.click(element=self.locators.active_radio_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_applied_filter(self):
        """
        To verify applied filter in activity list
        :return:
        """
        return self.webDriver.get_elements(element=self.locators.activity_arrow, locator_type='xpath')

    def select_first_activity(self):
        """
        To select first activity
        :return:
        """
        self.webDriver.click(element=self.locators.activity_arrow, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_vendor_status(self):
        """
        To verify the vendor status
        :return:
        """
        return self.webDriver.get_text(element=self.locators.vendor_status, locator_type='xpath')

    def click_back_button(self):
        """
        To come back to activity list page from vendor details page
        :return:
        """
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=70)

    def select_each_activity(self, activity):
        """
        To select each activity one by one
        :param activity:
        :return:
        """
        activity.click()
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_settle_all_account_available(self, test_data):
        """
        To verify settle all accounts button is available or not on UI page
        :param test_data:
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.settle_all_accounts, locator_type='xpath') \
                and self.webDriver.is_element_enabled(element=self.locators.settle_all_accounts, locator_type='xpath'):
            test_data['vendor_code'] = self.webDriver.get_text(element=self.locators.vendor_code, locator_type='xpath')
            return True
        else:
            return False

    def click_avtivity_dropdown_arrow(self):
        """
        To verify activity drop down arrow
        :return:
        """
        self.webDriver.click(element=self.locators.activity_dropdown_arrow, locator_type='xpath')

    def select_activity_checkbox(self):
        """
        To select activity checkbox
        :return:
        """
        self.webDriver.click(element=self.locators.activity_checkbox, locator_type='xpath')

    def click_action_drop_down(self, option):
        """
        To click action drop down
        :param option:
        :return:
        """
        self.webDriver.scroll(0, 5000)
        element = self.webDriver.get_web_element(element=self.locators.action_drop_down, locator_type='xpath')
        size = element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_option_by_offset(element, x, y, option)

    def fill_complaint_details(self):
        """
        To fill complaint details
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        sailor_element = self.webDriver.get_web_element(element=self.locators.sailor_name, locator_type='xpath')
        size = sailor_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_by_offset(sailor_element, x, y)
        description_element = self.webDriver.get_web_element(element=self.locators.description, locator_type='xpath')
        size = description_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_by_offset(description_element, x, y)
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def fill_adjust_form(self):
        """
        To fill reject form details
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.set_text(element=self.locators.adjust_amount, locator_type='xpath', text=5)
        adjust_element = self.webDriver.get_web_element(element=self.locators.adjustment_reason, locator_type='xpath')
        size = adjust_element.size
        x, y = size['width'], size['height']
        self.webDriver.selct_dropdown_by_offset(adjust_element, x, y)
        self.webDriver.click(element=self.locators.adjust, locator_type='xpath')

    def verify_complaint_count(self):
        """
        To verify complaint count
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.complaint_count, locator_type='xpath'):
            return self.webDriver.get_text(element=self.locators.complaint_count, locator_type='xpath')
        else:
            return False

    def select_settle_all_accounts(self):
        """
        To select settle all accounts button
        :return:
        """
        self.webDriver.click(element=self.locators.settle_all_accounts, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.click(element=self.locators.send_for_approval, locator_type='xpath')

    def get_account_status(self):
        """
        To get the status of account
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        statuses = self.webDriver.get_elements(element=self.locators.account_status, locator_type='xpath')
        return statuses

    def open_given_activity(self, activity):
        """
        To open given activity from vendor dashboard
        :param activity:
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        vendors = self.webDriver.get_elements(element=self.locators.vendor_list, locator_type='xpath')
        for vendor in vendors:
            if vendor.text == activity:
                self.webDriver.click(element=self.locators.vendor_arrow % activity, locator_type='xpath')
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                break
            else:
                continue

    def calculate_total_adjustment_amount(self):
        """
        To calculate total adjustment amount
        :return:
        """
        total_amount = self.webDriver.get_text(element=self.locators.total_adjustment, locator_type='xpath')
        if total_amount == "$" or total_amount == "$0":
            return 0
        else:
            splits = total_amount.split(".")[0]
            total_amount = int(splits.split("$")[1])
            amounts = self.webDriver.get_elements(element=self.locators.total_adjustment_amount, locator_type='xpath')
            adjust = []
            for amount in amounts:
                splits = amount.text.split(".")[0]
                adjust.append(int(splits.split("$")[1]))
            adjustment_sum = sum(adjust)
            if total_amount == adjustment_sum:
                return True

    def calculate_total_balance_amount(self):
        """
        To calculate total balance amount
        :return:
        """
        total_amount = self.webDriver.get_text(element=self.locators.total_balance, locator_type='xpath')
        splits = total_amount.split(".")[0]
        total_amount = int(splits.split("$")[1])
        amounts = self.webDriver.get_elements(element=self.locators.total_balance_amount, locator_type='xpath')
        balance = []
        for amount in amounts:
            splits = amount.text.split(".")[0]
            balance.append(int(splits.split("$")[1]))
        adjustment_sum = sum(balance)
        if total_amount == adjustment_sum:
            return True

    def get_total_balance_amount(self):
        """
        To get total balance amount
        :return:
        """
        return self.webDriver.get_text(element=self.locators.total_balance_amount, locator_type='xpath')

    def is_no_records_found(self):
        """
        Check if no records found is displayed
        """
        record_status = self.webDriver.is_element_display_on_screen(element=self.locators.no_records_found, locator_type="xpath")
        return record_status

    def get_vendor_list(self):
        """
        To get vendor list form vendor activities main page
        """
        vendors = self.webDriver.get_elements(element=self.locators.vendor_name, locator_type="xpath")
        vendors_list = []
        for vendor in vendors:
            vendors_list.append(vendor.text)
        return vendors_list

    def get_activity_balance(self):
        """
        To get the list of activities balance in a vendor
        """
        activities = self.webDriver.get_elements(element=self.locators.activity_balance, locator_type="xpath")
        activity_balance = []
        for activity in activities:
            activity_balance.append(activity.text)
        return activity_balance

    def slot_balance_in_activity(self):
        """
        To get the list of slots available in an activity
        """
        slots = self.webDriver.get_elements(element=self.locators.slot_balance, locator_type="xpath")
        slot_balance = []
        for slot in slots:
            slot_balance.append(slot.text)
        return slot_balance

    def success_message(self):
        """
        This is to get the success message after complaint log, approve reject invoice
        """
        notification = self.webDriver.get_text(element=self.locators.success_notification, locator_type="xpath")
        return notification

    def get_activity_slot_status(self):
        """
        This is to get the activity slot status for amount adjustment
        """
        activity_status = self.webDriver.get_elements(element=self.locators.slot_status, locator_type="xpath")
        status = []
        for act_status in activity_status:
            status.append(act_status.text)
        return status

    def log_complaint(self):
        """
        This is to check for the vendor having balance amount
        """
        vendors = self.get_vendor_list()
        for vendor in vendors:
            self.webDriver.click(element=self.locators.vendor_tab, locator_type="xpath")
            ven_balance = self.webDriver.get_text(element=self.locators.vendor_balance_amount.format(vendor),
                                                  locator_type="xpath")
            if int(float(ven_balance[1:].replace(',', ''))) > 0:
                self.webDriver.click(element=self.locators.open_vendor.format(vendor), locator_type="xpath")
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=60)
                act_balance = self.get_activity_balance()
                for activity_balance in act_balance:
                    if int(float(activity_balance[1:].replace(',', ''))) > 0:
                        self.webDriver.click(element=self.locators.open_activity.format(activity_balance),
                                             locator_type="xpath")
                        if self.webDriver.is_element_display_on_screen(element=self.locators.loader, locator_type='xpath'):
                            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader,locator_type='xpath', time_out=120)
                        balance = self.slot_balance_in_activity()
                        for count, slot_balance in enumerate(balance, start=1):
                            if int(float(slot_balance[1:].replace(',', ''))) > 0:
                                self.webDriver.scroll_complete_page()
                                self.webDriver.explicit_visibility_of_element(element=self.locators.select_slot.format(count),
                                                     locator_type="xpath", time_out=60)
                                self.webDriver.click(element=self.locators.select_slot.format(count),
                                                     locator_type="xpath")
                                self.webDriver.set_text(self.locators.action_to_log_complaint, locator_type="xpath", text="Log Complaint")
                                self.webDriver.key_chains().send_keys(Keys.ENTER).perform()
                                self.fill_complaint_details()
                                notification = self.success_message()
                                assert notification == "Success", "Failed to log complaint"
                                self.click_back_button()
                                return
        else:
            pytest.skip(msg='no vendors have balance > 0  to log complaint')

    def bulk_settlement(self):
        """
        bulk settlement for any vendor
        :params: test_data:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.loader, locator_type='xpath'):
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=120)
        vendors = self.get_vendor_list()
        for vendor in vendors:
            self.webDriver.click(element=self.locators.vendor_tab, locator_type="xpath")
            self.webDriver.click(element=self.locators.open_vendor.format(vendor), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            if self.webDriver.is_element_display_on_screen(element=self.locators.settle_all_accounts,
                                                           locator_type='xpath') and self.webDriver.is_element_enabled(
                element=self.locators.settle_all_accounts, locator_type='xpath'):
                self.select_settle_all_accounts()
                assert self.success_message() == "All Accounts are getting set", "failed to settle all accounts"
                break
        else:
            pytest.skip(msg='No vendor slots active to settle all accounts')

    def set_adjust_amount_in_action_drop_down(self):
        """
        Function to set adjust amount in actions dropdown
        :return:
        """
        try:
            self.webDriver.set_text(self.locators.adjust_amount_for_rejected, locator_type="xpath",
                                    text="Adjust Amount")
            self.webDriver.key_chains().send_keys(Keys.ENTER).perform()
        except Exception:
            self.webDriver.set_text(self.locators.action_to_log_complaint, locator_type="xpath",
                                    text="Adjust Amount")
            self.webDriver.key_chains().send_keys(Keys.ENTER).perform()

    def adjust_vendor_amount(self):
        """
        This is to modify or adjust the vendor amount for rejected slots
        """
        vendors = self.get_vendor_list()
        for vendor in vendors:
            self.webDriver.click(element=self.locators.vendor_tab, locator_type="xpath")
            self.webDriver.click(element=self.locators.open_vendor.format(vendor), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            act_balance = self.get_activity_balance()
            for activity_balance in act_balance:
                self.webDriver.click(element=self.locators.open_activity.format(activity_balance),
                                     locator_type="xpath")
                status = self.get_activity_slot_status()
                for count, slot_status in enumerate(status, start=1):
                    if slot_status == "REJECTED":
                        time.sleep(2)
                        self.webDriver.click(element=self.locators.select_slot.format(count),
                                             locator_type="xpath")
                        self.set_adjust_amount_in_action_drop_down()
                        self.fill_adjust_form()
                        notification = self.success_message()
                        assert notification == "Success", "Failed to log complaint"
                        self.click_back_button()
                        return
        else:
            pytest.skip(msg='There no Rejected slots to adjust vendor amount')

    def compare_vendor_balance(self):
        """
        To verify and compare Vendor Balance from main page and activity list page
        """
        vendors = self.get_vendor_list()
        for vendor in vendors:
            ven_balance = self.webDriver.get_text(element=self.locators.vendor_balance_amount.format(vendor),
                                                  locator_type="xpath")
            balance_on_main_page = int(float(ven_balance[1:].replace(',', '')))
            self.webDriver.click(element=self.locators.open_vendor.format(vendor), locator_type="xpath")
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            balance = self.webDriver.get_text(element=self.locators.child_page_balance, locator_type="xpath")
            balance_on_child_page = int(float(balance[1:].replace(',', '')))
            assert balance_on_main_page == balance_on_child_page, f"Balance {balance_on_main_page} == {balance_on_child_page}amount does not match"
            break

    def set_column_name(self, test_data):
        """
        Function to set the column name
        :param test_data:
        """
        column_number = 0
        total_column = self.webDriver.get_elements(element=self.locators.header_name, locator_type='xpath')
        for column in total_column:
            column_number = column_number + 1
            test_data[f"{column.text}_position"] = column_number

    def sort_report_and_verify(self, test_data, sort_by):
        """
        Function to sort reports and verify
        :param test_data:
        :param sort_by:
        """
        rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
        if len(rows) < 11:
            val = len(rows)+1
        else:
            val = 11

        self.webDriver.click(element=self.locators.sort_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        list1 = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(element=self.locators.column_values % (i, test_data[f'{sort_by}_position']), locator_type='xpath')
            list1.append(col_value)
        sorted_list = sorted(list1, key=str.lower)
        assert list1 == sorted_list, f'{sort_by} list is not sorted in ascending order according to {sort_by}'
        self.webDriver.click(element=self.locators.sort_descending_by % sort_by, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        desc_list = []
        for i in range(1, val):
            col_value = self.webDriver.get_text(
                element=self.locators.column_values % (i, test_data[f'{sort_by}_position']), locator_type='xpath')
            desc_list.append(col_value)
        sorted_list = sorted(desc_list, reverse=True, key=str.lower)
        assert desc_list == sorted_list, f'{sort_by} list is not sorted in descending order according to {sort_by}'

