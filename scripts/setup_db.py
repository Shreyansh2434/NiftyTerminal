"""Initialize the application's database schema.

This delegates to the existing async SQLAlchemy metadata initializer and is
kept at the repository-level for the documented setup command.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.db.database import engine
from app.db.models import Base


async def main() -> None:
    if engine is None:
        print("Database engine unavailable; nothing to initialize.")
        return
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Database tables initialized.")


if __name__ == "__main__":
    asyncio.run(main())
