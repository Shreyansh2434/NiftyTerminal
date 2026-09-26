"""Main terminal window and its Trading, Backtest and Phase 4 tabs."""

from __future__ import annotations

from pathlib import Path

from ..qt_compat import QT_AVAILABLE, QtCore, QtGui, QtWidgets

if QT_AVAILABLE:
    from ..dialogs.config_dialog import ConfigurationDialog
    from ..dialogs.settings_dialog import SettingsDialog
    from ..widgets.phase3_workspace import Phase3Workspace
    from ..widgets.phase4_widgets import Phase4Workspace
    from ..widgets.global_ticker_widget import GlobalTickerWidget
    from .backtest_window import BacktestWindow


def _stylesheet() -> str:
    path = Path(__file__).parents[1] / "styles" / "terminal_bloomberg.qss"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


if QT_AVAILABLE:

    class MainWindow(QtWidgets.QMainWindow):
        """Application shell with navigation, status and desktop settings."""

        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self.setWindowTitle("NIFTY Options Intelligence Terminal")
            self.setMinimumSize(1100, 720)
            self.resize(1360, 860)
            self.setStyleSheet(_stylesheet())
            self._build_ui()

        def _build_ui(self) -> None:
            shell = QtWidgets.QWidget()
            shell_layout = QtWidgets.QVBoxLayout(shell)
            shell_layout.setContentsMargins(4, 4, 4, 0)
            shell_layout.setSpacing(4)
            shell_layout.addWidget(GlobalTickerWidget(self))
            self.tabs = QtWidgets.QTabWidget()
            self.tabs.setObjectName("mainTabs")
            self.trading_tab = Phase3Workspace(self)
            self.backtest_tab = BacktestWindow(self)
            self.phase4_tab = Phase4Workspace(self)
            self.tabs.addTab(self.trading_tab, "Trading")
            self.tabs.addTab(self.backtest_tab, "Backtest")
            self.tabs.addTab(self.phase4_tab, "Execution / Risk")
            shell_layout.addWidget(self.tabs, 1)
            self.setCentralWidget(shell)

            file_menu = self.menuBar().addMenu("&File")
            quit_action = file_menu.addAction("Quit")
            quit_action.triggered.connect(self.close)
            tools_menu = self.menuBar().addMenu("&Tools")
            config_action = tools_menu.addAction("Backtest configuration…")
            config_action.triggered.connect(self._show_config)
            settings_action = tools_menu.addAction("Settings…")
            settings_action.triggered.connect(self._show_settings)
            help_menu = self.menuBar().addMenu("&Help")
            about_action = help_menu.addAction("About")
            about_action.triggered.connect(self._show_about)
            self.statusBar().showMessage("● PAPER MODE   |   KILL SWITCH ON   |   Data: OFFLINE-DETERMINISTIC   |   Risk: SAFE")

        def _show_config(self) -> None:
            dialog = ConfigurationDialog(self)
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.backtest_tab.apply_configuration(dialog.configuration())
                self.tabs.setCurrentWidget(self.backtest_tab)

        def _show_settings(self) -> None:
            dialog = SettingsDialog(self)
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.setStyleSheet(_stylesheet())

        def _show_about(self) -> None:
            QtWidgets.QMessageBox.about(
                self,
                "About",
                "NIFTY Options Intelligence Terminal\nNative Phase 3 and Phase 4 safety workspaces",
            )

else:

    class MainWindow:  # pragma: no cover - only a dependency-safe import shell
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create MainWindow")
