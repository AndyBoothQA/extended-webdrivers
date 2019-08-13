import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class Opera(selenium.webdriver.opera.webdriver.OperaDriver, ExtendedWebdriver):
    pass
