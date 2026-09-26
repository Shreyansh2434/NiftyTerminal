"""Compatibility exports for implied-volatility services."""

from app.services.iv import get_iv


class IVService:
    async def get_iv(self, symbol: str = "NIFTY") -> dict:
        return await get_iv(symbol)


iv_service = IVService()

__all__ = ["IVService", "iv_service", "get_iv"]
