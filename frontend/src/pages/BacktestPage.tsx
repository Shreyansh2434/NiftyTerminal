import { useState } from "react";
import { AlertTriangle, ArrowLeft, Play, RefreshCw } from "lucide-react";
import { useBacktest } from "../hooks/useBacktest";
import { Panel } from "../components/Panel";

const money = (value: number | null | undefined) =>
  value == null ? "—" : value.toLocaleString("en-IN", { maximumFractionDigits: 0 });

export default function BacktestPage() {
  const [runId, setRunId] = useState<string>();
  const { run, trades, loading, execute } = useBacktest(runId);
  const start = () => execute.mutate({}, { onSuccess: (result) => setRunId(result.run_id) });
  const metrics = run?.metrics || {};
  const maxEquity = Math.max(...(run?.equity_curve || []).map((point) => point.equity), 1);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-mark">N</div><div><h1>NIFTY / BACKTEST</h1><p>WALK-FORWARD LAB <span>· PHASE 2</span></p></div></div>
        <div className="top-actions"><a className="refresh-button" href="/"><ArrowLeft size={14} /> DASHBOARD</a><button className="refresh-button" onClick={start} disabled={execute.isPending}><Play size={14} /> {execute.isPending ? "RUNNING" : "RUN BACKTEST"}</button></div>
      </header>
      <main>
        {(run?.warning || execute.error) && <div className="alert muted"><AlertTriangle size={16} /> {run?.warning || "API unavailable — the run may be available from the resilient in-memory store."}</div>}
        {!run && !loading && <div className="empty-state backtest-empty"><p>Run the sample iron-condor configuration to generate a walk-forward report.</p><button className="run-button" onClick={start}><Play size={15} /> RUN SAMPLE CONFIGURATION</button></div>}
        {loading && <div className="alert muted"><RefreshCw size={15} className="spin" /> Loading backtest result…</div>}
        {run && <><div className="metric-grid">
          <div className="metric-card"><p className="eyebrow">NET P&amp;L</p><p className={`metric-value ${Number(metrics.total_pnl) >= 0 ? "cyan" : "red"}`}>{money(metrics.total_pnl)}</p><p className="metric-detail">{Number(metrics.total_return_pct || 0).toFixed(2)}% total return</p></div>
          <div className="metric-card"><p className="eyebrow">WIN RATE</p><p className="metric-value">{Number(metrics.win_rate || 0).toFixed(1)}%</p><p className="metric-detail">{metrics.total_trades || 0} trades</p></div>
          <div className="metric-card"><p className="eyebrow">SHARPE</p><p className="metric-value">{metrics.sharpe_ratio == null ? "—" : Number(metrics.sharpe_ratio).toFixed(2)}</p><p className="metric-detail">annualized</p></div>
          <div className="metric-card"><p className="eyebrow">MAX DRAWDOWN</p><p className="metric-value red">{money(metrics.max_drawdown)}</p><p className="metric-detail">{Number(metrics.max_drawdown_pct || 0).toFixed(2)}%</p></div>
        </div>
        <div className="dashboard-grid">
          <Panel title="Equity curve" eyebrow="MARK-TO-MARKET"><div className="equity-chart">{run.equity_curve.map((point) => <div className="equity-bar" key={point.date} title={`${point.date}: ${money(point.equity)}`} style={{ height: `${Math.max(3, point.equity / maxEquity * 100)}%` }} />)}</div></Panel>
          <Panel title="Per-regime statistics" eyebrow="REGIME ATTRIBUTION"><div className="regime-grid">{Object.entries(run.regime_stats).map(([regime, stat]) => <div className="regime-row" key={regime}><strong>{regime.replace("_", " ")}</strong><span>{money(stat.total_pnl)} · {Number(stat.win_rate || 0).toFixed(0)}% wins</span></div>)}</div></Panel>
        </div>
        <Panel title="Walk-forward windows" eyebrow={`TRAIN / TEST · ${run.walk_forward.length} FOLDS`}><div className="table-wrap"><table><thead><tr><th>FOLD</th><th>TRAIN</th><th>TEST</th><th>TRADES</th><th>NET P&amp;L</th></tr></thead><tbody>{run.walk_forward.map((fold) => <tr key={fold.fold}><td>{fold.fold}</td><td>{fold.train_start} → {fold.train_end}</td><td>{fold.test_start} → {fold.test_end}</td><td>{fold.metrics.total_trades || 0}</td><td className={Number(fold.metrics.total_pnl) >= 0 ? "positive" : "negative"}>{money(fold.metrics.total_pnl)}</td></tr>)}</tbody></table></div></Panel>
        <Panel title="Trades" eyebrow={`${trades.length} EXECUTED ROUND TRIPS`}><div className="table-wrap"><table><thead><tr><th>#</th><th>ENTRY</th><th>EXIT</th><th>STRATEGY</th><th>REGIME</th><th>SPOT</th><th>NET P&amp;L</th><th>REASON</th></tr></thead><tbody>{trades.map((trade) => <tr key={trade.trade_number}><td>{trade.trade_number}</td><td>{trade.entry_date}</td><td>{trade.exit_date || "—"}</td><td>{trade.strategy_type || "IRON_CONDOR"}</td><td>{trade.regime}</td><td>{money(trade.entry_spot)}</td><td className={trade.net_pnl >= 0 ? "positive" : "negative"}>{money(trade.net_pnl)}</td><td>{trade.exit_reason || "—"}</td></tr>)}</tbody></table></div></Panel>
        </>}
      </main>
      <footer>PHASE 2 · WALK-FORWARD RESEARCH <span>NO-LOOKAHEAD · SPREADS · COMMISSIONS</span></footer>
    </div>
  );
}
