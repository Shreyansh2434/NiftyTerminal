"""Compatibility worker entry point for desktop data fetching.

The current desktop client deliberately has no mandatory live provider.  Its
working background worker is the same Qt-safe worker used by the backtest tab,
so expose that implementation under the spec's data-worker filename.
"""

from __future__ import annotations

from .backtest_worker import BacktestWorker

DataFetchWorker = BacktestWorker

__all__ = ["DataFetchWorker", "BacktestWorker"]
