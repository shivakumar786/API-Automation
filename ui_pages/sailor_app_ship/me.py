__author__ = 'mohit.raghav'

from virgin_utils import *


class Me_tab(General):
    """
    Page class for ME page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "setting_icon": "//*[@id='SettingsBtn']",
            "my_agenda": "//div[text()='My Agenda']",
            'loading': '//img[@alt="loading..."]',
            "booked_event": "//div[text()='{}']",
            'time_of_day': "//div[@class='Agenda__daypart']",
            'my_agenda_active_date': "//div[@class='DayPicker__item DayPicker__item_active']",
            "open_lovelist": "//div[text()='LoveList']",
            "lovelist_header": "//div[@class='Lovelist__title text-center']",
            "fav_space_cards": "//div[@class='SpaceCard__name']",
            'fav_event_cards': "//div[@class='EventCard__name']",
            'lovelist_loading': "//span[@class='Loading__icon']",
            'my_wallet_btn': "//div[@id='walletButton']/span[2]",
            'balance_due_wallet': "//div[text()='Balance due']",
            'available_balance': "//div[@class='MyFolio__header-total']/div",
            'transactions': "//div[@class='MyFolio__list-item']",
            'rockstar_symbol': "//button[@id='rockstarButton']",
            'rockstar_benefits': "//li[@class='Rockstar__benefits-item']",
            'back_btn': "//button[@id='back-btn']/span"
        })

    def click_on_setting_icon(self):
        """
        To open Settings section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.setting_icon, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.setting_icon, locator_type='xpath')

    def check_availability_of_myagenda(self):
        """
        To verify availability of my agenda
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.scroll_complete_page_top()
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.my_agenda, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.my_agenda, locator_type='xpath'):
            logger.debug("User is able to see My agenda page")
        else:
            raise Exception("User is not able to view my agenda page")

    def verify_landing_on_booked_date(self, test_data):
        """
        To verify user is landed on correct date section in my agenda
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.my_agenda, locator_type='xpath')
        active_date = int(self.webDriver.get_text(element=self.locators.my_agenda_active_date, locator_type='xpath'))
        if active_date == int(test_data['lineup_schedule'].split(" ")[2][:-1]):
            logger.info("Sailor has landed on the booked lineup date")
        else:
            raise Exception("Sailor has not landed onn booked lineup date")

    def click_booked_event(self, test_data):
        """
        To click booked event in my agenda
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.booked_event.format(test_data['lineup_title']),
                                                          locator_type='xpath')
        times_of_day = self.webDriver.get_elements(element=self.locators.time_of_day, locator_type='xpath')
        for time in times_of_day:
            self.webDriver.scroll(pixel_x=time.location['x'], pixel_y=time.location['y'])
            try:
                self.webDriver.wait_for(2)
                self.webDriver.click(element=self.locators.booked_event.format(test_data['lineup_title']),
                                     locator_type='xpath')
                self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.booked_event.format(test_data['lineup_title']),
                                                                       locator_type='xpath')
                break
            except Exception:
                logger.info(f"Event not available in {time.text} section")
        else:
            raise Exception("Booked event is not shown in my agenda page.")

    def open_lovelist(self):
        """
        Function to open and view lovelist
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.open_lovelist, locator_type='xpath')
        self.webDriver.click(element=self.locators.open_lovelist, locator_type='xpath')

    def verify_events_available_in_lovelist(self, test_data):
        """
        Function to verify that liked events are available in lovelist
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.lovelist_loading,
                                                               locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.lovelist_header, locator_type='xpath')
        get_favourite_cards = self.webDriver.get_elements(element=self.locators.fav_space_cards, locator_type='xpath')
        get_favourite_events = self.webDriver.get_elements(element=self.locators.fav_event_cards, locator_type='xpath')
        for event in get_favourite_events:
            event_name = event.text
            if event_name not in test_data['love_list_events']:
                raise Exception("Liked events are not available in lovelist")
        for event in get_favourite_cards:
            event_name = event.text
            if event_name not in test_data['love_list_events']:
                raise Exception("Liked events are not available in lovelist")
            
    def open_my_wallet(self):
        """
        Function to open my wallet
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.my_wallet_btn,
                                                               locator_type='xpath')
        self.webDriver.click(element=self.locators.my_wallet_btn, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.balance_due_wallet,
                                                          locator_type='xpath')

    def verify_transactions_in_wallet(self, test_data):
        """
        Function to verify transactions in my wallet
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.balance_due_wallet,
                                                       locator_type='xpath'):
            logger.info("My wallet page is visible")
            available_blnc = self.webDriver.get_text(element=self.locators.available_balance, locator_type='xpath')
            logger.info(f"Balance due in wallet is : {available_blnc}")
        if test_data['bookable_excursion_available'] or test_data['spa_slots_availability']:
            if self.webDriver.is_element_display_on_screen(element=self.locators.transactions, locator_type='xpath'):
                no_of_transactions = self.webDriver.get_elements(element=self.locators.transactions,
                                                                 locator_type='xpath')
                logger.info(f"{len(no_of_transactions)} transactions are available")
            else:
                raise Exception("No transactions are available in wallet")

    def check_vip_sailor(self, test_data):
        """
        Function to verify if sailor is VIP or not
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.setting_icon, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_symbol, locator_type='xpath'):
            logger.info('Login user is VIP sailor')
            test_data['is_vip_sailor'] = True
        else:
            test_data['is_vip_sailor'] = False

    def click_rockstar_symbol(self):
        """
        Function to click on rockstar symbol of vip sailor
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.rockstar_symbol, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.rockstar_symbol,
                                                               locator_type='xpath')

    def verify_rockstar_benefits(self):
        """
        Function to verify rockstar benefits
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.rockstar_benefits, locator_type='xpath'):
            logger.info("Rockstar benefits are available on page")
            no_of_benefits = self.webDriver.get_elements(element=self.locators.rockstar_benefits, locator_type='xpath')
            logger.info(f"{len(no_of_benefits)} rockstar benefits for this VIP sailor")
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            self.webDriver.mobile_native_back()
        else:
            raise Exception('Rockstar benefits are available on rockstar page')

    def verify_unavailability_of_canceled_lineup(self, test_data):
        """
        Function to verify unavailability of booked lineup
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.booked_event.format(test_data['lineup_title']),
                                                           locator_type='xpath'):
            logger.info("Cancelled lineup is not visible on my agenda page")
        else:
            raise Exception("Cancelled lineup is visible on my agenda page")
