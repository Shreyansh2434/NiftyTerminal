"""Offline-first deterministic AI copilot tools.

These tools intentionally return research data only.  They never place orders
and do not call a live connector unless a caller explicitly supplies one.
"""
from __future__ import annotations

import hashlib
import random
from typing import Any, Callable, Protocol

from app.services.multi_asset_backtest_engine import multi_asset_backtest_engine


def _seed(value: str) -> int:
    return int(hashlib.sha256(value.upper().encode()).hexdigest()[:12], 16)


class ModelAdapter(Protocol):
    """Optional local/external model boundary; deterministic mode is the default."""

    def complete(self, prompt: str) -> str: ...


class AICopilot:
    def __init__(self, model: ModelAdapter | None = None) -> None:
        self.model = model
    def snapshot(self, symbol: str = "NIFTY") -> dict[str, Any]:
        quote = self.quote(symbol)
        return {
            "as_of": "offline",
            "symbol": quote["symbol"],
            "regime": "DATA-SAFE / RESEARCH",
            "confidence": 0.5,
            "summary": f"{quote['symbol']} is available through the offline research copilot at {quote['price']:.2f}.",
            "forecast": [
                {"horizon": "NEXT SESSION", "direction": "NEUTRAL", "target": quote["price"], "confidence": 0.5},
                {"horizon": "5 SESSIONS", "direction": "SCENARIO ONLY", "target": quote["price"], "confidence": 0.35},
            ],
            "deep_dive": [{"title": "DATA SOURCE", "detail": "Deterministic local research data; no live order or broker action.", "signal": "SAFE MODE"}],
            "historical_analogues": [],
            "risk": [{"label": "EXECUTION", "value": "PAPER ONLY", "status": "SAFE"}, {"label": "LIVE CONNECTOR", "value": "DISABLED", "status": "BLOCKED"}],
            "source": "offline-deterministic",
        }

    def answer(self, query: str, symbol: str = "NIFTY") -> dict[str, Any]:
        if self.model is not None:
            return {**self.snapshot(symbol), "query": query, "model_response": self.model.complete(query), "source": "model-adapter"}
        text = query.strip().lower()
        if "option" in text:
            result = self.options(symbol)
            summary = f"{result['symbol']} options snapshot has {len(result['rows'])} strikes."
        elif "backtest" in text or "rsi" in text:
            result = self.backtest(symbol)
            summary = "Deterministic research backtest completed; results are not trading advice."
        elif "monte" in text or "simulation" in text:
            result = self.monte_carlo()
            summary = "Deterministic Monte Carlo scenario completed; it is not a forecast."
        else:
            result = self.quote(symbol)
            summary = f"{result['symbol']} quote is {result['price']:.2f} in offline mode."
        return {**self.snapshot(symbol), "summary": summary, "query": query, "result": result}
    def quote(self, symbol: str = "NIFTY") -> dict[str, Any]:
        symbol = symbol.upper().strip()
        base = 100 + _seed(symbol) % 40_000
        change = ((_seed(symbol + ":change") % 401) - 200) / 100
        return {"symbol": symbol, "price": float(base), "change": change, "change_percent": round(change / base * 100, 4), "source": "offline-deterministic", "live": False}

    def options(self, symbol: str = "NIFTY", strikes: int = 5) -> dict[str, Any]:
        quote = self.quote(symbol)
        step, spot = 50, quote["price"]
        centre = round(spot / step) * step
        rows = []
        for offset in range(-max(1, min(strikes, 10)), max(1, min(strikes, 10)) + 1):
            strike = centre + offset * step
            rows.append({"strike": strike, "call_ltp": round(max(1, spot - strike) * .1 + 12, 2), "put_ltp": round(max(1, strike - spot) * .1 + 12, 2), "call_oi": 1000 + abs(offset) * 250, "put_oi": 1200 + abs(offset) * 200})
        return {"symbol": symbol.upper(), "spot": spot, "rows": rows, "source": "offline-deterministic", "live": False}

    def backtest(self, symbol: str = "NIFTY", days: int = 30, initial_capital: float = 100_000) -> dict[str, Any]:
        days = max(2, min(int(days), 2_000))
        rng = random.Random(_seed(symbol + ":history"))
        price = self.quote(symbol)["price"]
        bars = []
        for day in range(days):
            price = max(1, price * (1 + rng.uniform(-.012, .014)))
            bars.append({"timestamp": f"offline-day-{day:04d}", "close": round(price, 4)})
        return multi_asset_backtest_engine.run({symbol.upper(): bars}, initial_capital, "equal_weight_momentum", {"offline": True})

    def monte_carlo(self, initial: float = 100_000, drift: float = .0003, volatility: float = .01, days: int = 30, simulations: int = 200, seed: int = 7) -> dict[str, Any]:
        days, simulations = max(1, min(int(days), 2_000)), max(1, min(int(simulations), 5_000))
        rng = random.Random(seed)
        finals = []
        for _ in range(simulations):
            value = float(initial)
            for _ in range(days):
                value *= 1 + rng.gauss(float(drift), abs(float(volatility)))
            finals.append(value)
        finals.sort()
        return {"initial": float(initial), "days": days, "simulations": simulations, "seed": seed, "mean_final": round(sum(finals) / len(finals), 2), "p05": round(finals[max(0, int(.05 * len(finals)) - 1)], 2), "p50": round(finals[len(finals) // 2], 2), "p95": round(finals[min(len(finals) - 1, int(.95 * len(finals)))], 2), "source": "offline-deterministic"}

    def tools(self) -> dict[str, Callable[..., dict[str, Any]]]:
        return {"quote": self.quote, "options": self.options, "backtest": self.backtest, "monte_carlo": self.monte_carlo}

    def call_tool(self, name: str, **arguments: Any) -> dict[str, Any]:
        try:
            tool = self.tools()[name]
        except KeyError as exc:
            raise ValueError(f"Unknown copilot tool: {name}") from exc
        return tool(**arguments)


ai_copilot = AICopilot()
__all__ = ["AICopilot", "ai_copilot"]
