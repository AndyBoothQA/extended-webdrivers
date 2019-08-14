from selenium.webdriver.remote.webelement import WebElement


class Js:
    def __init__(self, driver):
        self.driver = driver

    def focus(self, element: WebElement) -> None:
        """ Focuses on an element. """
        self.driver.execute_script('arguments[0].focus()', element)

    def click(self, element: WebElement) -> None:
        """ Clicks on an element. """
        self.driver.execute_script('arguments[0].click()', element)

    def blur(self, element: WebElement) -> None:
        """ Clear the focus from a selected web element. """
        self.driver.execute_script('arguments[0].blur()', element)

    def scroll_into_view(self, element: WebElement) -> None:
        """ Scrolls the element into view.  """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    @property
    def window(self):
        return Window(self.driver)


class Window:
    def __init__(self, driver):
        self.driver = driver

    @property
    def local_storage(self):
        return LocalStorage(self.driver)


class LocalStorage:
    def __init__(self, driver):
        self.driver = driver

    def get_item(self, key):
        return self.driver.execute_script(
            "window.localStorage.getItem(arguments[0])", key)

    def set_item(self, key, value):
        self.driver.execute_script(
            "window.localStorage.getItem(arguments[0], arguments[1])", key,
            value)
