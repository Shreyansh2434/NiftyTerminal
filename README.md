# NIFTY Options Intelligence Terminal — Phase 3

A resilient NIFTY index-options dashboard. The API is a FastAPI application with
async SQLAlchemy/PostgreSQL persistence and an optional background refresh loop.
The Vite/React client displays the latest cached snapshot and clearly explains
when the database or market-data provider is unavailable.

## Project layout

```text
backend/
  app/
    core/        settings and logging
    db/          async engine, models and repositories
    models/      API and persistence compatibility models
    schemas/     Pydantic API schemas
    routers/     health, market, options and analytics APIs
    services/    data adapter, calculations and Phase 1 module services
    scheduler.py
    main.py
  scripts/init_db.py
scripts/
  setup_db.py
  backfill_ohlcv.py
  backfill_iv.py
  build_executable.py
ui/
  main.py
  windows/       native Trading and Backtest windows
  widgets/       dashboard, configuration, metrics and trade widgets
  workers/       QThread-compatible backtest worker
  dialogs/       configuration and settings dialogs
  styles/        terminal palette and QSS
  utils/         display formatting
alembic/
  versions/
frontend/
  src/
    components/
    hooks/
    lib/
    pages/
    App.tsx
requirements.txt
backend/requirements.txt
alembic.ini
```

## Local development

1. Copy `.env.example` to `.env` and set `DATABASE_URL` if PostgreSQL is
   available. The API remains usable without a database.
2. Install the backend requirements: `pip install -r requirements.txt` (or
   `pip install -r backend/requirements.txt`).
3. Initialize the database with `python scripts/setup_db.py`, or apply the
   checked-in Alembic migration with `alembic upgrade head`.
4. Start the API: `uvicorn app.main:app --reload --app-dir backend`.
5. Install and run the client:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The client defaults to `http://localhost:8000`. Set `VITE_API_BASE_URL` to
point it at another API.

## Phase 3 multi-asset workspace

Phase 3 adds a deterministic multi-asset universe and a complete offline-safe
vertical slice. The aggregator exposes quotes/history for equities and indices,
with the optional live providers retained as a future source layer and a
stable fallback for disconnected development. New endpoints are available at
`/api/v1/market/assets`, `/api/v1/market/heatmap`,
`/api/v1/market/workspace`, `/api/v1/sentiment`, `/api/v1/sectors`, and
`/api/v1/backtests/multi-asset/run` (the equivalent `/api` paths are retained).
Backtest results include aggregate, per-asset, per-sector, and per-regime
metrics. Open `/phase3` for the React workspace or use the desktop Trading tab
for the Bloomberg-style navigator. No new network or API-key dependency is
required; all Phase 3 sample data is reproducible offline.

## API

- `GET /api/options`
- `GET /api/iv`
- `GET /api/regime`
- `GET /api/notrade`
- `GET /api/health`
- `GET /api/ready`
- `GET /api/instruments`
- `GET /api/v1/health`
- `GET /api/v1/market/spot`
- `GET /api/v1/options/chain?symbol=NIFTY`
- `GET /api/v1/analytics/summary?symbol=NIFTY`
- `GET /api/v1/analytics/heatmap?symbol=NIFTY`
- `GET /api/v1/analytics/max-pain?symbol=NIFTY`
- `GET /api/v1/analytics/oi-changes?symbol=NIFTY`
- `GET /api/v1/analytics/signals?symbol=NIFTY`
- `POST /api/backtest/run`
- `GET /api/backtest/run/{run_id}`
- `GET /api/backtest/run/{run_id}/trades`
- `GET /api/backtest/compare?run_ids=<id>,<id>`

