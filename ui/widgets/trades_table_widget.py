"""Compatibility entry point for the backtest trades table."""

from __future__ import annotations

from .backtest_widgets import BacktestResultsWidget

TradesTableWidget = BacktestResultsWidget

__all__ = ["TradesTableWidget", "BacktestResultsWidget"]
