import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import get_settings
from app.services.market_data import market_data

logger = logging.getLogger(__name__)


def create_scheduler() -> AsyncIOScheduler | None:
    settings = get_settings()
    if not settings.scheduler_enabled:
        return None
    scheduler = AsyncIOScheduler()
    scheduler.add_job(market_data.fetch_chain, "interval", seconds=settings.refresh_interval_seconds, id="refresh-nifty", kwargs={"symbol": "NIFTY"}, replace_existing=True)
    return scheduler
