export type Meta = {
  source: string;
  cached: boolean;
  generated_at: string;
  warning?: string | null;
};

export type Spot = {
  symbol: string;
  value: number | null;
  change: number | null;
  change_percent: number | null;
  timestamp: string;
  meta: Meta;
};

export type OptionRow = {
  strike: number;
  call_oi: number;
  call_oi_change: number;
  call_volume: number;
  call_iv: number | null;
  call_ltp: number | null;
  put_oi: number;
  put_oi_change: number;
  put_volume: number;
  put_iv: number | null;
  put_ltp: number | null;
};

export type Chain = {
  symbol: string;
  expiry: string | null;
  spot: number | null;
  rows: OptionRow[];
  expiries: string[];
  meta: Meta;
};

export type Summary = {
  symbol: string;
  spot: number | null;
  pcr: number | null;
  max_pain: number | null;
  call_wall: number | null;
  put_wall: number | null;
  support: number | null;
  resistance: number | null;
  bias: string;
  meta: Meta;
};

export type Signal = {
  name: string;
  value: string;
  confidence: number;
  rationale: string;
};

export type Signals = { symbol: string; signals: Signal[]; meta: Meta };

export type IVPoint = {
  strike: number;
  call_iv: number | null;
  put_iv: number | null;
};

export type IVSnapshot = {
  symbol: string;
  spot: number | null;
  atm_iv: number | null;
  call_iv: number | null;
  put_iv: number | null;
  points: IVPoint[];
  meta: Meta;
};

export type Regime = {
  symbol: string;
  regime: string;
  bias: string;
  score: number;
  rationale: string;
  meta: Meta;
};

export type NoTrade = {
  symbol: string;
  no_trade: boolean;
  status: string;
  reasons: string[];
  meta: Meta;
};

export type Instrument = {
  symbol: string;
  name: string;
  kind: string;
  active: boolean;
};

export type Instruments = { instruments: Instrument[] };

export type BacktestTrade = {
  id?: number;
  trade_number: number;
  symbol: string;
  regime: string;
  strategy_type?: string;
  entry_date: string;
  exit_date?: string | null;
  entry_spot?: number | null;
  exit_spot?: number | null;
  legs: Record<string, unknown>[];
  gross_pnl: number;
  commission: number;
  slippage: number;
  net_pnl: number;
  return_pct: number;
  exit_reason?: string | null;
};

export type BacktestRun = {
  run_id: string;
  status: string;
  symbol: string;
  started_at?: string | null;
  completed_at?: string | null;
  configuration: Record<string, unknown>;
  metrics: Record<string, number | null>;
  equity_curve: { date: string; equity: number }[];
  walk_forward: { fold: number; train_start: string; train_end: string; test_start: string; test_end: string; metrics: Record<string, number | null> }[];
  regime_stats: Record<string, Record<string, number | null>>;
  trades_count: number;
  warning?: string | null;
  error?: string | null;
};
