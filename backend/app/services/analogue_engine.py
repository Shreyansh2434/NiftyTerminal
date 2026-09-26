"""Deterministic nearest-neighbour analogue search; no model or network required."""
from __future__ import annotations

import math
from typing import Any


class AnalogueEngine:
    def find(
        self,
        current: dict[str, Any],
        history: list[dict[str, Any]] | None = None,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        history = history or []
        if limit < 1:
            return []
        keys = sorted(set(current) & {key for row in history for key in row})
        numeric = [key for key in keys if isinstance(current.get(key), (int, float))]
        if not numeric:
            return []
        scored = []
        for index, row in enumerate(history):
            distance = math.sqrt(sum((float(current[key]) - float(row.get(key, 0))) ** 2 for key in numeric))
            scored.append((distance, index, row))
        scored.sort(key=lambda item: (item[0], item[1]))
        scale = max((item[0] for item in scored), default=1.0) or 1.0
        return [
            {
                **row,
                "regime": row.get("regime", "UNCLASSIFIED"),
                "distance": round(distance, 6),
                "similarity": round(max(0.0, 1.0 - distance / scale), 6),
                "similarity_percent": round(max(0.0, 1.0 - distance / scale) * 100, 2),
                "forward_returns": {
                    "5_sessions": row.get("forward_5", None),
                    "10_sessions": row.get("forward_10", None),
                    "30_sessions": row.get("forward_30", None),
                },
            }
            for distance, _, row in scored[:limit]
        ]

    # Common descriptive alias used by API clients.
    def find_analogues(self, current: dict[str, Any], history: list[dict[str, Any]] | None = None, limit: int = 5) -> list[dict[str, Any]]:
        return self.find(current, history, limit)


analogue_engine = AnalogueEngine()

__all__ = ["AnalogueEngine", "analogue_engine"]
