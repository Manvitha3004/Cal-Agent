from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeetingCreate(BaseModel):
    title: str
    datetime: datetime
    attendees: List[str]
    link: Optional[str] = None
    duration_minutes: int

class MeetingOut(BaseModel):
    id: str
    title: str
    datetime: datetime
    attendees: List[str]
    link: Optional[str]
    duration_minutes: int
