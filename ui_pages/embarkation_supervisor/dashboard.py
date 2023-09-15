__author__ = 'prahlad.sharma'

from virgin_utils import *
from datetime import datetime

class Dashboard(General):
    """
    Page Class for Embarkation Supervisor/Visitor Management Dashboard page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of Dashboard page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "dashboard_header_title": "//p[@class='pageTitle']//span[contains(text(),'Dashboard')]",
            "search": "//div[@class='SearchField__input']/input[@placeholder='Search']",
            "search_icon": "//div[@class='SearchField__input']//img[contains(@class,'SVGContainer')]",
            "search_header": "//p[@class='pageTitle' and contains(text(),'Search Results')]",
            "active_voyage_name": "//div[@class='react-select__single-value css-1uccc91-singleValue']",
            "active_voyage_selector_dd": "//div[@class='react-select__indicators css-1wy0on6']",
            "select_voyage_textbox": "//div[@class='react-select__single-value css-1uccc91-singleValue']",
            "application_name": "//strong[@class='is-size-5']",
            "checked_in_sailor_logo": "//span[@class='navbar-item logout is-uppercase']",
            "sailor_header": "//span[contains(text(),'sailor')]",
            "checked_in_header": "//span[contains(text(),'sailor')]/../../../following-sibling::div/div/div/div"
                                 "//span[contains(text(),'Checked-in')]",
            "checked_in_header_count": "//span[contains(text(),'sailor')]/../../../following-sibling::div/div/div/div"
                                       "//span[contains(text(),'Checked-in')]/../../following-sibling::div/p",
            "not_checked_in_header_count": "//span[contains(text(),'sailor')]/../../../following-sibling::div/div/div"
                                           "/div//span[contains(text(),"
                                           "'Not Checked-in')]/../../following-sibling::div/p",
            "checked_in_onboard": "//p[contains(text(),'Checked-In, Onboard')]",
            "checked_in_onboard_count": "//p[contains(text(),'Checked-In, Onboard')]/following-sibling::p["
                                        "@class='count']",
            "checked_in_not_onboard": " //p[contains(text(),'Checked-In, Not Onboard')]",
            "checked_in_not_onboard_count": "//p[contains(text(),'Checked-In, Not Onboard')]/following-sibling::p["
                                            "@class='count']",
            "RTS_Complete_Approved": "//p[contains(text(),'RTS Complete & Approved')]",
            "RTS_Complete_Approved_count": "//p[contains(text(),'RTS Complete & Approved')]/following-sibling::p["
                                           "@class='count']",
            "RTS_Complete_Approval_Pending": "//p[contains(text(),'RTS Complete & Approval Pending')]",
            "RTS_Complete_Approval_Pending_count": "//p[contains(text(),'RTS Complete & Approval "
                                                   "Pending')]/following-sibling::p[@class='count']",
            "RTS_Not_Complete": "//p[contains(text(),'RTS Not Complete')]",
            "RTS_Not_Complete_count": "//p[contains(text(),'RTS Not Complete')]/following-sibling::p[@class='count']",
            "Not_Checked_in_Onboard": "//p[contains(text(),'Not Checked-in Onboard')]",
            "Not_Checked_in_Onboard_count": "//p[contains(text(),'Not Checked-in Onboard')]/following-sibling::p["
                                            "@class='count']",
            "sailor_onboard": "//div[@class='GuestCard card']//span[contains(text(),'Onboard')]",
            "sailor_onboard_count": "//div[@class='GuestCard card']//span[contains(text(),'Onboard')]/../../p["
                                    "@class='subtitle']",
            "sailor_ashore": "//div[@class='GuestCard card']//span[contains(text(),'Ashore')]",
            "sailor_ashore_count": "//div[@class='GuestCard card']//span[contains(text(),'Ashore')]/../../p["
                                   "@class='subtitle']",
            "sailor_yet_to_Embark": "//div[@class='GuestCard card']//span[contains(text(),'Yet To Embark')]",
            "sailor_yet_to_Embark_count": "//div[@class='GuestCard card']//span[contains(text(),'Yet To "
                                          "Embark')]/../../p[@class='subtitle']",
            "sailor_yet_to_leave": "//div[@class='GuestCard card']//span[contains(text(),'Yet To Leave')]",
            "sailor_yet_to_leave_count": "//div[@class='GuestCard card']//span[contains(text(),'Yet To "
                                         "Leave')]/../../p[@class='subtitle']",
            "sailor_checkedout": "//div[@class='GuestCard card']//span[contains(text(),'Disembarked')]",
            "sailor_checkedout_count": "//div[@class='GuestCard card']//span[contains(text(),'Disembarked')]/../../p["
                                       "@class='subtitle']",
            "sailor_total_embarking_today": "//div[@class='GuestCard card']//span[contains(text(),'Total Embarking "
                                            "Today')]",
            "sailor_total_embarking_today_count": "//div[@class='GuestCard card']//span[contains(text(),'Total "
                                                  "Embarking Today')]/../../p[@class='subtitle']",
            "sailor_Total_leaving_Today": "//div[@class='GuestCard card']//span[contains(text(),'Total Leaving Today')]",
            "sailor_Total_leaving_Today_count": "//div[@class='GuestCard card']//span[contains(text(),'Total leaving "
                                                "Today')]/../../p[@class='subtitle']",
            "sailor_Sailor_with_Alerts": "//div[@class='GuestCard card']//span[contains(text(),'Sailor with Alerts')]",
            "sailor_Sailor_with_Alerts_count": "//div[@class='GuestCard card']//span[contains(text(),'Sailor with "
                                               "Alerts')]/../../p[@class='subtitle']",
            "sailor_US": "//div[@class='GuestCard card']//span[contains(text(),'US Sailor')]",
            "sailor_US_count": "//div[@class='GuestCard card']//span[contains(text(),'US Sailor')]/../../p["
                               "@class='subtitle']",
            "sailor_Need_Assistance": "//div[@class='GuestCard card']//span[contains(text(),'Need Assistance')]",
            "sailor_Need_Assistance_count": "//div[@class='GuestCard card']//span[contains(text(),'Need "
                                            "Assistance')]/../../p[@class='subtitle']",
            "total_sailor_count": "//div[@class='GuestCard card']//div[@class='column has-text-left']//p[1]",

            "crew_header": "//p[@class='heading']//span[contains(text(),'Crew')]",
            "total_crew_count": "//div[@class='CrewCard card']//div[@class='column has-text-left']//p[1]",
            "crew_embarking_today": "//span[contains(text(),'Embarking Today')]",
            "crew_embarking_today_count": "//span[contains(text(),'Embarking Today')]/../../p[@class='subtitle']",
            "crew_checked_in": "//p[@class='title']//span[contains(text(),'Checked-in')]",
            "crew-checked_in_count": "//p[@class='title']//span[contains(text(),'Checked-in')]/../../p["
                                     "@class='subtitle']",
            "crew_onboard": "//span[contains(text(),'Crew')]/../../../..//following-sibling::div//span[contains(text("
                            "),'Onboard')]",
            "crew_onboard_count": "//span[contains(text(),'Crew')]/../../../..//following-sibling::div//span["
                                  "contains(text(),'Onboard')]/../../p[@class='subtitle']",
            "crew_ashore": "//span[contains(text(),'Crew')]/../../../..//following-sibling::div//span[contains(text("
                           "),'Ashore')]",
            "crew_ashore_count": "//span[contains(text(),'Crew')]/../../../..//following-sibling::div//span[contains("
                                 "text(),'Ashore')]/../../p[@class='subtitle']",
            "crew_leaving_Today": "//span[contains(text(),'leaving Today')]",
            "crew_leaving_Today_count": "//span[contains(text(),'leaving Today')]/../../p[@class='subtitle']",

            "visitor_header": "//p[@class='heading']//span[contains(text(),'Visitor')]",
            "total_visitor_count": "//p[@class='heading']//span[contains(text(),'Visitor')]/following-sibling::span",
            "visitor_Expected_Today": "//span[contains(text(),'Expected Today')]",
            "visitor_Expected_Today_count": "//span[contains(text(),'Expected Today')]/../../p[@class='subtitle']",
            "visitor_Approved": "//span[contains(text(),'Approved')]",
            "visitor_Approved_count": "//span[contains(text(),'Approved')]/../../p[@class='subtitle']",
            "visitor_Onboard": "//span[contains(text(),'Visitor')]/../../../..//following-sibling::div//span["
                               "contains(text(),'Onboard')]",
            "visitor_Onboard_count": "//span[contains(text(),'Visitor')]/../../../..//following-sibling::div//span["
                                     "contains(text(),'Onboard')]/../../p[@class='subtitle']",
            "visitor_ashore": "//span[contains(text(),'Visitor')]/../../../..//following-sibling::div//span[contains("
                              "text(),'Ashore')]",
            "visitor_ashore_count": "//span[contains(text(),'Visitor')]/../../../..//following-sibling::div//span["
                                    "contains(text(),'Ashore')]/../../p[@class='subtitle']",
            "visitor_checkout": "//span[contains(text(),'Disembarked')]",
            "visitor_checkout_count": "//span[contains(text(),'Disembarked')]/../../p[@class='subtitle']",
            "visitor_rejected": "//span[contains(text(),'Rejected')]",
            "visitor_rejected_count": "//span[contains(text(),'Rejected')]/../../p[@class='subtitle']",

            "left_navigation_dashboard": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span[contains("
                                         "text(),'Dashboard')]",
            "left_navigation_sailor": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span[contains("
                                      "text(),'Sailor')]",
            "left_navigation_crew": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span[contains(text("
                                    "),'Crew')]",
            "left_navigation_visitor": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span[contains(text(),'Visitor')]",
            "left_navigation_alert_message": "//div[@class='LayoutContainer']//span[contains(text(),'Alerts & "
                                             "Messages')]",
            "left_navigation_boarding_slot": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span"
                                             "[contains(text(),'Boarding Slots')]",
            "left_navigation_IPM": "//div[@class='LayoutContainer']//span[contains(text(),'In Port Manning (IPM)')]",
            "left_navigation_reports": "//div[@class='LayoutContainer']//span[contains(text(),'Reports')]",
            "left_navigation_setting": "//div[@class='LayoutContainer']//div[@class='FixedSidebar']//span[contains("
                                       "text(),'Settings')]",

            "search_visitor_tab": "//button[@class='button is-primary-outline' and contains(text(),'Visitor')]",
            "search_sailor_tab": "//button[@class='button is-primary-outline' and contains(text(),'Sailors')]",
            "search_crew_tab": "//button[@class='button is-primary-outline' and contains(text(),'Crew')]",
            "name_in_table": "//div[@class='ProfileContainer is-pulled-left']/span",
            "dob_in_table": "//tbody/tr/td[%s]",
            "logout": "//button[contains(text(),'Logout')]",
            "refresh_icon": "//img[@class='SVGContainer refreshIcon']",
            "view_more": "//span[contains(text(),'View More')]",
            "ship_date_time": "//p[@class='pageSubTitle']/span",
            "copy_right_info": "//div[@class='LayoutContainer']//div[contains(text(),'© DeCurtis Corporation')]",
            "ship_name": "//div[@class='LayoutContainer']//div[@class='MenuItem is-title'][contains(text(),'%s')]",
            "search_list_arrow": "//div[@class='TabContent active']//button[@class='button is-icon-button ']",
            "no_records": "//span[contains(text(),'No Record(s) Available.')]",
            "ship_time": "//p[@class='pageSubTitle']",
            "visitor_details": "//span[contains(text(),'Visitor Details')]",
            "view_visitor_details_arrow":"//button[@class='button is-icon-button ']",
            "row_header": "//span[text()='Birth Date']/../../..//th",
            "row_element": "//span[text()='Birth Date']/../../..//th[%s]//span//span",
            "visitor_elements_details": "//div[@class='column is-one-third']",
            "visitor_element": "(//div[@class='label'])[%s]",
            "id_details": "(//div[@class='text'])[%s]",
        })

    def click_refresh_icon(self):
        """
        Click on refresh icon to get update ship time
        """
        self.webDriver.click(element=self.locators.refresh_icon, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def get_ship_time_ui(self):
        """
        Get the ship time from UI
        """
        return self.webDriver.get_text(element=self.locators.ship_time, locator_type='xpath')

    def click_dashboard_in_left_panel(self):
        """
        To click on dashboard tab in left navigation
        """
        self.webDriver.click(element=self.locators.left_navigation_dashboard, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_alert_message_in_left_panel(self):
        """
        To click on alert and message tab in left navigation
        """
        self.webDriver.click(element=self.locators.left_navigation_alert_message, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def click_setting_in_left_panel(self):
        """
        To click on Settings tab in left navigation
        """
        self.webDriver.click(element=self.locators.left_navigation_setting, locator_type='xpath')

    def click_boarding_in_left_panel(self):
        """
        To click on Boarding Slots tab in left navigation
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=20)
        self.webDriver.click(element=self.locators.left_navigation_boarding_slot, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def verification_of_dashboard_visitor(self):
        """
        To check the availability of dashboard page
        """
        self.webDriver.allure_attach_jpeg('just_land_dashboard')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        screen_title = self.webDriver.get_text(element=self.locators.dashboard_header_title, locator_type='xpath')
        if screen_title == "Dashboard":
            logger.debug("User is landed on Dashboard page after login")
        else:
            raise Exception("User is not landed on Dashboard page after login or login is not successful")

    def select_active_voyage(self, voyage_name):
        """
        To select the active voyage
        :param voyage_name:
        """
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.active_voyage_selector_dd,
                                                          locator_type='xpath', text=voyage_name)
        self.webDriver.wait_for(5)
        self.webDriver.allure_attach_jpeg('active_voyage')

    def select_active_voyage_in_boarding_page(self, voyage_name):
        """
        To select the active voyage
        :param voyage_name:
        """
        self.webDriver.enter_data_in_textbox_using_action(element=self.locators.select_voyage_textbox,
                                                          locator_type='xpath', text=voyage_name)
        self.webDriver.wait_for(5)
        self.webDriver.allure_attach_jpeg('active_voyage')

    def get_active_voyage_name(self, voyage_name):
        """
        To get the selected active voyage name
        :param voyage_name:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        selected_voyage_name = self.webDriver.get_text(element=self.locators.active_voyage_name, locator_type='xpath')
        if selected_voyage_name.split()[0] == voyage_name.split()[0] and selected_voyage_name.split()[1] == voyage_name.split()[1]:
            logger.debug(f"{selected_voyage_name} Selected Voyage name is matching with backend response")
        else:
            raise Exception(f"{selected_voyage_name} Selected Voyage name is not matching with backend response")

    # Visitor Management test cases for Shore side

    def availability_of_visitor_dashboard(self):
        """
        To check the visitor dashboard availability
        """
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        visitor_header = self.webDriver.get_text(element=self.locators.visitor_header, locator_type='xpath')
        if visitor_header == "VISITOR":
            logger.debug("Visitor section available on screen")
        else:
            raise Exception("Visitor section not available on screen")

    def get_total_visitor_count(self):
        """
        To get the Total Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.total_visitor_count, locator_type='xpath').replace('(',
                                                                                                                    '').replace(
            ')', ''))

    def get_total_sailor_count(self):
        """
        To get the Total Sailor count
        """
        total = (self.webDriver.get_text(element=self.locators.total_sailor_count, locator_type='xpath')).split(" ")[
            1].replace('(',
                       '').replace(
            ')', '')
        return int(total)

    def get_total_crew_count(self):
        """
        To get the Total Crew count
        """
        total = (self.webDriver.get_text(element=self.locators.total_crew_count, locator_type='xpath')).split(" ")[
            1].replace('(',
                       '').replace(
            ')', '')
        return int(total)

    def get_expected_today_visitor_count(self):
        """
        To get the Expected today Visitor count
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)
        return int(self.webDriver.get_text(element=self.locators.visitor_Expected_Today_count, locator_type='xpath'))

    def get_approval_pending_visitor_count(self):
        """
        To get the pending today Visitor count
        """
        return int(
            self.webDriver.get_text(element=self.locators.visitor_Expected_Today, locator_type='xpath').split('(')[
                1].split(' ')[0])

    def get_approved_visitor_count(self):
        """
        To get the Approved Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.visitor_Approved_count, locator_type='xpath'))

    def get_onboard_visitor_count(self):
        """
        To get the Onboard Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.visitor_Onboard_count, locator_type='xpath'))

    def get_ashore_visitor_count(self):
        """
        To get the Ashore Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.visitor_ashore_count, locator_type='xpath'))

    def get_checked_out_visitor_count(self):
        """
        To get the Checked-out Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.visitor_checkout_count, locator_type='xpath'))

    def get_rejected_visitor_count(self):
        """
        To get the Rejected Visitor count
        """
        return int(self.webDriver.get_text(element=self.locators.visitor_rejected_count, locator_type='xpath'))

    def match_total_visitor(self):
        """
        To verification of the total visitor count
        """
        self.webDriver.scroll_complete_page()
        total_visitor = self.get_total_visitor_count()
        expected_today = self.get_expected_today_visitor_count()
        approved = self.get_approved_visitor_count()
        onboard = self.get_onboard_visitor_count()
        ashore = self.get_ashore_visitor_count()
        checked_out = self.get_checked_out_visitor_count()
        rejected = self.get_rejected_visitor_count()
        if total_visitor == onboard + ashore:
            logger.debug("Total visitor Matched on dashboard")
        else:
            raise Exception("Total visitor not Matched on dashboard ")

    def match_total_sailors(self):
        """
        To verification of the total sailor (Onboard and Ashore) count
        """
        self.webDriver.scroll_complete_page_top()
        total_sailor = self.get_total_sailor_count()
        onboard = self.get_sailor_onboard_count()
        ashore = self.get_sailor_ashore_count()

        if total_sailor == onboard + ashore:
            logger.debug("Total Sailor Matched on dashboard")
        else:
            raise Exception("Total sailor not Matched on dashboard ")

    def match_total_crew(self):
        """
        To verification of the total crew (On board and Ashore) count
        """
        self.webDriver.scroll_till_element(element=self.locators.total_crew_count, locator_type='xpath')
        total_crew = self.get_total_crew_count()
        onboard = self.get_crew_onboard_count()
        ashore = self.get_crew_ashore_count()

        if total_crew == onboard + ashore:
            logger.debug("Total crew Matched on dashboard")
        else:
            raise Exception("Total crew not Matched on dashboard ")

    def click_onboard_count(self):
        """
        This function is used to click on On-board visitor count
        """
        self.webDriver.click(element=self.locators.visitor_Onboard, locator_type='xpath')

    def click_ashore_count(self):
        """
        This function is used to click on Ashore visitor count
        """
        self.webDriver.click(element=self.locators.visitor_ashore, locator_type='xpath')

    def click_visitor_tab(self):
        """
        click on visitor tab in left navigation bar
        """
        self.webDriver.click(element=self.locators.left_navigation_visitor, locator_type='xpath')

    def click_sailor_tab(self):
        """
        click on sailor tab in left navigation bar
        """
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.click(element=self.locators.left_navigation_sailor, locator_type='xpath')

    def click_crew_tab(self):
        """
        click on crew tab in left navigation bar
        """
        self.webDriver.click(element=self.locators.left_navigation_crew, locator_type='xpath')

    def click_user_avatar(self):
        """
        click on Logged in user avatar icon
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=20)
        self.webDriver.click(element=self.locators.checked_in_sailor_logo, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('click_avatar')

    def click_logout(self):
        """
        click on logout option after open avatar
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=10)
        self.webDriver.click(element=self.locators.logout, locator_type='xpath')

    def click_view_more(self):
        """
        click on view more
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.view_more, locator_type='xpath'):
            logger.debug("View More button display on page")
            self.webDriver.click(element=self.locators.view_more, locator_type='xpath')
            self.webDriver.scroll_till_element(element=self.locators.sailor_Need_Assistance, locator_type='xpath')
        else:
            logger.debug("View More button is already clicked")

    def enter_search_keywords(self, search_keyword):
        """
        Function to search with any keyword
        :param search_keyword:
        """
        self.webDriver.set_text(element=self.locators.search, locator_type='xpath', text=search_keyword)
        self.webDriver.click(element=self.locators.search_icon, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.search_header,
                                                          locator_type='xpath')
        self.webDriver.allure_attach_jpeg('search')

    def open_visitor_tab_in_global_search(self):
        """
        click on visitor tab once search result display
        """
        self.webDriver.click(element=self.locators.search_visitor_tab, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.allure_attach_jpeg('data_in_visitor')

    def open_sailor_tab_in_global_search(self):
        """
        click on visitor tab once search result display
        """
        self.webDriver.click(element=self.locators.search_sailor_tab, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.allure_attach_jpeg('data_in_sailor')

    def open_crew_tab_in_global_search(self):
        """
        click on visitor tab once search result display
        """
        self.webDriver.click(element=self.locators.search_crew_tab, locator_type='xpath')
        self.webDriver.wait_for(1)
        self.webDriver.allure_attach_jpeg('data_in_crew')

    def verify_search_result(self, search_name, search_type):
        """
        Verification of search result
        :param search_name:
        :param search_type:
        """
        if self.blank_list():
            raise Exception(f"{search_name} : Search result not found for {search_type}")
        elif search_type == 'DOB':
            number_of_column = self.webDriver.get_elements(element=self.locators.row_header, locator_type='xpath')
            for i in range(1,len(number_of_column)):
                header_name = self.webDriver.get_elements(element=self.locators.row_element % i, locator_type='xpath')
                if header_name[0].text == 'Birth Date':
                    visitor_dob_list = self.webDriver.get_elements(element=self.locators.dob_in_table % i, locator_type='xpath')
                    for DOB in visitor_dob_list:
                        DOB = datetime.strptime(DOB.text, "%d/%m/%Y").strftime("%Y-%d-%m")
                        if DOB == search_name:
                            self.webDriver.allure_attach_jpeg('_visitor_search')
                            logger.debug(f"{search_name} : Search result found for {search_type}")
                            break

        elif search_type == 'Doc Number':
            self.webDriver.click(
                element=self.locators.view_visitor_details_arrow, locator_type='xpath')
            self.webDriver.wait_till_element_appear_on_screen(element=self.locators.visitor_details, locator_type='xpath')
            self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')
            visitor_ele_list = self.webDriver.get_elements(element=self.locators.visitor_elements_details, locator_type='xpath')
            for i in range(1, len(visitor_ele_list)):
                element_name = self.webDriver.get_elements(element=self.locators.visitor_element % i, locator_type='xpath')
                if element_name[0].text == 'ID Number':
                    ID_element = self.webDriver.get_elements(element=self.locators.id_details % i, locator_type='xpath')
                    if ID_element[0].text == search_name:
                        self.webDriver.allure_attach_jpeg('_visitor_search')
                        logger.debug(f"{search_name} : Search result found for {search_type}")
                        break
                    else:
                        self.webDriver.allure_attach_jpeg('error_visitor_search')
                        raise Exception(f"{search_name} : Search result not found for {search_type}")

        else:
            visitor_name_list = self.webDriver.get_elements(element=self.locators.name_in_table, locator_type='xpath')
            for name in visitor_name_list:
                if name.text == search_name:
                    self.webDriver.allure_attach_jpeg('_visitor_search')
                    logger.debug(f"{search_name} : Search result found for {search_type}")
                    break
                if name.text.__contains__(search_name):
                    self.webDriver.allure_attach_jpeg('_visitor_search')
                    logger.debug(f"{search_name} : Search result found for {search_type}")
                    break

            else:
                self.webDriver.allure_attach_jpeg('error_visitor_search')
                raise Exception(f"{search_name} : Search result not found for {search_type}")

    def availability_of_search_option(self):
        """
        availability of search option
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.search, locator_type='xpath'):
            logger.debug("Search option available on Dashboard")
        else:
            raise Exception("Search option not available on Dashboard")

    def availability_of_user_profile(self):
        """
        availability of user profile logo
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.checked_in_sailor_logo,
                                                       locator_type='xpath'):
            logger.debug("User profile pick logo available on Dashboard")
        else:
            raise Exception("User profile pick logo not available on Dashboard")

    def availability_of_application_name(self):
        """
        availability of application name
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.application_name, locator_type='xpath'):
            logger.debug("Application name available on Dashboard")
        else:
            raise Exception("Application name is not available on Dashboard")

    def availability_of_refresh_icon(self):
        """
        availability of refresh icon
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.refresh_icon, locator_type='xpath'):
            logger.debug("refresh icon available on Dashboard")
        else:
            raise Exception("refresh icon is not available on Dashboard")

    def availability_of_onboard_sailor(self):
        """
        availability of Onboard Sailor
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_onboard, locator_type='xpath'):
            logger.debug("Onboard Sailor available on Dashboard")
        else:
            raise Exception("Onboard Sailor is not available on Dashboard")

    def availability_of_ashore_sailor(self):
        """
        availability of ashore Sailor
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_ashore, locator_type='xpath'):
            logger.debug("Ashore Sailor available on Dashboard")
        else:
            raise Exception("Ashore Sailor is not available on Dashboard")

    def availability_of_yet_to_Embark(self):
        """
        availability of yet_to_Embark
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_yet_to_Embark,
                                                       locator_type='xpath'):
            logger.debug("yet_to_Embark Sailor available on Dashboard")
        else:
            raise Exception("yet_to_Embark Sailor is not available on Dashboard")

    def availability_of_sailor_yet_to_leave(self):
        """
        availability of sailor_yet_to_leave
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_yet_to_leave, locator_type='xpath'):
            logger.debug("sailor_yet_to_leave Sailor available on Dashboard")
        else:
            raise Exception("sailor_yet_to_leave Sailor is not available on Dashboard")

    def availability_of_sailor_checked_out(self):
        """
        availability of sailor_checked out
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_checkedout, locator_type='xpath'):
            logger.debug("checked out Sailor available on Dashboard")
        else:
            raise Exception("Checked out Sailor is not available on Dashboard")

    def availability_of_sailor_total_embarking_today(self):
        """
        availability of sailor_total_embarking_today
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_total_embarking_today,
                                                       locator_type='xpath'):
            logger.debug("sailor_total_embarking_today available on Dashboard")
        else:
            raise Exception("sailor_total_embarking_today is not available on Dashboard")

    def availability_of_sailor_total_leaving_today(self):
        """
        availability of sailor_total_leaving_Today
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_Total_leaving_Today,
                                                       locator_type='xpath'):
            logger.debug("sailor_Total_leaving_Today available on Dashboard")
        else:
            raise Exception("sailor_Total_leaving_Today is not available on Dashboard")

    def availability_of_sailor_sailor_with_alerts(self):
        """
        availability of sailor_Sailor_with_Alerts
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_Sailor_with_Alerts,
                                                       locator_type='xpath'):
            logger.debug("sailor_Sailor_with_Alerts Sailor available on Dashboard")
        else:
            raise Exception("sailor_Sailor_with_Alerts Sailor is not available on Dashboard")

    def availability_of_sailor_us(self):
        """
        availability of sailor_US
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_US, locator_type='xpath'):
            logger.debug("sailor_US  available on Dashboard")
        else:
            raise Exception("sailor_US is not available on Dashboard")

    def availability_of_sailor_need_assistance(self):
        """
        availability of sailor_Need_Assistance
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.sailor_Need_Assistance,
                                                       locator_type='xpath'):
            logger.debug("sailor_Need_Assistance available on Dashboard")
        else:
            raise Exception("sailor_Need_Assistance is not available on Dashboard")

    def availability_of_crew_embarking_today(self):
        """
        availability of crew_embarking_today
        """
        self.webDriver.scroll_till_element(element=self.locators.crew_leaving_Today, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.crew_embarking_today,
                                                       locator_type='xpath'):
            logger.debug("crew_embarking_today available on Dashboard")
        else:
            raise Exception("crew_embarking_today is not available on Dashboard")

    def availability_of_crew_checked_in(self):
        """
        availability of crew_checked_in
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.crew_checked_in, locator_type='xpath'):
            logger.debug("crew_checked_in available on Dashboard")
        else:
            raise Exception("crew_checked_in is not available on Dashboard")

    def availability_of_crew_onboard(self):
        """
        availability of crew_onboard
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.crew_onboard, locator_type='xpath'):
            logger.debug("crew_onboard available on Dashboard")
        else:
            raise Exception("crew_onboard is not available on Dashboard")

    def availability_of_crew_ashore(self):
        """
        availability of crew_ashore
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.crew_ashore, locator_type='xpath'):
            logger.debug("crew_ashore available on Dashboard")
        else:
            raise Exception("crew_ashore is not available on Dashboard")

    def availability_of_crew_leaving_today(self):
        """
        availability of crew_leaving_Today
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.crew_leaving_Today, locator_type='xpath'):
            logger.debug("crew_leaving_Today available on Dashboard")
        else:
            raise Exception("crew_leaving_Today is not available on Dashboard")

    def availability_of_visitor_expected_today(self):
        """
        availability of visitor_Expected_Today
        """
        self.webDriver.scroll_till_element(element=self.locators.visitor_rejected, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_Expected_Today,
                                                       locator_type='xpath'):
            logger.debug("visitor_Expected_Today available on Dashboard")
        else:
            raise Exception("visitor_Expected_Today is not available on Dashboard")

    def availability_of_visitor_approved(self):
        """
        availability of visitor_Approved
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_Approved, locator_type='xpath'):
            logger.debug("visitor_Approved available on Dashboard")
        else:
            raise Exception("visitor_Approved is not available on Dashboard")

    def availability_of_visitor_onboard(self):
        """
        availability of visitor_Onboard
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_Onboard, locator_type='xpath'):
            logger.debug("visitor_Onboard available on Dashboard")
        else:
            raise Exception("visitor_Onboard is not available on Dashboard")

    def availability_of_visitor_ashore(self):
        """
        availability of visitor_ashore
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_ashore, locator_type='xpath'):
            logger.debug("visitor_ashore available on Dashboard")
        else:
            raise Exception("visitor_ashore is not available on Dashboard")

    def availability_of_visitor_checkout(self):
        """
        availability of visitor_checkout
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_checkout, locator_type='xpath'):
            logger.debug("visitor_checkout available on Dashboard")
        else:
            raise Exception("visitor_checkout is not available on Dashboard")

    def availability_of_visitor_rejected(self):
        """
        availability of visitor_rejected
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.visitor_rejected, locator_type='xpath'):
            logger.debug("visitor_rejected available on Dashboard")
        else:
            raise Exception("visitor_rejected is not available on Dashboard")

    def availability_of_report(self):
        """
        availability of report
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.left_navigation_reports,
                                                       locator_type='xpath'):
            logger.debug("Report available on Dashboard")
        else:
            raise Exception("Report is not available on Dashboard")

    def availability_of_in_port_manning(self):
        """
        availability of in_port_manning
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.left_navigation_IPM, locator_type='xpath'):
            logger.debug("Port Manning report available on Dashboard")
        else:
            raise Exception("Port Manning report is not available on Dashboard")

    def availability_of_ship_date_time(self):
        """
        availability of Ship Date time
        """
        ship_date_time = self.webDriver.get_text(element=self.locators.ship_date_time, locator_type='xpath')
        ship_date_time_list = ship_date_time.split(" ")
        ship_date = ship_date_time_list[2].replace(",", "")
        ship_time = ship_date_time_list[3]

        if len(ship_date) > 0:
            logger.debug(f"Ship Date: {ship_date} available on screen")
        else:
            raise Exception(f"Ship Date: {ship_date} not available on screen")

        if len(ship_time) > 0:
            logger.debug(f"Ship Time: {ship_time} available on screen")
        else:
            raise Exception(f"Ship Time: {ship_time} not available on screen")

    def availability_of_copyright_info(self):
        """
        availability of copy right info
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.copy_right_info, locator_type='xpath'):
            logger.debug("Copy Right info available on Dashboard")
        else:
            raise Exception("Copy Right info is not available on Dashboard")

    def availability_of_ship_name(self, ship_name):
        """
        availability of ship name
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.ship_name % ship_name,
                                                       locator_type='xpath'):
            logger.debug("Correct ship name available on Dashboard")
        else:
            raise Exception("orrect ship name is not available on Dashboard")

    def view_searched_visitor(self, position):
        """
        Function to open the visitor at provided position
        :param position:
        """
        visitor_name_list = self.webDriver.get_elements(element=self.locators.search_list_arrow,
                                                        locator_type='xpath')
        position = position - 1
        for name in visitor_name_list:
            if position == visitor_name_list.index(name):
                name.click()
                self.webDriver.allure_attach_jpeg('visitor_name')
                break
        else:
            self.webDriver.allure_attach_jpeg('error_visitor_name')
            raise Exception("Visitor name is not matching")

    def get_sailor_checked_in_onboard_count(self):
        """
        Function to get the checked in on board count
        """
        return self.webDriver.get_text(element=self.locators.checked_in_onboard_count, locator_type='xpath')

    def get_sailor_checked_in_not_onboard_count(self):
        """
        Function to get the checked in not on board count
        """
        return self.webDriver.get_text(element=self.locators.checked_in_not_onboard_count, locator_type='xpath')

    def get_rts_complete_approved_count(self):
        """
        Function to get the rts_complete_approved_count
        """
        return self.webDriver.get_text(element=self.locators.RTS_Complete_Approved_count, locator_type='xpath')

    def get_rts_complete_approval_pending_count(self):
        """
        Function to get the rts_complete_approval_pending_count
        """
        return self.webDriver.get_text(element=self.locators.RTS_Complete_Approval_Pending_count, locator_type='xpath')

    def get_rts_not_complete_count(self):
        """
        Function to get the RTS_Not_Complete_count
        """
        return self.webDriver.get_text(element=self.locators.RTS_Not_Complete_count, locator_type='xpath')

    def get_not_checked_in_onboard_count(self):
        """
        Function to get the Not_Checked_in_Onboard_count
        """
        return self.webDriver.get_text(element=self.locators.Not_Checked_in_Onboard_count, locator_type='xpath')

    def get_sailor_onboard_count(self):
        """
        Function to get the sailor_onboard_count
        """
        return int(self.webDriver.get_text(element=self.locators.sailor_onboard_count, locator_type='xpath'))

    def click_sailor_onboard_count(self):
        """
        Function to click on the sailor_onboard_count
        """
        self.webDriver.click(element=self.locators.sailor_onboard_count, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_sailor_ashore_count(self):
        """
        Function to get the sailor_ashore_count
        """
        return int(self.webDriver.get_text(element=self.locators.sailor_ashore_count, locator_type='xpath'))

    def click_sailor_ashore_count(self):
        """
        Function to click on the sailor_ashore_count
        """
        self.webDriver.click(element=self.locators.sailor_ashore_count, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_crew_onboard_count(self):
        """
        Function to get the crew_onboard_count
        """
        return int(self.webDriver.get_text(element=self.locators.crew_onboard_count, locator_type='xpath'))

    def click_crew_onboard_count(self):
        """
        Function to click on the sailor_onboard_count
        """
        self.webDriver.click(element=self.locators.crew_onboard_count, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def get_crew_ashore_count(self):
        """
        Function to get the sailor_ashore_count
        """
        return int(self.webDriver.get_text(element=self.locators.crew_ashore_count, locator_type='xpath'))

    def click_crew_ashore_count(self):
        """
        Function to click on the sailor_ashore_count
        """
        self.webDriver.click(element=self.locators.crew_ashore_count, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loader, locator_type='xpath')

    def blank_list(self):
        """
        Verification of blank list
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.no_records, locator_type='xpath'):
            return True
        else:
            return False

    def get_checked_in_count(self):
        """
        To get the checked in count
        """
        return int(self.webDriver.get_text(element=self.locators.checked_in_header_count, locator_type='xpath'))

    def get_non_checked_in_count(self):
        """
        To get the non checked in count
        """
        return int(self.webDriver.get_text(element=self.locators.not_checked_in_header_count, locator_type='xpath'))

    def get_total_of_checked_in_non_checked_in_count(self):
        """
        Total of checked in and non checked in count
        """
        return self.get_checked_in_count() + self.get_non_checked_in_count()

    def verify_percent_of_checked_in_onboard(self):
        """
        Percent of checked in and onboard sailor
        """
        text = self.webDriver.get_text(element=self.locators.checked_in_onboard_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"Checked-In, Onboard % is correct on Dashboard {calculation}")
        else:
            logger.error(f"Checked-In, Onboard % is not correct on Dashboard {calculation}")

    def verify_percent_of_checked_in_not_onboard(self):
        """
        Percent of checked in and not onboard sailor
        """
        text = self.webDriver.get_text(element=self.locators.checked_in_not_onboard_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"Checked-In, NOT Onboard % is correct on Dashboard {calculation}")
        else:
            logger.error(f"Checked-In, NOT Onboard % is not correct on Dashboard {calculation}")

    def verify_percent_of_rts_completed_approved(self):
        """
        Percent of rts completed and approved
        """
        text = self.webDriver.get_text(element=self.locators.RTS_Complete_Approved_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"RTS completed and Approved % is correct on Dashboard {calculation}")
        else:
            logger.error(f"RTS completed and Approved% is not correct on Dashboard {calculation}")

    def verify_percent_of_rts_completed_approval_pending(self):
        """
        Percent of rts completed and approval pending
        """
        text = self.webDriver.get_text(element=self.locators.RTS_Complete_Approval_Pending_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"RTS completed and Approval Pending  % is correct on Dashboard {calculation}")
        else:
            logger.error(f"RTS completed and Approval Pending % is not correct on Dashboard {calculation}")

    def verify_percent_of_rts_not_completed(self):
        """
        Percent of rts not completed
        """
        text = self.webDriver.get_text(element=self.locators.RTS_Not_Complete_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"RTS not completed % is correct on Dashboard {calculation}")
        else:
            logger.error(f"RTS not completed % is not correct on Dashboard {calculation}")

    def verify_percent_of_not_checked_in_onboard(self):
        """
        Percent of Not checked in onboard
        """
        text = self.webDriver.get_text(element=self.locators.Not_Checked_in_Onboard_count, locator_type='xpath')
        percent = str(text.split("%")[0])
        count = int(text.split("%")[1])

        calculation = str("{:.1f}".format((count / self.get_total_of_checked_in_non_checked_in_count()) * 100))

        if calculation == percent:
            logger.debug(f"Not Checked-In, Onboard % is correct on Dashboard {calculation}")
        else:
            logger.error(f"Not Checked-In, Onboard % is not correct on Dashboard {calculation}")

    def verify_report_tab_availability(self):
        """
        Function to check the availability of report tab
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.left_navigation_reports,
                                                       locator_type='xpath'):
            return True
        else:
            return False

    def open_reports_tab(self):
        """
        Function click the reports tab
        """
        self.webDriver.click(element=self.locators.left_navigation_reports, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('report_tab')

    def open_ipm_reports_tab(self):
        """
        Function click the IPM reports tab
        """
        self.webDriver.click(element=self.locators.left_navigation_IPM, locator_type='xpath')
        self.webDriver.allure_attach_jpeg('ipm_report_tab')
