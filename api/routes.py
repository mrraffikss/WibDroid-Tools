from flask import Blueprint, jsonify, request
from adb.client import ADB
from core.runner import ToolError

api = Blueprint("api", __name__)
adb = ADB()

def safe(call):
    try: return jsonify({"ok": True, **call()})
    except ToolError as exc: return jsonify({"ok": False, "error": str(exc), "code": "TOOL_UNAVAILABLE"}), 503
    except Exception as exc: return jsonify({"ok": False, "error": str(exc), "code": "COMMAND_FAILED"}), 400

@api.get("/health")
def health(): return jsonify({"ok": True, "service": "WibDroid Tools", "host": "127.0.0.1"})

@api.get("/devices")
def devices(): return safe(adb.devices)

@api.post("/adb/<action>")
def adb_action(action):
    allowed = {"start": ("start-server",), "stop": ("kill-server",), "restart": ("kill-server",)}
    if action not in allowed: return jsonify({"ok": False, "error": "Недопустимая операция"}), 400
    def run():
        result = adb.command(*allowed[action])
        if action == "restart": result = adb.command("start-server")
        return {"result": result}
    return safe(run)

@api.post("/adb/shell")
def shell():
    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).strip()
    if not command or len(command) > 4096: return jsonify({"ok": False, "error": "Введите команду"}), 400
    return safe(lambda: {"result": adb.shell(data.get("serial"), command)})

@api.get("/device/info")
def info(): return safe(lambda: adb.info(request.args.get("serial")))

@api.get("/packages")
def packages():
    return safe(lambda: {"result": adb.shell(request.args.get("serial"), "pm list packages -3")})
