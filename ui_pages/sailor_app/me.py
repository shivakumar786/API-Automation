__author__ = 'prahlad.sharma'

from virgin_utils import *


class Me_tab(General):
    """
    Page class for Login page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//*[@text='loading...']",
            "setting_icon": "//*[@id='SettingsBtn']",
            "my_agenda": "//div[text()='My Agenda']",
            "booked_event_name": "//div[@class='AgendaCard__event-name']",
            "available_booked_events": "//div[@class='AgendaCard__event-name']",
            "scroll_till_booked_event": "//div[text()='%s']",
            "open_lovelist": "//div[@class='LovelistAddon__item-name']",
            "favourite_events": "//div[@class='EventCard__name']",
            "my_wallet": "//div[@id='walletButton']",
            "vip_avatar": "//div[@class='MyVoyage__avatar MyVoyage__avatar-is-vip']",
            "available_days_in_my_agenda": "//div[@class='DayPicker__items']/div[%s]/div[2]/div",
            "day_selected": "//div[@class='DayPicker__item DayPicker__item_active']",
            "my_agenda_active_date": "//div[@class='DayPicker__item DayPicker__item_active']",
            "booked_event": "//div[text()='{}']",
        })

    def open_lovelist(self):
        """
        Function to open and view lovelist
        :return:
        """
        self.webDriver.click(element=self.locators.open_lovelist, locator_type='xpath')

    def verify_events_available_in_lovelist(self, test_data):
        """
        Function to verify that liked events are available in lovelist
        :param test_data:
        :return:
        """
        get_favourite_events = self.webDriver.get_elements(
            element=self.locators.favourite_events, locator_type='xpath')
        for i in get_favourite_events:
            event_name = i.text
            if event_name not in test_data['favourite_events']:
                raise Exception("Liked events are not available in lovelist")

    def click_on_setting_icon(self):
        """
        To open Me tab
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
        if self.webDriver.is_element_display_on_screen(element=self.locators.my_agenda, locator_type='xpath'):
            logger.debug("User is able to see My agenda")
        else:
            raise Exception("User is not able to view my agenda")

    def click_booked_lineup(self, test_data):
        """
        To click booked lineup in my agenda
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        get_all_events = self.webDriver.get_elements(
            element=self.locators.available_booked_events, locator_type='xpath')
        for i in get_all_events:
            if i.text == test_data['booked_lineup_name']:
                i.click()
                logger.debug(f"Booked lineup {test_data['booked_lineup_name']} is available in my agenda")
                break

    def click_booked_event(self, test_data):
        """
        To click booked lineup in my agenda
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.scroll_till_element(element=self.locators.scroll_till_booked_event % test_data['summary_event_title'], locator_type='xpath')
        self.webDriver.click(element=self.locators.scroll_till_booked_event % test_data['summary_event_title'], locator_type='xpath')

    def open_my_wallet(self):
        """
        Function to open my wallet
        :return:
        """
        self.webDriver.click(element=self.locators.my_wallet, locator_type='xpath')
        self.webDriver.click(element=self.locators.my_wallet, locator_type='xpath')

    def verify_availability_of_vip_avatar(self):
        """
        Function to verify that vip avatar is available vip sailor
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.vip_avatar,
                                                       locator_type='xpath'):
            logger.debug("Vip avatar is avalable for vip sailor")
        else:
            raise Exception("Vip avatar is not avalable for vip sailor")

    def click_vip_avatar(self):
        """
        Function to click vip avatar and open rockstar page
        """
        self.webDriver.click(element=self.locators.vip_avatar, locator_type='xpath')

    def get_days_and_dates_of_voyage(self, test_data):
        """
        Function to get days snd dates of my agenda
        :param test_data:
        """
        test_data['date_dict'] = {}
        embark_date = datetime.strptime(test_data['next_embarkDate'], "%m/%d/%Y")
        debark_date = datetime.strptime(test_data['next_debarkDate'], "%m/%d/%Y")
        days_in_voyage = int((str(embark_date - debark_date)).split(" ")[0]) + 1
        for i in range(1,days_in_voyage+1):
            embark_date_str = test_data['next_embarkDate'].strftime("%m/%d/%Y")
            embark_date = datetime.strptime(embark_date_str, "%m/%d/%Y")
            test_data['date_dict'][i] = embark_date_str.split('/')[1]
            test_data['next_embarkDate'] = (embark_date + timedelta(days=1))

    def get_and_verify_days_available_in_my_agenda(self, test_data):
        """
        Function to get days available in my agenda
        :param test_data:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        get_all_days = {}
        for i in range(1,test_data['get_days_available_on_homepage']+1):
            day = int(self.webDriver.get_text(element=self.locators.days_available % i, locator_type='xpath').split()[0])
            get_all_days[i] = day
        assert len(get_all_days) == len(test_data['date_dict']),f"Day in my agenda = {len(get_all_days)} whereas days in voyage are {len(test_data['date_dict'])} "
        assert get_all_days == test_data['date_dict'],"Correct dates are not displayed in my agenda"

    def verify_user_navigated_to_correct_day(self, test_data):
        """
        Function to verify user is navigated to correct day
        :param test_data:
        :return:
        """
        day_selected = self.webDriver.get_text(element=self.locators.day_selected, locator_type='xpath')
        assert day_selected == int(test_data['summary_event_schedule'].split()[2][0:2]),"User is not navigated to correct day"

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

    def click_booked_spa_event(self, test_data):
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

    def click_booked_spa_event(self, test_data):
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

