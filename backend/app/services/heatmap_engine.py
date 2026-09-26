"""Market heatmap transformations shared by API and desktop clients."""
from __future__ import annotations

from typing import Any, Iterable


class HeatmapEngine:
    def build(self, quotes: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted([
            {
                "symbol": quote.get("symbol"), "name": quote.get("name"),
                "sector": quote.get("sector", "OTHER"),
                "value": quote.get("change_percent", 0), "price": quote.get("price"),
                "volume": quote.get("volume", 0),
            }
            for quote in quotes
        ], key=lambda item: float(item["value"] or 0), reverse=True)


heatmap_engine = HeatmapEngine()
