"""Deterministic sentiment scoring for market headlines."""
from __future__ import annotations

from typing import Any, Iterable

POSITIVE = {"beat", "growth", "surge", "strong", "upgrade", "inflow", "record", "eases"}
NEGATIVE = {"miss", "fall", "weak", "downgrade", "outflow", "risk", "inflation", "slump"}


class SentimentEngine:
    def analyze(self, headlines: Iterable[str] | None = None, symbol: str = "MARKET") -> dict[str, Any]:
        items = list(headlines or [
            "Institutional inflow supports strong market breadth",
            "Technology earnings growth remains resilient",
            "Global inflation risk keeps volatility elevated",
        ])
        scores = []
        for headline in items:
            words = {word.strip(".,:;!?()").lower() for word in headline.split()}
            scores.append((len(words & POSITIVE) - len(words & NEGATIVE)) / 3)
        score = max(-1.0, min(1.0, sum(scores) / max(len(scores), 1)))
        label = "BULLISH" if score > 0.15 else "BEARISH" if score < -0.15 else "NEUTRAL"
        return {"symbol": symbol.upper(), "score": round(score, 3), "label": label,
                "confidence": round(min(1.0, 0.45 + abs(score) * 0.5), 3),
                "headlines": [{"text": text, "score": round(value, 3)} for text, value in zip(items, scores)],
                "source": "rule-based-offline"}


sentiment_engine = SentimentEngine()
