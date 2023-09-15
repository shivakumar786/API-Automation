__author__ = 'bhanu.pratap'

from virgin_utils import *
from datetime import date
import random
import string


class TableManagementAdmin(General):
    """
    Page Class For admin To Table Management Web
    """
    def __init__(self, web_driver):
        """
        To Initialize the locators of admin page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "tab": "//*[text()='%s']",
            "current_voyage": "//div[@class='sailing__header__info__title']",
            "edit_option": "//span[@id='admin-sailing-table-edit-button-icon-0']//*[name()='svg']",
            "back_button": "//a[@id='admin__sidebar__back']",
            "hamburger_menu_icon": "//*[@resource-id='button-main-menu']",
            "complete_voyages": "//*[contains(@id,'admin-sailings-list-item')]",
            "hamburger_menus": "//button[@id ='button-main-menu']",
            "modules": "//*[text()='%s']",
            "all_preset": "//*[contains(@class,'presets__list__item content__list__item row')]",
            "new_preset": "//*[text()='New preset']",
            "preset_name": "//*[@id='input-preset-name__input']",
            "preset_header": "//*[text()='Create new preset']",
            "create": "//*[@id='new-popup-button-close']",
            "name": "//*[text()='%s']",
            "get_all_preset_name": "//div[contains(@class,'content__list__item__col col-4')]",
            "three_dot_session": "//div//span[text()='%s']/../following-sibling::div//button[@class='button content__list__item__dots__button']",
            "delete_three_dot": "//span[text()='Delete']",
            "ok_delete": "//*[@id='new-popup-button-close']",
            "delete": "//span[text()='Delete']",
            "rename": "//span[text()='Rename']",
            "preset_header_rename": "//*[contains(@text,'Rename preset')]",
            "complete_voyages": "//*[contains(@class,'sailings__list__item content__list__item row')]",
            "preset": "//*[contains(@class,'sailings__list__item content__list__item row')][%s]//*[@class='sailings__list__item__preset']"
        })

    def open_current_tab(self):
        """
        To open current tab
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tab % 'Current', locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.tab % 'Current', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.edit_option, locator_type='xpath',
                                                      time_out=200)

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

    def open_completed_tab(self):
        """
        To open completed tab
        :return:
        """
        self.webDriver.click(element=self.locators.tab % 'Completed', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.complete_voyages, locator_type='xpath', time_out=200)

    def verify_completed_tab(self):
        """
        To verify completed tab
        :return:
        """
        if len(self.webDriver.get_elements(element=self.locators.complete_voyages, locator_type='xpath')) == 0:
            raise Exception("completed voyages not displaying in complete tab")

    def hamburger_menus(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.hamburger_menus, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.hamburger_menus, locator_type='xpath')

    def choose_module(self, module):
        """
        Choose module
        :param module:
        :return:
        """
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.modules % module, locator_type='xpath')
        self.webDriver.wait_for(3)

    def open_manage_preset(self):
        """
        To open manage preset
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.tab % 'Manage Presets', locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.tab % 'Manage Presets', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.all_preset, locator_type='xpath',
                                                      time_out=200)

    def new_preset(self, value):
        """
        To create new preset
        :param value:
        :return:
        """
        self.webDriver.click(element=self.locators.new_preset, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.preset_name, locator_type='xpath', time_out=60)
        self.webDriver.set_text(element=self.locators.preset_name, locator_type='xpath', text=value)
        self.webDriver.click(element=self.locators.preset_header, locator_type='xpath')
        self.webDriver.click(element=self.locators.create, locator_type='xpath')

    def verify_created_preset(self, value):
        """
        Verify the preset created is present in the list
        :param value:
        :return:
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.name % value, locator_type='xpath'):
            raise Exception("Preset not created:", value)

    def delete_if_already_present(self):
        """
        Delete preset created by automation if already visible in UI and is not a part of active automation run
        :return:
        """
        preset_list = []
        self.webDriver.wait_for(5)
        presets = self.webDriver.get_elements(element=self.locators.get_all_preset_name, locator_type='xpath')
        for preset in presets:
            if "Automation" in preset.text:
                preset_list.append(self.locators.three_dot_session % preset.text)
        for pre in preset_list:
            self.webDriver.click(element=pre, locator_type='xpath')
            self.webDriver.click(element=self.locators.delete_three_dot, locator_type='xpath')
            self.webDriver.click(element=self.locators.ok_delete, locator_type='xpath')

    def find_created_preset(self, value):
        """
        Verify clicking on preset present in the list of presets
        :param value:
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.name % value, locator_type='xpath')
        self.webDriver.click(element=self.locators.three_dot_session % value, locator_type='xpath')

    def rename_created_preset(self, test_data):
        """
        reanme the existing preset
        :param test_data:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.rename, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.rename, locator_type='xpath')
        test_data['preset_rename'] = test_data['preset_name'] + "_rename"
        self.webDriver.explicit_visibility_of_element(element=self.locators.preset_name, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.clear_text(element=self.locators.preset_name, locator_type='xpath', action_type='clear')
        self.webDriver.set_text(element=self.locators.preset_name, locator_type='xpath',
                                text=test_data['preset_rename'])
        self.webDriver.click(element=self.locators.rename, locator_type='xpath')

    def verify_rename_preset(self, value1):
        """
        To verify rename preset
        :param value1:
        :return:
        """
        self.webDriver.wait_for(5)
        all_presets = self.webDriver.get_elements(element=self.locators.get_all_preset_name, locator_type='xpath')
        for preset in all_presets:
            if value1 in preset.text:
                return True
            else:
                continue

    def delete_new_preset(self, value):
        """
        To delete new preset
        :param value:
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.name % value, locator_type='xpath')
        self.webDriver.click(element=self.locators.three_dot_session % value, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delete, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.ok_delete, locator_type='xpath', time_out=30)
        self.webDriver.click(element=self.locators.ok_delete, locator_type='xpath')

    def verify_delete_preset(self, value):
        """
        To verify deleted preset
        :param value:
        :return:
        """
        all_presets = self.webDriver.get_elements(element=self.locators.all_preset, locator_type='xpath')
        for preset in all_presets:
            if not value in preset.text:
                return True

    def open_upcoming_tab(self):
        """
        To open upcoming tab
        :return:
        """
        self.webDriver.click(element=self.locators.tab % 'Upcoming', locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.complete_voyages, locator_type='xpath',
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


