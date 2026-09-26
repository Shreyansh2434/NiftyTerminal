import { usePhase4 } from "../hooks/usePhase4";
import type { ReactNode } from "react";

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className="p4-panel"><h2>{title}</h2>{children}</section>;
}

export default function Phase4Workspace() {
  const { chart, portfolio, risk, compliance, preview } = usePhase4();
  const points = chart.data?.volume_profile || [];
  const bars = chart.data?.candles.slice(-12) || [];
  return <div className="p4-shell">
    <header className="p4-header"><div><small>PHASE 4 / PRODUCTION-GRADE SAFETY LAYER</small><h1>Execution & risk workspace</h1></div><span className="p4-safe">● PAPER ONLY · KILL SWITCH ON</span></header>
    <div className="p4-grid">
      <Panel title="ADVANCED CHART"><div className="p4-bars">{bars.map((bar) => <i key={bar.timestamp} style={{ height: `${Math.max(12, Math.min(100, bar.volume / 20))}%` }} title={`${bar.close}`} />)}</div><small>{chart.data?.source || "offline-deterministic"} · POC {chart.data?.point_of_control ?? "—"}</small></Panel>
      <Panel title="VOLUME PROFILE"><div className="p4-profile">{points.map((p) => <div key={p.price}><span>{p.price}</span><b style={{ width: `${Math.max(8, p.volume / 12)}%` }} /> <em>{p.volume}</em></div>)}</div></Panel>
      <Panel title="ORDER FLOW"><strong className="p4-value">Δ {chart.data?.order_flow.delta ?? "—"}</strong><p>Buy imbalance {Math.round((chart.data?.order_flow.buy_imbalance || 0) * 100)}%</p></Panel>
      <Panel title="PORTFOLIO / GREEKS"><pre>{JSON.stringify(portfolio.data?.greeks || {}, null, 2)}</pre><p>VaR 95% {String(portfolio.data?.var_95 ?? "—")} · CVaR {String(portfolio.data?.cvar_95 ?? "—")}</p></Panel>
      <Panel title="RISK DASHBOARD"><pre>{JSON.stringify(risk.data?.kill_switch || {}, null, 2)}</pre><p>Kelly {String(risk.data?.kelly_fraction ?? "—")}</p></Panel>
      <Panel title="COMPLIANCE"><strong className="p4-safe">{String(compliance.data?.status || "COMPLIANT")}</strong><p>Paper-only audit stream · live orders {String(compliance.data?.live_orders ?? 0)}</p></Panel>
      <Panel title="EXECUTION PREVIEW"><pre>{JSON.stringify(preview.data?.order || {}, null, 2)}</pre><small>No order is placed by preview.</small></Panel>
    </div>
  </div>;
}
