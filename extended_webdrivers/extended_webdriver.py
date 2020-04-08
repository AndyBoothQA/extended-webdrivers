import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .js import Js

LOGGER = logging.getLogger(__name__)


class ExtendedWebdriver:
    """ Extends a webdriver class with additional methods. """

    def __init__(self):
        if self is ExtendedWebdriver or not isinstance(self, WebDriver):
            raise TypeError(f'Class must inherit {WebDriver}')
        self.js = Js(self)
        self.wait_stable_timeout = 10
        self._angular_available = None
        self._jquery_available = None

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        self._angular_available = None
        self._jquery_available = None

    def refresh(self, *args, **kwargs):
        super().refresh(*args, **kwargs)
        self._angular_available = None
        self._jquery_available = None

    def back(self, *args, **kwargs):
        super().back(*args, **kwargs)
        self._angular_available = None
        self._jquery_available = None

    def forward(self, *args, **kwargs):
        super().forward(*args, **kwargs)
        self._angular_available = None
        self._jquery_available = None

    def get_angular_availability(self):
        result = self.execute_script('return window.getAllAngularRootElements != undefined')
        LOGGER.debug(f'get_angular_availability() returned {result}')
        return result

    def refresh_angular_availability(self):
        self._angular_available = self.get_angular_availability()

    def is_angular_available(self):
        if self._angular_available is None:
            self.refresh_angular_availability()
        return self._angular_available

    def is_angular_ready(self):
        if not self.is_angular_available():
            return True
        result = self.execute_script(
            'return window.getAllAngularTestabilities().every((testability) => testability.isStable())'
        )
        LOGGER.debug(f'is_angular_ready returned {result}')
        return result

    def get_jquery_availability(self):
        result = self.execute_script('return window.jQuery != undefined')
        LOGGER.debug(f'get_jquery_availability() returned {result}')
        return result

    def refresh_jquery_availability(self):
        self._jquery_available = self.get_jquery_availability()

    def is_jquery_available(self):
        if self._jquery_available is None:
            self.refresh_jquery_availability()
        return self._jquery_available

    def is_jquery_ready(self):
        if not self.is_jquery_available():
            LOGGER.debug('is_jquery_ready returned True')
            return True
        result = self.execute_script('return jQuery.active == 0')
        LOGGER.debug(f'is_jquery_ready returned {result}')
        return result

    def is_document_ready(self):
        result = self.execute_script('return document.readyState == "complete"')
        LOGGER.debug(f'is_document_ready returned {result}')
        return result

    def is_stable(self) -> bool:
        result = self.is_angular_ready() and self.is_jquery_ready() and self.is_document_ready()
        LOGGER.debug(f'is_stable returned {result}')
        return result

    def wait_for_stable(self, pause: float = 0.0, poll_rate: float = 0.5, timeout: int = -1) -> None:
        """
        Goes through a series of checks to verify the the web page is ready for use.
        Selenium does a majority of this but this adds extended functions by checking
        jQuery, Angular and the document ready state.

        :param pause: The amount of time in seconds to pause code execution before checking the web page. (Default: 0.0)
        :param poll_rate: How often in seconds to check the state of the web page. (Default: 0.5)
        :param timeout: The amount of time in seconds to wait for the browser to report back as ready. The default time
                        is determined by the wait_stable_timeout variable.
        """

        if timeout == -1:
            timeout = self.wait_stable_timeout
        if timeout <= 0:
            return
        time.sleep(pause)
        end_time = time.time() + timeout
        while True:
            if self.is_stable():
                return
            if poll_rate > 0:
                time.sleep(poll_rate)
            if time.time() > end_time:
                break
        LOGGER.warning(f'wait_for_stable() timed out after {timeout} seconds.')

    wait_stable = wait_for_stable

    def set_coordinates(self, coordinates: tuple) -> None:
        """ Sets the geolocation for location services. """
        self.execute_script(
            '''
        window.navigator.geolocation.getCurrentPosition = function(success) {
            var position = {
                "coords" : {
                    "latitude": "%s",
                    "longitude": "%s"
                }
            };
            success(position);
        }'''
            % coordinates
        )

    def get_coordinates(self) -> tuple:
        latitude = self.execute_script(
            '''
        latitude = ""
        window.navigator.geolocation.getCurrentPosition(function(pos) {
            latitude = pos.coords.latitude
        });
        return latitude
        '''
        )

        longitude = self.execute_script(
            '''
        longitude = ""
        window.navigator.geolocation.getCurrentPosition(function(pos) {
            longitude = pos.coords.longitude
        });
        return longitude
        '''
        )

        return latitude, longitude

    def get_current_frame(self) -> WebElement:
        """ Gets the current frame. """
        return self.execute_script('return window.frameElement')

    def get_timezone_offset(self) -> int:
        """ Gets the timezone offset of the browser in minutes. """
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
            'return window.outerWidth == screen.availWidth && window.outerHeight == screen.availHeight'
        )
