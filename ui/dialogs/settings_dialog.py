"""Local desktop settings dialog (no server or database settings required)."""

from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:

    class SettingsDialog(QtWidgets.QDialog):
        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self.setWindowTitle("Settings")
            form = QtWidgets.QFormLayout(self)
            self.theme = QtWidgets.QComboBox()
            self.theme.addItems(["Terminal dark"])
            self.refresh_seconds = QtWidgets.QSpinBox()
            self.refresh_seconds.setRange(5, 3600)
            self.refresh_seconds.setValue(60)
            self.offline_mode = QtWidgets.QCheckBox("Prefer offline/local data")
            self.offline_mode.setChecked(True)
            form.addRow("Theme", self.theme)
            form.addRow("Refresh interval (seconds)", self.refresh_seconds)
            form.addRow("", self.offline_mode)
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Save
                | QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(self.accept)
            buttons.rejected.connect(self.reject)
            form.addRow(buttons)

else:

    class SettingsDialog:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create SettingsDialog")
