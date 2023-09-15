__author__ = 'HT'

from virgin_utils import *
import datetime


@pytest.mark.SHIP
@pytest.mark.SUPPORT_QUEUE
@pytest.mark.run(order=29)
class TestSupportQueue:
    """
    Test Suite to Test Support Queue module
    """

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(23464605)
    def test_01_search_for_sailor(self, config, guest_data, test_data, rest_ship):
        """
        Search for the on-boarded Sailor
        :param guest_data:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['supportQueue'] = dict()
        test_data['supportQueue']['guest'] = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), 'reservationguests/search')
        body = {
            'reservationNumber': test_data['reservationNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="crew").content
        assert test_data['supportQueue']['guest']['reservationId'] == \
               _content['_embedded']['reservationGuestDetailsResponses'][0]['reservationDetails'][0][
                   'reservationId'], 'Guest Reservation Details are not matching'

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(913466)
    def test_02_select_guest_to_chat(self, config, test_data, rest_ship):
        """
        Capture the queue-id of sailor to initiate chat
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/crew')
        params = {
            "subject": "help",
            "sailor_id": test_data['iam_user_id'],
            "voyage_number": test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        test_data['supportQueue']['queueId'] = _content['id']
        if _content['result'] == 'success':
            is_key_there_in_dict('result', _content)
            is_key_there_in_dict('msg', _content)
            is_key_there_in_dict('id', _content)
            is_key_there_in_dict('status', _content)
            is_key_there_in_dict('loyalty', _content)
            is_key_there_in_dict('subject', _content)
            is_key_there_in_dict('sailor_iam_user_id', _content)
        else:
            raise Exception("Empty response")

    @pytestrail.case(959405)
    def test_03_get_support_queues(self, config, test_data, rest_ship):
        """
        To retrieve list of all new request from sailor and crew initiated
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
        for to_check in new_ids:
            if to_check == test_data['supportQueue']['queueId']:
                break
        else:
            raise Exception(f"ID: {test_data['supportQueue']['queueId']} not found in new/pending !!")

    @pytestrail.case(983645)
    def test_04_send_support_queue_messages(self, config, test_data, rest_ship):
        """
        To send messages to new request
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        content = "Hi..How can i help you"
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        params = {
            'queue_id': test_data['supportQueue']['queueId'],
            'content': content,
            'voyage_number': test_data['voyageNumber']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        if len(_content) != 0:
            if _content['result'] == "success":
                is_key_there_in_dict('result', _content)
                is_key_there_in_dict('msg', _content)
                is_key_there_in_dict('id', _content)
                test_data['supportQueue']['sent_msg_id'] = _content['id']
            else:
                raise Exception(f"ERROR: {_content['msg']}")
        else:
            raise Exception(f"ERROR: No data in response")

    @pytestrail.case(983646)
    def test_05_get_support_queue_messages(self, config, test_data, rest_ship):
        """
        To retrieve sent message
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        msg_sent = "<p>Hi..How can i help you</p>"
        params = {
            'queue_id': test_data['supportQueue']['queueId'],
            'use_first_unread_anchor': 'true',
            'num_before': '3',
            'num_after': '3'
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/messages')
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        assert _content['result'] == 'success', f'Getting {_content["result"]} as response inplace of "success"'
        for message in _content['messages']:
            if message['id'] == test_data['supportQueue']['sent_msg_id']:
                assert msg_sent == message['content'], "sent content is not matching with received."
                break
        else:
            raise Exception("Can't find the sent message id in response.")

    @pytestrail.case(24032442)
    def test_06_get_support_queues(self, config, test_data, rest_ship):
        """
        To verify that started request is appearing in in-progress request or not
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

        for to_check in in_progress_ids:
            if to_check == test_data['supportQueue']['queueId']:
                break
        else:
            raise Exception(f"ID: {test_data['supportQueue']['queueId']} not found in in-progress-pending !!")

    @pytestrail.case(64726469)
    def test_07_sending_link_in_chat(self, config, test_data, rest_ship):
        """
        To verify that the crew is able to send links successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/messages")
        param = {
            "content": "https://www.google.com/",
            "voyage_number": test_data['voyageNumber'],
            "is_send_notification": True,
            "queue_id": test_data['supportQueue']['queueId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=param, auth="crew").content
        assert _content['result'] == "success", 'link not send'

    @pytestrail.case(64726468)
    def test_08_sending_image_in_chat(self, config, test_data, rest_ship):
        """
        To verify that the crew is able to send images successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        security_photo = GeneratePhoto(first_name='alan', last_name='joseph', email_id='joseph.alan@yopmail.com',
                                       birth_date='09-12-1988', gender='male').add_text()
        security_photo_url = upload_media_file(config, rest_ship, security_photo)
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/messages")
        param = {
            "content": security_photo_url,
            "voyage_number": test_data['voyageNumber'],
            "is_send_notification": True,
            "queue_id": test_data['supportQueue']['queueId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=param, auth="crew").content
        assert _content['result'] == "success", 'image not sent'

    @pytestrail.case(27786558)
    def test_09_sending_vq_in_chat(self, config, test_data, rest_ship):
        """
        To verify that the crew is able to send Virtual Queue(VQ) successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        virtual_queue = "{\"message\":\"Join Help Desk\",\"venueName\":\"Sailor Services\"," \
                        "\"venueThumbnail\":\"https://cms-cert.ship.virginvoyages.com/dam/" \
                        "jcr:9888568d-21a9-44dc-881c-5d9ae3217fee/" \
                        "IMG-SPC-sailor-services-lifestyle-v1-01-7096-120x120.jpg\"," \
                        "\"virtualQueuesBackgroundImage\":\"https://cms-cert.ship.virginvoyages.com/dam/" \
                        "jcr:1a06ea4d-1ec6-44ae-9fa7-fa0645a18cc1/" \
                        "IMG-SPC-sailor-services-lifestyle-v1-7096-1200x1920.jpg\"," \
                        "\"virtualQueueName\":\"Help Desk\",\"deckLocation\":\"Deck 5 Mid-Aft\"," \
                        "\"virtualQueueDefinitionId\":\"21395c69-932d-4625-9e68-107ae278b476\"," \
                        "\"globalVenueId\":\"5a4bf485da0c112a66ed620d\"}"
        vq_content = json.dumps(virtual_queue)
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "api/v1/support_queue/messages")
        params = {
            "queue_id": test_data['supportQueue']['queueId'],
            "content": vq_content,
            "voyage_number": test_data['voyageNumber'],
            "is_send_notification": True,
            "is_virtual_queue": True
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        assert _content['result'] == "success", 'Virtual Queue(VQ) not sent'

    @pytestrail.case(983647)
    def test_10_resolve_support_queue_messages(self, config, test_data, rest_ship):
        """
        To mark the query Resolved in support queue
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), '/api/v1/support_queue/resolve')
        params = {
            'queue_id': test_data['supportQueue']['queueId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content

        if len(_content) != 0:
            assert test_data['supportQueue']['queueId'] == _content['id'], "id mismatch !!"
            assert _content['status'] == 'resolved', "Request is not Resolved !!"
            assert _content['result'] == "success", "Result is not Success !!"

    @pytestrail.case(23147367)
    def test_11_get_support_queues(self, config, test_data, rest_ship):
        """
        To verify the id in resolved request list
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
        resolved_ids = []
        for resolved in _content['resolved']:
            is_key_there_in_dict('first_message_time', resolved)
            is_key_there_in_dict('id', resolved)
            is_key_there_in_dict('loyalty', resolved)
            is_key_there_in_dict('requires_attention', resolved)
            is_key_there_in_dict('sailor_iam_user_id', resolved)
            is_key_there_in_dict('status', resolved)
            is_key_there_in_dict('stream_id', resolved)
            is_key_there_in_dict('subject', resolved)
            is_key_there_in_dict('voyage_number', resolved)
            resolved_ids.append(resolved['id'])

        for to_check in resolved_ids:
            if to_check == test_data['supportQueue']['queueId']:
                break
        else:
            raise Exception(f"ID: {test_data['supportQueue']['queueId']} not found in resolved state !!")

    @pytestrail.case(26949035)
    def test_12_chat_filter_by_vip_level(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the chats in support-queue using vip levels
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        test_data['supportQueue']["vip_levels"] = ["vip1", "vip2", "vip3", "vip4", "vip5", "vip6"]
        filter_by_vip = random.choice(test_data['supportQueue']["vip_levels"])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "&show_my_chats": False,
            "&sort_by": "created",
            "&loyalty": filter_by_vip
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew")
        if len(_content) != 0:
            pass
        else:
            raise Exception("no chat conversation history available to filter")

    @pytestrail.case(26952619)
    def test_13_filter_by_show_my_chats(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the chats in support-queue using 'show my chats' option
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        params = {
            "voyage_number": test_data['voyageNumber'],
            "&show_my_chats": True,
            "&sort_by": "created"
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew")
        if len(_content) != 0:
            pass
        else:
            raise Exception("no chat conversation history available to filter")

    @pytestrail.case(26953155)
    def test_14_filter_by_date_range(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the chats in support-queue using 'date range' option
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        current_date = datetime.datetime.today()
        previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
        params = {
            "voyage_number": test_data['voyageNumber'],
            "&show_my_chats": True,
            "&sort_by": "created",
            "&start": previous_date,
            "&end": current_date
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew")
        if len(_content) != 0:
            pass
        else:
            raise Exception("no chat conversation history available to filter")

    @pytestrail.case(26955831)
    def test_15_filter_for_yesterday_chat(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the previous day chats in support-queue using 'yesterday' option
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        yesterday_date = datetime.datetime.today() - datetime.timedelta(days=1)
        params = {
            "voyage_number": test_data['voyageNumber'],
            "&show_my_chats": True,
            "&sort_by": "created",
            "&start": yesterday_date,
            "&end": yesterday_date
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew")
        if len(_content) != 0:
            pass
        else:
            raise Exception("no chat conversation history available to filter")

    @pytestrail.case(1080193)
    def test_16_adding_custom_canned_message(self, config, test_data, rest_ship):
        """
        To verify that the crew is able to add custom canned messages successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/canned_message")
        params = {
            "message_content": "hello world",
            "is_default": "false",
        }
        _content = rest_ship.send_request(method="POST", params=params, url=_url, auth="crew").content
        test_data['supportQueue']["id"] = _content["id"]
        assert _content['result'] == "success", 'canned message not added'
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                      "/api/v1/support_queue/canned_message")
        _content_get = rest_ship.send_request(method="GET", url=_url_get, auth="crew").content
        for message_id in _content_get['custom_messages']:
            if message_id['id'] == _content["id"]:
                break
        else:
            raise Exception('canned message added not confirmed')

    @pytestrail.case(1080195)
    def test_17_deleting_custom_canned_message(self, config, test_data, rest_ship):
        """
        To verify that the crew is able to delete custom canned messages successfully
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       f"/api/v1/support_queue/canned_message/{test_data['supportQueue']['id']}")
        _content = rest_ship.send_request(method="DELETE", url=_url, auth="crew").content
        assert _content['result'] == "success", 'canned message not deleted'
        _url_get = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                           "/api/v1/support_queue/canned_message")
        _content_get = rest_ship.send_request(method="GET", url=_url_get, auth="crew").content
        for message_id in _content_get['custom_messages']:
            if message_id['id'] == test_data['supportQueue']['id']:
                raise Exception('canned message deleted not confirmed')

    @pytestrail.case(64726500)
    def test_18_sort_by(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the chats in support-queue using sort by filter
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        test_data['supportQueue']["sort_by"] = ["Create time", "Responded time", "Guest type"]
        sort_by = random.choice(test_data['supportQueue']["sort_by"])
        params = {
            "voyage_number": test_data['voyageNumber'],
            "&sort_by": sort_by
            }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew").content
        assert _content['result'] == "success", 'not sorted'

    @pytestrail.case(1080189)
    def test_19_event_registration(self, config, test_data, rest_ship):
        """
        To verify that events are registered
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/registration")
        _content = rest_ship.send_request(method="POST", url=_url, auth="crew").content
        test_data['supportQueue']['QueueId'] = _content['queue_id']
        test_data['supportQueue']['last_event_id'] = _content['last_event_id']

        assert _content['result'] == 'success', 'event not registered'

    @pytestrail.case(1080190)
    def test_20_event_list(self, config, test_data, rest_ship):
        """
        To verify that list of all the registered events appear
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/events")
        params = {"queue_id": test_data['supportQueue']['QueueId'],
                  "last_event_id": test_data['supportQueue']['last_event_id']
                  }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        assert _content['result'] == 'success', 'event list not appeared'

    @pytestrail.case(1080192)
    def test_21_notification_time(self, config, test_data, rest_ship):
        """
        To verify notification time value is retrieved
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/notification_time")
        params = {"notification_time": 600}
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="crew").content
        assert _content['result'] == 'success', 'notification time not retrieved'

    @pytestrail.case(1080191)
    def test_22_chat_configuration_time(self, config, test_data, rest_ship):
        """
        To verify notification time value is retrieved
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        test_data['supportQueue']['anchor'] = random.choice(range(100000, 10000000))
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/messages")
        params = {"anchor": test_data['supportQueue']['anchor'],
                  "queue_id": test_data['supportQueue']['queueId'],
                  "num_before": 30,
                  "num_after": 0,
                  "apply_markdown": 'true'}
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="crew").content
        is_key_there_in_dict('timestamp', _content['messages'][0])
        timing = _content['messages'][0]['timestamp']
        assert timing is not None, 'chat configuration time not found'

    @pytestrail.case(1080194)
    def test_23_owned_by_me(self, config, test_data, rest_ship):
        """
        To verify that requests are owned by user
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),
                       "/api/v1/support_queue/ownership")
        param = {"queue_id": test_data['supportQueue']['queueId']}
        _content = rest_ship.send_request(method="POST", url=_url, params=param, auth="crew").content
        assert _content['result'] == 'success', 'not owned'
        assert _content['queue_id'] == test_data['supportQueue']['queueId'], 'failed to own the request'

    @pytestrail.case(69243204)
    def test_24_chat_filter_by_decks_and_cabins(self, config, test_data, rest_ship):
        """
        To verify that crew is able to filter the chats using Decks & Cabins
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        params = {
            "voyage_number": test_data['voyageNumber'],
            "sort_by": "created",
            "cabin_number": test_data['cabinNumber']
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew").content
        assert _content['result'] == 'success', "filter the chats using Decks & Cabins call is not working"

    @pytestrail.case(69243205)
    def test_25_filter_by_owner(self, config, test_data, rest_ship):
        """
        To verify crew is able to Filter results by Ownership
        :param config:
        :param test_data:
        :param rest_ship:
        """
        test_data['supportQueue']['ownership'] = ["owned_by_me", "owned_by_none"]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        params = {
            "voyage_number": test_data['voyageNumber'],
            "sort_by": "created",
            "cabin_number": [test_data['cabinNumber']],
            "owned_by": random.choice(test_data['supportQueue']['ownership'])
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew").content
        assert _content['result'] == 'success', "filter by owner call is not working"

    @pytestrail.case(69243206)
    def test_26_filter_using_multiple_filters(self, config, test_data, rest_ship):
        """
        To verify Filter results should display by applying Multiple filters
        :param config:
        :param test_data:
        :param rest_ship:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'), "/api/v1/support_queue/list_v3")
        params = {
            "voyage_number": test_data['voyageNumber'],
            "sort_by": "created",
            "loyalty_level": random.choice(test_data['supportQueue']['vip_levels']),
            "cabin_number": [test_data['cabinNumber']],
            "owned_by": random.choice(test_data['supportQueue']['ownership'])
        }
        _content = rest_ship.send_request(method="GET", params=params, url=_url, auth="crew").content
        assert _content['result'] == 'success', "multiple filters call is not working"