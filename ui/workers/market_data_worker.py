"""Qt worker for deterministic Phase 3 snapshots."""
from __future__ import annotations

import sys
from pathlib import Path

from ..qt_compat import QT_AVAILABLE, QtCore

if QT_AVAILABLE:
    class MarketDataWorker(QtCore.QThread):
        snapshot_ready = QtCore.pyqtSignal(dict)

        def run(self) -> None:
            backend_root = Path(__file__).resolve().parents[2] / "backend"
            if backend_root.is_dir() and str(backend_root) not in sys.path:
                sys.path.insert(0, str(backend_root))
            from app.services.market_data_aggregator import market_data_aggregator
            import asyncio
            self.snapshot_ready.emit(asyncio.run(market_data_aggregator.snapshot()))
else:
    class MarketDataWorker:  # pragma: no cover
        pass
