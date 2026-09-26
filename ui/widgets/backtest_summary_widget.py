"""Compatibility entry point for the backtest summary surface."""

from __future__ import annotations

from .backtest_widgets import BacktestResultsWidget

BacktestSummaryWidget = BacktestResultsWidget

__all__ = ["BacktestSummaryWidget", "BacktestResultsWidget"]
