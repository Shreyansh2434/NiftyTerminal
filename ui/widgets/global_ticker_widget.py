"""Always-visible market ticker for the native terminal shell."""
from __future__ import annotations

from datetime import datetime

from ..qt_compat import QT_AVAILABLE, QtCore, QtWidgets

if QT_AVAILABLE:

    class GlobalTickerWidget(QtWidgets.QFrame):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setObjectName("globalTicker")
            layout = QtWidgets.QHBoxLayout(self)
            layout.setContentsMargins(8, 2, 8, 2)
            layout.setSpacing(12)
            brand = QtWidgets.QLabel("AURORA TERMINAL")
            brand.setObjectName("tickerBrand")
            layout.addWidget(brand)
            for symbol, value, change, positive in (
                ("NIFTY", "23,398.60", "+0.42%", True),
                ("BANKNIFTY", "47,332.15", "+0.18%", True),
                ("USDINR", "83.12", "-0.06%", False),
                ("VIX", "13.48", "-1.20%", False),
            ):
                label = QtWidgets.QLabel(f"{symbol} {value} {change}")
                label.setObjectName("tickerPositive" if positive else "tickerNegative")
                label.setToolTip(f"<b>{symbol}</b><br>Last: {value}<br>Change: {change}<br><span style='color:#a0a0a0'>Offline deterministic snapshot</span>")
                layout.addWidget(label)
            layout.addStretch()
            self.clock = QtWidgets.QLabel()
            self.clock.setObjectName("tickerClock")
            layout.addWidget(self.clock)
            self._timer = QtCore.QTimer(self)
            self._timer.timeout.connect(self._update_clock)
            self._timer.start(1000)
            self._update_clock()

        def _update_clock(self) -> None:
            self.clock.setText(datetime.now().astimezone().strftime("%H:%M:%S %Z"))

else:
    class GlobalTickerWidget:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
