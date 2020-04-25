from selenium.webdriver.opera.webdriver import OperaDriver as _OperaDriver

from .extended_webdriver import ExtendedWebdriver


class Opera(ExtendedWebdriver, _OperaDriver):
    pass
