# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    sender: str
    message: str
    timestamp: datetime

class ConversationCreate(BaseModel):
    conversationId: str
    messages: List[MessageCreate]

class Message(BaseModel):
    id: int
    sender: str
    message: str
    timestamp: datetime
    class Config:
        orm_mode = True

class Conversation(BaseModel):
    id: int
    conversationId: str
    messages: List[Message] = []
    class Config:
        orm_mode = True
