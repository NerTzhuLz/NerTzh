#!/usr/bin/env python3
"""Validate PyCharm run modes (same env as .idea/runConfigurations)."""
from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "bin" / "python"
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}


def ok(label: str) -> None:
    print(f"  OK  {label}")


def fail(label: str, detail: str = "") -> None:
    msg = f"  FAIL {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    raise SystemExit(1)


def check_file(path: Path, label: str) -> None:
    if not path.exists():
        fail(label, f"missing {path}")
    ok(label)


def check_pg(host: str = "127.0.0.1", port: int = 5433) -> None:
    try:
        with socket.create_connection((host, port), timeout=2.0):
            pass
    except OSError as e:
        fail("Postgres metrics-pg :5433", str(e))
    ok(f"Postgres {host}:{port}")


def run_cmd(label: str, args: list[str], *, timeout: float = 120.0) -> None:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()[-500:]
        fail(label, err)
    ok(label)


def main() -> None:
    print("PyCharm env validation — _Metrics_")
    print(f"root={ROOT}")

    check_file(PY, ".venv interpreter")
    check_file(ROOT / ".env", ".env")
    check_file(ROOT / "src" / "nertzh.py", "nertzh.py")
    check_file(ROOT / "src" / "api_app.py", "api_app.py")
    check_pg()

    run_cmd(
        "import settings.ConfigSettings",
        [str(PY), "-c", "from settings import ConfigSettings; ConfigSettings(); print('ok')"],
        timeout=30,
    )
    run_cmd(
        "import api_app",
        [str(PY), "-c", "import api_app; print(api_app.app.title)"],
        timeout=30,
    )
    run_cmd(
        "Tests (unittest)",
        [str(PY), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
        timeout=60,
    )
    run_cmd(
        "Bridge Status",
        [str(PY), str(ROOT / "scripts" / "bridge.py"), "status"],
        timeout=30,
    )
    run_cmd(
        "Readiness (make check)",
        ["/bin/bash", "-lc", f"cd {ROOT} && make check"],
        timeout=60,
    )

    print("\nAll PyCharm run modes validated.")


if __name__ == "__main__":
    main()