import json
import logging
import os
import shutil
import time

from selenium.webdriver import FirefoxProfile, ChromeOptions, FirefoxOptions, IeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .android import Android
from .chrome import Chrome
from .edge import Edge
from .extended_webdriver import ExtendedWebdriver
from .firefox import Firefox
from .ie import Ie
from .opera import Opera
from .phantomjs import PhantomJS
from .remote import Remote

LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = 'webdrivers-default.json'
MOBILE_CONFIG = 'webdrivers-mobile.json'
HEADLESS_CONFIG = 'webdrivers-headless.json'


class InvalidWebdriver(Exception):
    pass


def create_driver_config(file_name: str):
    """
    Creates a new webdriver configuration file based off the default.

    :param name: The name of the new configuration file.
    """
    shutil.copy(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), DEFAULT_CONFIG), os.path.join(os.getcwd(), file_name)
    )


def load_driver_from_config(name: str, file_path: str = DEFAULT_CONFIG) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a config file.

    :param name: The name of the webdriver to load.
    :param config_name: The name of the config file to load. This first searches for default config files in the
                        extended_webdrivers package. If it can't find any, it then searches the current directory.
    """
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError('Config file not found.')
    with open(file_path, 'r') as config_file:
        LOGGER.info(f'Loading webdriver settings from {config_file.name}.')
        data = json.load(config_file)
        return load_driver(name, data[name])


def load_driver(name: str, data: dict) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a dictionary.

    :param webdriver: The name of the webdriver to load.
    :param data: Dict containing the webdriver configuration.
    """
    name = name.lower()
    start_time = time.time()
    if name == 'remote':
        command_executor = data.get('command_executor', 'http://127.0.0.1:4444/wd/hub')
        desired_capabilities = data.get('desired_capabilities')
        browser_profile = data.get('browser_profile')
        if browser_profile:
            browser_profile = FirefoxProfile(browser_profile)
        keep_alive = bool(data.get('keep_alive', False))

        webdriver_ = Remote(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities,
            browser_profile=browser_profile,
            proxy=None,
            keep_alive=keep_alive,
            file_detector=None,
            options=None,
        )
    elif name == 'chrome':
        executable_path = data.get('executable_path', 'chromedriver')
        port = int(data.get('port', 0))
        service_args = data.get('service_args')
        desired_capabilities = data.get('desired_capabilities')
        service_log_path = data.get('service_log_path')
        keep_alive = data.get('keep_alive', True)

        options = data.get('options')
        if isinstance(options, dict):
            chrome_options = ChromeOptions()
            arguments = options.get('arguments')
            if isinstance(arguments, list):
                for argument in arguments:
                    chrome_options.add_argument(argument)

            experimental_options = options.get('experimental_options')
            if isinstance(experimental_options, dict):
                for k, v in experimental_options.items():
                    chrome_options.add_experimental_option(k, v)

            capabilities = options.get('capabilities')
            if isinstance(capabilities, dict):
                for k, v in capabilities.items():
                    chrome_options.set_capability(k, v)

            chrome_options.binary_location = data.get('binary_location', '')
            options = chrome_options

        webdriver_ = Chrome(
            executable_path=executable_path,
            port=port,
            options=options,
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            service_log_path=service_log_path,
            chrome_options=None,  # Deprecated
            keep_alive=keep_alive,
        )
    elif name == 'firefox':
        firefox_profile = data.get('firefox_profile')
        if isinstance(firefox_profile, dict):
            profile = FirefoxProfile()
            preferences = firefox_profile.get('preferences')
            if isinstance(preferences, dict):
                for k, v in preferences.items():
                    profile.set_preference(k, v)
            firefox_profile = profile

        firefox_binary = data.get('firefox_binary')
        timeout = int(data.get('timeout'), 30)
        executable_path = data.get('executable_path', 'geckodriver')

        options = data.get('options')
        if isinstance(options, dict):
            firefox_options = FirefoxOptions()
            arguments = options.get('arguments')
            if isinstance(arguments, list):
                for argument in arguments:
                    firefox_options.add_argument(argument)
            options = firefox_options

        service_log_path = data.get('service_log_path', 'geckodriver.log')
        service_args = data.get('service_args')
        desired_capabilities = data.get('desired_capabilities')
        log_path = data.get('log_path')

        webdriver_ = Firefox(
            firefox_profile=firefox_profile,
            firefox_binary=firefox_binary,
            timeout=timeout,
            capabilities=None,
            proxy=None,
            executable_path=executable_path,
            options=options,
            service_log_path=service_log_path,
            firefox_options=None,  # Deprecated
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            log_path=log_path,
        )
    elif name == 'edge':
        executable_path = data.get('executable_path', 'MicrosoftWebDriver.exe')
        capabilities = data.get('capabilities')
        port = int(data.get('port', 0))
        verbose = bool(data.get('verbose', False))
        service_log_path = data.get('service_log_path')
        log_path = data.get('log_path')
        keep_alive = bool(data.get('keep_alive', False))

        webdriver_ = Edge(
            executable_path=executable_path,
            capabilities=capabilities,
            port=port,
            verbose=verbose,
            service_log_path=service_log_path,
            log_path=log_path,
            keep_alive=keep_alive,
        )
    elif name == 'android':
        host = data.get('host', 'localhost')
        port = int(data.get('port', 4444))
        desired_capabilities = data.get('desired_capabilities', DesiredCapabilities.ANDROID)

        webdriver_ = Android(host=host, port=port, desired_capabilities=desired_capabilities)
    elif name == 'ie' or name == 'iexplore':
        from selenium.webdriver.ie.webdriver import (
            DEFAULT_PORT,
            DEFAULT_TIMEOUT,
            DEFAULT_HOST,
            DEFAULT_LOG_LEVEL,
            DEFAULT_SERVICE_LOG_PATH,
        )

        restricted_mode = bool(data.get('restricted_mode', False))
        executable_path = data.get('executable_path', 'IEDriverServer.exe')
        capabilities = data.get('capabilities')
        port = int(data.get('port', DEFAULT_PORT))
        timeout = int(data.get('port', DEFAULT_TIMEOUT))
        host = data.get('host', DEFAULT_HOST)
        log_level = data.get('log_level', DEFAULT_LOG_LEVEL)
        service_log_path = data.get('service_log_path', DEFAULT_SERVICE_LOG_PATH)

        options = data.get('options')
        if isinstance(options, dict):
            ie_options = IeOptions()

            capabilities = options.get('capabilities')
            if isinstance(capabilities, dict):
                for k, v in capabilities.items():
                    ie_options.set_capability(k, v)

            additional_options = options.get('additional_options')
            if isinstance(additional_options, dict):
                for k, v in additional_options.items():
                    ie_options.add_additional_option(k, v)
            options = ie_options

        desired_capabilities = data.get('desired_capabilities')
        log_file = data.get('log_file')
        keep_alive = bool(data.get('keep_alive', False))

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
            keep_alive=keep_alive,
        )
    elif name == 'opera':
        executable_path = data.get('executable_path')
        port = int(data.get('port', 0))

        options = data.get('options')
        if isinstance(options, dict):
            chrome_options = ChromeOptions()
            arguments = options.get('arguments')
            if isinstance(arguments, list):
                for argument in arguments:
                    chrome_options.add_argument(argument)

                experimental_options = options.get('experimental_options')
                if isinstance(experimental_options, dict):
                    for k, v in experimental_options.items():
                        chrome_options.add_experimental_option(k, v)

                capabilities = options.get('capabilities')
                if isinstance(capabilities, dict):
                    for k, v in capabilities.items():
                        chrome_options.set_capability(k, v)

                chrome_options.binary_location = data.get('binary_location', '')
                options = chrome_options

        service_args = data.get('service_args')
        desired_capabilities = data.get('desired_capabilities')
        service_log_path = data.get('service_log_path')
        keep_alive = bool(data.get('keep_alive', True))

        webdriver_ = Opera(
            executable_path=executable_path,
            port=port,
            options=options,
            service_args=service_args,
            desired_capabilities=desired_capabilities,
            service_log_path=service_log_path,
            opera_options=None,  # Deprecated
            keep_alive=keep_alive,
        )
    elif name == 'phantomjs':
        executable_path = data.get('executable_path', 'phantomjs')
        port = int(data.get('port', 0))
        desired_capabilities = data.get('desired_capabilities', DesiredCapabilities.PHANTOMJS)
        service_args = data.get('service_args')
        service_log_path = data.get('service_log_path')

        webdriver_ = PhantomJS(
            executable_path=executable_path,
            port=port,
            desired_capabilities=desired_capabilities,
            service_args=service_args,
            service_log_path=service_log_path,
        )
    else:
        raise InvalidWebdriver(f'{name} is an invalid webdriver.')

    size = data.get('size')
    if size:
        x, y = 1920, 1080
        if isinstance(size, list) and len(size) == 2:
            x, y = size
        elif isinstance(size, dict):
            x, y = size['x'], size['y']

        if isinstance(webdriver_, Chrome):
            options = data.get('options')
            if isinstance(options, dict):
                arguments = options.get('arguments')
                if isinstance(arguments, list):
                    for argument in arguments:
                        if '--window-size' in argument or '--start-maximized' in argument:
                            x, y = 0, 0
                            break

        if x and y:
            LOGGER.info(f'Setting webdriver window size to {x}x{y}')
            webdriver_.set_window_size(x, y)

    full_screen = bool(data.get('full_screen', False))
    if full_screen:
        if isinstance(webdriver_, Chrome):
            if isinstance(options, dict):
                arguments = options.get('arguments')
                if isinstance(arguments, list):
                    if '--start-maximized' in arguments or '--headless' in arguments:
                        full_screen = False

    if full_screen:
        LOGGER.info('Setting webdriver to full screen.')
        webdriver_.maximize_window()

    implicitly_wait = float(data.get('implicitly_wait', 0.0))
    if implicitly_wait > 0.0:
        LOGGER.info(f'Setting webdriver implicit wait time to {data["implicitly_wait"]}.')
        webdriver_.implicitly_wait(int(data['implicitly_wait']))

    coordinates = data.get('coordinates')
    if coordinates:
        latitude, longitude = None, None
        if isinstance(coordinates, list) and len(data['coordinates']) == 2:
            latitude, longitude = coordinates
        elif isinstance(coordinates, dict):
            latitude, longitude = coordinates['latitude'], coordinates['longitude']

        if latitude and longitude:
            LOGGER.info(f'Setting webdriver geolcation to {data["coordinates"]}.')
            webdriver_.set_coordinates((latitude, longitude))

    LOGGER.info(f'Loaded webdriver {webdriver_.name} in {round(time.time() - start_time, 2)} seconds.')
    return webdriver_


__all__ = ['DEFAULT_CONFIG', 'MOBILE_CONFIG', 'HEADLESS_CONFIG', 'create_driver_config', 'load_driver_from_config']
