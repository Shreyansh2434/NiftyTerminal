from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:
    class CloudSyncWorker(QtCore.QObject):
        finished = QtCore.pyqtSignal(dict)
        def run(self):
            self.finished.emit({"status": "disabled", "reason": "offline-safe by default"})
else:
    class CloudSyncWorker:  # pragma: no cover
        pass
