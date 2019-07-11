import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class Firefox(selenium.webdriver.Firefox, ExtendedWebdriver):
    pass
