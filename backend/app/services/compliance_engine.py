"""Compliance summaries over the append-only execution audit stream."""
from __future__ import annotations

from datetime import datetime, timezone


class ComplianceEngine:
    def __init__(self) -> None:
        self._records: list[dict] = []

    def record(self, event_type: str, payload: dict, actor: str = "system", correlation_id: str | None = None) -> dict:
        record = {
            "event_type": event_type, "actor": actor, "correlation_id": correlation_id,
            "payload": payload, "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._records.append(record)
        return record

    def records(self) -> list[dict]:
        return list(self._records)

    def summary(self) -> dict:
        events = len(self._records)
        rejected = sum(1 for r in self._records if r["event_type"].endswith("rejected"))
        return {"total_events": events, "rejected_events": rejected, "paper_only": True, "live_orders": 0, "status": "COMPLIANT" if rejected == 0 else "REVIEW_REQUIRED"}

    def compliance_summary(self) -> dict:
        return self.summary()


compliance_engine = ComplianceEngine()
