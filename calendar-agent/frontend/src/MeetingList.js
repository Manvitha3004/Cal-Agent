import React, { useEffect, useState } from "react";

function MeetingList({ token }) {
  const [meetings, setMeetings] = useState([]);

  useEffect(() => {
    async function fetchMeetings() {
      const res = await fetch("/meetings", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        setMeetings(await res.json());
      }
    }
    fetchMeetings();
  }, [token]);

  return (
    <div style={{ border: "1px solid #ccc", borderRadius: 8, padding: 16 }}>
      <h4>Scheduled Meetings</h4>
      {meetings.length === 0 ? (
        <div>No meetings scheduled.</div>
      ) : (
        <ul>
          {meetings.map(m => (
            <li key={m.id}>
              <b>{m.title}</b> <br />
              {new Date(m.datetime).toLocaleString()} <br />
              Attendees: {m.attendees.join(", ")}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MeetingList;
