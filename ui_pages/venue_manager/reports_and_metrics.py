__author__ = 'HT'

from virgin_utils import *


class ReportsAndMetrics(General):
    """
    Page Class for Reports and metrics
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Venue Manager staff page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "no_records_found": "//*[text()='No record found.']",
            "voyage_details": "voyage-details",
            "sales_report": "salesOrder",
            "order_status": "orderStatus",
            "apply": "searchSalesReportData",
            "download_icon": "//*[@class='menu-icon-dots']",
            "meal_period_chk_box": "//*[@class='main meal-period']",
            "filter_from_date": "filterFromDay",
            "from_day_filter_list": "//*[@id='voyageItinaryFrom']/option",
            "filter_from_to_date": "filterToDay",
            "to_date_filter_list": "//*[@id='voyageItinaryTo']/option",
            "filter_from_order_status": "filter-by-status",
            "from_time": "voyageFromTime",
            "to_time": "voyageToTime",
            "order_status_list": "//*[@id='ddlOrderStatus']/option",
            "download_pdf": "//*[text()='Download PDF']",
            "download_order_status_pdf": "//*[text()='Download Order Status PDF']",
            "download_excel": "//*[text()='Download Excel']",
            "download_order_status_excel": "//*[text()='Download Order Status Excel']",
            "downloading_popup": "//*[contains(text(),'OK')]",
            "current_meal_period": "//*[contains(text(),'Current Meal Period')]",
            "no_meal_period_currently": "//*[contains(text(),' No meal period currently')]",
            "order_list": "//*[@id='orderStatusReport']/tbody/tr",
            "voyage_update_icon": "update-icon",
            "voyage_drop_down": "custom-dropdown-style",
            "future_voyage": "(//*[@class='custom-options'])[5]",
            "order_cancel_metrics_list": "//*[@id='orderStatusReport']/tbody/tr/td[4]",
            "cancellation_reason_metrics": "//*[contains(text(),'Cancellation Reasons Metrics')]"
        })

    def no_records_found(self):
        """
        Check for no records found message
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_records_found, locator_type="xpath")

    def verif_elements_on_sales_and_reports(self):
        """
        verify elements on reports and metrics page
        :return:
        """
        self.webDriver.click(element=self.locators.sales_report, locator_type="id")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_details, locator_type="id"):
            raise Exception("current sailing voyage details are not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.apply, locator_type="id"):
            raise Exception("apply button is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.download_icon, locator_type="xpath"):
            raise Exception("download icon is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.meal_period_chk_box,
                                                           locator_type="xpath"):
            raise Exception("meal period check box icon is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_from_date, locator_type="id"):
            raise Exception("filter from day is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_from_to_date,
                                                           locator_type="id"):
            raise Exception("filter from to day is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.from_time, locator_type="id"):
            raise Exception("from time filter is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.to_time, locator_type="id"):
            raise Exception("to time filter is not showing up in sales reports page")

    def verify_elements_on_order_status_report(self):
        """
        To verify elements on order status report page
        :return:
        """
        self.webDriver.click(element=self.locators.order_status, locator_type="id")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.voyage_details, locator_type="id"):
            raise Exception("current sailing voyage details are not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.apply, locator_type="id"):
            raise Exception("apply button is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.download_icon, locator_type="xpath"):
            raise Exception("download icon is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.meal_period_chk_box,
                                                           locator_type="xpath"):
            raise Exception("meal period check box icon is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_from_date, locator_type="id"):
            raise Exception("filter from day is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_from_to_date,
                                                           locator_type="id"):
            raise Exception("filter from to day is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter_from_order_status,
                                                           locator_type="id"):
            raise Exception("filter from order status is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.from_time, locator_type="id"):
            raise Exception("from time filter is not showing up in sales reports page")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.to_time, locator_type="id"):
            raise Exception("to time filter is not showing up in sales reports page")

    def click_download(self):
        """
        To click on download option
        :return:
        """
        self.webDriver.click(element=self.locators.download_icon, locator_type="xpath")

    def click_sales_pdf(self):
        """
        To click pdf option
        :return:
        """
        self.webDriver.click(element=self.locators.download_pdf, locator_type="xpath")
        self.webDriver.click(element=self.locators.downloading_popup, locator_type="xpath")
        window = self.webDriver.get_current_window()
        self.webDriver.switch_to_main_tab(window)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.allure_attach_jpeg('after_download_pdf_click')

    def click_order_status_pdf(self):
        """
        To click pdf option
        :return:
        """
        self.webDriver.click(element=self.locators.download_order_status_pdf, locator_type="xpath")
        self.webDriver.click(element=self.locators.downloading_popup, locator_type="xpath")
        window = self.webDriver.get_current_window()
        self.webDriver.switch_to_main_tab(window)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.allure_attach_jpeg('after_download_pdf_click')

    def verify_pdf(self, file_name):
        """
        Verify report exported as PDF
        :param file_name:
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

    def click_sales_excel(self):
        """
        To click excel option
        :return:
        """
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.download_excel, locator_type="xpath")
        self.webDriver.click(element=self.locators.downloading_popup, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        self.webDriver.allure_attach_jpeg('after_export_click')

    def click_order_status_excel(self):
        """
        To click excel option
        :return:
        """
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.download_order_status_excel, locator_type="xpath")
        self.webDriver.click(element=self.locators.downloading_popup, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
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

    def click_order_status_tab(self):
        """
        To click on order status tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_status, locator_type="id")

    def click_sales_status_tab(self):
        """
        To click on order status tab
        :return:
        """
        self.webDriver.click(element=self.locators.sales_report, locator_type="id")

    def is_no_meal_period_currently_displayed(self):
        """
        To check for meal period checkbox is enabled or not
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.no_meal_period_currently,
                                                           locator_type="xpath")

    def filter_sales_and_order_with_current_meal_period(self):
        """
        To filter sales report with current meal period
        :return:
        """
        if self.is_no_meal_period_currently_displayed() or self.no_records_found():
            pytest.skip(msg="No records found to filer with current meal period")
        self.webDriver.click(element=self.locators.current_meal_period, locator_type="xpath")
        self.webDriver.click(element=self.locators.apply, locator_type="id")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        order_list = self.webDriver.get_elements(element=self.locators.order_list, locator_type="xpath")
        assert len(order_list) > 0, "Failed to filter for current meal period orders"

    def verify_custom_sales_report_filter(self):
        """
        To verify custom sales report filter
        :return:
        """
        from_dates = self.webDriver.get_elements(element=self.locators.from_day_filter_list, locator_type="xpath")
        assert len(from_dates) > 1, 'From date filter does not contains the dates list'
        to_dates = self.webDriver.get_elements(element=self.locators.to_date_filter_list, locator_type="xpath")
        assert len(to_dates) > 1, "To date filter does not contains the dates list"
        from_time = self.webDriver.is_element_enabled(element=self.locators.from_time, locator_type="id")
        assert from_time, "From time frame is not displayed on screen"
        to_time = self.webDriver.is_element_enabled(element=self.locators.to_time, locator_type="id")
        assert to_time, "To time frame is not displayed on screen"
        apply_button = self.webDriver.is_element_enabled(element=self.locators.apply, locator_type="id")
        assert apply_button, "Apply button not enabled to apply custom dropdown"

    def verify_orders_custom_report_filter(self):
        """
        To verify orders custom report filter
        :return:
        """
        from_dates = self.webDriver.get_elements(element=self.locators.from_day_filter_list, locator_type="xpath")
        assert len(from_dates) > 1, 'From date filter does not contains the dates list'
        to_dates = self.webDriver.get_elements(element=self.locators.to_date_filter_list, locator_type="xpath")
        assert len(to_dates) > 1, "To date filter does not contains the dates list"
        from_time = self.webDriver.is_element_enabled(element=self.locators.from_time, locator_type="id")
        assert from_time, "From time frame is not displayed on screen"
        to_time = self.webDriver.is_element_enabled(element=self.locators.to_time, locator_type="id")
        assert to_time, "To time frame is not displayed on screen"
        apply_button = self.webDriver.is_element_enabled(element=self.locators.apply, locator_type="id")
        assert apply_button, "Apply button not enabled to apply custom dropdown"
        order_status = self.webDriver.get_elements(element=self.locators.order_status_list, locator_type="xpath")
        assert len(order_status) > 0, "Order status list is not showing up"

    def filter_sales_and_orders_by_voyage(self):
        """
        Filter by voyages
        :return:
        """
        self.webDriver.click(element=self.locators.voyage_update_icon, locator_type="id")
        self.webDriver.click(element=self.locators.voyage_drop_down, locator_type="id")
        self.webDriver.click(element=self.locators.future_voyage, locator_type="xpath")
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=60)
        if self.is_no_meal_period_currently_displayed() or self.no_records_found():
            logger.info("no records found to filer with future voyages")

    def verify_cancellation_status_report(self):
        """
        This is to verify order cancellation report bar graph in reports and metrics
        :return:
        """
        self.webDriver.click(element=self.locators.order_status, locator_type="id")
        order_status = self.no_records_found()
        if not order_status:
            status = self.webDriver.get_elements(element=self.locators.order_cancel_metrics_list, locator_type="xpath")
            if status == "Canceled":
                bar_graph_message = self.webDriver.get_text(element=self.locators.cancellation_reason_metrics,
                                                            locator_type="xpath")
                assert bar_graph_message == "Today's Cancellation Reasons Metrics", "bar graph is not showing for " \
                                                                                    "cancelled orders "
