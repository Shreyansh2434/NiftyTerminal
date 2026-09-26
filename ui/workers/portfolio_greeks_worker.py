from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:
    class PortfolioGreeksWorker(QtCore.QObject):
        finished = QtCore.pyqtSignal(dict)
        def run(self):
            self.finished.emit({"greeks": {"delta": 0.86}, "var_95": 0.012})
else:
    class PortfolioGreeksWorker:  # pragma: no cover
        pass
