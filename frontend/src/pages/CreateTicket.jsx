import { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

export default function CreateTicket() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");

  const navigate = useNavigate();

  const createTicket = async () => {
    const token = localStorage.getItem("token");

    await API.post(
      "/tickets/",
      {
        title,
        description,
        priority,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    navigate("/dashboard");
  };

  return (
    <div>
      <h2>Create Ticket</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option>low</option>
        <option>medium</option>
        <option>high</option>
        <option>urgent</option>
      </select>

      <button onClick={createTicket}>Submit</button>
    </div>
  );
}
