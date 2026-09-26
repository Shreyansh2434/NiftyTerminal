from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:
    class ChartDataWorker(QtCore.QObject):
        finished = QtCore.pyqtSignal(dict)
        def run(self):
            self.finished.emit({"source": "offline-deterministic", "candles": []})
else:
    class ChartDataWorker:  # pragma: no cover
        pass
