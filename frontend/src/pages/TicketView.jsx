import { useEffect, useState } from "react";
import API from "../api/api";
import { useParams } from "react-router-dom";

export default function TicketView() {
  const { id } = useParams();

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  const token = localStorage.getItem("token");

  useEffect(() => {
    fetchConversation();
  }, []);

  const fetchConversation = async () => {
    const res = await API.get(`/tickets/${id}/conversation`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    setMessages(res.data);
  };

  const sendMessage = async () => {
    await API.post(
      `/tickets/${id}/messages`,
      { message: text },
      `http://127.0.0.1:8000/tickets/${id}/messages`,
      { message: text },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    setText("");
    fetchConversation();
  };

  return (
    <div>
      <h2>Ticket Conversation</h2>

      <div>
        {messages.map((msg, i) => (
          <div key={i}>
            <b>{msg.sender}</b> : {msg.message}
          </div>
        ))}
      </div>

      <input value={text} onChange={(e) => setText(e.target.value)} />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
