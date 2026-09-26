"""Seed the Phase 2 sample backtest configuration.

The Alembic migration seeds it for new installations; this idempotent helper
is useful for databases that were initialized with ``create_all``.
"""

import asyncio
import sys
from pathlib import Path

from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.database import engine
from app.db.models import BacktestConfiguration

PARAMETERS = {
    "initial_capital": 100000,
    "lot_size": 50,
    "entry_days": 5,
    "holding_days": 5,
    "short_delta": 0.16,
    "wing_width": 150,
    "commission_per_contract": 20,
    "slippage_bps": 4,
    "spread_bps": 10,
    "train_days": 126,
    "test_days": 63,
}


async def main() -> None:
    if engine is None:
        print("Database engine unavailable; nothing to seed.")
        return
    from sqlalchemy.ext.asyncio import async_sessionmaker

    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        exists = await session.scalar(
            select(BacktestConfiguration).where(BacktestConfiguration.name == "NIFTY Iron Condor — Balanced")
        )
        if not exists:
            session.add(
                BacktestConfiguration(
                    name="NIFTY Iron Condor — Balanced",
                    symbol="NIFTY",
                    parameters=PARAMETERS,
                    description="Conservative walk-forward iron-condor sample",
                )
            )
            await session.commit()
    await engine.dispose()
    print("Backtest sample configuration seeded.")


if __name__ == "__main__":
    asyncio.run(main())
