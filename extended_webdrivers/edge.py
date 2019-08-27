from selenium.webdriver import Edge as Edge_

from .extended_webdriver import ExtendedWebdriver


class Edge(Edge_, ExtendedWebdriver):
    pass
