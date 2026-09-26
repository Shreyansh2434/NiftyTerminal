"""Compatibility exports for integrations importing ``app.models.backtest``."""

from app.db.models import BacktestConfiguration, BacktestRun, BacktestTrade

BacktestTrades = BacktestTrade

__all__ = ["BacktestConfiguration", "BacktestRun", "BacktestTrade", "BacktestTrades"]
