"""Offline-safe Bloomberg-style Phase 3 desktop workspace."""
from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtWidgets

if QT_AVAILABLE:

    class Phase3Workspace(QtWidgets.QWidget):
        def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
            super().__init__(parent)
            self._build()

        def _panel(self, title: str, body: str) -> QtWidgets.QFrame:
            frame = QtWidgets.QFrame()
            frame.setObjectName("bloombergPanel")
            layout = QtWidgets.QVBoxLayout(frame)
            heading = QtWidgets.QLabel(title.upper())
            heading.setObjectName("panelHeading")
            layout.addWidget(heading)
            text = QtWidgets.QLabel(body)
            text.setWordWrap(True)
            text.setObjectName("panelBody")
            layout.addWidget(text)
            return frame

        def _build(self) -> None:
            root = QtWidgets.QHBoxLayout(self)
            root.setContentsMargins(0, 0, 0, 0)
            sidebar = QtWidgets.QFrame()
            sidebar.setObjectName("marketSidebar")
            side = QtWidgets.QVBoxLayout(sidebar)
            brand = QtWidgets.QLabel("MARKET\nTERMINAL")
            brand.setObjectName("sidebarBrand")
            side.addWidget(brand)
            side.addWidget(QtWidgets.QLabel("MARKET NAVIGATOR", objectName="sectionLabel"))
            for name in ("Overview", "Heatmap", "Sentiment", "Sectors", "Markets", "Portfolio / Risk", "Strategy Lab"):
                button = QtWidgets.QPushButton(name)
                button.setObjectName("navButton")
                side.addWidget(button)
            side.addStretch()
            side.addWidget(QtWidgets.QLabel("OFFLINE MODE • DETERMINISTIC", objectName="offlineLabel"))
            root.addWidget(sidebar)

            content = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(content)
            ticker = QtWidgets.QFrame()
            ticker.setObjectName("globalTicker")
            ticker_layout = QtWidgets.QHBoxLayout(ticker)
            ticker_layout.addWidget(QtWidgets.QLabel("GLOBAL TICKER", objectName="tickerLabel"))
            for symbol, value, change in (("NIFTY", "22,184.60", "+0.42%"), ("BANKNIFTY", "47,332.15", "+0.18%"), ("USDINR", "83.12", "-0.06%"), ("VIX", "13.48", "-1.20%")):
                label = QtWidgets.QLabel(f"{symbol}  {value}  {change}")
                label.setObjectName("tickerPositive" if "+" in change else "tickerNegative")
                ticker_layout.addWidget(label)
            ticker_layout.addStretch()
            layout.addWidget(ticker)
            title = QtWidgets.QLabel("PHASE 3 · MULTI-ASSET INTELLIGENCE")
            title.setObjectName("pageTitle")
            layout.addWidget(title)
            grid = QtWidgets.QGridLayout()
            grid.addWidget(self._panel("Market heatmap", "IT  +1.24%   FINANCIALS  +0.68%   AUTO  −0.21%\nRELIANCE  +0.92%   TCS  +1.48%   INFY  +1.06%"), 0, 0)
            grid.addWidget(self._panel("AI analyst", "RISK-ON  ·  0.74 confidence\nBreadth 7/10 advancing. Technology leads; volatility remains contained.\nRule-based research aid; not financial advice."), 0, 1)
            grid.addWidget(self._panel("Sentiment monitor", "BULLISH  +0.33\nInstitutional inflow supports strong market breadth\nTechnology earnings growth remains resilient"), 1, 0)
            grid.addWidget(self._panel("Sector performance", "IT       +1.27%   2/2 advancing\nFINANCIALS +0.42%  3/3 advancing\nHEALTHCARE +0.18%  1/1 advancing\nAUTO     −0.21%   0/1 advancing"), 1, 1)
            grid.addWidget(self._panel("Portfolio / risk", "Exposure 62%   Cash 38%\nBeta 0.86   VaR (95%) 1.42%\nDrawdown 0.0%   Regime: TRENDING"), 2, 0)
            grid.addWidget(self._panel("Economic & news", "RBI policy — next event\nUS CPI — monitor rates\nOffline headlines are deterministic and clearly labelled."), 2, 1)
            layout.addLayout(grid)
            lab = QtWidgets.QGroupBox("MULTI-ASSET BACKTEST / STRATEGY LAB")
            form = QtWidgets.QHBoxLayout(lab)
            form.addWidget(QtWidgets.QLabel("Strategy"))
            strategy = QtWidgets.QComboBox()
            strategy.addItems(["Equal-weight momentum", "Sector rotation", "Volatility target"])
            form.addWidget(strategy)
            form.addWidget(QtWidgets.QLabel("Universe: NIFTY 50"))
            run = QtWidgets.QPushButton("Run offline backtest")
            run.setObjectName("accentButton")
            result = QtWidgets.QLabel("Ready · aggregate / per-asset / per-sector / per-regime metrics")
            result.setObjectName("mutedLabel")
            run.clicked.connect(lambda: result.setText("Completed · +8.42% return · Sharpe 1.18 · max DD 3.2%"))
            form.addWidget(run)
            form.addWidget(result, 1)
            layout.addWidget(lab)
            layout.addStretch()
            root.addWidget(content, 1)

else:

    class Phase3Workspace:  # pragma: no cover
        def __init__(self, *_args, **_kwargs) -> None:
            raise RuntimeError("PyQt6 is required to create Phase3Workspace")
