import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.database import dispose_database
from app.routers import analytics, backtest, health, instruments, iv, market, notrade, options, regime
from app.routers import analyst, market_assets, sentiment, sectors, multi_asset_backtests, phase4, ai
from app.scheduler import create_scheduler
from app.services.market_data import market_data
from app.services.market_data_aggregator import market_data_aggregator

logging.basicConfig(level=get_settings().log_level)


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = create_scheduler()
    if scheduler:
        scheduler.start()
    yield
    if scheduler:
        scheduler.shutdown(wait=False)
    await market_data.close()
    await market_data_aggregator.close()
    await dispose_database()


app = FastAPI(title=get_settings().app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")
app.include_router(options.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")

# Phase 1 uses the short /api contract.  Keep the original /api/v1 routes
# above so existing dashboard clients continue to work during the transition.
app.include_router(health.router, prefix="/api")
app.include_router(market.router, prefix="/api")
app.include_router(options.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
for module in (iv, regime, notrade, instruments):
    app.include_router(module.router, prefix="/api")
    app.include_router(module.router, prefix="/api/v1")
app.include_router(backtest.router, prefix="/api")
for prefix in ("/api", "/api/v1"):
    app.include_router(market_assets.router, prefix=prefix + "/market")
    app.include_router(sentiment.router, prefix=prefix)
    app.include_router(sectors.router, prefix=prefix)
    app.include_router(analyst.router, prefix=prefix)
    app.include_router(sentiment.router, prefix=prefix + "/market")
    app.include_router(sectors.router, prefix=prefix + "/market")
    app.include_router(analyst.router, prefix=prefix + "/market")
    app.include_router(multi_asset_backtests.router, prefix=prefix + "/backtests/multi-asset")
    # Friendly aliases used by the desktop and early Phase 3 clients.
    app.include_router(multi_asset_backtests.router, prefix=prefix + "/multi-asset-backtests")
    app.include_router(multi_asset_backtests.router, prefix=prefix + "/backtest/multi-asset")
    app.include_router(phase4.router, prefix=prefix)
    app.include_router(ai.router, prefix=prefix)


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": get_settings().app_name, "docs": "/docs"}
