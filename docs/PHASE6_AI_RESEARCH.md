# Phase 6 AI research layer

Phase 6 is an offline-first research copilot, not an execution agent.

## Copilot tools

The local registry provides:

- `quote(symbol)`
- `options(symbol)`
- `backtest(config)`
- `monte_carlo(params)`

`GET /api/ai/copilot` returns the safe read-only snapshot. `POST
/api/ai/copilot/query` routes terminal-style prompts such as `NIFTY OPTIONS`,
`BACKTEST RSI < 30`, and `MONTE CARLO` to the appropriate research tool.

## Financial SQL

`POST /api/ai/fin-sql` accepts a supported natural-language query and returns
parameterized SQL, confidence, and a sample-size estimate. The validator
requires one `SELECT`/`WITH` statement and rejects comments, mutations,
administrative statements, and multiple statements. Execution must be
explicitly requested and fails clearly when the optional database is
unavailable.

## Historical analogues

`POST /api/ai/analogues` performs deterministic nearest-neighbour matching over
numeric feature vectors. Results default to three matches and include regime,
distance, similarity percentage, and optional 5/10/30-session forward outcomes
when those fields are present in the supplied history.

All outputs are research-only and include offline/deterministic provenance.
The layer does not submit orders, call a broker, or turn on live trading.
