"""Application entry point for the native desktop terminal."""

from __future__ import annotations

import sys

try:
    from .qt_compat import QT_AVAILABLE, missing_qt_message
except ImportError:  # Support `python ui/main.py` and PyInstaller entry points.
    from pathlib import Path

    root = str(Path(__file__).resolve().parents[1])
    if root not in sys.path:
        sys.path.insert(0, root)
    from ui.qt_compat import QT_AVAILABLE, missing_qt_message


def main(argv: list[str] | None = None) -> int:
    """Start the desktop application, or report a friendly dependency error."""

    if not QT_AVAILABLE:
        message = missing_qt_message()
        print(message, file=sys.stderr)
        return 1

    from PyQt6.QtWidgets import QApplication, QMessageBox

    try:
        from .windows.main_window import MainWindow
    except ImportError:
        from ui.windows.main_window import MainWindow

    try:
        app = QApplication(argv or sys.argv)
        app.setApplicationName("NIFTY Options Intelligence Terminal")
        app.setOrganizationName("Trader")
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as exc:  # Do not expose a traceback to desktop users.
        if "app" in locals():
            QMessageBox.critical(None, "Unable to start terminal", str(exc))
        else:
            print(f"Unable to start terminal: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
