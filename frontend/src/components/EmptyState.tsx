export function EmptyState({ message = "No live data available." }: { message?: string }) {
  return (
    <div className="empty-state">
      <span className="empty-dot" />
      <p>{message}</p>
      <small>Connect the API or wait for the next market refresh.</small>
    </div>
  );
}
