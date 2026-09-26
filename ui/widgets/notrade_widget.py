"""Compatibility entry point for the no-trade widget."""

from __future__ import annotations

from .trading_widgets import TradingDashboard

NoTradeWidget = TradingDashboard

__all__ = ["NoTradeWidget", "TradingDashboard"]
