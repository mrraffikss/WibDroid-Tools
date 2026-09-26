from adb.client import ADB

class ProcessManager:
    def __init__(self, adb_client=None):
        self.adb = adb_client or ADB()

    def list_processes(self, serial=None):
        result = self.adb.shell(serial, 'ps')
        return {'processes': result['stdout']}
