__author__ = 'Sarvesh.Singh'

from virgin_utils import *
from datetime import timezone

@pytest.mark.SHIP
@pytest.mark.INTEGRATION
@pytest.mark.SHIP_EATS_FNB
@pytest.mark.run(order=35)
class TestShipEatsFnb:
    """
    Test Suite to check integration of Ship Eats and Fnb
    """

    @pytestrail.case(26112982)
    def test_01_login(self, config, test_data, guest_data, rest_ship):
        """
        Create Guest Login
        :param config:
        :param test_data:
        :param guest_data:
        :param rest_ship:
        :return:
        """
        test_data['shipEatsFnb'] = dict()
        guest = guest_data[0]
        _shore = config.ship.url
        url = urljoin(_shore, "user-account-service/signin/email")
        body = {
            "userName": guest['email'],
            "password": test_data['guestPassword']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="Basic").content
        rest_ship.userToken = f"Bearer {_content['accessToken']}"
        test_data['userToken'] = rest_ship.userToken

    @pytestrail.case(17543852)
    def test_02_configurations_ship_eats(self, config, rest_ship, test_data):
        """
        Get ship eats configurations
        :param config:
        :param rest_ship:
        :param test_data:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/configuration/shipeats')
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        check_assertions([
            'ShipEatsBreakfastType', 'ShipEatsOrderHistoryPollingInterval', 'ShipEatsOrderOriginId',
            'ShipEatsEatNowOrderTypeId', 'ShipEatsPreOrderTypeId',
            'ShipEatsDefaultResponseTimeout', 'ActivityCodeDeliveredNotification',
            'ActivityCodeDeliveredPreOrderNotification', 'ActivityCodeGuestNotFoundNotification',
            'ActivityCodeCancelledOrderNotification', 'ActivityCodeCancelledByGuestNotification',
            'IsErrorMode'], _content)

        test_data['shipEatsFnb']['shipEatsEatNowOrderTypeId'] = _content['ShipEatsEatNowOrderTypeId']
        test_data['shipEatsFnb']['ShipEatsOrderOriginId'] = _content['ShipEatsOrderOriginId']

    @pytestrail.case(17543854)
    def test_03_get_venues(self, config, test_data, rest_ship, guest_data):
        """
        Get venues
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"/v1/venues/detection/{guest['reservationGuestId']}")
        params = {
            'onlyLocationRequired': False
        }
        _content = rest_ship.send_request(method="POST", url=_url, params=params, auth="user").content
        check_assertions([
            'Venue', 'Location', 'PreOrderBreakfastVenueId', 'CabinNumber', 'LocationId', 'ReturnCode'], _content)
        test_data['shipEatsFnb']['venue'] = _content

    @pytestrail.case(17548505)
    def test_04_get_allergens(self, config, rest_ship, test_data):
        """
        Get Allergens
        :param config:
        :param rest_ship:
        :param test_data:
        :return:
        """
        test_data['shipEatsFnb']['allergens'] = dict()
        test_data['shipEatsFnb']['allergens']['id'] = None
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/allergens")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        for _data in _content:
            check_assertions([
                'AllergyId', 'AllergenName'], _data)
        for _data in _content:
            test_data['shipEatsFnb']['allergens']['id'] = _data['AllergyId']
            test_data['shipEatsFnb']['allergens']['name'] = _data['AllergenName']
            break

    @pytestrail.case(17612300)
    def test_05_get_menu_items(self, config, test_data, rest_ship):
        """
        Get Menu Items
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/menuItems")
        epoch_time = int(datetime.now(tz=timezone.utc).timestamp()) + 19800
        test_data['shipEatsFnb']['startDate'] = str(datetime.fromtimestamp(epoch_time)).split(' ')[0]
        epoch_time = int(datetime.now(tz=timezone.utc).timestamp()) + 19800 + 86400
        test_data['shipEatsFnb']['endDate'] = str(datetime.fromtimestamp(epoch_time)).split(' ')[0]
        params = {
            'venueId': test_data['shipEatsFnb']['venue']['Venue']['VenueId'],
            'startDate': test_data['shipEatsFnb']['startDate'],
            'endDate': test_data['shipEatsFnb']['endDate']
        }
        _content = rest_ship.send_request(method="GET", url=_url, params=params, auth="user").content
        if len(_content) == 0:
            raise Exception('There is no menu item available to book')
        for _data in _content:
            check_assertions([
                'Name', 'MenuItemId', 'MenuItemNumber', 'VenueId', 'MenuItemType', 'MenuItemIngredients',
                'MenuItemPrices', 'CustomizationGroupMenuItems', 'MealPeriodMenuItems', 'MenuItemAllergies',
                'MenuItemCustomizationGroups', 'MenuItemExceptionWindows', 'MenuItemLifestyles', 'MenuItemNutritions',
                'MenuItemFilters', 'MenuItemOptions'], _data)
        for _data in _content:
            if len(_data['MenuItemPrices']) > 0 and len(_data['MealPeriodMenuItems']) > 0:
                test_data['shipEatsFnb']['menuItem'] = _data
                break

    @pytestrail.case(17647177)
    def test_06_get_order_wait_time(self, config, test_data, rest_ship):
        """
        Get ordered wait time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"v1/venues/{test_data['shipEatsFnb']['venue']['Venue']['VenueId']}/orderwaittimes")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content
        if len(_content) == 0:
            raise Exception('There is no OrderTypeId available for the chosen value')
        for _data in _content:
            check_assertions([
                'VenueId', 'OrderWaitTimeId', 'OrderTypeId', 'MinWaitTime', 'MaxWaitTime', 'IsDeleted', 'WaitTimeId'],
                _data)
        test_data['shipEatsFnb']['venue']['OrderTypeId'] = _content[0]['OrderTypeId']

    @pytestrail.case(10565604)
    def test_07_create_order_eats_verify_fnb(self, config, test_data, rest_ship, guest_data):
        """
        Create order from ship eats and verify in server and delivery manager
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders')
        body = {
            "GuestId": guest['reservationGuestId'],
            "AddedBy": guest['reservationGuestId'],
            "VenueId": test_data['shipEatsFnb']['venue']['Venue']['VenueId'],
            "OrderTypeId": test_data['shipEatsFnb']['shipEatsEatNowOrderTypeId'],
            "OrderOriginId": test_data['shipEatsFnb']['ShipEatsOrderOriginId'],
            "OrderDetails": [{
                "OrderQuantity": 1,
                "MenuItemId": test_data['shipEatsFnb']['menuItem']['MenuItemId'],
                "UnitPrice": int(test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['Price']),
                "UnitId": test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['UnitId'],
                "Amount": int(test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['Price']),
                "MenuItemOptionIds": [],
                "MenuItemOptionNames": []
            }],
            "IsDeliveryChargeApplied": True,
            "DeliveryAmount": 5,
            "Amount": 0,
            "Location": test_data['cabinNumber'],
            "OrderAllergies": [{"AllergyId": test_data['shipEatsFnb']['allergens']['id']}]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if 'Message' in _content and _content['Message'] == 'No account provided/found(check_id)':
            test_data['ship_eats_fnb_order'] = False
            pytest.skip("Not able to create order due to charge id issue")
        elif len(_content) != 0:
            check_assertions([
                'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'Location', 'OrderDate',
                'Status', 'GuestId', 'OrderNumber', 'AddedBy', 'Amount', 'OrderDetails', 'OrderAllergies'], _content)
            test_data['shipEatsFnb']['orderResponse'] = _content
            assert 1 == _content['Status'], "Ship Eats order did not get Booked !!"
            test_data['ship_eats_fnb_order'] = True
        else:
            raise Exception('No order data found!')

        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(config.ship.url, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception("Booked order from Ship Eats is not shown in server !!")
        assert _content['Status'] == 1, 'Status of booked from Ship Eats is not booked in server !!'

        url = urljoin(config.ship.url, 'fnbserver', f"/orders/{_order}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Booked order from Ship Eats is not shown in delivery manager !!")
        assert _content['Status'] == 1, 'Status of booked from Ship Eats is not booked in delivery manager !!'

    @pytestrail.case(11777692)
    def test_08_verify_allergies_fnb(self, config, test_data, rest_ship):
        """
        Verify the added allergies from ship eats are reflecting in server and delivery manager
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['ship_eats_fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(config.ship.url, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content['OrderAllergies']) == 0:
            raise Exception("Added Allergies is not reflecting in server !!")
        else:
            if not any(
                    d['AllergyId'] == test_data['shipEatsFnb']['allergens']['id'] for d in _content['OrderAllergies']):
                raise Exception('Allergy ID not found in server !!')

        url = urljoin(config.ship.url, 'fnbserver', f"/orders/{_order}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content

    @pytestrail.case(10565608)
    def test_09_deliver_order_fnb_verfiy_eats(self, config, test_data, rest_ship, guest_data):
        """
        Deliver order from fnb and verify in sailor app
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['ship_eats_fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        guest = guest_data[0]
        url = urljoin(config.ship.url, "fnbserver/orders")
        body = {
            "OrderIds": [test_data['shipEatsFnb']['orderResponse']['OrderId']], "UpdatedBy": test_data['personId'],
            "Status": 2, "VenueId": test_data['shipEatsFnb']['orderResponse']['VenueId']
        }
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        assert int(_content['Value']['Status']) == 2, "ERROR: Order Status != 2 !!"

        url = urljoin(config.ship.url, "fnbserver/Home/BumpOrder")
        body = {
            "VenueId": test_data['shipEatsFnb']['orderResponse']['VenueId'], "UserId": test_data['personId'],
            "OrderId": test_data['shipEatsFnb']['orderResponse']['OrderId'],
            "OrderNumber": test_data['shipEatsFnb']['orderResponse']['OrderNumber']
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['ReturnCode'] == 1001, 'Order is not bumped !!'
        assert _content['Message'] == 'OrderSuccessfullyBumped', 'Order is not bumped !!'

        url = urljoin(config.ship.url, "fnbserver/Home/DeliverOrder")
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['ReturnCode'] == 1005, 'Order is not delivered !!'
        assert _content['Message'] == 'OrderSuccessfullyDelivered', 'Order is not delivered !!'

        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders/search')
        body = {
            "StatusIds": "4",
            "GuestId": guest['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if not any(d['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId'] for d in _content):
            raise Exception('Ship Eats order is not showing in recent orders for Sailor !!')
        for _order in _content:
            if _order['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId']:
                assert _order['Status'] == 4, 'Order Delivered from Fnb is not getting updated in Ship Eats !!'

    @pytestrail.case(10565606)
    def test_10_cancel_order_eats_verify_server(self, config, test_data, rest_ship, guest_data):
        """
        Cancel the order from Ship Eats and verify that it gets removed from server
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['ship_eats_fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"/v1/orders/{test_data['shipEatsFnb']['orderResponse']['OrderId']}/cancel")
        body = {
            "OrderId": test_data['shipEatsFnb']['orderResponse']['OrderId'],
            "VenueId": test_data['shipEatsFnb']['venue']['Venue']['VenueId'],
            "OrderCancellations": [{
                "OrderId": test_data['shipEatsFnb']['orderResponse']['OrderId'],
                "CancellationRequestedBy": guest['reservationGuestId'],
                "AddedBy": guest['reservationGuestId'],
                "CancellationReason": "Canceled by sailor"
            }]
        }
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content
        check_assertions(['ReturnCode', 'Message', 'OrderNumber', 'GuestId', 'OrderOriginId', 'OrderTypeId'], _content)
        assert 1003 == _content['ReturnCode'], "ReturnCode Mismatch!!"
        assert 'OrderSuccessfullyCancelled' == _content['Message'], "Message Mismatch!!"

        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(config.ship.url, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        assert _content['Status'] == 5, 'Order Cancelled from ship eats is not reflecting in server !!'

    @pytestrail.case(11777693)
    def test_11_cancel_order_eats_verify_delivery_manager(self, config, test_data, rest_ship):
        """
        Cancel the order from Ship Eats and verify that it gets removed from delivery manager
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['ship_eats_fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        url = urljoin(config.ship.url, 'fnbserver', f"/orders/{_order}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        assert _content['Status'] == 5, 'Order Cancelled from ship eats is not reflecting in delivery manager !!'

    @pytestrail.case(11777694)
    def test_12_cancel_order_fnb_verify_eats(self, config, test_data, rest_ship, guest_data):
        """
        Cancel the order from delivery manager and verify the same in ship eats
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['ship_eats_fnb_order']:
            pytest.skip("Not able to create order due to charge id issue")
        guest = guest_data[0]
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders')
        body = {
            "GuestId": guest['reservationGuestId'],
            "AddedBy": guest['reservationGuestId'],
            "VenueId": test_data['shipEatsFnb']['venue']['Venue']['VenueId'],
            "OrderTypeId": test_data['shipEatsFnb']['shipEatsEatNowOrderTypeId'],
            "OrderOriginId": test_data['shipEatsFnb']['ShipEatsOrderOriginId'],
            "OrderDetails": [{
                "OrderQuantity": 1,
                "MenuItemId": test_data['shipEatsFnb']['menuItem']['MenuItemId'],
                "UnitPrice": int(test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['Price']),
                "UnitId": test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['UnitId'],
                "Amount": int(test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['Price']),
                "MenuItemOptionIds": [],
                "MenuItemOptionNames": []
            }],
            "IsDeliveryChargeApplied": True,
            "DeliveryAmount": 0,
            "Amount": 0,
            "Location": test_data['cabinNumber'],
            "OrderAllergies": [{"AllergyId": test_data['shipEatsFnb']['allergens']['id']}]
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        test_data['shipEatsFnb']['orderResponse'] = _content
        assert 1 == _content['Status'], "Ship Eats order did not get Booked !!"

        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        url = urljoin(config.ship.url, 'fnbserver', "/orders/cancel")
        body = {
            "OrderId": _order, "VenueId": test_data['shipEatsFnb']['venue']['Venue']['VenueId'],
            "OrderCancellations": [{
                "OrderId": _order,
                "CancellationRequestedBy": test_data['personId'],
                "AddedBy": test_data['personId'], "CancellationReason": "Wrong Order"
            }]
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['ReturnCode'] == 1003, 'ReturnCode != 1003'
        assert _content['Message'] == 'OrderSuccessfullyCancelled', 'Message != OrderSuccessfullyCancelled'

        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders/search')
        body = {
            "StatusIds": "5",
            "GuestId": guest['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if not any(d['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId'] for d in _content):
            raise Exception('Ship Eats order is not showing in recent orders for Sailor')
        for _order in _content:
            if _order['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId']:
                assert _order[
                           'Status'] == 5, 'Order Cancelled from delivery manager is not getting updated in Ship Eats !!'

    @pytestrail.case(24864560)
    def test_13_create_order_fnb_verify_eats(self, config, test_data, rest_ship, guest_data):
        """
        Create the order from server and verify in ship eats
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        url = urljoin(config.ship.url, "/fnbserver/Home/CreateOrder")
        body = {
            "VenueId": test_data['shipEatsFnb']['venue']['Venue']['VenueId'], "GuestId": guest['reservationGuestId'],
            "Gratuity": 0, "Amount": 7.25,
            "TaxAmount": 0, "TaxPercentage": 0, "GratuityPercentage": 15,
            "AddedBy": test_data['personId'], "OrderTypeId": "71b536df-b9ec-11e9-b327-16345b88f44a",
            "OrderOriginId": "71b536e3-b9ec-11e9-b327-16345b88f44a",
            "OrderDetails": [{
                "MenuItemId": test_data['shipEatsFnb']['menuItem']['MenuItemId'], "OrderQuantity": 1, "UnitPrice": 7.25,
                "TaxAmount": 0, "Amount": 7.25,
                "UnitId": test_data['shipEatsFnb']['menuItem']['MenuItemPrices'][0]['UnitId']
            }],
            "AdditionalNotes": ""
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if 'No account provided/found(check_id)' in _content:
            test_data['ship_Eats_Fnb'] = False
            pytest.skip("Not able to create order due to charge id issue")
        elif len(_content) != 0:
            is_key_there_in_dict('OrderId', json.loads(_content))
            test_data['shipEatsFnb']['orderResponse'] = json.loads(_content)
            test_data['ship_Eats_Fnb'] = True
        else:
            raise Exception('No order data found!')

        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), '/v1/orders/search')
        body = {
            "StatusIds": "1",
            "GuestId": guest['reservationGuestId']
        }
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if not any(d['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId'] for d in _content):
            raise Exception('Order crated from server is not showing in sailor app !!')
        for _order in _content:
            if _order['OrderId'] == test_data['shipEatsFnb']['orderResponse']['OrderId']:
                assert _order[
                           'Status'] == 1, 'Order booked from server is not updating in sailor app !!'

    @pytestrail.case(16902499)
    def test_14_check_shake_for_champagne_get_data(self, config, rest_ship):
        """
        Get the static data for Champagne
        :param config:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "resources/shakeforchampagne")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content

        is_key_there_in_dict('landing', _content)
        is_key_there_in_dict('landingPushButton', _content)
        is_key_there_in_dict('landingBottlesPanel', _content)
        is_key_there_in_dict('confirmation', _content)
        is_key_there_in_dict('confirmationCancel', _content)
        is_key_there_in_dict('error', _content)

    @pytestrail.case(16907912)
    def test_15_champagne_order_details(self, config, test_data, rest_ship):
        """
        Get the Champagne order venue and menu item details
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "v1/menuitems/champagne")
        _content = rest_ship.send_request(method="GET", url=_url, auth="user").content

        is_key_there_in_dict('OrderTypeId', _content)
        is_key_there_in_dict('OrderOriginId', _content)
        is_key_there_in_dict('MaximumBottlesAllowed', _content)

        test_data['menuItemID'] = _content['MenuItemDetails']['MenuItemId']
        test_data['menuItemNumber'] = _content['MenuItemDetails']['MenuItemNumber']
        for menuitem in _content['MenuItemDetails']['MenuItemPrices']:
            test_data['unitId'] = menuitem['UnitId']
            test_data['price'] = menuitem['Price']
        test_data['venueId'] = _content['VenueDetails']['VenueId']
        test_data['orderTypeId'] = _content['OrderTypeId']
        test_data['orderOriginId'] = _content['OrderOriginId']

    @pytestrail.case(24886214)
    def test_16_create_champagne_order_verify_fnb(self, config, test_data, rest_ship, guest_data):
        """
        Order the champagne for guest from sailor app and check in fnb server
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        guest = guest_data[0]
        test_data['taxAmount'] = 14
        body = {
            "OrderTypeId": test_data['orderTypeId'],
            "OrderOriginId": test_data['orderOriginId'],
            "VenueId": test_data['venueId'],
            "GuestId": guest['reservationGuestId'],
            "AddedBy": guest['reservationGuestId'],
            "TaxAmount": test_data['taxAmount'],
            "Amount": test_data['taxAmount'] + int(test_data['price']),
            "OrderDetails": [{
                "OrderQuantity": 1,
                "MenuItemId": test_data['menuItemID'],
                "UnitPrice": int(test_data['price']),
                "UnitId": test_data['unitId'],
                "TaxAmount": test_data['taxAmount'],
                "Amount": int(test_data['price'])
            }]
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "v1/orders")
        _content = rest_ship.send_request(method="POST", url=_url, json=body, auth="user").content
        if _content['Message'] == 'NotAvailableOnLocation':
            test_data['simulator_enabled'] = False
            pytest.skip('Simulator is not enabled')
        test_data['simulator_enabled'] = True
        test_data['shipEatsFnb']['orderResponse'] = _content
        assert 1 == _content['Status'], "Status of order is not booked"
        is_key_there_in_dict('OrderId', _content)

        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(config.ship.url, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception("Booked order from Shake for Champagne is not shown in server !!")
        assert _content['Status'] == 1, 'Status of Shake for Champagne order is not booked in server !!'

        url = urljoin(config.ship.url, 'fnbserver', f"/orders/{_order}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Booked order from Shake for Champagne is not shown in delivery manager !!")
        assert _content['Status'] == 1, 'Status of Shake for Champagne order is not booked in delivery manager !!'

    @pytestrail.case(24886215)
    def test_17_cancel_champagne_order_verify_fnb(self, config, test_data, rest_ship, guest_data):
        """
        cancel the champagne for guest from sailor app and check in fnb server
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        if not test_data['simulator_enabled']:
            pytest.skip('Simulator is not enabled')
        guest = guest_data[0]
        body = {
            "OrderId": test_data['shipEatsFnb']['orderResponse']['OrderId'],
            "VenueId": test_data['shipEatsFnb']['orderResponse']['VenueId'],
            "OrderCancellations": [{
                "OrderId": test_data['shipEatsFnb']['orderResponse']['OrderId'],
                "CancellationRequestedBy": guest['reservationGuestId'],
                "CancellationReason": "I have changed my mind",
                "AddedBy": guest['reservationGuestId']
            }]
        }
        _url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                       f"v1/orders/{test_data['shipEatsFnb']['orderResponse']['OrderId']}/cancel")
        _content = rest_ship.send_request(method="PUT", url=_url, json=body, auth="user").content
        assert "OrderSuccessfullyCancelled" == _content['Message'], "Champagne Order is not cancelled !!"
        assert guest['reservationGuestId'] == _content['GuestId'], "Guest Id is not matching for order is cancelled!!"
        assert test_data['orderOriginId'] == _content[
            'OrderOriginId'], "Order Origin Id is not matching for cancel order"
        assert test_data['orderTypeId'] == _content['OrderTypeId'], "Order Type Id is not matching for cancel order"

        _order = test_data['shipEatsFnb']['orderResponse']['OrderId']
        params = {
            'id': _order
        }
        url = urljoin(config.ship.url, "/fnbserver/Home/GetByOrderId")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception("Cancelled order from Shake for Champagne is not shown in server !!")
        assert _content['Status'] == 5, 'Status of Shake for Champagne order is not cancelled in server !!'

        url = urljoin(config.ship.url, 'fnbserver', f"/orders/{_order}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Cancelled order from Shake for Champagne is not shown in delivery manager !!")
        assert _content['Status'] == 5, 'Status of Shake for Champagne order is not cancelled in delivery manager !!'
