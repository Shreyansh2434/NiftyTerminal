import { FormEvent, useMemo, useState, type ReactNode } from "react";
import { BrainCircuit, ChevronRight, CircleAlert, LoaderCircle, Send, ShieldAlert, Sparkles } from "lucide-react";
import { useAICopilot } from "../hooks/useAICopilot";
import type { AICopilotData } from "../lib/api";

const tabs = ["SUMMARY", "FORECAST", "DEEP DIVE", "HISTORICAL ANALOGUES", "RISK"] as const;
type Tab = typeof tabs[number];

const fallback: AICopilotData = {
  symbol: "NIFTY", regime: "DATA PENDING", confidence: 0,
  summary: "Connect the intelligence service to populate the copilot readout.",
  forecast: [{ horizon: "NEXT SESSION", direction: "AWAITING DATA", target: "—", confidence: 0 }],
  deep_dive: [{ title: "NO LIVE CONTEXT", detail: "The backend did not return a copilot payload. This panel remains safe and read-only.", signal: "PENDING" }],
  historical_analogues: [{ period: "—", match: "—", outcome: "No analogue data" }],
  risk: [{ label: "MODEL STATUS", value: "UNAVAILABLE", status: "CAUTION" }],
};

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className="ai-panel"><div className="ai-panel-title">{title}<span>■</span></div>{children}</section>;
}

export default function AICopilot() {
  const { snapshot, query } = useAICopilot();
  const [tab, setTab] = useState<Tab>("SUMMARY");
  const [command, setCommand] = useState("");
  const data = useMemo(() => ({ ...fallback, ...(snapshot.data || {}), ...(query.data || {}) }), [snapshot.data, query.data]);
  const error = snapshot.isError || query.isError;

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const value = command.trim();
    if (value) { query.mutate(value); setCommand(""); }
  };

  return <div className="ai-shell">
    <header className="ai-header">
      <div><small>PHASE 6 / AI MARKET INTELLIGENCE</small><h1><BrainCircuit size={25} /> AI COPILOT</h1></div>
      <div className="ai-status"><span className={snapshot.isSuccess ? "ai-dot live" : "ai-dot"} /> {snapshot.isSuccess ? "MODEL ONLINE" : "SAFE MODE"}<b>{data.symbol || "NIFTY"}</b></div>
    </header>
    {error && <div className="ai-alert"><CircleAlert size={15} /> Intelligence API unavailable — showing a safe placeholder. Queries will retry when the service is available.</div>}
    <nav className="ai-tabs" aria-label="Copilot sections">{tabs.map((item) => <button key={item} className={tab === item ? "active" : ""} onClick={() => setTab(item)}>{item}</button>)}</nav>
    <div className="ai-grid">
      <Panel title="LIVE CONTEXT"><div className="ai-context"><strong>{data.regime}</strong><span>REGIME</span><strong>{Math.round((Number(data.confidence) || 0) * 100)}%</strong><span>CONFIDENCE</span></div></Panel>
      <Panel title={tab}><Content tab={tab} data={data} loading={snapshot.isLoading || query.isPending} /></Panel>
    </div>
    <form className="ai-command" onSubmit={submit}><span>copilot@nifty:~$</span><input value={command} onChange={(event) => setCommand(event.target.value)} placeholder="ask about trend, levels, risk or analogues…" aria-label="Copilot command" /><button disabled={query.isPending || !command.trim()}><Send size={15} /></button></form>
    <footer className="ai-footer"><Sparkles size={13} /> READ-ONLY INTELLIGENCE · NOT INVESTMENT ADVICE <span>as of {data.as_of || "—"}</span></footer>
  </div>;
}

function Content({ tab, data, loading }: { tab: Tab; data: AICopilotData; loading: boolean }) {
  if (loading) return <div className="ai-loading"><LoaderCircle className="spin" size={20} /> QUERYING MODEL…</div>;
  if (tab === "SUMMARY") return <div className="ai-summary"><strong>{data.summary}</strong><p>Use the command line below to ask a focused question. Every response is advisory and read-only.</p></div>;
  if (tab === "FORECAST") return <div className="ai-list">{(data.forecast || []).map((row, index) => <div className="ai-row" key={`${row.horizon}-${index}`}><b>{row.horizon || "HORIZON"}</b><span>{row.direction || "—"} · target {row.target ?? "—"}</span><em>{Math.round((Number(row.confidence) || 0) * 100)}%</em></div>)}</div>;
  if (tab === "DEEP DIVE") return <div className="ai-list">{(data.deep_dive || []).map((row, index) => <div className="ai-card" key={`${row.title}-${index}`}><b>{row.title}</b><span>{row.detail}</span><em>{row.signal || "—"}</em></div>)}</div>;
  if (tab === "HISTORICAL ANALOGUES") return <div className="ai-list">{(data.historical_analogues || []).map((row, index) => <div className="ai-row" key={`${row.period}-${index}`}><b>{row.period || "PERIOD"}</b><span>match {row.match ?? "—"}</span><em>{row.outcome || "—"}</em></div>)}</div>;
  return <div className="ai-list">{(data.risk || []).map((row, index) => <div className="ai-row" key={`${row.label}-${index}`}><b><ShieldAlert size={13} /> {row.label || "RISK"}</b><span>{row.value ?? "—"}</span><em>{row.status || "—"} <ChevronRight size={12} /></em></div>)}</div>;
}
