from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    conversationId = Column(String, index=True)
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    message = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship("Conversation", back_populates="messages")
