import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export function useBacktest(runId?: string) {
  const run = useQuery({
    queryKey: ["backtest", runId],
    queryFn: () => api.backtest(runId!),
    enabled: Boolean(runId),
  });
  const trades = useQuery({
    queryKey: ["backtest-trades", runId],
    queryFn: () => api.backtestTrades(runId!),
    enabled: Boolean(runId),
  });
  const execute = useMutation({ mutationFn: (body: Record<string, unknown>) => api.runBacktest(body) });
  return { run: run.data, trades: trades.data || [], loading: run.isLoading || trades.isLoading, execute };
}
