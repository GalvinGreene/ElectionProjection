#!/usr/bin/env python3
"""One-command launcher.

Usage:
  python start.py

What it does automatically:
1) Creates local virtualenv (.venv) if missing
2) Installs dependencies
3) Initializes DB
4) Seeds demo + map metadata
5) Starts the web app
"""

from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
PYTHON = VENV / "bin" / "python"
PIP = VENV / "bin" / "pip"


def run(cmd: list[str]) -> None:
    print("→", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def ensure_venv() -> None:
    if not PYTHON.exists():
        run([sys.executable, "-m", "venv", str(VENV)])


def main() -> None:
    ensure_venv()
    run([str(PIP), "install", "-r", "requirements.txt"])
    run([str(PYTHON), "-m", "app.tasks.init_db"])
    run([str(PYTHON), "-m", "app.tasks.seed_demo"])
    run([str(PYTHON), "-m", "app.tasks.refresh_data"])
    run([str(PYTHON), "-m", "app.tasks.recompute_models"])

    env = os.environ.copy()
    env.setdefault("FLASK_ENV", "development")
    print("\nDashboard starting at http://127.0.0.1:5000\n")
    subprocess.check_call([str(PYTHON), "run.py"], cwd=ROOT, env=env)


if __name__ == "__main__":
    main()
