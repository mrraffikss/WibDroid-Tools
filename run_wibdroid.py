from __future__ import annotations
import os, shutil, subprocess, sys, webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def tool(name: str) -> str | None:
    candidates = [ROOT / "bin" / (name + (".exe" if os.name == "nt" else "")), Path(shutil.which(name) or "")]
    return next((str(p) for p in candidates if p and p.exists() and p.is_file()), None)

def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Требуется Python 3.11 или новее.")
    try:
        import flask  # noqa: F401
    except ImportError:
        raise SystemExit("Flask не установлен. Выполните: pip install -r requirements.txt")
    adb, fastboot = tool("adb"), tool("fastboot")
    print("========================================\n       WibDroid Tools\n========================================\n")
    print("Local server:\nhttp://127.0.0.1:8765\n")
    print(f"ADB: {'detected' if adb else 'not detected'}")
    print(f"Fastboot: {'detected' if fastboot else 'not detected'}\n")
    print("Press CTRL+C to stop.")
    webbrowser.open("http://127.0.0.1:8765")
    from webapp import app
    app.run(host="127.0.0.1", port=8765, debug=False, threaded=True)

if __name__ == "__main__":
    main()
