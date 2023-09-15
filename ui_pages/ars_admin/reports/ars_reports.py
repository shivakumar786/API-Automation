__author__ = 'prahlad.sharma'

from virgin_utils import *


class ArsReports(General):
    """
    Page Class for ARS admin reports
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of ars admin reports page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "table_rows": "//div[@class='rt-tr-group']",
            "header_title": "//h1[contains(text(),'ARS Crew')]",
            "username": "//input[@name='username']",
            "password": "//input[@name='password']",
            "remember_me": "//label[contains(text(),'Remember Me')]",
            "login_button": "//button[contains(text(),'LOGIN')]",
            "invalid_login_toast": "//div[@class='notification is-danger']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "ars_admin_header": "//strong[contains(@class,'is-size-5')]",
            "dashboard_header_title": "//div[@class='card-header-title is-size-5']",
            "left_navigation_reports": "(//div[@class='link-text' and text()='Reports'])[2]",
            "search": "//input[@class='NavSearchFieldTextBox']",
            "reports_header": "//h1[text()='Reports']",
            "particular_report": "//a[text()='%s']",
            "full_activity_detail_report": "//a[text()='Full Activity Detail Report']",
            "sailor_experience_status_report": "//a[text()='Sailor Experience Status Report']",
            "vendor_manifest_detail_report": "//a[text()='Vendor Manifest Detail Report']",
            "active_voyage_name": "(//div[@class='react-select__single-value css-1uccc91-singleValue'])[2]",
            "particular_report_header": "//div[@class='column title is-4']",
            "printed_by": "(//div[@class='columns']/div[@class='column'][1])[2]",
            "printed_on": "(//div[@class='columns']/div[@class='column'][1])[3]",
            "voyage_id": "(//div[@class='columns']/div[@class='column is-7'][1])[1]",
            "voyage_date": "(//div[@class='columns']/div[@class='column is-7'][1])[2]",
            "back_button": "//a[@class='back-button']/h5",
            "export_icon": "//div[@class='dropdown-trigger' and text()='Export'] ",
            "export_csv": "//button[@class='button btn-export ' and text()='Excel File']",
            "export_pdf": "//button[@class='button btn-export ' and text()='PDF']",
            "export": "//button[@class='button is-primary ']",
            "sort_by": "//div[@class='rt-th -cursor-pointer']/div[text()='%s']",
            "sort_descending_by": "//div[@class='rt-th -sort-asc -cursor-pointer']/div[text()='%s']",
            "column_values": "//div[@class='rt-tbody']/div[@class='rt-tr-group'][%s]//div[@class='rt-td'][%s]",
            "no_records": "//div[@class='rt-noData']",
            "header_name": "//div[@class='rt-tr']/div",
            "filter": "//img[@class='SVGContainer btn-img-clr']",
            "filter_header": "(//div[@class='title is-4 has-text-left'][1])[1]",
            "filter_select_port": "//div[@class='column card-header-title point-button'][contains(text(),'Port')]",
            "filter_port_portsmouth": "//label[@class='break-text']",
            "filter_port_bimini": "//span[contains(text(),'The Beach Club At Bimini')]",
            "apply_filter": "//button[contains(text(),'APPLY')]",
            "clear_filter": "//button[contains(text(),'CLEAR')]",
            "filter_activity": "//div[@class='column card-header-title point-button'][text()='Activity']",
            "filter_activity_razzle_dazzle": "//span[contains(text(),'Razzle Dazzle Restaurant')]",
            "filter_activity_pdg": "//span[contains(text(),'Portsmouth Disembarkation Group')]",
            "filter_activity_two_tank_scuba_dive": "//span[contains(text(),'Guided Two-Tank Scuba Dive')]",
            "filter_status": "//div[@class='column card-header-title point-button'][contains(text(),'Status')]",
            "filter_vendor": "//div[@class='column card-header-title point-button'][contains(text(),'Vendor')]",
            "filter_status_open": "//span[contains(text(),'Open')]",
            "add_column_dropdown": "//div[@class='dropdown-trigger']//img[contains(@class,'SVGContainer')]",
            "column_added": "//label[contains(text(),'%s')]",
            "filter_vendor_adventure": "//span[contains(text(),'BIMINI SCUBA CENTER / SBC LTD')]",
            "filter_value": "//label[@class='break-text']",
            "select_port": "//*[text()='Port']/../../following-sibling::div/div/div[1]",
            "report_list": "//*[@class='rt-tbody']/div"
        })

    def click_reports_in_left_panel(self):
        """
        To open reports section from left panel
        """
        self.webDriver.click(element=self.locators.left_navigation_reports, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.allure_attach_jpeg('click_reports_in_left_panel')

    def verify_ars_admin_header_on_top_left_corner(self):
        """
        Verify ARS admin header on top left corner
        """
        ars_admin_header = self.webDriver.get_text(element=self.locators.ars_admin_header, locator_type='xpath')
        if ars_admin_header == "ARS Admin":
            logger.debug("ARS Admin header is present on reports page")
        else:
            raise Exception("ARS Admin header is not present on reports page")
        self.webDriver.allure_attach_jpeg('verify_ars_admin_header_on_top_left_corner')

    def verify_search_bar_present(self):
        """
        Verify ARS admin search bar on top
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.search, locator_type='xpath'):
            logger.debug("Search option available on Dashboard")
        else:
            raise Exception("Search option not available on Dashboard")
        self.webDriver.allure_attach_jpeg('verify_search_bar_present')

    def verify_reports_header(self):
        """
        Verify Reports header
        """
        reports_header = self.webDriver.get_text(element=self.locators.reports_header, locator_type='xpath')
        if reports_header == "Reports":
            logger.debug("User has landed on Reports page")
        else:
            raise Exception("User has not landed on Reports page")
        self.webDriver.allure_attach_jpeg('verify_reports_header')

    def verify_all_reports(self, report_name):
        """
        Verify Reports name
        :param report_name:
        """
        get_report_name = self.webDriver.get_text(element=self.locators.particular_report % report_name, locator_type='xpath')
        if get_report_name == report_name:
            logger.debug(f"{report_name} is available on reports page")
        else:
            raise Exception(f"{report_name} is not available on reports page")
        self.webDriver.allure_attach_jpeg('verify_all_reports')

    def verify_active_voyage_name(self, voyage_name):
        """
        Verify active voyage name
        :param voyage_name:
        """
        selected_voyage_name = self.webDriver.get_text(element=self.locators.active_voyage_name, locator_type='xpath')
        if selected_voyage_name.split()[0] == voyage_name.split()[0] and selected_voyage_name.split()[1] == voyage_name.split()[1]:
            logger.debug(f"{selected_voyage_name} Selected Voyage name is matching with backend response")
        else:
            raise Exception(f"{selected_voyage_name} Selected Voyage name is not matching with backend response")
        self.webDriver.allure_attach_jpeg('verify_active_voyage_name')

    def open_particular_report(self, report_name):
        """
        Function to open particular report
        :param report_name:
        """
        self.webDriver.click(element=self.locators.particular_report % report_name, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.loader, locator_type='xpath'):
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=120)
        self.webDriver.allure_attach_jpeg('open_particular_report')

    def verify_report_header(self, report_name):
        """
        Function to verify reports header after opening a particular report
        :param report_name:
        """
        reports_header = self.webDriver.get_text(element=self.locators.particular_report_header, locator_type='xpath')
        if reports_header == report_name:
            logger.debug(f"User has landed on {report_name} page")
        else:
            raise Exception(f"User has not landed on {report_name} page")
        self.webDriver.allure_attach_jpeg('verify_report_header')

    def verify_report_ui(self, test_data, report_name):
        """
        Function to verify report ui
        """
        if report_name == "":
            printed_by = self.webDriver.get_text(element=self.locators.printed_by, locator_type='xpath')
            assert printed_by == 'Printed By: Vertical QA', 'Failed to verify printed by crew name'
        printed_on = self.webDriver.get_text(element=self.locators.printed_on, locator_type='xpath')
        printed_on = printed_on[:-9]
        ship_date = datetime.strptime(test_data['shipDate'], '%Y-%m-%d').strftime('%m/%d/%Y')
        assert printed_on == f'Printed On: {ship_date}', 'Failed to verify printed on date'
        voyage_id = self.webDriver.get_text(element=self.locators.voyage_id, locator_type='xpath')
        assert voyage_id == f"Voyage ID: {test_data['voyageNumber']}"
        voyage_date = self.webDriver.get_text(element=self.locators.voyage_date, locator_type='xpath')
        assert voyage_date == f"Voyage: {test_data['embarkDate']} - {test_data['debarkDate']}",\
            "Failed to verify voyage from and to date"
        self.webDriver.allure_attach_jpeg('verify_report_ui')

    def click_back_button(self):
        """
        Function to click on back button
        """
        self.webDriver.scroll_complete_page_top()
        self.webDriver.click(element=self.locators.back_button, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('click_back_button')

    def availability_of_data(self):
        """
        Function to check if data i.e rows is available or not
        :return:
        """
        rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
        if len(rows) > 0:
            logger.debug(f"Data available on page and count is: {len(rows)}")
        else:
            raise Exception("Report is blank")
        self.webDriver.allure_attach_jpeg('availability_of_data')

    def export_report_as_excel(self):
        """
        Function to export the reports
        """
        self.webDriver.click(element=self.locators.export_icon, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.click(element=self.locators.export_csv, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.allure_attach_jpeg('after_export_click')

    def export_report_as_pdf(self, report_name):
        """
        Function to export the reports as pdf
        :param report_name:
        """
        self.webDriver.click(element=self.locators.export_icon, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.click(element=self.locators.export_pdf, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

        if report_name  == '':
            self.webDriver.click(element=self.locators.export, locator_type='xpath')
        window = self.webDriver.get_current_window()
        self.webDriver.switch_to_main_tab(window)
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('after_export_click')

    def verify_exported_report_as_excel(self, file_name, test_data, report_name):
        """
        Function to verify the exported report
        :param file_name:
        :param test_data:
        """
        ship_date = datetime.strptime(test_data['shipDate'], '%Y-%m-%d').strftime('%m/%d/%Y')
        self.webDriver.get_file_content()
        download_path = f"{os.getcwd()}/{file_name}"
        if len(download_path) > 0:
            xlsx_file = f'{download_path}.xlsx'
            wb = openpyxl.load_workbook(xlsx_file)
            ws = wb.active
            data = list(ws.iter_rows(values_only=True))
            if report_name == '':
                assert data[0][data[0].index('Printed By')+1] == 'Vertical QA', "Failed to validate printed by crew name"
                assert data[1][data[1].index('Printed On')+1].split()[0] == ship_date, "Failed to verify printed date"
                assert data[0][data[0].index('Voyage ID')+1] == test_data['voyageNumber'], "Failed to verify voyage number"
                assert data[1][data[1].index('Voyage')+1] == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify voyage from and to date "
                rows_count = len(data) - 3
                os.remove(f"{download_path}.xlsx")
            elif report_name == 'Refunded Bookings Report':
                assert "vertical-qa" in data[0][0], "Failed to validate printed by crew name"
                assert ship_date in data[1][0], "Failed to verify printed date"
                assert test_data['voyageNumber'] in data[0][8], "Failed to verify voyage number"
                assert f"{test_data['embarkDate']} - {test_data['debarkDate']}" in data[1][8], "Failed to verify voyage from and to date "
                rows_count = len(data) - 3
                os.remove(f"{download_path}.xlsx")
            else:
                assert data[1][0][8:31] == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify voyage from and to date "
                assert data[2][0][11:23] == test_data['voyageNumber'], "Failed to verify voyage number"
                assert data[3][0][12:22] == ship_date, "Failed to verify printed date"
                rows_count = len(data) - 3
                os.remove(f"{download_path}.xlsx")
        else:
            raise Exception("File is not transferred successfully")

        return rows_count

    def verify_exported_report_as_pdf(self, file_name, test_data, report_name):
        """
        Verify report exported as PDF
        :param test_data:
        :param file_name
        """
        ship_date = datetime.strptime(test_data['shipDate'], '%Y-%m-%d').strftime('%m/%d/%Y')
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
            if report_name == '':
                assert data[0][2] == test_data['voyageNumber'], "Failed to verify voyage number"
                assert f"{data[0][4]} - {data[0][6][0:10]}" == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify from and to date "
                assert f"{data[0][7][3:]} {data[0][8]}" == "Vertical QA", "failed to verify printed by crew"
                assert data[0][11] == ship_date, "Failed to verify ship date"
                pdfFileObj.close()
                os.remove(f"{download_path}.pdf")
            elif report_name == "Sales Report":
                assert data[0][2] == test_data['voyageNumber'], "Failed to verify voyage number"
                assert f"{data[0][4]} - {data[0][6][0:10]}" == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify from and to date "
                assert f"{data[0][8]} {data[0][9]}" == "Vertical QA", "failed to verify printed by crew"
                assert data[0][12] == ship_date, "Failed to verify ship date"
                pdfFileObj.close()
                os.remove(f"{download_path}.pdf")
            elif report_name == "Refunded Bookings Report":
                assert data[0][4] == test_data['voyageNumber'], "Failed to verify voyage number"
                assert f"{data[0][10]} - {data[0][12][0:10]}" == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify from and to date "
                assert "vertical-qa" in data[0][2][:11], "failed to verify printed by crew"
                assert data[0][7] == ship_date, "Failed to verify ship date"
                pdfFileObj.close()
                os.remove(f"{download_path}.pdf")
            else:
                assert f"{data[0][3]} - {data[0][5]}" == f"{test_data['embarkDate']} - {test_data['debarkDate']}", \
                    "Failed to verify from and to date "
                assert data[0][8][:12] == test_data['voyageNumber'], "Failed to verify voyage number"
                pdfFileObj.close()
                os.remove(f"{download_path}.pdf")
        else:
            raise Exception("File is not transferred successfully")

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

    def blank_list(self):
        """
        Verification of blank list
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_records, locator_type='xpath'):
            return True
        else:
            return False

    def apply_and_verify_port_filter(self, test_data):
        """
        Function to select port in filter
        :param test_data:
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.filter_select_port, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_value, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        if not self.blank_list():
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            if len(rows) < 11:
                val = len(rows)+1
            else:
                val = 11
            for i in range(1, val):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, test_data['Port_position']), locator_type='xpath')
                assert col_value == 'BIM', 'Bimini port not matching in filter'
        else:
            logger.debug('Data not available after applying filter')

    def apply_and_verify_activity_filter(self, test_data):
        """
        Function to select activity in filter
        :param test_data:
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.clear_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_activity, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_value, locator_type='xpath')
        filter_applied_value = self.webDriver.get_text(element=self.locators.filter_value, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        if not self.blank_list():
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            if len(rows) < 11:
                val = len(rows)+1
            else:
                val = 11
            for i in range(1, val):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, test_data['Event Name_position']), locator_type='xpath')
                assert col_value == filter_applied_value, f'{filter_applied_value} Activity not matching in filter'
        else:
            logger.debug('Dataa not available after applying filter')

    def apply_and_verify_status_filter(self, test_data):
        """
        Function to select activity in filter
        :param test_data:
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.clear_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_status, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_value, locator_type='xpath')
        filter_applied_value = self.webDriver.get_text(element=self.locators.filter_value, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        if not self.blank_list():
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            if len(rows) < 11:
                val = len(rows)+1
            else:
                val = 11
            for i in range(1, val):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, test_data['Event Status_position']), locator_type='xpath')
                assert col_value == filter_applied_value.upper(), f'{filter_applied_value} status not matching in filter'
        else:
            logger.debug('Data not available after applying filter')

    def add_column(self, column_name):
        """
        Function to add a column in report
        """
        self.webDriver.click(element=self.locators.add_column_dropdown, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.click(element=self.locators.column_added % column_name, locator_type='xpath')

    def apply_and_verify_activity_filter_in_waiver_detail_report(self, test_data):
        """
        Function to select activity in filter
        :param test_data:
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.clear_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_activity, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_value, locator_type='xpath')
        filter_applied_value = self.webDriver.get_text(element=self.locators.filter_value, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        if not self.blank_list():
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            if len(rows) < 11:
                val = len(rows)+1
            else:
                val = 11
            for i in range(1, val):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, test_data['Event Name_position']), locator_type='xpath')
                assert col_value == filter_applied_value, f'{filter_applied_value} Activity not matching in filter'
        else:
            logger.debug('Data not available after applying filter')

    def apply_and_verify_vendor_filter(self, test_data):
        """
        Function to select vendor in filter
        :param test_data:
        """
        self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_header,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.clear_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_vendor, locator_type='xpath')
        self.webDriver.click(element=self.locators.filter_value, locator_type='xpath')
        filter_applied_value = self.webDriver.get_text(element=self.locators.filter_value, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_filter, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        if not self.blank_list():
            rows = self.webDriver.get_elements(element=self.locators.table_rows, locator_type='xpath')
            if len(rows) < 11:
                val = len(rows)+1
            else:
                val = 11
            for i in range(1, val):
                col_value = self.webDriver.get_text(
                    element=self.locators.column_values % (i, test_data['Vendor Name_position']), locator_type='xpath')
                assert col_value == filter_applied_value, f'{filter_applied_value} vendor not matching in filter'
        else:
            logger.debug('Data not available after applying filter')

    def apply_filter_report(self):
        """
        to verify current booking and cancellation report
        :return:
        """
        self.webDriver.click(element=self.locators.filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.clear_filter, locator_type="xpath")
        self.webDriver.click(element=self.locators.filter_value, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply_filter, locator_type="xpath")
        report_list = self.webDriver.get_elements(element=self.locators.report_list, locator_type="xpath")
        if not len(report_list) > 0:
            logger.info("no records found for the selected port/activity")