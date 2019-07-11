import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class PhantomJS(selenium.webdriver.PhantomJS, ExtendedWebdriver):
    pass
