"""Reproducible chart analytics for disconnected development and review."""
from __future__ import annotations


class ChartDataEngine:
    def volume_profile(self, symbol: str = "NIFTY") -> list[dict]:
        return self.data(symbol, 1)["volume_profile"]

    def order_flow(self, symbol: str = "NIFTY") -> dict:
        return self.data(symbol, 1)["order_flow"]

    def market_profile(self, symbol: str = "NIFTY") -> dict:
        return self.data(symbol, 1)["market_profile"]

    def data(self, symbol: str = "NIFTY", points: int = 24) -> dict:
        points = max(1, min(200, points))
        candles = []
        for i in range(points):
            close = 22100.0 + ((i * 37) % 11) * 8.5 + i * 2.2
            candles.append({"timestamp": f"2026-01-01T{i:02d}:00:00Z", "open": round(close - 8, 2), "high": round(close + 18, 2), "low": round(close - 22, 2), "close": round(close, 2), "volume": 1000 + (i * 173) % 900})
        bins = [{"price": 22080 + i * 20, "volume": 500 + ((i * 97) % 700), "buy_volume": 300 + ((i * 41) % 350), "sell_volume": 200 + ((i * 23) % 300)} for i in range(12)]
        poc = max(bins, key=lambda item: item["volume"])["price"]
        return {"symbol": symbol.upper(), "source": "offline-deterministic", "candles": candles, "volume_profile": bins, "point_of_control": poc, "value_area": {"low": 22120, "high": 22260}, "order_flow": {"buy_imbalance": 0.57, "delta": 1840}, "market_profile": {"poc": poc, "initial_balance_high": 22210, "initial_balance_low": 22130}}


chart_data_engine = ChartDataEngine()
