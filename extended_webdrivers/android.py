from selenium.webdriver import Android as _Android

from .extended_webdriver import ExtendedWebdriver


class Android(_Android, ExtendedWebdriver):
    pass
