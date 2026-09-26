from adb.client import ADB

class BatteryMonitor:
    def __init__(self, adb_client=None):
        self.adb = adb_client or ADB()

    def get_battery_info(self, serial=None):
        result = self.adb.shell(serial, 'dumpsys battery')
        battery = {}
        for line in result['stdout'].splitlines():
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                battery[key.strip()] = value.strip()
        return {
            'percentage': battery.get('level', 'N/A'),
            'status': battery.get('status', 'N/A'),
            'temperature': battery.get('temperature', 'N/A'),
            'voltage': battery.get('voltage', 'N/A'),
            'health': battery.get('health', 'N/A'),
        }
