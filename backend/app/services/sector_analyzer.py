"""Sector breadth and relative-performance analysis."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


class SectorAnalyzer:
    def analyze(self, quotes: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for quote in quotes:
            groups[str(quote.get("sector", "OTHER"))].append(quote)
        result = []
        for sector, items in sorted(groups.items()):
            changes = [float(item.get("change_percent") or 0) for item in items]
            result.append({
                "sector": sector, "return_pct": round(sum(changes) / max(len(changes), 1), 3),
                "advance_count": sum(change >= 0 for change in changes),
                "decline_count": sum(change < 0 for change in changes),
                "constituents": [item.get("symbol") for item in items],
            })
        return result


sector_analyzer = SectorAnalyzer()
