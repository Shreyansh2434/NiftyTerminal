import type { OptionRow } from "../types";
import { EmptyState } from "./EmptyState";

function oi(value: number) {
  return value ? new Intl.NumberFormat("en-IN", { notation: "compact", maximumFractionDigits: 1 }).format(value) : "—";
}

export function OptionChainTable({ rows, spot }: { rows: OptionRow[]; spot: number | null }) {
  if (!rows.length) return <EmptyState message="Option chain is empty" />;
  const nearby = rows.filter((row) => spot === null || Math.abs(row.strike - spot) < 800).slice(0, 21);
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th colSpan={3}>CALLS</th>
            <th>STRIKE</th>
            <th colSpan={3}>PUTS</th>
          </tr>
          <tr className="subhead">
            <th>OI</th><th>Δ OI</th><th>IV</th><th />
            <th>IV</th><th>Δ OI</th><th>OI</th>
          </tr>
        </thead>
        <tbody>
          {nearby.map((row) => (
            <tr key={row.strike} className={spot !== null && Math.abs(row.strike - spot) < 60 ? "atm" : ""}>
              <td className="call">{oi(row.call_oi)}</td>
              <td className={row.call_oi_change >= 0 ? "positive" : "negative"}>{oi(row.call_oi_change)}</td>
              <td>{row.call_iv ? `${row.call_iv.toFixed(1)}%` : "—"}</td>
              <td className="strike">{row.strike.toLocaleString("en-IN")}</td>
              <td>{row.put_iv ? `${row.put_iv.toFixed(1)}%` : "—"}</td>
              <td className={row.put_oi_change >= 0 ? "positive" : "negative"}>{oi(row.put_oi_change)}</td>
              <td className="put">{oi(row.put_oi)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
