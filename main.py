from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from datetime import datetime
from .schemas import ConversationCreate, Conversation, MessageCreate
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 여기에 Pydantic 스키마 정의를 포함시킵니다.
@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}
@app.post("/conversations/", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def saveConversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = models.Conversation(conversationId=conversation.conversationId)
    db.add(db_conversation)
    db.commit()
    for msg in conversation.messages:
        db_msg = models.Message(**msg.dict(), conversation_id=db_conversation.id)
        db.add(db_msg)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


@app.get("/conversations/", response_model=List[Conversation])
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = db.query(models.Conversation).offset(skip).limit(limit).all()
    return conversations
