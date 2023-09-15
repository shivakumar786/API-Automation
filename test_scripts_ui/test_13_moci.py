from virgin_utils import *
from ui_pages.moci.apihit import Apihits
from ui_pages.moci.guest_details import GuestDetails
from ui_pages.moci.history import History
from ui_pages.moci.moci_login import MociLogin
from ui_pages.moci.moci_dashboard import MociDashboard
from ui_pages.moci.guest_list import GuestList
from ui_pages.moci.reports import Report
from ui_pages.moci.guest_filter import GuestFilter


@pytest.mark.MOCI
@pytest.mark.run(order=13)
class TestMOCI:
    """
    Test Suite to test Moderate Online Check-in
    """

    @pytestrail.case(481777)
    def test_01_open_website_and_check_invalid_login(self, web_driver, config, page, rest_shore, test_data, db_core,
                                                       guest_data):
        """
        Test cases to Launch the MOCI and login into application with invalid credentials
        :param web_driver:
        :param page:
        :param config:
        :param rest_shore:
        :param test_data:
        :param db_core:
        :param guest_data:
        :return:
        """
        try:
            setattr(page, 'login', MociLogin(web_driver))
            setattr(page, 'history', History(web_driver, test_data))
            setattr(page, 'apihit', Apihits(config, rest_shore, test_data, guest_data, db_core))
            setattr(page, 'detail', GuestDetails(web_driver, test_data))
            setattr(page, 'dashboard', MociDashboard(web_driver, test_data))
            setattr(page, 'list', GuestList(web_driver, test_data))
            setattr(page, 'report', Report(web_driver))
            setattr(page, 'guest_filter', GuestFilter(web_driver))

            guest_data = []
            page.apihit.get_voyages()
            page.apihit.reservation_details()
            page.apihit.shore_reservation_details(guest_data)

            web_driver.open_website(url=urljoin(config.shore.url, "/moderate-online-checkin/"
                                                                      "authentication?logintype=form"))
            page.login.verification_of_moci_login_page()
            web_driver.allure_attach_jpeg("availability_of_login_page")
            page.login.login_into_moci(username=generate_email_id(), password='abcd123')
            page.login.verification_of_invalid_user_login_error_toast()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg("invalid_login_error")
            raise Exception(exp)

    @pytestrail.case(44927567)
    def test_02_login_with_guests_credential_and_verify_error_message(self, page, web_driver, test_data, guest_data):
        """
        Crew should not login with sailor app guest credential
        :param page:
        :param web_driver:
        :param test_data:
        :param guest_data
        :return:
        """
        try:
            page.login.login_into_moci(username=guest_data[0]['Email'], password='Voyages@9876')
            page.login.verification_of_moci_login_error_toast_with_guest()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('valid_login_error')
            raise Exception(exp)

    @pytestrail.case(481778)
    def test_03_login(self, page, web_driver, creds):
        """
        Login with valid credentials
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.login.login_into_moci(username=creds.verticalqa.username, password=creds.verticalqa.password)
            if page.dashboard.verification_of_moci_dashboard():
                logger.debug("User is able to login successfully")
            else:
                web_driver.allure_attach_jpeg('login_not_done')
                raise Exception("Login is not working, some backend error is coming")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('valid_login_error')
            raise Exception(exp)

    @pytestrail.case(481781)
    def test_04_verify_crew_name(self, page, web_driver):
        """
        To verify the crew name.
        :params page:
        :params web_driver:
        """
        try:
            page.dashboard.click_logo()
            name = page.dashboard.verify_crew_name()
            if name != "VQ":
                raise Exception("Crew name is not matching")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Crew_name_error')
            raise Exception(exp)

    @pytestrail.case(481940)
    def test_05_verify_show_me_button(self, page, web_driver):
        """
        To verify show me button and total count of ship.
        :params page:
        :params web_driver:
        """
        try:
            page.dashboard.click_logo()
            count = page.dashboard.verify_availability_show_me()
            total = page.dashboard.total_voyages()
            if str(len(count)) != total:
                raise Exception("Count are matching !!")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Show_me_button_error')
            raise Exception(exp)

    @pytestrail.case(481949)
    def test_06_availability_history_page(self, page, web_driver):
        """
        Check the availability of History page after click on History button on Dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.click_history()
            page.history.verification_of_history_page()
            page.dashboard.click_logo()
            page.dashboard.click_voyage_view()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('history_error')
            raise Exception(exp)

    @pytestrail.case(481947)
    def test_07_availability_of_report_page(self, page, web_driver):
        """
        Check the availability of Report page on Dashboard
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_reports()
            page.report.verification_of_report_page()
            # verify the Sailor Records Moderation Status report
            page.report.open_report()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('report_error')
            raise Exception(exp)

    @pytestrail.case([6036277,76579857])
    def test_08_very_switch_ship_voyage(self, page, web_driver):
        """
        To verify the switch process ship and voyage mode
        :params page:
        :params web_driver:
        """
        try:
            page.dashboard.click_logo()
            # verify the Report Pop-up
            page.report.clear_pop_up()
            page.dashboard.click_voyage_view()
            page.dashboard.click_ship_view()
            page.dashboard.click_voyage_view()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Switch_error')
            raise Exception(exp)

    @pytestrail.case(41384492)
    def test_09_verify_ship_mode_page(self, page, web_driver):
        """
        To verify the ship mode page
        :params page:
        :params web_driver:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.click_ship_view()
            page.dashboard.verify_ship_mode()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Ship_page_error')
            raise Exception(exp)

    @pytestrail.case(41384493)
    def test_10_verify_voyage_mode_page(self, page, web_driver):
        """
        To verify the voyages mode page
        :params page:
        :params web_driver:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.click_voyage_view()
            page.dashboard.verify_voyage_mode()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Voyage_page_eror')
            raise Exception(exp)

    @pytestrail.case(481945)
    def test_11_search_with_firstname_lastname_res_number(self, page, web_driver, test_data):
        """
        Test to check the search with firstname lastname and reservation number
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.verification_of_moci_dashboard()
            page.dashboard.search(test_data['shore_reservationNumber'])
            page.list.get_total_guest_in_list()
            if test_data['total_guests'] > 0:
                page.list.verify_reservation_number()
                page.list.get_guest_name()
            page.dashboard.search(test_data['name_1'].split(" ")[0])
            if test_data['total_guests'] > 0:
                logger.debug("Search is working fine with First Name")
            else:
                raise Exception("Search is not working with First Name ")
            page.dashboard.search(test_data['name_1'].split(" ")[1])
            if test_data['total_guests'] > 0:
                logger.debug("Search is working fine with Last Name")
            else:
                raise Exception("Search is not working with Last Name")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('search_error')
            raise Exception(exp)

    @pytestrail.case(50350255)
    def test_12_moci_lading_on_primary_guest(self, page, web_driver, test_data):
        """
        Test to check the functionality that on guest details always load on Primary Guest
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        try:
            page.dashboard.search(test_data['shore_reservationNumber'])
            guest_count = test_data['total_guests']
            if guest_count > 0:
                page.list.get_non_primary_guest_name()
                page.list.get_primary_guest_name()
                if page.detail.check_status_in_guest_list(0) not in ["not started", "Incomplete"]:
                    page.list.click_selected_guest_name(test_data['primary_guest_name'])
                    if page.detail.verify_guest_name_disable_or_enable() == "false":
                        name = page.detail.get_active_tab_guest_name()
                        test_data['guest_name'] = name
                        if name == test_data['primary_guest_name_without_middle'].upper():
                            logger.debug("Primary Guest tab is selected")
                    else:
                        web_driver.allure_attach_jpeg("If we not click on edit button, The Guest name and "
                                                      "DOC fields are enabled!!")
                        pytest.skip("If we not click on edit button, The Guest name and DOC fields are enabled!!")
                else:
                    web_driver.allure_attach_jpeg("Guest_RTS_is_Not_completed")
                    pytest.skip("Guest RTS is not completed")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('fields_available_error')
            raise Exception(exp)

    @pytestrail.case([76590714,76590729,76590730])
    def test_13_edit_guest_name_and_dob(self, page, web_driver):
        """
        verify the guest edit option and update the guest name and DOB
        Test to check the Guest details page availability
        :param page:
        :param web_driver:
        :return:
        """
        try:
            if page.detail.verify_guest_name_disable_or_enable() == "false":
                page.detail.check_edit_button_is_visible()
                if page.detail.verify_guest_name_disable_or_enable() == "true":
                    page.detail.edit_first_name_value()
                    # page.detail.edit_middle_name_value() middle name is revert we have a know bug
                    page.detail.edit_last_name_value()
                    page.detail.edit_dob_value()

                    # verify the Update and Cancel button is visible or not and click on update.
                    page.detail.verify_the_update_and_cancel_button()

        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('Edit name functionality is not working')
            raise Exception(exp)

    @pytestrail.case(481946)
    def test_14_verify_guest_details_(self, page, web_driver, test_data):
        """
        Test to check the Guest details page availability
        :param page:
        :param web_driver:
        :return:
        """
        try:
            name = page.detail.get_active_tab_guest_name()
            test_data['guest_name'] = name
            page.detail.verify_guest_detail_page()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('guest_details_error')
            raise Exception(exp)

    @pytestrail.case(507121)
    def test_15_verify_personal_info(self, page, web_driver, test_data):
        """
        To verify personal info in guest detail page.
        :params page:
        :params web_driver:
        :params test_data:
        """
        try:
            page.detail.get_first_name_value()
            page.detail.get_last_name_value()
            page.detail.verify_guest_detail_page()
            first_name = test_data["display_fn"].upper()
            last_name = test_data["display_ln"].upper()
            name = test_data['guest_name'].split(" ")
            if len(name) == 2:
                n1 = name[0]
                n2 = name[1]
            else:
                n1 = name[0]
                n2 = name[2]
            assert n1 == first_name, "Details are not reflected in guest details page !!"
            assert n2 == last_name, "Details are not reflected in guest details page !!"

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('guest_details_error')
            raise Exception(exp)

    @pytestrail.case(507124)
    def test_16_verify_pregnancy_details(self, page, web_driver, guest_data, test_data):
        """
        verify pregnancy details.
        :params page:
        :params web_driver:
        :params test_data:
        :params guest_data:
        """
        try:
            for _guest in test_data['guest_details']['eCheckinGuestDetailsList']:
                if _guest['personalInfo']['firstName'] == test_data['display_fn'] and _guest['personalInfo']['lastName'] == test_data['display_ln']:
                    test_data["gender_code"] = _guest['personalInfo']['genderCode']
                    break
            if test_data["gender_code"] == 'F':
                page.detail.check_pregnancy_info()
                logger.debug("Pregnancy details is available")
            else:
                pytest.skip("Guest is Male. We can't verify the pregnancy details !!")
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Pregnancy_check_error')
            raise Exception(exp)

    @pytestrail.case(507122)
    def test_17_verify_payment_details(self, page, web_driver):
        """
        To verify the payment details
        :params page:
        :params web_driver:
        """
        try:
            page.detail.check_payment_info()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Payment info is not available')
            raise Exception(exp)

    @pytestrail.case(507123)
    def test_18_verify_user_contract_signed_or_not(self, page, web_driver):
        """
        To verify the contract signed or not
        :params page:
        :params web_driver:
        """
        try:
            val = page.detail.check_voyage_contract_info()

            if val:
                logger.debug("Voyage contract is signed")
            else:
                raise Exception("voyage contract is not signed")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Payment info is not available')
            raise Exception(exp)

    @pytestrail.case(481951)
    def test_19_verify_availability_approve_reject_button(self, page, web_driver):
        """
        Test to check the availability of approve or reject button
        :param page:
        :param web_driver:
        :return:
        """
        try:
            doc_name = page.detail.get_document_name()
            if doc_name == "Passport":
                if ((page.detail.check_availability_of_approve_button_with_security_photo() or
                     page.detail.check_availability_of_reject_button_with_security_photo()) and
                        (page.detail.check_availability_of_approve_button_with_passport_photo() or
                         page.detail.check_availability_of_reject_button_with_passport_photo())):
                    logger.info("Approve or Reject button display with passport and security image")
                else:
                    raise Exception("Approve or Reject button not display with passport and security image")

        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('approve_or_reject_button_missing')
            raise Exception(exp)

    @pytestrail.case(481958)
    def test_20_verify_that_user_add_comment(self, page, web_driver, test_data):
        """
        To verify the added message
        :params page:
        :params web_driver:
        :params test_data:
        """
        try:
            page.detail.click_on_text_field()
            page.detail.click_save_next()
            page.list.click_selected_guest_name(test_data['primary_guest_name'])
            page.detail.verify_guest_detail_page()
            comment = page.detail.verify_added_comment()
            assert comment, "Not able to add the comment"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('verify added comments')
            raise Exception(exp)

    @pytestrail.case(481950)
    def test_21_verify_review_later(self, page, web_driver):
        """
        verify review later functionality
        :params page:
        :params web_driver:
        """
        try:
            page.detail.check_availability_review_later()
            page.detail.verify_review_later()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('Verify review later')
            raise Exception(exp)

    @pytestrail.case(229)
    def test_22_approve_united_state_guest(self, page, web_driver, test_data):
        """
        Test to check the moderator able to approve the US guest
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        guest_data = []
        page.apihit.us_reservation_details()
        if test_data["personid"] != None:
            page.apihit.shore_reservation_details(guest_data)
            try:
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                page.list.get_total_guest_in_list()
                page.list.get_guest_name()
                for count in range(test_data['total_guests']):
                    if page.detail.check_status_in_guest_list(count) not in ["not started", "Incomplete", "Incomplete Messaged Overdue"]:
                        page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                        test_data[f"tab_guest_name_{count}"] = page.detail.get_active_tab_guest_name()
                        test_data[f"guest_name_{count}"] = page.detail.displayed_complete_name()
                        doc_name = page.detail.get_document_name()
                        page.detail.approve_security_photo()
                        if doc_name == "Passport":
                            page.detail.approve_passport()
                        page.detail.click_save_next()
                    else:
                        web_driver.allure_attach_jpeg("Guest_RTS_is_Not_completed")
                        pytest.skip("Guest RTS is not completed")
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                for count in range(test_data['total_guests']):
                    page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                    status = page.detail.check_status()
                    if status != "Approved":
                        raise Exception("Guest is not approved")
                    web_driver.wait_for(5)

            except(Exception, ValueError)as exp:
                web_driver.allure_attach_jpeg('us_approve_error')
                raise Exception(exp)
        else:
            web_driver.allure_attach_jpeg('us_approve_Guest_is_Not_available')
            pytest.skip("US guest is not available for Approved in MOCI for this reservation voyage !!")

    @pytestrail.case(236)
    def test_23_approve_indian_guest(self, page, web_driver, test_data):
        """
        Test to check the moderator able to approve the Indian guest
        :param page:
        :param web_driver:
        :param test_data:
        :return:
        """
        guest_data = []
        page.apihit.in_reservation_details()
        if test_data["personid"] != None:
            page.apihit.shore_reservation_details(guest_data)
            try:
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                page.list.get_total_guest_in_list()
                page.list.get_guest_name()
                for count in range(test_data['total_guests']):
                    if page.detail.check_status_in_guest_list(count) not in ["not started", "Incomplete"]:
                        page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                        test_data[f"tab_guest_name_{count}"] = page.detail.get_active_tab_guest_name()
                        test_data[f"guest_name_{count}"] = page.detail.displayed_complete_name()
                        doc_name = page.detail.get_document_name()
                        page.detail.approve_security_photo()
                        if doc_name == "Passport":
                            page.detail.approve_passport()
                        page.detail.approve_visa()
                        page.detail.click_save_next()
                    else:
                        web_driver.allure_attach_jpeg("Guest_RTS_is_Not_completed")
                        pytest.skip("Guest RTS is not completed")
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                for count in range(test_data['total_guests']):
                    page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                    status = page.detail.check_status()
                    if status != "Approved":
                        raise Exception("Guest is not approved")

            except(Exception, ValueError)as exp:
                web_driver.allure_attach_jpeg('indian_approve_error')
                raise Exception(exp)
        else:
            web_driver.allure_attach_jpeg('Indian_approve_Guest_is_Not_available')
            pytest.skip("Indian guest is not available for approved in MOCI for this reservation voyage !!")

    @pytestrail.case(227)
    def test_24_reject_us_guest(self, page, test_data, web_driver):
        """
        To reject us guest.
        :params page:
        :params test_data:
        :params web_driver:
        """
        guest_data = []
        page.apihit.us_reservation_details()
        if test_data["personid"] != None:
            page.apihit.shore_reservation_details(guest_data)
            try:
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                page.list.get_total_guest_in_list()
                page.list.get_guest_name()
                for count in range(test_data['total_guests']):
                    if page.detail.check_status_in_guest_list(count) not in ["not started", "Incomplete"]:
                        page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                        test_data[f"tab_guest_name_{count}"] = page.detail.get_active_tab_guest_name()
                        test_data[f"guest_name_{count}"] = page.detail.displayed_complete_name()
                        doc_name = page.detail.get_document_name()
                        if doc_name == "Passport":
                            page.detail.reject_passport()
                        page.detail.click_save_next()
                    else:
                        web_driver.allure_attach_jpeg("Guest_RTS_is_Not_completed")
                        pytest.skip("Guest RTS is not completed")
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                for count in range(test_data['total_guests']):
                    page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                    status = page.detail.check_status()
                    if status != 'Incomplete Messaged':
                        raise Exception("US guest is not rejected")

            except(Exception, ValueError)as exp:
                web_driver.allure_attach_jpeg('us_reject_Guest_is_Not_available')
                raise Exception(exp)
        else:
            web_driver.allure_attach_jpeg('us_reject_error')
            pytest.skip("US guest is not available foe Rejection in MOCI for this reservation voyage !!")

    @pytestrail.case(239)
    def test_25_reject_indian_guest(self, page, test_data, web_driver):
        """
        To reject indian guest.
        :params test_data:
        :params web_driver:
        """
        guest_data = []
        page.apihit.in_reservation_details()
        if test_data["personid"] != None:
            page.apihit.shore_reservation_details(guest_data)
            try:
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                page.list.get_total_guest_in_list()
                page.list.get_guest_name()
                for count in range(test_data['total_guests']):
                    if page.detail.check_status_in_guest_list(count) not in ["not started", "Incomplete"]:
                        page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                        test_data[f"tab_guest_name_{count}"] = page.detail.get_active_tab_guest_name()
                        test_data[f"guest_name_{count}"] = page.detail.displayed_complete_name()
                        doc_name = page.detail.get_document_name()
                        if doc_name == "Passport":
                            page.detail.reject_passport()
                        page.detail.reject_visa()
                        page.detail.click_save_next()
                    else:
                        web_driver.allure_attach_jpeg("Guest_RTS_is_Not_completed")
                        pytest.skip("Guest RTS is not completed")
                page.dashboard.click_logo()
                page.dashboard.verification_of_moci_dashboard()
                page.dashboard.search(test_data['shore_reservationNumber'])
                for count in range(test_data['total_guests']):
                    page.list.click_selected_guest_name(test_data[f'name_{count+1}'])
                    status = page.detail.check_status()
                    if status != 'Incomplete Messaged':
                        raise Exception("Guest is not approved")

            except(Exception, ValueError)as exp:
                web_driver.allure_attach_jpeg('indian_reject_error')
                raise Exception(exp)
        else:
            web_driver.allure_attach_jpeg('Indian_reject_Guest_is_Not_available')
            pytest.skip("Indian guest is not available foe Rejection in MOCI for this reservation voyage !!")

    @pytestrail.case(75601782)
    def test_26_verify_the_moderation_by_user_report(self, page, web_driver):
        """
        To verify the Moderation by user reports is visible
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.click_reports()
            page.report.moderate_by_user_report_is_visible()
            page.report.open_moderate_by_user_reports()
        except(Exception, ValueError) as exp:
            web_driver.allure_attach_jpeg('Moderation by User reports is missing in report section')
            raise Exception(exp)

    @pytestrail.case(6036278)
    def test_27_verify_guest_list_filter(self, page, web_driver):
        """
        Test to verify guest list filters in Ship Mode
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.click_ship_view()
            page.dashboard.search_ship("Scarlet Lady")
            page.dashboard.click_ship_tile()
            page.guest_filter.click_all_checkbox()
            page.guest_filter.click_all_checkbox()
            page.guest_filter.click_approved_checkbox()
            page.guest_filter.click_update_button()
            status = page.guest_filter.verify_guest_status()
            assert status == 'Approved', "Guest Status Mismatch"
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('filters_error')
            raise Exception(exp)

    @pytestrail.case(481962)
    def test_28_verify_logout(self, page, web_driver):
        """
        Logout from MOCI app
        :param page:
        :param web_driver:
        :return:
        """
        try:
            page.dashboard.click_logo()
            page.dashboard.verification_of_moci_dashboard()
            page.dashboard.click_user_avatar()
            page.dashboard.click_logout()
        except(Exception, ValueError)as exp:
            web_driver.allure_attach_jpeg('logout_error')
            raise Exception(exp)
