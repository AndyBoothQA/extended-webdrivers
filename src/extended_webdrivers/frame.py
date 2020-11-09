class Frame:
    """ Base class for handling switching to and from iframes using context managers. """

    def __init__(self, child_frame):
        self.browser = child_frame.parent
        assert child_frame.tag_name.lower() == 'iframe'
        self.child_frame = child_frame

    def _switch_to(self):
        """ Switches to the specified frame. """
        # Store the parent window and frame to access when we leave the child frame.
        self.parent_window = self.browser.current_window_handle
        self.parent_frame = self.browser.frame

        # Switch to the child frame.
        self.browser.switch_to.frame(self.child_frame)

        self.browser.angular = self.browser._test_angular()
        self.browser.jquery = self.browser._test_jquery()

        if self.browser.sync_angular:
            self.browser.wait_for_angular()
        if self.browser.sync_jquery:
            self.browser.wait_for_jquery(self.browser._script_timeout)

    def __enter__(self):
        self._switch_to()
        return self

    def _switch_from(self):
        """ Switches to the previous frame. """
        # Switch to the default window and frame.
        self.browser.switch_to.default_content()

        # Switch to the parent window.
        if self.browser.current_window_handle != self.parent_window:
            self.browser.switch_to.window(self.parent_window)

        # Switch to parent frame if it exists.
        if self.parent_frame is not None:
            self.browser.switch_to.frame(self.parent_frame)

        self.browser.angular = self.browser._test_angular()
        self.browser.jquery = self.browser._test_jquery()

        if self.browser.sync_angular:
            self.browser.wait_for_angular()
        if self.browser.sync_jquery:
            self.browser.wait_for_jquery(self.browser._script_timeout)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
