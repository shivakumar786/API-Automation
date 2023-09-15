__author__ = 'sarvesh.singh'


from ui_pages.aci.apihit import ApiHit
from ui_pages.aci.dashboard import Dashboard
from ui_pages.aci.login import Login
from ui_pages.aci.search_list import SearchList
from ui_pages.aci.setting import Setting
from ui_pages.aci.identification import Identification
from ui_pages.aci.health import Health
from ui_pages.aci.personal import Personal
from ui_pages.aci.travel import Travel
from ui_pages.aci.folio import Folio
from ui_pages.aci.contract import Contract
from ui_pages.aci.finalize import Finalize
from virgin_utils import *


@pytest.mark.ACI_UI
@pytest.mark.run(order=4)
class TestACIApp:
    """
    Test Suite to test ACI application Performance
    """

    @pytestrail.case(487)
    def test_01_login(self, page, config, web_driver, test_data, guest_data, creds, request, rest_ship, couch,
                      rest_shore=None):
        """
        Launch the ACI app and login into application
        :param rest_shore:
        :param web_driver:
        :param page:
        :param config:
        :param rest_shore:
        :param test_data:
        :param guest_data:
        :return:
        """
        try:
            username = request.config.getoption("--username")
            password = request.config.getoption("--password")
            web_driver.wait_for(10)
            setattr(page, 'login', Login(web_driver, config))
            setattr(page, 'setting', Setting(web_driver, config))
            setattr(page, 'apihit', ApiHit(config, rest_shore, rest_ship, test_data))
            setattr(page, 'dashboard', Dashboard(web_driver, config))
            setattr(page, 'search_list', SearchList(web_driver, config))
            setattr(page, 'identification', Identification(web_driver, guest_data, test_data, rest_ship, couch, config))
            setattr(page, 'health', Health(web_driver, config))
            setattr(page, 'personal', Personal(web_driver, config))
            setattr(page, 'travel', Travel(web_driver, config))
            setattr(page, 'folio', Folio(web_driver, config))
            setattr(page, 'contract', Contract(web_driver, config))
            setattr(page, 'finalize', Finalize(web_driver, config, test_data))
            if config.ship.url == 'https://application-integration.ship.virginvoyages.com/svc/':
                page.login.select_ship_name('Scarlet Lady')
            elif config.ship.url == 'https://dclshipdxpcore.wdw.disney.com/':
                page.login.select_ship_name('Disney Dream')
            if page.login.check_availability_of_login_page():
                if config.platform == 'DCL':
                    page.login.sign_in(username=username, password=password)
                else:
                    if config.env == 'CERT':
                        page.login.sign_in(username=creds.aci.login.username, password=creds.aci.login.password)
                    else:
                        page.login.sign_in(username=creds.verticalqa.username, password=creds.verticalqa.password)
            else:
                raise Exception("Login page not display after launch the app")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("login_error")
            raise Exception(exp)

    @pytestrail.case(32100941)
    def test_02_select_setting(self, page, web_driver):
        """
        Launch the ACI app and login into application
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.setting.check_availability_of_setting_page():
                page.setting.click_on_next()
            else:
                web_driver.allure_attach_jpeg("setting_error")
                raise Exception("Setting page not display after login into application")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("setting_error")
            raise Exception(exp)

    @pytestrail.case(482)
    def test_03_verify_dashboard(self, page, web_driver):
        """
        To verify dashboard
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if page.dashboard.check_availability_of_dashboard_page():
                page.dashboard.verify_voyage_dropdown()
                if not page.dashboard.verify_search_icon():
                    raise Exception("Incorrect dashboard")
            else:
                web_driver.allure_attach_jpeg("dashboard_error")
                raise Exception("Dashboard page not display after login into application")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("dashboard_error")
            raise Exception(exp)

    @pytestrail.case(32148262)
    def test_04_get_cabin(self, page, web_driver):
        """
        Get Cabin number
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.apihit.get_token()
            page.apihit.get_voyage_details()
            page.apihit.get_document_bucket()
            page.apihit.get_cabin()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("cabin_error")
            raise Exception(exp)

    @pytestrail.case(488)
    def test_05_travel_document_details(self, page, web_driver, test_data, config):
        """
        Perform travel document tab
        Perform Guest Info tab
        :param web_driver:
        :param page:
        :param test_data:
        :return:
        """
        try:
            for data in test_data['cabins']:
                page.dashboard.search(text=data)
                if page.search_list.check_availability_of_search_result():
                    logger.error(f"No records found in 10 sec with given search parameter: {data}")
                else:
                    page.apihit.get_reservation_details(data)
                    break
            page.search_list.click_check_in(index=1)
            # page.identification.check_availability_of_dob_and_fill()
            page.identification.click_identification_tab()
            total_guests = page.identification.get_total_guests()
            test_data['guest_count'] = total_guests
            for _count in range(total_guests):
                if page.identification.check_identification_tab_enabled() == 'false':
                    break
                page.health.scroll_top()
                page.identification.update_photo()
                if page.identification.check_us_citizenship():
                    page.identification.update_passport()
                else:
                    page.identification.update_passport()
                    page.identification.update_support_doc()
                web_driver.wait_for(2)
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest identification tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(29138719)
    def test_06_health_form(self, page, web_driver, test_data, config):
        """
        perform guest health tab
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            guests = test_data['guest_count']
            for _count in range(guests):
                if page.health.check_health_tab_enabled() == 'false':
                    break
                if config.platform != 'VIRGIN':
                    page.health.scroll_top()
                    # page.health.scroll_top()
                    page.health.perform_health()
                    page.health.click_save_proceed()
                else:
                    page.health.scroll_top()
                    # page.health.scroll_top()
                    # page.health.accept_voyage_well_terms()
                    # page.health.vaccination_details()
                    page.health.perform_health()
                    # page.health.pass_additional_health_protocol()
                    page.health.click_save_proceed()
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest Health tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(38813192)
    def test_07_personal_details(self, page, web_driver, test_data, config):
        """
        Perform Guest personal tab
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            guests = test_data['guest_count']
            for _count in range(guests):
                if page.personal.check_personal_tab_enabled() == 'false':
                    break
                page.health.scroll_top()
                page.personal.update_address()
                page.personal.update_emergency_contact()
                if config.platform != 'VIRGIN':
                    page.personal.additional()
                page.personal.click_save_proceed()
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest Personal detail tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(41623216)
    def test_08_travel_details(self, page, web_driver, test_data, config):
        """
        Perform Guest Travel tab
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            guests = test_data['guest_count']
            for _count in range(guests):
                if page.travel.check_travel_tab_enabled() == 'false':
                    break
                page.travel.scroll_top()
                # page.travel.scroll_top()
                page.travel.update_pre_cruise()
                page.travel.update_post_cruise()
                page.travel.click_save_proceed()
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest Travel tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(37689427)
    def test_09_guest_folio(self, page, web_driver, test_data, config):
        """
        perform folio
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            guests = test_data['guest_count']
            for _count in range(guests):
                if page.folio.check_folio_tab_enabled() == 'false':
                    break
                page.travel.scroll_top()
                page.folio.update_payment_information()
                page.folio.click_save_proceed()
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest Payment/Folio tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(41623217)
    def test_10_guest_cruise_contract(self, page, web_driver, test_data, config):
        """
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            guests = test_data['guest_count']
            for _count in range(guests):
                if page.contract.check_contract_tab_enabled() == 'false':
                    break
                page.travel.scroll_top()
                page.contract.update_digital_contract(test_data['guest_count'])
                page.contract.click_save_proceed()
                if page.contract.check_contract_tab_enabled() == 'false':
                    break
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest Cruise contract tab is not completed !!!")
            raise Exception(exp)

    @pytestrail.case(62291876)
    def test_11_finalize_tab(self, page, web_driver, test_data, config):
        """
        :param page:
        :param web_driver:
        :param test_data:
        :param config:
        :return:
        """
        try:
            if page.finalize.check_availability_of_alert_popup():
                page.finalize.click_done()
                page.finalize.click_done()
            else:
                page.travel.scroll_top()
                page.finalize.click_finalize_tab()
                page.finalize.click_check_in()
                page.finalize.click_done()
        except Exception as exp:
            web_driver.allure_attach_jpeg("Guest ACI has been not completed !!!")
            raise Exception(exp)

    @pytestrail.case(28607816)
    def test_12_create_alert(self, page, web_driver, test_data,config):
        """
        Verify create alert functionality
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.search(test_data['cabins'][0])
            page.apihit.get_reservation_details(test_data['cabins'][0])
            if page.search_list.check_availability_of_search_result():
                raise Exception(
                    f"No records found in 1 min with given search parameter :{test_data['cabins'][0]}")
            else:
                guests = len(page.search_list.get_search_results()) + 1
                page.search_list.select_sailor()
                page.dashboard.create_alert_option()
                if config.platform == 'DCL':
                    page.dashboard.select_alert_code()
                    page.dashboard.create_alert_sailor()
                else:
                    page.dashboard.create_alert_sailor()
                    if not page.dashboard.verify_alert():
                        raise Exception("Alert not created")

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("alert_error")
            raise Exception(exp)

    @pytestrail.case(70452113)
    def test_13_edit_alert(self, page, web_driver, test_data, config):
        """
        Verify edit alert
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.dashboard.verify_alert():
                raise Exception("Alert not created")
            else:
                page.dashboard.edit_alert()
                if not page.dashboard.verify_edit_alert():
                    raise Exception("Alert not edited")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("alert_edit_error")
            raise Exception(exp)

    @pytestrail.case(70452114)
    def test_14_delete_alert(self, page, web_driver, test_data, config):
        """
        Verify delete alert
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if not page.dashboard.verify_edited_alert():
                raise Exception("Alert not created")
            else:
                page.dashboard.delete_alert()
                if not page.dashboard.verify_delete_alert():
                    raise Exception("Alert not deleted")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("alert_delete_error")
            raise Exception(exp)

    @pytestrail.case(70452307)
    def test_15_create_message(self, page, web_driver, test_data, config):
        """
        Verify create message functionality
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if config.platform == 'DCL':
                page.dashboard.navigate_back()
                page.dashboard.navigate_back()
                page.dashboard.navigate_back()
                pytest.skip("message not available in dcl")
            else:
                page.dashboard.navigate_back()
                page.dashboard.create_message()
                if not page.dashboard.verify_message():
                    raise Exception("message not created")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("message_error")
            raise Exception(exp)

    @pytestrail.case(70452115)
    def test_16_edit_message(self, page, web_driver, test_data, config):
        """
        Verify edit message
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if config.platform == 'DCL':
                pytest.skip("message not available in dcl")
            else:
                if not page.dashboard.verify_message():
                    raise Exception("message not created")
                else:
                    page.dashboard.edit_message()
                    if not page.dashboard.verify_edit_msg():
                        raise Exception("message not edited")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("message_edit_error")
            raise Exception(exp)

    @pytestrail.case(70452116)
    def test_17_acknowledge_msg(self, page, web_driver, test_data, config):
        """
        Verify acknowledge message
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if config.platform == 'DCL':
                pytest.skip("message not available in dcl")
            else:
                if not page.dashboard.verify_message():
                    raise Exception("message not created")
                else:
                    if page.dashboard.acknowledge_message():
                        raise Exception("msg not acknowledged")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("msg_acknowledge_error")
            raise Exception(exp)

    @pytestrail.case(29139328)
    def test_18_express_checkin(self, page, web_driver, test_data, config):
        """
        Verify express check in
        :param web_driver:
        :param page:
        :return:
        """
        try:
            if config.platform == 'DCL':
                pytest.skip("express check in not available in dcl")
            else:
                page.dashboard.navigate_back()
                page.dashboard.navigate_back()
                random.shuffle(test_data['cabins'])
                if test_data['cabins'][0] == 'GTY' or test_data['cabins'][0] == 9999:
                    random.shuffle(test_data['cabins'])

                page.dashboard.search(text=test_data['cabins'][0])
                page.apihit.get_reservation_details(test_data['cabins'][0])
                if page.search_list.check_availability_of_search_result():
                    raise Exception(
                        f"No records found in 1 min with given search parameter :{test_data['cabins'][0]}")
                else:
                    guests = len(page.search_list.get_search_results()) + 1
                    page.search_list.click_check_in(index=1)
                    page.finalize.express_checkin()
                    if not page.finalize.verify_express_checkin():
                        raise Exception("Error for express check in not displaying")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("express_check_in_error")
            raise Exception(exp)

    @pytestrail.case(37690620)
    def test_19_verify_hotel_mode(self, page, web_driver,config):
        """
        Verify hotel mode
        :param web_driver:
        :param page:
        :param config:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu()
            page.dashboard.click_on_settings_page()
            page.setting.switch_mode()
            mode = page.dashboard.verify_hotel_mode()
            if config.platform == 'DCL':
                if mode != "Resort / Airport":
                    raise Exception("Mode note changed")
            else:
                if mode != "Hotel / Airport":
                    raise Exception("Mode note changed")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Hotel_mode_error")
            raise Exception(exp)

    @pytestrail.case(70452212)
    def test_20_hotel_mode_voyage(self, page, web_driver, config):
        """
        Verify hotel mode voyages
        :param web_driver:
        :param page:
        :param config:
        :return:
        """
        try:
            if not page.dashboard.verify_voyage_in_hotel_mode():
                raise Exception("No voyages are displaying in hotel mode")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("Hotel_mode_error")
            raise Exception(exp)

    @pytestrail.case(37690622)
    def test_21_ship_itinerary(self, page, web_driver, config):
        """
        Verify ship itinerary
        :param web_driver:
        :param page:
        :param config:
        :return:
        """
        try:
            page.dashboard.click_on_hamburger_menu()
            page.dashboard.click_on_ship_itinerary()
            if page.dashboard.verify_itinerary() <= 1:
                raise Exception("Itinerary page is giving error")
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("itinerary_error")
            raise Exception(exp)

    @pytestrail.case(481)
    def test_22_logout(self, page, web_driver):
        """
        Verify logout functionality
        :param web_driver:
        :param page:
        :return:
        """
        try:
            page.dashboard.navigate_back()
            page.dashboard.click_on_hamburger_menu()
            page.dashboard.click_signout()
            page.login.check_availability_of_login_page()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg("logout_error")
            raise Exception(exp)