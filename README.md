<div align="center">
<br/>

# 📈 NIFTY Options Intelligence Terminal

### *Real-Time Options Analytics • AI Research Copilot • Walk-Forward Backtesting • Self-Sovereign Execution Safety*

<br/>
[![Live Frontend](https://img.shields.io/badge/FRONTEND-VITE%2FREACT-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://claude.ai/new?incognito=#-live-deployment)
[![Backend API](https://img.shields.io/badge/BACKEND%20API-FASTAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://claude.ai/new?incognito=#-api-reference)
[![GitHub](https://img.shields.io/badge/SOURCE%20CODE-GITHUB-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shreyansh2434/NiftyTerminal)
[![Health](https://img.shields.io/badge/API%20HEALTH-STATUS-brightgreen?style=for-the-badge)](https://claude.ai/new?incognito=#-api-reference)

<br/>
![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_18-61DAFB?style=flat-square&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migration-6BA539?style=flat-square)
![PyQt6](https://img.shields.io/badge/PyQt6-Desktop-41CD52?style=flat-square&logo=qt&logoColor=white)
![NSE](https://img.shields.io/badge/NSE-Market%20Data-0066CC?style=flat-square)
![yfinance](https://img.shields.io/badge/yfinance-Fallback-8B00FF?style=flat-square)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=flat-square)

</div>

---

## 📌 Table of Contents

#
Section

01
[What This System Solves](https://claude.ai/new?incognito=#-what-this-system-solves)

02
[System at a Glance](https://claude.ai/new?incognito=#-system-at-a-glance)

03
[Live Deployment](https://claude.ai/new?incognito=#-live-deployment)

04
[Phase Roadmap](https://claude.ai/new?incognito=#-phase-roadmap)

05
[System Architecture](https://claude.ai/new?incognito=#-system-architecture)

06
[Project Structure](https://claude.ai/new?incognito=#-project-structure)

07
[Key Features](https://claude.ai/new?incognito=#-key-features)

08
[Tech Stack](https://claude.ai/new?incognito=#-tech-stack)

09
[Installation & Setup](https://claude.ai/new?incognito=#-installation--setup)

10
[Environment Configuration](https://claude.ai/new?incognito=#-environment-configuration)

11
[Database Setup & Migrations](https://claude.ai/new?incognito=#-database-setup--migrations)

12
[API Reference](https://claude.ai/new?incognito=#-api-reference)

13
[Backtesting Engine](https://claude.ai/new?incognito=#-backtesting-engine)

14
[AI Research Copilot](https://claude.ai/new?incognito=#-ai-research-copilot)

15
[Native Desktop Client](https://claude.ai/new?incognito=#-native-desktop-client)

16
[Formula Reference](https://claude.ai/new?incognito=#-formula-reference)

17
[Safety & Compliance](https://claude.ai/new?incognito=#-safety--compliance)

18
[Contributing](https://claude.ai/new?incognito=#-contributing)

---

## 🚨 What This System Solves

> **Retail options traders are forced to use fragmented, opaque, and expensive tools to trade NIFTY — or fly blind.** This terminal provides institutional-grade options intelligence, AI-assisted research, and a safety-first execution layer — entirely open and offline-capable.

Challenge
Industry Status Quo
This Terminal

**Options Chain Visibility**
🔒 Paywalled or delayed feeds
✅ Live + cached + offline fallback

**Backtesting Realism**
📉 Ignores slippage and spreads
✅ Bid/ask spread, slippage, commissions baked in

**Market Regime Logic**
🎲 Manual gut-call
✅ Automated signal-driven regime classification

**AI Trade Research**
💸 Costly third-party copilots
✅ Built-in AI copilot with read-only tool access

**Execution Safety**
⚠️ One-click live orders with no guardrails
✅ Paper-only default; live requires explicit flags + kill switch

**Offline Resilience**
❌ Crashes without internet
✅ Deterministic synthetic fallback at every layer

**Observability & Readiness**
📝 Logs buried in files
✅ `/api/ready` degraded-dependency reporting

---

## 📊 System at a Glance

Attribute
Detail

**Project Type**
Institutional-grade NIFTY index options analytics & research terminal

**Market Coverage**
NIFTY 50 (extensible to Sensex, BankNIFTY, equities)

**Data Sources**
NSE (primary) → yfinance (spot fallback) → Deterministic synthetic data

**Backend**
FastAPI + async SQLAlchemy + PostgreSQL (or in-memory offline mode)

**Frontend**
React 18 + Vite + TypeScript

**Desktop Client**
PyQt6 — Bloomberg-style native terminal, no HTTP dependency

**Backtest Engine**
Signal-driven walk-forward; iron condors, put/call spreads, regime logic

**AI Copilot**
Local tool registry (quote, options, backtest, Monte Carlo) — read-only

**Execution Mode**
Paper-only default; no live broker adapter shipped

**Offline Safety**
Every layer has a deterministic fallback — terminal never hard-crashes

**Current Phase**
Phase 6 (AI Research Copilot)

---

## 🌐 Live Deployment

Service
Status
URL / Command

⚡ **Backend API**
🟢 Active
`uvicorn app.main:app --reload --app-dir backend`

🌐 **Frontend Dev Server**
🟢 Active
`cd frontend && npm run dev` → `localhost:5173`

🏥 **Health Check**
⚡ Monitor
`GET /api/health` / `GET /api/ready`

🖥️ **Desktop App**
🟢 Active
`python -m ui.main`

📦 **Source Code**
GitHub
[Shreyansh2434/NiftyTerminal](https://github.com/Shreyansh2434/NiftyTerminal)

---

## 🗺 Phase Roadmap

> This terminal was built in six production-hardened phases. Each phase is independently deployable and backward-compatible.

Phase
Name
Status
Key Additions

**1**
Core Options Dashboard
✅ Complete
Options chain, IV, PCR, regime signals, health API, React frontend

**2**
Walk-Forward Backtest Engine
✅ Complete
Signal-driven backtest, spreads/condors, slippage, Sharpe, drawdown

**3**
Multi-Asset Workspace
✅ Complete
Equity universe, heatmaps, sector analytics, per-regime backtest results

**4**
Production Safety Layer
✅ Complete
Paper execution, portfolio Greeks, compliance, audit models, kill switch

**5**
Operational Readiness
✅ Complete
`/api/ready` degraded reporting, observability, safe deployment gates

**6**
AI Research Copilot
✅ Complete
Terminal AI workspace, Monte Carlo, analogues, FinSQL, tool registry

---

## 🏗 System Architecture

```
  NSE / yfinance                  Deterministic Synthetic Fallback
       |                                      |
       +-------------- Data Aggregator -------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
         +---------+   +-----------+   +-----------+
         | Market  |   | Options   |   | Backtest  |
         |  API    |   | Chain API |   |  Engine   |
         +---------+   +-----------+   +-----------+
              |               |               |
              +---------------+---------------+
                              |
               +--------------+-------------+
               |                            |
               v                            v
       +----------------+         +------------------+
       | Analytics Layer|         |  AI Copilot Layer|
       | Regime Signals |         |  Tool Registry   |
       | Max Pain / PCR |         |  FinSQL Engine   |
       | OI Heatmaps    |         |  Monte Carlo     |
       +----------------+         +------------------+
               |                            |
               +------------+---------------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
       +----------+  +----------+  +-----------+
       |FASTAPI   |  |Async SQLA|  |Alembic    |
       |REST API  |  |PostgreSQL|  |Migrations |
       +----------+  +----------+  +-----------+
              |
   +----------+----------+
   |                     |
   v                     v
+----------+      +-----------+
|React +   |      |  PyQt6    |
|Vite SPA  |      |  Desktop  |
|(Browser) |      | Terminal  |
+----------+      +-----------+
```

---

## 📁 Project Structure

```
NiftyTerminal/
│
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 core/            Settings, logging, config
│   │   ├── 📂 db/              Async engine, models, repositories
│   │   ├── 📂 models/          API & persistence compatibility models
│   │   ├── 📂 schemas/         Pydantic API schemas
│   │   ├── 📂 routers/
│   │   │   ├── 📄 health.py    /api/health, /api/ready
│   │   │   ├── 📄 market.py    /api/v1/market/*
│   │   │   ├── 📄 options.py   /api/v1/options/*
│   │   │   └── 📄 analytics.py /api/v1/analytics/*
│   │   ├── 📂 services/
│   │   │   ├── 📄 data_adapter.py      NSE + yfinance + synthetic fallback
│   │   │   ├── 📄 calculations.py      PCR, Max Pain, OI deltas
│   │   │   ├── 📄 backtest.py          Walk-forward engine
│   │   │   └── 📄 ai_copilot.py        Tool registry + FinSQL
│   │   ├── 📄 scheduler.py     Background data refresh loop
│   │   └── 📄 main.py          FastAPI app entry point
│   ├── 📂 scripts/
│   │   ├── 📄 init_db.py
│   │   ├── 📄 seed_backtest.py
│   │   └── 📄 smoke_desktop.py
│   └── 📄 requirements.txt
│
├── 📂 frontend/                 Vite + React + TypeScript SPA
│   └── 📂 src/
│       ├── 📂 components/       Options chain, heatmap, charts
│       ├── 📂 hooks/            API data hooks
│       ├── 📂 lib/              API client, formatters
│       ├── 📂 pages/
│       │   ├── 📄 index.tsx     Main dashboard (Phase 1)
│       │   ├── 📄 backtest.tsx  Backtest runner (Phase 2)
│       │   ├── 📄 phase3.tsx    Multi-asset workspace
│       │   ├── 📄 phase4.tsx    Execution & risk panels
│       │   └── 📄 ai.tsx        AI copilot terminal
│       └── 📄 App.tsx
│
├── 📂 ui/                       PyQt6 Native Desktop Client
│   ├── 📂 windows/              Trading & Backtest windows
│   ├── 📂 widgets/              Dashboard, metrics, trade widgets
│   ├── 📂 workers/              QThread backtest worker
│   ├── 📂 dialogs/              Config & settings dialogs
│   ├── 📂 styles/               Dark/gold terminal palette + QSS
│   ├── 📂 utils/                Display formatters
│   └── 📄 main.py               App entry point
│
├── 📂 alembic/
│   └── 📂 versions/
│       ├── 📄 0001_initial.py
│       ├── 📄 0002_backtest.py
│       └── 📄 0005_phase4_execution_risk.py
│
├── 📂 scripts/
│   ├── 📄 setup_db.py
│   ├── 📄 backfill_ohlcv.py
│   ├── 📄 backfill_iv.py
│   └── 📄 build_executable.py
│
├── 📄 .env.example
├── 📄 alembic.ini
├── 📄 requirements.txt
├── 📄 requirements-dev.txt
└── 📄 README.md
```

---

## ✨ Key Features

### 📡 Phase 1 — Options Intelligence Core

Feature
Description

📊 **Live Options Chain**
Real-time NIFTY options chain with OI, IV, PCR, and greeks

📈 **Regime Signals**
Automated market regime classification: trend / range / undefined

🔥 **Max Pain Strike**
OI-weighted max pain calculation updated each snapshot

♻️ **OI Change Tracking**
Current vs previous snapshot open interest delta per strike

✅ **Offline Fallback**
NSE → yfinance → deterministic synthetic data; never a hard API failure

🏥 **Health Endpoints**
`/api/health` (API up) and `/api/ready` (database + dependency status)

### 🔁 Phase 2 — Walk-Forward Backtest Engine

Feature
Description

🧠 **Signal-Driven Entry**
Classifies day from prior completed bars before entry decision

🎯 **Strategy Selection**
Iron condors for low-IV ranges; put/call spreads for low-IV trends

💸 **Realistic Cost Model**
Bid/ask spread, adverse slippage, lot-size risk, per-contract commissions

📊 **Metrics Suite**
Equity curve, max drawdown, Sharpe ratio, walk-forward fold results

🛡️ **No-Trade Days**
`/api/notrade` signals days that fail regime/IV qualification

🧪 **Synthetic Fallback**
Seeded synthetic history used when market data is unavailable

### 🌐 Phase 3 — Multi-Asset Workspace

Feature
Description

📋 **Asset Universe**
Deterministic multi-asset equity and index quotes/history

🗺 **Sector Heatmap**
OI-weighted sector-level exposure visualization

🏢 **Workspace API**
`/api/v1/market/workspace` — unified market state for all assets

📉 **Per-Regime Metrics**
Backtest results broken down by asset, sector, and regime

🖥️ **Desktop Navigator**
Bloomberg-style 180px market navigator panel in PyQt6 client

### 🛡️ Phase 4 — Production Safety Layer

Feature
Description

📋 **Paper Execution**
`/api/execution/preview` and `/api/execution/paper` — paper-only fills only

📐 **Portfolio Greeks**
Delta, Gamma, Theta, Vega across the full portfolio

🔒 **Compliance Layer**
Append-only audit models; no trade mutation post-entry

☠️ **Kill Switch**
Documented explicit-flag + confirmation token + kill-switch requirement

📖 **Safety Docs**
`docs/PHASE4_SAFETY.md` — full live-connector enablement requirements

### 📡 Phase 5 — Operational Readiness

Feature
Description

🩺 **Degraded Reporting**
`/api/ready` reports DB unavailable as degraded, not a 500

🔭 **Observability**
Structured logging, request tracing, startup dependency checks

🚦 **Safe Deployment Gate**
Paper-trading safety defaults enforced at boot

🧰 **No Live Broker**
Live broker connectivity explicitly out of scope until jurisdictional review

### 🤖 Phase 6 — AI Research Copilot

Feature
Description

💬 **Copilot Terminal**
Terminal-style AI workspace at `/ai` (or `/copilot`)

🧰 **Tool Registry**
Local read-only tools: quote, options chain, backtest, Monte Carlo

📊 **Monte Carlo Simulation**
`/api/ai/monte-carlo` — P&L distribution analysis

📚 **Market Analogues**
`/api/ai/analogues` — historical regime comparisons

🗄️ **FinSQL Engine**
Natural language → parameterized read-only SQL with confidence metadata

🔒 **Copilot Safety**
All tools are read-only; cannot place orders or enable broker connector

---

## 🛠 Tech Stack

Layer
Technology
Purpose

**Language (Backend)**
Python 3.11+
Async API, backtest engine, data services

**API Framework**
FastAPI
High-performance async REST API

**ASGI Server**
Uvicorn
Production-grade async server

**ORM**
SQLAlchemy (async)
Async database access and migrations

**Migrations**
Alembic
Schema version control

**Database**
PostgreSQL
Persistent storage (optional — fully offline-safe)

**Language (Frontend)**
TypeScript
Type-safe React components

**Frontend Framework**
React 18
Component-based UI

**Build Tool**
Vite
Fast development server and bundler

**Desktop Framework**
PyQt6
Native Bloomberg-style terminal client

**Market Data (Live)**
NSE API
Primary NIFTY data source

**Market Data (Fallback)**
yfinance
Spot price fallback

**Synthetic Data**
Deterministic Seeded
Fully offline development and CI

**Validation**
Pydantic v2
Schema validation and serialization

**Config**
python-dotenv
Environment configuration management

---

## 🚀 Installation & Setup

### Prerequisites

Tool
Version
Purpose

Python
3.11+
Backend runtime

Node.js
18.x–20.x
Frontend build toolchain

PostgreSQL
14+ (opt.)
Persistent storage

npm or yarn
Latest
Frontend package management

Git
Latest
Version control

### 1. Clone the Repository

```
git clone https://github.com/Shreyansh2434/NiftyTerminal.git
cd NiftyTerminal
```

### 2. Backend Setup

```
# Install backend dependencies
pip install -r requirements.txt
# or
pip install -r backend/requirements.txt

# Start the API server
uvicorn app.main:app --reload --app-dir backend
```

**API available at:** `http://localhost:8000`

**Health check:**

```
curl http://localhost:8000/api/health
curl http://localhost:8000/api/ready
```

### 3. Frontend Setup

```
cd frontend
npm install
npm run dev
```

**Frontend available at:** `http://localhost:5173`

> The client defaults to `http://localhost:8000`. Override via `VITE_API_BASE_URL`.

### 4. Native Desktop Client (Optional)

```
# Install desktop dependencies
pip install -r requirements-dev.txt

# Run dependency/import smoke test
python scripts/smoke_desktop.py

# Launch the terminal
python -m ui.main
```

### 5. Build Windows Executable (Optional)

```
python scripts/build_executable.py
```

---

## ⚙️ Environment Configuration

### Backend — `backend/.env` (or project root `.env`)

```
# Server
NODE_ENV=development
PORT=8000

# Database (optional — API works fully without it)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/nifty_terminal

# Market Data (optional — synthetic fallback used if absent)
NSE_BASE_URL=https://www.nseindia.com

# Logging
LOG_LEVEL=debug
```

### Frontend — `frontend/.env.local`

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=NIFTY Options Intelligence Terminal
```

> **Offline-first design:** Every environment variable is optional. The terminal
> initializes and runs fully on the deterministic synthetic fallback if no
> database or market data provider is reachable.

---

## 🗄 Database Setup & Migrations

### Option A — Alembic (Recommended)

```
# Apply all migrations (creates schema from scratch)
alembic upgrade head
```

### Option B — Init Script

```
python scripts/setup_db.py
```

### Seed Backtest Data (Phase 2)

```
python backend/scripts/seed_backtest.py
```

### Migration Inventory

Migration ID
Description

`0001_initial`
Base schema: options snapshots, instruments

`0002_backtest`
Backtest configurations and result persistence

`0005_phase4_...`
Execution orders, risk snapshots, audit log

---

## 📡 API Reference

### Health & Readiness

```
GET /api/health
GET /api/ready
GET /api/v1/health
```

`/api/ready` response:

```
{
  "api": "ok",
  "database": "degraded",
  "paper_mode": true,
  "live_broker": false
}
```

### Market Data

```
GET /api/v1/market/spot
GET /api/v1/market/assets
GET /api/v1/market/heatmap
GET /api/v1/market/workspace
GET /api/instruments
```

### Options Chain

```
GET /api/v1/options/chain?symbol=NIFTY
GET /api/options
GET /api/iv
```

**Response:**

```
{
  "symbol": "NIFTY",
  "spot": 24350.75,
  "expiry": "2025-07-31",
  "chain": [
    {
      "strike": 24000,
      "call_oi": 1250000,
      "put_oi": 980000,
      "call_iv": 14.2,
      "put_iv": 13.8,
      "call_ltp": 420.5,
      "put_ltp": 310.0
    }
  ]
}
```

### Analytics

```
GET /api/v1/analytics/summary?symbol=NIFTY
GET /api/v1/analytics/heatmap?symbol=NIFTY
GET /api/v1/analytics/max-pain?symbol=NIFTY
GET /api/v1/analytics/oi-changes?symbol=NIFTY
GET /api/v1/analytics/signals?symbol=NIFTY
GET /api/regime
GET /api/notrade
```

**Max Pain Response:**

```
{
  "symbol": "NIFTY",
  "max_pain_strike": 24200,
  "method": "minimum_total_payout",
  "computed_at": "2025-07-22T09:15:00Z"
}
```

### Sentiment & Sectors (Phase 3)

```
GET /api/v1/sentiment
GET /api/v1/sectors
```

### Backtesting

```
POST /api/backtest/run
GET  /api/backtest/run/{run_id}
GET  /api/backtest/run/{run_id}/trades
GET  /api/backtest/compare?run_ids=<id>,<id>
POST /api/v1/backtests/multi-asset/run
```

**Backtest Request:**

```
{
  "symbol": "NIFTY",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "seed": 42,
  "strategy": "auto",
  "commission_per_lot": 40
}
```

**Backtest Response:**

```
{
  "run_id": "uuid-...",
  "status": "complete",
  "metrics": {
    "total_pnl": 182400,
    "max_drawdown": -24500,
    "sharpe_ratio": 1.84,
    "win_rate": 0.63,
    "total_trades": 48,
    "walk_forward_folds": 4
  },
  "regime_breakdown": {
    "trend": { "trades": 18, "pnl": 94200 },
    "range": { "trades": 30, "pnl": 88200 }
  },
  "synthetic_fallback": false
}
```

### Paper Execution (Phase 4)

```
POST /api/execution/preview
POST /api/execution/paper
```

> ⚠️ **No live broker adapter is shipped.** These endpoints are paper-only.
> Enabling a live connector requires explicit flags, a confirmation token,
> and a kill switch. See `docs/PHASE4_SAFETY.md`.

### AI Research Copilot (Phase 6)

```
GET  /api/ai/copilot
POST /api/ai/copilot/query
POST /api/ai/tool
POST /api/ai/monte-carlo
POST /api/ai/analogues
POST /api/ai/fin-sql
```

**FinSQL Request:**

```
{
  "question": "What was the average PCR during high-IV range regimes in 2024?",
  "execute": true
}
```

**FinSQL Response:**

```
{
  "sql": "SELECT AVG(pcr) FROM snapshots WHERE regime = 'range' AND iv_rank > 50 AND date BETWEEN '2024-01-01' AND '2024-12-31'",
  "confidence": 0.91,
  "result": [{ "avg_pcr": 1.14 }],
  "executed": true
}
```

> **FinSQL Safety:** Mutations, comments, multiple statements, and unsupported
> patterns are rejected before execution. `execute: true` is opt-in and requires
> a healthy database session.

---

## 📊 Backtesting Engine

The Phase 2 walk-forward engine operates on a strict signal-before-entry protocol:

### Entry Classification

Signal
Regime
IV Condition
Strategy Selected

Directional ↑↓
Trend
Low IV
Put/Call Vertical Spread

Neutral ↔
Range
Low IV
Iron Condor

No signal
Undefined
Any
No trade (skip day)

### Cost Model

Cost Component
Implementation

**Bid/Ask Spread**
Quoted spread at entry; worst-case fill modeled

**Adverse Slippage**
Configurable slippage factor per leg

**Lot Size Risk**
Enforced per NIFTY lot size

**Wing Width Risk**
Maximum loss per lot enforced before entry

**Commission**
Per-contract fee deducted each fill

### Reported Metrics

```
Equity Curve  •  Max Drawdown  •  Sharpe Ratio  •  Win Rate
Walk-Forward Fold Results  •  Per-Regime Breakdown  •  Per-Asset (Phase 3)
```

---

## 🤖 AI Research Copilot

The Phase 6 copilot provides a terminal-style AI research interface that operates
entirely within the read-only tool registry.

### Available Tools

Tool
Endpoint
Description

**Quote**
`POST /api/ai/tool`
Fetch current spot and options data

**Options Chain**
`POST /api/ai/tool`
Pull chain snapshot for a given expiry

**Backtest**
`POST /api/ai/tool`
Run seeded backtest and return metrics

**Monte Carlo**
`POST /api/ai/monte-carlo`
P&L distribution simulation

**Analogues**
`POST /api/ai/analogues`
Surface historically similar regime periods

**FinSQL**
`POST /api/ai/fin-sql`
Natural language → read-only SQL

> **Copilot cannot place orders.** It cannot enable the broker connector.
> All tools are deterministic and read-only by design.

---

## 🖥️ Native Desktop Client

The PyQt6 client runs the entire terminal natively — no browser, no HTTP server,
no PostgreSQL required. It connects directly to the backtest engine and uses the
deterministic synthetic fallback when offline.

### Design System

Element
Specification

**Theme**
Dense Bloomberg-style dark/gold palette

**Navigator**
Fixed 180px market navigator sidebar

**Ticker**
Global market ticker — always visible

**Clock**
Live local clock in status bar

**Status Bar**
Persistent paper-mode / risk status

**Tables**
Compact dense option tables

### Available Tabs

Tab
Description

**Trading**
Live (paper) order entry, positions, P&L

**Backtest**
Walk-forward engine, config, results visualization

**Execution / Risk**
Paper execution preview, portfolio Greeks, risk summary

> **When database or live data is unavailable:** Trading and Backtest tabs
> remain fully functional with synthetic data. Execution tab is paper-only.

---

## 📐 Formula Reference

### Put/Call Ratio (PCR)

```
PCR = Total Put Open Interest / Total Call Open Interest
```

A PCR > 1 indicates put-heavy positioning (bearish hedging or directional bets).
A PCR < 1 indicates call-heavy positioning.

### Max Pain Strike

```
For each candidate strike S:
  payout(S) = Σ [ call_oi(k) × max(0, S - k) + put_oi(k) × max(0, k - S) ]
              for all strikes k

max_pain = argmin_S payout(S)
```

Max pain is the strike at which the total option payout to holders is minimized —
often where the most open interest stands to expire worthless.

### OI Change

```
OI Change (strike) = Current OI − Previous Snapshot OI
```

Positive = fresh positioning added. Negative = positions closed or expired.

### Put/Call Weighted Levels

```
Call Weighted Level = Σ (call_oi × strike) / Σ call_oi
Put Weighted Level  = Σ (put_oi  × strike) / Σ put_oi
```

Omitted when the relevant side has zero total OI.

---

## 🛡️ Safety & Compliance

Aspect
Implementation

**Execution Default**
✅ Paper-only — no live broker adapter shipped

**Live Enablement Gate**
✅ Requires explicit flags + confirmation token + kill switch

**FinSQL Mutations**
✅ Rejected before execution — SELECT queries only

**Audit Trail**
✅ Append-only audit models — no post-entry mutation

**Copilot Tools**
✅ Read-only registry — cannot place orders

**Offline Resilience**
✅ Degraded dependency reporting — never silently hides failure

**Database Optional**
✅ API and desktop run fully without PostgreSQL

**Compliance Docs**
✅ `docs/PHASE4_SAFETY.md` — live connector requirements

> **Live broker connectivity is intentionally excluded** until a broker,
> credentials policy, compliance jurisdiction, and independent operational
> review are specified and signed off.

---

## 🔮 Future Enhancements

Feature
Status
Target

**BankNIFTY Chain Support**
📋 Planned
Q3 2025

**IPFS Credential Anchoring**
🔄 Researching
Q3 2025

**Presentation Exchange**
📋 Planned
Q4 2025

**Live Broker Adapter**
📋 Requires review
Q4 2025+

**Multi-Expiry Chain View**
📋 Planned
Q1 2026

**ZK-Style Selective Proofs**
📋 Planned
Q2 2026

**Mobile PWA Client**
📋 Planned
Q2 2026

**Governance / Audit Dashboard**
🔄 Designing
Q3 2026

---

## 🤝 Contributing

We welcome contributions from developers, quants, and options researchers.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** changes: `git commit -m "feat: add your feature"`
4. **Push** to branch: `git push origin feature/your-feature`
5. **Open** a Pull Request with a clear description of what changed and why

### Report Issues

Found a bug or have a suggestion?

→ [Open an issue on GitHub](https://github.com/Shreyansh2434/NiftyTerminal/issues)

### Code Style

- Python: follow PEP 8; async functions for all I/O
- TypeScript: strict mode enabled; no `any`
- Commits: [Conventional Commits](https://www.conventionalcommits.org/) format preferred

---

## 📄 License

This project was developed as a **Final Year Major Project** for academic purposes at **UPES**.

---

<div align="center">
<br/>

## 🎯 Vision Statement

> **"Every retail trader deserves the same intelligence that institutions take for granted.**
> 
> 
> **This terminal is that intelligence — open, offline-safe, and safety-first by design."**

<br/>
Built with 📈 precision • 🔒 safety • 🤖 intelligence • 🚀 resilience

*UPES • Final Year Major Project • 2025–2026*

<br/>
[![Explore the Code](https://img.shields.io/badge/Explore%20the%20Code-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shreyansh2434/NiftyTerminal)

<br/>
</div>