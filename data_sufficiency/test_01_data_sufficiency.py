from virgin_utils import *

@pytest.mark.DataSufficiency
@pytest.mark.run(order=1)
class TestDataSufficiency:
    """
    Test suite to to check available activity.
    """

    @pytestrail.case(54150298)
    def test_01_verify_shore_activity(self, config, test_data, data_sufficiency, verification):
        """
        To check the shore side simple activity
        params: config
        params: test_data
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))

        query = verification.sql['activity_verification']['shore_ship_veri']
        rows = data_sufficiency.shore.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} shore-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"shore-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152687)
    def test_02_verify_ship_activiy(self, config, data_sufficiency, verification):
        """
        To check the ship side simple activity
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = query = verification.sql['activity_verification']['shore_ship_veri']
        rows = data_sufficiency.ship.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152688)
    def test_03_verify_spa_shore_activity(self, config, data_sufficiency, verification):
        """
        To check the availability of SPA activity shore side.
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['spa']
        rows = data_sufficiency.shore.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} shore-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"shore-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152689)
    def test_04_verify_spa_ship_activy(self, config, data_sufficiency, verification):
        """
        To check the activity of SPA activity ship side
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['spa']
        rows = data_sufficiency.ship.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152690)
    def test_05_verify_pa_shore_activy(self, config, data_sufficiency, verification):
        """
        To check the PA activity of shore side
        params: config
        params: data_sufficiency
        params: verification

        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['pa_ship_shore']
        rows = data_sufficiency.shore.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152691)
    def test_06_verify_pa_ship_activy(self, config, data_sufficiency, verification):
        """
        To check the PA activity of shore side
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['pa_ship_shore']
        rows = data_sufficiency.ship.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152692)
    def test_07_verify_entertainment_ship_activy(self, config, data_sufficiency, verification):
        """
        To check the entertainment activity of ship side
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['entertainment']
        rows = data_sufficiency.ship.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")

    @pytestrail.case(54152693)
    def test_08_verify_fitness_ship_activy(self, config, data_sufficiency, verification):
        """
        To check the fitness activity of ship side
        params: config
        params: data_sufficiency
        params: verification
        """
        maxDays = 10
        now = datetime.now(pytz.timezone('UTC'))
        query = verification.sql['activity_verification']['fitness']
        rows = data_sufficiency.ship.run_and_fetch_data(query)
        expectedDays = {(now + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, maxDays)}
        actualDays = {x['eventdate'].strftime("%Y-%m-%d") for x in rows}
        diffDays = sorted(expectedDays - actualDays)
        if len(diffDays) > 0:
            logger.error(f"{config.platform}-{config.env} ship-side arsActivityCode is missing data for"
                              f" following Dates: {', '.join(diffDays)}!!")
        else:
            logger.debug(f"ship-side arsActivityCode is Having data for all {', '.join(expectedDays)} Dates !!")





