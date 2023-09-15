__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.VENUE_MANAGER
@pytest.mark.run(order=19)
class TestVenueManager:
    """
    Test Suite to test Venue Manager

    """

    @pytestrail.case(15956405)
    def test_01_venue_manager_role(self, config, rest_ship):
        """
        Get Venue Manager Role
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'), "/userroles")
        params = {
            "includeSubModules": 'true',
            "applicationID": 'ff7dc28e-c3bf-468b-9ea8-e11dc4295bbf'
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception("Role data does not exist!!")
        else:
            is_key_there_in_dict('applications', _content)
            is_key_there_in_dict('modules', _content)
            for module in _content['modules']:
                is_key_there_in_dict('roles', module)
                for role in module['roles']:
                    is_key_there_in_dict('applicationRoleId', role)
                    is_key_there_in_dict('name', role)
                    is_key_there_in_dict('code', role)
                    is_key_there_in_dict('features', role)
                    for feature in role['features']:
                        is_key_there_in_dict('applicationFeatureId', feature)
                        is_key_there_in_dict('name', feature)
                        is_key_there_in_dict('code', feature)

    @pytestrail.case(381535)
    def test_02_venue_data(self, config, request, test_data, rest_ship):
        """
        Get Venue Manager Venues List
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/venue_data.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        user_id = test_data['personId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), f"/v1/users/{user_id}/venues")
        params = {
            "roleId": 'a480d8d5-3240-4818-a0ee-df865fe36ee6',
            "getNearByVenues": 'false'
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            raise Exception("Venue data does not exist!!")
        else:
            for venue in _content:
                if venue['VenueId'] == _ship_data['VenueId']:
                    for _key in _ship_data:
                        is_key_there_in_dict(_key, venue)
                    for _key in _ship_data['VenueType']:
                        is_key_there_in_dict(_key, venue['VenueType'])
            test_data['VenueManagerVenues'] = _content

    @pytestrail.case(381536)
    def test_03_order_wait_times(self, config, test_data, rest_ship):
        """
        Get order wait times
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), f"/v1/venues/{venue_id}/orderwaittimes")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        test_data['OrderWaitTimes'] = _content

    @pytestrail.case(15956406)
    def test_04_ship_time(self, config, test_data, rest_ship):
        """
        Get ship time
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/ship/shiptime")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Ship Time data does not exist!!")
        else:
            is_key_there_in_dict('ShipTimeOffset', _content)
            is_key_there_in_dict('ShipTime', _content)
            test_data['ShipTime'] = _content['ShipTime']

    @pytestrail.case(15956407)
    def test_05_select_venue(self, config, request, test_data, rest_ship):
        """
        Get select venue
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/venue_data.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), f"/v1/venues/{venue_id}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("venue data does not exist!!")
        else:
            for _key in _ship_data:
                is_key_there_in_dict(_key, _content)
            for _key in _ship_data['VenueType']:
                is_key_there_in_dict(_key, _content['VenueType'])

    @pytestrail.case(15956408)
    def test_06_venue_delivery_off(self, config, test_data, rest_ship):
        """
        Toggle Delivery OFF
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/venues/{venue_id}/foodDeliveryAvailability/false")
        body = {"VenueId": venue_id, "IsDeliveryAvailable": "false"}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if not _content:
            raise Exception("delivery not updated")

    @pytestrail.case(15956409)
    def test_07_venue_delivery_on(self, config, test_data, rest_ship):
        """
        Toggle Delivery ON
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/venues/{venue_id}/foodDeliveryAvailability/true")
        body = {"VenueId": venue_id, "IsDeliveryAvailable": "true"}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if not _content:
            raise Exception("delivery not updated")

    @pytestrail.case(15956410)
    def test_08_add_meal_period_capacity(self, config, test_data, rest_ship):
        """
        add meal period inventory
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        _today = test_data['ShipTime'].split('T')[0]
        user_id = test_data['personId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/menuitems/mealperiods")
        params = {
            "venueId": venue_id,
            "startDate": _today,
            "endDate": _today,
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for meal_period in _content:
                is_key_there_in_dict('MealPeriodId', meal_period)
                is_key_there_in_dict('MealPeriodType', meal_period)
                is_key_there_in_dict('Name', meal_period)
                is_key_there_in_dict('MealPeriodEffectiveWindows', meal_period)
                for MealPeriodEffectiveWindow in meal_period['MealPeriodEffectiveWindows']:
                    is_key_there_in_dict('MealPeriodEffectiveWindowId', MealPeriodEffectiveWindow)
                    is_key_there_in_dict('StartDate', MealPeriodEffectiveWindow)
                    is_key_there_in_dict('EndDate', MealPeriodEffectiveWindow)
                    MealPeriodEffectiveWindow.update({'Capacity': '100'})
            url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                          f"/v1/menuitems/mealperiods/Venue/{venue_id}/User/{user_id}")
            _content = rest_ship.send_request(method="POST", url=url, json=_content, auth="crew").content
            if not _content:
                raise Exception("capacity not added")

    @pytestrail.case(15956411)
    def test_09_add_preorder_slot(self, config, test_data, rest_ship):
        """
        Add Preorder Slot
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        _today = test_data['ShipTime'].split('T')[0]
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/PreOrders/timeslots?venueId={venue_id}&startDate={_today}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            venue_id = test_data['venueId']
            _today = test_data['ShipTime'].split('T')[0]
            _slotdate = f"{_today}T00:00:00"
            _starttime = f"{_today}T22:30:00"
            user_id = test_data['personId']
            url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/PreOrders/preordertimeslots")
            body = {
                "PreOrderSlotDetails": [
                    {"VenueId": venue_id, "PreOrderSlotDetailId": None, "PreOrderSlotDate": _slotdate,
                     "StartTime": _starttime, "EndTime": _starttime, "EditCutOffTime": _starttime,
                     "LastModifiedBy": user_id, "IsPreOrderAvailable": True, "PreOrderSlots": [{
                        "PreOrderSlotId": None, "PreOrderSettingId": None, "StartTime": '23:30:00',
                        "EndTime": '23:45:00', "OrderInventory": "100"}]}], "SaveAsTemplate": False,
                "TemplateName": None}
            _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
            if len(_content) == 0:
                raise Exception("preorder slot not added")
            else:
                for preorder in _content:
                    is_key_there_in_dict('VenueId', preorder)
                    is_key_there_in_dict('PreOrderSlotDetailId', preorder)
                    is_key_there_in_dict('PreOrderSlotDate', preorder)
                    is_key_there_in_dict('StartTime', preorder)
                    is_key_there_in_dict('EndTime', preorder)
                    is_key_there_in_dict('EditCutOffTime', preorder)
                    is_key_there_in_dict('LastModifiedBy', preorder)
                    is_key_there_in_dict('IsPreOrderAvailable', preorder)
                    is_key_there_in_dict('PreOrderSlots', preorder)
                    for PreOrderSlot in preorder['PreOrderSlots']:
                        is_key_there_in_dict('PreOrderSlotId', PreOrderSlot)
                        is_key_there_in_dict('PreOrderSettingId', PreOrderSlot)
                        is_key_there_in_dict('StartTime', PreOrderSlot)
                        is_key_there_in_dict('EndTime', PreOrderSlot)
                        is_key_there_in_dict('OrderInventory', PreOrderSlot)

    @pytestrail.case(15958673)
    def test_10_menu_items(self, config, request, test_data, rest_ship):
        """
        Get Menu Items
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/menu_items.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/MenuItems")
        params = {
            "VenueId": venue_id
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) == 0:
            pytest.mark.skip("Menu Item data does not exist!!")
        else:
            for menuitem in _content:
                for _key in _ship_data:
                    is_key_there_in_dict(_key, menuitem)
                for _key in _ship_data['MenuItemType']:
                    is_key_there_in_dict(_key, menuitem['MenuItemType'])
                for MenuItemIngredient in menuitem['MenuItemIngredients']:
                    for _key in _ship_data['MenuItemIngredients']:
                        is_key_there_in_dict(_key, MenuItemIngredient)
                for MenuItemPrice in menuitem['MenuItemPrices']:
                    for _key in _ship_data['MenuItemPrices']:
                        is_key_there_in_dict(_key, MenuItemPrice)
                for MealPeriodMenuItem in menuitem['MealPeriodMenuItems']:
                    for _key in _ship_data['MealPeriodMenuItems']:
                        is_key_there_in_dict(_key, MealPeriodMenuItem)
                for MealPeriodMenuItem in menuitem['MealPeriodMenuItems']:
                    for _key in _ship_data['MealPeriodMenuItems']:
                        is_key_there_in_dict(_key, MealPeriodMenuItem)
                    for _key in _ship_data['MealPeriodMenuItems']['MealPeriod']:
                        is_key_there_in_dict(_key, MealPeriodMenuItem['MealPeriod'])
                for MenuItemAllergy in menuitem['MenuItemAllergies']:
                    for _key in _ship_data['MenuItemAllergies']:
                        is_key_there_in_dict(_key, MenuItemAllergy)
                for MenuItemOption in menuitem['MenuItemOptions']:
                    for _key in _ship_data['MenuItemOptions']:
                        is_key_there_in_dict(_key, MenuItemOption)

    @pytestrail.case(15960935)
    def test_11_menu_items_filter(self, config, test_data, rest_ship):
        """
        Get Menu Items Filter
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/menuitemfilters")
        params = {
            "VenueId": venue_id
        }
        rest_ship.send_request(method="GET", url=url, params=params, auth="crew")

    @pytestrail.case(381537)
    def test_12_server_data(self, config, request, test_data, rest_ship):
        """
        Get Server Data
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/voyage_data.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/server/data")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        test_data['voyageEmbarkDate'] = _content['voyage']['embarkDate']
        test_data['voyageDebarkDate'] = _content['voyage']['debarkDate']
        if len(_content) == 0:
            raise Exception("Voyage data does not exist!!")
        else:
            for voyage in _ship_data:
                if voyage['embarkDate'] == test_data['voyageEmbarkDate'] and voyage['embarkDate'] == test_data[
                    'voyageDebarkDate']:
                    for _key in voyage:
                        is_key_there_in_dict(_key, _content['voyage'])
                    for voyageItinerary in _content['voyage']['voyageItineraries']:
                        for itinerary in voyage['voyageItineraries']:
                            if itinerary['itineraryDay'] == voyageItinerary['itineraryDay']:
                                for _key in itinerary:
                                    is_key_there_in_dict(_key, voyageItinerary)

    @pytestrail.case(381538)
    def test_13_order_types(self, config, rest_ship):
        """
        Get Order Types
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/ordertypes")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Order type data does not exist!!")
        else:
            for order in _content:
                is_key_there_in_dict('OrderTypeId', order)
                is_key_there_in_dict('OrderTypeName', order)
                is_key_there_in_dict('IsRecordDeleted', order)
                is_key_there_in_dict('AddedDateTime', order)
                is_key_there_in_dict('LastModifiedDateTime', order)
                is_key_there_in_dict('Order', order, False)

    @pytestrail.case(381539)
    def test_14_order_cancellation_reasons(self, config, rest_ship):
        """
        Get Order Cancellation Reasons
        :param config:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/orderCancellationReasons")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for order_cancellation_reason in _content:
                is_key_there_in_dict('CancellationReasonId', order_cancellation_reason)
                is_key_there_in_dict('CancellationReason', order_cancellation_reason)

    @pytestrail.case(381540)
    def test_15_meal_periods(self, config, test_data, rest_ship):
        """
        Get Meal Periods
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']

        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), f"/v1/menuitems/mealperiods")
        params = {
            "venueId": venue_id,
            "startDate": test_data['embarkDate'],
            "endDate": test_data['debarkDate']
        }
        _content = rest_ship.send_request(method="GET", url=url, params=params, auth="crew").content
        if len(_content) != 0:
            for meal_period in _content:
                is_key_there_in_dict('MealPeriodId', meal_period)
                is_key_there_in_dict('MealPeriodType', meal_period)
                is_key_there_in_dict('Name', meal_period)
                is_key_there_in_dict('MealPeriodEffectiveWindows', meal_period)
                for MealPeriodEffectiveWindow in meal_period['MealPeriodEffectiveWindows']:
                    is_key_there_in_dict('MealPeriodEffectiveWindowId', MealPeriodEffectiveWindow)
                    is_key_there_in_dict('StartDate', MealPeriodEffectiveWindow)
                    is_key_there_in_dict('EndDate', MealPeriodEffectiveWindow)

    @pytestrail.case(381541)
    def test_16_dashboard_counts(self, config, request, test_data, rest_ship):
        """
        Get Dashboard Counts
        :param config:
        :param request:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath,
                                       'test_data/verification_data/venue_manager_dashboard_data.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/VenueAdmin/venues/{venue_id}/dashboardCounts")
        body = {
            "DeliveryPersonIds": None, "PlacedByPersonIds": None, "GuestIds": None, "TeamMemberIds": None,
            "StatusIds": None, "VenueId": venue_id, "OrderDate": test_data['voyageEmbarkDate'], "OrderEndDate": None,
            "MinWaitTime": "30", "MaxWaitTime": "40", "DeliveryTimeLimit": "15"
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        for _key in _ship_data:
            is_key_there_in_dict(_key, _content, False)
        for _key in _ship_data['VenueAdminOrderStaticsDetails']:
            is_key_there_in_dict(_key, _content['VenueAdminOrderStaticsDetails'])

    @pytestrail.case(381542)
    def test_17_search_order(self, config, test_data, rest_ship):
        """
        Get Search Order
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        params = {"page": "1", "size": "10", "orderby": "orderdate,desc"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/orders/search")
        for count, _data in enumerate(test_data['bar']):
            body = {
                "DeliveryPersonIds": None, "PlacedByPersonIds": None, "MenuItems": None, "OrderDeliveredAt": None,
                "GuestIds": None, "TeamMemberIds": None, "GuestId": None, "Status": 5, "DeliveryPersonId": None,
                "OfferId": None, "VenueId": _data['VenueId'], "OrderDate": "", "IncludeAdditionalData": "false",
                "IncludeGuestData": "false", "LocationId": None, "TokenNumber": None,
                "OrderNumber": _data['OrderNumber'], "OrderEndDate": "", "StatusIds": None, "GetAllOrders": False,
                "FindByVoyage": None, "SearchGuestCrew": False, "IncludeTeamMemberData": "false",
                "IncludeLocation": None, "OrderTypeIds": None, "Embarkdate": None, "SearchKeyword": None
            }
            _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
            is_key_there_in_dict('Items', _content)
            for order in _content['Items']:
                check_assertions([
                    'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'OrderDate', 'Status', 'CurrentShipTime',
                    'TokenNumber', 'HasOtherAllergy', 'ColorCode', 'GuestId',
                    'DeliverToGuestId', 'OrderNumber', 'DeliveryPersonId', 'UpdatedBy', 'UpdatedBy', 'AddedBy',
                    'TaxAmount', 'Gratuity', 'Amount', 'ModifiedDate', 'DeliveryDate', 'AdditionalNotes',
                    'IsPickPlatesRequested', 'IsDeliveryChargeApplied', 'OrderCancellations', 'OrderDetails',
                    'OrderAllergies',
                ], order)

                assert order['VenueId'] == _data['VenueId'], "Venue Id is not matching !!"
                assert order['OrderNumber'] == _data['OrderNumber'], "OrderNumber is not matching !!"
                assert order['Status'] == 5, "Order Status != 5 !!"

    @pytestrail.case(15960936)
    def test_18_active_orders(self, config, test_data, rest_ship):
        """
        Get Active Orders
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _today = test_data['ShipTime'].split('T')[0]
        venue_id = test_data['venueId']
        params = {"page": "1", "size": "10", "orderby": "orderdate,desc"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/orders/search")
        body = {
            "DeliveryPersonIds": None, "PlacedByPersonIds": None, "MenuItems": None, "OrderDeliveredAt": None,
            "GuestIds": None, "TeamMemberIds": None, "GuestId": None, "Status": 0, "DeliveryPersonId": None,
            "OfferId": None, "VenueId": venue_id, "OrderDate": _today, "IncludeAdditionalData": "false",
            "IncludeGuestData": "false", "LocationId": None, "TokenNumber": None,
            "OrderNumber": None, "OrderEndDate": "", "StatusIds": "1,2,3", "GetAllOrders": False,
            "FindByVoyage": None, "SearchGuestCrew": False, "IncludeTeamMemberData": "false",
            "IncludeLocation": None, "OrderTypeIds": None, "Embarkdate": None, "SearchKeyword": None
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('Items', _content)
            for order in _content['Items']:
                check_assertions([
                    'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'OrderDate', 'Status', 'CurrentShipTime',
                    'TokenNumber', 'HasOtherAllergy', 'ColorCode', 'GuestId',
                    'DeliverToGuestId', 'OrderNumber', 'AddedBy', 'TaxAmount', 'Gratuity', 'Amount', 'ModifiedDate',
                    'AdditionalNotes', 'IsPickPlatesRequested', 'IsDeliveryChargeApplied', 'OrderCancellations',
                    'OrderDetails', 'OrderAllergies', ], order)

    @pytestrail.case(15960937)
    def test_19_delivered_orders(self, config, verification, test_data, rest_ship):
        """
        Get delivered orders
        :param config:
        :param verification:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data = verification.order_data
        _today = test_data['ShipTime'].split('T')[0]
        venue_id = test_data['venueId']
        params = {"page": "1", "size": "10", "orderby": "orderdate,desc"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/orders/search")
        body = {
            "DeliveryPersonIds": None, "PlacedByPersonIds": None, "MenuItems": None, "OrderDeliveredAt": None,
            "GuestIds": None, "TeamMemberIds": None, "GuestId": None, "Status": 0, "DeliveryPersonId": None,
            "OfferId": None, "VenueId": venue_id, "OrderDate": _today, "IncludeAdditionalData": "false",
            "IncludeGuestData": "false", "LocationId": None, "TokenNumber": None,
            "OrderNumber": None, "OrderEndDate": "", "StatusIds": "4", "GetAllOrders": False,
            "FindByVoyage": None, "SearchGuestCrew": False, "IncludeTeamMemberData": "false",
            "IncludeLocation": None, "OrderTypeIds": None, "Embarkdate": None, "SearchKeyword": None
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('Items', _content)
            for order in _content['Items']:
                check_assertions([
                    'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'OrderDate', 'Status', 'CurrentShipTime',
                    'TokenNumber', 'HasOtherAllergy', 'ColorCode', 'GuestId',
                    'DeliverToGuestId', 'OrderNumber', 'DeliveryPersonId', 'UpdatedBy', 'UpdatedBy', 'AddedBy',
                    'TaxAmount', 'Gratuity', 'Amount', 'ModifiedDate', 'DeliveryDate', 'AdditionalNotes',
                    'IsPickPlatesRequested', 'IsDeliveryChargeApplied', 'OrderCancellations', 'OrderDetails',
                    'OrderAllergies',
                ], order)

    @pytestrail.case(15960938)
    def test_20_cancelled_orders(self, config, verification, test_data, rest_ship):
        """
        Get Cancelled Order
        :param config:
        :param verification:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship_data = verification.order_data
        _today = test_data['ShipTime'].split('T')[0]
        venue_id = test_data['venueId']
        params = {"page": "1", "size": "10", "orderby": "orderdate,desc"}
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/orders/search")
        body = {
            "DeliveryPersonIds": None, "PlacedByPersonIds": None, "MenuItems": None, "OrderDeliveredAt": None,
            "GuestIds": None, "TeamMemberIds": None, "GuestId": None, "Status": 0, "DeliveryPersonId": None,
            "OfferId": None, "VenueId": venue_id, "OrderDate": _today, "IncludeAdditionalData": "false",
            "IncludeGuestData": "false", "LocationId": None, "TokenNumber": None,
            "OrderNumber": None, "OrderEndDate": "", "StatusIds": "5", "GetAllOrders": False,
            "FindByVoyage": None, "SearchGuestCrew": False, "IncludeTeamMemberData": "false",
            "IncludeLocation": None, "OrderTypeIds": None, "Embarkdate": None, "SearchKeyword": None
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, params=params, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('Items', _content)
            for order in _content['Items']:
                check_assertions([
                    'OrderId', 'OrderTypeId', 'OrderOriginId', 'VenueId', 'OrderDate', 'Status', 'CurrentShipTime',
                    'TokenNumber', 'HasOtherAllergy', 'ColorCode', 'GuestId',
                    'DeliverToGuestId', 'OrderNumber', 'DeliveryPersonId', 'UpdatedBy', 'UpdatedBy', 'AddedBy',
                    'TaxAmount', 'Gratuity', 'Amount', 'ModifiedDate', 'DeliveryDate', 'AdditionalNotes',
                    'IsPickPlatesRequested', 'IsDeliveryChargeApplied', 'OrderCancellations', 'OrderDetails',
                    'OrderAllergies',
                ], order)

    @pytestrail.case(381543)
    def test_21_voyage_data(self, config, request, rest_ship):
        """
        Get Voyage Data
        :param config:
        :param request:
        :param rest_ship:
        :return:
        """
        _ship_data_file = os.path.join(request.config.rootdir.strpath, 'test_data/verification_data/voyage_data.json')
        with open(_ship_data_file, 'r') as _fp:
            _ship_data = json.load(_fp)
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/voyages")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) == 0:
            raise Exception("Voyage data does not exist!!")
        else:
            for voyage in _content:
                for voyageData in _ship_data:
                    if voyage['voyageId'] == voyageData['voyageId']:
                        for _key in voyageData:
                            is_key_there_in_dict(_key, voyage)
                        for voyageItinerary in voyage['voyageItineraries']:
                            for itinerary in voyageData['voyageItineraries']:
                                if itinerary['itineraryDay'] == voyageItinerary['itineraryDay']:
                                    for _key in itinerary:
                                        is_key_there_in_dict(_key, voyageItinerary)

    @pytestrail.case(381544)
    def test_22_cancellation_metrics(self, config, test_data, rest_ship):
        """
        Get Cancellation Metrics
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'), "/v1/Orders/CancellationMetrics")
        body = {
            "DeliveryPersonIds": None, "PlacedByPersonIds": None, "MenuItems": None, "OrderDeliveredAt": None,
            "GuestIds": None, "TeamMemberIds": None, "GuestId": None, "Status": 0, "DeliveryPersonId": None,
            "OfferId": None, "VenueId": venue_id, "OrderDate": test_data['voyageEmbarkDate'],
            "IncludeAdditionalData": None,
            "IncludeGuestData": None, "LocationId": None, "TokenNumber": None, "OrderNumber": None,
            "OrderEndDate": None,
            "StatusIds": None, "GetAllOrders": None, "FindByVoyage": None, "SearchGuestCrew": False,
            "IncludeTeamMemberData": None, "IncludeLocation": None, "OrderTypeIds": None, "Embarkdate": None,
            "SearchKeyword": None
        }
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            for cancellation_reason in _content:
                is_key_there_in_dict('CancellationReasonId', cancellation_reason)
                is_key_there_in_dict('ItemCount', cancellation_reason)

    @pytestrail.case(381545)
    def test_23_venue_hours(self, config, test_data, rest_ship):
        """
        Get Venue Hours
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        venue_id = test_data['venueId']
        embark = test_data['voyageEmbarkDate']
        debark = test_data['voyageDebarkDate']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/Venues/{venue_id}/VenueHours?startDate={embark}&endDate={debark}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for venue_hour in _content:
                is_key_there_in_dict('FromTime', venue_hour)
                is_key_there_in_dict('FromDate', venue_hour)
                is_key_there_in_dict('ToDate', venue_hour)
                is_key_there_in_dict('AddedDate', venue_hour)
                is_key_there_in_dict('ToTime', venue_hour)
                is_key_there_in_dict('Type', venue_hour)

    @pytestrail.case(381546)
    def test_24_pre_order_time_slots(self, config, test_data, rest_ship):
        """
        Get Pre order Time slots for current day
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _ship = config.ship.url
        venue_id = test_data['venueId']
        embark = test_data['voyageEmbarkDate']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/PreOrders/timeslots?venueId={venue_id}&startDate={embark}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for pre_order in _content:
                is_key_there_in_dict('VenueId', pre_order)
                is_key_there_in_dict('PreOrderSlotDetailId', pre_order)
                is_key_there_in_dict('PreOrderSlotDate', pre_order)
                is_key_there_in_dict('StartTime', pre_order)
                is_key_there_in_dict('EndTime', pre_order)
                is_key_there_in_dict('IsPreOrderAvailable', pre_order)
                is_key_there_in_dict('PreOrderSlots', pre_order)
                for pre_order_slot in pre_order['PreOrderSlots']:
                    is_key_there_in_dict('PreOrderSlotId', pre_order_slot)
                    is_key_there_in_dict('PreOrderSettingId', pre_order_slot)
                    is_key_there_in_dict('StartTime', pre_order_slot)
                    is_key_there_in_dict('StartTime', pre_order_slot)
                    is_key_there_in_dict('OrderInventory', pre_order_slot)
                    is_key_there_in_dict('BookedOrders', pre_order_slot)

    @pytestrail.case(65098012)
    def test_25_food_delivery_toggle_on(self, config, test_data, rest_ship):
        """
        toggle the delivery option on
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/venues/{venue_id}/foodDeliveryAvailability/true")
        body = {"VenueId": venue_id, "IsDeliveryAvailable": "true"}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if not _content:
            raise Exception("delivery not updated")


    @pytestrail.case(65098013)
    def test_26_food_delivery_toggle_off(self, config, test_data, rest_ship):
        """
        toggle the delivery option off
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        venue_id = test_data['venueId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.fnb'),
                      f"/v1/venues/{venue_id}/foodDeliveryAvailability/false")
        body = {"VenueId": venue_id, "IsDeliveryAvailable": "false"}
        _content = rest_ship.send_request(method="PUT", url=url, json=body, auth="crew").content
        if not _content:
            raise Exception("delivery not updated")