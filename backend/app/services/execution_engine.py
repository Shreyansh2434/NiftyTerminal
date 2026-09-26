"""Paper-first execution boundary.

The Broker protocol is deliberately tiny: a future adapter must implement it and
still pass the explicit live-trading gates in ``ExecutionEngine``.
"""
from __future__ import annotations

import hashlib
import threading
from datetime import datetime, timezone
from typing import Protocol

from app.core.config import get_settings
from app.services.risk_engine import RiskEngine


class Broker(Protocol):
    def submit(self, order: dict) -> dict: ...


class PaperBroker:
    """Deterministic broker that never performs network I/O."""

    def submit(self, order: dict) -> dict:
        seed = f"{order['symbol']}:{order['side']}:{order['quantity']}:{order.get('price', 0)}"
        execution_id = "paper-" + hashlib.sha256(seed.encode()).hexdigest()[:16]
        return {
            "execution_id": execution_id,
            "status": "filled",
            "average_price": round(float(order.get("price", 0)), 4),
            "mode": "paper",
            "filled_quantity": int(order["quantity"]),
            "executed_at": datetime.now(timezone.utc).isoformat(),
        }


class ExecutionEngine:
    def __init__(self, broker: Broker | None = None) -> None:
        self.settings = get_settings()
        self.risk = RiskEngine()
        self.paper_broker = PaperBroker()
        self._broker = broker
        self._orders: dict[str, dict] = {}
        self._audit: list[dict] = []
        self._lock = threading.Lock()

    def preview(self, order: dict) -> dict:
        normalized = self._normalize(order)
        decision = self.risk.check_order(
            symbol=normalized["symbol"], side=normalized["side"],
            quantity=normalized["quantity"], price=normalized["price"],
        )
        mode = normalized["mode"]
        live_gate = self._live_gate()
        return {
            "accepted": decision.allowed and (mode == "paper" or live_gate["allowed"]),
            "mode": mode,
            "order": normalized,
            "risk_checks": decision.checks,
            "reasons": decision.reasons + ([] if mode == "paper" or live_gate["allowed"] else [live_gate["reason"]]),
            "live_gate": live_gate,
            "paper_only": True,
        }

    def execute_paper(self, order: dict) -> dict:
        normalized = self._normalize({**order, "mode": "paper"})
        with self._lock:
            if normalized["client_order_id"] in self._orders:
                return self._orders[normalized["client_order_id"]]
            preview = self.preview(normalized)
            if not preview["accepted"]:
                result = {"status": "rejected", **preview}
            else:
                result = {"status": "filled", **preview, "broker_response": self.paper_broker.submit(normalized)}
            self._orders[normalized["client_order_id"]] = result
            self._audit.append({"event_type": "paper_execution", "payload": result, "created_at": datetime.now(timezone.utc).isoformat()})
            return result

    # Stable service names for API and desktop integrations.
    def preview_order(self, order: dict) -> dict:
        return self.preview(order)

    def execute_order(self, order: dict) -> dict:
        return self.execute_paper(order)

    def audit_records(self) -> list[dict]:
        return list(self._audit)

    def _normalize(self, order: dict) -> dict:
        return {
            "client_order_id": str(order.get("client_order_id") or hashlib.sha256(repr(sorted(order.items())).encode()).hexdigest()[:24]),
            "symbol": str(order.get("symbol", "NIFTY")).upper(),
            "side": str(order.get("side", "BUY")).upper(),
            "quantity": int(order.get("quantity", 1)),
            "price": float(order.get("price", order.get("limit_price", 0) or 0)),
            "order_type": str(order.get("order_type", "MARKET")).upper(),
            "mode": str(order.get("mode", self.settings.trading_mode)).lower(),
        }

    def _live_gate(self) -> dict[str, bool | str]:
        confirmation = "I_UNDERSTAND_LIVE_TRADING"
        allowed = (
            self.settings.live_trading_enabled
            and self.settings.trading_mode.lower() == "live"
            and self.settings.live_trading_confirmation == confirmation
            and not self.settings.kill_switch_active
            and self._broker is not None
        )
        reason = "Live trading is disabled by default; paper broker selected."
        if self.settings.kill_switch_active:
            reason = "Kill switch is active."
        elif self._broker is None:
            reason = "No broker connector is configured."
        return {"allowed": allowed, "reason": reason, "confirmation_required": confirmation}


execution_engine = ExecutionEngine()
