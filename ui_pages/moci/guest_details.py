
from virgin_utils import *


class GuestDetails:
    """
    Page Class for MOCI Guest details page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of Guest List page
        :param web_driver:
        :param test_data:
        """
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = General.dict_to_ns({
            "loader": "//div[@class='app-loader-wrap app-overlays']",
            "personal_info": "//span[text()='Personal Information']",
            "first_name": "personalInfoObj-firstName",
            "last_name": "personalInfoObj-lastName",
            "middle_name": "personalInfoObj-middleName",
            "personal_dob": "personalInfoObj-birthDate",
            "personal_citizenship": "//div[@class='col-xs-4']//span[@class='Select-value-label']",
            "active_tab_guest_name": "//span[@class='name vertical-super text-uppercase']",

            "security_photorejectButton": "//button[contains(@title, 'security-photo-rejected-button')]",
            "security_photoapproveButton": "//button[contains(@title,'security-photo-approved-button')]",
            "security_reject_button_in_popup": "//button[contains(@title,'security-photo-rejected-button-in-popup')]",
            "rejection_reasons": "//div[@class='rejection']/ul/li",

            "passport_approve_button": "//button[@title='p-approved-button-1']",
            "passport_reject_button": "//button[contains(@title, 'p-rejected-button-1')]",
            "p_document_name": "//span[text()='Passport']",

            "saveandnext": "saveandnext",
            "savenextreservation": "saveandnextreservationPopUp",
            "next_reservation_in_popup": "//button[@id='popup-ok']",

            "passport_sirname": "P-surname",
            "passport_given_name": "P-givenName",
            "passport_birthday": "passportObj-birthDate",
            "visa_approve_button": "//button[contains(@title, 'v-approved-button-1')]",
            "visa_reject_button": "//button[contains(@title, 'v-rejected-button-1')]",

            "p_reject_reason": "//div[@class='reasons']//*[text()='Passport photo is not clear.']",
            "p_reject_pop": "//button[contains(@title, 'p-rejected-button-in-popu')]",
            "v_reject_reason": "//div[@class='reasons']//*[text()='Valid VISA photo is not provided.']",
            "v_reject_pop": "//button[contains(@title, 'v-rejected-button-in-popup')]",

            "pregnancy_info": "//span[text()='Pregnancy Details']",
            "payment_info": "//div[@class='col-xs-12 personal-information payment-method']",
            "voyage_contract": "//div[@class='col-xs-6 personal-information voyage-contract']",
            "signed": "//div/label[@for='contract-signed']",

            "days": "//div[contains(@class, 'react-datepicker__day react-datepicker')]",
            "months": "//select[@class='react-datepicker__month-select']",
            "years": "//select[@class='react-datepicker__year-select']",
            "guest_status": "//div[@class='overall-status vertical-super pull-right']//div//span",
            "add_comment": "additionalComments",
            "review_later": "//div/*[text() = 'Review Later']",
            "verify_review_later": "//div[@class = 'reviewLater-bubble is-reviewLater not-ellipsis']",
            "check_pending_status": "//div[@id='guest-%s']//div[@class='bubble is-pending']",
            "check_oci_not_started_status": "//div[@id='guest-%s']//div[@class='bubble is-ociNotStarted']",
            "check_in_incomplete_status": "//div[@id='guest-%s']//div[@class='bubble is-incomplete']",
            "in_complete_overdue_status": "//div[@id='guest-%s']//div[@class='bubble is-incompleteMessagedOverdue']",
            "edit_link": "//div[@class = 'edit']",
            "dob": "personalInfoObj-birthDate",
            "dob_arrow": "//button[@class='react-datepicker__close-icon']",
            "update": "//a[text()='Update']",
            "cancel": "//a[text()='CANCEL']",
            "update_msg": "//div[@class='col-xs-12 messageinfo-text']",
            "click_on_ok": "//button[@class='button btn btn-primary button btn btn-secondary ']"
        })

    def verify_guest_detail_page(self):
        """
        Function to check the availability of Guest Details page
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.personal_info, locator_type='xpath'):
            logger.debug("User land on Guest Details Page")
        else:
            raise Exception("Guest Details page not display")

    def availability_of_fn(self):
        """
        Function to check the availability of First name field
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.first_name, locator_type='id'):
            logger.debug("Guest First name field is available")
        else:
            raise Exception("Guest First name field is not available")

    def get_first_name_value(self):
        """
        Function to get the First Name
        :return:
        """
        first_name = self.webDriver.get_value_from_textbox(element=self.locators.first_name, locator_type='id')
        self.test_data["display_fn"] = first_name

    def get_middle_name_value(self):
        """
        Function to get the Middle Name
        :return:
        """
        middle_name = self.webDriver.get_value_from_textbox(element=self.locators.middle_name, locator_type='id')
        self.test_data["display_mn"] = middle_name

    def get_last_name_value(self):
        """
        Function to get the last Name
        :return:
        """
        last_name = self.webDriver.get_value_from_textbox(element=self.locators.last_name, locator_type='id')
        self.test_data["display_ln"] = last_name

    def displayed_complete_name(self):
        """
        Function to get the complete name of guest
        :return:
        """
        self.get_first_name_value()
        self.get_last_name_value()
        self.get_middle_name_value()
        if self.test_data["display_mn"] == "":
            name = f"{self.test_data['display_fn']} {self.test_data['display_ln']}"
            return name
        else:
            name = f"{self.test_data['display_fn']} {self.test_data['display_mn']} {self.test_data['display_ln']}"
            return name

    def availability_of_ln(self):
        """
        Function to check the availability of last name field
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.last_name, locator_type='id'):
            logger.debug("Guest last name field is available")
        else:
            raise Exception("Guest last name field is not available")

    def availability_of_dob(self):
        """
        Function to check the availability of last name field
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.personal_dob, locator_type='id'):
            logger.debug("Guest DOB field is available")
        else:
            raise Exception("Guest DOB field is not available")

    def get_dob_value(self):
        """
        Function to get the Date of Birth
        :return:
        """
        dob = self.webDriver.get_value_from_textbox(element=self.locators.personal_dob, locator_type='id')
        self.test_data["display_dob"] = dob

    def get_citizenship_value(self):
        """
        Function to get the citizenship
        :return:
        """
        citizenship = self.webDriver.get_text(element=self.locators.personal_citizenship, locator_type='xpath')
        self.test_data["display_citizenship"] = citizenship

    def availability_of_passport_exp(self):
        """
        Function to check the availability of Expiry date of Passport
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.passport_exp, locator_type='id'):
            logger.debug("Expiry date of Passport field is available")
        else:
            raise Exception("Expiry date of Passport field is not available")

    def availability_of_passport_number(self):
        """
        Function to check the availability of Passport Number
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.passport_number, locator_type='id'):
            logger.debug("Passport Number field is available")
        else:
            raise Exception("Passport Number field is not available")

    def reject_security_photo(self):
        """
        Function to reject the security Photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.security_photorejectButton,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" in class_value:
            logger.debug("Security photo is already rejected")
            return False
        else:
            self.webDriver.click(element=self.locators.security_photorejectButton, locator_type='xpath')
            self.webDriver.click(element=self.locators.reason_1, locator_type='xpath')
            self.webDriver.click(element=self.locators.reason_2, locator_type='xpath')
            self.webDriver.click(element=self.locators.security_reject_button_in_popup, locator_type='xpath')
            return True

    def approve_security_photo(self):
        """
        Function to approve the security Photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.security_photoapproveButton,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" in class_value:
            logger.debug("Security photo is already approved")
        else:
            self.webDriver.click(element=self.locators.security_photoapproveButton, locator_type='xpath')

    def check_availability_of_approve_button_with_security_photo(self):
        """
        Function to check the availability of approve button with security photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.security_photoapproveButton,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" not in class_value:
            logger.debug("Approve button is display with security photo")
            return True
        else:
            return False

    def check_availability_of_reject_button_with_security_photo(self):
        """
        Function to check the availability of reject button with security photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.security_photorejectButton,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" not in class_value:
            logger.debug("Reject button is display with security photo")
            return True
        else:
            return False

    def check_availability_of_approve_button_with_passport_photo(self):
        """
        Function to check the availability of approve button with Passport photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.passport_approve_button,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" not in class_value:
            logger.debug("Approve button is display with Passport photo")
            return True
        else:
            return False

    def check_availability_of_reject_button_with_passport_photo(self):
        """
        Function to check the availability of reject button with Passport photo
        :return:
        """
        class_value = self.webDriver.get_attribute(element=self.locators.passport_reject_button,
                                                   locator_type='xpath',
                                                   attribute_name='class')
        if "hide" not in class_value:
            logger.debug("Reject button is display with Passport photo")
            return True
        else:
            return False

    def get_document_name(self):
        """
        Get the selected Document name
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.p_document_name, locator_type='xpath'):
            return "Passport"

    def get_active_tab_guest_name(self):
        """
        Function to get the guest name of selected tab
        :return:
        """
        self.verify_guest_detail_page()
        guest_name = self.webDriver.get_text(element=self.locators.active_tab_guest_name, locator_type='xpath')
        return guest_name

    def approve_passport(self):
        """
        Function to approve the passport
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.passport_approve_button, locator_type='xpath')
        approve_passport_class_value = self.webDriver.get_attribute(element=self.locators.passport_approve_button,
                                                                    locator_type='xpath',
                                                                    attribute_name='class')
        if "hide" not in approve_passport_class_value:
            self.webDriver.click(element=self.locators.passport_approve_button, locator_type='xpath')

    def approve_visa(self):
        """
        Function to approve the passport
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.visa_approve_button, locator_type='xpath')
        self.webDriver.wait_for(5)
        approve_visa_class_value = self.webDriver.get_attribute(element=self.locators.visa_approve_button,
                                                                    locator_type='xpath',
                                                                    attribute_name='class')
        if "hide" not in approve_visa_class_value:
            self.webDriver.click(element=self.locators.visa_approve_button, locator_type='xpath')
        self.webDriver.wait_for(5)

    def fill_passport_details(self):
        """
        Fill the Birth Certification
        :return:
        """
        self.webDriver.scroll_till_element(element=self.locators.passport_approve_button, locator_type='xpath')

    def click_save_next(self):
        """
        Function to click on save and next button
        :return:
        """
        class_name = self.webDriver.get_attribute(element=self.locators.saveandnext,
                                                  locator_type='id',
                                                  attribute_name='class')
        if "disabled" in class_name:
            return False
        else:
            self.webDriver.click(element=self.locators.saveandnext, locator_type='id')
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=10)
            return True

    def click_save_next_reservation(self):
        """
        Function to click on save and next reservation button
        :return:
        """
        self.webDriver.click(element=self.locators.savenextreservation, locator_type='id')
        self.webDriver.click(element=self.locators.next_reservation_in_popup, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=60)

    def check_pregnancy_info(self):
        """
        Function to check the availability of pregnancy details
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.pregnancy_info, locator_type='xpath'):
            logger.debug("Pregnancy details are displayed")
        else:
            raise Exception("Pregnancy details are not display")

    def check_payment_info(self):
        """
        Function to check the Payament detatils
        return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.payment_info, locator_type='xpath'):
            logger.debug("Pregnancy details are displayed")
        else:
            raise Exception("Pregnancy details are not display")

    def check_voyage_contract_info(self):
        """
        Function to check voyage contract sign or not
        return:
        """

        if self.webDriver.is_element_display_on_screen(element=self.locators.voyage_contract, locator_type='xpath'):
            logger.debug("voyage contract is avaialavle")
        else:
            raise Exception("voyage contract is avaialavle")

        value = self.webDriver.is_element_enabled(element=self.locators.signed, locator_type='xpath')
        return value

    def check_status(self):
        """
        check status of guest
        """
        status = self.webDriver.get_text(element=self.locators.guest_status, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=5)

        return status

    def reject_passport(self):
        """
        To reject passport
        """
        self.webDriver.scroll_till_element(element=self.locators.passport_reject_button, locator_type='xpath')
        reject_passport_class_value = self.webDriver.get_attribute(element=self.locators.passport_reject_button,
                                                                    locator_type='xpath',
                                                                    attribute_name='class')
        if "hide" not in reject_passport_class_value:
            self.webDriver.click(element=self.locators.passport_reject_button, locator_type='xpath')

        self.webDriver.click(element=self.locators.p_reject_reason, locator_type='xpath')
        self.webDriver.click(element=self.locators.p_reject_pop, locator_type='xpath')

    def reject_visa(self):
        """
        To reject visa
        """
        self.webDriver.scroll_till_element(element=self.locators.visa_reject_button, locator_type='xpath')
        self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                        time_out=5)

        reject_visa_class_value = self.webDriver.get_attribute(element=self.locators.visa_reject_button,
                                                                    locator_type='xpath',
                                                                    attribute_name='class')
        if "hide" not in reject_visa_class_value:
            self.webDriver.click(element=self.locators.visa_reject_button, locator_type='xpath')
        self.webDriver.wait_for(5)

        self.webDriver.click(element=self.locators.v_reject_reason, locator_type='xpath')
        self.webDriver.click(element=self.locators.v_reject_pop, locator_type='xpath')

    def click_on_text_field(self):
        """
        click on text field to write comment
        """
        self.webDriver.scroll_till_element(element=self.locators.add_comment, locator_type='id')
        self.webDriver.click(element=self.locators.add_comment, locator_type='id')
        self.webDriver.set_text(element=self.locators.add_comment, locator_type='id', text="Write the comment here.")

    def verify_added_comment(self):
        """
        verify added comment
        """
        self.webDriver.scroll_till_element(element=self.locators.add_comment, locator_type='id')
        text = self.webDriver.get_text(element=self.locators.add_comment, locator_type='id')
        return text

    def check_availability_review_later(self):
        """
        check availability of review later functionality.
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.review_later, locator_type='xpath'):
            logger.debug("Review Later is available")
        else:
            raise Exception("Review Later is not available")

    def verify_review_later(self):
        """
        To verify review later functionality
        """
        self.webDriver.click(element=self.locators.review_later, locator_type='xpath')
        if not self.webDriver.is_element_display_on_screen(element=self.locators.verify_review_later, locator_type='xpath'):
            raise Exception("Review later is not visible")

    def check_status_in_guest_list(self, count):
        """
        Check status in guest list
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.check_oci_not_started_status % count,
                                                       locator_type='xpath'):
            return "not started"
        elif self.webDriver.is_element_display_on_screen(element=self.locators.check_in_incomplete_status % count,
                                                         locator_type='xpath'):
            return "Incomplete"
        elif self.webDriver.is_element_display_on_screen(element=self.locators.in_complete_overdue_status % count,
                                                         locator_type='xpath'):
            return "Incomplete Messaged Overdue"

    def check_edit_button_is_visible(self):
        """
        Verify the Guest edit name
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.edit_link, locator_type='xpath'):
            if self.webDriver.is_element_enabled(element=self.locators.edit_link, locator_type='xpath'):
                self.webDriver.click(element=self.locators.edit_link, locator_type='xpath')
            else:
                self.webDriver.allure_attach_jpeg('Edit Button/Link is visible but not enable on Guest info tab !!!')
                raise Exception("Edit Button/Link is visible but not enable on Guest info tab !!!")
        else:
            self.webDriver.allure_attach_jpeg('Edit Button/Link is not visible on Guest info tab !!!')
            raise Exception("Edit Button/Link is not visible on Guest info tab !!!")

    def verify_guest_name_disable_or_enable(self):
        """
        Verify the guest Name field is enable or disable
        :return:
        """
        guest_first_name = self.webDriver.is_element_enabled(element=self.locators.first_name,locator_type='id')
        guest_last_name = self.webDriver.is_element_enabled(element=self.locators.last_name,locator_type='id')
        guest_dob = self.webDriver.is_element_enabled(element=self.locators.dob,locator_type='id')
        if guest_first_name == guest_last_name == guest_dob == True:
            return "true"
        elif guest_first_name == guest_last_name == guest_dob == False:
            return "false"
        else:
            self.webDriver.allure_attach_jpeg('Tabs are not working fine, on Guest info tab !!!')
            raise Exception("first name:{fn}, Last name:{ln}, Dob:{ob} fields status. Enable ->  True, "
                            "Disable -> False !!!".format(fn=guest_first_name, ln=guest_last_name, ob=guest_dob))

    def edit_first_name_value(self):
        """
        Function to edit the First Name
        :return:
        """
        self.webDriver.click(element=self.locators.first_name, locator_type='id')
        self.get_first_name_value()
        if self.test_data["display_fn"].upper() == "TEST":
            content = "AUTOMATION"
        else:
            content = "TEST"
        self.webDriver.clear_text(element=self.locators.first_name, locator_type='id', action_type='action')
        self.webDriver.set_text(element=self.locators.first_name, locator_type='id', text=content)

    def edit_middle_name_value(self):
        """
        Function to edit the Middle Name
        :return:
        """
        self.webDriver.click(element=self.locators.middle_name, locator_type='id')
        self.webDriver.clear_text(element=self.locators.middle_name, locator_type='id', action_type='action')
        self.webDriver.set_text(element=self.locators.middle_name, locator_type='id', text="AUTOMATION")

    def edit_last_name_value(self):
        """
        Function to edit the last Name
        :return:
        """
        self.webDriver.click(element=self.locators.last_name, locator_type='id')
        self.webDriver.clear_text(element=self.locators.last_name, locator_type='id', action_type='action')
        self.webDriver.set_text(element=self.locators.last_name, locator_type='id', text="TEST")

    def edit_dob_value(self):
        """
        Function to edit the last Name
        :return:
        """
        self.webDriver.click(element=self.locators.dob_arrow, locator_type='xpath')
        self.webDriver.click(element=self.locators.dob, locator_type='id')
        self.webDriver.set_text(element=self.locators.dob, locator_type='id', text="0")

    def verify_the_update_and_cancel_button(self):
        """
        TO verify the Guest update and cancel button
        :return:
        """
        if self.webDriver.is_element_display_on_screen(element=self.locators.update, locator_type='xpath') and\
                self.webDriver.is_element_display_on_screen(element=self.locators.cancel, locator_type='xpath') and\
                self.webDriver.is_element_enabled(element=self.locators.update, locator_type='xpath') and\
                self.webDriver.is_element_enabled(element=self.locators.cancel, locator_type='xpath'):
            self.webDriver.click(element=self.locators.update, locator_type='xpath')
            self.webDriver.explicit_visibility_of_element(element=self.locators.update_msg, locator_type='xpath',
                                                              time_out=60)
            if self.webDriver.is_element_display_on_screen(element=self.locators.update_msg, locator_type='xpath'):
                txt = self.webDriver.get_text(element=self.locators.update_msg, locator_type='xpath')
                if txt == 'Personal Information has been updated successfully.':
                    if self.webDriver.is_element_display_on_screen(element=self.locators.click_on_ok, locator_type='xpath') \
                            and self.webDriver.is_element_enabled(element=self.locators.click_on_ok, locator_type='xpath'):
                        self.webDriver.click(element=self.locators.click_on_ok, locator_type='xpath')
                    else:
                        self.webDriver.allure_attach_jpeg('OK button is not visible and enable !!!')
                        raise Exception("OK Button is not visible and enable !!!")
                else:
                    self.webDriver.allure_attach_jpeg('updated message is not matched !!!')
                    raise Exception("Updated message is not matched !!!")
            else:
                self.webDriver.allure_attach_jpeg('update Pop-Up is not visible !!!')
                raise Exception("Update Pop-Up is not visible !!!")
        else:
            self.webDriver.allure_attach_jpeg('update and cancel button is not visible and enable on Guest info tab !!!')
            raise Exception("Update and cancel button is not visible and enable on Guest info tab !!!")
