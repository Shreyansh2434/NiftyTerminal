import { useQuery } from "@tanstack/react-query";
import { api, type Phase3WorkspaceData } from "../lib/api";

export function usePhase3() {
  return useQuery<Phase3WorkspaceData>({
    queryKey: ["phase3-workspace"],
    queryFn: api.phase3Workspace,
    staleTime: 30_000,
  });
}
