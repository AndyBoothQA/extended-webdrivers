import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class Chrome(selenium.webdriver.Chrome, ExtendedWebdriver):
    pass
