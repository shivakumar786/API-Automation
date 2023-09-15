__author__ = 'mohit.raghav'

from virgin_utils import *


class Ship_eats(General):
    """
    Page class for shipeats page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'order_for_my_cabin_btn': '//*[@text="Order for my cabin"]',
            "loader": "//*[@text='loading...']",
            'ship_eats_header': "//*[@text='Ship Eats']",
            'allow_access': ".//*[@text='ALLOW']",
            'items_unavailable': "//*[@text='Currently Unavailable']",
            'ship_eats_title': "//*[@text='Ship Eats']",
            'item_categories': "//*[@class='TabWrapper--tab']",
            'item': '//*[contains(@resource-id,"element_shipeats_")]',
            'add_quantity': "//*[@resource-id='increaseBtn']",
            'add_to_basket': "//*[@resource-id='addToCart']",
            'view_basket_btn': "//*[@resource-id='viewBasketBtn']",
            'place_order_btn': "//*[@text='Place order']",
            'order_confirmation': '//*[contains(@text,"We got your order")]',
            'order_id': "//*[@class='order-number p-t-24']//span",
            'oder_item': '//*[@class="android.view.View"][2]',
            'one_qty': '//*[@text="1"]',
            'done_btn': "//*[@resource-id='doneBtn']",
            'recent_order_btn': '//*[@resource-id="recentOrder"]',
            'recent_orders_header': "//*[@text='Recent orders']",
            'item_recent_order': "//*[@text='{}']",
            "recent_order_qty": "//*[@text='{}']",
            "cancel_btn": "//*[@text='Cancel order']",
            "confirm_cancel_btn": "//*[@resource-id='showActionBtn']",
            'cacellation_header': "//*[@text='Your order has been canceled']",
            'done_button': '//*[@text="Done"]',
            'pre_order_breakfast_btn': "//*[contains(@text,'Pre-order breakfast')]",
            'pre_order_slots': "//*[contains(@text,' - ')]",
            'edit_pre_order_btn': "//*[@resource-id='action1NormalBtn']",
            'edit_order_header': "//*[contains(@text,'Edit order')]",
            'add_allergy_btn': "//*[contains(@text, 'Add allergy details')]",
            'add_allergy_details': "//*[contains(@text,'Add allergy details for this item')]",
            'allergies_list_header': "//*[contains(@text,'NOTED ALLERGIES')]",
            'allergies_checkbox': "//*[@class='android.widget.CheckBox']",
            'save_and_continue_btn': "//*[contains(@text,'Save and continue')]",
            'update_order_btn': "//*[contains(@text,'Update my order')]",
            'pre_order_update_header': '//*[contains(@text,"got your order update.")]'
        })

    def verify_ship_eats_page(self):
        """
        To verify ship eats page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.allow_access,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.allow_access, locator_type='xpath')
        self.webDriver.wait_for(5)
        if self.webDriver.is_element_display_on_screen(element=self.locators.order_for_my_cabin_btn,
                                                       locator_type='xpath'):
            self.webDriver.click(element=self.locators.order_for_my_cabin_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_eats_header,
                                                       locator_type='xpath'):
            logger.info("Ship eats page is getting displayed")
        else:
            raise Exception("Ship eats page is not getting displayed")
        
    def add_items_to_basket(self, test_data):
        """
        To add items to the basket
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.ship_eats_title, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.items_unavailable, locator_type='xpath'):
            test_data['items_available'] = False
            return
        else:
            test_data['items_available'] = True
        for scroll_y in [930, 928, 927, 926, 925]:
            self.webDriver.scroll_mobile(546, 1018, 591, scroll_y)
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.item, locator_type='xpath'):
                self.webDriver.click(element=self.locators.item, locator_type='xpath')
                self.webDriver.wait_for(2)
                if self.webDriver.is_element_display_on_screen(element=self.locators.add_quantity, locator_type='xpath'):
                    break
        else:
            test_data['items_available'] = False
            return
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.add_quantity, locator_type='xpath')
        item_orders = self.webDriver.get_elements(element=self.locators.oder_item, locator_type='xpath')
        for item in item_orders:
            item_order = item.text
            if len(item_order) != 0:
                logger.info(f"Sailor is ordering this item: {item_order}")
                break
        else:
            raise Exception('Order item text is not visible')
        test_data['shipEats_order_item'] = item_order
        for count in range(3):
            self.webDriver.click(element=self.locators.add_quantity, locator_type='xpath')
            self.webDriver.wait_for(2)
            if self.webDriver.is_element_display_on_screen(element=self.locators.one_qty, locator_type='xpath'):
                test_data['shipEats_item_qty'] = 1
                break
        else:
            raise Exception("Not able to add the quantity for item to be ordered.")
        self.webDriver.explicit_check_element_is_click(element=self.locators.add_to_basket, locator_type='xpath',
                                                       time_out=30)
        self.webDriver.click(element=self.locators.add_to_basket, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.add_to_basket, locator_type='xpath')

    def place_order(self):
        """
        Function to place the order
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.view_basket_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.view_basket_btn, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.place_order_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.place_order_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.place_order_btn,
                                                               locator_type='xpath')

    def verify_order_confirmation_screen(self):
        """
        Function to verify order confirmation screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.order_confirmation, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.order_confirmation, locator_type='xpath'):
            logger.info("Order has been placed successfully")
        self.webDriver.scroll_mobile(200, 300, 800, 200)
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.done_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.done_btn, locator_type='xpath')

    def click_recent_orders(self):
        """
        Function to click on recent orders
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.recent_order_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.recent_order_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.recent_order_btn,
                                                               locator_type='xpath')

    def verify_recent_order(self, test_data):
        """
        Function to verify the recent order
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.recent_orders_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.item_recent_order.format(test_data['shipEats_order_item']), locator_type='xpath'):
            logger.info("Ordered item is matching in recent orders")
        else:
            raise Exception("Ordered item is not matching in recent orders")
        if self.webDriver.is_element_display_on_screen(element=self.locators.recent_order_qty.format(test_data['shipEats_item_qty']), locator_type='xpath'):
            logger.info("Ordered quantity is matching in recent orders")
        else:
            raise Exception("Ordered quantity is not matching in recent orders")

    def cancel_order(self):
        """
        Function to cancel the order
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_for(2)
        self.webDriver.scroll_mobile(200, 1018, 800, 200)
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cancel_btn, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.cancel_btn, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.confirm_cancel_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.confirm_cancel_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.confirm_cancel_btn,
                                                               locator_type='xpath')

    def confirm_cancellation_page(self):
        """
        Function to confirm order cancellation page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.cacellation_header, locator_type='xpath')
        self.webDriver.scroll_mobile(200, 1018, 800, 200)
        self.webDriver.click(element=self.locators.done_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.done_btn, locator_type='xpath')

    def click_pre_order_breakfast(self):
        """
        Function to click on pre-order breakfast btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.pre_order_breakfast_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.pre_order_breakfast_btn, locator_type='xpath')

    def select_time_slot(self, test_data):
        """
        Function to select the pre-order time slot
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        available_slots = self.webDriver.get_elements(element=self.locators.pre_order_slots, locator_type='xpath')
        if len(available_slots) != 0:
            chosen_slot = random.choice(available_slots).click()
            test_data['slots_available'] = True
        else:
            test_data['slots_available'] = False
            return
            

    def click_edit_pre_order_btn(self):
        """
        Function to clcik on edit pre-order btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.scroll_mobile(200, 1018, 800, 200)
        self.webDriver.wait_for(3)
        self.webDriver.click(element=self.locators.edit_pre_order_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.edit_pre_order_btn,
                                                               locator_type='xpath')

    def edit_order(self):
        """
        Function to edit the pre-order breakfast
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.edit_order_header, locator_type='xpath')
        self.webDriver.click(element=self.locators.add_quantity, locator_type='xpath')
        self.webDriver.scroll_mobile(200, 300, 800, 200)
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.add_allergy_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.add_allergy_btn, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.scroll_mobile(534, 1514, 459, 155)
        allergy = random.choice(self.webDriver.get_elements(element=self.locators.add_allergy_details,
                                                            locator_type='xpath'))
        allergy.click()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.allergies_list_header,
                                                          locator_type='xpath')
        allergies = self.webDriver.get_elements(element=self.locators.allergies_checkbox, locator_type='xpath')
        selected_allergy = random.choice(allergies).click()
        self.webDriver.explicit_check_element_is_click(element=self.locators.save_and_continue_btn, locator_type='xpath',
                                                       time_out=30)
        self.webDriver.click(element=self.locators.save_and_continue_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.save_and_continue_btn,
                                                               locator_type='xpath')

    def click_update_order(self):
        """
        Function to click on update my order btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.update_order_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.update_order_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.update_order_btn,
                                                               locator_type='xpath')

    def verify_preorder_update_confirmation_screen(self):
        """
        Function to verify pre-order update confirmation screen
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.pre_order_update_header,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.pre_order_update_header,
                                                       locator_type='xpath'):
            logger.info("Pre-Order has been updated successfully")
        self.webDriver.scroll_mobile(200, 300, 800, 200)
        self.webDriver.wait_for(2)
        self.webDriver.click(element=self.locators.done_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.done_btn, locator_type='xpath')




