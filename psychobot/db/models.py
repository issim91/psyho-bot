from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    summary = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    sender = Column(String(50), nullable=False)  # 'user' or 'psychologist'
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("Session", back_populates="messages") 