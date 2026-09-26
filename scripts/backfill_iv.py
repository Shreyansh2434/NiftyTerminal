"""Implied-volatility backfill entry point."""

import asyncio

from setup_db import main as setup_database


async def main() -> None:
    await setup_database()
    print("IV backfill ready; no provider data was requested.")


if __name__ == "__main__":
    asyncio.run(main())
