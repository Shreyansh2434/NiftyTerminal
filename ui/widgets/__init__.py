"""Reusable widgets used by the desktop terminal."""

from .backtest_widgets import BacktestConfigWidget, BacktestResultsWidget
from .backtest_metrics_widget import BacktestMetricsWidget
from .backtest_summary_widget import BacktestSummaryWidget
from .equity_curve_widget import EquityCurveWidget
from .iv_panel_widget import IVPanelWidget
from .notrade_widget import NoTradeWidget
from .options_chain_widget import OptionsChainWidget
from .regime_breakdown_widget import RegimeBreakdownWidget
from .regime_widget import RegimeWidget
from .trading_widgets import TradingDashboard
from .trades_table_widget import TradesTableWidget
from .phase4_widgets import (
    AdvancedChartWidget, VolumeProfileWidget, OrderFlowWidget, PortfolioGreeksWidget,
    ExecutionDashboardWidget, CompliancePanelWidget, RiskDashboardWidget,
    MarketScannerWidget, WatchlistManagerWidget,
)

__all__ = [
    "TradingDashboard",
    "BacktestConfigWidget",
    "BacktestResultsWidget",
    "OptionsChainWidget",
    "IVPanelWidget",
    "RegimeWidget",
    "NoTradeWidget",
    "BacktestSummaryWidget",
    "BacktestMetricsWidget",
    "RegimeBreakdownWidget",
    "EquityCurveWidget",
    "TradesTableWidget",
    "AdvancedChartWidget", "VolumeProfileWidget", "OrderFlowWidget", "PortfolioGreeksWidget",
    "ExecutionDashboardWidget", "CompliancePanelWidget", "RiskDashboardWidget",
    "MarketScannerWidget", "WatchlistManagerWidget",
]
