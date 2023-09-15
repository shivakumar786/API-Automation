__author__ = "sarvesh.singh"

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.CHAT_NOTIFICATION
@pytest.mark.run(order=32)
class TestChatNotifications:
    """
      Test Suite to Test Chat And Notification
    """

    @pytestrail.case(24655679)
    def test_01_search_for_sailor(self, config, guest_data, test_data, rest_ship):
        """
        Search for the on-boarded Sailor
        :param config:
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['chat_guest_id'] = dict()
        test_data['chat_guest_id']['guestId'] = guest_data[0]['guestId']
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservationguests/search')
        body = {
            'reservationNumber': test_data['reservationNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        assert _content['_embedded']['reservationGuestDetailsResponses'][0]['reservationDetails'][0]['cabinNumber'] == \
               test_data['cabinNumber'], 'Reserved Cabin number mismatched'

    @pytestrail.case(1080198)
    def test_02_get_iam_user_id(self, test_data, rest_ship, config):
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
            'personid': test_data['chat_guest_id']['guestId']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        test_data['chat_guest_id']['iam_userID'] = _content['userId']
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

    @retry_when_fails(retries=20, interval=5)
    @pytestrail.case(29614921)
    def test_03_event_registration(self, test_data, rest_ship, config):
        """
        User event registration
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/registration")
        _content = rest_ship.send_request(method="POST", url=_url, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('queue_id', _content)
                is_key_there_in_dict('last_event_id', _content)
            else:
                raise Exception(f"ERROR: {_content['queue_id']}")
        else:
            raise Exception("ERROR: No data in response")
        chat_data = {
            'chat_notification':
                {
                    'queue_id': str(_content['queue_id']),
                    'last_event_id': _content['last_event_id']
                }
        }
        test_data.update(chat_data)

    @pytestrail.case(959400)
    def test_04_get_event(self, test_data, rest_ship, config):
        """
        To get the event list
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _q_id = test_data['chat_notification']['queue_id']
        _last_event_id = test_data['chat_notification']['last_event_id']
        params = {
            'queue_id': _q_id,
            'last_event_id': _last_event_id
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), 'api/v1/events')
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('events', _content)
                for event_data in _content['events']:
                    is_key_there_in_dict('type', event_data)
                    is_key_there_in_dict('id', event_data)
            else:
                raise Exception(f"ERROR: {_content['events']}")
        else:
            raise Exception("ERROR: No event data in response")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(959849)
    def test_05_get_private_message(self, request, test_data, rest_ship, config):
        """
        To verify the private message
        :param test_data:
        :param request:
        :param rest_ship:
        :param config:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath,
                                       'test_data/verification_data/chat_notify_private_msg.json')
        with open(_ship_data_file, 'r') as _fp:
            _chat_data = json.load(_fp)
        _narrow = json.dumps([{"operand": test_data['iam_user_id'], "operator": "pm-with"}])
        params = {
            'num_after': '3',
            'client_gravatar': 'false',
            'apply_markdown': 'false',
            'narrow': _narrow,
            'use_first_unread_anchor': 'true',
            'num_before': '3'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if _content['result'] == "success":
            for _key in _chat_data:
                is_key_there_in_dict(_key, _content)
        else:
            raise Exception('chat notification messages list not available!')

    @pytestrail.case(959848)
    def test_06_send_private_message(self, test_data, rest_ship, config):
        """
        Sending a private message to the guest
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['_message_list'] = ["Good Afternoon", "Good Morning", "How can I help you", "Thank You!!", "Hii!!"]
        _contents = random.choice(test_data['_message_list'])
        params = {
            'type': 'private',
            'to': test_data['chat_guest_id']['iam_userID'],
            'content': _contents
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('id', _content)
                test_data['chat_notification'].update({"message_id": _content['id']})
            else:
                raise Exception(f"ERROR: {_content['id']}")
        else:
            raise Exception("ERROR: No message data in response")

    @pytestrail.case(25996156)
    def test_07_enable_chat_with_sailor(self, config, test_data, rest_ship):
        """
        Enable chat with sailor if chat is already ended
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/users/me/contacts'
                                                                                   '/enablechat')
        params = {
            "contact_iam_user_id": test_data['chat_guest_id']['iam_userID']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew")
        if len(_content.content) != 0:
            is_key_there_in_dict('result', _content.content)
            is_key_there_in_dict('msg', _content.content)
        else:
            raise Exception("Empty response")

    @pytestrail.case(1080203)
    def test_08_get_contacts(self, test_data, rest_ship, config):
        """
        To verify the guest in the 'my guest tab'
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/users/me/contacts/people?")
        params = {
            'voyage_number': test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
            else:
                raise Exception(f"ERROR: {_content['contacts']}")
        else:
            raise Exception("ERROR: No data in response")

    @retry_when_fails(retries=10, interval=5)
    @pytestrail.case(1080199)
    def test_09_search_for_crew(self, config, test_data, rest_ship):
        """
        Search for the on-duty crew member
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),
                       '/userprofiles/getuserdetails?')
        crew_personid = ['d68ede6c-8e51-40f9-b578-fc78ad593c29', 'd01796e7-2c4f-428e-b6a1-3ab996ab327c', 'd088e358-aa4d-4027-b7c1-30762fe1334e',
                         'a8b29390-fc19-4181-8e5a-c118a1ad0ceb']
        for _person in crew_personid:
            params = {
                'personid': _person
            }
            _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
            if len(_content) != 0:
                is_key_there_in_dict('userId', _content)
                is_key_there_in_dict('firstName', _content)
                is_key_there_in_dict('middleName', _content)
                is_key_there_in_dict('lastName', _content)
                is_key_there_in_dict('personTypeCode', _content)
                is_key_there_in_dict('personId', _content)
                is_key_there_in_dict('preferredName', _content)
                is_key_there_in_dict('userMediaItemId', _content)
                test_data['chat_guest_id']['crew'] = _content['userId']
                break
        if 'crew' not in test_data['chat_guest_id']:
            raise Exception("No crew is available for chat")

    @pytestrail.case(1080200)
    def test_10_crew_crew_chat(self, test_data, rest_ship, config):
        """
        TO chat with another crew
        :param test_data:
        :param rest_ship:
        :param config:
        :return:
        """
        test_data['_message_list'] = ["hi..", "is everything fine", "completed the task", "Thank You!!", "Hii!!"]
        _contents = random.choice(test_data['_message_list'])
        params = {
            'content': _contents,
            'voyage_number': test_data['voyageNumber'],
            'to': test_data['chat_guest_id']['crew'],
            'type': 'private'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('id', _content)
                test_data['chat_notification'].update({"message_id": _content['id']})
            else:
                raise Exception(f"ERROR: {_content['id']}")
        else:
            raise Exception("ERROR: No message data in response")

    @pytestrail.case(1080201)
    def test_11_get_crew_crew_private_message(self, request, test_data, rest_ship, config):
        """
        To get the private message sent by crew to crew
        :param test_data:
        :param request:
        :param rest_ship:
        :param config:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath,
                                       'test_data/verification_data/chat_notify_private_msg.json')
        with open(_ship_data_file, 'r') as _fp:
            _chat_data = json.load(_fp)
        _narrow = json.dumps([{"operand": test_data['chat_guest_id']['crew'], "operator": "pm-with"}])
        params = {
            'num_after': '3',
            'client_gravatar': 'false',
            'apply_markdown': 'false',
            'narrow': _narrow,
            'use_first_unread_anchor': 'true',
            'num_before': '3'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/messages")
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        if _content['result'] == "success":
            for _key in _chat_data:
                is_key_there_in_dict(_key, _content)
        else:
            raise Exception('chat notification messages list not available!')
