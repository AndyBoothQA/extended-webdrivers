from selenium.webdriver import Safari as _Safari

from .extended_webdriver import ExtendedWebdriver


class Safari(ExtendedWebdriver, _Safari):
    pass
