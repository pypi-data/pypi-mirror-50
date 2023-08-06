from wifi import Cell
from os import geteuid
import platform
from pyric import pyw, error as pyric_error


class SsidScanner:
    """
    Used to build a list of nearby WiFi Access Points with enough information to use with the Google Geolocation API.

    """

    def __init__(self, wifi_adapter_name: str = ''):
        if platform.system() != 'Linux':
            raise OSError('Iwlist functionality is required, which is only available on Linux.')
        if geteuid() != 0:
            raise PermissionError('Superuser access is required to list all access points.')

        if wifi_adapter_name == '' or not self.adapter_is_available(wifi_adapter_name):
            self.wifi_adapter_name = self.get_available_adapter()
        else:
            self.wifi_adapter_name = wifi_adapter_name

        self.ssid_list = []
        self.refresh_ssid_list()

    @staticmethod
    def adapter_is_available(wifi_adapter_name: str = '') -> bool:
        """
        See if the specified WiFi interface is connected and enabled.
        :param wifi_adapter_name: str
        :return: bool
        """
        try:
            # Try to create an adapter object relating to the specified adapter name.
            adapter_object = pyw.getcard(wifi_adapter_name)
        except pyric_error:
            # If a pyric_error is thrown, a wireless adapter doesn't exist with the specified name.
            return False

        if not pyw.isup(adapter_object):
            # If the specified adapter is off, return false.
            return False

        return True

    @staticmethod
    def get_available_adapter() -> str:
        """
        Find a WiFi adapter that is connected and enabled.
        :return: string
        """
        wifi_adapter_list = pyw.winterfaces()

        if len(wifi_adapter_list) == 0:
            raise WifiAdapterError('No WiFi interfaces found on the system.')

        for wifi_adapter_name in wifi_adapter_list:
            adapter_object = pyw.getcard(wifi_adapter_name)
            if pyw.isup(adapter_object):
                return wifi_adapter_name

        raise WifiAdapterError('The WiFi adapters are disabled. Please enable them and try again.')

    def refresh_ssid_list(self) -> list:
        """
        Get a list of nearby wifi networks.
        :return: list
        """
        ssids = Cell.all(self.wifi_adapter_name)

        processed_ssids = []
        for ssid in ssids:
            processed_ssids.append({
                'macAddress': ssid.address,
                'signalStrength': ssid.signal,
                'channel': ssid.channel
            })

        self.ssid_list = processed_ssids

        return processed_ssids


class WifiAdapterError(Exception):
    """
    Used to denote an issue with the system's WiFi adapter(s).
    """

    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    wifi_lister = SsidScanner()
    print(wifi_lister.refresh_ssid_list())
