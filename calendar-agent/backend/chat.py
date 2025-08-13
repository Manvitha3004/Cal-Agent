import socketio
from nlp_service import extract_meeting_details
from meeting_service import save_meeting
from models import Meeting
from database import db
from fastapi import Depends
from auth import get_current_user

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

@sio.event
async def connect(sid, environ):
    print(f"User connected: {sid}")

@sio.event
async def chat_message(sid, data):
    user_id = data.get("user_id")
    message = data.get("message")
    details = await extract_meeting_details(message)
    if details:
        meeting = Meeting(user_id=user_id, **details)
        try:
            meeting_id = await save_meeting(meeting)
            await sio.emit("meeting_scheduled", {"meeting_id": meeting_id, "details": details}, room=sid)
            await sio.emit("bot_response", {"message": f"Meeting scheduled: {details['title']} at {details['datetime']}"}, room=sid)
        except Exception as e:
            await sio.emit("bot_response", {"message": str(e)}, room=sid)
    else:
        await sio.emit("bot_response", {"message": "Sorry, I couldn't extract meeting details."}, room=sid)
