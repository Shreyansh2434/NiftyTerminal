from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:
    class StrategySimulator(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("STRATEGY SIMULATOR · OFFLINE DETERMINISTIC"))
            layout.addWidget(QtWidgets.QLabel("Simulation never routes orders to a broker."))
else:
    class StrategySimulator:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
