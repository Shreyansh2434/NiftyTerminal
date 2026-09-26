# Phase 4 safety and operational boundary

Phase 4 is **paper-first**. The API and desktop client use deterministic,
offline data and the `PaperBroker`; no network broker order is submitted.
`TRADING_MODE=paper`, `LIVE_TRADING_ENABLED=false`, and `KILL_SWITCH_ACTIVE=true`
are the safe defaults.

Any future broker adapter must be supplied explicitly to `ExecutionEngine` and
must pass all of these gates: `TRADING_MODE=live`,
`LIVE_TRADING_ENABLED=true`, `LIVE_TRADING_CONFIRMATION=I_UNDERSTAND_LIVE_TRADING`,
`KILL_SWITCH_ACTIVE=false`, configured broker credentials, and independently
verified operational limits. A connector must not be enabled by a UI toggle
alone. Idempotency keys, audit persistence, monitoring, reconciliation,
broker-specific compliance, credentials management, and incident runbooks
remain external production controls and are not claimed as complete here.

Use `GET /api/execution/preview` to inspect risk checks and
`POST /api/execution/paper` for a deterministic fill. Never point a connector
at a live account without a separate review and kill-switch procedure.
