__author__ = 'anshuman.goyal'

from decurtis.conftest import *
from decurtis.mxpdatabase import MxpDatabase
from virgin_utils import *
from decurtis.google import Storage


def pytest_addoption(parser):
    """
    Adds custom command line options for running the pytest harness
    All options will be stored in pytest config
    :param parser:
    :return:
    """
    parser.addoption("--appname", action="store", default='No', help="app name to be installed")
    parser.addoption("--module", action="store", default='No', help="module name ")
    parser.addoption("--ship", action="store", default=None, help="Ship URL")
    parser.addoption("--shore", action="store", default=None, help="Shore URL")
    parser.addoption("--test_data", action="store", default=None, help="Test Data Json")
    parser.addoption("--guests", action="store", default=2, type=int, help="No of guests")
    parser.addoption("--countries", action="store", default='US', help="Guest Countries (csv)")
    parser.addoption("--test-rail", action="store_true", default=False, help="Save Results in Test-Rails")
    parser.addoption("--embark-date", action="store", default=None, help="Embark Date (YYYY-MM-DD format)")
    parser.addoption("--debug-me", action="store_true", help="Debugging (Pick data from cache)")
    parser.addoption("--set-voyage", action="store", default=None, help="Voyage roll-over Date (YYYY-MM-DD)")
    parser.addoption("--test-performance", action="store_true", help="Test Performance")
    parser.addoption("--green-lane", action="store_true", help="Green Lane All Guests")

    # UI Specific Options
    parser.addoption("--ui-test-type", action="store", default=None, help="Type for UI test")
    parser.addoption("--bin-path", action="store", default=None, help="Binary APK/IPA Path")
    parser.addoption("--cmd-executor", action="store", default=None, help="command executor")
    parser.addoption("--device-name", action="store", default='DEVICE_01', help="Mobile device name")
    parser.addoption("--onboard-sailor", action="store", default='2', help="Required Onboard Guest")
    parser.addoption("--ashore-sailor", action="store", default='2', help="Required Ashore Guest")
    parser.addoption("--onboard-crew", action="store", default='2', help="Required Onboard Crew")
    parser.addoption("--ashore-crew", action="store", default='2', help="Required Ashore Crew")
    parser.addoption("--onboard-visitor", action="store", default='2', help="Required Onboard Visitor")
    parser.addoption("--ashore-visitor", action="store", default='2', help="Required Ashore Visitor")
    parser.addoption("--username", action="store", default='vertical-qa', help="Crew username")
    parser.addoption("--password", action="store", default='4BWm2tz4Xz', help="Crew Password")
    parser.addoption("--run-history", action="store_true", default=False, help="Configuration for run the History")

    # Virgin Specific Options
    parser.addoption("--add-extra", action="store_true", default=False, help="Add celebration")
    parser.addoption("--celebration-level", action="store", default=None, help="celebration level")
    parser.addoption("--vip-level", action="store", default=None, help="vip level")
    parser.addoption("--cancel-reservation", action="store_true", default=False, help="Cancel reservation")


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    """
    Here we skip the test-cases at the very beginning !!
    :param config:
    :param items:
    :return:
    """
    ship = config.getoption("--ship")
    shore = config.getoption("--shore")
    data = get_environment_data(ship, shore, nt=False)

    for item in items:
        class_markers = {x.name for x in item.parent.cls.pytestmark}
        if len(class_markers.intersection({'CABIN_CONTROL'})) > 0:
            item.add_marker(pytest.mark.xfail(reason='Skipping the vulnerable test cases'))

        # Skip Test Cases for Stage
        if data['envMasked'] == 'STAGE' and item.get_closest_marker('SkipForStageEnv'):
            item.add_marker(pytest.mark.skip('Skipping Stage Environment Tests'))

        if data['envMasked'] == 'CERT' and item.get_closest_marker('SkipForCertEnv'):
            item.add_marker(pytest.mark.skip('Skipping CERT Environment Tests'))

        if data['envMasked'] == 'INTEGRATION' and item.get_closest_marker('SkipForIntEnv'):
            item.add_marker(pytest.mark.skip('Skipping INT Environment Tests'))

    # Pull out test-case id's to be added in test-rails
    cases = list()
    for item in items:
        for own in item.own_markers:
            if own.name == 'pytestrail':
                if type(own.args[0]) == list:
                    cases.extend(x for x in own.args[0])
                else:
                    cases.extend([int(x) for x in own.args])
                break
        else:
            raise Exception(f'Test-Case {item.name} Cannot be without case-id')
    cases.sort()
    duplicates = [x for x in cases if cases.count(x) > 1]
    if len(duplicates) > 0:
        raise Exception(f"Duplicate Test-Cases ID's Found: {duplicates}")

    config.cache.set('cases', cases)


