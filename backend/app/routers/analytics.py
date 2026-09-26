from fastapi import APIRouter, Query

from app.schemas import (
    AnalyticsSummary,
    ApiMeta,
    HeatmapCell,
    HeatmapResponse,
    MaxPainResponse,
    OIChange,
    OIChangesResponse,
    Signal,
    SignalsResponse,
)
from app.services.analytics import calculate_levels, calculate_max_pain, calculate_pcr, infer_bias
from app.services.market_data import generated_at, market_data

router = APIRouter(prefix="/analytics", tags=["analytics"])


async def get_data(symbol: str) -> dict:
    return await market_data.fetch_chain(symbol)


def meta(data: dict) -> ApiMeta:
    return ApiMeta(
        source="nse" if data.get("rows") else "empty",
        cached=data.get("cached", False),
        generated_at=generated_at(),
        warning=data.get("warning"),
    )


@router.get("/summary", response_model=AnalyticsSummary)
async def summary(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> AnalyticsSummary:
    data = await get_data(symbol)
    rows = data.get("rows", [])
    pcr = calculate_pcr(rows)
    max_pain, _ = calculate_max_pain(rows)
    levels = calculate_levels(rows)
    return AnalyticsSummary(symbol=data["symbol"], spot=data.get("spot"), pcr=pcr, max_pain=max_pain, bias=infer_bias(pcr), **levels, meta=meta(data))


@router.get("/heatmap", response_model=HeatmapResponse)
async def heatmap(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> HeatmapResponse:
    data = await get_data(symbol)
    return HeatmapResponse(
        symbol=data["symbol"],
        rows=[HeatmapCell(**row) for row in data.get("rows", [])],
        meta=meta(data),
    )


@router.get("/max-pain", response_model=MaxPainResponse)
async def max_pain(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> MaxPainResponse:
    data = await get_data(symbol)
    strike, payouts = calculate_max_pain(data.get("rows", []))
    return MaxPainResponse(symbol=data["symbol"], strike=strike, payouts=payouts, meta=meta(data))


@router.get("/oi-changes", response_model=OIChangesResponse)
async def oi_changes(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> OIChangesResponse:
    data = await get_data(symbol)
    return OIChangesResponse(
        symbol=data["symbol"],
        changes=[OIChange(strike=row["strike"], call_change=row.get("call_oi_change", 0), put_change=row.get("put_oi_change", 0)) for row in data.get("rows", [])],
        meta=meta(data),
    )


@router.get("/signals", response_model=SignalsResponse)
async def signals(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> SignalsResponse:
    data = await get_data(symbol)
    rows = data.get("rows", [])
    pcr = calculate_pcr(rows)
    if pcr is None:
        result: list[Signal] = []
    else:
        result = [
            Signal(
                name="Put/Call Ratio",
                value=f"{pcr:.3f}",
                confidence=min(1.0, abs(pcr - 1) * 2),
                rationale=f"PCR suggests {infer_bias(pcr).lower()} positioning.",
            )
        ]
    return SignalsResponse(symbol=data["symbol"], signals=result, meta=meta(data))
