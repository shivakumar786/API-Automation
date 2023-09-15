from ui_pages.push_notification.ship_side.apihit import Apihit
from ui_pages.push_notification.ship_side.new_notification import Notification
from ui_pages.push_notification.ship_side.template import Template
from virgin_utils import *
from ui_pages.push_notification.ship_side.login import PushNotificationLogin
from ui_pages.push_notification.ship_side.dashboard import PushNotificationDashboard
from ui_pages.push_notification.ship_side.distribution_list import DistributionList


@pytest.mark.PUSH_NOTIFICATION_SHIP_UI
@pytest.mark.run(order=11)
class TestPushNotification:
    """
    Test Suite to test Push Notification
    """

    @pytestrail.case(26682462)
    def test_01_launch_website_and_login(self, web_driver, page, config, rest_ship, test_data, creds):
        """
        Test cases to Launch the push notification website and login with valid credentials

        :param test_data:
        :param rest_ship:
        :param web_driver:
        :param page:
        :param config:
        :return:
        """
        try:
            setattr(page, 'login', PushNotificationLogin(web_driver))
            setattr(page, 'dashboard', PushNotificationDashboard(web_driver))
            setattr(page, 'distribution', DistributionList(web_driver))
            setattr(page, 'notification', Notification(web_driver))
            setattr(page, 'template', Template(web_driver))
            setattr(page, 'apihit', Apihit(config, rest_ship, test_data, creds))
            page.apihit.get_token(side='ship')
            page.apihit.get_voyage_details()
            page.apihit.get_ship_date()
            page.apihit.get_sailor_details(flag=True)
            web_driver.open_website(url=urljoin(config.ship.url.replace('/svc', ''), "/notificationManagement/login"))
            page.login.verification_of_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            if not page.login.login_into_push_notification(username=creds.verticalqa.username, password=creds.verticalqa.password):
                raise Exception("User not landed on push notification dashboard")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("login_error")
            raise Exception(exp)

    @pytestrail.case(27798331)
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
            web_driver.allure_attach_jpeg("distribution list error")
            raise Exception(exp)

    @pytestrail.case(46176165)
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
            web_driver.allure_attach_jpeg("sailor notification error")
            raise Exception(exp)

    @pytestrail.case(46176632)
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
            web_driver.allure_attach_jpeg("search notification error")
            raise Exception(exp)

    @pytestrail.case(46176628)
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
            web_driver.allure_attach_jpeg("update notification error")
            raise Exception(exp)

    @pytestrail.case(40881818)
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
            web_driver.allure_attach_jpeg("update recipient list in notification error")
            raise Exception(exp)

    @pytestrail.case(46176631)
    def test_07_delete_notification_from_dashboard(self, web_driver, page):
        """
        Test cases to delete notification for sailor
        :param web_driver:
        :param page:
        :return:
        """
        try:
            old_notification_count = page.dashboard.get_dashboard_count()
            page.notification.delete_notification()
            count_verification_status = page.dashboard.get_notification_count_after_deleting(old_notification_count)
            if not count_verification_status:
                raise Exception("notification not getting deleted")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("search notification error")
            raise Exception(exp)

    @pytestrail.case(26682458)
    def test_08_free_form_notification_for_crew_schedule_now(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for crew in free form and schedule for now
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            old_notification_count = page.dashboard.get_dashboard_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            total_cabin_count = page.notification.create_new_free_form_notification(config, test_data, 'crew', 'now')
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
            web_driver.allure_attach_jpeg("crew notification error")
            raise Exception(exp)

    @pytestrail.case(46176166)
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
            web_driver.allure_attach_jpeg("distribution list notification error")
            raise Exception(exp)

    @pytestrail.case(26682461)
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
            web_driver.allure_attach_jpeg("template_error")
            raise Exception(exp)

    @pytestrail.case(46176633)
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
            web_driver.allure_attach_jpeg("sailor template notification error")
            raise Exception(exp)

    @pytestrail.case(26682459)
    def test_12_create_notification_by_template_for_crew_schedule_now(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for crew in template and schedule for now
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
            total_cabin_count = page.notification.create_new_template_notification(config, 'crew')
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
            web_driver.allure_attach_jpeg("crew template notification error")
            raise Exception(exp)

    @pytestrail.case(46176636)
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
            web_driver.allure_attach_jpeg("distribution list template notification error")
            raise Exception(exp)

    @pytestrail.case(46176635)
    def test_14_create_notification_by_template_for_sailor_schedule_voyage(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for sailor in template and schedule for voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_current_voyage()
            page.notification.create_template_notification_schedule_voyage('sailor', None)
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor template notification error")
            raise Exception(exp)

    @pytestrail.case(46176634)
    def test_15_create_notification_by_template_for_crew_schedule_voyage(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for crew in template and schedule for voayge
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_current_voyage()
            page.notification.create_template_notification_schedule_voyage('crew', None)
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                    raise Exception("Notification title is not displaying on dashboard")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("crew template notification error")
            raise Exception(exp)

    @pytestrail.case(46176637)
    def test_16_create_notification_by_template_for_dist_list_schedule_voyage(self, web_driver, page, test_data,
                                                                              config):
        """
        Test cases to create notification for distribution list in template and schedule for voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_current_voyage()
            page.notification.create_template_notification_schedule_voyage(
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
            web_driver.allure_attach_jpeg("distribution list template notification error")
            raise Exception(exp)

    @pytestrail.case(46175703)
    def test_17_free_form_notification_for_distribution_list_schedule_voyage(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for distribution list in free form and schedule for voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_free_form()
            page.notification.create_new_free_form_notification(config, test_data, test_data['distribution_list_name'],
                                                                'current_voyage')
            page.notification.click_save_button('current_voyage')
            count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
            if not count_verification_status:
                raise Exception("Notification count in dashboard not increasing")
            else:
                page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                if not page.notification.verify_created_scheduled_notification(test_data['TitleText']):
                    web_driver.allure_attach_jpeg("title error")
                    raise Exception("Notification title is not displaying on dashboard")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("distribution list free form voyage notification error")
            raise Exception(exp)

    @pytestrail.case(46177471)
    def test_18_template_notification_sailor_list_schedule_voyage(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for particular sailor in free form and schedule for voyage
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_current_voyage()
            if 'searched_sailor_stateroom' in test_data.keys():
                page.notification.create_template_notification_schedule_voyage('sailor', test_data['searched_sailor_stateroom'])
                count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
                if not count_verification_status:
                    raise Exception("Notification count in dashboard not increasing")
                else:
                    page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                    if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                        web_driver.allure_attach_jpeg("template error")
                        raise Exception("Notification title is not displaying on dashboard")
            else:
                page.notification.cancel_sailor()
                pytest.skip("No sailor available to add as recipient")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("sailor template voyage notification error")
            raise Exception(exp)

    @pytestrail.case(26682460)
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
            web_driver.allure_attach_jpeg("draft error")
            raise Exception(exp)

    @pytestrail.case(46177470)
    def test_20_template_notification_sailor_in_event(self, web_driver, page, test_data, config):
        """
        Test cases to create notification for user who have any of the event (shore thing, ent-inventoried etc)
        :param test_data:
        :param config:
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.click_on_tabs_from_dashboard('Dashboard')
            old_notification_count = page.dashboard.get_scheduled_notification_count()
            page.dashboard.click_on_tabs_from_dashboard('CREATE NEW NOTIFICATION')
            page.notification.verify_header()
            page.notification.select_random_template(test_data)
            page.notification.select_template_arrow(test_data)
            page.notification.enter_url(config)
            page.notification.schedule_for_current_voyage()
            if not page.notification.create_event_notification_schedule_voyage('sailor'):
                count_verification_status = page.dashboard.get_new_scheduled_notification_count(old_notification_count)
                if not count_verification_status:
                    raise Exception("Notification count in dashboard not increasing")
                else:
                    page.dashboard.click_on_tabs_from_dashboard("Scheduled Notifications")
                    if not page.notification.verify_created_scheduled_notification(test_data['templateTitle']):
                        web_driver.allure_attach_jpeg("template error")
                        raise Exception("Notification title is not displaying")
            else:
                logger.info('No sailor for particular event')

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("event notification error")
            raise Exception(exp)

    @pytestrail.case(46176630)
    def test_21_download_notification_pdf(self, web_driver, page):
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
            web_driver.allure_attach_jpeg("pdf download error")
            raise Exception(exp)

    @pytestrail.case(46176629)
    def test_22_download_notification_excel(self, web_driver, page):
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
            web_driver.allure_attach_jpeg("pdf download error")
            raise Exception(exp)

    @pytestrail.case(71158095)
    def test_23_delete_used_template(self, web_driver, page, test_data):
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
            web_driver.allure_attach_jpeg("delete used template error")
            raise Exception(exp)

    @pytestrail.case([60788995, 75341979])
    def test_24_delete_template(self, web_driver, page, test_data):
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
            web_driver.allure_attach_jpeg("delete_template")
            raise Exception(exp)