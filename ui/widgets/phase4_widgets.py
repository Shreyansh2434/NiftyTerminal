"""Dense offline-safe Phase 4 desktop panels."""
from __future__ import annotations

from ..qt_compat import QT_AVAILABLE, QtWidgets
from .base_widgets import DenseCard, DenseDataTable, MetricRow

if QT_AVAILABLE:

    class Phase4Panel(DenseCard):
        def __init__(self, title: str, body: str, parent=None):
            super().__init__(title, parent)
            text = QtWidgets.QLabel(body)
            text.setWordWrap(True)
            text.setObjectName("panelBody")
            self.content_layout.addWidget(text)

    class AdvancedChartWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Advanced chart", "NIFTY 23,398.60  |  1D  |  MA20  |  RSI\nCandles, VWAP and market profile are offline-safe.", parent)

    class VolumeProfileWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Volume profile", "POC 23,400  |  VAH 23,450  |  VAL 23,350\nBuy / sell volume buckets available.", parent)

    class OrderFlowWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Order flow", "Delta +1,840  |  buy imbalance 57%\nNo live feed is requested by this widget.", parent)

    class PortfolioGreeksWidget(DenseCard):
        def __init__(self, parent=None):
            super().__init__("Portfolio / Greeks", parent)
            for row in (
                MetricRow("DELTA", "+0.86", True, self),
                MetricRow("GAMMA", "0.0003", None, self),
                MetricRow("VEGA", "+0.21", True, self),
                MetricRow("THETA", "-0.05", False, self),
                MetricRow("VAR 95%", "-3.2L", False, self),
            ):
                self.content_layout.addWidget(row)

    class ExecutionDashboardWidget(DenseCard):
        def __init__(self, parent=None):
            super().__init__("Execution dashboard", parent)
            self.content_layout.addWidget(QtWidgets.QLabel("PAPER BROKER ONLY", objectName="metricPositive"))
            table = DenseDataTable(["SYMBOL", "SIDE", "QTY", "STATUS"], self)
            table.setRowCount(1)
            for column, value in enumerate(("NIFTY", "BUY", "1", "READY")):
                table.setItem(0, column, QtWidgets.QTableWidgetItem(value))
            self.content_layout.addWidget(table)
            self.content_layout.addWidget(QtWidgets.QLabel("Preview and idempotent paper fills; live connector unavailable.", objectName="panelBody"))

    class CompliancePanelWidget(DenseCard):
        def __init__(self, parent=None):
            super().__init__("Compliance / Audit", parent)
            self.content_layout.addWidget(MetricRow("AUDIT TRAIL", "ENABLED", True, self))
            self.content_layout.addWidget(MetricRow("LIVE ORDERS", "0", None, self))
            self.content_layout.addWidget(MetricRow("CHECKS", "ALL PASS", True, self))
            actions = QtWidgets.QHBoxLayout()
            actions.addWidget(QtWidgets.QPushButton("Export CSV", objectName="compactButton"))
            actions.addWidget(QtWidgets.QPushButton("Export JSON", objectName="compactButton"))
            self.content_layout.addLayout(actions)

    class RiskDashboardWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Risk dashboard", "KILL SWITCH: ON  |  max notional 100,000\nKelly sizing, limits and stress scenarios.", parent)

    class MarketScannerWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Market scanner", "NIFTY  +0.42%  |  BANKNIFTY +0.18%  |  VIX -1.20%\nDeterministic universe.", parent)

    class WatchlistManagerWidget(Phase4Panel):
        def __init__(self, parent=None):
            super().__init__("Watchlist", "NIFTY\nBANKNIFTY\nUSDINR\nWatchlists are local and offline-safe.", parent)

    class Phase4Workspace(QtWidgets.QWidget):
        """Compact production safety workspace embedded in the desktop terminal."""

        def __init__(self, parent=None):
            super().__init__(parent)
            layout = QtWidgets.QGridLayout(self)
            layout.setContentsMargins(4, 4, 4, 4)
            layout.setSpacing(4)
            widgets = (
                AdvancedChartWidget(self), VolumeProfileWidget(self),
                OrderFlowWidget(self), PortfolioGreeksWidget(self),
                ExecutionDashboardWidget(self), CompliancePanelWidget(self),
                RiskDashboardWidget(self), MarketScannerWidget(self),
                WatchlistManagerWidget(self),
            )
            for index, widget in enumerate(widgets):
                layout.addWidget(widget, index // 3, index % 3)
else:
    class Phase4Panel:  # pragma: no cover
        def __init__(self, *_args, **_kwargs): raise RuntimeError("PyQt6 is required")
    AdvancedChartWidget = VolumeProfileWidget = OrderFlowWidget = PortfolioGreeksWidget = ExecutionDashboardWidget = CompliancePanelWidget = RiskDashboardWidget = MarketScannerWidget = WatchlistManagerWidget = Phase4Panel
    Phase4Workspace = Phase4Panel
