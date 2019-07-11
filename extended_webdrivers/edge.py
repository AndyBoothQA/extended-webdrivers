import selenium.webdriver

from .extended_webdriver import ExtendedWebdriver


class Edge(selenium.webdriver.Edge, ExtendedWebdriver):
    pass
