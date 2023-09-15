__author__ = 'prahlad.sharma'



from virgin_utils import *


class IncidentList(General):
    """
    Page Class for Incident Management list page
    """

    def __init__(self, web_driver, test_data):
        """
        To Initialize the locators of details page
        :param web_driver:
        """
        super().__init__()
        self.webDriver = web_driver
        self.test_data = test_data
        self.locators = self.dict_to_ns({
            "loader": "//div[@class='LoaderContainer__div']//img",
            "aims_data": "//span/span[text()='AIMS#']/../following-sibling::span[@class='tag-value-data']",
            "incident_location": "//div[@class='incident-card-location']",
            "incident_category": "incident-card-category",
            "all_incident": "//div[@class='cardlistpadding  ']",
            "AOMS_value": "//span[@class='tag-value-data' and text()='%s']"
        })

    def verify_incident(self, flag):
        """
        Function to verify the incident in assigned tab
        :param flag:
        :return:
        """
        aoms_list = self.webDriver.get_elements(element=self.locators.aims_data, locator_type='xpath')
        for lists in aoms_list:
            if lists.text == self.test_data["AIMS#"]:
                if flag:
                    self.webDriver.wait_for(5)
                    lists.click()
                    self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                                    time_out=60)
                    break
                else:
                    logger.info("Incident found")
                    break
        else:
            raise Exception("Created Incident is not display in Assigned Tab")

    def open_incident_details_page(self):
        """
        Function to open incident page
        :return:
        """
        all_list = self.webDriver.get_elements(element=self.locators.all_incident, locator_type='xpath')
        for incident in all_list:
            incident.click()
            self.webDriver.explicit_invisibility_of_element(element=self.locators.loader, locator_type='xpath',
                                                            time_out=60)
            break
        else:
            self.webDriver.allure_attach_jpeg('blank incident')
            raise Exception("Incident not available in list")
