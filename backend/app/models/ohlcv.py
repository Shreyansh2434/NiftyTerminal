"""Compatibility exports for OHLCV persistence models."""

from app.db.models import OHLCV

Ohlcv = OHLCV
OHLCVModel = OHLCV

__all__ = ["OHLCV", "Ohlcv", "OHLCVModel"]
