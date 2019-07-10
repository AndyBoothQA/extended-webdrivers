__version__ = '0.0.1'

import json
import shutil
import os

from selenium import webdriver

from .extended_webdriver import ExtendedWebdriver

from .android import Android
from .chrome import Chrome
from .edge import Edge
from .firefox import Firefox
from .ie import Ie
from .opera import Opera
from .phantomjs import PhantomJS
from .remote import Remote

DEFAULT_CONFIG = 'webdrivers-default.json'
MOBILE_CONFIG = 'webdrivers-mobile.json'


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


def load_driver_from_config(driver: str, config_name: str = DEFAULT_CONFIG
                            ) -> ExtendedWebdriver:
    """
    Loads a driver with settings from a config file.

    Parameters
    ----------
    driver - The name of the driver to load.
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
        return load_driver(driver, data)


def load_driver_from_json(driver: str, data: str) -> ExtendedWebdriver:
    """
    Loads a driver with settings from a json string.

    Parameters
    ----------
    driver - The name of the driver to load.
    data - The raw json string.
    """
    data = json.loads(data)
    return load_driver(driver, data)


def load_driver(driver: str, data: dict) -> ExtendedWebdriver:
    """
    Loads a driver with settings from a dictionary.

    Parameters
    ----------
    driver - The name of the driver to load.
    data - The raw json string.
    """
    if driver == 'remote':
        return Remote(command_executor=data['remote']['command_executor'])
    elif driver == 'chrome':
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
        return Chrome(
            executable_path=data['chrome']['executable_path'],
            port=data['chrome']['port'],
            options=options,
            service_args=data['chrome']['service_args'],
            desired_capabilities=data['chrome']['desired_capabilities'],
            service_log_path=data['chrome']['service_log_path'],
            chrome_options=None,
            keep_alive=data['chrome']['keep_alive'])
    elif driver == 'firefox':
        options = webdriver.FirefoxOptions()
        if isinstance(data['firefox']['options']['arguments'], dict):
            for argument in data['firefox']['options']['arguments']:
                options.add_argument(argument)
        firefox_profile = webdriver.FirefoxProfile()
        if isinstance(data['firefox']['firefox_profile']['preferences'], dict):
            for k, v in data['firefox']['firefox_profile'][
                    'preferences'].items():
                firefox_profile.set_preference(k, v)
        return Firefox(
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
    elif driver == 'edge':
        return Edge(executable_path=data['edge']['executable_path'],
                    capabilities=data['edge']['capabilities'],
                    port=data['edge']['port'],
                    verbose=data['edge']['verbose'],
                    service_log_path=data['edge']['service_log_path'],
                    log_path=data['edge']['log_path'],
                    keep_alive=data['edge']['keep_alive'])
    elif driver == 'android':
        return Android(
            host=data['android']['host'],
            port=data['android']['port'],
            desired_capabilities=data['android']['desired_capabilities'])
    elif driver == 'ie' or driver == 'iexplore':
        ie_options = webdriver.IeOptions()
        if isinstance(data['ie']['ie_options']['capabilities'], dict):
            for k, v in data['ie']['ie_options']['capabilities'].items():
                ie_options.set_capability(k, v)
        if isinstance(data['ie']['ie_options']['additional_options'], dict):
            for additional_option in data['ie']['ie_options'][
                    'additional_options']:
                ie_options.add_additional_option(additional_option.name,
                                                 additional_option.value)
        return Ie(restricted_mode=False,
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
    elif driver == 'opera':
        return Opera(
            desired_capabilities=data['opera']['desired_capabilities'],
            executable_path=data['opera']['executable_path'],
            port=data['opera']['port'],
            service_log_path=data['opera']['service_log_path'],
            service_args=data['opera']['service_args'],
            options=data['opera']['options'])
    elif driver == 'phantomjs':
        return PhantomJS(
            executable_path=data['phantomjs']['executable_path'],
            port=data['phantomjs']['port'],
            desired_capabilities=json.dumps(
                data['phantomjs']['desired_capabilities']),
            service_args=data['phantomjs']['service_args'],
            service_log_path=data['phantomjs']['service_log_path'])
