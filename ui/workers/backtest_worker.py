"""Qt worker for executing the pure backtest service off the UI thread."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:

    class BacktestWorker(QtCore.QObject):
        progress = QtCore.pyqtSignal(int, str)
        completed = QtCore.pyqtSignal(dict)
        failed = QtCore.pyqtSignal(str)

        def __init__(self, configuration: dict[str, Any]) -> None:
            super().__init__()
            self.configuration = configuration

        @QtCore.pyqtSlot()
        def run(self) -> None:
            try:
                self.progress.emit(10, "Loading local history…")
                # Import lazily so importing the desktop package never requires
                # SQLAlchemy/PostgreSQL or any web-server dependency.
                backend_root = Path(__file__).resolve().parents[2] / "backend"
                if backend_root.is_dir() and str(backend_root) not in sys.path:
                    sys.path.insert(0, str(backend_root))
                from app.services.backtest_engine import run_backtest

                self.progress.emit(35, "Calculating signals…")
                result = run_backtest(self.configuration)
                self.progress.emit(85, "Calculating metrics…")
                self.completed.emit(result)
            except Exception as exc:
                self.failed.emit(
                    f"Backtest could not be completed: {exc}. "
                    "Check the configuration and optional backend dependencies."
                )

else:

    class BacktestWorker:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create BacktestWorker")
