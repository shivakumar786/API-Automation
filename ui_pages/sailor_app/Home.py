__author__ = 'prahlad.sharma'

from virgin_utils import *


class Home(General):
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
            "me_tab": "FMACC",
            "me_tab_xpath": "//*[@text='ME']",
            "home_tab": "//*[@id='FMPRE']",
            "discover_tab": "//*[@text='Discover']",
            "discover_tab_id": "//*[@id='FMDISC']",
            "services_tab": "//*[@text='Services']",
            "messenger_tab": "//div[@id='FMCHAT']",
            "open_rts": "//div[text()='Check in & get ready to sail']",
            "hero_image_desc": "//div[@class='hero-image__description']",
            "rts": "//div[@id='checkInGetReadyToSailItem']",
            "activate_the_band": "//div[@id='activateTheBandItem']",
            "voyage_well_form": "//div[@id='signVoyageWellFormItem']",
            "health_form": "//div[@id='completeYourHealthFormItem']",
            "homepage_voyage_name": "//span[@class='voyage-card__title']",
            "homepage_port_names": "//span[@class='voyage-card__route']",
            "ship_spaces_quicklink": "//div[text()='View the ship spaces']",
            "view_your_agenda_quicklink": "//div[text()='View your agenda']",
            "book_dining_quicklink": "//div[text()='Book dining']",
            "book_a_shore_thing_quicklink": "//div[text()='Book a Shore Thing']",
            "browse_the_event_lineup_quicklink": "//div[text()='Browse the event line-up']",
            "book_a_spa_treatment_quicklink": "//div[text()='Book a spa treatment']",
            "rts_steps_completed": "//div[text()='Check in & get ready to sail']/following-sibling::div",
            "voyage_well_form_task": "//div[text()='Sign Voyage Well form']",
            "search_bar": "//div[@class='SearchBar__placeholder']",
            "search_input": "//input[@id='SearchInput']",
            "search_result": "//div[text()='Razzle Dazzle Restaurant']",
            "arrival_time_slot": "//span[text()='Arrival time slot']",
            "home_embarkation_slot": "//span[@class='voyage-card__embarkation__info__value']",
            "days_available": "//div[@class='hero-image__day']",
            "homepgae_card_title": "//span[@class='content-card__title']",
            "homepage_card_details_title": "//div[@class='PageTitle--highlighted']",
            "cross_icon": "//div[@class='FixedElement__float']",
            "hero_image_day": "//div[@class='hero-image__day']",
            "hero_image_description": "//div[@class='hero-image__description']",
            "book_next_adv": "//button[@id='connectBookingButton']",
            "switch_voyage": "//button[@id='bookAnotherVoyageButton'']",
            "complete_your_health_form": "//div[text()='Complete your health form']",
            "source_iframe": "//iframe[@id='moods-editorial']",
            "back": "//*[@id='back-btn']"
    })

    def verify_availability_of_search_bar(self):
        """
        Function to verify that search bar is available on discover screen
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_bar, locator_type='xpath'
                                                      , time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_bar, locator_type='xpath'):
            logger.debug("Search bar is not available on discover screen")
        else:
            raise Exception("Search bar is not available on discover screen")

    def search_keyword(self):
        """
        Function to search keyword in search bar
        :return:
        """
        self.webDriver.click(element=self.locators.search_bar, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_input, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.set_text(element=self.locators.search_input, locator_type='xpath', text="Razzle Dazzle")

    def verify_search_results(self):
        """
        Function to verify search results
        :return:
        """
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_result,
                                                            locator_type='xpath' ,time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_result, locator_type='xpath'):
            logger.debug("Search results are available in discover search")
        else:
            raise Exception("Search results are available in discover search")

    def open_and_verify_search_results(self):
        """
        Function to verify search results
        :return:
        """
        self.webDriver.click(element=self.locators.search_result, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.search_result,
                                                          locator_type='xpath',time_out=60)
        if self.webDriver.is_element_display_on_screen(element=self.locators.search_result, locator_type='xpath'):
            logger.debug("Search results are available in discover search")
        else:
            raise Exception("Search results are available in discover search")

    def open_me_tab(self):
        """
        To open Me tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.me_tab_xpath, locator_type='xpath')

    def open_homepage_tab(self):
        """
        To open Me tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.home_tab, locator_type='xpath')

    def click_checkin_and_get_ready_to_sail(self):
        """
        To click checkin and get ready to sail
        :return:
        """
        self.webDriver.scroll_mobile(x_press=696, y_press=778, x_move=673, y_move=1551)
        self.webDriver.click(element=self.locators.me_tab_xpath, locator_type='xpath')

    def open_discover_tab(self):
        """
        To open discover tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.discover_tab_id, locator_type='xpath')

    def open_services_tab(self):
        """
        To open services tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.services_tab, locator_type='xpath')

    def open_messenger_tab(self):
        """
        To open messenger tab
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.click(element=self.locators.messenger_tab, locator_type='xpath')

    def verify_precruise_text(self):
        """
        To verify hero image description
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.scroll_complete_page_top()
        self.webDriver.explicit_visibility_of_element(element=self.locators.hero_image_desc, locator_type='xpath'
                                                      , time_out=60)
        hero_image_text = self.webDriver.get_text(element=self.locators.hero_image_desc,locator_type='xpath')
        assert hero_image_text == 'until you sail. Soon you\'ll be sipping champagne after a deep tissue massage at Redemption Spa — so go on and get lost in your future plans.'

    def verify_correct_embarkation_slot_shown_on_homepage(self, test_data):
        """
        Function to verify that correct embarkation slot is shown on homepage
        :param test_data:
        """
        self.webDriver.scroll_till_element(element=self.locators.arrival_time_slot, locator_type='xpath')
        home_embarkation_slot = self.webDriver.get_text(element=self.locators.home_embarkation_slot, locator_type='xpath')
        assert home_embarkation_slot == test_data['selected_arrival_time'],"Correct embarkation slot is not shown on homepage"

    def verify_availability_of_precruise_task(self):
        """
        To verify availability of precruise tasks
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.rts, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.rts, locator_type='xpath'):
            logger.debug("RTS is available on precruise screen")
        else:
            raise Exception("RTS is not available on precruise screen")

    def save_homepage_voyage_data(self, test_data):
        """
        To save homepage voyage data
        :param test_data:
        :return:
        """
        test_data['homepage_voyage_name'] = self.webDriver.get_text(element=self.locators.homepage_voyage_name,locator_type='xpath')
        test_data['homepage_port_names'] = self.webDriver.get_text(element=self.locators.homepage_port_names,locator_type='xpath')


    def click_view_the_ship_spaces_quicklink(self):
        """
        Function to click on view the ship spaces quicklink
        """
        self.webDriver.scroll_till_element(element=self.locators.ship_spaces_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_spaces_quicklink, locator_type='xpath')

    def click_view_your_agenda_quicklink(self):
        """
        Function to click on view your agenda quicklink on homepage
        """
        self.webDriver.scroll_till_element(element=self.locators.ship_spaces_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.view_your_agenda_quicklink, locator_type='xpath')

    def click_book_dining_quicklink(self):
        """
        Function to click book dining quicklink
        """
        self.webDriver.scroll_till_element(element=self.locators.book_dining_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.book_dining_quicklink, locator_type='xpath')

    def click_book_a_shore_thing_quicklink(self):
        """
        Function to click book a shore thing quicklink
        """
        self.webDriver.scroll_till_element(element=self.locators.book_dining_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.book_a_shore_thing_quicklink, locator_type='xpath')

    def click_browse_the_event_lineup_quicklink(self):
        """
        Function to click browse the event lineup quicklink
        """
        self.webDriver.scroll_till_element(element=self.locators.book_dining_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.browse_the_event_lineup_quicklink, locator_type='xpath')

    def click_book_a_spa_treatment_quicklink(self):
        """
        Function to click book a spa treatment quicklink
        """
        self.webDriver.scroll_till_element(element=self.locators.book_dining_quicklink, locator_type='xpath')
        self.webDriver.click(element=self.locators.book_a_spa_treatment_quicklink, locator_type='xpath')

    def verify_number_of_steps_in_rts(self, guest_data, test_data):
        """
        Function to verify number of steps in rts as per gender
        :param guest_data:
        :paream test_data:
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.rts, locator_type='xpath')
        steps_completed_text = self.webDriver.get_text(element=self.locators.rts_steps_completed, locator_type='xpath')
        test_data['number_of_steps_in_rts'] = int(steps_completed_text.split('/')[1][0:1])
        if guest_data[0]['GenderCode'] == "Male":
            assert test_data['number_of_steps_in_rts'] == 6, "Total number os steps in rts is not 6 when gender is Male"
        elif guest_data[0]['GenderCode'] == "Female" or guest_data[0]['GenderCode'] == "Another Gender":
            assert test_data['number_of_steps_in_rts'] == 7, "Total number os steps in rts is not 7 when gender is Female or Another Gender"

    def open_rts(self):
        """
        Function to click checkin and get ready to sail on homepage
        """
        self.webDriver.scroll_till_element(element=self.locators.open_rts, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.open_rts, locator_type='xpath'
                                                      , time_out=60)
        self.webDriver.click(element=self.locators.open_rts, locator_type='xpath')

    def open_sign_voyage_well_form_task(self):
        """
        Function to open sign voyage well form task
        """
        self.webDriver.scroll_till_element(element=self.locators.rts, locator_type='xpath')
        self.webDriver.click(element=self.locators.voyage_well_form_task, locator_type='xpath')

    def verify_no_of_days_on_homepage(self, test_data):
        """
        Function to verify no of days on homepage
        :param test_data:
        """
        today_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
        embark_date = datetime.strptime(test_data['next_embarkDate'], "%m/%d/%Y")
        days =int((str(embark_date-today_date)).split(" ")[0])
        get_days_available_on_homepage = int(self.webDriver.get_text(element=self.locators.days_available, locator_type='xpath').split()[0])
        assert days == get_days_available_on_homepage,"No of days is not matching on homepage"

    def open_and_verify_homepage_card(self):
        """
        Function to open and verify homepage cards
        """
        self.webDriver.scroll_till_element(element=self.locators.homepgae_card_title, locator_type='xpath')
        get_all_cards = self.webDriver.get_elements(element=self.locators.homepgae_card_title, locator_type='xpath')
        for i in get_all_cards:
            homepage_card_title = i.text
            i.click()
            self.webDriver.explicit_visibility_of_element(element=self.locators.source_iframe, locator_type='xpath'
                                                          , time_out=60)
            self.webDriver.switch_to_iframe(frame_reference=self.webDriver.get_web_element(element=self.locators.source_iframe, locator_type='xpath'))
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.homepage_card_details_title,locator_type='xpath')
            homepage_card_title_on_Details_screen = self.webDriver.get_text(element=self.locators.homepage_card_details_title, locator_type='xpath')
            assert homepage_card_title == homepage_card_title_on_Details_screen, "User is not able to access homepage cad details screen"
            self.webDriver.switch_to_default_content()
            self.webDriver.scroll_complete_page()
            self.webDriver.click(element=self.locators.cross_icon, locator_type='xpath')
            break

    def verify_post_voyage_screen(self):
        """
        Function to verify post voyage screen
        """
        hero_image_day = self.webDriver.get_text(element=self.locators.hero_image_day,locator_type='xpath')
        hero_image_description = self.webDriver.get_text(element=self.locators.hero_image_description, locator_type='xpath')
        book_next_adventure = self.webDriver.get_text(element=self.locators.book_next_adv, locator_type='xpath')
        assert hero_image_day == "BON VOYAGE", "Correct Bon Voyage text is displayed on post voyage screen"
        assert hero_image_description == "Till we sail again, may the land care for you while our waters tempt you back", "Correct hero image description is shown on post voyage screen"
        assert book_next_adventure == "Book your next adventure", "Book your next advanture text is present"

    def verify_global_navigation_menu_disabled_on_post_voyage_screen(self):
        """
        Function to verify that footer menu is disabled on post voyage screen
        """
        home = self.webDriver.is_element_enabled(element=self.locators.home_tab, locator_type='xpath')
        discover = self.webDriver.is_element_enabled(element=self.locators.discover_tab, locator_type='xpath')
        services = self.webDriver.is_element_enabled(element=self.locators.services_tab, locator_type='xpath')
        messenger = self.webDriver.is_element_enabled(element=self.locators.messenger_tab, locator_type='xpath')
        me = self.webDriver.is_element_enabled(element=self.locators.me_tab, locator_type='id')
        assert home == True, "Home section is not enabled on post voyage screen"
        assert discover == False, "Discover section is not disabled on post voyage screen"
        assert services == False, "Services section is not disabled on post voyage screen"
        assert messenger == False, "Messenger section is not disabled on post voyage screen"
        assert me == False, " Me section is not disabled on post voyage screen"

    def click_switch_voyage(self):
        """
        Function to verify that user is able to click switch voyage button
        """
        self.webDriver.click(element=self.locators.switch_voyage, locator_type='id')

    def open_health_form(self):
        """
        Function to open health form
        """
        self.webDriver.scroll_till_element(element=self.locators.rts, locator_type='xpath')
        self.webDriver.click(element=self.locators.complete_your_health_form, locator_type='id')

    def click_back_button(self):
        """
        Function to click back button
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='NATIVE_APP')
        self.webDriver.mobile_native_back()
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')







