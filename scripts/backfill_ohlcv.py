"""OHLCV backfill entry point.

Historical providers are intentionally not invoked implicitly.  The command
ensures the schema exists and leaves provider-specific ingestion to callers.
"""

import asyncio

from setup_db import main as setup_database


async def main() -> None:
    await setup_database()
    print("OHLCV backfill ready; no provider data was requested.")


if __name__ == "__main__":
    asyncio.run(main())
