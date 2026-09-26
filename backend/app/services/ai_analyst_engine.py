"""Explainable rule-based market analyst; intentionally no LLM dependency."""
from __future__ import annotations

from typing import Any


class AIAnalystEngine:
    def analyze(self, snapshot: dict[str, Any], sentiment: dict[str, Any], sectors: list[dict[str, Any]]) -> dict[str, Any]:
        assets = snapshot.get("assets", [])
        breadth = sum(float(asset.get("change_percent") or 0) >= 0 for asset in assets)
        total = max(len(assets), 1)
        score = sum(float(asset.get("change_percent") or 0) for asset in assets) / total
        if score > 0.15 and breadth / total >= 0.55:
            stance, confidence = "RISK-ON", min(0.95, 0.55 + breadth / total * 0.35)
        elif score < -0.15 and breadth / total <= 0.45:
            stance, confidence = "RISK-OFF", min(0.95, 0.55 + (1 - breadth / total) * 0.35)
        else:
            stance, confidence = "SELECTIVE", 0.52
        leaders = sorted(sectors, key=lambda item: item.get("return_pct", 0), reverse=True)
        return {
            "stance": stance, "confidence": round(confidence, 3),
            "summary": f"{stance.title()} conditions with {breadth}/{total} assets advancing.",
            "signals": [
                {"name": "Breadth", "value": f"{breadth}/{total}", "rationale": "Advancing assets versus total universe"},
                {"name": "Sentiment", "value": sentiment.get("label", "NEUTRAL"), "rationale": "Lexicon-scored market headlines"},
                {"name": "Leadership", "value": leaders[0]["sector"] if leaders else "—", "rationale": "Best performing sector"},
            ],
            "disclaimer": "Rule-based research aid; not financial advice.",
        }


ai_analyst_engine = AIAnalystEngine()
