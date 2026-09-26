"""Names shared by the desktop widget specification.

The first desktop pass keeps these surfaces in the consolidated widgets.  The
aliases below intentionally point at those tested implementations so callers
can migrate to the spec's module layout without changing runtime behaviour.
"""

from __future__ import annotations

from .backtest_widgets import BacktestConfigWidget, BacktestResultsWidget
from .trading_widgets import TradingDashboard

DashboardWidget = TradingDashboard
ResultsWidget = BacktestResultsWidget
ConfigWidget = BacktestConfigWidget

__all__ = [
    "TradingDashboard",
    "BacktestConfigWidget",
    "BacktestResultsWidget",
    "DashboardWidget",
    "ResultsWidget",
    "ConfigWidget",
]
