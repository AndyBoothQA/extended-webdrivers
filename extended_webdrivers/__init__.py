"""
Extends the funcionality of the selenium webdriver in Python with 
additional methods to get the state of jQuery and Angular calls, 
change the geolocation of the browser, and directly call javascript 
on elements.
"""

import json
import logging
import os
import shutil
import time

from selenium import webdriver

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

LOGGER = logging.getLogger('extended_webdrivers')


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
        webdriver_ = Remote(command_executor=data['remote']['command_executor'])
    elif name == 'chrome':
        options = webdriver.ChromeOptions()
        if isinstance(data['chrome']['options']['arguments'], dict):
            for argument in data['chrome']['options']['arguments']:
                options.add_argument(argument)
        if isinstance(data['chrome']['options']['experimental_options'], dict):
            for experimental_option in data['chrome']['options'][
                    'experimental_options']:
                options.add_experimental_option(
                    experimental_option, data['chrome']['options']
                    ['experimental_options'][experimental_option])
        if isinstance(data['chrome']['options']['capabilities'], dict):
            for capability in data['chrome']['options']['capabilities']:
                options.set_capability = data['chrome']['options'][
                    'capabilities'][capability]
        webdriver_ = Chrome(
            executable_path=data['chrome']['executable_path'],
            port=data['chrome']['port'],
            options=options,
            service_args=data['chrome']['service_args'],
            desired_capabilities=data['chrome']['desired_capabilities'],
            service_log_path=data['chrome']['service_log_path'],
            chrome_options=None,
            keep_alive=data['chrome']['keep_alive'])
    elif name == 'firefox':
        options = webdriver.FirefoxOptions()
        if isinstance(data['firefox']['options']['arguments'], dict):
            for argument in data['firefox']['options']['arguments']:
                options.add_argument(argument)
        firefox_profile = webdriver.FirefoxProfile()
        if isinstance(data['firefox']['firefox_profile']['preferences'], dict):
            for k, v in data['firefox']['firefox_profile'][
                    'preferences'].items():
                firefox_profile.set_preference(k, v)
        webdriver_ = Firefox(
            firefox_profile=firefox_profile,
            firefox_binary=data['firefox']['firefox_binary'],
            timeout=data['firefox']['timeout'],
            capabilities=data['firefox']['capabilities'],
            proxy=data['firefox']['proxy'],
            executable_path=data['firefox']['executable_path'],
            options=options,
            service_log_path=data['firefox']['service_log_path'],
            firefox_options=data['firefox']['firefox_options'],
            service_args=data['firefox']['service_args'],
            desired_capabilities=data['firefox']['desired_capabilities'],
            log_path=data['firefox']['log_path'])
    elif name == 'edge':
        webdriver_ = Edge(executable_path=data['edge']['executable_path'],
                      capabilities=data['edge']['capabilities'],
                      port=data['edge']['port'],
                      verbose=data['edge']['verbose'],
                      service_log_path=data['edge']['service_log_path'],
                      log_path=data['edge']['log_path'],
                      keep_alive=data['edge']['keep_alive'])
    elif name == 'android':
        webdriver_ = Android(
            host=data['android']['host'],
            port=data['android']['port'],
            desired_capabilities=data['android']['desired_capabilities'])
    elif name == 'ie' or name == 'iexplore':
        ie_options = webdriver.IeOptions()
        if isinstance(data['ie']['ie_options']['capabilities'], dict):
            for k, v in data['ie']['ie_options']['capabilities'].items():
                ie_options.set_capability(k, v)
        if isinstance(data['ie']['ie_options']['additional_options'], dict):
            for additional_option in data['ie']['ie_options'][
                    'additional_options']:
                ie_options.add_additional_option(additional_option.name,
                                                 additional_option.value)
        webdriver_ = Ie(restricted_mode=False,
                    executable_path=data['ie']['executable_path'],
                    capabilities=data['ie']['capabilities'],
                    port=data['ie']['port'],
                    timeout=data['ie']['timeout'],
                    host=data['ie']['host'],
                    log_level=data['ie']['log_level'],
                    service_log_path=data['ie']['service_log_path'],
                    options=data['ie']['options'],
                    ie_options=ie_options,
                    desired_capabilities=data['ie']['desired_capabilities'],
                    log_file=data['ie']['log_file'],
                    keep_alive=data['ie']['keep_alive'])
    elif name == 'opera':
        webdriver_ = Opera(
            desired_capabilities=data['opera']['desired_capabilities'],
            executable_path=data['opera']['executable_path'],
            port=data['opera']['port'],
            service_log_path=data['opera']['service_log_path'],
            service_args=data['opera']['service_args'],
            options=data['opera']['options'])
    elif name == 'phantomjs':
        webdriver_ = PhantomJS(
            executable_path=data['phantomjs']['executable_path'],
            port=data['phantomjs']['port'],
            desired_capabilities=json.dumps(
                data['phantomjs']['desired_capabilities']),
            service_args=data['phantomjs']['service_args'],
            service_log_path=data['phantomjs']['service_log_path'])
    else:
        raise InvalidWebdriver(f'{name} is an invalid webdriver.')

    if isinstance(data[name]['size'], (list, tuple)):
        LOGGER.debug(
            f'Setting webdriver window size to {data[name]["size"][0]}x{data[name]["size"][1]}'
        )
        webdriver_.set_window_size(data[name]['size'][0], data[name]['size'][1])

    if data[name]['full_screen'] == True:
        LOGGER.debug('Setting webdriver to full screen.')
        webdriver_.maximize_window()

    if isinstance(data[name]['implicitly_wait'],
                  (int, float)) and data[name]['implicitly_wait'] > 0:
        LOGGER.debug(
            f'Setting webdriver implicit wait time to {data[name]["implicitly_wait"]}.'
        )
        webdriver_.implicitly_wait(data[name]['implicitly_wait'])

    if isinstance(data[name]['coordinates'], (list, tuple)):
        LOGGER.debug(
            f'Setting webdriver geolcation to {data[name]["coordinates"]}.')

    LOGGER.debug(
        f'Loaded webdriver {webdriver_.name} in {round(time.time() - start_time, 2)} seconds.'
    )

    return webdriver_

__version__ = '0.0.7'
