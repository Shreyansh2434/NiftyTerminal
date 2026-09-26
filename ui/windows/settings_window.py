from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:
    class SettingsWindow(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Terminal settings")
            layout = QtWidgets.QFormLayout(self)
            layout.addRow("Trading mode", QtWidgets.QLabel("PAPER (fixed safe default)"))
            layout.addRow("Kill switch", QtWidgets.QLabel("ON"))
else:
    class SettingsWindow:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
