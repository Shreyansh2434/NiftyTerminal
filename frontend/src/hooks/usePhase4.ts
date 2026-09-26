import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export function usePhase4() {
  const chart = useQuery({ queryKey: ["phase4-chart"], queryFn: api.phase4Chart });
  const portfolio = useQuery({ queryKey: ["phase4-portfolio"], queryFn: api.phase4Portfolio });
  const risk = useQuery({ queryKey: ["phase4-risk"], queryFn: api.phase4Risk });
  const compliance = useQuery({ queryKey: ["phase4-compliance"], queryFn: api.phase4Compliance });
  const preview = useQuery({ queryKey: ["phase4-preview"], queryFn: api.phase4Preview });
  return { chart, portfolio, risk, compliance, preview };
}
