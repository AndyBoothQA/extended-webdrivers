import selenium.webdriver

from . import ExtendedWebdriver


class Opera(selenium.webdriver.Opera, ExtendedWebdriver):
    pass