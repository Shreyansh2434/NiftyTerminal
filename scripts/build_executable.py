"""Build a distributable Windows executable for the native desktop client.

Usage:
    python scripts/build_executable.py

PyInstaller is intentionally imported only when the build command runs so this
script remains importable in API-only environments.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    pyinstaller = shutil.which("pyinstaller")
    if pyinstaller is None:
        print("PyInstaller is not installed. Run: pip install -r requirements-dev.txt")
        return 1
    command = [
        pyinstaller,
        "--noconfirm",
        "--clean",
        "--name",
        "NiftyTerminal",
        "--windowed",
        "--paths",
        str(ROOT),
        "--add-data",
        f"{ROOT / 'ui' / 'styles'};ui/styles",
        str(ROOT / "ui" / "main.py"),
    ]
    print("Building native desktop executable…")
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
