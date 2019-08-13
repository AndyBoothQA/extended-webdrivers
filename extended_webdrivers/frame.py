import logging

from selenium.common.exceptions import NoSuchElementException

LOGGER = logging.getLogger('extended_webdrivers')


class Frame:
    """ Base class for handling switching to and from iframes using __enter__ and __exit__. """

    def __init__(self, browser, child_frame):
        self.browser = browser
        self.child_frame = child_frame

    def _switch_to(self):
        """ Switches to the specified frame. """
        # Store the parent window and frame to access when we leave the child frame.
        self.parent_window = self.browser.current_window_handle
        self.parent_frame = self.browser.get_current_frame()

        # Switch to the child frame.
        self.browser.switch_to.frame(self.child_frame)
        self.browser.wait_for_stable(pause=2.0)

        if self.parent_frame != None:
            LOGGER.debug('Switched to frame {} from {}.'.format(
                self.child_frame, self.parent_frame))
        else:
            LOGGER.debug('Switched to frame {}.'.format(self.child_frame))

        # Focuses on the child frame's body element.
        try:
            self.browser.js_focus(
                self.browser.find_element_by_tag_name('body'))
        except NoSuchElementException:
            pass

    def __enter__(self):
        self._switch_to()
        return self

    def _switch_from(self):
        """ Switches to the previous frame. """
        # Switch to default frame.
        self.browser.switch_to.window(self.parent_window)
        self.browser.wait_for_stable(pause=2.0)

        # Switch to parent frame if it exists.
        if self.parent_frame != None:
            self.browser.switch_to.frame(self.parent_frame)
            self.browser.wait_for_stable(pause=2.0)

            LOGGER.debug('Switched to frame {} from {}.'.format(
                self.parent_frame, self.child_frame))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
