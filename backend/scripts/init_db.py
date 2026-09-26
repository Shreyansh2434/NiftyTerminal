import asyncio
import sys
from pathlib import Path

# Allow both `python -m scripts.init_db` from backend and
# `python backend/scripts/init_db.py` from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
