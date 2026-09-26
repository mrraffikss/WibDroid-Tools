from adb.client import ADB

class PerformanceMonitor:
    def __init__(self, adb_client=None):
        self.adb = adb_client or ADB()

    def get_memory_info(self, serial=None):
        result = self.adb.shell(serial, 'dumpsys meminfo')
        return {'memory': result['stdout']}

    def get_cpu_info(self, serial=None):
        result = self.adb.shell(serial, 'cat /proc/stat')
        return {'cpu': result['stdout']}
