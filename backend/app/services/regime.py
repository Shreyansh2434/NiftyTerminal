from typing import Any

from app.services.analytics import calculate_pcr, infer_bias
from app.services.market_data import market_data


async def get_regime(symbol: str = "NIFTY") -> dict[str, Any]:
    data = await market_data.fetch_chain(symbol)
    pcr = calculate_pcr(data.get("rows", []))
    bias = infer_bias(pcr)
    if pcr is None:
        regime = "NEUTRAL"
        score = 0.0
        rationale = "Insufficient market data for a directional regime."
    elif bias == "BULLISH":
        regime = "BULLISH"
        score = min(1.0, round((pcr - 1.0) / 0.5, 3))
        rationale = "Put open interest is materially higher than call open interest."
    elif bias == "BEARISH":
        regime = "BEARISH"
        score = -min(1.0, round((1.0 - pcr) / 0.5, 3))
        rationale = "Call open interest is materially higher than put open interest."
    else:
        regime = "RANGE_BOUND"
        score = 0.0
        rationale = "Put/call open interest is balanced."
    return {**data, "regime": regime, "bias": bias, "score": score, "rationale": rationale}
