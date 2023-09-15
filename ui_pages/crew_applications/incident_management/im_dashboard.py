__author__ = 'aatir.fayyaz'

from virgin_utils import *


class IncidentManagement(General):
    """
    Page class for Incident Management page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "create_incident_button": "//*[@class='android.widget.Button'][@index='0']",
            "create_incident_header": "//*[@class='android.widget.TextView'][@text='Create Incident']",
            "show_all_incidents": "//*[@class='android.widget.Button'][@text='Show All Incidents']",
            "filter_icon": "//*[@class='android.widget.Image'][@text='logo'][@index='0']",
            "search_incident_button": "//*[@class='android.widget.TextView'][@text='Dashboard']/following-sibling::android.widget.Button",
            "search_for_incident": "//*[@class='android.widget.EditText']",
            "search_result": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "search_cabin": "//*[@class='android.view.View'][contains(@text,'Cabin %s')]",
            "search_close": "//*[@class='android.widget.Button'][@index='2']",
            "back_to_im_dashboard": "//*[@class='android.widget.Button'][@text='menu']",
            "un_assign_list": "//*[contains(@text,'Incidents Unassigned')]/following-sibling::android.view.View",
            "assign_list": "//*[contains(@text,'Incidents Assigned')]/following-sibling::android.view.View",
            "assigned_incident": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "assigned_counts": "//*[@class='android.widget.TextView'][contains(@text,'Incidents Assigned')]",
            "unassigned_counts": "//*[@class='android.widget.TextView'][contains(@text,'Unassigned')]",
            "total_counts": "//*[@class='android.widget.TextView'][contains(@text,'/')]",
            "search_vip": "//*[@class='android.widget.Image'][contains(@text,'VIP')]",
            "incident_resolved": "//*[@class='android.widget.TextView'][contains(@text,'Incident Resolved')]",
            "incidents": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
            "im_header": "//*[@class='android.widget.TextView'][contains(@text,'%s')]",
        })

    def click_create_incident_button(self):
        """
        Function to click on create button
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.explicit_visibility_of_element(element=self.locators.create_incident_button,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.create_incident_button, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.create_incident_header,
                                                      locator_type='xpath', time_out=120)

    def open_filter(self):
        """
        Function open all Incident
        :return:
        """
        self.webDriver.wait_for(5)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.show_all_incidents,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(300, 200, 300, 1200)
            self.webDriver.scroll_mobile(300, 1200, 300, 200)
        self.webDriver.click(element=self.locators.show_all_incidents, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.explicit_visibility_of_element(element=self.locators.filter_icon,
                                                      locator_type='xpath', time_out=240)
        self.webDriver.click(element=self.locators.filter_icon, locator_type='xpath')

    def search_by_cabin(self, value):
        """
        Function to search the Incident with cabin
        :param value:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.im_header % 'Dashboard',
                                                      locator_type='xpath', time_out=240)
        self.webDriver.scroll_mobile(360, 1000, 360, 800)
        self.webDriver.scroll_mobile(360, 800, 360, 1200)
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_incident_button,
                                                      locator_type='xpath', time_out=60)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_incident_button,
                                                           locator_type='xpath'):
            self.webDriver.scroll_mobile(300, 1200, 300, 200)
            self.webDriver.scroll_mobile(300, 200, 300, 1200)
        self.webDriver.click(element=self.locators.search_incident_button, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.search_for_incident, locator_type='xpath', text=value)
        self.webDriver.submit()
        self.webDriver.scroll_mobile(360, 1200, 360, 800)
        self.webDriver.scroll_mobile(360, 800, 360, 1200)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_result % f'Cabin {value}',
                                                           locator_type='xpath'):
            raise Exception(f'Not able to search Incident using {value}')

    def search_by_name(self, value):
        """
        Function to search the Incident
        :param value:
        :return:
        """
        self.webDriver.clear_text(element=self.locators.search_for_incident, locator_type='xpath', action_type='clear')
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.search_for_incident, locator_type='xpath', text=value)
        self.webDriver.submit()
        self.webDriver.scroll_mobile(360, 1200, 360, 800)
        self.webDriver.scroll_mobile(360, 800, 360, 1200)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_result % value,
                                                           locator_type='xpath'):
            raise Exception(f'Not able to search Incident using {value}')

    def click_search_close_icon(self):
        """
        Function to close the search result page
        :return:
        """
        self.webDriver.click(element=self.locators.search_close, locator_type='xpath')
        self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
        self.webDriver.wait_for(5)

    def all_incidents_count(self, test_data):
        """
        To get all incident count
        :param test_data:
        :return:
        """
        self.webDriver.wait_for(5)
        test_data['all_incidents'] = []
        self.webDriver.scroll_mobile(360, 1200, 360, 800)
        self.webDriver.click(element=self.locators.un_assign_list, locator_type='xpath')
        assigned_counts = self.webDriver.get_text(element=self.locators.assigned_counts,
                                                  locator_type="xpath").split('(')[1]
        unassigned_counts = self.webDriver.get_text(element=self.locators.unassigned_counts,
                                                    locator_type="xpath").split('(')[1]
        test_data['all_incidents'] = int(assigned_counts[:-1]) + int(unassigned_counts[:-1])

    def verify_total_count(self, test_data):
        """
        To verify the progress bar total count
        :param test_data:
        :return:
        """
        progress_total_count = self.webDriver.get_text(element=self.locators.total_counts,
                                                       locator_type="xpath").split('/')[1]
        progress_closed_count = self.webDriver.get_text(element=self.locators.total_counts,
                                                        locator_type="xpath").split('/')[0]
        assert int(progress_total_count) == test_data['all_incidents'] + int(progress_closed_count),\
            'Total Counts not matched'

    def check_availability_of_incident(self, value):
        """
        Function to check the incident available in Assigned tab or not
        :param value:
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.assign_list,
                                                      locator_type='xpath', time_out=240)
        self.webDriver.click(element=self.locators.assign_list, locator_type='xpath')
        self.webDriver.wait_for(5)
        for i in range(20):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.assigned_incident % f'Cabin {value}',
                                                               locator_type='xpath'):
                self.webDriver.scroll_mobile(360, 1200, 360, 250)
                continue
            self.webDriver.click(element=self.locators.assigned_incident % f'Cabin {value}', locator_type='xpath')
            logger.info('Created Incident is present in Assigned Incidents List')
            break
        else:
            raise Exception('Created Incident not found in Assigned Incidents List')

    def verify_reopen_incident(self, value):
        """
        To verify crew is able to Re-open the closed incident
        :param value:
        :return:
        """
        self.webDriver.wait_for(3)
        self.webDriver.scroll_mobile(300, 1200, 300, 800)
        self.webDriver.scroll_mobile(300, 800, 300, 1200)
        for i in range(20):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.incidents % f'Cabin {value}',
                                                               locator_type='xpath'):
                self.webDriver.scroll_mobile(300, 1200, 300, 250)
                continue
            logger.info('Incident Reopened Successfully')
            break
        else:
            raise Exception('Incident not Reopened Successfully')

    def check_vip_incidents(self):
        """
        To check VIP incidents are present
        :return:
        """
        for j in range(20):
            if not self.webDriver.is_element_display_on_screen(element=self.locators.show_all_incidents,
                                                               locator_type='xpath'):
                self.webDriver.scroll_mobile(300, 200, 300, 1200)
                continue
            self.webDriver.click(element=self.locators.show_all_incidents, locator_type='xpath')
            self.webDriver.wait_for(5)
            break
        for i in range(6):
            if self.webDriver.is_element_display_on_screen(element=self.locators.search_vip, locator_type='xpath'):
                logger.info('VIP incidents available')
                self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
                self.webDriver.wait_for(5)
                self.webDriver.explicit_visibility_of_element(element=self.locators.im_header % 'Dashboard',
                                                              locator_type='xpath', time_out=240)
                break
            else:
                self.webDriver.scroll_mobile(300, 1200, 300, 150)
                continue
        else:
            self.webDriver.click(element=self.locators.back_to_im_dashboard, locator_type='xpath')
            self.webDriver.wait_for(5)
            return False

    def verify_vip_incidents_on_top(self):
        """
        To verify that VIP issues are always coming on top
        :return:
        """
        self.webDriver.wait_for(5)
        self.webDriver.scroll_mobile(300, 1200, 300, 800)
        self.webDriver.scroll_mobile(300, 800, 300, 1200)
        self.webDriver.explicit_visibility_of_element(element=self.locators.show_all_incidents,
                                                      locator_type='xpath', time_out=240)
        self.webDriver.click(element=self.locators.show_all_incidents, locator_type='xpath')
        self.webDriver.wait_for(3)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.search_vip, locator_type='xpath'):
            raise Exception('No VIP issues are on top')

