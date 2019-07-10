import selenium.webdriver

from . import ExtendedWebdriver


class Android(selenium.webdriver.Android, ExtendedWebdriver):
    pass
