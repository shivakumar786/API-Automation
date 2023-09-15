__author__ = 'saloni.pattnaik'

from virgin_utils import *


class ChooseVoyage(General):
    """
    Page Class for Choose Voyage page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of choose voyage page
        :param test_data:
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "header_title": "//*[text()='Ahoy']",
            "summary_header": "//div[@class='VoyagePlanner__content']//h1",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "booking_acount": "//span[@class='Icon Account']",
            "m_booking": "//button[contains(text(),'Manage Booking')]",
            "account_icon": "//span[@class='Svg-module_icon__IPxNG undefined Icon Account']",
            "logout": "//span[text()=' Logout']",
            "my_voyage": "//button[contains(text(),'My Voyages')]",
            "signin_to_account": "//button[contains(text(),'Sign in to your account')]",
            "go_to_your_account": "//button[contains(text(),'My Account')]",
            "plan_voyage_button": "//button[contains(text(),'Plan Voyage')]",
            "voyage_count": "//div[@class='VoyageCardContainer']",
            "voyage_month": "(//time[@class='VoyageCalendar__departureDate'])[%s]",
            "depart_date": "(//time[@aria-label='departs']//span[2])[%s]",
            "arrive_date": "(//time[@aria-label='arrives']//span[2])[%s]",
            "voyage_type": "(//span[@aria-label='Ship Ready To Sail']/..)[%s]",
            "choose_voyage_button": "(//button[text()=' Choose Voyage'])[2]",
            "scroll_choose_voyage_button": "(//button[text()=' Choose Voyage'])[1]",
            "cabin_type": "//span[@class='Icon Cabin']/..",
            "filter_reset": "//button[contains(text(),'Reset all')]",
            "cabin_filter": "//span[@class='Icon AdvancedOptions']",
            "cabin_type_option": "//span[text()=' Cabin types']",
            "cabin_category": "//p[text()='%s']/..",
            "apply_button": "//button[text()=' APPLY']",
            "sailor_filter": "//span[@class='Icon Sailors']",
            "sailor_count": "//button[@value='1']",
            "price_toggle": "//div[@class='can-toggle__switch']",
            "foot_note": "//div[@class='VoyageCard__price-footnote']",
            "price": "//div[@class='VoyageCard__price-footnote']/..",
            "calender_filter": "//span[@class='Icon Calendar']",
            "current_month": "//button//span[text()='%s']",
            "increment_sailor_count": "//span[@class='Incrementor__value']",
            "add": "//span[@class='Icon Plus']",
            "choose_cabin": "//button[text()='Book this']",
            "cabin_header": "//button[text()=' SHOW OPTIONS']",
            "voyage_name": "(//div[@class='VoyageCard__block VoyageCard__title']/h3)[%s]",
            "total_voyage_price": "//span[text()=' Voyage total']/..//span[@class='PriceBreakdown__VoyagePrice']",
            "total_discount_voyage_price": "//span[text()=' Voyage total']/..//span[@class='PriceBreakdown__VoyagePrice']//span[@class='original-amount']",
            "cabin_price": "//div[@class='CabinPriceSummary__title']/span[2]",
            "checkout": "//button[text()=' Checkout']",
            "text_field": "//div[@class='TextField active']/label",
            "add_flight": "//label[@for='add_flights']",
            "sailor_gender": "//label[contains(text(),'M')]",
            "citizenship": "primary_citizenShip",
            "country_code": "primary_phoneCountryCode",
            "sailor_number": "primary_contactnumber",
            "adult_checkbox": "//label[@for='primary_over18']",
            "newz_letter_checkbox": "//label[@for='add_newsletter']",
            "first_name": "primary_firstname",
            "voyage_protection": "//label[@for='primary_insurance_notOpted']",
            "continue_button": "//button[text()=' Continue']",
            "selected_button": "//label[@for='FULL']",
            "name": "//*[@name='ccFullName']",
            "credit_card": "//*[@name='ccCardNumber']",
            "expire_month": "//select[@name='ccExpMonth']",
            "expire_year": "//select[@name='ccExpYear']",
            "cvv": "//*[@name='ccCVV']",
            "country_billing": "//select[@name='billingAddressCountry']",
            "street": "//*[@name='billingAddressStreet']",
            "city": "//*[@name='billingAddressCity']",
            "state": "//select[@name='billingAddressState']",
            "zipcode": "//*[@name='billingAddressZipCode']",
            "remember_checkbox": "//*[text()='Yes, remember this card']",
            "terms_and_condition": "//label[@id='chkTermsAndConditions-label']",
            "pay": "//*[text()='PAY & CONTINUE']",
            "pay_button": "//button[@id='submitHppPaymentForm']",
            "popup": "//*[@class='Flyout__dismiss CloseBtn']/span",
            "booking_number": "ConfirmationCardReference",
            "close_icon": "//span[@class='Icon Close']",
            "iframe": "//iframe[@class='PaymentIframe']",
            "fancy_cabin_popup": "//div[@class='UpsellBookingModal']",
            "fancy_button": "//button[text()=' Yes, Please']",
            "count_botton": "//span[@class='Icon Sailors']",
            "inactive_sailor_count": "//button[@class='btn btn-sm TravelPartyRefinement__sailorBtn']",
            "content_page": "//div[@class='Flyout__backdrop -dark']",
            "date_arrow": "(//span[@class='Icon Arrow'])[2]",
            "connect_booking": "//button[contains(text(),'CONNECT A BOOKING')]",
            "cabin_types": "//span[@class='CabinTypeRefinement__name']",
            "term_conditio": "//div/p[text()='The terms & conditions linked below contain important information on your rights and ours, as well as limitations to those rights. They are binding on us and you, so we urge you to read them.']",
            "tell_me_more": "//button[text()=' Tell me more']",
            "tell_me_click": "//button[text()=' Tell me more']/span[@class='Icon FlyOut']",
            "voyage_protect": "//h2[text()='Voyage Protection']",
            "persistent_header": "//div[@class='ProgressiveSummaryItinerary']",
            "progress_bar_amount": "//span[@class='Progress__price']",
            "click_on_insurance": "//label[@for='primary_insurance_opted']",
            "location_price": "//div[@class='WhatsIncluded__headerSection']",
            "itenary_edit_icon": "//button[@aria-label='ITINERARY']",
            "cabin_edit_icon": "//button[@aria-label='Edit']",
            "weekend_filter": "//label[@for='weekendOnly']",
            "ready_to_pick": '''//span[text()="I'm really picky"]''',
            "click_on_duration": "//span[text()=' Duration']",
            "weeken_apply": "//button[@type='submit']",
            "verify_weeken": "//span[text()=' Weekends only']",
            "click_mainlogo": "//div[@class='MainNav__logo']",
            "all_reasons": "(//span[@id='selectedRegions'])[1]",
            "apply_reason": "(//span[text()='PLAN VOYAGE'])[1]",
            "click_acount": "//span[@class='Icon Account']",
            "verify_account": " Sign in to your account",
            "reset_all": "//button[contains(text(),'Reset all')]",
            "access_cabin": "//label[@for='accesscabin']",
            "check_box": "//label[@for='chkTermsAndConditions']",
            "view_details": "//span[text()='View Details']",
            "buy_button": "//button[@aria-label='Buy AddOn']",
            "guest1": "//img[@id='avatar9e963d2b-004c-4883-a223-e3b11a2cd2e6']",
            "guest2": "//img[@id='avatarbb103428-24d7-4a18-b89a-62a3d4914962']",
            "bar_summary": "//div[text()='Summary']",
            "add_pay": "//button[text()='Add card and Pay']",

            "cabin_togale": "//div[@class='can-toggle__switch']",
            "price_switch": "(//div[@class='VoyageCard__price-footnote']/..)[1]",
            "country": "primary_country",
            "select_state": "primary_stateCode",
            "cabin_sailor": "(//span[@class='refinementText'])[1]",
            "date_range": "(//span[@class='refinementText'])[2]",
            "pay_amount": "//div[@class='PaymentOption__fullPrice']",
            "manage_voyage": "(//button[@class='btn btn-primary PromotionCard__cta'])[1]",
            "bartab": "//h3[contains(text(),'It pays to prepay')]",
            "bar_view_details": "//span[contains(text(),'VIEW DETAILS')]",
            "buy_tab": "//button[text() = ' Buy']",
            "bar_image": "//div/img[contains(@class, 'avatar')]",
            "bar_add_apy": "//button[text() = ' Pay with saved card']",
            "dash_ac": "//button[text() = ' Go to your Account']",
            "bartab_next": "//button[text() = ' NEXT']",
            "tab_agree": "//span[@id='submitFormAgreeLabel']",
            "pay_and_continue": "//span[text() = 'PAY & CONTINUE']",
            "tab_ifarame": "//iframe[@class='payment_Iframe']",
            "cvv_tab": "//input[@class='payment-widget--field cvv-text savedCardCVV']",
            "complete_booking": "//button[text() = ' Done']",
            "accesible_cabins": "//label[contains(text(),'Accessible cabins')]",
            "travel_party": "//span[contains(text(),'Travel party')]",
            "count_3": "//button[@value='3']",
            "count_4": "//button[@value='4']",
            "party_apply": "//button[contains(text(),'APPLY')]",
            "sailor_per_night": "//div[text()=' Sailor per night']",
            "all_destination": "//span[contains(text(),'Destinations')]",
            "reasons": "//div[contains(text(),'Regions')]",
            "itenary_title": "//div[@class='itinerariesTitle']",
            "togle_check": "//div[@class='can-toggle__switch']",
            "select_itenary": "//input[@value='CARIBBEAN']",
            "apply_iter": "//button[contains(text(),'APPLY')]",
            "filter": "//h2[contains(text(),'Filters')]",
            "duration": "//div[contains(text(),' Duration')]",
            "c_type": "//div[contains(text(),' cabin type')]",
            "price_range": "//div[contains(text(),' Price range')]",
            "ship": "//div[contains(text(),' Ship')]",
            "departure_port": "//div[contains(text(),' Departure Port')]",
            "wkd_filter": "//span[contains(text(),' Any number of nights')]",
            "v_only": "//label[contains(text(),'Weekend voyages only')]",
            "night": "//button[contains(text(),'1-4')]",
            "available_cabins": "//span[contains(text(),' Any — the best value available')]",
            "in_sider": "//span[contains(text(),'Insider')]",
            "sea_view": "//span[contains(text(),'Sea View')]",
            "sea_terrace": "//span[contains(text(),'Sea Terrace')]",
            "any_available": "//p[contains(text(),'Any — the best value available')]",
            "apply_advance_filter": "//button[@id='PriceBreakdownCheckout']",
            "travel_date": "//span[contains(text(),'Travel dates')]",
            "available_cabin": "//div[@class='CabinTypeFilter__main']//div[@class='col col2']",
            "cabin_radio": "//div[@class= 'CabinTypeRefinement__cardRadio']",
            "price_filter": "//div[@class='PriceRangeFilter__main']//div[@class='col col2']",
            "price_per_cabin": "//div[@class='PriceRangeFilter__main']//div[@class='col col2']//span[text()='Cabin']",
            "price_per_sailor": "//div[@class='PriceRangeFilter__main']//div[@class='col col2']//span[text()='Sailor']",
            "price_per_night": "//div[@class='PriceRangeFilter__main']//div[@class='col col2']//span[text()='Sailor/night']",
            "ship_filter": "//div[@class='ShipFilter__main']//div[@class='col col2']",
            "departure_port": "//div[@class='DeparturePortFilter__main']//div[@class='col col2']",
            "upcoming_voyage": "//div[contains(text(),'Your Upcoming Voyages')]",
            "booking_ref": "//span[contains(text(),'Booking reference')]",
            "cabin_filters": "//span[contains(text(),'%s')]",
            "s_ship": "//p[contains(text(),'Scarlet Lady')]",
            "res_count": "//div[@id='ResultsCount']",
            "s_port": "//p[contains(text(),'Miami')]"

        })

    def convert_month_to_number(self, month_name):
        """
        To convert month name to number format
        :param month_name:
        :return:
        """
        datetime_object = datetime.strptime(month_name, "%b")
        month_number = datetime_object.month
        if len(str(month_number)) == 1:
            return "0" + str(month_number)
        else:
            return month_number

    def reduce_sailor_count(self):
        """
        To reduce the sailor count
        :return:
        """
        self.webDriver.click(element=self.locators.count_botton, locator_type='xpath')
        self.webDriver.click(element=self.locators.inactive_sailor_count, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def fill_payment_page(self, guest_data, country):
        """
        To fill payment information
        :param guest_data:
        :param country:
        :return:
        """
        self.webDriver.scroll(0, 500)
        self.webDriver.explicit_visibility_of_element(element=self.locators.name, locator_type='xpath', time_out=120)
        self.webDriver.set_text(element=self.locators.name, locator_type='xpath',
                                text=guest_data[0]['FirstName'] + " " + guest_data[0]['LastName'])
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.credit_card, locator_type='xpath', text="4111")
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.credit_card, locator_type='xpath', text="1111")
        self.webDriver.set_text(element=self.locators.credit_card, locator_type='xpath', text="1111")
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.credit_card, locator_type='xpath', text="1111")
        self.webDriver.select_by_index(element=self.locators.expire_month, locator_type='xpath', index=1)
        self.webDriver.select_by_index(element=self.locators.expire_year, locator_type='xpath', index=5)
        self.webDriver.set_text(element=self.locators.cvv, locator_type='xpath', text="987")
        self.webDriver.select_by_text(element=self.locators.country_billing, locator_type='xpath', text=country)
        self.webDriver.set_text(element=self.locators.street, locator_type='xpath',
                                text=guest_data[0]['Addresses'][0]['lineOne'])
        self.webDriver.set_text(element=self.locators.city, locator_type='xpath',
                                text=guest_data[0]['Addresses'][0]['city'])
        self.webDriver.wait_for(2)
        self.webDriver.select_by_index(element=self.locators.state, locator_type='xpath', index=1)
        self.webDriver.wait_for(2)
        self.webDriver.set_text(element=self.locators.zipcode, locator_type='xpath',
                                text=guest_data[0]['Addresses'][0]['zipCode'])
        self.webDriver.scroll_till_element(element=self.locators.zipcode, locator_type='xpath')
        self.webDriver.click(element=self.locators.remember_checkbox, locator_type='xpath')

    def verify_confirmation_page(self):
        """
        To verify confirmation page
        :return:
        """
        self.webDriver.wait_for(10)
        self.webDriver.click(element=self.locators.close_icon, locator_type='xpath')
        return self.webDriver.get_text(element=self.locators.booking_number, locator_type='id')

    def click_pay_button(self):
        """
        To click pay and continue button
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.pay, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.terms_and_condition, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.pay_button, locator_type='xpath')
        self.webDriver.wait_for(5)
        count = 1
        while self.webDriver.is_element_enabled(element=self.locators.pay_button, locator_type='xpath') is False and count <= 40:
            self.webDriver.click_element_with_location_type_js(element=self.locators.terms_and_condition, locator_type='xpath')
            if self.webDriver.is_element_enabled(element=self.locators.pay_button, locator_type='xpath'):
                logger.info("Pay Button is enabled")
                self.webDriver.click_element_with_location_type_js(element=self.locators.pay, locator_type='xpath')
                self.webDriver.switch_to_default_content()
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath', time_out=120)
                break
            else:
                logger.info(f"Pay Button is disabled: {count}")
                count = count + 1
                continue

    def verify_terms_and_condition(self):
        """
        To verify terms and condition is displaying on vxp or not
        :return:
        """
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.zipcode, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.zipcode, locator_type='xpath')
        return self.webDriver.is_element_display_on_screen(element=self.locators.terms_and_condition, locator_type='xpath')

    def click_terms_and_condition(self):
        """
        To click terms and condition checkbox
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.pay_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.terms_and_condition, locator_type='xpath')
        if not self.webDriver.is_element_enabled(element=self.locators.pay_button, locator_type='xpath'):
            self.webDriver.click(element=self.locators.terms_and_condition, locator_type='xpath')
        else:
            return True

    def verify_pay_button(self):
        """
        To verify pay and continue button is enabled or not
        :return:
        """
        return self.webDriver.is_element_enabled(element=self.locators.pay_button, locator_type='xpath')

    def select_country_code(self, country, number):
        """
        To select country code from drop down
        :param country:
        :param number:
        :return:
        """
        self.webDriver.select_by_index(element=self.locators.country_code, locator_type='id', index=country)
        self.webDriver.set_text(element=self.locators.sailor_number, locator_type='id', text=number)

    def click_category(self):
        """
        To select category checkbox
        :return:
        """
        self.webDriver.click(element=self.locators.adult_checkbox, locator_type='xpath')
        self.webDriver.click(element=self.locators.newz_letter_checkbox, locator_type='xpath')
        self.webDriver.click(element=self.locators.voyage_protection, locator_type='xpath')

    def select_citizenship(self, country):
        """
        To select citizenship from drop down
        :param country:
        :return:
        """
        self.webDriver.select_by_text(element=self.locators.citizenship, locator_type='id', text=country)

    def click_gender(self):
        """
        To select gender
        :param gender:
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.first_name, locator_type='id')
        self.webDriver.click(element=self.locators.sailor_gender, locator_type='xpath')

    def click_continue_button(self):
        """
        To click continue button
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.continue_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_flight_contact_checkbox(self):
        """
        To verify flight contact checkbox is available or not
        :return:
        """
        return self.webDriver.is_element_display_on_screen(element=self.locators.add_flight, locator_type='xpath')

    def click_flight_contact_checkbox(self):
        """
        To click flight contact checkbox
        :return:
        """
        self.webDriver.scroll_complete_page()
        self.webDriver.click(element=self.locators.add_flight, locator_type='xpath')

    def verify_sailor_details(self):
        """
        To verify sailor details
        :return:
        """
        field_name = ['First/Given name*', 'Last name*', 'Email*', 'Sex*', 'Citizenship*', 'Voyage Protection*']
        field_names = []
        fields = self.webDriver.get_elements(element=self.locators.text_field, locator_type='xpath')
        for field in fields:
            field_names.append(field.text)
        texts = set(field_name)
        check_texts = set(field_names)
        if texts == check_texts:
            return True
        else:
            return False

    def click_checkout(self):
        """
        To click checkout option
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.checkout, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.click(element=self.locators.checkout, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_checkout(self):
        """
        To verify checkout button functionality
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.checkout, locator_type='xpath')
        return self.webDriver.is_element_display_on_screen(element=self.locators.checkout, locator_type='xpath')

    def get_cabin_count(self):
        """
        To get the total count of cabin price
        :return:
        """
        return self.webDriver.get_text(element=self.locators.cabin_price, locator_type='xpath')

    def get_voyage_count(self):
        """
        To verify voyage total price
        :return:
        """
        self.webDriver.scroll_complete_page()
        if self.webDriver.is_element_display_on_screen(element=self.locators.total_discount_voyage_price, locator_type='xpath'):
            return self.webDriver.get_text(element=self.locators.total_discount_voyage_price, locator_type='xpath')
        else:
            return self.webDriver.get_text(element=self.locators.total_voyage_price, locator_type='xpath')

    def verify_go_to_account(self):
        """
        To verify go to your account cta is available or not on signin page
        :return:
        """
        self.webDriver.click(element=self.locators.account_icon, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.go_to_your_account,
                                                           locator_type='xpath'):
            raise Exception("Go to your account cta is not available on sailor logged in page")
        self.webDriver.click(element=self.locators.go_to_your_account, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_summary_page(self):
        """
        To verify summary page after select cabin
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.fancy_cabin_popup,
                                                           locator_type='xpath') is True:
            self.webDriver.click(element=self.locators.fancy_button, locator_type='xpath')
            return self.webDriver.get_text(element=self.locators.summary_header, locator_type='xpath')
        else:
            return self.webDriver.get_text(element=self.locators.summary_header, locator_type='xpath')

    def select_cabin(self):
        """
        To select cabin from list
        :return:
        """
        #self.webDriver.scroll_till_element(element=self.locators.cabin_header, locator_type='xpath')
        # self.test_data['cabin_header'] = self.webDriver.get_text(element=self.locators.cabin_header,
        #                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.cabin_header, locator_type='xpath')
        self.webDriver.explicit_visibility_of_element(element=self.locators.choose_cabin, locator_type='xpath',
                                                      time_out=60)
        self.webDriver.click(element=self.locators.choose_cabin, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def increase_sailor(self):
        """
        To increase sailor count
        :return:
        """
        self.webDriver.click(element=self.locators.account_icon, locator_type='xpath')
        self.webDriver.scroll(0, 1000)
        sailor_count = self.webDriver.get_text(element=self.locators.increment_sailor_count, locator_type='xpath')
        self.webDriver.click(element=self.locators.add, locator_type='xpath')
        added_sailor_count = self.webDriver.get_text(element=self.locators.increment_sailor_count, locator_type='xpath')
        if sailor_count == added_sailor_count:
            return False
        else:
            return True

    def verify_calender_filter(self):
        """
        To verify calender option on ui
        :return:
        """
        self.webDriver.scroll_complete_page_top()
        self.webDriver.click(element=self.locators.filter_reset, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        return self.webDriver.is_element_display_on_screen(element=self.locators.calender_filter, locator_type='xpath')

    def verify_duration_filter(self):
        """
        To verify date filter
        :return:
        """
        voyage_count = self.webDriver.get_elements(element=self.locators.voyage_count, locator_type='xpath')
        if len(voyage_count) == 0:
            return False
        else:
            return True

    def apply_travel_date_filter(self):
        """
        To apply travel date filter
        :return:
        """
        self.webDriver.scroll_complete_page_top()
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.click(element=self.locators.travel_date, locator_type='xpath')
        current_month = datetime.now().strftime("%b")
        datetime_object = datetime.strptime(current_month, "%b")
        month_number = datetime_object.month
        if month_number < 12:
            month_number = str(month_number + 1)
            datetime_object = datetime.strptime(str(month_number), "%m")
            next_month_name = datetime_object.strftime("%b")
            self.webDriver.click(element=self.locators.current_month % current_month, locator_type='xpath')
            self.webDriver.click(element=self.locators.current_month % next_month_name, locator_type='xpath')
        else:
            month_number = 1
            datetime_object = datetime.strptime(str(month_number), "%m")
            next_month_name = datetime_object.strftime("%b")
            self.webDriver.click(element=self.locators.current_month % current_month, locator_type='xpath')
            self.webDriver.click(element=self.locators.date_arrow, locator_type='xpath')
            self.webDriver.click(element=self.locators.current_month % next_month_name, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def apply_sailor_filter(self):
        self.webDriver.scroll_complete_page_top()
        self.webDriver.click(element=self.locators.filter_reset, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.click(element=self.locators.sailor_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.sailor_count, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def get_cabin_wise_price(self):
        """
        To get the price per cabin
        :return:
        """
        self.webDriver.scroll(0, 500)
        foot_note = self.webDriver.get_text(element=self.locators.foot_note, locator_type='xpath')
        if foot_note == "starting price per cabin":
            price = self.webDriver.get_text(element=self.locators.price, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.price_toggle, locator_type='xpath')
            price = self.webDriver.get_text(element=self.locators.price, locator_type='xpath')
        self.test_data['sailor_count'] = 2
        return price.split("\n")[0]

    def get_sailor_wise_price(self):
        """
        To get sailor wise price
        :return:
        """
        self.webDriver.click(element=self.locators.price_toggle, locator_type='xpath')
        foot_note = self.webDriver.get_text(element=self.locators.foot_note, locator_type='xpath')
        if foot_note == "starting price per sailor":
            price = self.webDriver.get_text(element=self.locators.price, locator_type='xpath')
            self.webDriver.click(element=self.locators.price_toggle, locator_type='xpath')
            return price.split("\n")[0]

    def select_cabin_type(self, unfiltered_cabin_type):
        """
        To select cabin type from filter
        :param unfiltered_cabin_type:
        :return:
        """
        cabins = []
        self.webDriver.scroll_complete_page_top()
        self.webDriver.click(element=self.locators.filter_reset, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        self.webDriver.click(element=self.locators.cabin_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.cabin_type_option, locator_type='xpath')
        cabin_types = self.webDriver.get_elements(element=self.locators.cabin_types, locator_type='xpath')
        for cabin in cabin_types:
            if str(cabin.text) != str(unfiltered_cabin_type):
                self.webDriver.click(element=self.locators.cabin_category % cabin.text, locator_type='xpath')
            else:
                continue
        self.webDriver.click(element=self.locators.apply_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=160)

    def get_cabin_type(self):
        """
        To get the type of cabin
        :return:
        """
        self.webDriver.scroll(0, 700)
        self.webDriver.explicit_visibility_of_element(element=self.locators.cabin_type, locator_type='xpath',
                                                      time_out=120)
        return self.webDriver.get_text(element=self.locators.cabin_type, locator_type='xpath')

    def select_choose_voyage(self):
        """
        Click choose voyage button for booking
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.scroll_choose_voyage_button, locator_type='xpath')
        self.webDriver.move_to_element_and_double_click(element=self.locators.choose_voyage_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_plan_voyage_button(self):
        """
        To click plan voyage button from dashboard
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.connect_booking, locator_type='xpath')
        self.webDriver.click(element=self.locators.plan_voyage_button, locator_type='xpath')
        self.webDriver.wait_for(5)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verify_voyage_list(self):
        """
        To verify voyage list is coming or not and future voyage is displaying or not
        :return:
        """
        self.webDriver.page_refresh()
        voyage_count = self.webDriver.get_elements(element=self.locators.voyage_count, locator_type='xpath')
        if len(voyage_count) == 0:
            return False
        else:
            return True

    def verify_sailor_details_page(self):
        """
        To verify sailor details page after signup for new sailor
        :return:
        """
        return self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')

    def logout(self):
        """
        To verify logout functionality
        :return:
        """
        self.webDriver.click(element=self.locators.account_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_signin_account_button(self):
        """
        To click on sign in to you account button
        :return:
        """
        self.webDriver.click(element=self.locators.account_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.signin_to_account, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def get_term_and_condition(self):
        """
        To get term & condition.
        """
        return self.webDriver.get_text(element=self.locators.term_conditio, locator_type='xpath')

    def verify_tell_me_more(self):
        """
        To verify tell me more button
        """
        text = self.webDriver.get_text(element=self.locators.tell_me_more, locator_type='xpath')
        if text == 'TELL ME MORE':
            return True
        else:
            return False

    def click_on_tell_me(self):
        """
        To verify tell me field after click
        """
        self.webDriver.click(element=self.locators.tell_me_click, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=30)
        text = self.webDriver.get_text(element=self.locators.voyage_protect, locator_type='xpath')
        if text != 'Voyage Protection':
            raise Exception("Tell me more not opened")
        self.webDriver.click(element=self.locators.close_icon, locator_type='xpath')

    def verify_persistent_header(self):
        """
        To verify persistent header
        """
        text = self.webDriver.get_web_element(element=self.locators.persistent_header, locator_type='xpath')
        return text

    def verify_persistent_header_on_payment(self):
        """
        To verify persistent header
        """

        self.webDriver.scroll_complete_page_top()
        text = self.webDriver.get_web_element(element=self.locators.persistent_header, locator_type='xpath')
        if not text:
            raise Exception("Persitent header is not abvailavle")

    def verify_progress_bar_amoount(self):
        """
        To verify progress bar amount
        """

        amount1 = self.webDriver.get_web_element(element=self.locators.progress_bar_amount, locator_type='xpath')
        amt1 = amount1.text
        self.webDriver.click(element=self.locators.click_on_insurance, locator_type='xpath')
        amount2 = self.webDriver.get_web_element(element=self.locators.progress_bar_amount, locator_type='xpath')
        amt2 = amount2.text
        if amt1 == amt2:
            raise Exception("insurance amount is not added")

    def travel_insurance_field(self):
        """
        To verify travel insurance field
        """
        self.webDriver.click(element=self.locators.click_on_insurance, locator_type='xpath')

    def verify_price_on_location(self):
        """
        To verify the price on location
        """
        return self.webDriver.get_text(element=self.locators.location_price, locator_type='xpath')

    def verify_itenary_edit_icon(self):
        """
        To verify itenary edit icon
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.itenary_edit_icon, locator_type='xpath'):
            raise Exception("Summary Icon not displayed")

    def verify_cabin_edit_icon(self):
        """
        To verify cabin edit icon
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_edit_icon, locator_type='xpath'):
            raise Exception("Summary Icon not displayed")

    def verify_weeken_filter(self):
        """
        To verify weekend filter
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.click_on_duration, locator_type='xpath'):
            self.webDriver.click(element=self.locators.ready_to_pick, locator_type='xpath')
        self.webDriver.click(element=self.locators.click_on_duration, locator_type='xpath')
        self.webDriver.click(element=self.locators.weekend_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.weeken_apply, locator_type='xpath')

    def verify_reason_filter(self):
        """
        To verify the reason filter
        """
        self.webDriver.click(element=self.locators.click_mainlogo, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=30)
        self.webDriver.scroll_till_element(element=self.locators.all_reasons, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.all_reasons, locator_type='xpath'):
            raise Exception("Not displayed")
        self.webDriver.click(element=self.locators.apply_reason, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_cabin_and_voyage_amount(self):
        """
        To verify can and voyage amount
        """
        self.webDriver.get_text(element=self.locators.progress_bar_amount, locator_type='xpath')

    def verify_check_box(self):
        """
        To verify term & condition check box
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.check_box, locator_type='xpath'):
            raise Exception("Not displayed")
        self.webDriver.click(element=self.locators.check_box, locator_type='xpath')

    def verify_pay_continue_button(self):
        """
        To verify pay and continue
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.pay_button, locator_type='xpath'):
            raise Exception("Not displayed")
        self.webDriver.click(element=self.locators.check_box, locator_type='xpath')

    def verify_logout_page(self):
        """
        To verify logout
        """
        self.webDriver.click(element=self.locators.account_icon, locator_type='xpath')
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')
        self.webDriver.wait_for(2)
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def reset_all(self):
        """
        To reset all filter
        """
        self.webDriver.click(element=self.locators.reset_all, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_accessible_filter(self):
        """
        to verify access filter
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.access_cabin, locator_type='xpath'):
            raise Exception("access filter")
        self.webDriver.click(element=self.locators.access_cabin, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=30)

    def verify_cabin_and_sailor_amount(self):
        """
        To verify he amount using toggle button
        """
        self.webDriver.click(element=self.locators.price_toggle, locator_type='xpath')
        foot_note = self.webDriver.get_text(element=self.locators.foot_note, locator_type='xpath')
        if foot_note == "starting price per sailor":
            price = self.webDriver.get_text(element=self.locators.price, locator_type='xpath')
            price1 = price.split("\n")[0]
            self.webDriver.click(element=self.locators.price_toggle, locator_type='xpath')
            price = self.webDriver.get_text(element=self.locators.price, locator_type='xpath')
            price2 = price.split("\n")[0]
            if price1 != price2 or price1 == "$0" or price2 == "$0":
                return False
            else:
                return True

    def select_country(self, country):
        """
        To select the county
        """
        self.webDriver.scroll_till_element(element=self.locators.country, locator_type='id')
        self.webDriver.select_by_text(element=self.locators.country, locator_type='id', text=country)

    def select_state(self, state):
        """
        To select the state
        """
        self.webDriver.select_by_text(element=self.locators.select_state, locator_type='id', text=state)

    def verify_cabin_sailor(self):
        """
        To verify defaul cabin and sailor
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.cabin_sailor, locator_type='xpath'):
            raise Exception("Element is not displayed")
        test = self.webDriver.get_elements(element=self.locators.cabin_sailor, locator_type='xpath')
        res = test[0].text.split(",")
        if "2" not in res[0] and "1" not in res[1]:
            raise ('Default filter is not working')

    def verify_and_purchage_bartab(self, guest_data, country):
        """
        To verify bartab
        :params guest_data:
        :params country:
        """

        self.webDriver.click(element=self.locators.m_booking, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.scroll_till_element(element=self.locators.bartab, locator_type='xpath')
        self.webDriver.is_element_display_on_screen(element=self.locators.bartab, locator_type='xpath')
        self.webDriver.is_element_display_on_screen(element=self.locators.bar_view_details, locator_type='xpath')
        self.webDriver.click(element=self.locators.bar_view_details, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.is_element_display_on_screen(element=self.locators.buy_tab, locator_type='xpath')
        self.webDriver.click(element=self.locators.buy_tab, locator_type='xpath')
        self.webDriver.is_element_display_on_screen(element=self.locators.bar_image, locator_type='xpath')
        self.webDriver.click(element=self.locators.bar_image, locator_type='xpath')
        self.webDriver.click(element=self.locators.bartab_next, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.is_element_display_on_screen(element=self.locators.bar_add_apy, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.bar_add_apy, locator_type='xpath')
        self.webDriver.click(element=self.locators.bar_add_apy, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

        payment_frame = self.webDriver.get_web_element(element=self.locators.tab_ifarame, locator_type='xpath')
        self.webDriver.switch_to_iframe(frame_reference=payment_frame)
        self.webDriver.click(element=self.locators.cvv_tab, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.cvv_tab, locator_type='xpath', text="111")
        self.webDriver.scroll_till_element(element=self.locators.tab_agree, locator_type='xpath')
        self.webDriver.click(element=self.locators.tab_agree, locator_type='xpath')
        self.webDriver.click(element=self.locators.pay_and_continue, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        self.webDriver.click(element=self.locators.complete_booking, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def verify_date_filter(self):
        """
        To verify defaul cabin and sailor
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.date_range, locator_type='xpath'):
            raise Exception("Element is not displayed")
        text = self.webDriver.get_elements(element=self.locators.date_range, locator_type='xpath')
        res = text[0].text
        if not res:
            raise Exception("Filter is not working")

    def verify_amount_on_payment(self):
        """
        verify amount on payment page
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.pay_amount, locator_type='xpath'):
            raise Exception("Amount is not available")
        amount = self.webDriver.get_text(element=self.locators.pay_amount, locator_type='xpath')

        self.webDriver.scroll_complete_page()
        self.webDriver.move_to_element_and_double_click(element=self.locators.selected_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=180)
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.iframe, locator_type='xpath')
        payment_frame = self.webDriver.get_web_element(element=self.locators.iframe, locator_type='xpath')
        self.webDriver.switch_to_iframe(frame_reference=payment_frame)
        self.webDriver.wait_for(5)

    def accesible_cabins(self):
        """
        verify the accesible cabins
        """

        if not self.webDriver.is_element_display_on_screen(element=self.locators.accesible_cabins, locator_type='xpath'):
            raise Exception("Not displaying on screen")
        else:
            self.webDriver.click(element=self.locators.accesible_cabins, locator_type='xpath')
            self.webDriver.click(element=self.locators.accesible_cabins, locator_type='xpath')
            self.webDriver.click(element=self.locators.accesible_cabins, locator_type='xpath')

    def travel_party(self):
        """
        To verify the travel party
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.travel_party, locator_type='xpath'):
            raise Exception("Not displaying")
        else:
            self.webDriver.click(element=self.locators.travel_party, locator_type='xpath')
            self.webDriver.click(element=self.locators.count_3, locator_type='xpath')
            self.webDriver.click(element=self.locators.count_4, locator_type='xpath')
            self.webDriver.click(element=self.locators.party_apply, locator_type='xpath')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                          time_out=60)

    def verify_sailor_per_night(self):
        """
        To verify default sailor per night
        """
        text = self.webDriver.get_text(element=self.locators.sailor_per_night, locator_type='xpath')
        if text != 'Sailor per night':
            raise Exception("Content mismatched")
        else:
            self.webDriver.click(element=self.locators.sailor_per_night, locator_type='xpath')

    def verify_destination_filter(self):
        """
        To verify the destination filter
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.all_destination, locator_type='xpath'):
            raise Exception("Not displaying")
        else:
            self.webDriver.click(element=self.locators.all_destination, locator_type='xpath')
            self.webDriver.is_element_display_on_screen(element=self.locators.reasons, locator_type='xpath')
            self.webDriver.is_element_display_on_screen(element=self.locators.itenary_title, locator_type='xpath')

    def verify_togle_ite_pot(self):
        """
        verify togle itenary and port call
        """

        if not self.webDriver.is_element_display_on_screen(element=self.locators.togle_check, locator_type='xpath'):
            raise Exception("Not displaying")
        else:
            self.webDriver.click(element=self.locators.togle_check, locator_type='xpath')
            self.webDriver.click(element=self.locators.togle_check, locator_type='xpath')
            self.webDriver.click(element=self.locators.togle_check, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=10)

        # self.webDriver.get_web_element(element="//div[@class='filterRegion showRegions']//input[@type='checkbox']", locator_type='xpath')
        # self.webDriver.click(element=self.locators.apply_iter, locator_type='xpath')

    def verify_filter(self):
        """
        To verify the advance filter
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.filter, locator_type='xpath'):
            raise Exception("Not displaying filter")
        else:
            self.webDriver.click(element=self.locators.filter, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.c_type, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.price_range, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.ship, locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.departure_port, locator_type='xpath')

    def weekend_filter(self):
        """
        To verify weeken filter
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.wkd_filter, locator_type='xpath'):
            raise Exception("Weeken duration filter is not available")
        self.webDriver.is_element_display_on_screen(element=self.locators.v_only, locator_type='xpath')

    def cabins_type(self):
        """
        To verify the cabins type
        """
        if not self.webDriver.is_element_display_on_screen(element=self.locators.available_cabins, locator_type='xpath'):
            raise Exception("cabins section are not available")

        else:
            self.webDriver.click(element=self.locators.available_cabin, locator_type='xpath')
            list = ['Insider', 'Sea View', 'Sea Terrace', 'RockStar Quarters', 'Mega RockStar Quarters']
            for cabins in range(0, len(list)-1):
                self.webDriver.scroll_till_element(element=self.locators.cabin_filters % list[cabins], locator_type='xpath')
                self.webDriver.wait_for(2)
                self.webDriver.click(element=self.locators.cabin_filters % list[cabins+1], locator_type='xpath')
                self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                time_out=30)
                break
        self.webDriver.click(element=self.locators.apply_advance_filter, locator_type='xpath')

    def verify_price(self):
        """
        To verify the price per sailor, cabin, sailor per night
        """
        self.webDriver.move_to_element(element=self.locators.price_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.price_filter, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.price_per_cabin, locator_type='xpath'):
            raise Exception("Cabin is not available")
        self.webDriver.click(element=self.locators.price_per_cabin, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.price_per_sailor, locator_type='xpath'):
            raise Exception("Cabin is not available")
        self.webDriver.click(element=self.locators.price_per_sailor, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.price_per_night, locator_type='xpath'):
            raise Exception("Cabin is not available")
        self.webDriver.click(element=self.locators.price_per_night, locator_type='xpath')
        self.webDriver.click(element=self.locators.apply_advance_filter, locator_type='xpath')

    def verify_ship_filter(self):
        """
        To verify the ship filter
        """
        self.webDriver.move_to_element(element=self.locators.ship_filter, locator_type='xpath')
        self.webDriver.click(element=self.locators.ship_filter, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.s_ship, locator_type='xpath'):
            raise Exception("Ship is not available")
        self.webDriver.click(element=self.locators.s_ship, locator_type='xpath')
        text = self.webDriver.get_text(element=self.locators.apply_advance_filter, locator_type='xpath')
        count1 = text.split(" ")[1]
        self.webDriver.click(element=self.locators.apply_advance_filter, locator_type='xpath')
        text2 = self.webDriver.get_text(element=self.locators.res_count, locator_type='xpath')
        count2 = text2.split(" ")[0]
        assert count1 == count2, "Voyages counts are not equal"

    def verify_departure_port(self):
        """
        verify departure port filter
        """
        self.webDriver.move_to_element(element=self.locators.departure_port, locator_type='xpath')
        self.webDriver.click(element=self.locators.departure_port, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.s_port, locator_type='xpath'):
            raise Exception("Ship is not available")
        self.webDriver.click(element=self.locators.s_port, locator_type='xpath')
        text = self.webDriver.get_text(element=self.locators.apply_advance_filter, locator_type='xpath')
        miami_count1 = text.split(" ")[1]
        self.webDriver.click(element=self.locators.apply_advance_filter, locator_type='xpath')
        text2 = self.webDriver.get_text(element=self.locators.res_count, locator_type='xpath')
        miami_count2 = text2.split(" ")[0]
        assert miami_count1 == miami_count2, "Miami Voyages counts are not equal"

    def verify_res_details_dash(self):
        """
        To verify reservation details on dashboard
        """
        self.webDriver.is_element_display_on_screen(element=self.locators.booking_number, locator_type='id')
        self.webDriver.click(element=self.locators.booking_acount, locator_type='xpath')
        self.webDriver.click(element=self.locators.dash_ac, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

        self.webDriver.click(element=self.locators.my_voyage, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)
        if not self.webDriver.is_element_display_on_screen(element=self.locators.upcoming_voyage, locator_type='xpath'):
            raise Exception("Details are not available")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.booking_ref, locator_type='xpath'):
            raise Exception("reservation details are not available")
        if not self.webDriver.is_element_display_on_screen(element=self.locators.m_booking, locator_type='xpath'):
            raise Exception("Manage booking fields are not available")