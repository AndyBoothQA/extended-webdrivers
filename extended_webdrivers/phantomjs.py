from selenium.webdriver import PhantomJS as _PhantomJS

from .extended_webdriver import ExtendedWebdriver


class PhantomJS(_PhantomJS, ExtendedWebdriver):
    pass
