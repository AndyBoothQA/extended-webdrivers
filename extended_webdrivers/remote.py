from selenium.webdriver import Remote as _Remote

from .extended_webdriver import ExtendedWebdriver


class Remote(_Remote, ExtendedWebdriver):
    pass
