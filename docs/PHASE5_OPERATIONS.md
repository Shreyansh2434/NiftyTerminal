# Phase 5 operations

Phase 5 starts with an observable, safe deployment boundary around the
paper-first terminal.

## Readiness

Use the following endpoints after starting the API:

- `GET /api/health` — liveness and dependency summary.
- `GET /api/ready` — operational checks and safety configuration.
- `GET /api/v1/ready` — versioned alias.

The database is optional for the offline-safe application. A database
connection failure is therefore reported in the response instead of causing a
false healthy dependency or preventing local research workflows.

## Safety gate

The readiness response reports `paper_safety_defaults` as true only when:

- `TRADING_MODE=paper`
- `LIVE_TRADING_ENABLED=false`
- `KILL_SWITCH_ACTIVE=true`

Readiness is marked `attention_required` when those defaults are changed. This
does not activate live execution; broker connectivity, credentials, audit
reconciliation, monitoring, and compliance review are still required before
any live connector can be considered.

## Local verification

From the project root:

```powershell
$env:PYTHONPATH = "$PWD\backend"
& ".venv\Scripts\python.exe" -c "from fastapi.testclient import TestClient; from app.main import app; print(TestClient(app).get('/api/ready').json())"
```
