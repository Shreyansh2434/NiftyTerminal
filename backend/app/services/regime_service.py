"""Compatibility exports for regime services."""

from app.services.regime import get_regime


class RegimeService:
    async def get_regime(self, symbol: str = "NIFTY") -> dict:
        return await get_regime(symbol)


regime_service = RegimeService()

__all__ = ["RegimeService", "regime_service", "get_regime"]
