__author__ = 'anshuman.goyal'
__maintainer__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.FNB
@pytest.mark.run(order=14)
class TestFoodBeverage:
    """
    Test Suite to test Food and Beverage
    """

    @pytestrail.case(109)
    def test_01_get_venue_list(self, config, test_data, rest_ship):
        """
        Get F&B Venues List
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        user_id = test_data['personId']
        params = {
            'userId': user_id
        }
        url = urljoin(_ship, "/fnbserver/Home/GetVenueList")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for venue in _content:
                test_data['venues'] = venue
                break
        else:
            raise Exception('No venue found!')

    @pytestrail.case(169)
    def test_02_get_menu_items(self, config, test_data, rest_ship):
        """
        Get F&B Menu Items
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        venues = test_data['venues']
        _venue = venues['VenueId']
        params = {
            'venueId': _venue
        }
        url = urljoin(_ship, "/fnbserver/Home/GetMenuItems")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for menuItem in _content:
                is_key_there_in_dict('MenuItemId', menuItem)
                is_key_there_in_dict('MenuItemPrices', menuItem)
                for MenuItemPrice in menuItem['MenuItemPrices']:
                    is_key_there_in_dict('UnitId', MenuItemPrice)
                    is_key_there_in_dict('UnitName', MenuItemPrice)
                    is_key_there_in_dict('Price', MenuItemPrice)
                    is_key_there_in_dict('StartDate', MenuItemPrice)
                    is_key_there_in_dict('IsSelected', MenuItemPrice)
                    is_key_there_in_dict('Count', MenuItemPrice)
            venues['menuItems'] = _content
        else:
            raise Exception('No menu item found!')
        test_data['venues'] = venues

    @pytestrail.case(159)
    def test_03_create_order(self, config, test_data, rest_ship, guest_data):
        """
        Create F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        _ship = config.ship.url
        venues = test_data['venues']
        guest = guest_data[0]
        # Reservation Guest ID is different for VV and DXP (case change)
        _id = guest['reservationGuestId']
        url = urljoin(_ship, "/fnbserver/Home/CreateOrder")
        menu_items = venues['menuItems']
        _menu_items = random.choice(menu_items)
        body = {
            "VenueId": venues['VenueId'], "GuestId": _id, "Gratuity": 0, "Amount": 7.25,
            "TaxAmount": 0, "TaxPercentage": 0, "GratuityPercentage": 15,
            "AddedBy": test_data['personId'], "OrderTypeId": "71b536df-b9ec-11e9-b327-16345b88f44a",
            "OrderOriginId": "71b536e3-b9ec-11e9-b327-16345b88f44a",
            "OrderDetails": [{
                "MenuItemId": _menu_items['MenuItemId'], "OrderQuantity": 1, "UnitPrice": 7.25,
                "TaxAmount": 0, "Amount": 7.25,
                "UnitId": _menu_items['MenuItemPrices'][0]['UnitId']
            }],
            "AdditionalNotes": ""
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if 'No account provided/found(check_id)' in _content:
            test_data['fnb_order'] = False
            pytest.skip("Not able to create order due to charge id issue")
        elif len(_content) != 0:
            is_key_there_in_dict('OrderId', json.loads(_content))
            test_data['fnb'].append(json.loads(_content))
            test_data['fnb_order'] = True
        else:
            raise Exception('No order data found!')

    @pytestrail.case(139)
    def test_04_verify_create_order(self, config, test_data, rest_ship):
        """
        Verify F&B Created Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _order = _data['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(_ship, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if _content['Status'] != 1:
            raise Exception("Order Status != 1")

    @pytestrail.case(133)
    def test_05_place_on_deck_order(self, config, test_data, rest_ship):
        """
        Place an F&B On-Deck Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(config.ship.url, "/fnbserver/orders")
        body = {
            "OrderIds": [_data['OrderId']],
            "UpdatedBy": test_data['personId'],
            "Status": 2,
            "VenueId": _data['VenueId']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        test_data['fnb'][0]['OrderId'] = _content['Value']['OrderIds'][0]
        if int(_content['Value']['Status']) != 2:
            raise Exception("ERROR: Order Status != 2")

    @pytestrail.case(110)
    def test_06_verify_place_on_deck_order(self, config, test_data, rest_ship):
        """
        Verify F&B Placed On Deck Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _order = _data['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(_ship, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['fnb'][0]['Status'] = _content['Status']
        if int(_content['Status']) != 2:
            raise Exception("ERROR: Order Status != 2")

    @pytestrail.case(103)
    def test_07_bump_order(self, config, test_data, rest_ship):
        """
        Bump F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Home/BumpOrder")
        body = {
            "VenueId": _data['VenueId'], "UserId": test_data['personId'],
            "OrderId": _data['OrderId'], "OrderNumber": _data['OrderNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['ReturnCode'] != 1001:
            raise Exception("ReturnCode != 1001")
        if _content['Message'] != 'OrderSuccessfullyBumped':
            raise Exception("Message != OrderSuccessfullyBumped")

    @pytestrail.case(173)
    def test_08_verify_bumped_order(self, config, test_data, rest_ship):
        """
        Verify F&B Bumped Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _order = _data['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(_ship, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['fnb'][0]['Status'] = _content['Status']
        if int(_content['Status']) != 3:
            raise Exception("ERROR: Order Status != 3")

    @pytestrail.case(93)
    def test_09_deliver_order(self, config, test_data, rest_ship):
        """
        Deliver F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Home/DeliverOrder")
        body = {
            "VenueId": _data['VenueId'], "UserId": test_data['personId'],
            "OrderId": _data['OrderId'], "OrderNumber": _data['OrderNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['ReturnCode'] != 1005:
            raise Exception("ReturnCode != 1005")
        if _content['Message'] != 'OrderSuccessfullyDelivered':
            raise Exception("Message != OrderSuccessfullyDelivered")

    @pytestrail.case(114)
    def test_10_verify_delivered_order(self, config, test_data, rest_ship):
        """
        Verify F&B Delivered Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _order = _data['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(_ship, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['fnb'][0]['Status'] = _content['Status']
        if int(_content['Status']) != 4:
            raise Exception("ERROR: Order Status != 4")

    @pytestrail.case(149)
    def test_11_cancel_order(self, config, test_data, rest_ship):
        """
        Cancel F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Home/Cancel")
        body = {
            "OrderId": _data['OrderId'], "VenueId": _data['VenueId'],
            "OrderCancellations": [{
                "OrderId": _data['OrderId'],
                "CancellationRequestedBy": test_data['personId'],
                "AddedBy": test_data['personId'], "CancellationReason": "Wrong Order"
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['ReturnCode'] != 1003:
            raise Exception("ReturnCode != 1003")
        if _content['Message'] != 'OrderSuccessfullyCancelled':
            raise Exception("Message != OrderSuccessfullyCancelled")

    @pytestrail.case(134)
    def test_12_verify_cancelled_order(self, config, test_data, rest_ship):
        """
        Verify F&B Cancelled Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _order = _data['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(_ship, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        test_data['fnb'][0]['Status'] = _content['Status']
        if int(_content['Status']) != 5:
            raise Exception("ERROR: Order Status != 5")

    @pytestrail.case(65984861)
    def test_13_mark_unbump_order(self, config, test_data, rest_ship):
        """
        Bump F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Orders/UnBump")
        body = {
            "VenueId": _data['VenueId'], "UserId": test_data['personId'],
            "OrderId": _data['OrderId'], "OrderNumber": _data['OrderNumber'], "TokenNumber": None
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['Message'] != 'OrderSuccessfullyPrepared':
            raise Exception("Message != OrderSuccessfullyPrepared")

    @pytestrail.case(65984862)
    def test_14_mark_undeliverable_order(self, config, test_data, rest_ship):
        """
        Cancel F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Orders/Cancel")
        body = {
            "OrderId": _data['OrderId'], "VenueId": _data['VenueId'],
            "OrderCancellations": [{
                "OrderId": _data['OrderId'],
                "CancellationRequestedBy": test_data['personId'],
                "AddedBy": test_data['personId'], "CancellationReason": "Wrong Order",
                "CancellationReasonIds": []
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['Message'] != 'OrderSuccessfullyCancelled':
            raise Exception("Message != OrderSuccessfullyCancelled")

    @pytestrail.case(65984863)
    def test_15_verify_guest_is_present(self, config, test_data, rest_ship, guest_data):
        """
        Bump F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _id = guest_data[0]['reservationGuestId']
        url = urljoin(_ship, "/fnbserver/notification/guestnotfound")
        body = {
            "crewMemberId": "9404e29c-32ed-4144-8a0a-3676ffa89115", "OrderId": _data['OrderId'], "GuestId": _id

        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['Message'] != 'OrderAllreadyPreparedBySameUser':
            raise Exception("Guest not found")

    @pytestrail.case(67857603)
    def test_16_search_guest(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _id = guest_data[0]['guestId']
        url = urljoin(_ship, "/fnbserver/Orders/Search")
        body = {
            "TeamMemberId": "",
            "GuestId": _id,
            "MenuItems": "",
            "OrderNumber": "",
            "VenueId": _data['VenueId'],
            "IncludeAdditionalData": True,
            "SearchGuestCrew": True,
            "OrderDeliveredAt": "",
            "OrderDate": _data['OrderDate']
        }

        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0 and _content['GuestId'] != _id:
            raise Exception("Couldn't find guest")

    @pytestrail.case(67857604)
    def test_17_search_menu_item(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B menu_item
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Orders/Search")
        _id = guest_data[0]['guestId']
        body = {
            "TeamMemberId": "",
            "GuestId": _id,
            "MenuItems": _data['OrderDetails'][0]['MenuItemId'],
            "OrderNumber": "",
            "VenueId": _data['VenueId'],
            "IncludeAdditionalData": True,
            "SearchGuestCrew": True,
            "OrderDeliveredAt": "",
            "OrderDate": _data['OrderDate']
        }

        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if (len(_content) != 0) and (_content[0]['OrderDetails'][0]['MenuItemId'] != _data['OrderDetails'][0]['MenuItemId']):
            raise Exception("Couldn't find menu item")

    @pytestrail.case(67857605)
    def test_18_search_order(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "/fnbserver/Orders/Search")
        _id = guest_data[0]['guestId']
        body = {
            "TeamMemberId": "", "GuestId": _id, "MenuItems": _data['OrderDetails'][0]['MenuItemId'],
            "OrderNumber": _data['OrderNumber'], "VenueId": _data['VenueId'],
            "IncludeAdditionalData": True, "SearchGuestCrew": True,
            "OrderDeliveredAt": "", "OrderDate": _data['OrderDate']
        }

        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if (len(_content) != 0) and (_content[0]['OrderNumber'] != _data['OrderNumber']):
            raise Exception("Couldn't find order")

    @pytestrail.case(67857606)
    def test_19_notification_enabled(self, config, test_data, rest_ship, guest_data):
        """
        Notification enabled
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _id = guest_data[0]['reservationGuestId']
        url = urljoin(_ship, "/fnbserver/notificationpreference/update")
        body = {
                "TeammemberId": "53952924-fad5-4a02-813b-150900b8c981",
                "VenueId": _data['VenueId'],
                "IsNotificationOptedOut": False
                }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if _content['Message'] != 'IsNotificationOptedOut':
            raise Exception("notification on")

    @pytestrail.case(67857607)
    def test_20_notification_Disabled(self, config, test_data, rest_ship, guest_data):
        """
        Notification disabled
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        _id = guest_data[0]['reservationGuestId']
        url = urljoin(_ship, "/fnbserver/notificationpreference/update")
        body = {
                "TeammemberId": "53952924-fad5-4a02-813b-150900b8c981",
                "VenueId": _data['VenueId'],
                "IsNotificationOptedOut": True
                }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if _content['Message'] != 'IsNotificationOptedOut':
            raise Exception("notification off")

    @pytestrail.case(68357109)
    def test_21_filter_Delivered_order(self, config, test_data, rest_ship):
        """
        Filter order on the delivered tab
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "fnbserver/Orders/Search")
        body = {

            "VenueId": _data['VenueId'],
            "OrderDate": _data['OrderDate'],
            "statusIds": "5", "OrderDeliveredAt": "",
            "DeliveryPersonIds": _data['DeliveryPersonIds'],
            "PlacedByPersonIds": _data['DeliveryPersonIds'],
            "SearchWithDeliveryDate": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['SearchWithDeliveryDate'] != True:
            raise Exception("no order is to be delivered for these selections")

    @pytestrail.case(68357110)
    def test_22_filter_cancelled_order(self, config, test_data, rest_ship, ):
        """
        Filter order on the cancelled tab
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _data = test_data['fnb'][0]
        _ship = config.ship.url
        url = urljoin(_ship, "fnbserver/Orders/Search")
        body = {

            "VenueId": _data['VenueId'],
            "OrderDate": _data['OrderDate'],
            "statusIds": "5", "OrderDeliveredAt": "",
            "IncludePartialCancelled": True, "SearchWithCancelledDate": True
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if (_content['IncludePartialCancelled'] != True) and (_content['SearchWithCancelledDate'] != True):
            raise Exception("no cancelled order on this selection")
