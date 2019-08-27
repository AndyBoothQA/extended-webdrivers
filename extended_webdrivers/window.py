import logging

from selenium.common.exceptions import (NoAlertPresentException,
                                        NoSuchElementException,
                                        NoSuchFrameException,
                                        NoSuchWindowException,
                                        StaleElementReferenceException)

LOGGER = logging.getLogger('extended_webdrivers')


class Window:
    """ Base class for handling switching to and from different windows __enter__ and __exit__. """

    def __init__(self,
                 browser,
                 child_window=None,
                 close_on_exit=True,
                 remember_frame=True):
        self.browser = browser
        self.child_window = child_window
        self.close_on_exit = close_on_exit
        self.remember_frame = remember_frame

    def _switch_to(self):
        """ Switches to the specified window if defined, otherwise the top-most window. """
        # Store the parent window and frame to access when we leave the child window.
        self.parent_window = self.browser.current_window_handle
        self.current_frame = self.browser.get_current_frame()

        # If the child window isn't defined, set it to the outermost window.
        if not self.child_window:
            self.child_window = self.browser.window_handles[-1]

        # Switch to the child window.
        self.browser.switch_to.window(self.child_window)
        self.browser.wait_for_stable(pause=2.0)

        LOGGER.debug('Switched to window {} from {}.'.format(
            self.child_window, self.parent_window))

        # Focuses on the window's body element.
        try:
            self.browser.js.focus(
                self.browser.find_element_by_tag_name('body'))
        except NoSuchElementException:
            pass

    def __enter__(self):
        self._switch_to()
        return self

    def _switch_from(self):
        """ Switches to the previous window and frame. """
        try:
            # Closes the window if it is still open.
            try:
                if self.close_on_exit and self.browser.current_window_handle != self.parent_window:
                    self.browser.close()
            except NoSuchWindowException:
                pass

            # Switches to the parent window.
            self.browser.switch_to.window(self.parent_window)
            self.browser.wait_for_stable(pause=2.0)

            LOGGER.debug('Switched to window {} from {}.'.format(
                self.parent_window, self.child_window))

            # Switches to the original frame if it's still valid.
            if self.remember_frame and self.current_frame:
                try:
                    self.browser.switch_to.frame(self.current_frame)
                except (NoSuchFrameException, StaleElementReferenceException):
                    pass
                else:
                    LOGGER.debug('Switched to frame {}.'.format(
                        self.current_frame))
        except NoSuchWindowException:
            # Switches to default content if somehow the parent window was closed.
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.wait_for_stable(pause=2.0)

            LOGGER.debug('Switched to window {} from {}.'.format(
                self.browser.current_window_handle, self.child_window))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
