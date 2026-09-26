"""NSE client compatibility layer.

The live implementation remains in :mod:`market_data`; this adapter preserves
the client-oriented import path used by integrations.
"""

from typing import Any

from app.services.market_data import MarketDataService, market_data


class NSEClient:
    """Small adapter around the application's resilient market-data client."""

    async def fetch_option_chain(self, symbol: str = "NIFTY") -> dict[str, Any]:
        return await market_data.fetch_chain(symbol)

    async def close(self) -> None:
        await market_data.close()


nse_client = NSEClient()

__all__ = ["MarketDataService", "NSEClient", "nse_client", "market_data"]
