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


def create_driver_config(config_name: str):
    """
    Creates a new webdriver configuration file based off the default.

    :param config_name: The name of the new configuration file.
    """
    shutil.copy(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), DEFAULT_CONFIG),
        os.path.join(os.getcwd(), config_name),
    )


def load_driver_from_config(name: str, config_path: str = DEFAULT_CONFIG) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a config file.

    :param name: The name of the webdriver to load.
    :param config_path: The path of the config file to load.
    """
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError('Config file not found.')
    with open(config_path, 'r') as f:
        LOGGER.info(f'Loading webdriver settings from {f.name}.')
        return load_driver(name, json.load(f)[name])


def load_driver(name: str, driver_settings: dict) -> ExtendedWebdriver:
    """
    Loads a webdriver with settings from a dictionary.

    :param name: The name of the webdriver to load.
    :param driver_settings: Dict containing the webdriver configuration.
    """
    start_time = time.time()
    if (name := name.lower()) == 'remote':
        if browser_profile := driver_settings.get('browser_profile'):
            browser_profile = FirefoxProfile(browser_profile)

        driver = Remote(
            command_executor=driver_settings.get('command_executor', 'http://127.0.0.1:4444/wd/hub'),
            desired_capabilities=driver_settings.get('desired_capabilities'),
            browser_profile=browser_profile,
            proxy=None,
            keep_alive=bool(driver_settings.get('keep_alive', False)),
            file_detector=None,
            options=None,
        )
    elif name == 'chrome':
        if isinstance(options := driver_settings.get('options'), dict):
            chrome_options = ChromeOptions()
            if isinstance(arguments := options.get('arguments'), list):
                for argument in arguments:
                    chrome_options.add_argument(argument)
            if isinstance(experimental_options := options.get('experimental_options'), dict):
                for k, v in experimental_options.items():
                    chrome_options.add_experimental_option(k, v)
            if isinstance(capabilities := options.get('capabilities'), dict):
                for k, v in capabilities.items():
                    chrome_options.set_capability(k, v)
            chrome_options.binary_location = driver_settings.get('binary_location', '')
            options = chrome_options

        driver = Chrome(
            executable_path=driver_settings.get('executable_path', 'chromedriver'),
            port=int(driver_settings.get('port', 0)),
            options=options,
            service_args=driver_settings.get('service_args'),
            desired_capabilities=driver_settings.get('desired_capabilities'),
            service_log_path=driver_settings.get('service_log_path'),
            chrome_options=None,  # Deprecated
            keep_alive=driver_settings.get('keep_alive', True),
        )
    elif name == 'firefox':
        if isinstance(firefox_profile := driver_settings.get('firefox_profile'), dict):
            profile = FirefoxProfile()
            if isinstance(preferences := firefox_profile.get('preferences'), dict):
                for k, v in preferences.items():
                    profile.set_preference(k, v)
            firefox_profile = profile

        if isinstance(options := driver_settings.get('options'), dict):
            firefox_options = FirefoxOptions()
            if isinstance(arguments := options.get('arguments'), list):
                for argument in arguments:
                    firefox_options.add_argument(argument)
            options = firefox_options

        driver = Firefox(
            firefox_profile=firefox_profile,
            firefox_binary=driver_settings.get('firefox_binary'),
            timeout=int(driver_settings.get('timeout'), 30),
            capabilities=None,
            proxy=None,
            executable_path=driver_settings.get('executable_path', 'geckodriver'),
            options=options,
            service_log_path=driver_settings.get('service_log_path', 'geckodriver.log'),
            firefox_options=None,  # Deprecated
            service_args=driver_settings.get('service_args'),
            desired_capabilities=driver_settings.get('desired_capabilities'),
            log_path=driver_settings.get('log_path'),
        )
    elif name == 'edge':
        driver = Edge(
            executable_path=driver_settings.get('executable_path', 'MicrosoftWebDriver.exe'),
            capabilities=driver_settings.get('capabilities'),
            port=int(driver_settings.get('port', 0)),
            verbose=bool(driver_settings.get('verbose', False)),
            service_log_path=driver_settings.get('service_log_path'),
            log_path=driver_settings.get('log_path'),
            keep_alive=bool(driver_settings.get('keep_alive', False)),
        )
    elif name == 'android':
        driver = Android(
            host=driver_settings.get('host', 'localhost'),
            port=int(driver_settings.get('port', 4444)),
            desired_capabilities=driver_settings.get('desired_capabilities', DesiredCapabilities.ANDROID),
        )
    elif name == 'ie' or name == 'iexplore':
        from selenium.webdriver.ie.webdriver import (
            DEFAULT_PORT,
            DEFAULT_TIMEOUT,
            DEFAULT_HOST,
            DEFAULT_LOG_LEVEL,
            DEFAULT_SERVICE_LOG_PATH,
        )

        if isinstance(options := driver_settings.get('options'), dict):
            ie_options = IeOptions()
            if isinstance(capabilities := options.get('capabilities'), dict):
                for k, v in capabilities.items():
                    ie_options.set_capability(k, v)
            if isinstance(additional_options := options.get('additional_options'), dict):
                for k, v in additional_options.items():
                    ie_options.add_additional_option(k, v)
            options = ie_options

        driver = Ie(
            restricted_mode=bool(driver_settings.get('restricted_mode', False)),
            executable_path=driver_settings.get('executable_path', 'IEDriverServer.exe'),
            capabilities=driver_settings.get('capabilities'),
            port=int(driver_settings.get('port', DEFAULT_PORT)),
            timeout=int(driver_settings.get('port', DEFAULT_TIMEOUT)),
            host=driver_settings.get('host', DEFAULT_HOST),
            log_level=driver_settings.get('log_level', DEFAULT_LOG_LEVEL),
            service_log_path=driver_settings.get('service_log_path', DEFAULT_SERVICE_LOG_PATH),
            options=options,
            ie_options=None,  # Deprecated
            desired_capabilities=driver_settings.get('desired_capabilities'),
            log_file=driver_settings.get('log_file'),
            keep_alive=bool(driver_settings.get('keep_alive', False)),
        )
    elif name == 'opera':
        if isinstance(options := driver_settings.get('options'), dict):
            chrome_options = ChromeOptions()
            arguments = options.get('arguments')
            if isinstance(arguments, list):
                for argument in arguments:
                    chrome_options.add_argument(argument)
                if isinstance(experimental_options := options.get('experimental_options'), dict):
                    for k, v in experimental_options.items():
                        chrome_options.add_experimental_option(k, v)
                if isinstance(capabilities := options.get('capabilities'), dict):
                    for k, v in capabilities.items():
                        chrome_options.set_capability(k, v)
                chrome_options.binary_location = driver_settings.get('binary_location', '')
                options = chrome_options

        driver = Opera(
            executable_path=driver_settings.get('executable_path'),
            port=int(driver_settings.get('port', 0)),
            options=options,
            service_args=driver_settings.get('service_args'),
            desired_capabilities=driver_settings.get('desired_capabilities'),
            service_log_path=driver_settings.get('service_log_path'),
            opera_options=None,  # Deprecated
            keep_alive=bool(driver_settings.get('keep_alive', True)),
        )
    elif name == 'phantomjs':
        driver = PhantomJS(
            executable_path=driver_settings.get('executable_path', 'phantomjs'),
            port=int(driver_settings.get('port', 0)),
            desired_capabilities=driver_settings.get('desired_capabilities', DesiredCapabilities.PHANTOMJS),
            service_args=driver_settings.get('service_args'),
            service_log_path=driver_settings.get('service_log_path'),
        )
    else:
        raise InvalidWebdriver(f'{name} is an invalid webdriver.')

    if size := driver_settings.get('size'):
        x, y = 1920, 1080
        if isinstance(size, list) and len(size) == 2:
            x, y = size
        elif isinstance(size, dict):
            x, y = size['x'], size['y']
        if isinstance(driver, Chrome):
            if isinstance(options := driver_settings.get('options'), dict):
                if isinstance(arguments := options.get('arguments'), list):
                    if any(a for a in arguments if a in ['--window-size', '--start-maximized']):
                        x, y = 0, 0
        if x and y:
            LOGGER.debug(f'{x=} {y=}')
            driver.set_window_size(x, y)

    if full_screen := bool(driver_settings.get('full_screen', False)):
        if isinstance(driver, Chrome):
            if isinstance(options, dict):
                if isinstance(arguments := options.get('arguments'), list):
                    if any(a for a in arguments if a in ['--start-maximized', '--headless']):
                        full_screen = False
    if full_screen:
        LOGGER.debug(f'{full_screen=}')
        driver.maximize_window()

    if implicitly_wait := float(driver_settings.get('implicitly_wait', 0.0)) > 0.0:
        LOGGER.debug(f'{implicitly_wait=}')
        driver.implicitly_wait(int(driver_settings['implicitly_wait']))

    if coordinates := driver_settings.get('coordinates'):
        latitude, longitude = None, None
        if isinstance(coordinates, list) and len(driver_settings['coordinates']) == 2:
            latitude, longitude = coordinates
        elif isinstance(coordinates, dict):
            latitude, longitude = coordinates['latitude'], coordinates['longitude']
        if latitude and longitude:
            LOGGER.debug(f'{latitude=} {longitude=}')
            driver.set_coordinates((latitude, longitude))

    LOGGER.debug(f'Loaded webdriver {driver.name} in {round(time.time() - start_time, 2)} seconds.')
    return driver


__all__ = ['DEFAULT_CONFIG', 'MOBILE_CONFIG', 'HEADLESS_CONFIG', 'create_driver_config', 'load_driver_from_config']
