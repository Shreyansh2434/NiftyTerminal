from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

engine: AsyncEngine | None = None
session_factory: async_sessionmaker[AsyncSession] | None = None

try:
    engine = create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
except Exception as exc:  # pragma: no cover - protects imports in minimal installs
    logger.warning("Database engine is unavailable: %s", exc)


async def get_db() -> AsyncIterator[AsyncSession | None]:
    if session_factory is None:
        yield None
        return
    async with session_factory() as session:
        yield session


async def check_database() -> bool:
    if engine is None:
        return False
    try:
        from sqlalchemy import text

        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.info("Database health check failed: %s", exc)
        return False


async def dispose_database() -> None:
    if engine is not None:
        await engine.dispose()


@asynccontextmanager
async def optional_session() -> AsyncIterator[AsyncSession | None]:
    async for session in get_db():
        yield session
