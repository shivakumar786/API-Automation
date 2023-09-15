__author__ = 'mohit.raghav'

from virgin_utils import *


class Home(General):
    """
    Page class for Home page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            'loading': '//img[@alt="loading..."]',
            'dashboard_ship_time': "//div[@class='Clock__shiptime__text']",
            'add_friend_quick_link': "//div[contains(text(), 'Add your friends')]",
            'book_restaurant_quick_link': "//div[contains(text(), 'Book a Restaurant')]",
            "quick_links": "//div[contains(text(),'{}')]",
            "me_tab_xpath": "//*[@text='ME']",
            'cabin_no': "//*[@id='stateroomButton']",
            "home_tab": "//*[@id='FMPRE']",
            "quicklinks": '//*[text()="{}"]',
            "share_pop_up": "//*[contains(@text,'Ahoy! A fellow Sailor on your voyage would like to add you as a contact')]",
            "loader": "//*[@text='loading...']",
            "discover_tab": "//*[@id='FMDISC']",
            'service_tab': "//div[@id='FMSRV']",
            'homepage_cards': "//div[contains(@id,'homepageCard')]",
            'card_details_back': "//div[@class='FixedElement__float']//button//span",
            'watch_muster_drill_btn': "//div[@class='MusterCard__link']/span",
            'muster_drill_window': "//div[contains(text(),'Watch this before the drill starts and then head to your assembly station')]",
            'muster_video_btn': "//div[@class='FullscreenVideoPlayer__play-cta']/span",
            'rts_btn': "//[text()='Check in & get ready to sail']"
        })

    def verify_oncruise_ship_time(self):
        """
        To verify hero image description
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        self.webDriver.scroll_complete_page_top()
        if self.webDriver.is_element_display_on_screen(element=self.locators.dashboard_ship_time, locator_type='xpath'):
            logger.info("Ship Time is available on Dashboard")

    def verify_availability_of_dashboard_quick_links(self):
        """
        To verify availability of dashboard_quick_links
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.add_friend_quick_link, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.add_friend_quick_link, locator_type='xpath')
        quick_links_text = ['Add your friends', 'View the ship venues', 'View your Agenda',
                            'View your wallet', 'Cabin house-keeping', 'Ship Eats Delivery']
        for link in quick_links_text:
            if self.webDriver.is_element_display_on_screen(element=self.locators.quick_links.format(link),
                                                           locator_type='xpath'):
                logger.info(f"{link} quick link is available on dashboard page")
            else:
                raise Exception(f"{link} quick link is not available on dashboard page")

        self.webDriver.scroll_till_element(element=self.locators.book_restaurant_quick_link, locator_type='xpath')
        quick_links_discover = ['Book a Restaurant', 'Book a Shore Thing', 'Browse the Line-Up', 'Book a Treatment']
        for link in quick_links_discover:
            if self.webDriver.is_element_display_on_screen(element=self.locators.quick_links.format(link),
                                                           locator_type='xpath'):
                logger.info(f"{link} quick link is available on dashboard page")
            else:
                raise Exception(f"{link} quick link is not available on dashboard page")

    def open_me_tab(self, test_data):
        """
        To open Me tab
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.dashboard_ship_time,
                                                          locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.click(element=self.locators.me_tab_xpath, locator_type='xpath')
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_no, locator_type='xpath',
                                                      time_out=60)
        cabin_number = self.webDriver.get_text(element=self.locators.cabin_no, locator_type='xpath')
        test_data['shipside_guests'][0]['cabin_no'] = cabin_number

    def open_homepage_tab(self):
        """
        To open Home tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.home_tab, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.home_tab, locator_type='xpath')

    def click_book_dining_quicklink(self):
        """
        Function to click book dining quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quick_links.format('Book a Restaurant'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quick_links.format('Book a Restaurant'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quick_links.format('Book a Restaurant'), locator_type='xpath')

    def click_book_a_shore_thing_quicklink(self):
        """
        Function to click book a shore thing quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quick_links.format('Book a Shore Thing'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quick_links.format('Book a Shore Thing'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quick_links.format('Book a Shore Thing'), locator_type='xpath')


    def click_browse_the_event_lineup_quicklink(self):
        """
        Function to click browse the event lineup quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quick_links.format('Browse the Line-Up'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quick_links.format('Browse the Line-Up'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quick_links.format('Browse the Line-Up'), locator_type='xpath')

    def click_book_a_spa_treatment_quicklink(self):
        """
        Function to click book a spa treatment quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quick_links.format('Book a Treatment'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quick_links.format('Book a Treatment'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quick_links.format('Book a Treatment'), locator_type='xpath')

    def click_add_your_friends_quicklink(self):
        """
        Function to click add your friends quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('Add your friends'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('Add your friends'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('Add your friends'), locator_type='xpath')

    def click_view_the_ship_venues(self):
        """
        Function to click view the ship venues quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('View the ship venues'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('View the ship venues'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('View the ship venues'), locator_type='xpath')

    def click_view_your_agenda(self):
        """
        Function to click view your agenda quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('View your Agenda'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('View your Agenda'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('View your Agenda'), locator_type='xpath')

    def click_view_your_wallet(self):
        """
        Function to click view your wallet quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('View your wallet'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('View your wallet'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('View your wallet'), locator_type='xpath')

    def click_cabin_house_keeping(self):
        """
        Function to click cabin housekeeping quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('Cabin house-keeping'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('Cabin house-keeping'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('Cabin house-keeping'), locator_type='xpath')

    def click_ship_eats_delivery(self):
        """
        Function to click ship eats delivery quicklink on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.quicklinks.format('Ship Eats Delivery'),
                                                      locator_type='xpath', time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.quicklinks.format('Ship Eats Delivery'),
                                           locator_type='xpath')
        self.webDriver.click(element=self.locators.quicklinks.format('Ship Eats Delivery'), locator_type='xpath')

    def verify_share_pop_up(self):
        """
        Function to verify share pop-up on dashboard
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_for(2)
        if self.webDriver.is_element_display_on_screen(element=self.locators.share_pop_up, locator_type='xpath'):
            logger.debug("Share popup is getting displayed on dashboard")
        else:
            raise Exception("Share popup is not getting displayed on dashboard")
        self.webDriver.mobile_native_back()

    def open_discover_tab(self):
        """
        To open discover tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.discover_tab,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.discover_tab, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        
    def open_services_tab(self):
        """
        To open services tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.explicit_visibility_of_element(element=self.locators.service_tab,
                                                      locator_type='xpath', time_out=60)
        self.webDriver.click(element=self.locators.service_tab, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')

    def verify_homepage_cards(self):
        """
        Function to verify availability of homepage cards
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.homepage_cards, locator_type='xpath'):
            logger.info('Oncruise cards are visible on dashboard')
        else:
            raise Exception("No Oncruise cards are visible on dashboard")

    def open_card_details_page(self):
        """
        Function to open card details page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        no_of_cards = self.webDriver.get_elements(element=self.locators.homepage_cards, locator_type='xpath')
        for card in no_of_cards:
            self.webDriver.scroll(pixel_x=card.location['x'], pixel_y=card.location['y'])
            self.webDriver.wait_for(2)
            card.click()
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.card_details_back,
                                                              locator_type='xpath')
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            self.webDriver.mobile_native_back()
            break

    def click_watch_muster_drill(self, test_data):
        """
        Function to click on watch the muster drill video
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.watch_muster_drill_btn,
                                                       locator_type='xpath'):
            self.webDriver.scroll_till_element(element=self.locators.watch_muster_drill_btn, locator_type='xpath')
            self.webDriver.wait_for(2)
            self.webDriver.click(element=self.locators.watch_muster_drill_btn, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.watch_muster_drill_btn,
                                                                   locator_type='xpath')
            test_data['muster_drill_available'] = True
        else:
            test_data['muster_drill_available'] = False
            logger.info("Sailor has already watched the muster drill video")

    def verify_availability_of_muster_drill_video(self):
        """
        Function to verify availability of muster drill video btn
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.muster_drill_window,
                                                          locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.muster_video_btn, locator_type='xpath'):
            logger.info("Muster drill video is available to watch.")
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
            self.webDriver.mobile_native_back()
            contexts = self.webDriver.get_contexts()
            self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.dashboard_ship_time,
                                                              locator_type='xpath')
        else:
            raise Exception("Muster drill video is not available to watch.")

    def verify_no_rts_on_homepage(self):
        """
        Function to verify no rts should be available on home page
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        if self.webDriver.is_element_display_on_screen(element=self.locators.rts_btn, locator_type='xpath'):
            raise Exception("RTS option is getting displayed for onboarded sailor.")
        else:
            logger.info("No RTS option is getting displayed for onboarded sailor.")

