from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ConversationCreate(BaseModel):
    conversation_text: str

@app.post("/conversations/")
async def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = models.Conversation(conversation_text=conversation.conversation_text)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@app.get("/conversations/")
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = db.query(models.Conversation).offset(skip).limit(limit).all()
    return conversations