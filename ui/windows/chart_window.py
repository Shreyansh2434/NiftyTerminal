from ..qt_compat import QT_AVAILABLE, QtWidgets
from ..widgets.advanced_chart_widget import AdvancedChartWidget

if QT_AVAILABLE:
    class ChartWindow(QtWidgets.QMainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Phase 4 Chart")
            self.setCentralWidget(AdvancedChartWidget())
else:
    class ChartWindow:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
