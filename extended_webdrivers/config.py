import json
import os
import shutil
import time

from selenium import webdriver

from . import LOGGER
from .android import Android
from .chrome import Chrome
from .edge import Edge
from .extended_webdriver import ExtendedWebdriver
from .firefox import Firefox
from .ie import Ie
from .opera import Opera
from .phantomjs import PhantomJS
from .remote import Remote

DEFAULT_CONFIG = 'webdrivers-default.json'
MOBILE_CONFIG = 'webdrivers-mobile.json'
HEADLESS_CONFIG = 'webdrivers-headless.json'

NoneType = type(None)


class InvalidWebdriver(Exception):
    pass


def create_driver_config(name: str):
    """
    Creates a new webdriver configuration file based off the default.

    Parameters
    ----------
    name - The name of the new configuration file.
    """
    if not name.endswith('.json'):
        name += '.json'
    shutil.copy(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     DEFAULT_CONFIG), os.path.join(os.getcwd(), name))


def load_driver_from_config(name: str, config_name: str = DEFAULT_CONFIG
                            ) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a config file.

    Parameters
    ----------
    name - The name of the webdriver to load.
    config_name - The name of the config file to load. This first searches for
                  default config files in the extended_webdrivers package. If
                  it can't find any, it then searches the current directory.
    """
    if not config_name.endswith('.json'):
        config_name += '.json'
    if not os.path.exists(config_name):
        config_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   config_name)
    if not os.path.exists(config_name):
        raise FileNotFoundError('Config file not found.')
    with open(config_name, 'r') as config_file:
        LOGGER.info(f'Loading webdriver settings from {config_file.name}.')
        data = json.load(config_file)
        return load_driver(name, data)


def load_driver_from_json(name: str, data: str) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a json string.

    Parameters
    ----------
    name - The name of the webdriver to load.
    data - The raw json string.
    """
    data = json.loads(data)
    return load_driver(name, data)


