import { useEffect, useState } from "react";
import API from "../api/api";

export default function Chat() {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    const existingSession = localStorage.getItem("chat_session");

    if (existingSession) {
      setSession(existingSession);
      loadMessages(existingSession);
    } else {
      createSession();
    }
  }, []);

  const createSession = async () => {
    const res = await API.post("/chat/session");

    const sessionId = res.data.id;

    localStorage.setItem("chat_session", sessionId);

    setSession(sessionId);
  };

  const sendMessage = async () => {
    await API.post("/chat/message", null, {
      params: {
        session_id: session,
        message: text,
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    setText("");
    loadMessages();
  };

  const loadMessages = async (sessionId) => {
    const res = await API.get(`/chat/session/${sessionId}`);

    setMessages(res.data);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <div className="bg-white shadow p-4 text-xl font-bold">AI Assistant</div>

      <div className="flex-1 p-6 overflow-y-auto">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`mb-3 flex ${
              m.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-lg max-w-md ${
                m.sender === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-white border"
              }`}
            >
              {m.message}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 bg-white flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-4 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
