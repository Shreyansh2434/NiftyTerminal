import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import DashboardPage from "./pages/DashboardPage";
import BacktestPage from "./pages/BacktestPage";
import Phase3Workspace from "./pages/Phase3Workspace";
import Phase4Workspace from "./pages/Phase4Workspace";
import AICopilot from "./pages/AICopilot";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { refetchOnWindowFocus: false },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {window.location.pathname.startsWith("/backtest") ? <BacktestPage /> :
        window.location.pathname.startsWith("/ai") || window.location.pathname.startsWith("/copilot") ? <AICopilot /> :
        window.location.pathname.startsWith("/phase4") ? <Phase4Workspace /> :
        window.location.pathname.startsWith("/phase3") || window.location.pathname.startsWith("/workspace") ? <Phase3Workspace /> : <DashboardPage />}
    </QueryClientProvider>
  );
}
