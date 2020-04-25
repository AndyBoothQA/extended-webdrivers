from selenium.webdriver import PhantomJS as _PhantomJS

from .extended_webdriver import ExtendedWebdriver


class PhantomJS(ExtendedWebdriver, _PhantomJS):
    pass