Phase 2 adds a deterministic, resilient, signal-driven walk-forward engine.
It classifies each day from completed prior bars, uses directional put/call
spreads for low-IV trends and iron condors for low-IV ranges, and skips
non-qualifying signals. It models quoted bid/ask spreads, adverse slippage,
lot-size/wing-width risk and per-contract commissions, and reports equity,
drawdown, Sharpe, walk-forward folds, and per-regime results. Open
`/backtest` in the client to run the seeded sample configuration. If the
database or historical vendor is unavailable, the API runs against a
deterministic synthetic fallback history and keeps the illustrative result in
memory with a clear warning.
Apply the `0002_backtest` Alembic migration (or run
`python backend/scripts/seed_backtest.py` after `create_all`) to persist the
configuration and results.

Market data is fetched from NSE first and yfinance is used for the spot
fallback. Requests are cached in memory and return a valid empty
payload instead of failing when an upstream service is blocked or offline.
The `/api/v1` routes are retained for existing clients; the short `/api`
routes are the Phase 1 contract.

## Native desktop client

The optional PyQt6 client runs the pure backtest engine directly, without
HTTP or a running PostgreSQL server. From the repository root, install the
desktop dependencies and launch it with:

```bash
pip install -r requirements-dev.txt
python -m ui.main
```

The Trading, Backtest, and Execution / Risk tabs remain available when live
data or PostgreSQL is unavailable; the Backtest tab uses the deterministic
synthetic history fallback and the Execution / Risk tab is paper-only. Run
`python scripts/smoke_desktop.py` for a dependency-safe import check (or an
offscreen Qt widget check when Qt is installed). To package a Windows
executable, run:

```bash
python scripts/build_executable.py
```

The native shell uses a dense Bloomberg-style design system: a fixed 180px
market navigator, compact tabs and tables, strict dark/gold palette, global
market ticker, live local clock, and a persistent paper-mode/risk status bar.

The spec-named widget, dialog, and worker modules are compatibility entry
points over the consolidated implementation, so either import layout remains
supported.

## Phase 4 production-grade safety layer

Open `/phase4` for the chart, volume profile, order flow, portfolio Greeks,
risk, compliance and execution panels. Phase 4 adds paper-only execution
preview/fills (`/api/execution/preview`, `/api/execution/paper`), deterministic
portfolio/risk and chart endpoints, append-only audit models, and migration
`0005_phase4_execution_risk`. No live broker adapter is included or enabled.
The explicit flags, confirmation token and kill-switch requirements for any
future connector are documented in `docs/PHASE4_SAFETY.md`.

## Phase 5 operational readiness

Phase 5 begins with production observability and safe deployment boundaries.
`GET /api/ready` reports API availability, optional database connectivity, and
the paper-trading safety defaults without enabling live execution. A database
failure is reported as a degraded dependency rather than hiding the condition
or preventing the offline-safe terminal from starting. Live broker
connectivity remains intentionally out of scope until a broker, credentials
policy, compliance jurisdiction, and independent operational review are
specified.

## Phase 6 AI research copilot

Open `/ai` (or `/copilot`) for the terminal-style AI research workspace.
Available backend routes include `GET /api/ai/copilot`, `POST
/api/ai/copilot/query`, `POST /api/ai/tool`, `POST /api/ai/monte-carlo`, and
`POST /api/ai/analogues`. The local tool registry exposes quote, options,
backtest, and Monte Carlo research tools. These tools are deterministic and
read-only by default; they cannot place orders or enable a broker connector.

`POST /api/ai/fin-sql` converts supported natural-language regime questions to
parameterized read-only SQL and returns confidence metadata. SQL execution is
opt-in with `{"execute": true}` and requires a healthy database session.
Mutations, comments, multiple statements, and unsupported patterns are
rejected before execution.

## Formula notes

- **PCR** = total put open interest / total call open interest.
- **Max pain** is the strike with the minimum total option payout at expiry:
  `sum(call_oi * max(0, settlement - strike) + put_oi * max(0, strike - settlement))`.
- **OI change** is current OI minus the previous snapshot.
- **Put/Call weighted levels** use OI-weighted strikes and are omitted when the
  relevant side has no OI.
