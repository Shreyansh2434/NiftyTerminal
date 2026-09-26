from fastapi import APIRouter

from app.services.sentiment_engine import sentiment_engine

router = APIRouter(prefix="/sentiment", tags=["phase3-sentiment"])


@router.get("")
@router.get("/")
async def sentiment() -> dict:
    return sentiment_engine.analyze()


@router.get("/{symbol}")
async def sentiment_for_symbol(symbol: str) -> dict:
    return sentiment_engine.analyze(symbol=symbol.upper())


@router.post("/score")
async def score(payload: dict) -> dict:
    return sentiment_engine.analyze(payload.get("headlines"), payload.get("symbol", "MARKET"))
