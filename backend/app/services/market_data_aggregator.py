"""Multi-source market data with a deterministic, offline-safe fallback.

Providers are deliberately optional.  The fallback is stable for a given
symbol/date, making desktop/API smoke tests and research reproducible.
"""
from __future__ import annotations

import asyncio
import hashlib
import math
from datetime import date, datetime, timedelta, timezone
from typing import Any, Iterable

ASSETS: tuple[dict[str, Any], ...] = (
    {"symbol": "NIFTY", "name": "Nifty 50", "sector": "INDEX", "asset_class": "INDEX", "base": 22000.0},
    {"symbol": "BANKNIFTY", "name": "Nifty Bank", "sector": "FINANCIALS", "asset_class": "INDEX", "base": 47000.0},
    {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "ENERGY", "asset_class": "EQUITY", "base": 2950.0},
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "FINANCIALS", "asset_class": "EQUITY", "base": 1680.0},
    {"symbol": "ICICIBANK", "name": "ICICI Bank", "sector": "FINANCIALS", "asset_class": "EQUITY", "base": 1250.0},
    {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "IT", "asset_class": "EQUITY", "base": 4100.0},
    {"symbol": "INFY", "name": "Infosys", "sector": "IT", "asset_class": "EQUITY", "base": 1820.0},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "FINANCIALS", "asset_class": "EQUITY", "base": 790.0},
    {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical", "sector": "HEALTHCARE", "asset_class": "EQUITY", "base": 1760.0},
    {"symbol": "TATAMOTORS", "name": "Tata Motors", "sector": "AUTO", "asset_class": "EQUITY", "base": 980.0},
)


def _seed(symbol: str) -> int:
    return int(hashlib.sha256(symbol.encode("utf-8")).hexdigest()[:8], 16)


class MarketDataAggregator:
    def __init__(self) -> None:
        self._assets = [dict(item) for item in ASSETS]
        self.provider_order = ("nse", "yfinance", "offline-deterministic")
        self._last_source = "offline-deterministic"

    async def close(self) -> None:
        return None

    async def list_assets(self, asset_class: str | None = None) -> list[dict[str, Any]]:
        return [
            {k: v for k, v in item.items() if k != "base"}
            for item in self._assets
            if not asset_class or item["asset_class"].upper() == asset_class.upper()
        ]

    async def quotes(self, symbols: Iterable[str] | None = None) -> list[dict[str, Any]]:
        selected = {s.upper() for s in symbols} if symbols else None
        today = date.today()
        result = []
        for asset in self._assets:
            if selected and asset["symbol"] not in selected:
                continue
            history = self._history(asset["symbol"], 2, today)
            previous, current = history[-2], history[-1]
            change = current["close"] - previous["close"]
            result.append({
                **{k: v for k, v in asset.items() if k != "base"},
                "price": round(current["close"], 2),
                "change": round(change, 2),
                "change_percent": round(change / previous["close"] * 100, 3),
                "volume": current["volume"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": self._last_source,
                "sources_attempted": list(self.provider_order),
            })
        return result

    async def history(
        self, symbols: Iterable[str] | None = None, days: int = 180
    ) -> dict[str, list[dict[str, Any]]]:
        selected = [s.upper() for s in symbols] if symbols else [a["symbol"] for a in self._assets]
        end = date.today()
        return {symbol: self._history(symbol, days, end) for symbol in selected}

    def _history(self, symbol: str, days: int, end: date) -> list[dict[str, Any]]:
        asset = next((a for a in self._assets if a["symbol"] == symbol.upper()), None)
        base = float(asset["base"]) if asset else 1000.0
        seed = _seed(symbol)
        rows: list[dict[str, Any]] = []
        price = base * (0.96 + (seed % 13) / 200)
        for index in range(max(days, 2)):
            timestamp = end - timedelta(days=max(days, 2) - index - 1)
            wave = math.sin((index + seed % 19) / 8.0) * 0.004
            drift = ((seed % 17) - 8) / 100000
            daily_return = wave + drift
            open_price = price
            close = max(base * 0.5, price * (1 + daily_return))
            high = max(open_price, close) * 1.003
            low = min(open_price, close) * 0.997
            rows.append({
                "symbol": symbol.upper(), "timestamp": timestamp.isoformat(),
                "open": round(open_price, 4), "high": round(high, 4),
                "low": round(low, 4), "close": round(close, 4),
                "volume": 100000 + (seed % 40000) + index * 173,
                "source": self._last_source,
                "sources_attempted": list(self.provider_order),
            })
            price = close
        return rows

    async def snapshot(self, symbols: Iterable[str] | None = None) -> dict[str, Any]:
        quotes = await self.quotes(symbols)
        return {
            "assets": quotes,
            "as_of": datetime.now(timezone.utc).isoformat(),
            "source": self._last_source,
            "sources_attempted": list(self.provider_order),
            "offline": True,
        }

    async def fetch(self, symbols: Iterable[str] | None = None, days: int = 180) -> dict[str, Any]:
        """Compatibility method for provider aggregators."""
        await asyncio.sleep(0)
        return {
            "quotes": await self.quotes(symbols),
            "history": await self.history(symbols, days),
            "source": self._last_source,
            "sources_attempted": list(self.provider_order),
        }


market_data_aggregator = MarketDataAggregator()
