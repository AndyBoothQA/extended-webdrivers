from selenium.webdriver import Edge as _Edge

from .extended_webdriver import ExtendedWebdriver


class Edge(ExtendedWebdriver, _Edge):
    pass
