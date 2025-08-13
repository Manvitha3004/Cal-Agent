from database import db
from models import Meeting
from datetime import datetime, timedelta
import asyncio
from fastapi import HTTPException

async def check_conflict(user_id: str, meeting_time: datetime, duration: int):
    start = meeting_time
    end = meeting_time + timedelta(minutes=duration)
    meetings = await db.meetings.find({"user_id": user_id}).to_list(length=100)
    for m in meetings:
        m_start = m["datetime"]
        m_end = m_start + timedelta(minutes=m["duration_minutes"])
        if (start < m_end and end > m_start):
            return True
    return False

async def save_meeting(meeting: Meeting):
    conflict = await check_conflict(meeting.user_id, meeting.datetime, meeting.duration_minutes)
    if conflict:
        raise HTTPException(status_code=400, detail="Meeting time conflicts with existing meeting.")
    result = await db.meetings.insert_one(meeting.dict())
    meeting_id = str(result.inserted_id)
    asyncio.create_task(schedule_reminder(meeting_id, meeting.datetime, meeting.user_id))
    return meeting_id

async def schedule_reminder(meeting_id: str, meeting_time: datetime, user_id: str):
    now = datetime.utcnow()
    delay = (meeting_time - timedelta(minutes=5) - now).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)
    # Here, you would send a reminder (e.g., via websocket, notification, etc.)
    # For now, just print
    print(f"Reminder: Meeting {meeting_id} for user {user_id} starts in 5 minutes!")
