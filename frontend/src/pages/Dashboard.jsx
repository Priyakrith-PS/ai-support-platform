import { useEffect, useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [tickets, setTickets] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    const token = localStorage.getItem("token");

    const res = await API.get("/tickets/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    setTickets(res.data);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("chat_session");

    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">
            AI-Powered Support System Using FastAPI + React + LLM Integration
          </h1>

          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>

        <button
          onClick={() => navigate("/chat")}
          className="bg-blue-600 text-white px-4 py-2 rounded mb-6"
        >
          Start AI Chat
        </button>

        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">My Tickets</h2>

          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              className="border p-3 rounded mb-2 flex justify-between"
            >
              <span>{ticket.title}</span>

              <button
                onClick={() => navigate(`/ticket/${ticket.id}`)}
                className="text-blue-600"
              >
                Open
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
