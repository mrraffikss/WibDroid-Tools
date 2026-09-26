from adb.client import ADB

class NetworkInfo:
    def __init__(self, adb_client=None):
        self.adb = adb_client or ADB()

    def get_network_info(self, serial=None):
        ipv4 = self.adb.shell(serial, 'getprop dhcp.wlan0.ipaddress')
        return {'ipv4': ipv4['stdout'].strip()}
