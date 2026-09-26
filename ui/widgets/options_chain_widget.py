"""Compatibility entry point for the options-chain widget.

The desktop implementation originally grouped the trading surfaces in
``trading_widgets``.  Keep the spec's module name available without creating
another implementation to maintain.
"""

from __future__ import annotations

from .trading_widgets import TradingDashboard

OptionsChainWidget = TradingDashboard

__all__ = ["OptionsChainWidget", "TradingDashboard"]
