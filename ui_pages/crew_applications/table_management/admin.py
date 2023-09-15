__author__ = 'saloni.pattnaik'

from virgin_utils import *
from datetime import date
import random
import string


class TableManagementAdmin(General):
    """
    Page Class For admin To Table Management
    """
    def __init__(self, web_driver):
        """
        To Initialize the locators of admin page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "admin": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Admin']",
            "admin_drop_down": "//*[@resource-id='dropdown-venues_selected_title']",
            "admin_tabs": "(//*[@class='android.widget.ListView'])[1]//*[@class='android.view.View']//*[@content-desc]",
            "tab": "//*[@text='%s']",
            "current_voyage": "(//*[@resource-id='admin__sidebar__back']/..//*[@class='android.widget.TextView'])[1]",
            "edit_option": "//*[@resource-id='admin-sailing-table-edit-button-icon-0']",
            "back_button": "//*[@resource-id='admin__sidebar__back']//*[@class='android.widget.Image']",
            "hamburger_menu_icon": "//*[@resource-id='button-main-menu']",
            "click_tm": "//*[@resource-id='android:id/content']//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']",
            "complete_voyages": "//*[contains(@resource-id,'admin-sailings-list-item')]",
            "sort": "//*[@resource-id='sailings-content-header-set-sorting']",
            "complte_date": "//*[@resource-id='admin-sailings-list-item-0']//*[@class='android.widget.TextView']",
            "preset": "((//*[contains(@resource-id,'admin-sailings-list-item')])[%s]//*[@class='android.widget.TextView'])[3]",
            "edit_icon": "//*[contains(@resource-id,'admin-sailing-table-edit-button-icon')]",
            "tabs": "//*[@content-desc='%s']",
            "add_capacity": "//*[@resource-id='table-capacity-add']",
            "save": "//*[@resource-id='sailing-settings-admin-button-save']",
            "add_periods": "//*[@resource-id='precruise-booking-table-list-add-period']",
            "sailor_availability": "//*[@text='Availability for Booking via Sailor App']",
            "delete_slot": "//*[@resource-id='precruise-booking-table-list-remove-period']",
            "host_availability": "//*[@text='Availability for Host Booking']",
            "new_layout": "//*[@text='NEW LAYOUT']",
            "name_popup": "//*[@resource-id='input-layout-name__input']",
            "create": "//*[@resource-id='new-popup-button-close']",
            "layout_name": "//*[@text='Test_layout_automation']",
            "tables": "(//*[@resource-id='table-layout-container'])[2]",
            "new_table": "//*[@text='NEW TABLE']",
            "create_table": "//*[@text='CREATE TABLE']",
            "new_tables": "//*[@resource-id='table-icon_text']",
            "layout_back_button": "//*[@content-desc='layouts']//*[@class='android.widget.Image']",
            "discard": "//*[@text='DISCARD']",
            "layout_header": "//*[@text='Creating a new layout']",
            "new_preset": "//*[@text='NEW PRESET']",
            "preset_name": "//*[@resource-id='input-preset-name__input']",
            "preset_header": "//*[@text='Create new preset']",
            "preset_names": "((//*[contains(@resource-id,'overflow-menu-button')])[%s]/../..//*[@class='android.widget.TextView'][2])[1]",
            "three_dot_preset": "(//*[contains(@resource-id,'overflow-menu-button')])[%s]",
            "delete_preset": "//*[@text='DELETE']",
            "delete_msg": "//*[@text='Preset has been deleted']",
            "todays_date": "(((//*[contains(@resource-id,'admin-sailing-table-row')])[%s])//*[@class='android.view.View'][2])[1]",
            "edit_icons": "(((//*[contains(@resource-id,'admin-sailing-table-row')])[%s])//*[@class='android.view.View'][2])[2]",
            "layout": "//*[@text='Layouts']",
            "layouts": "//*[@resource-id='table-layout-container']",
            "normal_tables": "//*[contains(@resource-id,'table-drag-container')]",
            "normal_table": "//*[contains(@resource-id,'table-drag-container')][%s]",
            "custom_icon": "//*[contains(@resource-id,'custom-table-layout-drag-source-item-show-settings')]",
            "main_table_no": "//*[contains(@resource-id,'custom-table-layout-update-sidebar')]//*[@class='android.widget.TextView']",
            "link": "//*[@text='LINK']",
            "link_done": "//*[@text='DONE']",
            "link_close": "//*[@resource-id='button-close-custom-table-layout-update-sidebar-button-close']",
            "reports": "//*[@resource-id='AUTOTEST__sidebar__hierarchic__Table-Management']//*[@resource-id='AUTOTEST__sidebar__simple__Reports']",
            "all_preset": "//*[contains(@resource-id,'overflow-menu-button')]",
            "presets_name": "((//*[contains(@resource-id,'overflow-menu-button')])[%s]/../..//*[@class='android.widget.TextView'])[1]",
            "preset_three_dot": "(//*[contains(@resource-id,'overflow-menu-button')])[%s]",
            "rename": "//*[@text='RENAME']",
            "preset_header_rename": "//*[contains(@text,'Rename preset')]",
            "delete": "//*[@text='DELETE']",
            "total_tables": "//*[contains(@resource-id,'table-drag-container')]",
            "source_table": "(//*[contains(@resource-id,'table-drag-container')])[1]",
            "dest_table": "(//*[contains(@resource-id,'table-drag-container')])[2]",
            "upcoming_back": "//*[@resource-id='admin__sidebar__back']",
            "add_period": "//*[@text='ADD PERIOD']",
            "start_time": "//*[@resource-id='time-timeStart_0_0']",
            "end_time": "//*[@resource-id='time-timeStop_0_0']",
            "link_close_ok": "//*[@resource-id='new-popup-button-close']",
        })

    def verify_delete_preset(self, delete_preset):
        """
        To verify deleted preset
        :param delete_preset:
        :return:
        """
        all_presets = self.webDriver.get_elements(element=self.locators.all_preset, locator_type='xpath')
        for preset in range(1, len(all_presets)):
            if self.webDriver.get_text(element=self.locators.presets_name % preset, locator_type='xpath') == delete_preset:
                return False
            else:
                return True

    def delete_new_preset(self):
        """
        To delete new preset
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.create, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def verify_rename_preset(self, rename):
        """
        To verify rename preset
        :param rename:
        :return:
        """
        self.webDriver.wait_for(5)
        all_presets = self.webDriver.get_elements(element=self.locators.all_preset, locator_type='xpath')
        for preset in range(1, len(all_presets)):
            if self.webDriver.get_text(element=self.locators.presets_name % preset, locator_type='xpath') == rename:
                self.webDriver.click(element=self.locators.preset_three_dot % preset, locator_type='xpath')
                return True

    def rename_new_preset(self, test_data):
        """
        To rename new preset
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.rename, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.rename, locator_type='xpath')
        test_data['preset_rename'] = test_data['preset_name'] + "_rename"
        self.webDriver.explicit_visibility_of_element(element=self.locators.preset_name, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.clear_text(element=self.locators.preset_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.preset_name, locator_type='xpath', text=test_data['preset_rename'])
        self.webDriver.click(element=self.locators.preset_header_rename, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def click_three_dot_preset(self, presetname):
        """
        To click on three dot option for new preset
        :param presetname:
        :return:
        """
        preset_len = 10
        while preset_len != 0:
            all_presets = self.webDriver.get_elements(element=self.locators.all_preset, locator_type='xpath')
            for preset in range(1, len(all_presets)+1):
                if self.webDriver.get_text(element=self.locators.presets_name % preset, locator_type='xpath') == presetname:
                    self.webDriver.click(element=self.locators.preset_three_dot % preset, locator_type='xpath')
                    preset_len = 1
                    break
            if preset_len == 1:
                break
            self.webDriver.scroll_mobile(2233, 1366, 2250, 494)
            preset_len = preset_len-1

    def open_report_page(self):
        """
        To open table management  report page
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu_icon, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu_icon, locator_type='xpath')
        self.webDriver.scroll_mobile(540, 1492, 500, 390)
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.click(element=self.locators.reports, locator_type='xpath')

    def link_table(self, test_data):
        """
        To link tables
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.normal_tables, locator_type='xpath', time_out=60)
        tables = self.webDriver.get_elements(element=self.locators.normal_tables, locator_type='xpath')
        self.webDriver.click(element=self.locators.normal_table % random.randint(1, len(tables)), locator_type='xpath')
        self.webDriver.click(element=self.locators.custom_icon, locator_type='xpath')
        test_data['main_table_no'] = self.webDriver.get_text(element=self.locators.main_table_no, locator_type='xpath')
        self.webDriver.scroll_mobile(630, 1357, 671, 1039)
        self.webDriver.click(element=self.locators.link, locator_type='xpath')
        tables = self.webDriver.get_elements(element=self.locators.normal_tables, locator_type='xpath')
        self.webDriver.click(element=self.locators.normal_table % random.randint(1, len(tables)), locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.link_close_ok, locator_type='xpath'):
            self.webDriver.click(element=self.locators.link_done, locator_type='xpath')
            self.webDriver.click(element=self.locators.link_close, locator_type='xpath')
            if self.webDriver.is_element_display_on_screen(element=self.locators.link_close, locator_type='xpath'):
                raise Exception("Tables are not linked")
            else:
                self.webDriver.click(element=self.locators.layout_back_button, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.link_close_ok, locator_type='xpath')
            self.webDriver.click(element=self.locators.link_close, locator_type='xpath')
            self.webDriver.click(element=self.locators.layout_back_button, locator_type='xpath')

    def click_edit_option(self):
        """
        To click on edit option
        :return:
        """
        today = date.today()
        today_date = today.strftime("%d")
        for day in range(1, 10):
            if (self.webDriver.get_text(element=self.locators.todays_date % day, locator_type='xpath').split(","))[1].split(" ")[2] == today_date:
                self.webDriver.click(element=self.locators.edit_icons % day, locator_type='xpath')
                self.webDriver.click(element=self.locators.layout, locator_type='xpath')
                self.webDriver.explicit_visibility_of_element(element=self.locators.layouts, locator_type='xpath', time_out=200)
                self.webDriver.click(element=self.locators.layouts, locator_type='xpath')
                break

    def new_preset(self, test_data):
        """
        To create new preset
        :param test_data:
        :return:
        """
        test_data['preset_name']="Test_preset_automation_" + ''.join(random.sample(string.ascii_lowercase, 5))
        self.webDriver.click(element=self.locators.new_preset, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.preset_name, locator_type='xpath', time_out=60)
        self.webDriver.set_text(element=self.locators.preset_name, locator_type='xpath', text=test_data['preset_name'])
        self.webDriver.click(element=self.locators.preset_header, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def open_manage_preset(self):
        """
        To open manage preset
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tab % 'Manage Presets', locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.tab % 'Manage Presets', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.all_preset, locator_type='xpath',
                                                      time_out=200)

    def add_table(self):
        """
        To add table in created layout
        :return:
        """
        self.webDriver.click(element=self.locators.tables, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.discard, locator_type='xpath'):
            self.webDriver.click(element=self.locators.discard, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.new_table, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.new_table, locator_type='xpath')
        self.webDriver.click(element=self.locators.create_table, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.new_table, locator_type='xpath',
                                                      time_out=120)
        if self.webDriver.is_element_display_on_screen(element=self.locators.new_tables, locator_type='xpath'):
            self.webDriver.click(element=self.locators.layout_back_button, locator_type='xpath')
            return True
        else:
            self.webDriver.click(element=self.locators.layout_back_button, locator_type='xpath')
            return False

    def verify_layout(self):
        """
        To verify added layout
        :return:
        """
        self.webDriver.wait_for(5)
        layouts_name = self.webDriver.get_web_element(element=self.locators.layout_name, locator_type='xpath').text
        if layouts_name != "Test_layout_automation":
            return False
        else:
            return True

    def add_new_layout(self):
        """
        To add new layout
        :return:
        """
        self.webDriver.click(element=self.locators.new_layout, locator_type='xpath')
        self.webDriver.click(element=self.locators.name_popup, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.name_popup, locator_type='xpath', text= "Test_layout_automation")
        self.webDriver.click(element=self.locators.layout_header, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def click_layout(self):
        """
        To click layouts
        :return:
        """
        self.webDriver.click(element=self.locators.tabs % 'Layouts', locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.discard, locator_type='xpath'):
            self.webDriver.click(element=self.locators.discard, locator_type='xpath')
        self.webDriver.click(element=self.locators.tabs % 'Layouts', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.new_layout, locator_type='xpath',
                                                      time_out=200)

    def remove_slots(self):
        """
        To remove slots
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete_slot, locator_type='xpath',
                                                      time_out=200)
        self.webDriver.click(element=self.locators.delete_slot, locator_type='xpath')
        if not self.webDriver.is_element_enabled(element=self.locators.save, locator_type='xpath'):
            return False
        else:
            return True

    def add_slots(self):
        """
        To add slots
        :return:
        """
        self.webDriver.wait_for(3)
        if self.webDriver.is_element_display_on_screen(element=self.locators.add_period, locator_type='xpath'):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.start_time, locator_type='xpath'):
                self.webDriver.click(element=self.locators.add_period, locator_type='xpath')
                self.webDriver.click(element=self.locators.start_time, locator_type='xpath')
                self.webDriver.set_text(element=self.locators.start_time, locator_type='xpath', text="12:00 AM")
                self.webDriver.click(element=self.locators.end_time, locator_type='xpath')
                self.webDriver.set_text(element=self.locators.end_time, locator_type='xpath', text="11:59 PM")
                if not self.webDriver.is_element_enabled(element=self.locators.save, locator_type='xpath'):
                    return False
                else:
                    return True
            else:
                self.remove_slots()
                return True
        else:
            self.remove_slots()
            return True

    def click_sailor_booking(self):
        """
        To click sailor booking
        :return:
        """
        self.webDriver.click(element=self.locators.tabs % 'Sailor Booking', locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.discard, locator_type='xpath'):
            self.webDriver.click(element=self.locators.discard, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.sailor_availability, locator_type='xpath',
                                                      time_out=200)

    def click_host_booking(self):
        """
        To click sailor booking
        :return:
        """
        self.webDriver.click(element=self.locators.tabs % 'Host Booking', locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.discard, locator_type='xpath'):
            self.webDriver.click(element=self.locators.discard, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.host_availability, locator_type='xpath',
                                                      time_out=200)

    def add_tables(self):
        """
        To add tables
        :return:
        """
        self.webDriver.click(element=self.locators.add_capacity, locator_type='xpath')
        if not self.webDriver.is_element_enabled(element=self.locators.save, locator_type='xpath'):
            return False
        else:
            return True

    def click_tables(self):
        """
        To click tables
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tabs % 'Tables', locator_type='xpath', time_out=180)
        self.webDriver.click(element=self.locators.tabs % 'Tables', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.add_capacity, locator_type='xpath',
                                                      time_out=200)

    def click_edit(self):
        """
        To click edit icon
        :return:
        """
        self.webDriver.click(element=self.locators.edit_icon, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.tabs % 'Reservations', locator_type='xpath',
                                                      time_out=200)

    def open_upcoming_voyage(self):
        """
        To open upcoming voyage
        :return:
        """
        self.webDriver.click(element=self.locators.complete_voyages, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.edit_icon, locator_type='xpath',
                                                      time_out=200)

    def verify_applied_preset(self):
        """
        To verify preset has applied or not
        :return:
        """
        voyages = self.webDriver.get_elements(element=self.locators.complete_voyages, locator_type='xpath')
        for voyage in range(1, len(voyages)):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.preset % voyage, locator_type='xpath'):
                return False
            else:
                return True

    def open_upcoming_tab(self):
        """
        To open upcoming tab
        :return:
        """
        self.webDriver.click(element=self.locators.tab % 'Upcoming', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.complete_voyages, locator_type='xpath',
                                                      time_out=200)

    def verify_completed_tab(self):
        """
        To verify completed tab
        :return:
        """
        if len(self.webDriver.get_elements(element=self.locators.complete_voyages, locator_type='xpath')) == 0:
            raise Exception("completed voyages not displaying in complete tab")

    def open_completed_tab(self):
        """
        To open completed tab
        :return:
        """
        self.webDriver.click(element=self.locators.tab % 'Completed', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.complete_voyages, locator_type='xpath', time_out=200)

    def click_back_button(self):
        """
        To click back button
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.back_button, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')

    def verify_current_tab(self, test_data):
        """
        To verify current tab
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.edit_option, locator_type='xpath', time_out=120)
        current_days = self.webDriver.get_web_element(element=self.locators.current_voyage, locator_type='xpath')
        current_voyage = (datetime.strptime(test_data['firstDay'], '%Y-%m-%d').strftime('%m/%d/%Y')) + " — " + (datetime.strptime(test_data['lastDay'], '%Y-%m-%d').strftime('%m/%d/%Y'))
        if current_voyage != current_days.text:
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            return False
        else:
            self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
            return True

    def open_current_tab(self):
        """
        To open current tab
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tab % 'Current', locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.tab % 'Current', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.edit_option, locator_type='xpath', time_out=200)

    def open_admin_page(self):
        """
        To open table management  admin page
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menu_icon, locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.hamburger_menu_icon, locator_type='xpath')
        self.webDriver.scroll_mobile(540, 1492, 500, 390)
        self.webDriver.click(element=self.locators.click_tm, locator_type='xpath')
        self.webDriver.click(element=self.locators.admin, locator_type='xpath')

    def verify_admin_module(self):
        """
        To verify admin tab
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.admin_drop_down, locator_type='xpath', time_out=120)
        drop_down = self.webDriver.get_web_element(element=self.locators.admin_drop_down, locator_type='xpath')
        if drop_down.text != "The Test Kitchen":
            raise Exception("Venue not matching")
        else:
            if len(self.webDriver.get_elements(element=self.locators.admin_tabs, locator_type='xpath')) != 4:
                raise Exception("Admin tabs are not available")