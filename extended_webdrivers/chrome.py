import json

from selenium.webdriver import Chrome as Chrome_

from .extended_webdriver import ExtendedWebdriver
from .window import Window


class Chrome(Chrome_, ExtendedWebdriver):
    def online(self, **kwargs):
        latency = kwargs.get('latency') or 0
        download_throughput = kwargs.get('download_throughput') or 500 * 1024
        upload_throughput = kwargs.get('download_throughput') or 500 * 1024
        self.set_network_conditions(
            offline=False, latency=latency, download_throughput=download_throughput, upload_throughput=upload_throughput
        )

    def offline(self, **kwargs):
        latency = kwargs.get('latency') or 0
        download_throughput = kwargs.get('download_throughput') or 500 * 1024
        upload_throughput = kwargs.get('download_throughput') or 500 * 1024
        self.set_network_conditions(
            offline=True, latency=latency, download_throughput=download_throughput, upload_throughput=upload_throughput
        )

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
