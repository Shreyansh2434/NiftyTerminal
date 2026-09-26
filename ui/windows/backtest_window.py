"""Backtest tab: configuration, threaded execution and result presentation."""

from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtCore, QtGui, QtWidgets

if QT_AVAILABLE:
    from ..dialogs.config_dialog import ConfigurationDialog
    from ..widgets.backtest_widgets import (
        BacktestConfigWidget,
        BacktestResultsWidget,
    )
    from ..workers.backtest_worker import BacktestWorker


if QT_AVAILABLE:

    class BacktestWindow(QtWidgets.QWidget):
        """Run the pure backtest engine without starting the HTTP server."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self._thread: QtCore.QThread | None = None
            self._worker: BacktestWorker | None = None
            self._build_ui()

        def _build_ui(self) -> None:
            self.config_widget = BacktestConfigWidget(self)
            self.results_widget = BacktestResultsWidget(self)
            self.run_button = QtWidgets.QPushButton("Run backtest")
            self.run_button.setObjectName("primaryButton")
            self.run_button.clicked.connect(self.run_backtest)
            self.progress = QtWidgets.QProgressBar()
            self.progress.setRange(0, 100)
            self.progress.setValue(0)
            self.progress.setTextVisible(True)
            self.progress_label = QtWidgets.QLabel("Ready")
            self.progress_label.setObjectName("mutedLabel")

            left = QtWidgets.QVBoxLayout()
            left.addWidget(self.config_widget)
            left.addWidget(self.run_button)
            left.addWidget(self.progress)
            left.addWidget(self.progress_label)
            left.addStretch()
            left_panel = QtWidgets.QWidget()
            left_panel.setLayout(left)
            left_panel.setMinimumWidth(300)

            splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
            splitter.addWidget(left_panel)
            splitter.addWidget(self.results_widget)
            splitter.setStretchFactor(1, 1)
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(splitter)

        def apply_configuration(self, configuration: dict) -> None:
            self.config_widget.set_configuration(configuration)

        def run_backtest(self) -> None:
            if self._thread is not None and self._thread.isRunning():
                return
            configuration = self.config_widget.configuration()
            self.results_widget.clear_results()
            self.progress.setValue(0)
            self.progress_label.setText("Starting…")
            self.run_button.setEnabled(False)
            self._thread = QtCore.QThread(self)
            self._worker = BacktestWorker(configuration)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.progress.connect(self._on_progress)
            self._worker.completed.connect(self._on_completed)
            self._worker.failed.connect(self._on_failed)
            self._worker.completed.connect(self._thread.quit)
            self._worker.failed.connect(self._thread.quit)
            self._thread.finished.connect(self._thread.deleteLater)
            self._thread.finished.connect(self._worker.deleteLater)
            self._thread.finished.connect(self._thread_finished)
            self._thread.start()

        def _on_progress(self, value: int, message: str) -> None:
            self.progress.setValue(value)
            self.progress_label.setText(message)

        def _on_completed(self, result: dict) -> None:
            self.results_widget.set_results(result)
            self.progress.setValue(100)
            self.progress_label.setText("Completed")

        def _on_failed(self, message: str) -> None:
            self.progress_label.setText("Failed")
            QtWidgets.QMessageBox.warning(self, "Backtest unavailable", message)

        def _thread_finished(self) -> None:
            self.run_button.setEnabled(True)
            self._thread = None
            self._worker = None

        def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # type: ignore[name-defined]
            if self._thread is not None and self._thread.isRunning():
                self._thread.quit()
                self._thread.wait(2000)
            event.accept()

else:

    class BacktestWindow:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create BacktestWindow")
