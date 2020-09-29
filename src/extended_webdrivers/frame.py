class Frame:
    """ Base class for handling switching to and from iframes using context managers. """

    def __init__(self, child_frame):
        self.driver = child_frame.parent
        assert child_frame.tag_name == 'iframe'
        self.child_frame = child_frame

    def _switch_to(self):
        """ Switches to the specified frame. """
        # Store the parent window and frame to access when we leave the child frame.
        self.parent_window = self.driver.current_window_handle
        self.parent_frame = self.driver.frame

        # Switch to the child frame.
        self.driver.switch_to.frame(self.child_frame)

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
        """ Switches to the previous frame. """
        # Switch to the default window and frame.
        self.driver.switch_to.default_content()

        # Switch to the parent window.
        if self.driver.current_window_handle != self.parent_window:
            self.driver.switch_to.window(self.parent_window)

        # Switch to parent frame if it exists.
        if self.parent_frame is not None:
            self.driver.switch_to.frame(self.parent_frame)

        self.driver.angular = self.driver._test_angular()
        self.driver.jquery = self.driver._test_jquery()

        if self.driver.sync_angular:
            self.driver.wait_for_angular()
        if self.driver.sync_jquery:
            self.driver.wait_for_jquery(self.driver._script_timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
