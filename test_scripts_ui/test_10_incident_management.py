__author__ = 'prahlad.sharma'

import pytest

from ui_pages.ars_admin.apihit.apihit import Apihit
from ui_pages.incident_management.create_incident import CreateIncident
from ui_pages.incident_management.dashboard import Dashboard
from ui_pages.incident_management.incident_details import IncidentDetails
from ui_pages.incident_management.incident_list import IncidentList
from ui_pages.incident_management.login import Login
from virgin_utils import *


@pytest.mark.INCIDENT_MANAGEMENT_UI
@pytest.mark.run(order=10)
class TestIncidentManagement:
    """
    Test ui suite to run Incident Management
    """

    @pytestrail.case('46391342')
    def test_01_login_incident_management(self, config, page, web_driver, test_data, rest_shore, creds):
        """
        Verify Incident Management login functionality
        :param rest_shore:
        :param config:
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data, creds))
            setattr(page, 'login', Login(web_driver))
            setattr(page, 'dashboard', Dashboard(web_driver, test_data))
            setattr(page, 'incident', CreateIncident(web_driver, test_data))
            setattr(page, 'details', IncidentDetails(web_driver, test_data))
            setattr(page, 'list', IncidentList(web_driver, test_data))
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/incident-management-system"))
            page.apihit.get_ship_reservation_details()
            if page.login.verify_login_page():
                logger.debug("Login page loaded successfully")
            else:
                web_driver.allure_attach_jpeg('login_page_not_loaded')
                raise Exception("Failed to load Login page successfully")
            page.login.login_into_incident_management_web_app(user_name=creds.incident.username, password=creds.incident.password)
            page.dashboard.verify_dashboard_page()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_login_page")
            raise Exception(exp)

    @pytestrail.case('24390027')
    def test_02_verify_sla_update_as_per_priority(self, page, web_driver, test_data):
        """
        Verify SLA is updated as per selected Priority
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            if test_data["sailor_data"]:
                logger.info(f"Incident created for cabin Number : {test_data['searched_sailor_stateroom']}")
                page.dashboard.click_create_incident_button()
                page.incident.fill_incident(test_data['searched_sailor_stateroom'])
                page.incident.check_sla_value()
            else:
                pytest.skip("CheckedIn and Onboarded guest not available in DB")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_sla_update")
            raise Exception(exp)

    @pytestrail.case('41551057')
    def test_03_verify_admin_can_adjust_priority_severity(self, page, web_driver):
        """
        Verify admin can update the priority and Severity
        :param page:
        :param web_driver:
        """
        try:
            page.incident.severity_slider()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_pri_sev")
            raise Exception(exp)

    @pytestrail.case('24389656')
    def test_04_create_incident(self, page, web_driver):
        """
        Verify Create Incident flow
        :param page:
        :param web_driver:
        """
        try:
            page.incident.click_save()
            page.details.verify_incident_details_page()
            page.details.match_AOMS()
            page.details.match_cabin_number()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_incident_creation")
            raise Exception(exp)

    @pytestrail.case('24389657')
    def test_05_verify_created_incident_in_assigned_tab(self, page, web_driver):
        """
        Verify Created Incident in Assigned tab
        :param page:
        :param web_driver:
        """
        try:
            page.details.go_back()
            active_tab_name = page.dashboard.get_active_tab_value()
            if "UNASSIGNED" in active_tab_name:
                page.dashboard.open_assigned_tab()
                page.dashboard.sort_by(" Sort by Creation Date")
            page.list.verify_incident(False)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_assign_tab")
            raise Exception(exp)

    @pytestrail.case('24390026')
    def test_06_update_the_priority_of_incident(self, page, web_driver, test_data):
        """
        Verify Crew can Update the priority of Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            logger.info(test_data["AIMS#"])
            page.list.verify_incident(True)
            page.details.click_edit_icon()
            page.incident.priority_slider()
            page.incident.click_update()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_incident_priority_update")
            raise Exception(exp)

    @pytestrail.case('41551058')
    def test_07_reassign_crew(self, page, web_driver):
        """
        Re assign incident to crew
        :param page:
        :param web_driver:
        """
        try:
            page.details.go_back()
            page.dashboard.open_tab("UNASSIGNED")
            if page.dashboard.check_availability_of_incident():
                page.list.open_incident_details_page()
                page.details.click_reassign_button()
                if page.details.reassign_incident():
                    assert page.details.get_incident_status() == "Assigned", "Reassignment not done for an Incident"
                else:
                    logger.info("No crew in assign to dropdown")
            else:
                web_driver.allure_attach_jpeg("blank_unassigned")
                pytest.skip("Data is not available in Unassigned tab")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_reassignment")
            raise Exception(exp)

    @pytestrail.case('41551059')
    def test_08_search_incident(self, page, web_driver, test_data):
        """
        Search the Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            page.dashboard.search_incident(test_data['searched_sailor_stateroom'])
            page.dashboard.click_close_icon()
            page.dashboard.search_incident(test_data['searched_sailor_fn'])
            page.dashboard.click_close_icon()
            page.dashboard.search_incident(test_data['searched_sailor_ln'])
            page.dashboard.click_close_icon()
            page.dashboard.search_incident('david warner')
            page.dashboard.click_close_icon()
            page.details.go_back()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_search")
            raise Exception(exp)

    @pytestrail.case('41552332')
    def test_09_filter_incident(self, page, web_driver):
        """
        Filter the Incident
        :param page:
        :param web_driver:
        """
        try:
            if page.dashboard.check_availability_of_incident():
                page.dashboard.get_vir_value()
                page.list.open_incident_details_page()
                page.details.click_edit_icon()
                page.incident.select_incident_location()
                page.incident.set_highest_priority()
                page.incident.set_highest_severity()
                page.incident.click_update()
                page.details.go_back()
                page.dashboard.sort_by("Sort by Severity")
                page.list.open_incident_details_page()
                assert page.dashboard.verify_severity_on_details() == 1, "Incident sorting not display as per severity"
                page.details.go_back()
                page.dashboard.sort_by("Sort by Priority")
                page.list.open_incident_details_page()
                assert page.dashboard.verify_priority_on_details() == 1, "Incident sorting not display as per priority"
                page.details.go_back()
            else:
                pytest.skip(msg='No Unassigned incidents to filter')
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_filter")
            raise Exception(exp)

    @pytestrail.case('46374265')
    def test_10_close_incident(self, page, web_driver):
        """
        Close the Incident
        :param page:
        :param web_driver:
        :param test_data:
        """
        try:
            active_tab_name = page.dashboard.get_active_tab_value()
            if "UNASSIGNED" in active_tab_name:
                page.dashboard.open_assigned_tab()
            page.dashboard.sort_by(" Sort by Creation Date")
            page.list.verify_incident(True)
            page.details.close_incident()
            page.details.go_back()
            page.dashboard.open_tab("CLOSED")
            page.list.verify_incident(False)
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_close_incident")
            raise Exception(exp)

    @pytestrail.case('70511966')
    def test_11_resolved_and_total_count_match(self, page, web_driver):
        """
        To verify resolved and total count matching
        :param page:
        :param web_driver:
        """
        try:
            progress_bar_resolved_count = page.dashboard.get_progress_bar_resolved_count()
            incident_closed_count = page.dashboard.closed_count()
            assert progress_bar_resolved_count == incident_closed_count, "resolved count does not match"
            assert page.dashboard.get_progress_bar_total_count() == page.dashboard.all_incident_count(), "total incident count does not match"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("error_incident_count")
            raise Exception(exp)