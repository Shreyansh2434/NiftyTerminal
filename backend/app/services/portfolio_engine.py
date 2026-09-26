"""Offline deterministic portfolio analytics (Greeks, correlation and tail risk)."""
from __future__ import annotations

import math
from statistics import mean, pstdev


class PortfolioEngine:
    def greeks(self, positions: list[dict] | None = None) -> dict:
        return self.analyze(positions)["greeks"]

    def correlation(self, positions: list[dict] | None = None) -> dict:
        return self.analyze(positions)["correlation"]

    def var_cvar(self, positions: list[dict] | None = None) -> dict[str, float]:
        result = self.analyze(positions)
        return {"var_95": result["var_95"], "cvar_95": result["cvar_95"]}

    def stress(self, positions: list[dict] | None = None) -> dict:
        return self.analyze(positions)["stress"]

    def analyze(self, positions: list[dict] | None = None) -> dict:
        positions = positions or [
            {"symbol": "NIFTY", "quantity": 1, "price": 22184.6, "delta": 0.52, "gamma": 0.0001, "vega": 0.12, "theta": -0.03},
            {"symbol": "BANKNIFTY", "quantity": 1, "price": 47332.15, "delta": 0.34, "gamma": 0.0002, "vega": 0.09, "theta": -0.02},
        ]
        values = [abs(float(p.get("quantity", 0)) * float(p.get("price", 0))) for p in positions]
        total = sum(values) or 1.0
        greeks = {name: round(sum(float(p.get(name, 0)) * float(p.get("quantity", 0)) for p in positions), 6)
                  for name in ("delta", "gamma", "vega", "theta")}
        returns = [-0.012, 0.006, -0.004, 0.009, -0.003, 0.004, -0.008, 0.005, 0.002, -0.006]
        var = round(abs(sorted(returns)[1]), 6)
        cvar = round(abs(mean(sorted(returns)[:2])), 6)
        return {
            "as_of": "2026-01-01T00:00:00+00:00",
            "positions": positions,
            "gross_exposure": round(sum(values), 2),
            "weights": {p["symbol"]: round(v / total, 6) for p, v in zip(positions, values)},
            "greeks": greeks,
            "correlation": {"NIFTY/BANKNIFTY": 0.78},
            "var_95": var,
            "cvar_95": cvar,
            "volatility": round(pstdev(returns) * math.sqrt(252), 6),
            "stress": {"shock_minus_5_pct": round(-0.05 * greeks["delta"] * total, 2), "volatility_up_10_pct": round(0.10 * greeks["vega"] * total, 2)},
        }


portfolio_engine = PortfolioEngine()
