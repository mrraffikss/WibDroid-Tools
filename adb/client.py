from __future__ import annotations
from dataclasses import asdict
from .runner import CommandRunner, ToolError

class ADB:
    def __init__(self): self.runner = CommandRunner()
    def command(self, *args): return asdict(self.runner.run(["adb", *args]))
    def devices(self):
        result = self.command("devices", "-l")
        devices = []
        for line in result["stdout"].splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2: devices.append({"serial": parts[0], "status": parts[1], "details": parts[2:]})
        return {"devices": devices, "result": result}
    def shell(self, serial: str | None, command: str):
        args = (["-s", serial] if serial else []) + ["shell", command]
        return self.command(*args)
    def info(self, serial: str | None):
        props = self.shell(serial, "getprop")
        values = {}
        for line in props["stdout"].splitlines():
            if line.startswith("[") and "]: [" in line:
                key, value = line[1:].split("]: [", 1); values[key] = value.rstrip("]")
        return {"properties": values, "result": props}
