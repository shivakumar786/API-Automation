_author_ = 'sudhansh.arora'

from virgin_utils import *


class Scheduled(General):
    """
    Page Class For Selecting venue in  delivery_manager
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of scheduled tab
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "navigation_bar": "//*[@resource-id='navigationTopBar']",
            "hamburger_menu": "//*[contains(@resource-id, 'hamburger-button')]",
            "search_icon": "(//*[@class='android.widget.TextView'])[2]",
            "three_dot_icon": "(//*[@class='android.widget.TextView'])[3]",
            "order_tabs": "//*[@resource-id='tab-container-inner']",
            "scheduled": "//*[contains(@text,'SCHEDULED ')]",
            "pending": "//*[contains(@text,'PENDING ')]",
            "OnDeck": "//*[contains(@text,'ON DECK ')]",
            "cart": "//*[contains(@text,'CART ')]",
            "delivered": "//*[contains(@text,'DELIVERED ')]",
            "cancelled": "//*[contains(@text,'CANCELED ')]",
            "options": "//*[@resource-id='modalRoot']",
            "menu": "//*[@class='android.view.View']//[@text='Menu']",
            "select_venue" : "//*[@class='android.view.View']//[@text='Current Venue']",
            "Notifications" : "//*[@class='android.widget.CheckBox']//[0]",
            "place_order": "//*[@class='android.widget.Button']//[@text='PLACE NEW ORDER']",
            "cancel_order": "//*[@class='android.view.View']//[@text='Cancel Order']",
            "filter":"//*[@class='android.widget.CheckBox']//[1]",
            "apply": "//*[@class='android.widget.Button'][@index='1']",
            "placeondeck":"//*[@text='PLACE ON DECK']",
            "bumporder":"//*[@text='BUMP']",
            "deliverorder":"//*[@text='DELIVER']",
            "waittime":"//*[@text='Ship Eats - Bell Box']/..//*[@class='android.widget.TextView'][3]",
            "set":"//*[@text='SET']",
            "movetopending":"//*[@text='MOVE TO PENDING']",
            "orderdetails": "//*[contains(@text,'Wait Time')]",
            "soon":"//*[contains(@text,'SOON')]",
            "fifteenmins":"//*[contains(@text,'15 MINS')]",
            "thirtymins":"//*[contains(@text,'30 MINS')]",
            "placedeck":"(//*[@text='PLACE ON DECK'])[3]",
            "close":"//*[@resource-id='modalRoot']//*[@class='android.view.View']//*[@class='android.view.View']//*[@class='android.widget.TextView']",
            "cancelorder":"//*[@text='CANCEL ORDER']",
            "cancelall":"//*[@text='CANCEL ALL']",
            "reason":"//*[@text='Unable to fulfill the order']",
            "proceed":"//*[@text='PROCEED']",
            "confirmcancel":"//*[@text='CONFIRM CANCELLATION']",
            "viewlater":"//*[@text='VIEW LATER']",
            "filterscheduled":"//*[@text='All']/..//*[@class='android.widget.TextView']",
            "filterapply":"//*[@text='APPLY']",
            "delivery_manager": "//*[@class='android.view.View']//*[@text='DELIVERY MANAGER']",
            "SE_Bell_Box": "//*[@class='android.view.View']//*[@index='3']",
            "apply": "//*[@class='android.widget.Button']"
    })

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_menu, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.delivery_manager, locator_type='xpath'):
            return True
        else:
            raise Exception("Something Wrong Happend")

    def select_delivery_manager(self):
        """
        To open delivery_manager module
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.delivery_manager, locator_type='xpath'):
            self.webDriver.click(element=self.locators.delivery_manager, locator_type='xpath')
        else:
            raise Exception("delivery manger is not present")

    def select_bell_box(self):
        """
        To open bell box Venue
        :return:
        """
        self.webDriver.wait_for(20)
        self.webDriver.click(element=self.locators.SE_Bell_Box, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.apply, locator_type='xpath'):
            self.webDriver.click(element=self.locators.apply, locator_type='xpath')
        else:
            raise Exception("nothing is selected")

    def open_scheduled_tab(self):
        """
        open scheduled tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.scheduled, locator_type='xpath'):
            self.webDriver.click(element=self.locators.scheduled, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.scheduled,
                                                          locator_type='xpath', time_out=120)

    def open_pending_tab(self):
        """
        open pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.pending, locator_type='xpath'):
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.pending,
                                                          locator_type='xpath', time_out=120)

    def open_OnDeck_tab(self):
        """
        open on deck tab
        :return:
        """
        self.webDriver.click(element=self.locators.OnDeck, locator_type='xpath')
        self.webDriver.wait_for(2)

    def cart_tab(self):
        """
        open cart tab
        :return:
        """
        self.webDriver.click(element=self.locators.cart, locator_type='xpath')
        self.webDriver.wait_for(2)

    def delivered_tab(self):
        """
        open delivered tab
        :return:
        """
        self.webDriver.click(element=self.locators.delivered, locator_type='xpath')
        self.webDriver.wait_for(2)

    def cancelled_tab(self):
        """
        open cancelled tab
        :return:
        """
        self.webDriver.click(element=self.locators.delivered, locator_type='xpath')
        self.webDriver.wait_for(2)

    def place_on_deck(self):
        """
        place on deck tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.placeondeck, locator_type='xpath'):
            self.webDriver.click(element=self.locators.placeondeck, locator_type='xpath')
            self.webDriver.wait_for(2)
        else:
            self.webDriver.click(element=self.locators.OnDeck, locator_type='xpath')
            self.webDriver.wait_for(2)

    def verify_pending_tab(self):
        """
        verify pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.pending, locator_type='xpath'):
            return True
        else:
            raise Exception("Something Wrong Happend")

    def bump_order(self):
        """
        place bump order
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.bumporder, locator_type='xpath'):
            self.webDriver.click(element=self.locators.bumporder, locator_type='xpath')
            self.webDriver.wait_for(2)
        else:
            self.webDriver.click(element=self.locators.cart, locator_type='xpath')
            self.webDriver.wait_for(2)

    def deliver_order(self):
        """
        place deliver order
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.deliverorder, locator_type='xpath'):
            self.webDriver.click(element=self.locators.deliverorder, locator_type='xpath')
            self.webDriver.wait_for(2)
        else:
            self.webDriver.click(element=self.locators.delivered, locator_type='xpath')
            self.webDriver.wait_for(2)


    def verify_pending(self):
        """
        verify pending tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.pending, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.pending,
                                                      locator_type='xpath', time_out=120)

    def verify_scheduled(self):
        """
        verify scheduled tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.scheduled, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.scheduled,
                                                      locator_type='xpath', time_out=120)


    def verify_ondeck(self):
        """
        verify ondeck tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.OnDeck, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.OnDeck,
                                                      locator_type='xpath', time_out=120)

    def verify_cart(self):
        """
        verify cart tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.cart, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.cart,
                                                      locator_type='xpath', time_out=120)

    def verify_delivered(self):
        """
        verify delivered tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.delivered, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.delivered,
                                                      locator_type='xpath', time_out=120)

    def verify_cancelled(self):
        """
        verify cancelled tab
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.cancelled, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.cancelled,
                                                      locator_type='xpath', time_out=120)

    def open_wait_times(self):
        """
        open wait time popup
        :return:
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.waittime, locator_type='xpath')
        self.webDriver.click(element=self.locators.waittime, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.waittime,
                                                      locator_type='xpath', time_out=120)
        self.webDriver.click(element=self.locators.set, locator_type='xpath')


    def order_details(self):
        """
        get order details on pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.orderdetails, locator_type='xpath'):
            self.webDriver.click(element=self.locators.orderdetails, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')

    def notify_soon(self):
        """
        notify as soon on pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.orderdetails, locator_type='xpath'):
            self.webDriver.click(element=self.locators.orderdetails, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.soon,locator_type='xpath', time_out=60)
            self.webDriver.click(element=self.locators.soon, locator_type='xpath')
            self.webDriver.click(element=self.locators.close, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')

    def notify_fifteen_mins(self):
        """
        notify for fifteen mins on pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.orderdetails, locator_type='xpath'):
            self.webDriver.click(element=self.locators.orderdetails, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.soon, locator_type='xpath', time_out=60)
            self.webDriver.click(element=self.locators.fifteenmins, locator_type='xpath')
            self.webDriver.click(element=self.locators.close, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')

    def notify_thirty_mins(self):
        """
        notify for thirty mins on pending tab
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.orderdetails, locator_type='xpath'):
            self.webDriver.click(element=self.locators.orderdetails, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.soon, locator_type='xpath', time_out=60)
            self.webDriver.click(element=self.locators.thirtymins, locator_type='xpath')
            self.webDriver.click(element=self.locators.close, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')


    def cancel_order(self):
        """
        cancel order
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.cancelorder, locator_type='xpath'):
            self.webDriver.click(element=self.locators.cancelorder, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.cancelall, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.cancelall, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.reason, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.reason, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.proceed, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.proceed, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.confirmcancel, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.confirmcancel, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.viewlater, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.viewlater, locator_type='xpath')
        else :
            self.webDriver.click(element=self.locators.pending, locator_type='xpath')

    def filter_mealperiod(self):
        """
        filter according to meal period
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.filterscheduled, locator_type='xpath'):
            self.webDriver.click(element=self.locators.filterscheduled, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.filterapply, locator_type='xpath',
                                                          time_out=60)
            self.webDriver.click(element=self.locators.filterapply, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.scheduled, locator_type='xpath')
