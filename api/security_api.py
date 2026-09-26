from flask import Blueprint, jsonify, request
from security.scanner import scan_apk
from pathlib import Path
import tempfile

security_api = Blueprint("security_api", __name__)

@security_api.post("/scan")
def scan():
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename: return jsonify({"ok": False, "error": "Файл не выбран"}), 400
    suffix = Path(uploaded.filename).suffix.lower()
    if suffix not in {".apk", ".apks", ".xapk", ".apkm"}: return jsonify({"ok": False, "error": "Поддерживаются APK/APKS/XAPK/APKM"}), 400
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
        uploaded.save(handle.name)
    try: return jsonify({"ok": True, "scan": scan_apk(handle.name)})
    finally: Path(handle.name).unlink(missing_ok=True)
