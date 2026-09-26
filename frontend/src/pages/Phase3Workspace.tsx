import { Activity, BarChart3, BrainCircuit, LayoutDashboard, Radio, RefreshCw, ShieldAlert } from "lucide-react";
import type { ReactNode } from "react";
import { usePhase3 } from "../hooks/usePhase3";
import { api } from "../lib/api";

const fmt = (value: number) => `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className="p3-panel"><div className="p3-panel-title">{title}</div>{children}</section>;
}

export default function Phase3Workspace() {
  const { data, isLoading, isError, refetch } = usePhase3();
  const assets = data?.snapshot.assets || [];
  return (
    <div className="p3-shell">
      <aside className="p3-sidebar">
        <div className="p3-brand">MARKET<br /><b>TERMINAL</b></div>
        <small>MARKET NAVIGATOR</small>
        {["Overview", "Heatmap", "Sentiment", "Sectors", "Markets", "Portfolio / Risk", "Strategy Lab"].map((item, index) =>
          <button className={index === 0 ? "active" : ""} key={item}><LayoutDashboard size={14} />{item}</button>)}
        <div className="p3-offline">● OFFLINE-SAFE<br />DETERMINISTIC FEED</div>
      </aside>
      <main className="p3-main">
        <header className="p3-ticker"><span>GLOBAL TICKER</span>{assets.slice(0, 4).map((asset) =>
          <b className={asset.change_percent >= 0 ? "up" : "down"} key={asset.symbol}>{asset.symbol} {asset.price.toLocaleString("en-IN")} {fmt(asset.change_percent)}</b>)}
          <button className="p3-refresh" onClick={() => void refetch()}><RefreshCw size={14} /> REFRESH</button>
        </header>
        <div className="p3-title"><div><small>PHASE 3 / MULTI-ASSET INTELLIGENCE</small><h1>Market workspace</h1></div><span className="p3-live"><Radio size={13} /> DETERMINISTIC</span></div>
        {(isError || isLoading) && <div className="p3-alert">{isLoading ? "Loading offline workspace…" : "API unavailable — retrying safely."}</div>}
        <div className="p3-grid">
          <Panel title="MARKET HEATMAP"><div className="heatmap">{(data?.heatmap || []).map((cell) =>
            <div className={cell.value >= 0 ? "heat up-bg" : "heat down-bg"} key={cell.symbol}><strong>{cell.symbol}</strong><span>{fmt(cell.value)}</span><small>{cell.sector}</small></div>)}</div></Panel>
          <Panel title="AI ANALYST"><div className="analyst"><BrainCircuit size={28} /><strong>{data?.analyst.stance || "SELECTIVE"}</strong><span>{data?.analyst.summary || "Rule-based market read"}</span><em>Confidence {Math.round((data?.analyst.confidence || 0) * 100)}%</em></div></Panel>
          <Panel title="SENTIMENT MONITOR"><div className="big-signal"><Activity size={20} /><strong>{data?.sentiment.label || "NEUTRAL"}</strong><span>{(data?.sentiment.score || 0).toFixed(2)} score · {Math.round((data?.sentiment.confidence || 0) * 100)}% confidence</span></div>{(data?.sentiment.headlines || []).map((headline) => <p className="p3-news" key={headline.text}>{headline.text}</p>)}</Panel>
          <Panel title="SECTOR PERFORMANCE">{(data?.sectors || []).map((sector) => <div className="sector-row" key={sector.sector}><b>{sector.sector}</b><span>{sector.advance_count}/{sector.advance_count + sector.decline_count}</span><strong className={sector.return_pct >= 0 ? "up" : "down"}>{fmt(sector.return_pct)}</strong></div>)}</Panel>
          <Panel title="PORTFOLIO / RISK"><div className="risk-grid"><span>Exposure <b>62%</b></span><span>Cash <b>38%</b></span><span>Beta <b>0.86</b></span><span>VaR (95%) <b>1.42%</b></span></div><div className="risk-note"><ShieldAlert size={14} /> Regime: TRENDING</div></Panel>
          <Panel title="MARKETS / ECONOMIC NEWS"><p className="p3-news">RBI policy — next event</p><p className="p3-news">US CPI — monitor rates</p><p className="p3-news">Offline headlines are labelled and reproducible.</p></Panel>
        </div>
        <Panel title="MULTI-ASSET BACKTEST / STRATEGY LAB"><div className="strategy-lab"><select><option>Equal-weight momentum</option><option>Sector rotation</option><option>Volatility target</option></select><span>Aggregate · per-asset · per-sector · per-regime results</span><button onClick={() => void apiRun()}>RUN OFFLINE BACKTEST <BarChart3 size={14} /></button></div></Panel>
      </main>
    </div>
  );
}

async function apiRun() {
  await api.runMultiAssetBacktest({ days: 180 });
}
