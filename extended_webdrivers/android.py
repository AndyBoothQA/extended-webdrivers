import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class Android(selenium.webdriver.Android, ExtendedWebdriver):
    pass
