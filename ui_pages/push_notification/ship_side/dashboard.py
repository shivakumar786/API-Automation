__author__ = 'saloni.pattnaik'


import time


from virgin_utils import *


class PushNotificationDashboard(General):
    """
    Page Class for Push Notification dashboard page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of dashboard page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//h6[contains(text(),'Push Notifications')]",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "tabs": "//span[text()='%s']",
            "notification_count": "//div[@class='MuiCardContent-root']/h3",
            "schedule_count": "//h6[text()='Scheduled']/../..//div[@class='MuiCardContent-root']/h3 ",
            "download_icon": "//span[@edge='end']/img",
            "pdf": "//h6[text()='Download PDF']",
            "excel": "//h6[text()='Download EXCEL']",
            "success_message": "//div[contains(text(),'Success')]"
        })

    def click_on_tabs_from_dashboard(self, tab_name):
        """
        To click on tabs from the dashboard
        :param tab_name:
        """
        self.webDriver.scroll_complete_page_top()
        self.webDriver.explicit_visibility_of_element(element=self.locators.tabs % tab_name, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.tabs % tab_name, locator_type="xpath")
        self.wait_for_loader_to_complete()

    def wait_for_loader_to_complete(self):
        """
        Function to wait for page loading to complete
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=160)

    def get_dashboard_count(self):
        """
        To get dashboard count
        :return:
        """
        return self.webDriver.get_text(element=self.locators.notification_count, locator_type="xpath")

    def get_notification_count(self, old_notification_count):
        """
        To get the count of sent notification
        :return:
        """
        new_count = ''
        for retry in range(0, 10):
            self.webDriver.page_refresh()
            self.wait_for_loader_to_complete()
            new_notification_count = self.get_dashboard_count()
            new_count.replace(new_count, str(new_notification_count))
            if new_notification_count >= old_notification_count:
                return True
        else:
            logger.info(f"old count is {old_notification_count} and new count is {new_count}")
            return False

    def get_notification_count_after_deleting(self, old_notification_count):
        """
        To get the count of sent notification
        :return:
        """
        new_count = ''
        for retry in range(0, 10):
            self.webDriver.page_refresh()
            self.wait_for_loader_to_complete()
            new_notification_count = self.get_dashboard_count()
            new_count = new_count.replace(new_count, str(new_notification_count))
            if new_notification_count < old_notification_count:
                return True
        else:
            logger.info(f"old count is {old_notification_count} and new count is {new_count}")
            return False

    def get_success_message(self):
        """
        verifying success message after performing action
        """
        time.sleep(5)
        return self.webDriver.get_text(element=self.locators.success_message, locator_type="xpath")

    def get_scheduled_notification_count(self):
        """
        To get the count of sent  scheduled notification
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.schedule_count, locator_type="xpath", time_out=60)
        return self.webDriver.get_text(element=self.locators.schedule_count, locator_type="xpath")

    def get_new_scheduled_notification_count(self, old_notification_count):
        """
        To get the count of sent  scheduled notification
        :return:
        """
        new_count = ''
        for retry in range(0, 10):
            self.webDriver.page_refresh()
            self.wait_for_loader_to_complete()
            new_scheduled_notification_count = self.get_scheduled_notification_count()
            new_count.replace(new_count, str(new_scheduled_notification_count))
            if new_scheduled_notification_count >= old_notification_count:
                return True
        else:
            logger.info(f"old count {old_notification_count} and new count {new_count}")
            return False

    def click_download(self):
        """
        To click on download option
        :return:
        """
        time.sleep(5)
        self.webDriver.click(element=self.locators.download_icon, locator_type="xpath")

    def click_pdf(self):
        """
        To click pdf option
        :return:
        """
        self.webDriver.click(element=self.locators.pdf, locator_type="xpath")
        window = self.webDriver.get_current_window()
        self.webDriver.switch_to_main_tab(window)
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('after_download_pdf_click')

    def verify_pdf(self, file_name):
        """
        Verify report exported as PDF
        :param file_name
        """
        self.webDriver.get_file_content()
        download_path = f"{os.getcwd()}/{file_name}"
        if len(download_path) > 0:
            pdf_path = f'{download_path}.pdf'
            pdfFileObj = open(pdf_path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            pagecount = len(pdfReader.pages)
            i = 0
            data = []
            while i < pagecount:
                pageObj = pdfReader.pages[i]
                data.append(pageObj.extract_text().split())
                i += 1
            assert len(data) != 0, "No data available"
            pdfFileObj.close()
            os.remove(f"{download_path}.pdf")
        else:
            raise Exception("File is not transferred successfully")

    def click_excel(self):
        """
        To click excel option
        :return:
        """
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.excel, locator_type="xpath")
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('after_export_click')

    def verify_excel(self, file_name):
        """
        To verify downloaded excel
        :param file_name:
        :return:
        """
        self.webDriver.get_file_content()
        download_path = f"{os.getcwd()}/{file_name}"
        if len(download_path) > 0:
            xlsx_file = f'{download_path}.xlsx'
            wb = openpyxl.load_workbook(xlsx_file)
            ws = wb.active
            data = list(ws.iter_rows(values_only=True))
            assert len(data) != 0, "No data available"
            rows_count = len(data) - 3
            os.remove(f"{download_path}.xlsx")
        else:
            raise Exception("File is not transferred successfully")

        return rows_count
