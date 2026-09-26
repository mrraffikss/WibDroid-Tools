from __future__ import annotations
import os, shutil, subprocess, threading
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CommandResult:
    command: list[str]
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool = False

class ToolError(RuntimeError): pass

class CommandRunner:
    def __init__(self, root: Path | None = None, timeout: int = 30):
        self.root = root or Path(__file__).resolve().parents[1]
        self.timeout = timeout
        self._processes: set[subprocess.Popen] = set()
        self._lock = threading.Lock()

    def executable(self, name: str) -> str | None:
        filename = name + (".exe" if os.name == "nt" else "")
        bundled = self.root / "bin" / filename
        return str(bundled) if bundled.is_file() else shutil.which(name)

    def run(self, args: list[str], timeout: int | None = None) -> CommandResult:
        if not args: raise ValueError("Пустая команда")
        executable = self.executable(args[0])
        if not executable: raise ToolError(f"{args[0]} не найден в bin/ или PATH")
        command = [executable, *args[1:]]
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    encoding="utf-8", errors="replace", start_new_session=True)
            with self._lock: self._processes.add(proc)
            try:
                out, err = proc.communicate(timeout=timeout or self.timeout)
                return CommandResult(args, out, err, proc.returncode)
            except subprocess.TimeoutExpired:
                proc.kill(); out, err = proc.communicate()
                return CommandResult(args, out, err, -1, True)
            finally:
                with self._lock: self._processes.discard(proc)
        except OSError as exc: raise ToolError(str(exc)) from exc
