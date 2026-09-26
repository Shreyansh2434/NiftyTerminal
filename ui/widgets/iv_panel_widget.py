"""Compatibility entry point for the implied-volatility panel."""

from __future__ import annotations

from .trading_widgets import TradingDashboard

IVPanelWidget = TradingDashboard

__all__ = ["IVPanelWidget", "TradingDashboard"]
