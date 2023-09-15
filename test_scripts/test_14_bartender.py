__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.BAR_TENDER
@pytest.mark.run(order=15)
class TestBartender:
    """
    Test Suite to test Bartender

    """

    @pytestrail.case(457)
    def test_01_get_venue_list(self, config, test_data, rest_ship):
        """
        Get F&B Venues List
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        user_id = test_data['personId']
        params = {"userId": user_id, "requestedBy": "DM"}
        url = urljoin(config.ship.url, "/fnbserver/venues")
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for venue in _content:
                is_key_there_in_dict('VenueId', venue)
                test_data['Venue_Id'] = venue['VenueId']
            test_data['venues'] = _content
        else:
            raise Exception('No venue found!')

    @pytestrail.case(458)
    def test_02_get_menu_items(self, config, test_data, rest_ship):
        """
        Get F&B Menu Items
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venues = test_data['venues']
        for count, venue in enumerate(venues):
            _venue = venue['VenueId']
            url = urljoin(config.ship.url, f"/fnbserver/Menu/menuitems?venueId={_venue}")
            _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
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
                venues[count]['menuItems'] = _content
                break
            else:
                raise Exception('No menu item found!')
        test_data['venues'] = venues

    @pytestrail.case(459)
    def test_03_create_order(self, config, test_data, rest_ship, guest_data):
        """
        Create F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :param guest_data:
        :return:
        """
        venues = test_data['venues']
        guest = guest_data[0]
        # Reservation Guest ID is different for VV and DXP (case change)
        _id = guest['reservationGuestId']

        for venue in venues:
            url = urljoin(config.ship.url, "/fnbserver/Home/CreateOrder")
            menu_items = random.choice(venue['menuItems'])
            body = {
                "VenueId": venue['VenueId'], "GuestId": _id, "Gratuity": 0, "Amount": 7.25,
                "TaxAmount": 0, "TaxPercentage": 0, "GratuityPercentage": 15,
                "AddedBy": test_data['personId'], "OrderTypeId": "71b536df-b9ec-11e9-b327-16345b88f44a",
                "OrderOriginId": "71b536e3-b9ec-11e9-b327-16345b88f44a",
                "OrderDetails": [{
                    "MenuItemId": menu_items['MenuItemId'], "OrderQuantity": 1, "UnitPrice": 7.25,
                    "TaxAmount": 0, "Amount": 7.25,
                    "UnitId": menu_items['MenuItemPrices'][0]['UnitId']
                }],
                "AdditionalNotes": ""
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if 'No account provided/found(check_id)' in _content:
                test_data['fnb_order'] = False
                pytest.skip("Not able to create order due to charge id issue")
            elif len(_content) != 0:
                is_key_there_in_dict('OrderId', json.loads(_content))
                test_data['bar'].append(json.loads(_content))
                test_data['bartab_order'] = True
                break
        else:
            raise Exception('Not able to create order for any venue')

    @pytestrail.case(460)
    def test_04_verify_created_order(self, config, test_data, rest_ship):
        """
        Verify F&B Created Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/orders/{_order}")
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if _content['Status'] != 1:
                raise Exception("Order Status != 1")

    @pytestrail.case(461)
    def test_05_place_on_deck_order(self, config, test_data, rest_ship):
        """
        Place an F&B On-Deck Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            url = urljoin(config.ship.url, "/fnbserver/orders")
            body = {
                "OrderIds": [_data['OrderId']], "UpdatedBy": test_data['personId'],
                "Status": 2, "VenueId": _data['VenueId']
            }
            _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
            test_data['bar'][count]['OrderId'] = _content['Value']['OrderIds'][0]
            if int(_content['Value']['Status']) != 2:
                raise Exception("ERROR: Order Status != 2")

    @pytestrail.case(468)
    def test_06_verify_placed_on_deck_order(self, config, test_data, rest_ship):
        """
        Verify Cancelled Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/orders/{_order}")
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if _content['Status'] != 2:
                raise Exception("Order Status != 2")

    @pytestrail.case(462)
    def test_07_bump_order(self, config, test_data, rest_ship):
        """
        Bump F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            url = urljoin(config.ship.url, "/fnbserver/orders")
            body = {
                "OrderIds": [_data['OrderId']], "UpdatedBy": test_data['personId'],
                "Status": 3, "VenueId": _data['VenueId']
            }
            _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
            test_data['bar'][count]['OrderId'] = _content['Value']['OrderIds'][0]
            if int(_content['Value']['Status']) != 3:
                raise Exception("ERROR: Order Status != 3")

    @pytestrail.case(467)
    def test_08_verify_bumped_order(self, config, test_data, rest_ship):
        """
        Verify Cancelled Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/orders/{_order}")
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if _content['Status'] != 3:
                raise Exception("Order Status != 3")

    @pytestrail.case(463)
    def test_09_deliver_order(self, config, test_data, rest_ship):
        """
        Deliver F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            url = urljoin(config.ship.url, "/fnbserver/orders")
            body = {
                "OrderIds": [_data['OrderId']], "UpdatedBy": test_data['personId'],
                "Status": 4, "VenueId": _data['VenueId']
            }
            _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
            test_data['bar'][count]['OrderId'] = _content['Value']['OrderIds'][0]
            if int(_content['Value']['Status']) != 4:
                raise Exception("ERROR: Order Status != 4")

    @pytestrail.case(466)
    def test_10_verify_delivered_order(self, config, test_data, rest_ship):
        """
        Verify Cancelled Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/orders/{_order}")
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if _content['Status'] != 4:
                raise Exception("Order Status != 4")

    @pytestrail.case(464)
    def test_11_cancel_order(self, config, test_data, rest_ship):
        """
        Cancel F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            url = urljoin(config.ship.url, "/fnbserver/orders/cancel")
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

    @pytestrail.case(465)
    def test_12_verify_cancelled_order(self, config, test_data, rest_ship):
        """
        Verify Cancelled Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['bar']):
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/orders/{_order}")
            _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
            if _content['Status'] != 5:
                raise Exception("Order Status != 5")

    @pytestrail.case(67857568)
    def test_13_search_guest(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B guest
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            _id = guest_data[0]['reservationGuestId']
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/Orders/Search/{_order}")
            body = {
                "TeamMemberId": "" , "GuestId": _id , "MenuItems":"",
                "OrderNumber":"" , "VenueId": _data['VenueId'],
                "IncludeAdditionalData":True , "SearchGuestCrew": True ,
                "OrderDeliveredAt":"", "OrderDate":test_data['OrderDate']
            }

            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if ( len(_content) != 0 ) and (_content != _id ) :
                raise Exception("Couldn't find guest")

    @pytestrail.case(67857600)
    def test_14_search_menu_item(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B menu_item
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/Orders/Search/{_order}")
            body = {
                "TeamMemberId": "", "GuestId":"", "MenuItems": _data['menuItems'],
                "OrderNumber": "", "VenueId": _data['VenueId'],
                "IncludeAdditionalData": True, "SearchGuestCrew": True,
                "OrderDeliveredAt": "", "OrderDate": test_data['OrderDate']
            }

            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if (len(_content) != 0) and (_content != _data['menuItems']):
                raise Exception("Couldn't find menu item")

    @pytestrail.case(67857601)
    def test_15_search_order(self, config, test_data, rest_ship, guest_data):
        """
        Search F&B Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/Orders/Search/{_order}")
            body = {
                "TeamMemberId": "", "GuestId":"", "MenuItems": "",
                "OrderNumber": _data['OrderNumber'], "VenueId": _data['VenueId'],
                "IncludeAdditionalData": True, "SearchGuestCrew": True,
                "OrderDeliveredAt": "", "OrderDate": test_data['OrderDate']
            }

            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if (len(_content) != 0) and (_content != _data['OrderNumber']):
                raise Exception("Couldn't find order")

    @pytestrail.case(67857602)
    def test_16_filter_order_action_needed(self, config, test_data, rest_ship, guest_data):
        """
        filter order on basis of action needed
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            _order = _data['OrderId']
            params = {"requestedBy": "DM"}
            url = urljoin(config.ship.url, f"/fnbserver/Orders/Search/{_order}")
            body = {
                "StatusIds":"5", "showActionNeeded":True,"selectActionNeeded":True,
                "OrderDate":test_data['OrderDate'], "OrderEndDate":"",
                "IncludePartialCancelled":True,"VenueId": _data['VenueId'],
                "SearchWithCancelledDate": True
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if _content['ActionNeeded'] != True:
                raise Exception("no order data found")

    @pytestrail.case(68357249)
    def test_17_order_wait_times(self, config, test_data, rest_ship, guest_data):
        """
        Order wait times
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            for count, venue in enumerate(venue):
                _venue = venue['VenueId']
            _ship = config.ship.url
            _order = _data['OrderId']
            url = urljoin(config.ship.url, f"/fnbserver/venues/venueId={_venue}/orderwaittimes")
            body = {
                "OrderWaitTimeId": "",
                "OrderTypeId": _data["OrderTypeId"],
                "VenueId": _data['VenueId'],
                "MinWaitTime": 20,
                "MaxWaitTime": 30,
                "IsDeleted": False,
                "WaitTimeId": ""
            }
            _content = rest_ship.send_request(method="GET", url=url, json=body, auth="crew").content
            if _content['OrderTypeId'] == 0:
                raise Exception("no order wait times")

    @pytestrail.case(68357250)
    def test_18_filter_Delivered_order(self, config, test_data, rest_ship):
        """
        Filter order on the delivered tab
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            url = urljoin(_ship, "fnbserver/Orders/search?requestedBy=DM")
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
                raise Exception("no order is to be delivered for the selection")

    @pytestrail.case(68357251)
    def test_19_filter_cancelled_order(self, config, test_data, rest_ship, ):
        """
        Filter order on the cancelled tab
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        if not test_data['bar']:
            pytest.skip("Not able to create order due to charge id issue")
        for count, _data in enumerate(test_data['fnb']):
            _ship = config.ship.url
            url = urljoin(_ship, "fnbserver/Orders/search?requestedBy=DM")
            body = {

                "VenueId": _data['VenueId'],
                "OrderDate": _data['OrderDate'],
                "statusIds": "5", "OrderDeliveredAt": "",
                "IncludePartialCancelled": True, "SearchWithCancelledDate": True
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if (_content['IncludePartialCancelled'] != True) and (_content['SearchWithCancelledDate'] != True):
                raise Exception("no cancelled orders available")