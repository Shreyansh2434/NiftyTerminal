from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.models.iv import IVResponse
from app.services.iv import get_iv

router = APIRouter(prefix="/iv", tags=["iv"])


@router.get("", response_model=IVResponse, name="iv")
async def iv(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> IVResponse:
    data = await get_iv(symbol)
    return IVResponse(
        symbol=data["symbol"],
        spot=data.get("spot"),
        atm_iv=data.get("atm_iv"),
        call_iv=data.get("call_iv"),
        put_iv=data.get("put_iv"),
        points=data.get("points", []),
        meta={
            "source": "nse" if data.get("points") else "empty",
            "cached": data.get("cached", False),
            "generated_at": datetime.now(timezone.utc),
            "warning": data.get("warning"),
        },
    )


@router.get("/{symbol}", response_model=IVResponse)
async def iv_for_symbol(symbol: str) -> IVResponse:
    return await iv(symbol)
