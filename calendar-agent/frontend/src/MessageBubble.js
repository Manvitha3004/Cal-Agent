import React from "react";

function MessageBubble({ sender, text }) {
  const isUser = sender === "user";
  return (
    <div style={{
      textAlign: isUser ? "right" : "left",
      margin: "6px 0"
    }}>
      <span style={{
        display: "inline-block",
        background: isUser ? "#007bff" : "#eee",
        color: isUser ? "#fff" : "#333",
        borderRadius: 16,
        padding: "8px 16px",
        maxWidth: "70%"
      }}>{text}</span>
    </div>
  );
}

export default MessageBubble;
