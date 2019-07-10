import selenium.webdriver

from . import ExtendedWebdriver


class Edge(selenium.webdriver.Edge, ExtendedWebdriver):
    pass
