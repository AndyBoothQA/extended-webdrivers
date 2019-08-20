from selenium.webdriver.remote.webelement import WebElement


class Js:
    def __init__(self, driver):
        self.driver = driver
        self.window = Window(self.driver)

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
    
    def get_bounding_client_rect(self, element: WebElement) -> dict:
        """ Gets the bounding client rect of an element. """
        return self.driver.execute_script('return arguments[0].getBoundingClientRect()', element)


class Window:
    def __init__(self, driver):
        self.driver = driver
        self.local_storage = LocalStorage(self.driver)
        self.indexed_db = IndexedDB(self.driver)


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


class IndexedDB:
    def __init__(self, driver):
        self.driver = driver

    def get_database_object(self, database_name: str,
                            object_name: str) -> dict:
        """ Gets an object from a database in IndexedDB by name.

        :param database_name: Name of the database to search in.
        :param object_name: Name of the object to find.
        """
        script = """
        var databaseName = arguments[0]
        var objectName = arguments[1]
        var callback = arguments[arguments.length - 1];

        var db_request = window.indexedDB.open(databaseName);

        db_request.onerror = function(event) {
            callback(null)
        };

        db_request.onsuccess = function(event) {
            var db = db_request.result;
            var transaction = db.transaction(objectName);
            var objectStore = transaction.objectStore(objectName);
            var data_request = objectStore.getAll();

            data_request.onerror = function(event) {
                callback(null)
            };

            data_request.onsuccess = function(event) {
                callback(data_request.result)
            };
        };
        """
        return self.driver.execute_async_script(script, database_name,
                                                object_name)
