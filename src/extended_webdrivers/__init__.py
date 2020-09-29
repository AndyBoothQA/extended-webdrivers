"""
Extends the funcionality of the selenium webdriver in Python with additional methods to get the state of jQuery and
Angular calls, change the geolocation of the browser, directly call javascript on elements, and more.
"""

from .android import Android
from .chrome import Chrome
from .edge import Edge
from .extended_webdriver import ExtendedWebdriver
from .firefox import Firefox
from .ie import Ie
from .opera import Opera
from .phantomjs import PhantomJS
from .remote import Remote
from .safari import Safari

__version__ = '0.5'
