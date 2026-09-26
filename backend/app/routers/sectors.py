from fastapi import APIRouter

from app.services.market_data_aggregator import market_data_aggregator
from app.services.sector_analyzer import sector_analyzer

router = APIRouter(prefix="/sectors", tags=["phase3-sectors"])


@router.get("")
@router.get("/")
async def sectors() -> dict:
    quotes = await market_data_aggregator.quotes()
    return {"sectors": sector_analyzer.analyze(quotes), "source": "offline-deterministic"}


@router.get("/performance")
async def sector_performance() -> dict:
    return await sectors()
