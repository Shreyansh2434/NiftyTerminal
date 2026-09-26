from datetime import datetime, timezone

from fastapi import APIRouter, Query

from app.models.regime import RegimeResponse
from app.services.regime import get_regime

router = APIRouter(prefix="/regime", tags=["regime"])


@router.get("", response_model=RegimeResponse, name="regime")
async def regime(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> RegimeResponse:
    data = await get_regime(symbol)
    return RegimeResponse(
        symbol=data["symbol"],
        regime=data["regime"],
        bias=data["bias"],
        score=data["score"],
        rationale=data["rationale"],
        meta={
            "source": "nse" if data.get("rows") else "empty",
            "cached": data.get("cached", False),
            "generated_at": datetime.now(timezone.utc),
            "warning": data.get("warning"),
        },
    )


@router.get("/{symbol}", response_model=RegimeResponse)
async def regime_for_symbol(symbol: str) -> RegimeResponse:
    return await regime(symbol)
