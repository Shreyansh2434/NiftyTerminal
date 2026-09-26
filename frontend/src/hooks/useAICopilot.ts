import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export function useAICopilot(symbol = "NIFTY") {
  const snapshot = useQuery({
    queryKey: ["ai-copilot", symbol],
    queryFn: () => api.aiCopilot(symbol),
    staleTime: 30_000,
    retry: 1,
  });
  const query = useMutation({
    mutationFn: (prompt: string) => api.aiCopilotQuery(prompt, symbol),
  });
  return { snapshot, query };
}
