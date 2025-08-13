import React, { useState } from "react";
import ChatInterface from "./ChatInterface";
import MeetingList from "./MeetingList";

function App() {
  const [token, setToken] = useState("");
  const [userId, setUserId] = useState("");

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Calendar Agent</h2>
      {!token ? (
        <Login setToken={setToken} setUserId={setUserId} />
      ) : (
        <>
          <ChatInterface token={token} userId={userId} />
          <MeetingList token={token} />
        </>
      )}
    </div>
  );
}

function Login({ setToken, setUserId }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    const url = `/auth/${isRegister ? "register" : "login"}`;
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (res.ok) {
        setToken(data.access_token);
        setUserId(username);
      } else {
        setError(data.detail || "Error");
      }
    } catch {
      setError("Network error");
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" required />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">{isRegister ? "Register" : "Login"}</button>
      <button type="button" onClick={() => setIsRegister(x => !x)} style={{ marginLeft: 10 }}>
        {isRegister ? "Go to Login" : "Go to Register"}
      </button>
      {error && <div style={{ color: "red" }}>{error}</div>}
    </form>
  );
}

export default App;
