"""Compatibility exports for no-trade services."""

from app.services.notrade import get_no_trade


class NoTradeService:
    async def get_no_trade(self, symbol: str = "NIFTY") -> dict:
        return await get_no_trade(symbol)


notrade_service = NoTradeService()

__all__ = ["NoTradeService", "notrade_service", "get_no_trade"]
