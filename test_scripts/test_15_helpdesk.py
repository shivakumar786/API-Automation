__author__ = 'piyush.kumar'

from virgin_utils import *

@pytest.mark.SHIP
@pytest.mark.HELPDESK
@pytest.mark.run(order=16)
class TestHelpdesk:
    """
    Test Suite to test Helpdesk

    """

    @pytestrail.case(30467786)
    def test_01_add_vq_definition(self, config, guest_data, test_data, rest_ship):
        """
        Add vq definition
        :param guest_data:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueuedefinitions")
        _name = f"{guest_data[0]['FirstName']}_{(random.randint(10, 99))} sample VQ for e2e"
        body = {"virtualQueueDefinitionName": _name, "virtualQueueSettings": [
            {"key": "isTurnedOff", "value": "false", "description": "Whether the queue is turned off or not"}]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueDefinitionName', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            assert _content['virtualQueueDefinitionName'] == _name, 'vq definition not matching!'
            for virtualQueueSetting in _content['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                is_key_there_in_dict('key', virtualQueueSetting)
                is_key_there_in_dict('value', virtualQueueSetting)
                is_key_there_in_dict('description', virtualQueueSetting)
                assert virtualQueueSetting['key'] == 'isTurnedOff', 'key not matching!'
                assert virtualQueueSetting['value'] == 'false', 'value not matching!'
            test_data['virtualQueue'] = _content
        else:
            raise Exception('vq definition not added!')

    @pytestrail.case(30467787)
    def test_02_list_vq_definitions(self, config, rest_ship):
        """
        List vq definitions
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueuedefinitions")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for definition in _content:
                is_key_there_in_dict('virtualQueueDefinitionId', definition)
                is_key_there_in_dict('virtualQueueDefinitionName', definition)
                is_key_there_in_dict('virtualQueueSettings', definition)
                for virtualQueueSetting in definition['virtualQueueSettings']:
                    is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                    is_key_there_in_dict('key', virtualQueueSetting)
                    is_key_there_in_dict('value', virtualQueueSetting)
                    is_key_there_in_dict('virtualQueueDefinitionId', virtualQueueSetting)
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467788)
    def test_03_get_vq_definition(self, test_data, config, rest_ship):
        """
        Get vq definitions
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueDefinitionName', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            for virtualQueueSetting in _content['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                is_key_there_in_dict('key', virtualQueueSetting)
                is_key_there_in_dict('value', virtualQueueSetting)
                is_key_there_in_dict('description', virtualQueueSetting)
                is_key_there_in_dict('virtualQueueDefinitionId', virtualQueueSetting)
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467789)
    def test_04_update_vq_definition(self, config, guest_data, test_data, rest_ship):
        """
        Update vq definition
        :param guest_data:
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _name = f"{guest_data[0]['FirstName']} {guest_data[0]['LastName']} sample VQ for e2e"
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}")
        body = {"virtualQueueDefinitionName": _name, "virtualQueueSettings": [
            {"key": "isTurnedOff", "value": "false", "description": "Whether the queue is turned off or not"}]}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueDefinitionName', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            assert _content['virtualQueueDefinitionName'] == _name, 'vq definition not updated!'
            for virtualQueueSetting in _content['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                is_key_there_in_dict('key', virtualQueueSetting)
                is_key_there_in_dict('value', virtualQueueSetting)
                is_key_there_in_dict('description', virtualQueueSetting)
                is_key_there_in_dict('virtualQueueDefinitionId', virtualQueueSetting)
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467790)
    def test_05_get_vq_definition_setting(self, config, test_data, rest_ship):
        """
        Get vq definition setting
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/settings")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            if len(_content['virtualQueueSettings']) != 0:
                for virtualQueueSetting in _content['virtualQueueSettings']:
                    is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                    is_key_there_in_dict('key', virtualQueueSetting)
                    is_key_there_in_dict('value', virtualQueueSetting)
                    is_key_there_in_dict('description', virtualQueueSetting)
            else:
                raise Exception('No vq definition setting found!')
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467791)
    def test_06_add_vq_definition_setting(self, config, test_data, rest_ship):
        """
        Add vq definition setting
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/settings")
        body = [{"key": "turnOffLimit", "value": "10", "description": "What is the turned off limit for queue"}]
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/settings")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            _virtualQueueSetting = False
            for virtualQueueSetting in _content['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                is_key_there_in_dict('key', virtualQueueSetting)
                is_key_there_in_dict('value', virtualQueueSetting)
                is_key_there_in_dict('description', virtualQueueSetting)
                if virtualQueueSetting['key'] == 'turnOffLimit' and virtualQueueSetting['value'] == '10':
                    _virtualQueueSetting = True
            assert _virtualQueueSetting, 'vq definition setting not added successfully!'
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467792)
    def test_07_update_vq_definition_setting(self, config, test_data, rest_ship):
        """
        Update vq definition setting
        :param config:
        :param test_data:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/settings")
        body = [{"key": "isTurnedOff", "value": "true", "description": "Whether the queue is turned off or not"}]
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/settings")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            _virtualQueueSetting = False
            if len(_content['virtualQueueSettings']) != 0:
                for virtualQueueSetting in _content['virtualQueueSettings']:
                    is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                    is_key_there_in_dict('key', virtualQueueSetting)
                    is_key_there_in_dict('value', virtualQueueSetting)
                    is_key_there_in_dict('description', virtualQueueSetting)
                    if virtualQueueSetting['key'] == 'isTurnedOff' and virtualQueueSetting['value'] == 'true':
                        _virtualQueueSetting = True
                assert _virtualQueueSetting, 'vq definition setting not updated successfully!'
            else:
                raise Exception('No vq definition setting found!')
        else:
            raise Exception('No vq definition found!')

    @pytestrail.case(30467793)
    def test_08_list_vq_definitions_counts(self, config, rest_ship):
        """
        List vq definitions counts
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueuedefinitions/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for definition in _content:
                is_key_there_in_dict('notifiedCount', definition)
                is_key_there_in_dict('waitingCount', definition)
                is_key_there_in_dict('noShowCount', definition)
                is_key_there_in_dict('virtualQueueDefinitionId', definition)

    @pytestrail.case(30467794)
    def test_09_get_vq_definition_counts(self, test_data, config, rest_ship):
        """
        Get vq definition counts
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            test_data['virtualQueue']['counts'] = _content
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467795)
    def test_10_add_person(self, test_data, config, rest_ship, guest_data):
        """
        Add person
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "origin": "CA"}
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 1, 'Person not added successfully!'
            test_data['virtualQueue']['counts'] = _content
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467796)
    def test_11_search_person(self, test_data, config, rest_ship, guest_data):
        """
        Search person
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue/search?page=1&size=20")
        body = {"virtualQueueDefinitionId": _virtualQueueDefinitionId}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] > 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('virtualQueuePersons', _content['_embedded'])
            for virtualQueuePerson in _content['_embedded']['virtualQueuePersons']:
                is_key_there_in_dict('personId', virtualQueuePerson)
                is_key_there_in_dict('personTypeCode', virtualQueuePerson)
                is_key_there_in_dict('status', virtualQueuePerson)
                assert virtualQueuePerson['personId'] == _personId, 'Person data not matching!'
                assert virtualQueuePerson['status'] == 'W', 'Person is not in the waiting list!'
        else:
            raise Exception('No person found in vq!')

    @pytestrail.case(30467797)
    def test_12_notify_person(self, test_data, config, rest_ship, guest_data):
        """
        Notify person
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "status": "N"}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 0 and _content['notifiedCount'] == 1, 'Person not notified successfully!'
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467798)
    def test_13_verify_vq_after_notify(self, test_data, config, rest_ship, guest_data):
        """
        Verify VQ after Notify
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue/search?page=1&size=20")
        body = {"virtualQueueDefinitionId": _virtualQueueDefinitionId}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] > 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('virtualQueuePersons', _content['_embedded'])
            for virtualQueuePerson in _content['_embedded']['virtualQueuePersons']:
                is_key_there_in_dict('personId', virtualQueuePerson)
                is_key_there_in_dict('personTypeCode', virtualQueuePerson)
                is_key_there_in_dict('status', virtualQueuePerson)
                is_key_there_in_dict('notifiedCount', virtualQueuePerson)
                assert virtualQueuePerson['personId'] == _personId, 'Person data not matching!'
                assert virtualQueuePerson['status'] == 'N', 'person is not in the notified list!'
                assert virtualQueuePerson['notifiedCount'] > 0, 'person is not notified!'
        else:
            raise Exception('No person found in vq!')

    @pytestrail.case(30467799)
    def test_14_re_notify_person(self, test_data, config, rest_ship, guest_data):
        """
        Re_notify person
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "status": "N"}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 0 and _content['notifiedCount'] == 1, 'Person not notified successfully!'
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467800)
    def test_15_verify_vq_after_re_notify(self, test_data, config, rest_ship, guest_data):
        """
        Verify VQ after Re_Notify
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue/search?page=1&size=20")
        body = {"virtualQueueDefinitionId": _virtualQueueDefinitionId}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['page']['totalElements'] > 0:
            is_key_there_in_dict('_embedded', _content)
            is_key_there_in_dict('virtualQueuePersons', _content['_embedded'])
            for virtualQueuePerson in _content['_embedded']['virtualQueuePersons']:
                is_key_there_in_dict('personId', virtualQueuePerson)
                is_key_there_in_dict('personTypeCode', virtualQueuePerson)
                is_key_there_in_dict('status', virtualQueuePerson)
                is_key_there_in_dict('notifiedCount', virtualQueuePerson)
                assert virtualQueuePerson['personId'] == _personId, 'Person data not matching!'
                assert virtualQueuePerson['status'] == 'N', 'person is not in the notified list!'
                assert virtualQueuePerson['notifiedCount'] > 1, 'person is not re-notified!'
        else:
            raise Exception('No person found in vq!')

    @pytestrail.case(30467801)
    def test_16_mark_complete(self, test_data, config, rest_ship, guest_data):
        """
        Mark Complete
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "status": "C"}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 0 and _content['notifiedCount'] == 0, 'VQ is not marked completed!'
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467802)
    def test_17_verify_vq_after_mark_completed(self, test_data, config, rest_ship, guest_data):
        """
        Verify VQ after Mark Completed
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue/search?page=1&size=20")
        body = {"virtualQueueDefinitionId": _virtualQueueDefinitionId}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['page']['totalElements'] == 0, 'VQ has not been marked completed for that person!'

    @pytestrail.case(30467803)
    def test_18_remove_from_vq(self, test_data, config, rest_ship, guest_data):
        """
        Verify Remove from VQ
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[1]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "origin": "CA"}
        rest_ship.send_request(method="POST", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 1, 'Person not added successfully!'
            test_data['virtualQueue']['counts'] = _content
        else:
            raise Exception('No vq definition counts found!')
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue")
        body = {"personId": _personId, "personTypeCode": "RG",
                "virtualQueueDefinitionId": _virtualQueueDefinitionId, "status": "R"}
        rest_ship.send_request(method="PUT", url=url, json=body, auth="crew")
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('notifiedCount', _content)
            is_key_there_in_dict('waitingCount', _content)
            is_key_there_in_dict('noShowCount', _content)
            assert _content['waitingCount'] == 0, 'Person is not removed successfully!'
        else:
            raise Exception('No vq definition counts found!')

    @pytestrail.case(30467804)
    def test_19_verify_vq_after_mark_completed(self, test_data, config, rest_ship, guest_data):
        """
        Verify VQ after Mark Completed
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueue/search?page=1&size=20")
        body = {"virtualQueueDefinitionId": _virtualQueueDefinitionId}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        assert _content['page']['totalElements'] == 0, 'Person has not been removed from VQ!'

    @pytestrail.case(30467805)
    def test_20_delete_vq_definition(self, test_data, config, rest_ship):
        """
        Delete vq definition
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _virtualQueueDefinitionId = test_data['virtualQueue']['virtualQueueDefinitionId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'),
                      f"virtualqueuedefinitions/{_virtualQueueDefinitionId}")
        _content = rest_ship.send_request(method="DELETE", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('virtualQueueDefinitionId', _content)
            is_key_there_in_dict('virtualQueueDefinitionName', _content)
            is_key_there_in_dict('virtualQueueSettings', _content)
            for virtualQueueSetting in _content['virtualQueueSettings']:
                is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                is_key_there_in_dict('key', virtualQueueSetting)
                is_key_there_in_dict('value', virtualQueueSetting)
                is_key_there_in_dict('description', virtualQueueSetting)
                is_key_there_in_dict('virtualQueueDefinitionId', virtualQueueSetting)
        else:
            raise Exception('No vq definition found!')
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueuedefinitions")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for definition in _content:
                is_key_there_in_dict('virtualQueueDefinitionId', definition)
                is_key_there_in_dict('virtualQueueDefinitionName', definition)
                is_key_there_in_dict('virtualQueueSettings', definition)
                for virtualQueueSetting in definition['virtualQueueSettings']:
                    is_key_there_in_dict('virtualQueueSettingsId', virtualQueueSetting)
                    is_key_there_in_dict('key', virtualQueueSetting)
                    is_key_there_in_dict('value', virtualQueueSetting)
                    is_key_there_in_dict('virtualQueueDefinitionId', virtualQueueSetting)
                assert definition['virtualQueueDefinitionId'] != _virtualQueueDefinitionId, 'VQ has not been deleted!'
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcore'), "virtualqueuedefinitions/counts")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            for definition in _content:
                is_key_there_in_dict('notifiedCount', definition)
                is_key_there_in_dict('waitingCount', definition)
                is_key_there_in_dict('noShowCount', definition)
                is_key_there_in_dict('virtualQueueDefinitionId', definition)
                assert definition['virtualQueueDefinitionId'] != _virtualQueueDefinitionId, 'VQ has not been deleted!'

    @pytestrail.case(68357855)
    def test_21_get_user_details(self, test_data, config, rest_ship, guest_data):
        """
        Get User Details
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _personId = guest_data[0]['reservationGuestId']
        _name = f"{guest_data[0]['FirstName']} {guest_data[0]['LastName']} sample VQ for e2e"
        url = urljoin(getattr(config.ship.contPath, 'url.path.identityaccessmanagement'),"userprofiles/getuserdetails")
        body = {"personIds": [_personId]}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if len(_content) != 0:
            raise Exception('No User Found')

    @retry_when_fails(retries=3, interval=5)
    @pytestrail.case(68357856)
    def test_22_canned_messages(self, test_data, config, rest_ship, guest_data):
        """
        Get Canned messages
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        url = urljoin(getattr(config.ship.contPath, 'url.path.chatnotification'),"api/v1/crew/canned_message")
        _content = rest_ship.send_request(method="GET", url=url, auth="crew").content
        if len(_content) != 0:
            is_key_there_in_dict('predefined_messages', _content)
        else:
            raise Exception('no canned messages')

    @pytestrail.case(68357889)
    def test_23_view_profile(self, test_data, config, rest_ship, guest_data):
        """
        View Profile
        :param guest_data:
        :param test_data:
        :param config:
        :param rest_ship:
        :return:
        """
        _personId = guest_data[0]['reservationGuestId']
        url = urljoin(getattr(config.ship.contPath, 'url.path.dxpcorePublicURL'),"connections/search")
        body = {
            "personId": _personId, "personTypeCode": "RG", "isTravelWith": True,
             "isIncludeSameStateroomGuests": True}
        _content = rest_ship.send_request(method="POST", url=url, json=body, auth="crew").content
        if _content['_embedded']['connectionDetailsResponses'][0]["isTravelWith"]!=True:
            raise Exception("no results")
