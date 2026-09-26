"""Phase 3 asset universe, quote and heatmap endpoints."""
from fastapi import APIRouter, Query

from app.services.ai_analyst_engine import ai_analyst_engine
from app.services.heatmap_engine import heatmap_engine
from app.services.market_data_aggregator import market_data_aggregator
from app.services.sector_analyzer import sector_analyzer
from app.services.sentiment_engine import sentiment_engine

router = APIRouter(tags=["phase3-market"])


@router.get("/assets")
async def assets(asset_class: str | None = Query(None)) -> dict:
    return {"assets": await market_data_aggregator.list_assets(asset_class), "source": "offline-deterministic"}


@router.get("/assets/{symbol}")
async def asset(symbol: str) -> dict:
    quotes = await market_data_aggregator.quotes([symbol])
    return quotes[0] if quotes else {"symbol": symbol.upper(), "error": "Unknown asset"}


@router.get("/heatmap")
async def heatmap() -> dict:
    snapshot = await market_data_aggregator.snapshot()
    return {"cells": heatmap_engine.build(snapshot["assets"]), "as_of": snapshot["as_of"], "source": snapshot["source"]}


@router.get("/workspace")
async def workspace() -> dict:
    snapshot = await market_data_aggregator.snapshot()
    sentiment = sentiment_engine.analyze()
    sectors = sector_analyzer.analyze(snapshot["assets"])
    return {"snapshot": snapshot, "heatmap": heatmap_engine.build(snapshot["assets"]),
            "sentiment": sentiment, "sectors": sectors,
            "analyst": ai_analyst_engine.analyze(snapshot, sentiment, sectors)}
