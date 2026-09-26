from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:
    class AlertConfigDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Alert configuration")
            QtWidgets.QVBoxLayout(self).addWidget(QtWidgets.QLabel("Alerts are local and deterministic."))
else:
    class AlertConfigDialog:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
