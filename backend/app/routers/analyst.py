from fastapi import APIRouter

from app.services.ai_analyst_engine import ai_analyst_engine
from app.services.market_data_aggregator import market_data_aggregator
from app.services.sector_analyzer import sector_analyzer
from app.services.sentiment_engine import sentiment_engine

router = APIRouter(prefix="/analyst", tags=["phase3-analyst"])


@router.get("")
@router.get("/")
async def analyst() -> dict:
    snapshot = await market_data_aggregator.snapshot()
    sentiment = sentiment_engine.analyze()
    sectors = sector_analyzer.analyze(snapshot["assets"])
    return ai_analyst_engine.analyze(snapshot, sentiment, sectors)


@router.get("/{symbol}")
async def analyst_for_symbol(symbol: str) -> dict:
    result = await analyst()
    result["symbol"] = symbol.upper()
    return result
