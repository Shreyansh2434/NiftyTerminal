import { Activity, AlertTriangle, BarChart3, CircleHelp, RefreshCw, Radio, TrendingDown, TrendingUp } from "lucide-react";
import { useDashboardData } from "../hooks/useDashboardData";
import { EmptyState } from "../components/EmptyState";
import { MetricCard } from "../components/MetricCard";
import { OptionChainTable } from "../components/OptionChainTable";
import { Panel } from "../components/Panel";
import { SpotChart } from "../components/SpotChart";

function fmt(value: number | null, digits = 2) {
  return value === null ? "—" : value.toLocaleString("en-IN", { maximumFractionDigits: digits });
}

export default function DashboardPage() {
  const { spot, chain, summary, signals, error, refreshing, refresh } = useDashboardData();
  const warning = chain?.meta.warning || spot?.meta.warning;
  const bullish = summary?.bias === "BULLISH";

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-mark">N</div><div><h1>NIFTY / OPTIONS</h1><p>INTELLIGENCE TERMINAL <span>· PHASE 1</span></p></div></div>
        <div className="top-actions"><span className="live-chip"><Radio size={12} /> NSE FEED</span><span className="session-chip">MARKET CLOSED</span><a className="refresh-button" href="/backtest">BACKTEST</a><button className="refresh-button" onClick={() => void refresh()} disabled={refreshing}><RefreshCw size={15} className={refreshing ? "spin" : ""} /> REFRESH</button></div>
      </header>
      <main>
        {error && <div className="alert"><AlertTriangle size={16} /> API unavailable — showing an empty terminal.</div>}
        {warning && !error && <div className="alert muted"><AlertTriangle size={16} /> {warning}. Cached or empty values are shown safely.</div>}
        <div className="hero-row">
          <div><p className="eyebrow">INDEX SPOT · {spot?.meta.cached ? "CACHED" : "LIVE"}</p><div className="spot-value">{fmt(spot?.value ?? null)} <span className={spot?.change && spot.change >= 0 ? "positive" : "negative"}>{spot?.change !== null && spot?.change !== undefined ? `${spot.change >= 0 ? "+" : ""}${fmt(spot.change)} (${fmt(spot.change_percent)}%)` : "—"}</span></div><p className="timestamp">Last update {spot ? new Date(spot.timestamp).toLocaleTimeString() : "—"}</p><SpotChart value={spot?.value ?? null} /></div>
          <div className={`bias-badge ${bullish ? "bullish" : summary?.bias === "BEARISH" ? "bearish" : ""}`}><Activity size={18} /><span>BIAS</span><strong>{summary?.bias || "NEUTRAL"}</strong></div>
        </div>
        <div className="metric-grid">
          <MetricCard label="PUT / CALL RATIO" value={fmt(summary?.pcr ?? null, 3)} detail="OI-weighted" />
          <MetricCard label="MAX PAIN" value={fmt(summary?.max_pain ?? null, 0)} detail="minimum payout" accent="amber" />
          <MetricCard label="PUT WALL" value={fmt(summary?.put_wall ?? null, 0)} detail="largest put OI" />
          <MetricCard label="CALL WALL" value={fmt(summary?.call_wall ?? null, 0)} detail="largest call OI" accent="amber" />
        </div>
        <div className="dashboard-grid">
          <Panel title="Option chain" eyebrow={`EXPIRY ${chain?.expiry || "—"}`} className="chain-panel"><OptionChainTable rows={chain?.rows || []} spot={chain?.spot ?? spot?.value ?? null} /></Panel>
          <div className="side-stack">
            <Panel title="Key levels" eyebrow="OI DISTRIBUTION"><div className="levels"><div><span>SUPPORT</span><strong>{fmt(summary?.support ?? null)}</strong><TrendingUp size={15} /></div><div><span>RESISTANCE</span><strong>{fmt(summary?.resistance ?? null)}</strong><TrendingDown size={15} /></div></div><div className="range-line"><span style={{ width: "42%" }} /><i /></div><div className="range-labels"><span>PUT SUPPORT</span><span>CALL RESISTANCE</span></div></Panel>
            <Panel title="Signals" eyebrow="RULE-BASED READ"><div className="signal-list">{signals?.signals?.length ? signals.signals.map((signal) => <div className="signal" key={signal.name}><div className="signal-icon">{signal.value.startsWith("-") ? <TrendingDown size={16} /> : <BarChart3 size={16} />}</div><div><strong>{signal.name}</strong><p>{signal.rationale}</p></div><b>{signal.value}</b></div>) : <EmptyState message="No signals until option data arrives" />}</div></Panel>
          </div>
        </div>
        <Panel title="Desk notes" eyebrow="SYSTEM STATUS" className="notes-panel"><div className="notes"><span><CircleHelp size={14} /> Formula-driven analytics; not financial advice.</span><span><span className="status-dot" /> API resilient mode enabled</span><span>Rows: {chain?.rows.length || 0} · Source: {chain?.meta.source || "empty"}</span></div></Panel>
      </main>
      <footer>PHASE 1 · NIFTY OPTIONS INTELLIGENCE <span>DATA REFRESHES EVERY 60 SECONDS</span></footer>
    </div>
  );
}
