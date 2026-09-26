from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path

DANGEROUS_PERMISSIONS = {"READ_SMS", "RECEIVE_SMS", "RECORD_AUDIO", "CAMERA", "ACCESS_FINE_LOCATION", "SYSTEM_ALERT_WINDOW", "REQUEST_INSTALL_PACKAGES"}

def scan_apk(path: str) -> dict:
    file = Path(path)
    if not file.is_file(): raise FileNotFoundError(path)
    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    result = {"file": file.name, "sha256": digest, "size": file.stat().st_size, "format": file.suffix.lower(),
              "status": "UNKNOWN", "warnings": [], "note": "Это эвристическая проверка, не полноценный антивирус."}
    try:
        with zipfile.ZipFile(file) as archive:
            names = set(archive.namelist())
            if "AndroidManifest.xml" not in names: result["warnings"].append("Нет AndroidManifest.xml")
            suspicious = [n for n in names if n.endswith((".dex", ".so")) and len(n) > 180]
            if suspicious: result["warnings"].append("Обнаружены необычно длинные пути в архиве")
            result["status"] = "WARNING" if result["warnings"] else "PASS"
    except zipfile.BadZipFile:
        result["status"] = "ERROR"; result["warnings"].append("Файл не является корректным ZIP/APK")
    return result

def scan_directory(path: str) -> list[dict]:
    return [scan_apk(str(p)) for p in Path(path).rglob("*") if p.suffix.lower() in {".apk", ".apks", ".xapk", ".apkm"}]
