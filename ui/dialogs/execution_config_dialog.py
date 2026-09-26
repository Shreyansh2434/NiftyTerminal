from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:
    class ExecutionConfigDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Execution configuration")
            QtWidgets.QVBoxLayout(self).addWidget(QtWidgets.QLabel("Paper broker only. Live connector is not configured."))
else:
    class ExecutionConfigDialog:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
