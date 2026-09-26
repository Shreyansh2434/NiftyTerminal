from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:
    class StrategyBuilderDialog(QtWidgets.QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Strategy builder")
            QtWidgets.QVBoxLayout(self).addWidget(QtWidgets.QLabel("Build and simulate offline; execution remains paper-only."))
else:
    class StrategyBuilderDialog:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
