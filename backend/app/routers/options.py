from fastapi import APIRouter, Query

from app.schemas import ApiMeta, OptionChainResponse, OptionRow
from app.services.market_data import generated_at
from app.services.options import get_options

router = APIRouter(prefix="/options", tags=["options"])


async def _chain_response(symbol: str) -> OptionChainResponse:
    data = await get_options(symbol)
    return OptionChainResponse(
        symbol=data["symbol"],
        expiry=data.get("expiry"),
        spot=data.get("spot"),
        rows=[OptionRow(**row) for row in data.get("rows", [])],
        expiries=data.get("expiries", []),
        meta=ApiMeta(
            source="nse" if data.get("rows") else "empty",
            cached=data.get("cached", False),
            generated_at=generated_at(),
            warning=data.get("warning"),
        ),
    )


@router.get("", response_model=OptionChainResponse, name="options")
async def options(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> OptionChainResponse:
    """Phase 1 contract: return the latest normalized option chain."""
    return await _chain_response(symbol)


@router.get("/chain", response_model=OptionChainResponse)
async def chain(symbol: str = Query("NIFTY", min_length=1, max_length=20)) -> OptionChainResponse:
    return await _chain_response(symbol)


@router.get("/chain/{symbol}", response_model=OptionChainResponse)
async def chain_for_symbol(symbol: str) -> OptionChainResponse:
    return await _chain_response(symbol)


@router.get("/expiries/{symbol}")
async def expiries(symbol: str) -> dict:
    data = await get_options(symbol)
    return {"symbol": symbol.upper(), "expiries": data.get("expiries", []), "fetched_at": generated_at()}


@router.get("/pcr/{symbol}")
async def pcr(symbol: str) -> dict:
    data = await get_options(symbol)
    return {
        "symbol": symbol.upper(),
        "pcr_oi": data.get("pcr_oi"),
        "pcr_volume": data.get("pcr_volume"),
        "history": [],
        "fetched_at": generated_at(),
    }
