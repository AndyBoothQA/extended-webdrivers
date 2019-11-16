## Requirements:

* [Selenium webdriver v3.141.0](https://pypi.org/project/selenium/)

## About:

Extends the funcionality of the selenium webdriver in Python with additional methods to get the state of jQuery and Angular calls, change the geolocation of the browser, directly call javascript on elements, and more.

## Usage:

    from extended_webdrivers import load_driver_from_config, DEFAULT_CONFIG

    browser = load_driver_from_config('chrome', DEFAULT_CONFIG)
    browser.get('https://angular.io/')

    browser.wait_for_stable()  # Waits for Angular and jQuery to load before continuing.

    browser.set_cordinates(90.0000, 135.0000)  # Sets the browser's geolcation.