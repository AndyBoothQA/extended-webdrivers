from selenium.webdriver import Remote as _Remote

from .extended_webdriver import ExtendedWebdriver


class Remote(ExtendedWebdriver, _Remote):
    pass
