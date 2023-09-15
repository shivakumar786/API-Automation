__author__ = 'aatir.fayyaz'

import pytest

from virgin_utils import *
from ui_pages.crew_applications.apihit.apihit import Apihit
from ui_pages.crew_applications.login.login import CrewAppLogin
from ui_pages.crew_applications.crew_framework.dashboard import CrewDashboard
from ui_pages.crew_applications.incident_management.im_dashboard import IncidentManagement
from ui_pages.crew_applications.incident_management.create_incident import CreateIncident
from ui_pages.crew_applications.incident_management.incident_details import IncidentDetails
from ui_pages.crew_applications.incident_management.filter import Filters


@pytest.mark.CREW_INCIDENT_MANAGEMENT
@pytest.mark.run(order=20)
class TestCrewIncidentManagement:
    """
    Test Suite to test Incident Management Apk
    """
    @pytestrail.case(46391342)
    def test_01_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Launch the Crew app and login into Incident Management Application
        :param web_driver:
        :param page:
        :param config:
        :param rest_ship:
        :param test_data:
        :param creds:
        :return:
        """
        try:
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            setattr(page, 'login', CrewAppLogin(web_driver))
            setattr(page, 'dashboard', CrewDashboard(web_driver))
            setattr(page, 'im_dashboard', IncidentManagement(web_driver))
            setattr(page, 'create_incident', CreateIncident(web_driver))
            setattr(page, 'incident_details', IncidentDetails(web_driver))
            setattr(page, 'filter', Filters(web_driver))
            page.apihit.get_ship_reservation_details()
            page.login.allow_call_popup()
            if page.login.verify_select_ship():
                web_driver.allure_attach_jpeg("availability_of_virgin_select_ship_page")
            else:
                raise Exception("Invalid select ship page")
            page.login.sign_in(username=creds.incident.username, password=creds.incident.password)
            if not page.login.verify_create_pin_page():
                web_driver.allure_attach_jpeg("login unsuccessful")
                raise Exception("Error in login")
            page.login.verify_crew_dashboard()
            page.dashboard.open_crew_app_module(module_name='INCIDENT MANAGEMENT', module_heading='Dashboard')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(62818543)
    def test_02_verify_mandatory_fields(self, page, web_driver):
        """
        Verify mandatory fields are star (*) marked
        :param page:
        :param web_driver:
        """
        try:
            page.im_dashboard.click_create_incident_button()
            page.create_incident.check_mandatory_fields()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_mandatory_fields")
            raise Exception(exp)

    @pytestrail.case(53037640)
    def test_03_verify_department_auto_display(self, page, web_driver, test_data):
        """
        Verify Department Auto displayed after choosing parent incident and incident category
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.create_incident.department_auto_display(test_data['searched_sailor_stateroom_1'], test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_department")
            raise Exception(exp)

    @pytestrail.case([57700704, 41551058])
    def test_04_assign_to_crew(self, page, web_driver, test_data):
        """
        To verify admin is able to assign incidents to crew members
        :param page:
        :param web_driver:
        """
        try:
            page.create_incident.verify_assign_to_crew('david warner')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_assign_to_crew")
            raise Exception(exp)

    @pytestrail.case(24390027)
    def test_05_verify_sla_update_as_per_priority(self, page, web_driver, test_data):
        """
        Verify SLA is updated as per selected Priority
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.create_incident.fill_incident(test_data)
            page.create_incident.set_lowest_sla()
            page.create_incident.set_priority(test_data)
            page.create_incident.check_sla_value(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sla_update")
            raise Exception(exp)

    @pytestrail.case(62819584)
    def test_06_verify_high_low_text(self, page, web_driver):
        """
        To verify priority and severity is showing high to low indication text
        :param page:
        :param web_driver:
        """
        try:
            page.create_incident.high_low_text()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_high_low_text")
            raise Exception(exp)

    @pytestrail.case(41551057)
    def test_07_verify_admin_can_adjust_priority_severity(self, page, web_driver, test_data):
        """
        Verify admin can update the priority and Severity while creating an incident
        :param page:
        :param web_driver:
        """
        try:
            page.create_incident.set_severity(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_adjust_priority_severity")
            raise Exception(exp)

    @pytestrail.case(50913571)
    def test_08_verify_crew_can_upload_photo(self, page, web_driver):
        """
        Verify crew can upload photo while creating an incident
        :param page:
        :param web_driver:
        """
        try:
            page.create_incident.upload_photo()
            page.create_incident.verify_upload_photo()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_upload_photo")
            raise Exception(exp)

    @pytestrail.case(24389656)
    def test_09_create_incident(self, page, web_driver, test_data):
        """
        Verify Create Incident flow
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.create_incident.click_create()
            page.incident_details.verify_priority_on_details(test_data['priority'])
            page.incident_details.verify_severity_on_details(test_data['severity'])
            page.incident_details.match_aims(test_data['AIMS'])
            page.incident_details.match_cabin_number(test_data['searched_sailor_stateroom_1'])
            page.incident_details.get_vir_value(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_incident_creation")
            raise Exception(exp)

    @pytestrail.case(52392723)
    def test_10_verify_sla(self, page, web_driver):
        """
        To verify SLA time should be same in incident details page after creating incident
        :param page:
        :param web_driver:
        """
        try:
            page.incident_details.verify_sla()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_verify_sla")
            raise Exception(exp)

    @pytestrail.case(70511966)
    def test_11_progress_bar_count(self, page, web_driver, test_data):
        """
        To verify progress bar count with closed and all incident count
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.im_dashboard.all_incidents_count(test_data)
            page.im_dashboard.verify_total_count(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_incident_count")
            raise Exception(exp)

    @pytestrail.case(24389657)
    def test_12_verify_created_incident_in_assigned_tab(self, page, web_driver, test_data):
        """
        Verify Created Incident in Assigned tab
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.im_dashboard.check_availability_of_incident(test_data['searched_sailor_stateroom_1'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_incident_in_assigned_tab")
            raise Exception(exp)

    @pytestrail.case(24390026)
    def test_13_update_the_priority_of_incident(self, page, web_driver, test_data):
        """
        Verify crew can Update the priority of Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.incident_details.open_3_dot_menu()
            page.incident_details.click_edit_icon()
            page.create_incident.set_priority(test_data)
            page.create_incident.click_update()
            page.incident_details.verify_priority_on_details(test_data['priority'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_incident_priority_update")
            raise Exception(exp)

    @pytestrail.case(46374265)
    def test_14_close_incident(self, page, web_driver, test_data):
        """
        Close the Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.incident_details.open_3_dot_menu()
            page.incident_details.close_incident()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_close_incident")
            raise Exception(exp)

    @pytestrail.case(60794190)
    def test_15_reopen_incident(self, page, web_driver, test_data):
        """
        Reopen the Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.incident_details.open_3_dot_menu()
            page.incident_details.reopen_closed_incident()
            page.im_dashboard.verify_reopen_incident(test_data['searched_sailor_stateroom_1'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_reopen_incident")
            raise Exception(exp)

    @pytestrail.case(41552653)
    def test_16_vip_incidents_at_top(self, page, web_driver):
        """
        To verify that VIP issues are always coming on top in the list at dashboard
        :param page:
        :param web_driver:
        """
        try:
            if page.im_dashboard.check_vip_incidents():
                page.im_dashboard.verify_vip_incidents_on_top()
            else:
                logger.info('No VIP incidents available')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_vip_at_top")
            raise Exception(exp)

    @pytestrail.case(41552332)
    def test_17_sort_incident(self, page, web_driver, test_data):
        """
        Sort Incidents
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.im_dashboard.open_filter()
            page.filter.sort_incident()
            page.filter.verify_sort_incident(test_data['searched_sailor_stateroom_1'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_sorting")
            raise Exception(exp)

    @pytestrail.case(41551059)
    def test_18_search_incident(self, page, web_driver, test_data):
        """
        Search the Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.im_dashboard.search_by_cabin(test_data['searched_sailor_stateroom_1'])
            page.im_dashboard.search_by_name(test_data['sailor'].split(' ')[0])
            page.im_dashboard.search_by_name(test_data['sailor'].split(' ')[1])
            page.im_dashboard.click_search_close_icon()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("error_search")
            raise Exception(exp)
