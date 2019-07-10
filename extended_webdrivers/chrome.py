import selenium.webdriver

from . import ExtendedWebdriver


class Chrome(selenium.webdriver.Chrome, ExtendedWebdriver):
    pass
