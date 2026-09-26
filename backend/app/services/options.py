from typing import Any

from app.services.market_data import market_data


async def get_options(symbol: str = "NIFTY") -> dict[str, Any]:
    """Return the resilient, normalized option-chain snapshot."""
    return await market_data.fetch_chain(symbol)
