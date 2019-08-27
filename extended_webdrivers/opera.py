from selenium.webdriver.opera.webdriver import OperaDriver as OperaDriver_

from .extended_webdriver import ExtendedWebdriver


class Opera(OperaDriver_, ExtendedWebdriver):
    pass
