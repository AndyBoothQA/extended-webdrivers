import selenium.webdriver

from . import ExtendedWebdriver


class PhantomJS(selenium.webdriver.PhantomJS, ExtendedWebdriver):
    pass