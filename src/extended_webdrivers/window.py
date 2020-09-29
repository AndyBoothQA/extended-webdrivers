from selenium.common.exceptions import NoSuchFrameException, NoSuchWindowException, StaleElementReferenceException


class NoNewWindow(Exception):
    """ Thrown when the outermost window is the same as the current window. """

    pass


class Window:
    """ Base class for handling switching to and from different windows __enter__ and __exit__. """

    def __init__(self, driver, child_window=None, parent_window=None, close_on_exit=True, remember_frame=True):
        self.driver = driver
        self.child_window = child_window
        self.parent_window = parent_window
        self.close_on_exit = close_on_exit
        self.remember_frame = remember_frame

    def _switch_to(self):
        """ Switches to the specified window if defined, otherwise the top-most window. """
        # Store the parent window and frame to access when we leave the child window.
        if not self.parent_window:
            self.parent_window = self.driver.current_window_handle
        self.current_frame = self.driver.frame

        # If the child window isn't defined, set it to the outermost window.
        if not self.child_window:
            self.child_window = self.driver.window_handles[-1]

        # Check if the child window is the same as the current window.
        if self.child_window == self.parent_window:
            raise NoNewWindow(self.child_window)

        # Switch to the child window.
        self.driver.switch_to.window(self.child_window)

        self.driver.angular = self.driver._test_angular()
        self.driver.jquery = self.driver._test_jquery()

        if self.driver.sync_angular:
            self.driver.wait_for_angular()
        if self.driver.sync_jquery:
            self.driver.wait_for_jquery(self.driver._script_timeout)

    def __enter__(self):
        self._switch_to()
        return self

    def _switch_from(self):
        """ Switches to the previous window and frame. """
        try:
            # Closes the window if it is still open.
            try:
                if self.close_on_exit and self.driver.current_window_handle != self.parent_window:
                    self.driver.close()
            except NoSuchWindowException:
                pass

            # Switches to the parent window.
            self.driver.switch_to.window(self.parent_window)

            # Switches to the original frame if it's still valid.
            if self.remember_frame and self.current_frame:
                try:
                    self.driver.switch_to.frame(self.current_frame)
                except (NoSuchFrameException, StaleElementReferenceException):
                    pass
        except NoSuchWindowException:
            # Switches to default content if somehow the parent window was closed.
            self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.angular = self.driver._test_angular()
        self.driver.jquery = self.driver._test_jquery()

        if self.driver.sync_angular:
            self.driver.wait_for_angular()
        if self.driver.sync_jquery:
            self.driver.wait_for_jquery(self.driver._script_timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
