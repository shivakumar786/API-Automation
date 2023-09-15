__author__ = 'vanshika.arora'

from virgin_utils import *


class Guides(General):
    """
    Page class for huides page
    """

    def __init__(self, web_driver):
        """
        To initialise the locators
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "guides_header": "//h1[text()='Guides']",
            "guides_cards": "//div[@class='PromoCard__title']",
            "guide_card_details_title": "//div[text()='%s']",
            "back_button": "back-btn",
            "guide_title": "//div[@class='PageTitle--highlighted']",
            "source_iframe": "//iframe[@id='moods-editorial']",
        })

    def verify_user_landed_on_guides_page(self):
        """
        Function to verify that user has landed on guides page
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.guides_header, locator_type='xpath'):
            logger.debug("User has landed on guides page")
        else:
            raise Exception("User has not landed on guides page")

    def open_and_verify_guides(self):
        """
        Function to verify that user is able to access guides
        """
        get_all_cards = self.webDriver.get_elements(element=self.locators.guides_cards, locator_type='xpath')
        for card in get_all_cards:
            guide_card_title = card.text
            card.click()
            self.webDriver.explicit_visibility_of_element(element=self.locators.source_iframe, locator_type='xpath'
                                                          , time_out=60)
            self.webDriver.switch_to_iframe(frame_reference=self.webDriver.get_web_element(element=self.locators.source_iframe,
                                                               locator_type='xpath'))
            self.webDriver.explicit_visibility_of_element(element=self.locators.guide_title,locator_type='xpath',time_out=60)
            guide_text = self.webDriver.get_text(element=self.locators.guide_title, locator_type='xpath')
            assert guide_card_title == guide_text, "User has landed on guide detail screen"
            self.webDriver.scroll_complete_page()
            self.webDriver.switch_to_default_content()
            self.webDriver.click(element=self.locators.back_button, locator_type='id')
