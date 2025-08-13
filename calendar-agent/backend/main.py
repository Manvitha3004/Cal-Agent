from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from database import db
from models import User, Meeting
from schemas import UserCreate, UserLogin, Token, MeetingCreate, MeetingOut
from auth import get_password_hash, verify_password, create_access_token, get_current_user
import chat
import socketio
from bson import ObjectId

app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

sio_app = socketio.ASGIApp(chat.sio)

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists.")
    password_hash = get_password_hash(user.password)
    user_doc = {"username": user.username, "password_hash": password_hash}
    result = await db.users.insert_one(user_doc)
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)

@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    user_doc = await db.users.find_one({"username": user.username})
    if not user_doc or not verify_password(user.password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)

@app.get("/meetings", response_model=list[MeetingOut])
async def list_meetings(current_user: str = Depends(get_current_user)):
    user_doc = await db.users.find_one({"username": current_user})
    meetings = await db.meetings.find({"user_id": str(user_doc["_id"])}).to_list(length=100)
    return [MeetingOut(id=str(m["_id"]), title=m["title"], datetime=m["datetime"], attendees=m["attendees"], link=m.get("link"), duration_minutes=m["duration_minutes"]) for m in meetings]

@app.post("/meetings", response_model=MeetingOut)
async def create_meeting(meeting: MeetingCreate, current_user: str = Depends(get_current_user)):
    user_doc = await db.users.find_one({"username": current_user})
    meeting_doc = meeting.dict()
    meeting_doc["user_id"] = str(user_doc["_id"])
    result = await db.meetings.insert_one(meeting_doc)
    m = await db.meetings.find_one({"_id": result.inserted_id})
    return MeetingOut(id=str(m["_id"]), title=m["title"], datetime=m["datetime"], attendees=m["attendees"], link=m.get("link"), duration_minutes=m["duration_minutes"]) 

@app.get("/meetings/{id}", response_model=MeetingOut)
async def get_meeting(id: str, current_user: str = Depends(get_current_user)):
    m = await db.meetings.find_one({"_id": ObjectId(id)})
    if not m or m["user_id"] != str((await db.users.find_one({"username": current_user}))["_id"]):
        raise HTTPException(status_code=404, detail="Meeting not found.")
    return MeetingOut(id=str(m["_id"]), title=m["title"], datetime=m["datetime"], attendees=m["attendees"], link=m.get("link"), duration_minutes=m["duration_minutes"]) 

@app.delete("/meetings/{id}")
async def delete_meeting(id: str, current_user: str = Depends(get_current_user)):
    m = await db.meetings.find_one({"_id": ObjectId(id)})
    if not m or m["user_id"] != str((await db.users.find_one({"username": current_user}))["_id"]):
        raise HTTPException(status_code=404, detail="Meeting not found.")
    await db.meetings.delete_one({"_id": ObjectId(id)})
    return JSONResponse(content={"detail": "Deleted"})

# Mount Socket.IO app
app.mount("/ws", sio_app)
