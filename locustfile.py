import json
from locust import HttpLocust, TaskSet, task
import base64
from decurtis.common import *
from decurtis.rest import SendRestRequest


class UserBehavior(TaskSet):
    """
    Locust User Behavior File
    """

    def __init__(self, parent):
        """
        Init Function
        :param parent:
        """
        super().__init__(parent)

    @task(1)
    def get_track_ables(self):
        """
        Get Token
        :return:
        """
        headers = dict()
        for header in self.parent.rest_ship_crew.session.headers:
            headers[header] = self.rest_ship_crew.session.headers[header]
        response = self.client.get('/trackable-service/trackables', headers=headers)
        content = json.loads(response.content.decode('utf-8'))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = 'https://dev-sagar.dxp-decurtis.com'

    ship = 'https://dev-sagar.dxp-decurtis.com'
    shore = 'https://dev-shore.dxp-decurtis.com'
    auth_oci = "MjU3NWIzMGItNjkzMC00Y2ZiLTk3NzMtNDY2MjllMDk4ODhlOnRlYW0tZ2VuZXNpcw=="
    auth_moci = "NTAzOTMxNjktY2E5YS00Njk5LWIyZDEtNGE5YWJkNGI2NzM1OmR4cG1vZGVyYXRlb25saW5lY2hlY2tpbkAxMjM="

    rest_oci = rest_oci(ship, shore, rest_oci, auth_moci)
    rest_ship = rest_ship(ship, shore, rest_oci, auth_moci)
    rest_oci_crew = rest_oci_crew(ship, shore, rest_oci, auth_moci)
    rest_ship_crew = rest_ship_crew(ship, shore, rest_oci, auth_moci)

    min_wait = 1000
    max_wait = 2000
    stop_timeout = 1200


def rest_oci(ship, shore, auth_oci, auth_moci):
    """
    Rest Session Fixture for OCI
    :param request:
    :param test_data:
    :return:
    """
    _user_pass = base64.b64decode(auth_oci).decode()
    _user = str(_user_pass).split(":")[0]
    _pass = str(_user_pass).split(":")[1]
    _host = urljoin(shore, "reservation-bff/auth")
    response = SendRestRequest(host=_host, username=_user, password=_pass)
    return response


def rest_ship(ship, shore, auth_oci, auth_moci):
    """
    Rest Session Fixture for OCI
    :param request:
    :param test_data:
    :return:
    """
    _user_pass = base64.b64decode(auth_moci).decode()
    _user = str(_user_pass).split(":")[0]
    _pass = str(_user_pass).split(":")[1]
    _host = urljoin(shore, "reservation-bff/auth")
    response = SendRestRequest(host=_host, username=_user, password=_pass)
    return response


def rest_oci_crew(ship, shore, auth_oci, auth_moci):
    """
    Rest Session Fixture for Generating token for Gangway
    :param request:
    :param test_data:
    :return:
    """
    _user_pass = base64.b64decode(auth_oci).decode()
    _user = str(_user_pass).split(":")[0]
    _pass = str(_user_pass).split(":")[1]
    _host = urljoin(shore, "reservation-bff/auth")
    response = SendRestRequest(host=_host, username=_user, password=_pass)

    _host = "{}/user-account-service/signin/email".format(ship)
    body = {"userName": "rosa.yang@gmail.com", "password": "1234", "appId": "38c1ab51-ce97-439c-9d20-c48d724e1fe5"}
    response.session.headers.update({
        "Content-Type": "application/json"
    })
    _content = process_response(response.session.post(url=_host, json=body)).content
    response.userToken = "{} {}".format(_content['tokenType'], _content['accessToken'])
    return response


def rest_ship_crew(ship, shore, auth_oci, auth_moci):
    """
    Rest Session Fixture for Generating token for Gangway
    :param request:
    :param test_data:
    :return:
    """
    _user_pass = base64.b64decode(auth_moci).decode()
    _user = str(_user_pass).split(":")[0]
    _pass = str(_user_pass).split(":")[1]
    _host = urljoin(shore, "reservation-bff/auth")
    response = SendRestRequest(host=_host, username=_user, password=_pass)

    # Get User Token
    _host = "{}/identityaccessmanagement-service/oauth/token?grant_type=password".format(ship)
    body = {
        "username": "rosa.yang",
        "password": "1234",
        "appId": "a7c8d0ac-7e69-11e7-a7e8-0a1a4261e962"
    }
    response.session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    _content = process_response(response.session.post(url=_host, json=body)).content
    response.userToken = "{} {}".format(_content['token_type'], _content['access_token'])
    response.session.headers.update({'Content-Type': 'application/json'})
    return response


if __name__ == "__main__":
    print()
    WebsiteUser().run()
