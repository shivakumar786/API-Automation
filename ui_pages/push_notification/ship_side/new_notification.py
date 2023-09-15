__author__ = 'saloni.pattnaik'

from selenium.webdriver.common.keys import Keys
from virgin_utils import *


class Notification(General):
    """
    Page Class for new notification page
    """

    def __init__(self, web_driver):
        """
        To Initialize the locators of notification page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.locators = self.dict_to_ns({
            "header_title": "//*[text()='New Notification']",
            "loader": "//div[@class='LoaderContainer__div']//img",
            "free_form": "//span[text()='free form']",
            "template": "//span[text()='template']",
            "success": "//div[text()='Success']",
            "notification_title": "//input[@id='freeform-notification-title']",
            "text_area": "//div//textarea[@id='filled-basic-template']",
            "url": "//input[@id='filled-basic-externalUrl']",
            "add_recipient_button": "//span[text()='ADD RECIPIENTS']",
            "recipients": "//div[@data-cy='recipients-dropdown']//input[@type='text']",
            "select_cabin_button": "//span[text()='Select Cabins']",
            "all_checkbox": "//input[@name='checkedCabins']/..",
            "deck_list": "//div[@class='decks-listing']/div",
            "deck": "//div[@class='decks-listing']/div[%s]",
            "all_cabin_checkbox": "//input[@name='All']",
            "ok_button": "//span[text()='OK']",
            "done_button": "//span[text()='DONE']",
            "cabin_count": "//div//h6[text()='Total Selected']//span",
            "send_button": "(//span[text()='SEND'])[%s]",
            "search_bar": "//input[@placeholder='Search by Keyword']",
            "notification_list": "//div[@class='MuiCardContent-root']//mark",
            "view_details_button": "(//div[@class='MuiCardContent-root']//mark)[1]/../../../..//span[text()=' View List ']",
            "update_button": "(//div[@class='MuiCardContent-root']//mark)[1]/../../../../button/span[text()='UPDATE & SEND']",
            "total_recipients": "//h6[text()='Total Recipients']//span",
            "message": "(//div[@class='MuiCardContent-root']//mark)/../../../..//h6//span/mark",
            "clean": "//button[@aria-label='To Clean']",
            "close": "//button[@aria-label='close']",
            "delete": "//*[text()='DELETE']",
            "delete_button": "//*[@id='customized-dialog-title']/following-sibling::div//button/span[text()='DELETE']",
            "templates": "//li[@class='MuiListItem-container']",
            "template_title": "(//li[@class='MuiListItem-container'][%s]//h6)[1]/span/span",
            "mark": "//li[@class='MuiListItem-container']//mark",
            "template_search_bar": "//input[@placeholder='Search by keyword']",
            "title_name": "(//li[@class='MuiListItem-container'][%s]//h6)[1]/span/mark",
            "template_arrow": "//li[@class='MuiListItem-container']['%s']/..//div[@class='MuiListItemSecondaryAction-root']//img",
            "text": "(//input[@id='filled-basic-'])[1]",
            "number": "//input[@type='number']",
            "added_title": "//div[@role='tabpanel']/div/p[2]",
            "schedule_radio_btn": "//span[text()='Schedule for current Voyage']",
            "days": "//div[@id='demo-select-filled-days']",
            "template_time": "notification-time",
            "schedule_time": "(//input[@id='notification-time'])[2]",
            "hour_selection": "//span[@class='MuiTypography-root MuiPickersClockNumber-clockNumber MuiTypography-body1']",
            "ok": "//span[text()='OK']",
            "save": "//*[text()='SAVE']",
            "cancel_sailor": "//span[text()='CANCEL']",
            "save_draft": "//*[text()='SAVE AS DRAFT']",
            "edit_button": "//span[text()='EDIT']",
            "deck_number": "//span[text()='Deck']/ancestor::div[@class='MuiTypography-root MuiTypography-body2']/../h5/div/div",
            "deck_status": "//div[@class='deck-component']//div/div",
            "search_sailor_radio": "//input[@value='SEARCH']",
            "event_radio": "//input[@value='EVENTS']",
            "search_sailor_bar": "//div[@class='search-input']//input[@type='text']",
            "sailor_name": "//div[@class='search-option-item']",
            "close_icon": "//div[@class='search-input']//span[@class='MuiIconButton-label']",
            "event_type": "demo-select-filled-event-type",
            "event": "demo-select-filled-event",
            "slot": "demo-select-filled-slot",
            "cancel": "//span[text()='CANCEL']",
            "delete_template": "//*[text()='DELETE']",
            "search_not_fount_message": "//*[contains(text(),'Oops!')]",
            "public_tab": "//*[text()='PUBLIC']",
            "Private_tab":"//*[text()='PRIVATE']",
            "delete_temp": "(//*[text()='DELETE'])[2]",
            "no_recipients": "//h6[text()=' No recipients to display']"
        })

    def cancel_sailor(self):
        """
        Click sailor cancel button
        :return:
        """
        self.webDriver.click(element=self.locators.cancel_sailor, locator_type='xpath')

    def wait_for_loader_to_complete(self):
        """
        Function to wait for page loading to complete
        :return:
        """
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=120)

    def get_deck_number(self):
        """
        To get selected deck number
        :return:
        """
        return self.webDriver.get_text(element=self.locators.deck_number, locator_type='xpath')

    def schedule_for_current_voyage(self):
        """
        To schedule for current voyage
        :return:
        """
        self.webDriver.click(element=self.locators.schedule_radio_btn, locator_type='xpath')
        self.webDriver.scroll_complete_page()
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.days, locator_type='xpath')
        self.webDriver.key_chains().send_keys(Keys.ARROW_DOWN, Keys.ENTER).perform()
        start_slot_time = datetime.now(timezone("Asia/Kolkata")).time().strftime("%I:%M%p")
        datetime_object = datetime.strptime(start_slot_time, '%I:%M%p')
        now_plus_15m = datetime_object + timedelta(minutes=50)
        new_time = str(now_plus_15m.strftime("%I:%M %p"))
        if len(self.webDriver.get_elements(element=self.locators.template_time, locator_type='id')) > 1:
            self.webDriver.explicit_visibility_of_element(element=self.locators.schedule_time, locator_type='id',
                                                          time_out=120)
            self.webDriver.click(element=self.locators.schedule_time, locator_type='xpath')
            self.webDriver.clear_text(element=self.locators.schedule_time, locator_type='xpath', action_type='action')
            self.webDriver.set_text(element=self.locators.schedule_time, locator_type='xpath', text=new_time)
        else:
            self.webDriver.explicit_visibility_of_element(element=self.locators.template_time, locator_type='id',
                                                          time_out=120)
            self.webDriver.click(element=self.locators.template_time, locator_type='id')
            self.webDriver.clear_text(element=self.locators.template_time, locator_type='id', action_type='action')
            self.webDriver.set_text(element=self.locators.template_time, locator_type='id', text=new_time)

    def enter_url(self, config):
        """
        To enter url
        :param config:
        """
        url = urljoin(config.ship.url.replace('/svc', ''), "/notificationManagement/login")
        self.webDriver.set_text(element=self.locators.url, locator_type='xpath', text=url)
        self.wait_for_loader_to_complete()

    def create_template_notification_schedule_voyage(self, recipient_category, cabin):
        """
        To create new template notification with scheduled voyage
        :param cabin:
        :param recipient_category:
        :return:
        """
        self.webDriver.click(element=self.locators.add_recipient_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.set_text(element=self.locators.recipients, locator_type='xpath', text=recipient_category)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(
            Keys.ARROW_DOWN)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ENTER)
        if (recipient_category == 'sailor' or recipient_category == 'crew') and cabin is None:
            self.select_cabins_from_deck()
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            self.wait_for_loader_to_complete()
            total_cabin_count = self.get_list_count()
            time.sleep(5)
            self.webDriver.explicit_visibility_of_element(element=self.locators.save, locator_type='xpath', time_out=120)
            self.webDriver.click(element=self.locators.save, locator_type='xpath')
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
            return total_cabin_count
        elif recipient_category == 'sailor' and cabin is not None:
            self.webDriver.scroll_complete_page()
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.search_sailor_radio, locator_type='xpath')
            self.webDriver.click(element=self.locators.search_sailor_bar, locator_type='xpath')
            self.webDriver.set_text(element=self.locators.search_sailor_bar, locator_type='xpath', text=cabin)
            self.webDriver.wait_for(5)
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.sailor_name, locator_type='xpath')
            self.webDriver.click(element=self.locators.close_icon, locator_type='xpath')
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.save, locator_type='xpath')
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
        else:
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            self.wait_for_loader_to_complete()
            total_cabin_count = self.get_list_count()
            self.webDriver.click(element=self.locators.save, locator_type='xpath')
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
            return total_cabin_count

    def select_random_template(self, test_data):
        """
        To select any random template title from template list
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.template_search_bar, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.template_search_bar, locator_type='xpath',
                                text=test_data['templateTitle'])
        self.webDriver.get_web_element(element=self.locators.template_search_bar, locator_type='xpath').send_keys(
            Keys.ENTER)
        self.wait_for_loader_to_complete()

    def select_template_arrow(self, test_data):
        """
        To select searched template arrow button
        :param test_data:
        :return:
        """
        self.webDriver.click(element=self.locators.template_arrow % test_data['templateTitle'], locator_type='xpath')

    def create_new_template_notification(self, config, recipient_category):
        """
        To create new template notification
        :param config:
        :param recipient_category:
        :return:
        :return:
        """
        url = urljoin(config.ship.url.replace('/svc', ''), "/notificationManagement/login")
        self.webDriver.set_text(element=self.locators.url, locator_type='xpath', text=url)
        self.webDriver.click(element=self.locators.add_recipient_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.set_text(element=self.locators.recipients, locator_type='xpath', text=recipient_category)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(
            Keys.ARROW_DOWN)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ENTER)
        if recipient_category == 'sailor' or recipient_category == 'crew':
            self.select_cabins_from_deck()
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
        else:
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        total_cabin_count = self.get_list_count()
        self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
        self.webDriver.click(element=self.locators.send_button % 2, locator_type='xpath')
        self.wait_for_loader_to_complete()
        return total_cabin_count

    def create_new_free_form_notification(self, config, test_data, recipient_category, scheduling):
        """
        To create new free form notification
        :param scheduling:
        :param recipient_category:
        :param test_data:
        :param config:
        :return:
        """
        notification_title = self.create_random_notification_title(5)
        test_data['TitleText'] = "Automation title " + notification_title
        test_data['message'] = self.create_random_notification_message(5)
        url = urljoin(config.ship.url.replace('/svc', ''), "/notificationManagement/login")
        self.webDriver.set_text(element=self.locators.notification_title, locator_type='xpath',
                                text=test_data['TitleText'])
        self.webDriver.set_text(element=self.locators.text_area, locator_type='xpath', text=test_data['message'])
        self.webDriver.set_text(element=self.locators.url, locator_type='xpath', text=url)
        if scheduling == 'current_voyage':
            self.schedule_for_current_voyage()
        self.webDriver.click(element=self.locators.add_recipient_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.set_text(element=self.locators.recipients, locator_type='xpath', text=recipient_category)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(
            Keys.ARROW_DOWN)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ENTER)
        if recipient_category == 'sailor' or recipient_category == 'crew':
            self.select_cabins_from_deck()
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            self.wait_for_loader_to_complete()
        else:
            self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
            self.wait_for_loader_to_complete()
        total_cabin_count = self.get_list_count()
        return total_cabin_count

    def click_save_button(self, scheduling):
        """
        To click on either save or send button
        :param scheduling:
        :return:
        """
        if scheduling == 'current_voyage':
            self.webDriver.click(element=self.locators.save, locator_type='xpath')
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
        else:
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.send_button % 2, locator_type='xpath')
            self.wait_for_loader_to_complete()

    def select_cabins_from_deck(self):
        """
        To select cabins from deck as recipient
        :return:
        """
        self.webDriver.click(element=self.locators.select_cabin_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.ok_button, locator_type='xpath')

    def verify_created_notification(self, title):
        """
        To verify created notification is coming on dashboard or not
        :param title:
        :return:
        """
        self.wait_for_loader_to_complete()
        for retry in range(0, 10):
            self.webDriver.explicit_visibility_of_element(element=self.locators.search_bar, locator_type='xpath', time_out=60)
            self.webDriver.clear_text(element=self.locators.search_bar, locator_type='xpath', action_type="clear")
            self.webDriver.set_text(element=self.locators.search_bar, locator_type='xpath', text=title)
            self.webDriver.get_web_element(element=self.locators.search_bar, locator_type='xpath').send_keys(Keys.ENTER)
            self.wait_for_loader_to_complete()
            notification_list = self.webDriver.get_elements(element=self.locators.notification_list,
                                                            locator_type='xpath')
            for name in notification_list:
                if name.text == title:
                    return True
        else:
            return False

    def verify_message(self, test_data):
        """
        To verify message is matching or not
        :param test_data:
        :return:
        """
        self.clean_search_bar()
        self.webDriver.wait_for(3)
        self.webDriver.set_text(element=self.locators.search_bar, locator_type='xpath', text=test_data['message'])
        self.webDriver.get_web_element(element=self.locators.search_bar, locator_type='xpath').send_keys(Keys.ENTER)
        notification_list = self.webDriver.get_elements(element=self.locators.notification_list, locator_type='xpath')
        if len(notification_list) == 0:
            return 0
        else:
            for name in notification_list:
                if name.text == test_data['message']:
                    return True
                else:
                    return False

    def clean_search_bar(self):
        """
        To clean the search bar
        :return:
        """
        self.wait_for_loader_to_complete()
        is_displayed = self.webDriver.is_element_display_on_screen(element=self.locators.clean, locator_type='xpath')
        if is_displayed:
            self.webDriver.click(element=self.locators.clean, locator_type='xpath')

    def delete_notification(self):
        """
        To delete notification
        :return:
        """
        self.webDriver.click(element=self.locators.delete, locator_type='xpath')
        self.webDriver.click(element=self.locators.delete_button, locator_type='xpath')
        self.wait_for_loader_to_complete()

    def view_list(self):
        """
        To verify the list of cabins
        :return:
        """
        self.webDriver.click(element=self.locators.view_details_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        recipient = self.webDriver.get_text(element=self.locators.total_recipients, locator_type='xpath')
        time.sleep(5)
        self.webDriver.press_escape_key()
        return recipient

    def update_and_save(self):
        """
        To verify the list of cabins
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.update_button, locator_type='xpath')
        self.webDriver.click(element=self.locators.update_button, locator_type='xpath')
        self.wait_for_loader_to_complete()

    def update_message(self, test_data):
        """
        To update message content
        :param test_data
        :return:
        """
        self.webDriver.scroll_complete_page_top()
        test_data['message'] = test_data['message']+" updated"
        self.webDriver.click(element=self.locators.text_area, locator_type='xpath')
        self.webDriver.clear_text(element=self.locators.text_area, locator_type='xpath', action_type='action')
        self.webDriver.set_text(element=self.locators.text_area, locator_type='xpath', text=test_data['message'])
        self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.send_button % 2, locator_type='xpath')
        self.wait_for_loader_to_complete()

    def update_recipient_list(self, test_data):
        """
        To update message content
        :param test_data
        :return:
        """
        self.webDriver.click(element=self.locators.edit_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.select_cabins_from_deck()
        self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        new_deck_number = self.get_deck_number()
        self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
        self.webDriver.click(element=self.locators.send_button % 2, locator_type='xpath')
        self.wait_for_loader_to_complete()
        return new_deck_number

    def get_list_count(self):
        """
        To get the count of selected cabin list
        :return:
        """
        return self.webDriver.get_text(element=self.locators.cabin_count, locator_type='xpath')

    def verify_header(self):
        """
        To verify page header of distribution list
        """
        screen_title = self.webDriver.get_text(element=self.locators.header_title, locator_type='xpath')
        if screen_title == "New Notification":
            logger.debug("User is land on new notification page of Push Notification")
        else:
            raise Exception("user is not on new notification page of Push Notification")

    def select_free_form(self):
        """
        To select free form option
        :return:
        """
        self.webDriver.click(element=self.locators.free_form, locator_type='xpath')

    def select_template(self):
        """
        To select template option
        :return:
        """
        self.webDriver.click(element=self.locators.template, locator_type='xpath')

    def create_random_notification_title(self, length):
        """
        To generate random notification title
        :param length:
        :return:
        """
        title = ''.join((random.choice(string.ascii_letters) for x in range(length)))
        return title

    def create_random_notification_message(self, length):
        """
        To generate random notification message
        :param length:
        :return:
        """
        today_date = date.today().strftime("%m/%d/%Y")
        time = datetime.now().time().strftime("%H:%M")
        message = "Automation message generated by " + ''.join((random.choice(string.ascii_letters)
                                                                for x in
                                                                range(length))) + " on " + today_date + " at " + time
        return message

    def get_deck_list_count(self):
        """
        To get the count of deck list
        :return:
        """
        return self.webDriver.get_elements(element=self.locators.deck_list, locator_type='xpath')

    def verify_created_scheduled_notification(self, title):
        """
        To verify created notification is coming on dashboard or not
        :param title:
        :return:
        """
        self.clean_search_bar()
        self.webDriver.click(element=self.locators.template_search_bar, locator_type='xpath')
        self.webDriver.set_text(element=self.locators.template_search_bar, locator_type='xpath', text=title)
        self.webDriver.get_web_element(element=self.locators.template_search_bar, locator_type='xpath').send_keys(Keys.ENTER)
        self.webDriver.wait_for(3)
        notification_list = self.webDriver.get_elements(element=self.locators.notification_list, locator_type='xpath')
        for name in notification_list:
            if name.text == title:
                return True
            else:
                return False

    def save_as_draft(self):
        """
        To click on save draft button
        :return:
        """
        self.webDriver.click(element=self.locators.save_draft, locator_type='xpath')
        self.wait_for_loader_to_complete()

    def create_event_notification_schedule_voyage(self, recipient_category):
        """
        To verify user is able to send notification to any of the event slot like (shore thing, ent-inventoried etc)
        :param recipient_category:
        :return:
        """
        self.webDriver.click(element=self.locators.add_recipient_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        self.webDriver.set_text(element=self.locators.recipients, locator_type='xpath', text=recipient_category)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(
            Keys.ARROW_DOWN)
        self.webDriver.get_web_element(element=self.locators.recipients, locator_type='xpath').send_keys(Keys.ENTER)
        self.webDriver.scroll_complete_page()
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.event_radio, locator_type='xpath')
        self.webDriver.move_to_element_and_double_click(element=self.locators.event_type, locator_type='id')
        self.wait_for_loader_to_complete()
        self.webDriver.move_to_element_and_double_click(element=self.locators.event, locator_type='id')
        self.wait_for_loader_to_complete()
        self.webDriver.move_to_element_and_double_click(element=self.locators.slot, locator_type='id')
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.done_button, locator_type='xpath')
        self.wait_for_loader_to_complete()
        is_displayed = self.webDriver.is_element_display_on_screen(element=self.locators.no_recipients, locator_type='xpath')
        if is_displayed:
            self.webDriver.click(element=self.locators.cancel, locator_type='xpath')
            return True
        else:
            self.webDriver.click(element=self.locators.save, locator_type='xpath')
            self.wait_for_loader_to_complete()
            self.webDriver.click(element=self.locators.send_button % 1, locator_type='xpath')
            self.wait_for_loader_to_complete()
            return False

    def delete_template_and_verify(self):
        """
        To verify user is able to delete template
        :return:
        """
        self.webDriver.click(element=self.locators.delete_template, locator_type="xpath")
        self.webDriver.click(element=self.locators.delete_temp, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.public_tab, locator_type="xpath")
        self.wait_for_loader_to_complete()
        self.webDriver.click(element=self.locators.Private_tab, locator_type="xpath")
        self.wait_for_loader_to_complete()
        search_response = self.webDriver.get_text(element=self.locators.search_not_fount_message, locator_type="xpath")
        assert search_response == "Oops! We couldn't find the thing you are looking for. Try with something else.", \
            "failed to delete created template "
