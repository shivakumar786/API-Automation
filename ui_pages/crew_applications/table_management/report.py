__author__ = 'saloni.pattnaik'

from virgin_utils import *
from datetime import date
import random
import string


class TableManagementReport(General):
    """
    Page Class For report To Table Management
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of admin page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "export": "//*[@text='EXPORT']",
            "csv": "//*[@text='CSV']",
            "pdf": "//*[@text='PDF']",
            "export_button": "(//*[@text='EXPORT'])[2]",
            "allow":  "//*[@text='Allow']",
        })

    def verify_csv_report(self):
        """
        To verify exported report
        :return:
        """
        self.webDriver.check_local_system_download(file_path="/Internal storage/Download/")

    def click_export_csv(self):
        """
        To click export csv
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.export, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.export, locator_type='xpath')
        if self.webDriver.explicit_visibility_of_element(element=self.locators.csv, locator_type='xpath', time_out=60):
            self.webDriver.click(element=self.locators.csv, locator_type='xpath')
            self.webDriver.click(element=self.locators.export_button, locator_type='xpath')
            if self.webDriver.explicit_visibility_of_element(element=self.locators.allow, locator_type='xpath', time_out=60):
                self.webDriver.click(element=self.locators.allow, locator_type='xpath')
        else:
            return False

    def click_export_pdf(self):
        """
        To click export pdf
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.export, locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.export, locator_type='xpath')
        if self.webDriver.explicit_visibility_of_element(element=self.locators.pdf, locator_type='xpath', time_out=60):
            self.webDriver.click(element=self.locators.csv, locator_type='xpath')
            self.webDriver.click(element=self.locators.export_button, locator_type='xpath')
        else:
            return False