def load_driver(name: str, data: dict) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a dictionary.

    Parameters
    ----------
    webdriver - The name of the webdriver to load.
    data - The raw json string.
    """
    name = name.lower()
    start_time = time.time()
    if name == 'remote':
        """
        def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None):
        """

        command_executor = 'http://127.0.0.1:4444/wd/hub'
        desired_capabilities = None
        browser_profile = None
        proxy = None
        keep_alive = False
        file_detector = None
        options = None

        if 'remote' in data and isinstance(data['remote'], dict):
            if 'command_executor' in data['remote'] and isinstance(
                    data['remote']['command_executor'], (NoneType, str)):
                command_executor = data['remote']['command_executor']

            if 'desired_capabilities' in data['remote'] and isinstance(
                    data['remote']['desired_capabilities'], dict):
                desired_capabilities = data['remote']['desired_capabilities']

            if 'browser_profile' in data['remote'] and isinstance(
                    data['remote']['browser_profile'], str):
                browser_profile = webdriver.FirefoxProfile(
                    data['remote']['browser_profile'])

            if 'keep_alive' in data['remote'] and isinstance(
                    data['remote']['keep_alive'], (bool, int)):
                keep_alive = bool(data['remote']['keep_alive'])

            #if 'file_detector' in data['remote']:
            #    file_detector = webdriver.remote.file_detector.FileDetector()

            #if 'options' in data['remote']:
            #    options = data['remote']['options'])
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Remote(
            command_executor={command_executor},
            desired_capabilities={desired_capabilities},
            browser_profile={browser_profile},
            proxy={proxy},
            keep_alive={keep_alive}
            file_detector={file_detector},
            options={options})''')

        webdriver_ = Remote(command_executor=command_executor,
                            desired_capabilities=desired_capabilities,
                            browser_profile=browser_profile,
                            proxy=proxy,
                            keep_alive=keep_alive,
                            file_detector=file_detector,
                            options=options)
    elif name == 'chrome':
        """
        def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):
        """

        executable_path = 'chromedriver'
        port = 0
        service_args = None
        desired_capabilities = None
        service_log_path = None
        keep_alive = True
        options = None

        if 'chrome' in data and isinstance(data['chrome'], dict):
            if 'executable_path' in data['chrome'] and isinstance(
                    data['chrome']['executable_path'], (NoneType, str)):
                executable_path = data['chrome']['executable_path']

            if 'port' in data['chrome'] and isinstance(data['chrome']['port'],
                                                       (int, float, str)):
                port = int(data['chrome']['port'])

            if 'service_args' in data['chrome'] and isinstance(
                    data['chrome']['service_args'], (list, tuple)):
                service_args = data['chrome']['service_args']

            if 'desired_capabilities' in data['chrome'] and isinstance(
                    data['chrome']['desired_capabilities'], dict):
                desired_capabilities = data['chrome']['desired_capabilities']

            if 'service_log_path' in data['chrome'] and isinstance(
                    data['chrome']['service_log_path'], (NoneType, str)):
                service_log_path = data['chrome']['service_log_path']

            if 'keep_alive' in data['chrome'] and isinstance(
                    data['chrome']['keep_alive'], (bool, int)):
                keep_alive = bool(data['chrome']['keep_alive'])

            if 'options' in data['chrome']:
                options = webdriver.ChromeOptions()
                if 'arguments' in data['chrome']['options'] and isinstance(
                        data['chrome']['options']['arguments'], list):
                    for argument in data['chrome']['options']['arguments']:
                        options.add_argument(argument)
                if 'experimental_options' in data['chrome'][
                        'options'] and isinstance(
                            data['chrome']['options']['experimental_options'],
                            dict):
                    for experimental_option in data['chrome']['options'][
                            'experimental_options']:
                        options.add_experimental_option(
                            experimental_option, data['chrome']['options']
                            ['experimental_options'][experimental_option])
                if 'capabilities' in data['chrome']['options'] and isinstance(
                        data['chrome']['options']['capabilities'], dict):
                    for k, v in data['chrome']['options'][
                            'capabilities'].items():
                        options.set_capability(k, v)
                if 'binary_location' in data['chrome'][
                        'options'] and isinstance(
                            data['chrome']['options']['binary_location'],
                            (NoneType, str)):
                    options.binary_location = data['chrome']['options'][
                        'binary_location']
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Chrome(
executable_path={executable_path},
port={port},
options={options},
service_args={service_args},
desired_capabilities={desired_capabilities},
service_log_path={service_log_path},
chrome_options=None,
keep_alive={keep_alive})''')

        webdriver_ = Chrome(
            executable_path=executable_path,
            port=port,
            options=options,
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            service_log_path=service_log_path,
            chrome_options=None,  # Deprecated
            keep_alive=keep_alive)
    elif name == 'firefox':
        """
        def __init__(self, firefox_profile=None, firefox_binary=None,
                 timeout=30, capabilities=None, proxy=None,
                 executable_path="geckodriver", options=None,
                 service_log_path="geckodriver.log", firefox_options=None,
                 service_args=None, desired_capabilities=None, log_path=None,
                 keep_alive=True):
        """

        firefox_profile = None
        firefox_binary = None
        timeout = 30
        capabilities = None
        proxy = None
        executable_path = 'geckodriver'
        options = None
        service_log_path = "geckodriver.log"
        #firefox_options = None
        service_args = None
        desired_capabilities = None
        log_path = None
        keep_alive = True

        if 'firefox' in data and isinstance(data['firefox'], dict):
            if 'firefox_profile' in data['firefox']:
                firefox_profile = webdriver.FirefoxProfile()
                if 'preferences' in data['firefox'][
                        'firefox_profile'] and isinstance(
                            data['firefox']['firefox_profile']['preferences'],
                            dict):
                    for k, v in data['firefox']['firefox_profile'][
                            'preferences'].items():
                        firefox_profile.set_preference(k, v)

            if 'firefox_binary' in data['firefox'] and isinstance(
                    data['firefox']['firefox_binary'], (NoneType, str)):
                firefox_binary = data['firefox']['firefox_binary']

            if 'timeout' in data['firefox'] and isinstance(
                    data['firefox']['timeout'], (int, float, str)):
                timeout = int(data['firefox']['timeout'])

            #if 'capabilities' in data['firefox']:
            #    capabilities = data['firefox']['capabilities']

            #if 'proxy' in data['firefox']:
            #    proxy = data['firefox']['proxy']

            #if 'proxy' in data['firefox']:
            #    proxy = data['firefox']['proxy']

            if 'executable_path' in data['firefox'] and isinstance(
                    data['firefox']['executable_path'], (NoneType, str)):
                executable_path = int(data['firefox']['executable_path'])

            if 'options' in data['firefox'] and isinstance(
                    data['firefox']['options'], 'dict'):
                options = webdriver.FirefoxOptions()
                if 'arguments' in data['firefox']['options'] and isinstance(
                        data['firefox']['options']['arguments'],
                    (list, tuple)):
                    for argument in data['firefox']['options']['arguments']:
                        options.add_argument(argument)

            if 'service_log_path' in data['firefox'] and isinstance(
                    data['firefox']['service_log_path'], (NoneType, str)):
                service_log_path = data['firefox']['service_log_path']

            if 'service_args' in data['firefox'] and isinstance(
                    data['firefox']['service_args'], (list, tuple)):
                service_args = data['firefox']['service_args']

            if 'desired_capabilities' in data['firefox'] and isinstance(
                    data['firefox']['desired_capabilities'], dict):
                desired_capabilities = data['firefox']['desired_capabilities']

            if 'log_path' in data['firefox'] and isinstance(
                    data['firefox']['log_path'], (NoneType, str)):
                log_path = data['firefox']['log_path']
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Firefox(
firefox_profile={firefox_profile},
firefox_binary={firefox_binary},
timeout={timeout},
capabilities={capabilities},
proxy={proxy},
executable_path={executable_path},
options={options},
service_log_path={service_log_path},
firefox_options=None,  # Deprecated
service_args={service_args},
desired_capabilities={desired_capabilities},
log_path={log_path}''')

        webdriver_ = Firefox(
            firefox_profile=firefox_profile,
            firefox_binary=firefox_binary,
            timeout=timeout,
            capabilities=capabilities,
            proxy=proxy,
            executable_path=executable_path,
            options=options,
            service_log_path=service_log_path,
            firefox_options=None,  # Deprecated
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            log_path=log_path)
    elif name == 'edge':
        """
        def __init__(self, executable_path='MicrosoftWebDriver.exe',
                 capabilities=None, port=0, verbose=False, service_log_path=None,
                 log_path=None, keep_alive=False):
        """

        executable_path = 'MicrosoftWebDriver.exe'
        capabilities = None
        port = 0
        verbose = False
        service_log_path = None
        log_path = None
        keep_alive = False

        if 'edge' in data and isinstance(data['edge'], dict):
            if 'executable_path' in data['edge'] and isinstance(
                    data['edge']['executable_path'], (NoneType, str)):
                executable_path = data['edge']['executable_path']

            if 'capabilities' in data['edge'] and isinstance(
                    data['edge']['capabilities'], (NoneType, dict)):
                capabilities = data['edge']['capabilities']

            if 'port' in data['edge'] and isinstance(data['edge']['port'],
                                                     (int, float, str)):
                port = int(data['edge']['port'])

            if 'verbose' in data['edge'] and isinstance(
                    data['edge']['verbose'], (bool, int)):
                verbose = bool(data['edge']['verbose'])

            if 'service_log_path' in data['edge'] and isinstance(
                    data['edge']['service_log_path'], (NoneType, str)):
                service_log_path = data['edge']['service_log_path']

            if 'log_path' in data['edge'] and isinstance(
                    data['edge']['log_path'], (NoneType, str)):
                log_path = data['edge']['log_path']

            if 'keep_alive' in data['edge'] and isinstance(
                    data['edge']['keep_alive'], (bool, int)):
                keep_alive = bool(data['edge']['keep_alive'])
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Edge(executable_path=executable_path,
capabilities={capabilities},
port={port},
verbose={verbose},
service_log_path={service_log_path},
log_path={log_path},
keep_alive={keep_alive})''')

        webdriver_ = Edge(executable_path=executable_path,
                          capabilities=capabilities,
                          port=port,
                          verbose=verbose,
                          service_log_path=service_log_path,
                          log_path=log_path,
                          keep_alive=keep_alive)
    elif name == 'android':
        """
        def __init__(self, host="localhost", port=4444, desired_capabilities=DesiredCapabilities.ANDROID):
        """

        host = 'localhost'
        port = 4444
        desired_capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.ANDROID

        if 'android' in data and isinstance(data['android'], dict):
            if 'host' in data['android'] and isinstance(
                    data['android']['host'], (NoneType, str)):
                host = data['android']['host']

            if 'port' in data['android'] and isinstance(
                    data['android']['port'], (int, float, str)):
                port = int(data['android']['port'])

            if 'desired_capabilities' in data['android'] and isinstance(
                    data['android']['desired_capabilities'], (NoneType, dict)):
                desired_capabilities = data['android']['desired_capabilities']
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''
        Android(
host={host},
port={port},
desired_capabilities={desired_capabilities})''')

        webdriver_ = Android(host=host,
                             port=port,
                             desired_capabilities=desired_capabilities)
    elif name == 'ie' or name == 'iexplore':
        """
        def __init__(self, executable_path='IEDriverServer.exe', capabilities=None,
                 port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT, host=DEFAULT_HOST,
                 log_level=DEFAULT_LOG_LEVEL, service_log_path=DEFAULT_SERVICE_LOG_PATH, options=None,
                 ie_options=None, desired_capabilities=None, log_file=None, keep_alive=False):
        """

        restricted_mode = False
        executable_path = 'IEDriverServer.exe'
        capabilities = None,
        port = webdriver.ie.webdriver.DEFAULT_PORT
        timeout = webdriver.ie.webdriver.DEFAULT_TIMEOUT
        host = webdriver.ie.webdriver.DEFAULT_HOST,
        log_level = webdriver.ie.webdriver.DEFAULT_LOG_LEVEL
        service_log_path = webdriver.ie.webdriver.DEFAULT_SERVICE_LOG_PATH
        options = None,
        #ie_options = None
        desired_capabilities = None
        log_file = None
        keep_alive = False

        if 'ie' in data and isinstance(data['ie'], dict):
            if 'restricted_mode' in data['ie'] and isinstance(
                    data['ie']['restricted_mode'], (bool, int)):
                restricted_mode = bool(data['ie']['restricted_mode'])

            if 'executable_path' in data['ie'] and isinstance(
                    data['ie']['executable_path'], (NoneType, str)):
                service_log_path = data['ie']['executable_path']

            if 'capabilities' in data['ie'] and isinstance(
                    data['ie']['capabilities'], (NoneType, dict)):
                capabilities = data['ie']['capabilities']

            if 'port' in data['ie'] and isinstance(data['ie']['port'],
                                                   (int, float, str)):
                port = int(data['ie']['port'])

            if 'timeout' in data['ie'] and isinstance(data['ie']['timeout'],
                                                      (int, float, str)):
                timeout = int(data['ie']['timeout'])

            if 'host' in data['ie'] and isinstance(data['ie']['host'],
                                                   (NoneType, str)):
                host = data['ie']['host']

            if 'log_level' in data['ie'] and isinstance(
                    data['ie']['log_level'], (NoneType, str)):
                log_level = data['ie']['log_level']

            if 'service_log_path' in data['ie'] and isinstance(
                    data['ie']['service_log_path'], (NoneType, str)):
                service_log_path = data['ie']['service_log_path']

            if 'options' in data['ie'] and isinstance(data['ie']['options'],
                                                      dict):
                options = webdriver.IeOptions()
                if 'capabilities' in data['ie']['options'] and isinstance(
                        data['ie']['options']['capabilities'], dict):
                    for k, v in data['ie']['options']['capabilities'].items():
                        options.set_capability(k, v)
                if 'additional_options' in data['ie']['options'] and isinstance(
                        data['ie']['options']['additional_options'], dict):
                    for k, v in data['ie']['options'][
                            'additional_options'].items():
                        options.add_additional_option(k, v)

            if 'desired_capabilities' in data['ie'] and isinstance(
                    data['ie']['desired_capabilities'], (NoneType, dict)):
                desired_capabilities = data['ie']['desired_capabilities']

            if 'log_file' in data['ie'] and isinstance(data['ie']['log_file'],
                                                       (NoneType, str)):
                log_file = data['ie']['log_file']

            if 'keep_alive' in data['ie'] and isinstance(
                    data['ie']['keep_alive'], (bool, int)):
                keep_alive = bool(data['ie']['keep_alive'])
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Ie(
restricted_mode={restricted_mode},
executable_path={executable_path},
capabilities={capabilities},
port={port},
timeout={timeout},
host={host},
log_level={log_level},
service_log_path={service_log_path},
options={options},
ie_options=None, # Deprecated
desired_capabilities={desired_capabilities},
log_file={log_file},
keep_alive={keep_alive})''')

        webdriver_ = Ie(
            restricted_mode=restricted_mode,
            executable_path=executable_path,
            capabilities=capabilities,
            port=port,
            timeout=timeout,
            host=host,
            log_level=log_level,
            service_log_path=service_log_path,
            options=options,
            ie_options=None,  # Deprecated
            desired_capabilities=desired_capabilities,
            log_file=log_file,
            keep_alive=keep_alive)
    elif name == 'opera':
        """
        def __init__(self, executable_path=None, port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 opera_options=None, keep_alive=True):
        """

        executable_path = None
        port = 0
        options = None
        service_args = None
        desired_capabilities = None
        service_log_path = None
        #opera_options = None
        keep_alive = True

        if 'opera' in data and isinstance(data['opera'], dict):
            if 'executable_path' in data['opera'] and isinstance(
                    data['opera']['executable_path'], (NoneType, str)):
                executable_path = data['opera']['executable_path']

            if 'port' in data['opera'] and isinstance(data['opera']['port'],
                                                      (int, float, str)):
                port = int(data['opera']['port'])

            if 'options' in data['opera']:
                options = webdriver.ChromeOptions()
                if 'arguments' in data['opera']['options'] and isinstance(
                        data['opera']['options']['arguments'], list):
                    for argument in data['opera']['options']['arguments']:
                        options.add_argument(argument)
                if 'experimental_options' in data['opera'][
                        'options'] and isinstance(
                            data['opera']['options']['experimental_options'],
                            dict):
                    for experimental_option in data['opera']['options'][
                            'experimental_options']:
                        options.add_experimental_option(
                            experimental_option, data['opera']['options']
                            ['experimental_options'][experimental_option])
                if 'capabilities' in data['opera']['options'] and isinstance(
                        data['opera']['options']['capabilities'], dict):
                    for k, v in data['opera']['options']['capabilities'].keys(
                    ):
                        options.set_capability(k, v)
                if 'binary_location' in data['opera']['options'] and isinstance(
                        data['opera']['options']['binary_location'],
                    (NoneType, str)):
                    options.binary_location = data['opera']['options'][
                        'binary_location']

            if 'service_args' in data['opera'] and isinstance(
                    data['opera']['service_args'], (list, tuple)):
                service_args = data['opera']['service_args']

            if 'desired_capabilities' in data['opera'] and isinstance(
                    data['opera']['desired_capabilities'], dict):
                desired_capabilities = data['opera']['desired_capabilities']

            if 'service_log_path' in data['opera'] and isinstance(
                    data['opera']['service_log_path'], (NoneType, str)):
                service_log_path = data['opera']['service_log_path']

            if 'keep_alive' in data['opera'] and isinstance(
                    data['opera']['keep_alive'], (bool, int)):
                keep_alive = bool(data['opera']['keep_alive'])
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''Opera(executable_path={executable_path},
port={port},
options={options},
service_args={service_args},
desired_capabilities={desired_capabilities},
service_log_path={service_log_path},
opera_options=None,  # Deprecated
keep_alive={keep_alive})''')

        webdriver_ = Opera(
            executable_path=executable_path,
            port=port,
            options=options,
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            service_log_path=service_log_path,
            opera_options=None,  # Deprecated
            keep_alive=keep_alive)
    elif name == 'phantomjs':
        """
        def __init__(self, executable_path="phantomjs",
                 port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                 service_args=None, service_log_path=None):
        """

        executable_path = "phantomjs"
        port = 0
        desired_capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.PHANTOMJS
        service_args = None
        service_log_path = None

        if 'phantomjs' in data and isinstance(data['phantomjs'], dict):
            if 'executable_path' in data['phantomjs'] and isinstance(
                    data['phantomjs']['executable_path'], (NoneType, str)):
                executable_path = data['phantomjs']['executable_path']

            if 'port' in data['phantomjs'] and isinstance(
                    data['phantomjs']['port'], (int, float, str)):
                port = int(data['phantomjs']['port'])

            if 'desired_capabilities' in data['phantomjs'] and isinstance(
                    data['phantomjs']['desired_capabilities'], dict):
                desired_capabilities = data['phantomjs'][
                    'desired_capabilities']

            if 'service_args' in data['phantomjs'] and isinstance(
                    data['phantomjs']['service_args'], (list, tuple)):
                service_args = data['phantomjs']['service_args']

            if 'service_log_path' in data['phantomjs'] and isinstance(
                    data['phantomjs']['service_log_path'], (NoneType, str)):
                service_log_path = data['phantomjs']['service_log_path']
        else:
            LOGGER.info(
                f'No settings found for webdriver {name}. Loading defaults.')

        LOGGER.info(f'''
webdriver_ = PhantomJS(
executable_path={executable_path},
port={port},
desired_capabilities={desired_capabilities},
service_args={service_args},
service_log_path={service_log_path})
''')

        webdriver_ = PhantomJS(executable_path=executable_path,
                               port=port,
                               desired_capabilities=desired_capabilities,
                               service_args=service_args,
                               service_log_path=service_log_path)
    else:
        raise InvalidWebdriver(f'{name} is an invalid webdriver.')

    if name in data and isinstance(data[name], dict):
        if 'size' in data[name]:
            set_window_size = False
            x = 1920
            y = 1080

            if isinstance(data[name]['size'],
                          (list, tuple)) and len(data[name]['size']) == 2:
                set_window_size = True
                x, y = data[name]['size']
            elif isinstance(data[name]['size'], dict):
                x = data[name]['size']['x']
                y = data[name]['size']['y']

            if isinstance(webdriver_, Chrome) and isinstance(
                    data['chrome']['options']['arguments'], list) and (
                        any('--window-size' in x
                            for x in data['chrome']['options']['arguments']) or
                        any('--start-maximized' in x
                            for x in data['chrome']['options']['arguments'])):
                set_window_size = False

            if set_window_size:
                LOGGER.info(f'Setting webdriver window size to {x}x{y}')
                webdriver_.set_window_size(x, y)

        if 'full_screen' in data[name] and data[name] == True:
            set_full_screen = True
            try:
                if isinstance(webdriver_, Chrome) and isinstance(
                        data['chrome']['options']['arguments'],
                        list) and '--start-maximized' in data['chrome'][
                            'options']['arguments']:
                    set_full_screen = False
            except:
                pass

            if set_full_screen:
                LOGGER.info('Setting webdriver to full screen.')
                webdriver_.maximize_window()

        if 'implicitly_wait' in data[name] and isinstance(
                data[name]['implicitly_wait'],
            (int, float, str)) and int(data[name]['implicitly_wait']) > 0:
            LOGGER.info(
                f'Setting webdriver implicit wait time to {data[name]["implicitly_wait"]}.'
            )
            webdriver_.implicitly_wait(int(data[name]['implicitly_wait']))

        if 'coordinates' in data[name]:
            latitude = None
            longitude = None
            if isinstance(data[name]['coordinates'], (list, tuple)) and len(
                    data[name]['coordinates']) == 2:
                latitude, longitude = data[name]['coordinates']
            elif isinstance(data[name]['coordinates'], dict):
                latitude = data[name]['coordinates']['latitude']
                longitude = data[name]['coordinates']['longitude']

            if latitude and longitude:
                LOGGER.info(
                    f'Setting webdriver geolcation to {data[name]["coordinates"]}.'
                )
                webdriver_.set_coordinates((latitude, longitude))

    LOGGER.info(
        f'Loaded webdriver {webdriver_.name} in {round(time.time() - start_time, 2)} seconds.'
    )

    return webdriver_


__all__ = [
    'DEFAULT_CONFIG', 'MOBILE_CONFIG', 'HEADLESS_CONFIG',
    'create_driver_config', 'load_driver_from_config'
]
