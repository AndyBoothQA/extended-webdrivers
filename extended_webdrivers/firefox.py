import selenium.webdriver

from . import ExtendedWebdriver


class Firefox(selenium.webdriver.Firefox, ExtendedWebdriver):
    pass
