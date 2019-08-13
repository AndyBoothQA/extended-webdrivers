import logging
import time

import selenium.webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.remote.webelement import WebElement

LOGGER = logging.getLogger('extended_webdrivers')


class ExtendedWebdriver(selenium.webdriver.Remote):
    """
    Extends the funcionality of the selenium webdriver with additional methods
    to get the state of jQuery and Angular calls, change the geolocation of the
    browser, and directly call javascript on elements.
    """

    def is_angular_available(self):
        try:
            result = self.execute_script(
                'return window.getAllAngularRootElements != undefined')
        except NoSuchWindowException:
            return True
        LOGGER.debug(f'is_angular_available returned {result}')
        return result

    def is_angular_ready(self):
        if not self.is_angular_available():
            return True
        script = '''
        var testabilities = window.getAllAngularTestabilities()
        for (i = 0; i < testabilities.length; i++) {
            if (!testabilities[i].isStable()) {
                return false
            }
        }
        return true
        '''
        try:
            result = self.execute_script(script)
        except NoSuchWindowException:
            return True
        LOGGER.debug(f'is_angular_ready returned {result}')
        return result

    def is_jquery_available(self):
        try:
            result = self.execute_script('return window.jQuery != undefined')
        except NoSuchWindowException:
            return True
        LOGGER.debug(f'is_jquery_available returned {result}')
        return result

    def is_jquery_ready(self):
        if not self.is_jquery_available():
            LOGGER.debug('is_jquery_ready returned True')
            return True
        try:
            result = self.execute_script('return jQuery.active == 0')
        except NoSuchWindowException:
            return True
        LOGGER.debug(f'is_jquery_ready returned {result}')
        return result

    def is_document_ready(self):
        try:
            result = self.execute_script(
                'return document.readyState == "complete"')
        except NoSuchWindowException:
            return True
        LOGGER.debug(f'is_document_ready returned {result}')
        return result

    def is_stable(self) -> bool:
        result = self.is_angular_ready() and self.is_jquery_ready(
        ) and self.is_document_ready()
        LOGGER.debug(f'is_stable returned {result}')
        return result

    def wait_for_stable(self,
                        pause: float = 0.0,
                        poll_rate: float = 0.5,
                        timeout: int = 10) -> None:
        """
        Goes through a series of checks to verify the the web page is ready for use.
        Selenium does a majority of this but this adds extended functions by checking
        jQuery, Angular and the document ready state.

        Parameters
        ----------
            pause - The amount of time in seconds to pause code execution before checking the web page. (Default: 0.0)
            poll_rate - How often in seconds to check the state of the web page. (Default: 0.5)
            timeout - The amount of time in seconds to allow the web page to report as not ready until bypassing.
                    If this occurs, technically there can be an issue, but code execution will continue
                    without raising an exception. (Default: 10)
        """

        time.sleep(pause)

        end_time = time.time() + timeout
        while True:
            if self.is_stable():
                return True
            time.sleep(poll_rate)
            if time.time() > end_time:
                break
        LOGGER.debug(f'wait_for_stable() timed out after {timeout} seconds.')
        return None

    def set_coordinates(self, cords: tuple) -> None:
        """ Sets the geolocation for location services. """
        self.execute_script('''
        window.navigator.geolocation.getCurrentPosition = function(success) {
            var position = {
                "coords" : {
                    "latitude": "%s",
                    "longitude": "%s"
                }
            };
            success(position);
        }''' % cords)

    def get_coordinates(self) -> tuple:
        latitude = self.execute_script('''
        latitude = ""
        window.navigator.geolocation.getCurrentPosition(function(pos) {
            latitude = pos.coords.latitude
        });
        return latitude
        ''')

        longitude = self.execute_script('''
        longitude = ""
        window.navigator.geolocation.getCurrentPosition(function(pos) {
            longitude = pos.coords.longitude
        });
        return longitude
        ''')

        return (latitude, longitude)

    def get_current_frame(self) -> WebElement:
        """ Returns the current iframe element, None if not in an iframe. """
        return self.execute_script('return window.frameElement')

    def get_timezone_offset(self) -> int:
        """
        Returns the timezone offset of the browser in minutes.
        """
        script = """
        var dt = new Date();
        var tz = dt.getTimezoneOffset();
        return tz
        """
        return self.execute_script(script)

    @property
    def fullscreen(self) -> bool:
        """ Returns if the window is maximized. """
        return self.execute_script(
            'return window.outerWidth == screen.availWidth && window.outerHeight == screen.availHeight')

    def js_focus(self, element: WebElement) -> None:
        """ Focuses on an element. """
        self.execute_script('arguments[0].focus()', element)

    def js_click(self, element: WebElement) -> None:
        """ Clicks on an element. """
        self.execute_script('arguments[0].click()', element)

    def js_blur(self, element: WebElement) -> None:
        """ Clear the focus from a selected web element. """
        self.execute_script('arguments[0].blur()', element)

    def js_scroll_into_view(self, element: WebElement) -> None:
        """ Scrolls the element into view.  """
        self.execute_script("arguments[0].scrollIntoView();", element)
