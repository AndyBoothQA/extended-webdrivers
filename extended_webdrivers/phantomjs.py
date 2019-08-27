from selenium.webdriver import PhantomJS as PhantomJS_

from .extended_webdriver import ExtendedWebdriver


class PhantomJS(PhantomJS_, ExtendedWebdriver):
    pass
