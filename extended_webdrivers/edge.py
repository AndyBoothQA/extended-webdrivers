from selenium.webdriver import Edge as _Edge

from .extended_webdriver import ExtendedWebdriver


class Edge(_Edge, ExtendedWebdriver):
    pass
