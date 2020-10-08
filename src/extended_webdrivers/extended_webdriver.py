import logging
import time
from urllib.parse import urljoin

from selenium.common.exceptions import JavascriptException
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.wait import WebDriverWait, POLL_FREQUENCY

from .js import Js

LOGGER = logging.getLogger(__name__)

COMMANDS_NEEDING_WAIT = [
    Command.CLICK_ELEMENT,
    Command.SEND_KEYS_TO_ELEMENT,
    Command.GET_CURRENT_URL,
    Command.GET_PAGE_SOURCE,
    Command.GET_TITLE,
    Command.GET_ELEMENT_TAG_NAME,
    Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY,
    Command.GET_ELEMENT_ATTRIBUTE,
    Command.GET_ELEMENT_TEXT,
    Command.GET_ELEMENT_SIZE,
    Command.GET_ELEMENT_LOCATION,
    Command.IS_ELEMENT_ENABLED,
    Command.IS_ELEMENT_SELECTED,
    Command.IS_ELEMENT_DISPLAYED,
    Command.SUBMIT_ELEMENT,
    Command.CLEAR_ELEMENT,
    Command.FIND_ELEMENT,
    Command.FIND_ELEMENTS,
    Command.FIND_CHILD_ELEMENT,
    Command.FIND_CHILD_ELEMENTS,
]

COMMANDS_NEEDING_RESYNC = [
    Command.SWITCH_TO_CONTEXT,
    Command.SWITCH_TO_FRAME,
    Command.SWITCH_TO_PARENT_FRAME,
    Command.SWITCH_TO_WINDOW,
    Command.GET,
    Command.REFRESH,
    Command.GO_BACK,
    Command.GO_FORWARD
]


class ExtendedWebdriver:
    """ Mixin class that extends a webdriver instance with additional methods. """

    def __init__(self, base_url=None, sync_angular=True, sync_jquery=True, sync_document=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.js = Js(self)
        self.base_url = base_url
        self.sync_angular = sync_angular
        self.sync_jquery = sync_jquery
        self.sync_document = sync_document
        self._script_timeout = 30  # I believe this is the default timeout.
        self.angular = self._test_angular()
        self.jquery = self._test_jquery()

    def execute(self, driver_command, params=None):
        if driver_command in COMMANDS_NEEDING_WAIT:
            if self.sync_angular:
                self.wait_for_angular()
            if self.sync_jquery:
                self.wait_for_jquery(self._script_timeout)
            if self.sync_document:
                self.wait_for_document(self._script_timeout)
            return super().execute(driver_command, params=params)
        result = super().execute(driver_command, params=params)
        if driver_command in COMMANDS_NEEDING_RESYNC:
            self.angular = self._test_angular()
            self.jquery = self._test_jquery()
        return result

    def get(self, url):
        if (self.base_url and self.base_url in url) or not self.base_url:
            super().get(url)
        else:
            super().get(urljoin(str(self.base_url), str(url)))

    def set_script_timeout(self, time_to_wait):
        super().set_script_timeout(time_to_wait)
        self._script_timeout = time_to_wait

    def _test_angular(self):
        try:
            return self.execute_script('return window.getAllAngularRootElements != undefined;')
        except JavascriptException:
            return False

    def is_angular_ready(self):
        if not self.angular:
            return True
        script = 'return window.getAllAngularTestabilities().every((t) => t.isStable());'
        try:
            return self.execute_script(script)
        except JavascriptException:
            self._test_angular()
            return True

    def wait_for_angular(self):
        if self.angular:
            script = '''var cb = arguments[arguments.length - 1];
Promise.all(window.getAllAngularTestabilities().map(t => { 
    return new Promise(resolve => {
        return t.whenStable(resolve);
    })
})).then(cb);'''
            try:
                self.execute_async_script(script)
            except JavascriptException:
                self._test_angular()

    def _test_jquery(self):
        return self.execute_script('return window.jQuery != undefined;')

    def is_jquery_ready(self):
        if not self.jquery:
            return True
        try:
            return self.execute_script('return jQuery.active == 0;')
        except JavascriptException:
            self._test_jquery()
            return True

    def wait_for_jquery(self, timeout):
        if self.jquery:
            try:
                WebDriverWait(self, timeout).until(lambda d: d.execute_script('return jQuery.active == 0;'))
            except JavascriptException:
                self._test_jquery()

    def is_document_ready(self):
        return self.execute_script("return document.readyState == 'complete'")

    def wait_for_document(self, timeout):
        WebDriverWait(self, timeout).until(lambda d: d.execute_script("return document.readyState == 'complete';"))

    def is_stable(self) -> bool:
        return self.is_document_ready() and self.is_jquery_ready() and self.is_angular_ready()

    def wait_for_stable(
        self, pause: float = 0.0, poll_frequency: float = POLL_FREQUENCY, timeout: (None, int) = None
    ) -> None:
        """
        Goes through a series of checks to verify the the web page is ready for use. Selenium does a majority of these
        checks but this additionally checks the status of the document ready state, jQuery and Angular testabilities.

        :param pause: The amount of time in seconds to pause code execution before checking the web page. (Default: 0.0)
        :param poll_frequency: How often in seconds to check the state of the web page. (Default: 0.5)
        :param timeout: The amount of time in seconds to wait for the browser to report back as ready. The default time
                        is determined by the current script timeout.
        """

        if timeout is None:
            timeout = self._script_timeout
        time.sleep(pause)
        WebDriverWait(self, timeout, poll_frequency).until(
            lambda d: d.is_angular_ready() and d.is_jquery_ready() and d.is_document_ready()
        )

    wait_stable = wait_for_stable

    @property
    def frame(self):
        return self.execute_script('return window.frameElement')

    @property
    def fullscreen(self) -> bool:
        """ Returns if the window is maximized. """
        script = 'return window.outerWidth == screen.availWidth && window.outerHeight == screen.availHeight'
        return self.execute_script(script)
