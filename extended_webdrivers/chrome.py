import json

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome as Chrome_

from .extended_webdriver import ExtendedWebdriver
from .window import Window


class Chrome(Chrome_, ExtendedWebdriver):
    def is_online(self):
        try:
            network_conditions = self.get_network_conditions()
            return network_conditions['offline'] is False
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

    def send_cmd(self, cmd, params):
        resource = f'/session/{self.session_id}/chromium/send_command_and_get_result'
        url = self.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = self.command_executor._request('POST', url, body)
        return response.get('value')


class OnlineContextManager:
    def __init__(self, driver):
        self.driver = driver

    def _go_online(self, **kwargs):
        latency = kwargs.get('latency') or 0
        download_throughput = kwargs.get('download_throughput') or 500 * 1024
        upload_throughput = kwargs.get('download_throughput') or 500 * 1024
        self.driver.set_network_conditions(
            offline=False, latency=latency, download_throughput=download_throughput, upload_throughput=upload_throughput
        )

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
        latency = kwargs.get('latency') or 0
        download_throughput = kwargs.get('download_throughput') or 500 * 1024
        upload_throughput = kwargs.get('download_throughput') or 500 * 1024
        self.driver.set_network_conditions(
            offline=True, latency=latency, download_throughput=download_throughput, upload_throughput=upload_throughput
        )

    def __call__(self, **kwargs):
        self._go_offline(**kwargs)

    def __enter__(self):
        self.driver.offline()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.online()
