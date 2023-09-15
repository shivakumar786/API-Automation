__author__ = 'sudhansh.arora'

from virgin_utils import *


class Deliver(General):
    """
    Page Class For Selecting venue in  Server
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of pending page
        :param web_driver
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "navigation_bar": "//*[@resource-id='navigationTopBar']",
            "hamburger_icon": "(//*[@class='android.widget.TextView'])[0]",
            "search_icon": "(//*[@class='android.widget.TextView'])[2]",
            "three_dot_icon": "(//*[@class='android.widget.TextView'])[3]",
            "order_tabs": "//*[@resource-id='tab-container-inner']",
            "pending": "(//*[@class='android.view.View'])[0]",
            "OnDeck": "(//*[@class='android.view.View'])[0]",
            "cart": "(//*[@class='android.view.View'])[0]",
            "delivered": "(//*[@class='android.view.View'])[0]",
            "cancelled": "(//*[@class='android.view.View'])[0]",
            "options": "//*[@resource-id='modalRoot']",
            "menu": "//*[@class='android.view.View']//*[@text='Menu']",
            "select_venue" : "//*[@class='android.view.View']//*[@text='Current Venue']",
            "Notifications" : "//*[@class='android.widget.CheckBox']//*[0]",
            "place_order": "//*[@class='android.widget.Button']//*[@text='PLACE NEW ORDER']",
            "cancel_order": "//*[@class='android.view.View']//*[@text='Cancel Order']",
        })

    def click_hamburger_menu(self):
        """
        To click on hamburger menu
        :return:
        """
        self.webDriver.click(element=self.locators.hamburger_icon, locator_type='xpath')

    def notifications(self):
        """
        To interact with notifications
        :return:
        """
        self.webDriver.click(element=self.locators.options, locator_type='xpath')
        self.webDriver.click(element=self.locators.Notifications, locator_type='xpath')

    def open_pending_tab(self):
        """
        open pending tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_tabs, locator_type='xpath')
        self.webDriver.click(element=self.locators.pending, locator_type='xpath')

    def open_cart_tab(self):
        """
        open cart tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_tabs, locator_type='xpath')
        self.webDriver.click(element=self.locators.cart, locator_type='xpath')

    def open_OnDeck_tab(self):
        """
        open on deck tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_tabs, locator_type='xpath')
        self.webDriver.click(element=self.locators.OnDeck, locator_type='xpath')

    def delivered_tab(self):
        """
        open delivered tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_tabs, locator_type='xpath')
        self.webDriver.click(element=self.locators.delivered, locator_type='xpath')

    def cancelled_tab(self):
        """
        open cancelled tab
        :return:
        """
        self.webDriver.click(element=self.locators.order_tabs, locator_type='xpath')
        self.webDriver.click(element=self.locators.cancelled, locator_type='xpath')