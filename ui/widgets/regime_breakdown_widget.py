"""Compatibility entry point for the regime breakdown surface."""

from __future__ import annotations

from .backtest_widgets import BacktestResultsWidget

RegimeBreakdownWidget = BacktestResultsWidget

__all__ = ["RegimeBreakdownWidget", "BacktestResultsWidget"]
