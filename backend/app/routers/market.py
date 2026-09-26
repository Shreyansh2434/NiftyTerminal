from datetime import timezone

from fastapi import APIRouter, Query

from app.schemas import ApiMeta, SpotQuote
from app.services.market_data import generated_at, market_data

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/spot", response_model=SpotQuote)
async def spot(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> SpotQuote:
    data = await market_data.fetch_spot(symbol)
    return SpotQuote(
        symbol=data["symbol"],
        value=data.get("value"),
        change=data.get("change"),
        change_percent=data.get("change_percent"),
        timestamp=generated_at(),
        meta=ApiMeta(
            source="nse/yfinance" if data.get("value") is not None else "empty",
            cached=data.get("cached", False),
            generated_at=generated_at(),
            warning=data.get("warning"),
        ),
    )
