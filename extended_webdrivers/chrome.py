import logging

from selenium.webdriver import Chrome as Chrome_

from .extended_webdriver import ExtendedWebdriver

LOGGER = logging.getLogger('extended_webdrivers')


class Chrome(Chrome_, ExtendedWebdriver):
    def set_network_conditions(self, **network_conditions):
        super().set_network_conditions(**network_conditions)
        LOGGER.info(f'Set network conditions: {network_conditions}')
