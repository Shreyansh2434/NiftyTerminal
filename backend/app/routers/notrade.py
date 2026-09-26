from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.models.notrade import NoTradeResponse
from app.services.notrade import get_no_trade

router = APIRouter(prefix="/notrade", tags=["notrade"])


@router.get("", response_model=NoTradeResponse, name="notrade")
async def notrade(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> NoTradeResponse:
    data = await get_no_trade(symbol)
    return NoTradeResponse(
        symbol=data["symbol"],
        no_trade=data["no_trade"],
        status=data["status"],
        reasons=data.get("reasons", []),
        meta={
            "source": "nse" if data.get("rows") else "empty",
            "cached": data.get("cached", False),
            "generated_at": datetime.now(timezone.utc),
            "warning": data.get("warning"),
        },
    )


@router.get("/{symbol}", response_model=NoTradeResponse)
async def notrade_for_symbol(symbol: str) -> NoTradeResponse:
    return await notrade(symbol)
