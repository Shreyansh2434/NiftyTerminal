from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

EMPTY_CHAIN: dict[str, Any] = {"symbol": "NIFTY", "expiry": None, "spot": None, "rows": [], "expiries": []}


class MarketDataService:
    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._chain_cache: tuple[float, dict[str, Any]] | None = None
        self._spot_cache: tuple[float, dict[str, Any]] | None = None

    async def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=settings.nse_timeout_seconds,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; NIFTY-Options-Terminal/1.0)",
                    "Accept": "application/json",
                },
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def fetch_chain(self, symbol: str = "NIFTY") -> dict[str, Any]:
        now = asyncio.get_running_loop().time()
        if self._chain_cache and now - self._chain_cache[0] < settings.market_cache_seconds:
            return {**self._chain_cache[1], "cached": True, "warning": None}
        try:
            response = await (await self.client()).get(
                f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol.upper()}"
            )
            response.raise_for_status()
            payload = response.json()
            result = self._normalize_chain(payload, symbol.upper())
            self._chain_cache = (now, result)
            return result
        except Exception as exc:
            logger.info("NSE option chain unavailable: %s", exc)
            if self._chain_cache:
                return {**self._chain_cache[1], "cached": True, "warning": "Live NSE data unavailable"}
            return {**EMPTY_CHAIN, "symbol": symbol.upper(), "cached": False, "warning": "Live NSE data unavailable"}

    async def fetch_spot(self, symbol: str = "NIFTY") -> dict[str, Any]:
        now = asyncio.get_running_loop().time()
        if self._spot_cache and now - self._spot_cache[0] < settings.market_cache_seconds:
            return {**self._spot_cache[1], "cached": True, "warning": None}
        try:
            chain = await self.fetch_chain(symbol)
            if chain.get("spot") is not None:
                result = {"symbol": symbol.upper(), "value": chain["spot"], "change": None, "change_percent": None}
                self._spot_cache = (now, result)
                return {**result, "cached": chain.get("cached", False), "warning": chain.get("warning")}
        except Exception:
            pass
        try:
            import yfinance as yf

            ticker = await asyncio.to_thread(yf.Ticker, "^NSEI")
            history = await asyncio.to_thread(ticker.history, period="2d", interval="1d")
            if not history.empty:
                close = float(history["Close"].iloc[-1])
                previous = float(history["Close"].iloc[-2]) if len(history) > 1 else None
                result = {
                    "symbol": symbol.upper(),
                    "value": close,
                    "change": close - previous if previous is not None else None,
                    "change_percent": ((close - previous) / previous * 100) if previous else None,
                }
                self._spot_cache = (now, result)
                return {**result, "cached": False, "warning": None}
        except Exception as exc:
            logger.info("yfinance spot unavailable: %s", exc)
        if self._spot_cache:
            return {**self._spot_cache[1], "cached": True, "warning": "Live market data unavailable"}
        return {"symbol": symbol.upper(), "value": None, "change": None, "change_percent": None, "cached": False, "warning": "Market data unavailable"}

    @staticmethod
    def _normalize_chain(payload: dict[str, Any], symbol: str) -> dict[str, Any]:
        records = payload.get("records", {})
        rows: dict[float, dict[str, Any]] = {}
        for item in records.get("data", []):
            strike = item.get("strikePrice")
            if strike is None:
                continue
            row = rows.setdefault(float(strike), {"strike": float(strike)})
            for side, key in (("CE", "call"), ("PE", "put")):
                quote = item.get(side) or {}
                row[f"{key}_oi"] = int(quote.get("openInterest", 0) or 0)
                row[f"{key}_oi_change"] = int(quote.get("changeinOpenInterest", 0) or 0)
                row[f"{key}_volume"] = int(quote.get("totalTradedVolume", 0) or 0)
                row[f"{key}_iv"] = quote.get("impliedVolatility")
                row[f"{key}_ltp"] = quote.get("lastPrice")
        return {
            "symbol": symbol,
            "expiry": (records.get("expiryDates") or [None])[0],
            "spot": records.get("underlyingValue"),
            "rows": sorted(rows.values(), key=lambda row: row["strike"]),
            "expiries": records.get("expiryDates", []),
            "cached": False,
            "warning": None,
        }


market_data = MarketDataService()


def generated_at() -> datetime:
    return datetime.now(timezone.utc)