@pytest.fixture(scope="session", autouse=True)
def config(request):
    """
    Generate Test Data
    :param request:
    :return:
    """
    # Fetch Ship link and set it to lower if it is not None
    ship = request.config.getoption("--ship")
    if ship is not None:
        ship = str(request.config.getoption("--ship")).lower()

    # Fetch Shore link and set it to lower if it is not None
    shore = request.config.getoption("--shore")
    if shore is not None:
        shore = str(request.config.getoption("--shore")).lower()

    helms = HelmCreds(ship=ship, shore=shore).read_helms_data()

    # Using developer Auth OCI and MOCI's here, we will over-ride when it is DC Environment
    start_date = request.config.getoption("--embark-date")

    user_embark_date = request.config.getoption("--embark-date")
    voyage_roll_over_date = request.config.getoption("--set-voyage")

    if user_embark_date and user_embark_date != 'auto':
        try:
            user_embark_date = str(datetime.strptime(user_embark_date, "%Y-%m-%d").date())
        except Exception as exp:
            logger.error(exp)
            raise Exception(f"Wrong User Embark Date Format {user_embark_date}")

    '''
    structure = {
        'ship': {
            'db': {
                'host': db_details.ship.db.host, 'port': db_details.ship.db.port,
                'username': db_details.ship.db.username, 'password': db_details.ship.db.password
            },
            'kafka': {
                'brokers': db_details.ship.kafka.brokers, 'servers': db_details.ship.kafka.servers,
                'port': db_details.ship.kafka.port, 'prefix': db_details.ship.kafka.prefix
            },
            'couch': {
                'url': db_details.ship.couch.url, 'username': db_details.ship.couch.username,
                'password': db_details.ship.couch.password, 'bucket': db_details.ship.couch.bucket
            },
            'instance': None,
            'url': ship, 'sync': data.ship.sync, 'code': data.ship.code, 'contPath': dict(),
            'chat': re.sub(r'(https://)(.*?)(-.*)', r"\1chat\3", ship, re.I | re.M)
        },
        'shore': {
            'db': {
                'host': db_details.shore.db.host, 'port': db_details.shore.db.port,
                'username': db_details.shore.db.username, 'password': db_details.shore.db.password
            },
            'kafka': {
                'brokers': db_details.shore.kafka.brokers, 'servers': db_details.shore.kafka.servers,
                'port': db_details.shore.kafka.port, 'prefix': db_details.shore.kafka.prefix
            },
            'instance': None, 'url': shore, 'seaware': seaware, 'ota': ota, 'sync': data.shore.sync, 'contPath': dict()
        },
    }
    '''

    setattr(helms.ship, 'contPath', dict())
    setattr(helms.shore, 'contPath', dict())
    setattr(helms.ship, 'chat', re.sub(r'(https://)(.*?)(-.*)', r"\1chat\3", ship, re.I | re.M))

    setattr(helms, 'rollOverDate', voyage_roll_over_date)
    setattr(helms, 'startDate', start_date)
    setattr(helms, 'userEmbarkDate', user_embark_date)
    setattr(helms, 'greenLane', request.config.getoption("--green-lane"))
    setattr(helms, 'testPerformance', request.config.getoption("--test-performance"))
    setattr(helms, 'cancel', request.config.getoption("--cancel-reservation"))
    setattr(helms, 'extra', request.config.getoption("--add-extra"))
    setattr(helms, 'celebrationLevel', request.config.getoption("--celebration-level"))
    setattr(helms, 'vipLevel', request.config.getoption("--vip-level"))
    if request.config.getoption("--ui-test-type") is not None:
        setattr(helms, 'isUiTest', True)

    logger.debug(f"Configs => {helms}")
    return helms


