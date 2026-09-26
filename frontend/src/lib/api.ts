import axios from "axios";
import type { BacktestRun, BacktestTrade, Chain, Instruments, IVSnapshot, NoTrade, Regime, Signals, Spot, Summary } from "../types";

const baseUrl = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");

const client = axios.create({ baseURL: `${baseUrl}/api`, timeout: 10_000 });

export type Phase3Asset = { symbol: string; name: string; sector: string; price: number; change_percent: number; volume: number };
export type Phase3WorkspaceData = {
  snapshot: { assets: Phase3Asset[]; as_of: string; source: string; offline: boolean };
  heatmap: Array<{ symbol: string; name: string; sector: string; value: number; price: number }>;
  sentiment: { label: string; score: number; confidence: number; headlines: Array<{ text: string; score: number }> };
  sectors: Array<{ sector: string; return_pct: number; advance_count: number; decline_count: number; constituents: string[] }>;
  analyst: { stance: string; confidence: number; summary: string; signals: Array<{ name: string; value: string; rationale: string }> };
};
export type Phase4ChartData = {
  symbol: string; source: string; candles: Array<{ timestamp: string; open: number; high: number; low: number; close: number; volume: number }>;
  volume_profile: Array<{ price: number; volume: number; buy_volume: number; sell_volume: number }>;
  point_of_control: number; value_area: { low: number; high: number };
  order_flow: { buy_imbalance: number; delta: number };
  market_profile: { poc: number; initial_balance_high: number; initial_balance_low: number };
};
export type AICopilotData = {
  as_of?: string;
  symbol?: string;
  regime?: string;
  confidence?: number;
  summary?: string;
  forecast?: Array<{ horizon?: string; direction?: string; target?: string | number; confidence?: number }>;
  deep_dive?: Array<{ title?: string; detail?: string; signal?: string }>;
  historical_analogues?: Array<{ period?: string; match?: string | number; outcome?: string }>;
  risk?: Array<{ label?: string; value?: string | number; status?: string }>;
  [key: string]: unknown;
};

async function request<T>(path: string): Promise<T> {
  const response = await client.get<T>(path);
  return response.data;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await client.post<T>(path, body);
  return response.data;
}

export const api = {
  spot: () => request<Spot>("/market/spot?symbol=NIFTY"),
  chain: () => request<Chain>("/options?symbol=NIFTY"),
  summary: () => request<Summary>("/analytics/summary?symbol=NIFTY"),
  signals: () => request<Signals>("/analytics/signals?symbol=NIFTY"),
  iv: () => request<IVSnapshot>("/iv?symbol=NIFTY"),
  regime: () => request<Regime>("/regime?symbol=NIFTY"),
  noTrade: () => request<NoTrade>("/notrade?symbol=NIFTY"),
  health: () => request("/health"),
  instruments: () => request<Instruments>("/instruments"),
  runBacktest: (body: Record<string, unknown> = {}) => post<BacktestRun>("/backtest/run", body),
  backtest: (runId: string) => request<BacktestRun>(`/backtest/run/${runId}`),
  backtestTrades: (runId: string) => request<BacktestTrade[]>(`/backtest/run/${runId}/trades`),
  phase3Workspace: () => request<Phase3WorkspaceData>("/market/workspace"),
  assets: () => request<{ assets: Phase3Asset[] }>("/market/assets"),
  heatmap: () => request<{ cells: Phase3WorkspaceData["heatmap"] }>("/market/heatmap"),
  sentiment: () => request<Phase3WorkspaceData["sentiment"]>("/sentiment"),
  sectors: () => request<{ sectors: Phase3WorkspaceData["sectors"] }>("/sectors"),
  runMultiAssetBacktest: (body: Record<string, unknown> = {}) =>
    post<Record<string, unknown>>("/backtests/multi-asset/run", body),
  phase4Chart: () => request<Phase4ChartData>("/chart-data?symbol=NIFTY"),
  phase4Portfolio: () => request<Record<string, unknown>>("/portfolio"),
  phase4Risk: () => request<Record<string, unknown>>("/risk"),
  phase4Compliance: () => request<Record<string, unknown>>("/compliance"),
  phase4Preview: () => request<Record<string, unknown>>("/execution/preview?symbol=NIFTY&side=BUY&quantity=1&price=22184.6"),
  aiCopilot: (symbol = "NIFTY") => request<AICopilotData>(`/ai/copilot?symbol=${encodeURIComponent(symbol)}`),
  aiCopilotQuery: (query: string, symbol = "NIFTY") =>
    post<AICopilotData>("/ai/copilot/query", { query, symbol }),
};
