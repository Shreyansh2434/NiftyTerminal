"""Compatibility exports for implied-volatility history models."""

from app.db.models import IVHistory

IvHistory = IVHistory
IVHistoryModel = IVHistory

__all__ = ["IVHistory", "IvHistory", "IVHistoryModel"]
