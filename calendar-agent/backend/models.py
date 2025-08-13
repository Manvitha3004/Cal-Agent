from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str]
    username: str
    password_hash: str

class Meeting(BaseModel):
    id: Optional[str]
    user_id: str
    title: str
    datetime: datetime
    attendees: List[str]
    link: Optional[str] = None
    duration_minutes: int

class Conversation(BaseModel):
    id: Optional[str]
    user_id: str
    messages: List[str]
