from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:
    class ExecutionWorker(QtCore.QObject):
        finished = QtCore.pyqtSignal(dict)
        def run(self):
            self.finished.emit({"status": "paper-ready", "live_orders": 0})
else:
    class ExecutionWorker:  # pragma: no cover
        pass
