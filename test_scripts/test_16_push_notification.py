__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.PUSH_NOTIFICATION
@pytest.mark.run(order=17)
class TestPushNotification:
    """
    Test Suite to test Push Notification
    """

    @pytestrail.case(31611532)
    def test_01_user_role(self, config, rest_ship):
        """
        Get User role
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'), "userroles")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('applicationFeatures', _content)
            is_key_there_in_dict('applicationRoles', _content)
            for applicationFeature in _content['applicationFeatures']:
                is_key_there_in_dict('applicationFeatureId', applicationFeature)
                is_key_there_in_dict('name', applicationFeature)
                is_key_there_in_dict('code', applicationFeature)
            for applicationRole in _content['applicationRoles']:
                is_key_there_in_dict('applicationRoleId', applicationRole)
                is_key_there_in_dict('name', applicationRole)
                is_key_there_in_dict('code', applicationRole)
        else:
            logger.warn("No roles assigned to crew")

    @pytestrail.case(31611534)
    def test_02_recipient_type(self, config, rest_ship, test_data):
        """
        Get Recipient Type
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        test_data['pushNotification'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/recipienttype")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for recipient in _content:
                is_key_there_in_dict('id', recipient)
                is_key_there_in_dict('label', recipient)
                if recipient['label'] == 'sailor':
                    test_data['pushNotification']['recipientId'] = recipient['id']
        else:
            raise Exception('No recipient type found!')

    @pytestrail.case(31611535)
    def test_03_team_member_search(self, config, test_data, rest_ship, verification):
        """
        Search Team Member
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        test_data['crewData'] = dict()
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "teammembers/search/findbysearchparameters")
        params = {'size': 100}
        body = {'teamMemberIds': [test_data['personId']]}
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('teammembers', _content['_embedded'])
            if len(_content['_embedded']['teammembers']) != 0:
                for teammember in _content['_embedded']['teammembers']:
                    test_data['crewData']['firstName'] = teammember['firstName']
                    test_data['crewData']['lastName'] = teammember['lastName']
            else:
                raise Exception('No crew data found!')
        else:
            raise Exception('No crew data found!')

    @pytestrail.case(31611536)
    def test_04_find_duty_locations(self, config, rest_ship):
        """
        Find Duty Locations
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "teammembers/search/finddutylocation")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('dutyLocations', _content)
        else:
            logger.warn("Duty location not found")

    @pytestrail.case(31612963)
    def test_05_template_type(self, config, rest_ship, test_data):
        """
        Get Template Type
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notificationtemplatetype")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            test_data['pushNotification']['notificationTemplateType'] = _content
        else:
            raise Exception('No template type found!')

    @pytestrail.case(31612964)
    def test_06_template_category(self, config, rest_ship, test_data):
        """
        Get Template Category
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notificationtemplatecategory")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for template_category in _content:
                is_key_there_in_dict('id', template_category)
                is_key_there_in_dict('label', template_category)
            test_data['pushNotification']['notificationTemplateCategory'] = _content
        else:
            raise Exception('No template category found!')

    @pytestrail.case(31612965)
    def test_07_create_template(self, config, rest_ship, test_data, guest_data):
        """
        Create Template
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notificationtemplate")
        body = {"name": f"Template for {guest_data[0]['FirstName']}",
                "title": "Push Notification Template", "body": "Push Notification Template",
                "type": test_data['pushNotification']['notificationTemplateType'][0],
                "categoryId": test_data['pushNotification']['notificationTemplateCategory'][0]['id']}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('id', _content)
            is_key_there_in_dict('type', _content)
            is_key_there_in_dict('ownerId', _content)
            is_key_there_in_dict('name', _content)
            is_key_there_in_dict('categoryId', _content)
            is_key_there_in_dict('title', _content)
            is_key_there_in_dict('body', _content)
            assert _content['name'] == f"Template for {guest_data[0]['FirstName']}", "Template not matched"
            test_data['pushNotification']['templateId'] = _content['id']
        else:
            raise Exception('template not created!')

    @pytestrail.case(31612966)
    def test_08_verify_created_templates(self, config, rest_ship, test_data):
        """
        Verify Created Templates
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notificationtemplates")
        params = {'page': 0, 'size': 99999}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for template in _content['content']:
                    is_key_there_in_dict('id', template)
                    is_key_there_in_dict('type', template)
                    is_key_there_in_dict('ownerId', template)
                    is_key_there_in_dict('name', template)
                    is_key_there_in_dict('categoryId', template)
                    is_key_there_in_dict('title', template)
                    is_key_there_in_dict('body', template)
                    if template['id'] == test_data['pushNotification']['templateId']:
                        _status = True
                assert _status, "Created template not found in the list!"
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No template found!')

    @pytestrail.case(31612967)
    def test_09_get_slots(self, config, rest_ship, test_data):
        """
        Get Slots
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "slots")
        params = {'shipcode': config.ship.code, 'embarkDate': test_data['embarkDate']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for slot in _content:
                is_key_there_in_dict('slotNumber', slot)
                is_key_there_in_dict('startTime', slot)
                is_key_there_in_dict('endTime', slot)
                is_key_there_in_dict('status', slot)
                is_key_there_in_dict('reserved', slot)
        else:
            raise Exception('No slot found!')

    @pytestrail.case(31612968)
    def test_10_get_guest_types(self, config, rest_ship):
        """
        Get Guest Types
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "guesttypes")
        params = {'size': 1500, 'sort': 'name', 'parts': 'name,isDeleted,code,guestTypeId'}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('guesttypes', _content['_embedded'])
            if len(_content['_embedded']['guesttypes']) != 0:
                for _type in _content['_embedded']['guesttypes']:
                    is_key_there_in_dict('guestTypeId', _type)
                    is_key_there_in_dict('name', _type)
                    is_key_there_in_dict('isDeleted', _type)
                    is_key_there_in_dict('code', _type)
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No guest type found!')

    @pytestrail.case(31612969)
    def test_11_get_departments(self, config, rest_ship):
        """
        Get Departments
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "departments")
        params = {'size': 500, 'sort': 'name', 'parts': 'name,isDeleted,code,departmentId'}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('departments', _content['_embedded'])
            if len(_content['_embedded']['departments']) != 0:
                for _type in _content['_embedded']['departments']:
                    is_key_there_in_dict('departmentId', _type)
                    is_key_there_in_dict('name', _type)
                    is_key_there_in_dict('isDeleted', _type)
                    is_key_there_in_dict('code', _type)
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No department found!')

    @pytestrail.case(31612970)
    def test_12_get_duties(self, config, rest_ship):
        """
        Get Duties
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "duties")
        params = {'size': 100, 'page': 0, 'parts': 'dutyName,dutyId'}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('duties', _content['_embedded'])
            if len(_content['_embedded']['duties']) != 0:
                for _type in _content['_embedded']['duties']:
                    is_key_there_in_dict('dutyId', _type)
                    is_key_there_in_dict('dutyName', _type)
                    is_key_there_in_dict('isDeleted', _type)
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No duty found!')

    @pytestrail.case(31612971)
    def test_13_get_activity_group(self, config, rest_ship):
        """
        Get Activity Group
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.ars'), "/activitygroups")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for activityGroup in _content:
                is_key_there_in_dict('activityGroupId', activityGroup)
                is_key_there_in_dict('groupCode', activityGroup)
                is_key_there_in_dict('isDeleted', activityGroup)
                is_key_there_in_dict('subActivityGroups', activityGroup)
        else:
            raise Exception('Activity Group data does not exist')

    @pytestrail.case(31612972)
    def test_14_get_distribution_list_users(self, config, rest_ship, test_data):
        """
        Get Distribution List users
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/distributionlistUsers")
        params = {'size': 9999, 'page': 0, 'voyagenumber': test_data['voyageNumber']}
        body = [{"filter": {"cabin": [test_data['cabinNumber']]},
                 "recipientTypeId": test_data['pushNotification']['recipientId']}]
        _content = rest_ship.send_request(method="POST", url=url, params=params, json=body, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('content', _content)
            if len(_content['content']) != 0:
                for distributionlistUser in _content['content']:
                    is_key_there_in_dict('recipientTypeId', distributionlistUser)
                    is_key_there_in_dict('name', distributionlistUser)
                    is_key_there_in_dict('personId', distributionlistUser)
                    is_key_there_in_dict('personTypeCode', distributionlistUser)
                    is_key_there_in_dict('cabin', distributionlistUser)
                test_data['pushNotification']['distributionListUsers'] = _content['content']
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No distribution list user found!')

    @pytestrail.case(31612973)
    def test_15_create_distribution_list(self, config, rest_ship, test_data, guest_data):
        """
        Create Distribution List
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        number = four_digit_random_number()
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/distributionlist")
        body = {
            "filter": {
                "cabin": [test_data['cabinNumber']]
            },
            "recipientTypeId": test_data['pushNotification']['recipientId'],
            "name": f"Distribution List for {guest_data[0]['FirstName']}{number}",
            "type": test_data['pushNotification']['notificationTemplateType'][0],
            "members": test_data['pushNotification']['distributionListUsers'],
            "voyageNumber": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('id', _content)
            is_key_there_in_dict('type', _content)
            is_key_there_in_dict('ownerId', _content)
            is_key_there_in_dict('name', _content)
            is_key_there_in_dict('recipientTypeId', _content)
            is_key_there_in_dict('voyageNumber', _content)
            is_key_there_in_dict('filter', _content)
            is_key_there_in_dict('members', _content)
            test_data['pushNotification']['distributionList'] = _content
            assert _content['name'] == f"Distribution List for {guest_data[0]['FirstName']}{number}", "DL not matched!"
        else:
            raise Exception('No distribution list created!')

    @pytest.mark.xfail(reason="DCP-114159")
    @retry_when_fails(retries=5, interval=5)
    @pytestrail.case(31612974)
    def test_16_verify_distribution_list(self, config, rest_ship, test_data):
        """
        Verify Distribution List
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/distributionlists")
        params = {'size': 10}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            is_key_there_in_dict('content', _content)
            _status = False
            if len(_content['content']) != 0:
                for distributionlist in _content['content']:
                    is_key_there_in_dict('id', distributionlist)
                    is_key_there_in_dict('type', distributionlist)
                    is_key_there_in_dict('ownerId', distributionlist)
                    is_key_there_in_dict('name', distributionlist)
                    is_key_there_in_dict('recipientTypeId', distributionlist)
                    is_key_there_in_dict('filter', distributionlist)
                    if distributionlist['id'] == test_data['pushNotification']['distributionList']['id']:
                        _status = True
                        break
                assert _status, "Created distribution list not found in the list"
            else:
                raise Exception('No data found!')
        else:
            raise Exception('No distribution list found!')

    @pytestrail.case(31612975)
    def test_17_get_distribution_list_type(self, config, rest_ship, test_data):
        """
        Get Distribution List Type
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/distributionlisttype")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            test_data['pushNotification']['distributionListType'] = _content
        else:
            raise Exception('No distribution list type found!')

    @pytestrail.case(31612976)
    def test_18_send_notification(self, config, rest_ship, test_data, verification):
        """
        Send Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notification")
        body = {"freeForm": True, "repeatDaily": False,
                "notificationTemplateId": test_data['pushNotification']['templateId'], "params": [],
                "title": "Sample e2e testing for Sent Notification", "voyageNumber": test_data['voyageNumber'],
                "scheduledTime": f"{test_data['embarkDate']}T00:01:01", "itineraryDay": 1,
                "distributionList": [{"filter": {"cabin": [test_data['cabinNumber']]},
                                      "recipientTypeId": test_data['pushNotification']['recipientId']}],
                "members": test_data['pushNotification']['distributionListUsers'], "draft": False,
                "ownerName": f"{test_data['crewData']['firstName']} {test_data['crewData']['lastName']}",
                "ownerDesignation": "Terminal Coordinator", "ownerLocation": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            test_data['pushNotification']['sentNotificationId'] = _content['id']
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
            for distribution_list in _content["distributionList"]:
                for _key in verification.notification['distributionList']:
                    is_key_there_in_dict(_key, distribution_list)
            for member in _content["members"]:
                for _key in verification.notification['members']:
                    is_key_there_in_dict(_key, member)
            test_data['pushNotification']['sentNotification'] = _content
        else:
            raise Exception("Notification not created")

    @pytestrail.case(31612977)
    def test_19_verify_sent_notification(self, config, rest_ship, test_data, verification):
        """
        Verify Sent Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['sentNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
            for distribution_list in _content["distributionList"]:
                for _key in verification.notification['distributionList']:
                    is_key_there_in_dict(_key, distribution_list)
            for member in _content["members"]:
                for _key in verification.notification['members']:
                    is_key_there_in_dict(_key, member)
        else:
            raise Exception("Notification not found")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(31612978)
    def test_20_get_sent_notifications(self, test_data, config, rest_ship):
        """
        Get Sent Notifications
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/sentnotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'size': 10}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        for count in range(0, len(_content['content'])):
            if _content['content'][count]['id'] == test_data['pushNotification']['sentNotificationId']:
                break
        else:
            raise Exception("sent message not coming on dashboard")

    @pytestrail.case(31612979)
    def test_21_search_sent_notifications(self, test_data, config, rest_ship, verification):
        """
        Search Sent Notifications
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/sentnotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999,
                  'search': 'Sample e2e testing for Sent Notification'}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict(_key, notification)
                    for distribution_list in notification["distributionList"]:
                        for _key in verification.notification['distributionList']:
                            is_key_there_in_dict(_key, distribution_list)
                    for member in notification["members"]:
                        for _key in verification.notification['members']:
                            is_key_there_in_dict(_key, member)
                    if notification['title'] == 'Sample e2e testing for Sent Notification':
                        _status = True
                assert _status, "Sent notification not found in the search results"
            else:
                raise Exception("No data found")
        else:
            raise Exception("No notification found in search results")

    @pytestrail.case(31612980)
    def test_22_sent_notifications_pdf(self, test_data, config, rest_ship):
        """
        Sent Notifications PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/sentnotifications/pdf")
        params = {'voyagenumber': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('Byte Array Not Received !!')
        allure.attach(_content, name='sent_notifications.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(31612981)
    def test_23_sent_notifications_csv(self, test_data, config, rest_ship):
        """
        Sent Notifications CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/sentnotifications/excel")
        params = {'voyagenumber': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('Byte Array Not Received !!')
        allure.attach(_content, name='sent_notifications.csv', attachment_type=allure.attachment_type.CSV)

    @pytestrail.case(31612982)
    def test_24_delete_sent_notification(self, config, rest_ship, test_data, verification):
        """
        Delete Sent Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['sentNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        rest_ship.send_request(method="DELETE", url=url, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/sentnotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 10}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict('id', notification)
                    if notification['id'] == test_data['pushNotification']['sentNotification']['id']:
                        _status = True
                assert not _status, "Sent notification not deleted successfully"
            else:
                raise Exception('No data found !!')
        else:
            logger.warn("No sent notification found")

    @pytestrail.case(31612983)
    def test_25_schedule_notification(self, config, rest_ship, test_data, verification):
        """
        Schedule Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notification")
        body = {"freeForm": True, "repeatDaily": False,
                "notificationTemplateId": test_data['pushNotification']['templateId'], "params": [],
                "title": "Sample e2e testing for Scheduled Notification", "voyageNumber": test_data['voyageNumber'],
                "scheduledTime": f"{test_data['debarkDate']}T23:59:59", "itineraryDay": 5,
                "distributionList": [{"filter": {"cabin": [test_data['cabinNumber']]},
                                      "recipientTypeId": test_data['pushNotification']['recipientId']}],
                "members": test_data['pushNotification']['distributionListUsers'], "draft": False,
                "ownerName": f"{test_data['crewData']['firstName']} {test_data['crewData']['lastName']}",
                "ownerDesignation": "Terminal Coordinator", "ownerLocation": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
            test_data['pushNotification']['scheduledNotification'] = _content
        else:
            raise Exception("notification not scheduled")

    @pytestrail.case(31613741)
    def test_26_verify_scheduled_notification(self, config, rest_ship, test_data, verification):
        """
        Verify Created Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['scheduledNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
        else:
            raise Exception("notification not found")

    @pytest.mark.xfail(reason="DCP-114159")
    @pytestrail.case(31613742)
    def test_27_get_scheduled_notifications(self, test_data, config, rest_ship, verification):
        """
        Get Scheduled Notifications
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/schedulednotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict(_key, notification)
                    if notification['id'] == test_data['pushNotification']['scheduledNotification']['id']:
                        _status = True
                        break
                assert _status, "Scheduled notification not present in the list"
            else:
                raise Exception('No data found !!')
        else:
            raise Exception("No scheduled notification found on dashboard")

    @pytestrail.case(31613743)
    def test_28_search_scheduled_notifications(self, test_data, config, rest_ship, verification):
        """
        Search Scheduled Notifications
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/schedulednotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999,
                  'search': 'Sample e2e testing for Scheduled Notification'}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict(_key, notification)
                    if notification['title'] == 'Sample e2e testing for Scheduled Notification':
                        _status = True
                assert _status, "Scheduled notification not present in the search results"
            else:
                raise Exception('No data found !!')
        else:
            raise Exception("No scheduled notification found in search results")

    @pytestrail.case(31613744)
    def test_29_scheduled_notifications_pdf(self, test_data, config, rest_ship):
        """
        Scheduled Notifications PDF
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/schedulednotifications/pdf")
        params = {'voyagenumber': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('Byte Array Not Received !!')
        allure.attach(_content, name='scheduled_notifications.pdf', attachment_type=allure.attachment_type.PDF)

    @pytestrail.case(31613745)
    def test_30_scheduled_notifications_csv(self, test_data, config, rest_ship):
        """
        Scheduled Notifications CSV
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/schedulednotifications/excel")
        params = {'voyagenumber': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if not isinstance(_content, bytes):
            raise Exception('Byte Array Not Received !!')
        allure.attach(_content, name='scheduled_notifications.csv', attachment_type=allure.attachment_type.CSV)

    @pytest.mark.xfail(reason="DCP-114159")
    @pytestrail.case(31613746)
    def test_31_delete_scheduled_notification(self, config, rest_ship, test_data, verification):
        """
        Delete Scheduled Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['scheduledNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        rest_ship.send_request(method="DELETE", url=url, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/schedulednotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict(_key, notification)
                    if notification['id'] == test_data['pushNotification']['scheduledNotification']['id']:
                        _status = True
                        break
                assert not _status, "Scheduled notification not deleted successfully"
            else:
                raise Exception('No data found !!')
        else:
            logger.warn("No schedule notification found")

    @pytestrail.case(31613747)
    def test_32_draft_notification(self, config, rest_ship, test_data, verification):
        """
        Draft Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/notification")
        body = {"freeForm": True, "repeatDaily": False,
                "notificationTemplateId": test_data['pushNotification']['templateId'], "params": [],
                "title": "Sample e2e testing for Draft Notification", "voyageNumber": test_data['voyageNumber'],
                "scheduledTime": f"{test_data['embarkDate']}T00:02:02", "itineraryDay": 1,
                "distributionList": [{"filter": {"cabin": [test_data['cabinNumber']]},
                                      "recipientTypeId": test_data['pushNotification']['recipientId']}],
                "members": test_data['pushNotification']['distributionListUsers'], "draft": True,
                "ownerName": f"{test_data['crewData']['firstName']} {test_data['crewData']['lastName']}",
                "ownerDesignation": "Terminal Coordinator", "ownerLocation": None}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
            test_data['pushNotification']['draftNotification'] = _content
        else:
            raise Exception("Notification not drafted")

    @pytestrail.case(31613748)
    def test_33_verify_draft_notification(self, config, rest_ship, test_data, verification):
        """
        Verify Draft Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['draftNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for _key in verification.notification:
                is_key_there_in_dict(_key, _content)
        else:
            raise Exception("Notification not found")

    @pytestrail.case(31613749)
    def test_34_get_draft_notifications(self, test_data, config, rest_ship, verification):
        """
        Get Draft Notifications
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/draftnotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict('id', notification)
                    if notification['id'] == test_data['pushNotification']['draftNotification']['id']:
                        _status = True
                assert _status, "Draft notification not present in the list"
            else:
                raise Exception('No data found !!')
        else:
            raise Exception("No Draft notification found on dashboard")

    @pytestrail.case(31613750)
    def test_35_delete_draft_notification(self, config, rest_ship, test_data, verification):
        """
        Delete Draft Notification
        :param verification:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _notification = test_data['pushNotification']['draftNotification']['id']
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), f"nm/notification/{_notification}")
        rest_ship.send_request(method="DELETE", url=url, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.messaging'), "nm/draftnotifications")
        params = {'voyagenumber': test_data['voyageNumber'], 'page': 0, 'size': 99999}
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['page']['totalElements'] != 0:
            _status = False
            if len(_content['content']) != 0:
                for notification in _content['content']:
                    for _key in verification.notification:
                        is_key_there_in_dict('id', notification)
                    if notification['id'] == test_data['pushNotification']['draftNotification']['id']:
                        _status = True
                assert not _status, "Draft notification not deleted successfully"
            else:
                raise Exception('No data found !!')
        else:
            logger.warn("No draft notification found")
