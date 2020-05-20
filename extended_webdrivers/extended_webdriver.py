import logging
import time
import warnings
from functools import cached_property

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .js import Js

LOGGER = logging.getLogger(__name__)


class ExtendedWebdriver:
    """ Mixin class that extends a webdriver instance with additional methods. """

    def __init__(self):
        if self is ExtendedWebdriver or not isinstance(self, WebDriver):
            raise TypeError(f'Class must inherit {WebDriver}')
        self.js = Js(self)
        self.wait_stable_timeout = 15

    def _delete_availability_cache(self):
        try:
            del self.jquery_available
        except AttributeError:
            pass
        try:
            del self.angular_available
        except AttributeError:
            pass

    def get(self, url):
        super().get(url)
        self._delete_availability_cache()
        self.wait_stable()

    def refresh(self):
        super().refresh()
        self._delete_availability_cache()
        self.wait_stable()

    def back(self):
        super().back()
        self._delete_availability_cache()
        self.wait_stable()

    def forward(self):
        super().forward()
        self._delete_availability_cache()
        self.wait_stable()

    @cached_property
    def angular_available(self):
        return self.execute_script('return window.getAllAngularRootElements != undefined;')

    def is_angular_ready(self):
        if not self.angular_available:
            return True
        return self.execute_script(
            'return window.getAllAngularTestabilities().every((testability) => testability.isStable());'
        )

    @cached_property
    def jquery_available(self):
        return self.execute_script('return window.jQuery != undefined;')

    def is_jquery_ready(self):
        if not self.jquery_available:
            return True
        return self.execute_script('return jQuery.active == 0;')

    def is_document_ready(self):
        return self.execute_script("return document.readyState == 'complete'")

    def is_stable(self) -> bool:
        return self.is_document_ready() and self.is_jquery_ready() and self.is_angular_ready()

    def wait_for_stable(self, pause: float = 0.0, poll_rate: float = 0.5, timeout: int = -1) -> None:
        """
        Goes through a series of checks to verify the the web page is ready for use. Selenium does a majority of these
        checks but this additionally checks the status of the document ready state, jQuery and Angular testabilities.

        :param pause: The amount of time in seconds to pause code execution before checking the web page. (Default: 0.0)
        :param poll_rate: How often in seconds to check the state of the web page. (Default: 0.5)
        :param timeout: The amount of time in seconds to wait for the browser to report back as ready. The default time
                        is determined by wait_stable_timeout.
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
        warnings.warn('use driver.js.set_coordinates', DeprecationWarning)
        self.js.set_coordinates(coordinates)

    def get_coordinates(self) -> tuple:
        warnings.warn('use driver.js.get_coordinates', DeprecationWarning)
        return self.js.get_coordinates()

    @property
    def frame(self):
        return self.execute_script('return window.frameElement')

    def get_current_frame(self) -> WebElement:
        """ Gets the current frame. """
        warnings.warn('use driver.frame', DeprecationWarning)
        return self.frame

    def get_timezone_offset(self) -> int:
        """ Gets the timezone offset of the browser in minutes. """
        warnings.warn('use driver.js.get_timezone_offset', DeprecationWarning)
        return self.js.get_timezone_offset()

    @property
    def fullscreen(self) -> bool:
        """ Returns if the window is maximized. """
        return self.execute_script(
            'return window.outerWidth == screen.availWidth && window.outerHeight == screen.availHeight'
        )
