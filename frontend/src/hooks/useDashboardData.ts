import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

const queryOptions = {
  refetchInterval: 60_000,
  staleTime: 30_000,
  retry: 1,
};

export function useDashboardData() {
  const spot = useQuery({ queryKey: ["spot", "NIFTY"], queryFn: api.spot, ...queryOptions });
  const chain = useQuery({ queryKey: ["options", "NIFTY"], queryFn: api.chain, ...queryOptions });
  const summary = useQuery({ queryKey: ["summary", "NIFTY"], queryFn: api.summary, ...queryOptions });
  const signals = useQuery({ queryKey: ["signals", "NIFTY"], queryFn: api.signals, ...queryOptions });

  return {
    spot: spot.data ?? null,
    chain: chain.data ?? null,
    summary: summary.data ?? null,
    signals: signals.data ?? null,
    refreshing: [spot, chain, summary, signals].some((query) => query.isFetching),
    error: [spot, chain, summary, signals].every((query) => query.isError),
    refresh: () => Promise.all([spot.refetch(), chain.refetch(), summary.refetch(), signals.refetch()]),
  };
}
