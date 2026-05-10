import { useEffect, useState } from "react";
import API from "../api/api";

export default function SupportDashboard() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    const res = await API.get("/tickets/all");
    setTickets(res.data);
  };

  const updateStatus = async (id, status) => {
    await API.patch(`/tickets/${id}/status`, null, {
      params: { status },
    });

    fetchTickets();
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Support Dashboard</h1>

      {tickets.map((t) => (
        <div key={t.id} className="border p-4 mb-3 rounded">
          <div className="font-semibold">{t.title}</div>
          <div>{t.description}</div>
          <div>Status: {t.status}</div>

          <div className="flex gap-2 mt-2">
            <button onClick={() => updateStatus(t.id, "in_progress")}>
              In Progress
            </button>
            <button onClick={() => updateStatus(t.id, "resolved")}>
              Resolve
            </button>
            <button onClick={() => updateStatus(t.id, "closed")}>Close</button>
          </div>
        </div>
      ))}
    </div>
  );
}
