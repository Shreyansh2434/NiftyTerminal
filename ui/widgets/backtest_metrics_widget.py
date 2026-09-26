"""Compatibility entry point for backtest metrics."""

from __future__ import annotations

from .backtest_widgets import BacktestResultsWidget

BacktestMetricsWidget = BacktestResultsWidget

__all__ = ["BacktestMetricsWidget", "BacktestResultsWidget"]
