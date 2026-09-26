"""Compatibility entry point for the market-regime widget."""

from __future__ import annotations

from .trading_widgets import TradingDashboard

RegimeWidget = TradingDashboard

__all__ = ["RegimeWidget", "TradingDashboard"]
