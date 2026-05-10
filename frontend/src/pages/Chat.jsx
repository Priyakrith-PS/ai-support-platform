import { useEffect, useState } from "react";
import API from "../api/api";
import ReactMarkdown from "react-markdown";

export default function Chat() {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [mode, setMode] = useState("rag");

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
    const id = res.data.id;

    localStorage.setItem("chat_session", id);
    setSession(id);
    loadMessages(id);
  };

  const loadMessages = async (id) => {
    const res = await API.get(`/chat/session/${id}`);
    setMessages(res.data);
  };

  const sendMessage = async () => {
    if (!text.trim() || !session) return;

    const userText = text;

    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: "user", message: userText },
    ]);

    setText("");

    try {
      const res = await API.post("/chat/send", null, {
        params: {
          session_id: session,
          message: userText,
          mode: mode,
        },
      });

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: "ai", message: res.data.reply },
      ]);
    } catch (err) {
      console.error(err);
      alert("Error sending message");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <div className="bg-white shadow p-4 flex justify-between items-center">
        <div className="text-xl font-bold">AI Assistant</div>

        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="border rounded px-3 py-1"
        >
          <option value="rag">RAG</option>
          <option value="finetuned">Fine-Tuned</option>
        </select>
      </div>

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
              <ReactMarkdown>{m.message}</ReactMarkdown>
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 bg-white flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your message..."
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
