export function MetricCard({
  label,
  value,
  detail,
  accent = "cyan",
}: {
  label: string;
  value: string;
  detail?: string;
  accent?: "cyan" | "amber" | "red";
}) {
  return (
    <div className="metric-card">
      <p className="eyebrow">{label}</p>
      <p className={`metric-value ${accent}`}>{value}</p>
      {detail && <p className="metric-detail">{detail}</p>}
    </div>
  );
}
