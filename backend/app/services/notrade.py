from typing import Any

from app.services.market_data import market_data


async def get_no_trade(symbol: str = "NIFTY") -> dict[str, Any]:
    data = await market_data.fetch_chain(symbol)
    reasons: list[str] = []
    if data.get("warning"):
        reasons.append(data["warning"])
    if not data.get("rows"):
        reasons.append("Option-chain data is unavailable.")
    no_trade = bool(reasons)
    return {
        **data,
        "no_trade": no_trade,
        "status": "NO_TRADE" if no_trade else "TRADE_ALLOWED",
        "reasons": reasons,
    }
