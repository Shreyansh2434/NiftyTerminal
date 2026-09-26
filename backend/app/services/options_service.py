"""Compatibility exports for option-chain services."""

from app.services.options import get_options


class OptionsService:
    async def get_options(self, symbol: str = "NIFTY") -> dict:
        return await get_options(symbol)

    async def fetch_chain(self, symbol: str = "NIFTY") -> dict:
        return await get_options(symbol)


options_service = OptionsService()

__all__ = ["OptionsService", "options_service", "get_options"]
