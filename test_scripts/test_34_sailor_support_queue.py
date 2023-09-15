__author__ = 'HT'

from virgin_utils import *


@pytest.mark.INTEGRATION
@pytest.mark.SAILOR_CREW_CHAT
@pytest.mark.run(order=36)
class TestSailorCrewChat:
    """
    Test Suite to check integration between sailor application and crew application
    """

    @pytestrail.case(26112983)
    def test_01_login(self, config, test_data, guest_data, rest_ship):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        test_data['sailorServices'] = dict()
        guest = guest_data[0]
        url = urljoin(config.ship.url, "user-account-service/signin/email")
        body = {
            "userName": guest['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

    @pytestrail.case(26152207)
    def test_02_get_support_queues(self, config, test_data, rest_ship):
        """
        Open sailor service to initiate chat
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/users/me/support_queue')
        params = {'voyage_number': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
            is_key_there_in_dict('sailor_iam_user_id', _content)
            is_key_there_in_dict('subject', _content)
            is_key_there_in_dict('status', _content)
            is_key_there_in_dict('loyalty', _content)
            is_key_there_in_dict('requires_attention', _content)
            is_key_there_in_dict('first_message_time', _content)
            is_key_there_in_dict('stream_id', _content)
            is_key_there_in_dict('voyage_number', _content)
            is_key_there_in_dict('resolved_at', _content)
            test_data['sailorServices']['id'] = _content['id']
        else:
            raise Exception("Sailor service not found in sailor application")

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(11968498)
    def test_03_send_request_to_crew(self, config, test_data, rest_ship):
        """
        To raise a request to sailor service(support-queue) from sailor application
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['message_from_sailor'] = ['hi..', 'hello..', 'need assistance', 'cabin tv is not working',
                                            'need your help.']
        _contents = random.choice(test_data['message_from_sailor'])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "queue_id": test_data['sailorServices']['id'],
            "content": _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
        else:
            raise Exception("Raising request to crew failed..")

    @pytestrail.case(11968499)
    def test_04_verify_the_new_request_received(self, config, test_data, rest_ship):
        """
        To verify the the new request from sailor is received at support queue application
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/list_v3')
        params = {
            'voyage_number': test_data['voyageNumber'],
            'owned_by_me': False,
            'sort_by': "created"
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        new_ids = []
        for new in _content['new']:
            is_key_there_in_dict('first_message_time', new)
            is_key_there_in_dict('id', new)
            is_key_there_in_dict('loyalty', new)
            is_key_there_in_dict('requires_attention', new)
            is_key_there_in_dict('sailor_iam_user_id', new)
            is_key_there_in_dict('status', new)
            is_key_there_in_dict('stream_id', new)
            is_key_there_in_dict('subject', new)
            is_key_there_in_dict('voyage_number', new)
            new_ids.append(new['id'])
        for chat_id in new_ids:
            if chat_id == test_data['sailorServices']['id']:
                break
        else:
            raise Exception(f"ID: {test_data['supportQueue']['queueId']} not found in new/pending !!")

    @pytestrail.case(11968501)
    def test_05_replay_to_sailor_request(self, config, test_data, rest_ship):
        """
        Replay to sailor request received
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['message_from_crew'] = ['hi..', 'hello..', 'how can i help you', 'thanks for raising request']
        _contents = random.choice(test_data['message_from_crew'])
        params = {
            "queue_id": test_data['sailorServices']['id'],
            "content": _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)

        else:
            raise Exception("Raising request to crew failed..")

    @pytestrail.case(26152209)
    def test_06_verify_request_in_progress(self, config, test_data, rest_ship):
        """
        To verify started attending to sailor request is appearing in in-progress request or not
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/list_v3')
        params = {
            'voyage_number': test_data['voyageNumber'],
            'owned_by_me': False,
            'sort_by': "created"
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        in_progress_ids = []
        for pending in _content['in_progress']:
            is_key_there_in_dict('first_message_time', pending)
            is_key_there_in_dict('id', pending)
            is_key_there_in_dict('loyalty', pending)
            is_key_there_in_dict('requires_attention', pending)
            is_key_there_in_dict('sailor_iam_user_id', pending)
            is_key_there_in_dict('status', pending)
            is_key_there_in_dict('stream_id', pending)
            is_key_there_in_dict('subject', pending)
            is_key_there_in_dict('voyage_number', pending)
            in_progress_ids.append(pending['id'])

        for chat_id in in_progress_ids:
            if chat_id == test_data['sailorServices']['id']:
                break
        else:
            raise Exception(f"ID: {test_data['supportQueue']['queueId']} not found in in-progress-pending !!")

    @pytestrail.case(11968500)
    def test_07_resolve_support_queue_messages(self, config, test_data, rest_ship):
        """
        To mark the Sailor Request Resolved in support queue
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/resolve')
        params = {
            'queue_id': test_data['sailorServices']['id']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        if len(_content) != 0:
            assert test_data['sailorServices']['id'] == _content['id'], "id mismatch !!"
            assert _content['status'] == 'resolved', "Request is not Resolved !!"
            assert _content['result'] == "success", "Result is not Success !!"
        else:
            raise Exception("Failed to resolve the request")

    @pytestrail.case(25279617)
    def test_08_send_request_to_crew(self, config, test_data, rest_ship):
        """
        To raise a request to sailor service from same chat id
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['message_to_same_id'] = ['hi..', 'can you do one more help', 'need water', 'need towel']
        _contents = random.choice(test_data['message_to_same_id'])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "queue_id": test_data['sailorServices']['id'],
            "content": _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        try:
            _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user")
            raise Exception('sailor is allowed to raise request in the resolved ticket')
        except Exception as exp:
            if 'This ticket has already been resolved' in exp.args[0]:
                pass
            else:
                raise Exception('sailor is allowed to raise request in the resolved ticket')

    @pytestrail.case(26152208)
    def test_09_get_support_queues(self, config, test_data, rest_ship):
        """
        Open sailor service to initiate chat chat again after crew resoles previous ticket
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/users/me/support_queue')
        params = {'voyage_number': test_data['voyageNumber']}
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
            is_key_there_in_dict('sailor_iam_user_id', _content)
            is_key_there_in_dict('subject', _content)
            is_key_there_in_dict('status', _content)
            is_key_there_in_dict('loyalty', _content)
            is_key_there_in_dict('requires_attention', _content)
            is_key_there_in_dict('first_message_time', _content)
            is_key_there_in_dict('stream_id', _content)
            is_key_there_in_dict('voyage_number', _content)
            is_key_there_in_dict('resolved_at', _content)
            test_data['sailorServices']['id'] = _content['id']
        else:
            raise Exception("Sailor service not found in sailor application")

    @pytestrail.case(25339114)
    def test_10_send_new_request_to_crew(self, config, test_data, rest_ship):
        """
        To raise a new request to sailor service from sailor application again after crew resoles previous ticket
        :param test_data:
        :param rest_ship:
        :param config:
        param test_data:
        :return:
        """
        test_data['new_sailor_request'] = ['hi..', 'hello.', 'need cabin cleaning', 'need AC', 'need water']
        _contents = random.choice(test_data['new_sailor_request'])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "queue_id": test_data['sailorServices']['id'],
            "content": _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        _content = None
        retries = 20
        while retries >= 0:
            try:
                _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
                break
            except (Exception, ValueError):
                retries -= 1

        if _content is None:
            raise Exception("Raising new request to crew failed..")

        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
        else:
            raise Exception("Raising new request to crew failed..")

    @pytestrail.case(26112984)
    def test_11_login(self, config, test_data, rest_ship):
        """
        Login to crew application using crew credentials who has permission to chat with sailor
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(config.ship.url, 'user-account-service/signin/username')
        body = {
            "userName": "vkholi01",
            "password": "Test@1234"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.crewToken = f"{str(_content['tokenType']).capitalize()} {_content['accessToken']}"

    @pytestrail.case(26152697)
    def test_12_search_for_sailor_on_crew_chat(self, config, guest_data, test_data, rest_ship):
        """
        Search for the on-boarded Sailor from crew chat module
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['sailorServices']['guestId'] = guest_data[0]['guestId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservationguests/search')
        body = {
            'reservationNumber': test_data['reservationNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        guest_cabinnumber = _content['_embedded']['reservationGuestDetailsResponses'][0]['reservationDetails'][0][
            'cabinNumber']
        assert guest_cabinnumber == test_data['cabinNumber'], 'Reserved Cabin number mismatched'

    @pytestrail.case(26154558)
    def test_13_get_iam_user_id(self, test_data, rest_ship, config):
        """
        To get the iam user id from guest id
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),
                       '/userprofiles/getuserdetails')
        params = {
            'personid': test_data['sailorServices']['guestId']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        test_data['sailorServices']['iam_userID'] = _content['userId']
        if len(_content) != 0:
            is_key_there_in_dict('userId', _content)
            is_key_there_in_dict('firstName', _content)
            is_key_there_in_dict('middleName', _content)
            is_key_there_in_dict('lastName', _content)
            is_key_there_in_dict('personTypeCode', _content)
            is_key_there_in_dict('personId', _content)
            is_key_there_in_dict('preferredName', _content)
            is_key_there_in_dict('userMediaItemId', _content)
        else:
            raise Exception('Received Empty response')

    @pytestrail.case(10770752)
    def test_14_send_private_message(self, test_data, rest_ship, config):
        """
        Sending a private message to the guest from crew application
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['_message_list'] = ["Good Afternoon", "Good Morning", "How can I help you", "Thank You!!", "Hii!!"]
        _contents = random.choice(test_data['_message_list'])
        params = {
            'type': 'private',
            'to': test_data['sailorServices']['iam_userID'],
            'content': _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('id', _content)
                test_data['sailorServices']['id'] = _content['id']
            else:
                raise Exception(f"ERROR: {_content['id']}")
        else:
            raise Exception("ERROR: No message data in response")

    @pytestrail.case(26154559)
    def test_15_get_contacts(self, test_data, rest_ship, config):
        """
        Search for the received crew message in sailor application messenger module
        :param test_data:
        :param rest_ship:
        :param config
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/users/me/contacts")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('contacts', _content)
                for crew_contacts in _content["contacts"]:
                    is_key_there_in_dict('iam_user_id', crew_contacts)
                    is_key_there_in_dict('personId', crew_contacts)
                    test_data['sailorServices']['crew_iam_user_id'] = _content['contacts'][0]['iam_user_id']
            else:
                raise Exception(f"ERROR: {_content['contacts']}")
        else:
            raise Exception("ERROR: No data in response")

    @pytestrail.case(11968504)
    def test_16_send_reply_to_crew(self, config, test_data, rest_ship):
        """
        Send reply to crew message
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['message_list'] = ['hi..', 'hello..', 'yes please..', 'may i know who is this', 'greetings..']
        _contents = random.choice(test_data['message_list'])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "to": test_data['sailorServices']['crew_iam_user_id'],
            "type": "private",
            "content": _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/messages')
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        if _content['result'] == 'success':
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
        else:
            raise Exception("Failed to replay to crew message...")

    @pytestrail.case(11968503)
    def test_17_end_the_chat_with_sailor(self, config, test_data, rest_ship):
        """
        End sailor chat from crew chat module
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/users/me/contacts/stopchat')
        params = {
            "contact_iam_user_id": test_data['sailorServices']['iam_userID']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew")
        if len(_content.content) != 0:
            is_key_there_in_dict('result', _content.content)
            is_key_there_in_dict('msg', _content.content)
        else:
            raise Exception("Empty response")

    @pytestrail.case(29910638)
    def test_18_enable_chat_with_sailor(self, config, test_data, rest_ship):
        """
        After ending conversation Re-start conversation again with same sailor
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/users/me/contacts'
                                                                                   '/enablechat')
        params = {
            "contact_iam_user_id": test_data['sailorServices']['iam_userID']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew")
        if len(_content.content) != 0:
            is_key_there_in_dict('result', _content.content)
            is_key_there_in_dict('msg', _content.content)
        else:
            raise Exception("Empty response")

    @pytestrail.case(25996937)
    def test_19_resend_private_message(self, test_data, rest_ship, config):
        """
        To check weather crew is able to resend message to same sailor after enabling chat
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['_message_list'] = ["hi..", "need feedback", "forgot to inform one thing", "Thank You!!", "fine"]
        _contents = random.choice(test_data['_message_list'])
        params = {
            'type': 'private',
            'to': test_data['sailorServices']['iam_userID'],
            'content': _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('id', _content)
                test_data['sailorServices']['id'] = _content['id']
            else:
                raise Exception(f"ERROR: {_content['id']}")
        else:
            raise Exception("ERROR: No message data in response")
