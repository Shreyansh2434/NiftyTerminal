"""yfinance compatibility adapter for spot-price consumers."""

from typing import Any

from app.services.market_data import market_data


class YFinanceClient:
    """Delegate spot retrieval to the shared cached market-data service."""

    async def fetch_spot(self, symbol: str = "NIFTY") -> dict[str, Any]:
        return await market_data.fetch_spot(symbol)


yfinance_client = YFinanceClient()


async def fetch_spot(symbol: str = "NIFTY") -> dict[str, Any]:
    return await yfinance_client.fetch_spot(symbol)


__all__ = ["YFinanceClient", "yfinance_client", "fetch_spot"]
