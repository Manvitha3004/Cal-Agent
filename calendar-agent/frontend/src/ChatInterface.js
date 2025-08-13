import React, { useState, useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import { socket } from "./api";

function ChatInterface({ token, userId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    socket.auth = { token };
    socket.connect();
    socket.on("bot_response", (data) => {
      setMessages((msgs) => [...msgs, { sender: "bot", text: data.message }]);
    });
    socket.on("meeting_scheduled", (data) => {
      setMessages((msgs) => [...msgs, { sender: "bot", text: `Meeting scheduled: ${data.details.title}` }]);
    });
    return () => {
      socket.off("bot_response");
      socket.off("meeting_scheduled");
      socket.disconnect();
    };
  }, [token, userId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { sender: "user", text: input }]);
    socket.emit("chat_message", { user_id: userId, message: input });
    setInput("");
  }

  return (
    <div style={{ border: "1px solid #ccc", borderRadius: 8, padding: 16, marginBottom: 20 }}>
      <div style={{ height: 250, overflowY: "auto", marginBottom: 10 }}>
        {messages.map((msg, i) => (
          <MessageBubble key={i} sender={msg.sender} text={msg.text} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={sendMessage} style={{ display: "flex" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a message..."
          style={{ flex: 1, marginRight: 8 }}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default ChatInterface;
