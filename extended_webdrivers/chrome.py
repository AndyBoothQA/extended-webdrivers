from selenium.webdriver import Chrome as Chrome_

from .extended_webdriver import ExtendedWebdriver


class Chrome(Chrome_, ExtendedWebdriver):
    pass