@pytest.fixture(scope="session", autouse=True)
def guest_data(request, config, test_data, data_init):
    """
    Fixture to generate guest data
    :param request:
    :param config:
    :param test_data:
    :param data_init:
    :return:
    :rtype:
    """
    guest_count = test_data['guests']
    all_guest_details = []
    gender_codes = ['Male', 'Female']
    unique_names = []
    for count in range(guest_count):
        if len(test_data['countries']) > 1:
            country = random.choice(test_data['countries'])
        else:
            country = test_data['countries'][0]
        first_name = generate_first_name()
        last_name = generate_last_name()
        name = f"{first_name} {last_name}"

        # Make sure we have a unique name for all guests in one single reservation
        while name in unique_names:
            first_name = generate_first_name()
            last_name = generate_last_name()
            name = f"{first_name} {last_name}"
            continue
        unique_names.append(name)
        email_id = generate_email_id(from_saved=True, first_name=first_name, last_name=last_name)
        if os.environ.get('JOB_NAME', None) == 'data-generation-vv-stage-client':
            email_id = email_id.replace('@mailinator', '@yopmail')
        # We make sure the One Adult, One Child and One Minor
        if count in [0, 1]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        elif count == 3:  # 4th Guest as always Minor
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        else:  # 3rd and other guests are randomly chose between adult and child
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        if count in [0, 4]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        data = {
            "FirstName": first_name, "LastName": last_name,
            "GenderCode": random.choice(gender_codes), "BirthDate": birth_date,
            "CitizenshipCountryCode": country, "Email": email_id,
            "Phones": [{
                "number": str(generate_phone_number(max_digits=10)), "phoneTypeCode": "Home"
            }],
            "Addresses": [{
                "lineOne": "221b Baker Street", "lineTwo": "wallaby way",
                "city": "Miami", "stateCode": "FL", "countryCode": "US",
                "zipCode": "33012"
            }]
        }
        all_guest_details.append(data)

    # Use init Data, if Cache is not cleared !!
    if request.config.getoption('--debug-me'):
        guest_data_file = 'guest_data.json'
        if os.path.isfile(guest_data_file):
            print(f"WARNING :: USING CACHED DATA FROM {guest_data_file} !!")
            with open(guest_data_file, 'r') as _fp:
                all_guest_details = json.load(_fp)
        else:
            print(f"Cache file {guest_data_file} missing !! Cannot Debug !!")
    return all_guest_details


@pytest.fixture(scope="session", autouse=True)
def v_guest_data(request, config, test_data, data_init):
    """
    Fixture to generate guest data for visa test
    :param request:
    :param config:
    :param test_data:
    :param data_init:
    :return:
    :rtype:
    """
    guest_count = test_data['guests']
    visa_guest_details = []
    gender_codes = ['Male', 'Female']
    unique_names = []
    for count in range(guest_count):
        if len(test_data['countries']) > 1:
            country = 'IN'
        else:
            country = 'IN'
        first_name = generate_first_name()
        last_name = generate_last_name()
        name = f"{first_name} {last_name}"

        # Make sure we have a unique name for all guests in one single reservation
        while name in unique_names:
            first_name = generate_first_name()
            last_name = generate_last_name()
            name = f"{first_name} {last_name}"
            continue
        unique_names.append(name)
        email_id = generate_email_id(from_saved=True, first_name=first_name, last_name=last_name)
        if os.environ.get('JOB_NAME', None) == 'data-generation-vv-stage-client':
            email_id = email_id.replace('@mailinator', '@yopmail')
        # We make sure the One Adult, One Child and One Minor
        if count in [0, 1]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        elif count == 3:  # 4th Guest as always Minor
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        else:  # 3rd and other guests are randomly chose between adult and child
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        if count in [0, 4]:  # 1st 2 guests always adults
            birth_date = generate_birth_date(member='adult').strftime('%Y-%m-%d')
        data = {
            "FirstName": first_name, "LastName": last_name,
            "GenderCode": random.choice(gender_codes), "BirthDate": birth_date,
            "CitizenshipCountryCode": country, "Email": email_id,
            "Phones": [{
                "number": str(generate_phone_number(max_digits=10)), "phoneTypeCode": "Home"
            }],
            "Addresses": [{
                "lineOne": "221b Baker Street", "lineTwo": "wallaby way",
                "city": "Miami", "stateCode": "FL", "countryCode": "US",
                "zipCode": "33012"
            }]
        }
        visa_guest_details.append(data)

    # Use init Data, if Cache is not cleared !!
    if request.config.getoption('--debug-me'):
        guest_data_file = 'visa_guest_data.json'
        if os.path.isfile(guest_data_file):
            print(f"WARNING :: USING CACHED DATA FROM {guest_data_file} !!")
            with open(guest_data_file, 'r') as _fp:
                visa_guest_details = json.load(_fp)
        else:
            print(f"Cache file {guest_data_file} missing !! Cannot Debug !!")
    return visa_guest_details


