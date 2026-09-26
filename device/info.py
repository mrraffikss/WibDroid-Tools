from adb.client import ADB

class DeviceInfoCollector:
    def __init__(self, adb_client=None):
        self.adb = adb_client or ADB()

    def get_all_info(self, serial=None):
        info = self.adb.info(serial)
        props = info.get('properties', {})
        return {
            'manufacturer': props.get('ro.product.manufacturer', 'N/A'),
            'model': props.get('ro.product.model', 'N/A'),
            'device': props.get('ro.product.device', 'N/A'),
            'serial': props.get('ro.serialno', 'N/A'),
            'android_version': props.get('ro.build.version.release', 'N/A'),
            'api_level': props.get('ro.build.version.sdk', 'N/A'),
            'build_id': props.get('ro.build.id', 'N/A'),
            'fingerprint': props.get('ro.build.fingerprint', 'N/A'),
            'security_patch': props.get('ro.build.version.security_patch', 'N/A'),
        }
