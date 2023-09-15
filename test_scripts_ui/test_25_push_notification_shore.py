__author__ = 'aatir.fayyaz'

import pytest
from ui_pages.push_notification.shore_side.apihit import Apihit
from ui_pages.push_notification.shore_side.new_notification import Notification
from ui_pages.push_notification.shore_side.template import Template
from virgin_utils import *
from ui_pages.push_notification.shore_side.login import PushNotificationLogin
from ui_pages.push_notification.shore_side.dashboard import PushNotificationDashboard
from ui_pages.push_notification.shore_side.distribution_list import DistributionList
from ui_pages.push_notification.shore_side.schedule_notification import ScheduleNotifications


@pytest.mark.PUSH_NOTIFICATION_SHORE_UI
@pytest.mark.run(order=25)
class TestPushNotificationShore:
    """
    Test Suite to test Push Notification Shore Side
    """

    @pytestrail.case([72524206, 72597293])
    def test_01_launch_website_and_login(self, web_driver, page, config, rest_shore, test_data, creds):
        """
        Test cases to Launch the push notification website and login with valid credentials
        :param test_data:
        :param rest_shore:
        :param web_driver:
        :param page:
        :param config:
        :return:
        """
        try:
            setattr(page, 'login', PushNotificationLogin(web_driver))
            setattr(page, 'dashboard', PushNotificationDashboard(web_driver))
            setattr(page, 'distribution', DistributionList(web_driver))
            setattr(page, 'notification', Notification(web_driver, test_data))
            setattr(page, 'template', Template(web_driver))
            setattr(page, 'schedule', ScheduleNotifications(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_shore, test_data, creds))
            page.apihit.get_token(side='shore')
            page.apihit.get_voyage_details()
            web_driver.open_website(url=urljoin(config.shore.url, "/notificationManagement/login"))
            page.login.verification_of_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            page.login.login_into_push_notification(username=creds.verticalqa.username,
                                                    password=creds.verticalqa.password)
            if not page.login.ship_selection('Scarlet Lady'):
                raise Exception("Ship Selection page is not displayed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("login_error")
            raise Exception(exp)

    @pytestrail.case(72524207)
    def test_02_create_new_distribution_list(self, web_driver, test_data, page):
        """
        Test cases to verify new distribution list
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Distribution Lists')
            page.distribution.verify_header()
            page.distribution.create_new_distribution_list(test_data)
            if not page.distribution.verify_created_distribution_list(test_data):
                raise Exception("Distribution list not created")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("create_distribution_list_error")
            raise Exception(exp)

    @pytestrail.case(72524202)
    def test_03_free_form_notification_for_sailor_schedule_now(self, web_driver, page, config, test_data):
        """
        Test cases to create notification for sailor in free form and schedule for now
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            total_cabin_count = page.notification.create_new_free_form_notification(config, test_data, 'sailor', 'now')
            page.notification.click_save_button('now')
            count_verification_status = page.dashboard.get_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                if not page.notification.verify_created_notification(test_data['TitleText']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_free_form_now_error")
            raise Exception(exp)

    @pytestrail.case(72524217)
    def test_04_search_notification_by_keyword(self, web_driver, page, test_data):
        """
        Test cases to search notification by keyword
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.verify_message(test_data) == 0:
                raise Exception("No notification is displaying")
            elif not page.notification.verify_message(test_data):
                raise Exception("Notification message is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("search_notification_error")
            raise Exception(exp)

    @pytestrail.case(72524211)
    def test_05_update_and_send_exist_notification(self, web_driver, page, test_data):
        """
        Test cases to update and send exist notification
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.notification.clean_search_bar()
            if not page.notification.verify_created_notification(test_data['TitleText']):
                raise Exception("Notification title is not displaying on dashboard")
            else:
                page.notification.update_and_save()
                page.notification.update_message(test_data)
                if not page.notification.verify_message(test_data):
                    raise Exception("Notification message has not updated")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("update_notification_error")
            raise Exception(exp)

    @pytestrail.case(72524208)
    def test_06_update_and_verify_recipient_list(self, web_driver, page, test_data):
        """
        Test cases to update verify the recipient list in existing notification
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.notification.clean_search_bar()
            if not page.notification.verify_created_notification(test_data['TitleText']):
                raise Exception("Notification title is not displaying on dashboard")
            else:
                old_notification_count = page.dashboard.get_dashboard_count()
                page.notification.update_and_save()
                page.notification.update_recipient_list(test_data)
                count_verification_status = page.dashboard.get_notification_count(old_notification_count)
                if not count_verification_status:
                    raise Exception("Failed to update notification")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("update_recipient_list_error")
            raise Exception(exp)

    @pytestrail.case(72524216)
    def test_07_delete_notification_from_dashboard(self, web_driver, page):
        """
        Test cases to delete notification for sailor
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.notification.delete_notification()
            count_verification_status = page.dashboard.get_notification_count_after_deleting(old_notification_count)
            if not count_verification_status:
                raise Exception("notification not getting deleted")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_notification_error")
            raise Exception(exp)

    @pytestrail.case([72524218, 73191259])
    def test_08_free_form_notification_for_sailor_schedule_recurring(self, web_driver, page, test_data, config):
        """
        To create notification for sailor in free form and schedule for recurring
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('recurring'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, 'sailor', 'recurring')
            page.notification.click_save_button('recurring')
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                    raise Exception("Notification title is not displaying on Scheduled Notifications")
            page.schedule.verify_notification_card(test_data)
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_schedule_recurring_error")
            raise Exception(exp)

    @pytestrail.case(72524212)
    def test_09_free_form_notification_for_distribution_list_schedule_now(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for distribution list in free form and schedule for now
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            total_cabin_count = page.notification.create_new_free_form_notification(config, test_data,
                                                                                    test_data['distribution_list_name'],
                                                                                    'now')
            page.notification.click_save_button('now')
            count_verification_status = page.dashboard.get_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.notification.clean_search_bar()
                if not page.notification.verify_created_notification(test_data['TitleText']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_free_form_now_error")
            raise Exception(exp)

    @pytestrail.case(72524205)
    def test_10_create_template(self, web_driver, page, test_data):
        """
        Test cases to create template
        :param test_data:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Templates')
            page.template.click_new_template_button()
            page.template.create_template(test_data)
            if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("create_template_error")
            raise Exception(exp)

    @pytestrail.case(72524203)
    def test_11_create_notification_by_template_for_sailor_schedule_now(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for sailor in template and schedule for now
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            total_cabin_count = page.notification.create_new_template_notification(config, 'sailor')
            count_verification_status = page.dashboard.get_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.notification.clean_search_bar()
                if not page.notification.verify_created_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_template_now_error")
            raise Exception(exp)

    @pytestrail.case(72531469)
    def test_12_create_notification_by_template_for_sailor_schedule_recurring(self, web_driver, page, test_data, config):
        """
        To create notification for sailor in template and schedule for recurring
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('recurring'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.schedule_recurring(test_data)
            page.notification.create_template_notification_schedule_selected_voyage('sailor', None)
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_template_recurring_error")
            raise Exception(exp)

    @pytestrail.case(72524221)
    def test_13_create_notification_by_template_for_dist_list_schedule_now(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for distribution list in template and schedule for now
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            total_cabin_count = page.notification.create_new_template_notification(config,
                                                                                   test_data['distribution_list_name'])
            count_verification_status = page.dashboard.get_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.notification.clean_search_bar()
                if not page.notification.verify_created_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_template_now_error")
            raise Exception(exp)

    @pytestrail.case(72524220)
    def test_14_create_notification_by_template_for_sailor_schedule_voyage(self, web_driver, page, test_data, config):
        """
        To create notification for sailor in template and schedule for selected voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('selected voyage'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_selected_voyage()
            page.notification.create_template_notification_schedule_selected_voyage('sailor', None)
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_template_voyage_error")
            raise Exception(exp)

    @pytestrail.case(72531471)
    def test_15_create_notification_by_template_for_dist_list_schedule_recurring(self, web_driver, page, test_data, config):
        """
        To create notification for distribution list in template and schedule for recurring
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('recurring'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            total_cabin_count = page.notification.create_new_template_notification(config,
                                                                                   test_data['distribution_list_name'])
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.notification.clean_search_bar()
                if not page.notification.verify_created_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_template_recurring_error")
            raise Exception(exp)

    @pytestrail.case(72524222)
    def test_16_create_notification_by_template_for_dist_list_schedule_voyage(self, web_driver, page, test_data,
                                                                              config):
        """
        To create notification for distribution list in template and schedule for selected voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('selected voyage'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_selected_voyage()
            page.notification.create_template_notification_schedule_selected_voyage(
                test_data['distribution_list_name'], None)
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                    web_driver.allure_attach_jpeg("title error")
                    raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_template_voyage_error")
            raise Exception(exp)

    @pytestrail.case(72524210)
    def test_17_free_form_notification_for_distribution_list_schedule_voyage(self, web_driver, page, test_data, config):
        """
        To create notification for distribution list in free form and schedule for selected voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('selected voyage'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, test_data['distribution_list_name'],
                                                                'selected_voyage')
            page.notification.click_save_button('selected_voyage')
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                    web_driver.allure_attach_jpeg("title error")
                    raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_free_form_voyage_error")
            raise Exception(exp)

    @pytestrail.case(75735734)
    def test_18_create_notification_by_template_for_sailor_for_now(self, config, web_driver, page, test_data):
        """
        To create notification for sailor in template and schedule for now
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            total_cabin_count = page.notification.select_and_save_recipients('sailor')
            count_verification_status = page.dashboard.get_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                if not page.notification.verify_created_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")
                else:
                    total_recipient_count = page.notification.view_list()
                    if total_cabin_count != total_recipient_count:
                        raise Exception("cabin count is not matching")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_free_form_now_error")
            raise Exception(exp)

    @pytestrail.case(72524204)
    def test_19_save_notification_as_draft(self, web_driver, page, config, test_data):
        """
        Test cases to save notification as draft
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, 'sailor', 'now')
            page.notification.save_as_draft()
            page.dashboard.click_on_tabs_from_dashboard("My Drafts")
            if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                web_driver.allure_attach_jpeg("draft dashboard error")
                raise Exception("Notification title is not displaying on draft page")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("save_as_draft_error")
            raise Exception(exp)

    @pytestrail.case(72526286)
    def test_20_saved_draft_in_ship(self, web_driver, page, config, test_data):
        """
        To verify that saved draft notifications should not display in the different ship
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.change_ship('Resilient Lady')
            page.dashboard.click_on_tabs_from_dashboard('My Drafts')
            if page.dashboard.verify_draft_list():
                if not page.notification.verify_draft_ship(test_data['TitleText']):
                    web_driver.allure_attach_jpeg("different ship draft error")
                    raise Exception("Notification title is not displaying on draft page")
            page.dashboard.change_ship('Valiant Lady')
            page.dashboard.click_on_tabs_from_dashboard('My Drafts')
            if page.dashboard.verify_draft_list():
                if not page.notification.verify_draft_ship(test_data['TitleText']):
                    web_driver.allure_attach_jpeg("different ship draft error")
                    raise Exception("Notification title is not displaying on draft page")
            page.dashboard.change_ship('Scarlet Lady')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("saved_draft_different_ship_error")
            raise Exception(exp)

    @pytestrail.case([72524201, 73196782])
    def test_21_edit_send_saved_draft(self, web_driver, page, config, test_data):
        """
        To verify user should be able to edit and send the saved draft
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard("My Drafts")
            if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                web_driver.allure_attach_jpeg("draft dashboard error")
                raise Exception("Notification title is not displaying on draft page")
            else:
                page.notification.update_and_save()
                page.notification.update_message(test_data)
                page.dashboard.click_on_tabs_from_dashboard('Dashboard')
                if not page.notification.verify_message(test_data):
                    raise Exception("Draft has not updated")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("edit_draft_error")
            raise Exception(exp)

    @pytestrail.case(75063215)
    def test_22_free_form_notification_for_dist_list_schedule_recurring(self, web_driver, page, test_data, config):
        """
        To create notification for distribution list in free form and schedule for recurring
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('recurring'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, test_data['distribution_list_name'],
                                                                'recurring')
            page.notification.click_save_button('recurring')
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                    web_driver.allure_attach_jpeg("title error")
                    raise Exception("Notification title is not displaying on dashboard")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dist_list_free_form_recurring_error")
            raise Exception(exp)

    @pytestrail.case(72524214)
    def test_23_download_notification_pdf(self, web_driver, page):
        """
        Test cases to download pdf
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.dashboard.click_download()
            page.dashboard.click_pdf()
            today = date.today()
            today_date = today.strftime("%m_%d_%Y")
            page.dashboard.verify_pdf(f"{'VV_SentNotification_'}{today_date}")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("pdf_download_error")
            raise Exception(exp)

    @pytestrail.case(72524215)
    def test_24_download_notification_excel(self, web_driver, page):
        """
        Test cases to download excel
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.dashboard.click_download()
            page.dashboard.click_excel()
            today = date.today()
            today_date = today.strftime("%m_%d_%Y")
            page.dashboard.verify_excel(f"{'VV_SentNotification_'}{today_date}")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("excel_download_error")
            raise Exception(exp)

    @pytestrail.case(75341980)
    def test_25_delete_used_template(self, web_driver, page, test_data):
        """
        Test cases to delete template
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Templates')
            page.notification.verify_created_scheduled_notification(test_data['templateTitle'])
            page.template.delete_used_template_and_verify()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_used_template_error")
            raise Exception(exp)

    @pytestrail.case([72524225, 75341981])
    def test_26_delete_template(self, web_driver, page, test_data):
        """
        Test cases to delete template
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Templates')
            page.template.click_new_template_button()
            page.template.create_template(test_data)
            page.notification.verify_created_scheduled_notification(test_data['templateTitle'])
            page.notification.delete_template_and_verify()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_template_error")
            raise Exception(exp)

    @pytestrail.case(75732696)
    def test_27_delete_distribution_list(self, web_driver, page, test_data):
        """
        Test cases to delete distribution list
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Distribution Lists')
            page.notification.verify_created_scheduled_notification(test_data['distribution_list_name'])
            page.distribution.delete_dist_list_and_verify()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("delete_distribution_list_error")
            raise Exception(exp)

    @pytestrail.case(72526289)
    def test_28_log_off_refreshing(self, web_driver, page, test_data):
        """
        To verify that user should not log off from the application by refreshing any page
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.login.verify_refresh_page('Scarlet Lady')
            page.dashboard.click_on_tabs_from_dashboard('Scheduled Notifications')
            page.login.verify_refresh_page('Scarlet Lady')
            page.dashboard.click_on_tabs_from_dashboard('My Drafts')
            page.login.verify_refresh_page('Scarlet Lady')
            page.dashboard.click_on_tabs_from_dashboard('Templates')
            page.login.verify_refresh_page('Scarlet Lady')
            page.dashboard.click_on_tabs_from_dashboard('Distribution Lists')
            page.login.verify_refresh_page('Scarlet Lady')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("log_off_refreshing_error")
            raise Exception(exp)

    @pytestrail.case(72524224)
    def test_29_free_form_notification_sailor_schedule_voyage(self, web_driver, page, test_data, config):
        """
        To create notification for sailor in free form and schedule for selected voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('selected voyage'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, 'sailor', 'selected_voyage')
            page.notification.click_save_button('selected_voyage')
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                    raise Exception("Notification title is not displaying on Scheduled Notifications")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor_free_form_voyage_error")
            raise Exception(exp)

    @pytestrail.case(74897600)
    def test_30_send_now(self, web_driver, page, test_data):
        """
        To verify that user is able to send scheduled notifications by clicking on "Send Now"
        button before completing the scheduled time
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.notification.check_embark_date('selected voyage'):
                pytest.skip('Date should not be after maximal date')
            page.dashboard.click_on_tabs_from_dashboard('Scheduled Notifications')
            page.notification.verify_created_scheduled_notification(test_data['TitleText'])
            page.schedule.send_now('SEND NOW')
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.notification.verify_created_notification(test_data['TitleText'])
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("send_now_notification_error")
            raise Exception(exp)

    @pytestrail.case([73806910, 72529225])
    def test_31_boarding_slots(self, web_driver, page, test_data, config):
        """
        To verify that "Boarding time" dropdown is not empty while creating notification
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.verify_boarding_slots('sailor')
            page.login.verify_refresh_page('Scarlet Lady')
            page.dashboard.click_on_tabs_from_dashboard('Distribution Lists')
            page.distribution.verify_header()
            page.distribution.verify_boarding_slots('sailor')
            page.login.verify_refresh_page('Scarlet Lady')
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("boarding_slots_error")
            raise Exception(exp)
