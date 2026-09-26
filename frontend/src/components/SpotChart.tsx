import { useEffect, useRef } from "react";
import { createChart, LineSeries, type IChartApi } from "lightweight-charts";

export function SpotChart({ value }: { value: number | null }) {
  const container = useRef<HTMLDivElement>(null);
  const chart = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!container.current) return;
    const instance = createChart(container.current, {
      height: 72,
      layout: { textColor: "#718093", background: { color: "transparent" } },
      grid: { vertLines: { visible: false }, horzLines: { color: "#202d3d" } },
      rightPriceScale: { visible: false },
      timeScale: { visible: false },
      crosshair: { vertLine: { visible: false }, horzLine: { visible: false } },
    });
    const series = instance.addSeries(LineSeries, { color: "#45d6d2", lineWidth: 2 });
    if (value !== null) {
      const now = Math.floor(Date.now() / 1000);
      series.setData([
        { time: (now - 60) as never, value: value * 0.998 },
        { time: now as never, value },
      ]);
      instance.timeScale().fitContent();
    }
    chart.current = instance;
    return () => {
      instance.remove();
      chart.current = null;
    };
  }, [value]);

  return <div className="spot-chart" ref={container} aria-label="NIFTY spot chart" />;
}
