from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome as _Chrome

from .extended_webdriver import ExtendedWebdriver
from .window import Window


class ExtendedChromeMixin(ExtendedWebdriver):
    def is_online(self):
        try:
            return self.get_network_conditions()['offline'] is False
        except WebDriverException:
            return True

    def is_offline(self):
        return not self.is_online()

    def is_open(self):
        try:
            return self.current_url is not None
        except WebDriverException:
            return False

    @property
    def online(self):
        return OnlineContextManager(self)

    @property
    def offline(self):
        return OfflineContextManager(self)

    def get_default_zoom(self):
        """ EXPERIMENTAL - Get the current default zoom level. """
        self.execute_script('window.open()')
        with Window(self):
            self.get('chrome://settings/')
            result = self.execute_async_script(
                '''var callback = arguments[arguments.length - 1];
            chrome.settingsPrivate.getDefaultZoom(function(e) {
                callback(e)
            })
            '''
            )
            self.close()
            return float(result)

    def set_default_zoom(self, percent):
        """ EXPERIMENTAL - Set the current default zoom level. """
        self.execute_script('window.open()')
        with Window(self):
            self.get('chrome://settings/')
            self.execute_script(f'chrome.settingsPrivate.setDefaultZoom({percent / 100});')
            self.close()

    def reset_default_zoom(self):
        """ EXPERIMENTAL - Resets the default zoom level. """
        self.set_default_zoom(100)


class Chrome(ExtendedChromeMixin):
    def is_online(self):
        try:
            return self.get_network_conditions()['offline'] is False
        except WebDriverException:
            return True

    def is_offline(self):
        return not self.is_online()

    def is_open(self):
        try:
            return self.current_url is not None
        except WebDriverException:
            return False

    @property
    def online(self):
        return OnlineContextManager(self)

    @property
    def offline(self):
        return OfflineContextManager(self)

    def get_default_zoom(self):
        """ EXPERIMENTAL - Get the current default zoom level. """
        self.execute_script('window.open()')
        with Window(self):
            self.get('chrome://settings/')
            result = self.execute_async_script(
                '''var callback = arguments[arguments.length - 1];
            chrome.settingsPrivate.getDefaultZoom(function(e) {
                callback(e)
            })
            '''
            )
            self.close()
            return float(result)

    def set_default_zoom(self, percent):
        """ EXPERIMENTAL - Set the current default zoom level. """
        self.execute_script('window.open()')
        with Window(self):
            self.get('chrome://settings/')
            self.execute_script(f'chrome.settingsPrivate.setDefaultZoom({percent / 100});')
            self.close()

    def reset_default_zoom(self):
        """ EXPERIMENTAL - Resets the default zoom level. """
        self.set_default_zoom(100)


class OnlineContextManager:
    def __init__(self, driver):
        self.driver = driver

    def _go_online(self, **kwargs):
        self.driver.set_network_conditions(offline=False, latency=0, throughput=0)

        # Angular takes a very short amount of time (about 8 hundredths of a second) to report back as not ready after
        # setting the browser online if when there are pending HTTP requests. Adding a small pause allows Angular to
        # report accurately.
        self.driver.wait_stable(0.5)

    def __call__(self, **kwargs):
        self._go_online(**kwargs)

    def __enter__(self):
        self._was_offline = self.driver.is_offline()
        self.driver.online()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if getattr(self, '_was_offline'):
            self.driver.offline()


class OfflineContextManager:
    def __init__(self, driver):
        self.driver = driver

    def _go_offline(self, **kwargs):
        self.driver.set_network_conditions(offline=True, latency=0, throughput=0)

    def __call__(self, **kwargs):
        self._go_offline(**kwargs)

    def __enter__(self):
        self.driver.offline()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.online()
