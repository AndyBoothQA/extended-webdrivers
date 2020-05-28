from selenium.webdriver import Firefox as _Firefox

from .extended_webdriver import ExtendedWebdriver


class Firefox(ExtendedWebdriver, _Firefox):
    pass
