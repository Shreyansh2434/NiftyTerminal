"""Headless desktop smoke check.

The check validates import safety without Qt and, when PyQt6 is installed,
constructs the main window with the offscreen platform plugin.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    from ui.qt_compat import QT_AVAILABLE, missing_qt_message

    if not QT_AVAILABLE:
        from ui.main import main as desktop_main

        assert desktop_main([]) == 1
        assert "PyQt6" in missing_qt_message()
        print("Desktop smoke: dependency-free import and graceful error OK")
        return 0

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PyQt6.QtWidgets import QApplication
    from ui.windows.main_window import MainWindow

    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    assert window.tabs.count() == 3
    assert window.tabs.tabText(0) == "Trading"
    assert window.tabs.tabText(1) == "Backtest"
    assert window.tabs.tabText(2) == "Execution / Risk"
    window.close()
    app.processEvents()
    print("Desktop smoke: offscreen window construction OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
