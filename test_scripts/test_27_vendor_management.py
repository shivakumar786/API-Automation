__author__ = 'HT'
__maintainer__ = 'piyush.kumar'

from virgin_utils import *


@pytest.mark.VENDOR_MANAGEMENT
@pytest.mark.run(order=28)
class TestVendorManagement:
    """
    Test Suite to test ARS Vendor Management
    """

    @pytestrail.case(929363)
    def test_01_retrieve_payment_term(self, config, test_data, rest_ship):
        """
        Retrieving vendor payment term id
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settings/paymentterm")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) > 0:
            test_data['vendor']['paymenttermuuid'] = _content[0]['vendorpaymenttermid']
        else:
            body = [
                {
                    "description": "By The End of Voyage"
                }
            ]
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            test_data['vendor']['paymenttermuuid'] = _content[0]['vendorpaymenttermid']

    @pytestrail.case(24874456)
    def test_02_get_vendor(self, config, test_data, rest_ship):
        """
        To verify the vendor list availability
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['vendor']['current_date'] = change_epoch_time(datetime.today().date())
        test_data['vendor']['current_time'] = change_epoch_of_datetime(test_data['crew_framework']['currentDate'])
        test_data['vendor']['accountstatus'] = ['SETTLED', 'PENDING', 'REJECTED','REPORT_UPLOADED']
        test_data['vendor']['accountStatus'] = False
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {"voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty vendor list"
        for _vendor in _content:
            if _vendor['accountstatus'] not in test_data['vendor']['accountstatus'] and _vendor['balance'] > 0:
                test_data['vendor']['vendor_uuid'] = _vendor['vendoruuid']
                _vendor_uuid = _vendor['vendoruuid']
                test_data['vendor']['accountStatus'] = True
                break
        else:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")

    @pytestrail.case(686778)
    def test_03_retrieve_all_vendor_details(self, verification, config, test_data, rest_ship):
        """
        Retrieve details of the Vendor
        :param verification:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data = verification.vendor_management_data
        _url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor")
        _content = rest_ship.send_request(method="GET", url=_url, auth="crew").content
        test_data['vendor']['vendors'] = _content['vendor']
        for _key in _ship_data:
            for vendors in test_data['vendor']['vendors']:
                is_key_there_in_dict(_key, vendors)

    @pytestrail.case(700724)
    def test_04_retrieve_vendor_details(self, config, test_data, rest_ship):
        """
        To get and verify account settelment for individual slot
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['slotBalance'] = False
        if not test_data['vendor']['accountStatus']:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {"voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty vendor list"
        for _vendor in _content:
            if _vendor['accountstatus'] not in test_data['vendor']['accountstatus'] and _vendor['balance'] > 0:
                test_data['vendor']['vendor_uuid_settle'] = _vendor['vendoruuid']
                vendor_uuid = test_data['vendor']['vendor_uuid_settle']
                url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f'vendor/details/{vendor_uuid}')
                params = {'voyagenumber': test_data['voyageNumber']}
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                for activity in _content['activities']:
                    acti_date = datetime.strptime(activity['activitydate'], "%m/%d/%Y").strftime('%Y-%m-%d')
                    activity_date = change_epoch_time(acti_date)
                    if activity_date <= test_data['vendor']['current_date']:
                        for slot in activity['slot']:
                            is_key_there_in_dict("activityslotid", slot)
                            is_key_there_in_dict("activityid", slot)
                            is_key_there_in_dict("activityslotid", slot)
                            if test_data['vendor']['current_time'] > slot['enddate']:
                                if slot['balanceamount'] > 0 and slot['accountstatus'] not in test_data['vendor'][
                                    'accountstatus']:
                                    test_data['vendor']['activityid_settle'] = slot['activityid']
                                    test_data['vendor']['activityslotid_settle'] = slot['activityslotid']
                                    test_data['slotBalance'] = True
                                    return
        else:
            pytest.skip(msg='no slots are available for settlement')

    @pytestrail.case(24892232)
    def test_05_initiate_settle_account(self, config, test_data, rest_ship):
        """
        Initiate Settle Account of individual slot
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settlement/initiate")
        body = {
            "vendoruuid": test_data['vendor']['vendor_uuid_settle'], "activity":
                [
                    {"activityuuid": test_data['vendor']['activityid_settle'],
                     "activityslotuuid": [test_data['vendor']['activityslotid_settle']]
                     }
                ], "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('mediaitemid', _content)
        is_key_there_in_dict('Message', _content)
        if _content['Message'] != 'Success' and _content['mediaitemid'] is None:
            raise Exception("Settle account request is not initiated successfully")
        else:
            test_data['vendor']['mediaitemid'] = _content['mediaitemid']

    @pytestrail.case(68852209)
    def test_06_individual_settle_account_pdf(self, config, test_data, rest_ship):
        """
        To verify Settling Accounts PDF for individual activity downloaded successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'),
                      f"mediaitems/{test_data['vendor']['mediaitemid']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Settling Accounts PDF for individual activity not downloaded successfully !!')
        allure.attach(_content, attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(24892234)
    def test_07_send_for_approval(self, config, test_data, rest_ship):
        """
        Send for Approval
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settlement/sendforapproval")
        body = {"mediaitemid": test_data['vendor']['mediaitemid'], "acknowledgedbyvendor": True,
                "emailacknowledgement": True, "vendoruuid": test_data['vendor']['vendor_uuid_settle'], "activity":
                    [{"activityuuid": test_data['vendor']['activityid_settle'],
                      "activityslotuuid": [test_data['vendor']['activityslotid_settle']]}],
                "voyageNumber": test_data['voyageNumber']
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('Message', _content)
        if _content['Message'] != 'Success':
            raise Exception("Settle account request is not approved successfully")

    @pytestrail.case(33612352)
    def test_08_reject_pending_approval(self, config, test_data, rest_ship):
        """
        Reject the invoice from pending approval
        :param rest_ship:
        :param config:
        :param test_data:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/activityslot/reject")
        body = {"activityslotids": [test_data['vendor']['activityslotid_settle']],
                "customdescription": "Arrangements for the activities was not as promised",
                "voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict("Message", _content)
        if not _content['Message'] == "Activity Slot Rejected":
            raise Exception("Failed to reject the vendor pending approval")

    @pytestrail.case(28520856)
    def test_09_adjust_amount(self, config, test_data, rest_ship):
        """
        To verify user is able to adjust individual slot amount
        :param config:
        :param test_data:
        :param rest_ship:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settlement/adjustamount")
        body = {
            "vendoruuid": test_data['vendor']['vendor_uuid_settle'],
            "activityuuid": test_data['vendor']['activityid_settle'],
            "activityslotid": test_data['vendor']['activityslotid_settle'],
            "description": "Sailor did not find value in the Shore Thing.",
            "amount": "50", "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content

    @pytestrail.case(28521463)
    def test_10_sign_and_approve(self, config, test_data, rest_ship):
        """
        To verify user is able to sign and approve
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/activityslot/signandapprove")
        body = {"activityslotid": test_data['vendor']['activityslotid_settle'],
                "voyageNumber": test_data['voyageNumber']
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict("Message", _content)
        if _content['Message'] == "ActivitySlot SETTLED":
            pass
        else:
            raise Exception("Failed to sign and approve the vendor account")

    @pytestrail.case(27856113)
    def test_11_match_vendor_account_balance(self, config, test_data, rest_ship):
        """
        verify total account balance of vendor list and vendor details page
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {"voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty vendor list"
        for _vendor in _content:
            is_key_there_in_dict("accountstatus", _vendor)
            is_key_there_in_dict("balance", _vendor)
            if _vendor['accountstatus'] != 'SETTLED':
                if _vendor['balance'] > 0:
                    test_data['vendor']['vendor_uuid'] = _vendor['vendoruuid']
                    _vendor_uuid = _vendor['vendoruuid']
                    test_data['vendor']['balance'] = _vendor['balance']
                    url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f'vendor/details/{_vendor_uuid}')
                    params = {'voyagenumber': test_data['voyageNumber']}
                    _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                    if "{:.2f}".format(test_data['vendor']['balance']) == str(_content['balance']) or "{:.1f}".format(test_data['vendor']['balance']) == str(_content['balance']):
                        break
                    else:
                        raise Exception("account balance does not matched")
        else:
            pytest.skip(msg="skipped there are no unsettled accounts")

    @pytestrail.case(27856114)
    def test_12_retrieve_vendor_details(self, config, test_data, rest_ship):
        """
        To get and settle all account
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['slotBalance'] = False
        if not test_data['vendor']['accountStatus']:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {"voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty vendor list"
        for _vendor in _content:
            if _vendor['accountstatus'] not in test_data['vendor']['accountstatus'] and _vendor['balance'] > 0:
                test_data['vendor']['vendor_uuid_settle_all'] = _vendor['vendoruuid']
                vendor_uuid = test_data['vendor']['vendor_uuid_settle_all']
                url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f'vendor/details/{vendor_uuid}')
                params = {'voyagenumber': test_data['voyageNumber']}
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                for activity in _content['activities']:
                    acti_date = datetime.strptime(activity['activitydate'], "%m/%d/%Y").strftime('%Y-%m-%d')
                    activity_date = change_epoch_time(acti_date)
                    if activity_date <= test_data['vendor']['current_date']:
                        for slot in activity['slot']:
                            is_key_there_in_dict("activityslotid", slot)
                            is_key_there_in_dict("activityid", slot)
                            is_key_there_in_dict("activityslotid", slot)
                            if test_data['vendor']['current_time'] > slot['enddate']:
                                test_data['vendor']['activity_slot_ids'] = []
                                if slot['balanceamount'] > 0 and slot['accountstatus'] not in test_data['vendor'][
                                    'accountstatus']:
                                    test_data['vendor']['activity_slot_ids'].append(slot['activityslotid'])
                                    test_data['vendor']['activityid_settle_all'] = slot['activityid']
                                    test_data['vendor']['activityslotid_settle_all'] = slot['activityslotid']
                                    test_data['slotBalance'] = True
                                    return
        else:
            pytest.skip(msg='no slots are available for settlement')

    @pytestrail.case(24892233)
    def test_13_initiate_settle_all_accounts(self, config, test_data, rest_ship):
        """
        Initiate Settle All Account
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settlement/initiateallactivities")
        body = {"vendoruuid": test_data['vendor']['vendor_uuid_settle_all'],
                "activitySlotIds": test_data['vendor']['activity_slot_ids'], "voyageNumber": test_data['voyageNumber']
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        is_key_there_in_dict('mediaitemid', _content)
        is_key_there_in_dict('Message', _content)
        if _content['Message'] != 'Success' and _content['mediaitemid'] is None:
            raise Exception("Settle all account request is not initiated successfully")
        else:
            test_data['vendor']['mediaitemid'] = _content['mediaitemid']

    @pytestrail.case(68852210)
    def test_14_settle_all_accounts_pdf(self, config, test_data, rest_ship):
        """
        To verify Settling Accounts PDF for all activities downloaded successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg="skipped, there is no unsettled accounts in vendor list")
        url = urljoin(getattr(config.ship.contPath, 'embarkationServiceBaseAddress'),
                      f"mediaitems/{test_data['vendor']['mediaitemid']}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception(f'Settling Accounts PDF for all activities not downloaded successfully !!')
        allure.attach(_content, attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(24892235)
    def test_15_send_all_for_approval(self, config, test_data, rest_ship):
        """
        Send All for Approval
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['slotBalance']:
            pytest.skip(msg='slots with zero balance cannot be settled or no unsettled account available')
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/settlement/sendforapprovalallactivities")
        body = {"vendoruuid": test_data['vendor']['vendor_uuid_settle_all'],
                "mediaitemid": test_data['vendor']['mediaitemid'],
                "voyageNumber": test_data['voyageNumber']
                }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        is_key_there_in_dict('Message', _content)
        if _content['Message'] != 'Success':
            raise Exception("Settle all account request is not approved successfully")

    @pytestrail.case(11777732)
    def test_16_settlement_filter(self, verification, config, test_data, rest_ship):
        """
        Settlement Filter
        :param verification:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data = verification.vendor_management_data
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {
            "vendorsettlementstatus": ["SETTLED"], "vendorpaymentterm": [],
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for vendor in _content:
                for _key in _ship_data:
                    is_key_there_in_dict(_key, vendor)
                if vendor['accountstatus'] != 'SETTLED':
                    raise Exception("Settlement filter is not working")

    @pytestrail.case(11777733)
    def test_17_payment_term_filter(self, verification, config, test_data, rest_ship):
        """
        Payment Term Filter
        :param verification:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data = verification.vendor_management_data
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {
                "voyageNumber": test_data['voyageNumber']
                }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for vendor in _content:
                for _key in _ship_data:
                    is_key_there_in_dict(_key, vendor)
                if vendor['paymentterm'] != 'By The End of Voyage':
                    raise Exception("Payment Term filter is not working")

    @pytestrail.case(28469012)
    def test_18_log_complaint(self, config, test_data, rest_ship):
        """
        To verify user is able to log complaint for the vendor activity
        :param config:
        :param test_data:
        :param rest_ship:
        """
        test_data['vendor']['search_slot'] = False
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/list")
        body = {"voyageNumber": test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert len(_content) != 0, "empty vendor list"
        for _vendor in _content:
            if _vendor['accountstatus'] != 'SETTLED':
                test_data['vendor']['vendor_uuid_log'] = _vendor['vendoruuid']
                vendor_uuid = test_data['vendor']['vendor_uuid_log']
                url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f'vendor/details/{vendor_uuid}')
                params = {'voyagenumber': test_data['voyageNumber']}
                _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
                if _content['activities'] is not None:
                    for activity in _content['activities']:
                        for slot in activity['slot']:
                            is_key_there_in_dict("activityslotid", slot)
                            is_key_there_in_dict("activityid", slot)
                            is_key_there_in_dict("activityslotid", slot)
                            test_data['vendor']['activity_slot_ids_log'] = slot['activityslotid']
                            test_data['vendor']['activityid_log'] = slot['activityid']
                            test_data['vendor']['activityslotid_log'] = slot['activityslotid']
                            test_data['vendor']['search_slot'] = True
                            return
                else:
                    continue
                break
        if not test_data['vendor']['search_slot']:
            pytest.skip(msg="skipped no slots available to log complaint")
        _url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/initiatelogcomplaint")
        body = {"activityslotid": test_data['vendor']['activityslotid_log']}
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        test_data['vendor']['activityPersonBookingId'] = _content[0]['activityPersonBookingId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/vendor/complaint")
        body = {
            "activitypersonbookingid": test_data['vendor']['activityPersonBookingId'],
            "activityslotid": test_data['vendor']['activityslotid_log'],
            "activityuuid": test_data['vendor']['activityid_log'],
            "description": "Activity was not worth that I have paid for.",
            "vendoruuid": test_data['vendor']['vendor_uuid_log'],
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content

    @pytestrail.case(68043512)
    def test_19_create_notification_template(self, config, test_data, rest_ship):
        """
        To verify New Notification Template created successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['account'] = {}
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codevalues")
        body = {"codeTypeCode": "NT", "nameKey": "notificationTemplate", "descriptionKey": None,
                "template":
                    {"title": title, "body": description,
                     "url": "https://application-integration.ship.virginvoyages.com/activityReservationCrew/settings"}}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['account']['code'] = _content['code']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codetypes/search")
        body = {"codes": ["NT"], "codeValuesRequired": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        template = _content[0]['codeValues']
        flag = 1
        for activity in template:
            if activity['code'] == test_data['account']['code']:
                flag = 0
                logger.info('New Notification Template created successfully')
        if flag:
            raise Exception('New Notification Template not created successfully')

    @pytestrail.case(68043544)
    def test_20_edit_notification_template(self, config, test_data, rest_ship):
        """
        To verify Notification Template edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": "notificationTemplate",
                "template":
                    {"title": title, "body": description, "url": "https://www.google.com/"}}
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        assert len(_content) != 0, 'Notification Template not edited successfully'

    @pytestrail.case(68043545)
    def test_21_delete_notification_template(self, config, test_data, rest_ship):
        """
        To verify Notification Template deleted successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": "notificationTemplate", "isDeleted": True}
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        assert len(_content) != 0, 'Notification Template not deleted successfully'

    @pytestrail.case(68043546)
    def test_22_create_activity_ship(self, config, test_data, rest_ship):
        """
        To verify New Activity/Meeting Location for Shipboard created successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codevalues")
        body = {"codeTypeCode": "SPV", "nameKey": title,
                "descriptionKey": description, "template": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['account']['code'] = _content['code']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codetypes/search")
        body = {"codes": ["SPV"], "codeValuesRequired": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        template = _content[0]['codeValues']
        flag = 1
        for activity in template:
            if activity['code'] == test_data['account']['code']:
                flag = 0
                logger.info('New Activity/Meeting Location for Shipboard created successfully')
        if flag:
            raise Exception('New Activity/Meeting Location not created successfully')

    @pytestrail.case(68043682)
    def test_23_edit_activity_ship(self, config, test_data, rest_ship):
        """
        To verify Activity/Meeting Location for Shipboard edited successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": title, "descriptionKey": description}
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        test_data['account']['nameKey'] = _content['nameKey']
        assert len(_content) != 0, 'Activity/Meeting Location not edited successfully'

    @pytestrail.case(68043683)
    def test_24_delete_activity_ship(self, config, test_data, rest_ship):
        """
        To verify Activity/Meeting Location for Shipboard deleted successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": test_data['account']['nameKey'], "isDeleted": True}
        _content = rest_ship.send_request(method="PATCH", url=url, json=body, auth="crew").content
        assert len(_content) != 0, 'Activity/Meeting Location not deleted successfully'

    @pytestrail.case(68043684)
    def test_25_create_activity_shore(self, config, test_data, rest_shore):
        """
        To verify New Activity/Meeting Location for Shore Side created successfully
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        test_data['account'] = {}
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codevalues")
        body = {"codeTypeCode": "SRV", "nameKey": title,
                "descriptionKey": description, "template": None}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="crew").content
        test_data['account']['code'] = _content['code']
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/codetypes/search")
        body = {"codes": ["SRV"], "codeValuesRequired": True}
        _content = rest_shore.send_request(method="POST", url=url, json=body, auth="crew").content
        template = _content[0]['codeValues']
        flag = 1
        for activity in template:
            if activity['code'] == test_data['account']['code']:
                flag = 0
                logger.info('New Activity/Meeting Location for Shore Side created successfully')
        if flag:
            raise Exception('New Activity/Meeting Location not created successfully')

    @pytestrail.case(68043685)
    def test_26_edit_activity_shore(self, config, test_data, rest_shore):
        """
        To verify Activity/Meeting Location for Shore Side edited successfully
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": title, "descriptionKey": description}
        _content = rest_shore.send_request(method="PATCH", url=url, json=body, auth="crew").content
        test_data['account']['nameKey'] = _content['nameKey']
        assert len(_content) != 0, 'Activity/Meeting Location not edited successfully'

    @pytestrail.case(68044922)
    def test_27_delete_activity_shore(self, config, test_data, rest_shore):
        """
        To verify Activity/Meeting Location for Shore Side deleted successfully
        :param config:
        :param test_data:
        :param rest_shore:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), f"/{test_data['account']['code']}")
        body = {"nameKey": test_data['account']['nameKey'], "isDeleted": True}
        _content = rest_shore.send_request(method="PATCH", url=url, json=body, auth="crew").content
        assert len(_content) != 0, 'Activity/Meeting Location not deleted successfully'
