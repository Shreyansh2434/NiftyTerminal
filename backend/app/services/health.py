from datetime import datetime, timezone

from app.db.database import check_database
from app.core.config import get_settings


async def get_health() -> dict:
    return {
        "status": "ok",
        "database": await check_database(),
        "market_data": "best-effort",
        "generated_at": datetime.now(timezone.utc),
        "details": {"message": "API is available; providers may be offline"},
    }


async def get_readiness() -> dict:
    """Return operational checks without treating optional providers as fatal."""
    settings = get_settings()
    database = await check_database()
    paper_safe = (
        settings.trading_mode.lower() == "paper"
        and not settings.live_trading_enabled
        and settings.kill_switch_active
    )
    return {
        "status": "ready" if paper_safe else "attention_required",
        "checks": {
            "api": True,
            "database": database,
            "paper_safety_defaults": paper_safe,
            "market_data": "best-effort",
        },
        "mode": settings.trading_mode,
        "generated_at": datetime.now(timezone.utc),
        "details": {
            "database_optional": True,
            "live_trading_enabled": settings.live_trading_enabled,
            "kill_switch_active": settings.kill_switch_active,
        },
    }
