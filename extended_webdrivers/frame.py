class Frame:
    """ Base class for handling switching to and from iframes using context managers. """

    def __init__(self, child_frame):
        self.browser = child_frame.parent
        assert child_frame.tag_name == 'iframe'
        self.child_frame = child_frame

    def _switch_to(self):
        """ Switches to the specified frame. """
        # Store the parent window and frame to access when we leave the child frame.
        self.parent_window = self.browser.current_window_handle
        self.parent_frame = self.browser.get_current_frame()

        # Switch to the child frame.
        self.browser.switch_to.frame(self.child_frame)

    def __enter__(self):
        self._switch_to()
        return self

    def _switch_from(self):
        """ Switches to the previous frame. """
        # Switch to default frame.
        self.browser.switch_to.window(self.parent_window)

        # Switch to parent frame if it exists.
        if self.parent_frame is not None:
            self.browser.switch_to.frame(self.parent_frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._switch_from()
