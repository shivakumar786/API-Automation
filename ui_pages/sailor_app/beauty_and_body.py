__author__ = 'vanshika.arora'

from virgin_utils import *


class Beauty_and_body(General):
    """
    Page class for Beauty And body page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "redemption_spa": "//div[@id='SpaceItem_1']",
            "beauty_and_body": "/h1[text()=Beauty & Body']",
            "acupuncture_section": "//div[text()='Acupuncture']",
            'resurrection_acupuncture': "//div[text()='Resurrection Acupuncture']",
            'choose_a_treatment_btn': "//button[@id='BookBtn']",
            'loading': '//img[@alt="loading..."]',
            'spa_slots': "//span[@class='MenuItem__text-value']",
            'slots_time': "//div[@class='time-item']",
            'next_btn': "//button[@id='nextButton']",
            'days_available_to_choose': "//div[@class='day-item']",
            'day_selected': "//div[@class='day-item selected']"
        })

    def verify_availability_of_beauty_and_body_header(self):
        """
        Function to verify beauty and body header available on the screen
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.beauty_and_body, locator_type='xpath'):
            logger.debug("Beauty and Body header is available on screen, hence user has landed on spa listing screen")
        else:
            raise Exception("Beauty and Body header is not available on screen, hence user has not landed on spa listing screen")


    def open_redemption_spa(self):
        """
        Function to open redemption spa
        :return:
        """
        self.webDriver.click(element=self.locators.redemption_spa, locator_type='xpath')

    def open_acupuncture(self):
        """
        Click Acupuncture section
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.acupuncture_section,
                                                          locator_type='xpath')
        self.webDriver.scroll_till_element(element=self.locators.acupuncture_section, locator_type='xpath')
        self.webDriver.click(element=self.locators.acupuncture_section, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.resurrection_acupuncture,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.resurrection_acupuncture, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')

    def book_resurrection_acupuncture(self, test_data):
        """
        Book resurrection acupuncture
        :param test_data:
        :return:
        """
        contexts = self.webDriver.get_contexts()
        self.webDriver.set_context(contexts=contexts, context_name='WEBVIEW_com.virginvoyages.guest.integration')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.choose_a_treatment_btn,
                                                          locator_type='xpath')
        self.webDriver.click(element=self.locators.choose_a_treatment_btn, locator_type='xpath')
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.spa_slots, locator_type='xpath')
        available_spa_slots = self.webDriver.get_elements(element=self.locators.spa_slots, locator_type='xpath')
        if len(available_spa_slots) == 0:
            test_data['spa_slots_availability'] = False
            return
        for slot in available_spa_slots:
            slot.click()
            test_data['spa_slots_availability'] = True
            break
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.loading, locator_type='xpath')
        if self.webDriver.is_element_display_on_screen(element=self.locators.day_selected,
                                                       locator_type='xpath'):
            day_selected = int(self.webDriver.get_text(element=self.locators.day_selected,
                                                       locator_type='xpath').split("\n")[1])
            available_days = self.webDriver.get_elements(element=self.locators.days_available_to_choose,
                                                         locator_type='xpath')
            for day in available_days:
                if int(day.text.split("\n")[1]) > day_selected + 1:
                    day.click()
                    break
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.slots_time, locator_type='xpath')
        time_slots = self.webDriver.get_elements(element=self.locators.slots_time, locator_type='xpath')
        for slot in time_slots:
            slot.click()
            break
        self.webDriver.wait_till_element_appear_on_screen(element=self.locators.next_btn, locator_type='xpath')
        self.webDriver.click(element=self.locators.next_btn, locator_type='xpath')
        self.webDriver.wait_till_element_disappear_from_screen(element=self.locators.next_btn, locator_type='xpath')