@pytest.fixture(scope='session')
def web_driver(request, config):
    """
    Fixture to initialise the web driver
    :param request:
    :param config:
    :return:
    """
    binPath = request.config.getoption("--bin-path")
    browser = request.config.getoption("--ui-test-type")
    app_activity = "com.decurtis.dxp.shared.splash.ui.SplashActivity"
    app_package = None

    if binPath:
        if 'https://' in binPath or not os.path.isfile(binPath):
            # When https:// in binPath or the given path does not exist, we download file from GCS
            prefix = str(binPath).replace('https://storage.cloud.google.com/', '')
            bucket_name = prefix.split("/")[0]
            prefix = prefix.replace(f"{bucket_name}/", "")
            s = Storage()
            s.download_file(bucket_name=bucket_name, cwd="/tmp", prefix=prefix)
            executor = request.config.getoption("--cmd-executor")
            remote = re.search(r"http://(.*?):", executor, re.I | re.M).group(1)
            cmd = "scp -o StrictHostKeyChecking=no /tmp/" + prefix.split('/')[-1] + " buildadmin@" + remote + ":/tmp/"
            status = s.run_cmd(cmd=cmd, cwd='/tmp')

        if 'aci-' in binPath:
            if config.envMasked == 'LATEST':
                app_package = f"com.decurtis.dxp.aci.dclnp"
            else:
                app_package = f"com.decurtis.dxp.aci"
        elif 'gangway-' in binPath:
            app_package = f"com.decurtis.dxp.gangway"
        elif 'crew' in binPath:
            app_package = f"com.decurtis.crew.embark"
            app_activity = "com.zoontek.rnbootsplash.RNBootSplashActivity"
        elif 'sailor' in binPath:
            app_package = 'com.virginvoyages.guest.integration'
            app_activity = 'com.virginvoyages.guest.integration.MainActivity'
        else:
            raise Exception(f'--bin-path does not point to any app_package/app_activity !!')

    driver = WebDriver(
        browser=browser,
        command_executor=request.config.getoption("--cmd-executor"),
        device_name=request.config.getoption("--device-name"),
        # Mobile apps related params
        bin_path=binPath, app_package=app_package, app_activity=app_activity
    )

    yield driver
    try:
        driver.driver.quit()
    except (Exception, ValueError):
        pass


@pytest.fixture(scope='session')
def page():
    """
    Fixture to initialise the Page Class
    :return:
    """
    named_tuple = namedtuple("page", ["page"])
    return named_tuple


@pytest.fixture(scope="session")
def db_mxp(config):
    """
    Connect to MXP Database
    :param config:
    :return:
    """
    logger.debug(f"Connecting to MXP Database")
    named_tuple = namedtuple("database", ["ship"])
    details = f"{config.ship.mxp_db.host} {config.ship.mxp_db.port} {config.ship.mxp_db.username} {config.ship.mxp_db.password}"
    logger.debug(details)
    try:
        ship = MxpDatabase(
            host=config.ship.mxp_db.host,
            username=config.ship.mxp_db.username,
            password=config.ship.mxp_db.password,
            database="MXP_INT",
            port=config.ship.mxp_db.port,
            odbc_version=17
        )
    except Exception as exp:
        logger.error(exp)
        raise Exception(f"Unable to connect to MXP DB {config.ship.mxp_db.host, config.ship.mxp_db.port}")
    return named_tuple(ship=ship)


@pytest.fixture(scope="session")
def data_sufficiency(config):
    """
    Connect to ars Database
    :param config:
    :return:
    """
    logger.debug(f"Connecting to ars Core Database")
    named_tuple = namedtuple("database", ["ship", "shore"])

    details = f"{config.ship.db.host} {config.ship.db.port} {config.ship.db.username} {config.ship.db.password}"
    logger.debug(details)
    try:
        ship = Database(
            host=config.ship.db.host,
            username=config.ship.db.username,
            password=config.ship.db.password,
            database="ars",
            port=config.ship.db.port,
        )
    except Exception as exp:
        logger.error(exp)
        raise Exception(f"Unable to connect to Ship DB {config.ship.db.host, config.ship.db.port}")

    details = f"{config.shore.db.host} {config.shore.db.port} {config.shore.db.username} {config.shore.db.password}"
    logger.debug(details)
    try:
        shore = Database(
            host=config.shore.db.host,
            username=config.shore.db.username,
            password=config.shore.db.password,
            database="ars",
            port=config.shore.db.port,
        )
    except Exception as exp:
        logger.error(exp)
        raise Exception(f"Unable to connect to Shore DB {config.shore.db.host, config.shore.db.port}")

    return named_tuple(ship=ship, shore=shore)
