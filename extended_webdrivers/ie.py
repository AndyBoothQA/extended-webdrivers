from selenium.webdriver import Ie as _Ie

from .extended_webdriver import ExtendedWebdriver


class Ie(ExtendedWebdriver, _Ie):
    def __init__(self, restricted_mode=False, **kwargs):
        import winreg

        for zone in range(1, 5):
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                f'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\{zone}',
                0,
                winreg.KEY_ALL_ACCESS,
            )
            if restricted_mode:
                winreg.SetValueEx(key, '2500', 1, winreg.REG_DWORD, 0)
            else:
                winreg.SetValueEx(key, '2500', 1, winreg.REG_DWORD, 3)
        super().__init__(**kwargs)
