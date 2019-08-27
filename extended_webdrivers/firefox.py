from selenium.webdriver import Firefox as Firefox_

from .extended_webdriver import ExtendedWebdriver


class Firefox(Firefox_, ExtendedWebdriver):
    pass
