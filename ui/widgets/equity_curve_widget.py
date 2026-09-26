"""Compatibility entry point for the backtest equity curve."""

from __future__ import annotations

from ..qt_compat import QT_AVAILABLE
from .backtest_widgets import BacktestResultsWidget

if QT_AVAILABLE:
    from .backtest_widgets import _EquityChart

    EquityCurveWidget = _EquityChart
else:
    # Keep imports safe on API-only installations, just like the consolidated
    # widget module does.
    EquityCurveWidget = BacktestResultsWidget

__all__ = ["EquityCurveWidget", "BacktestResultsWidget"]
