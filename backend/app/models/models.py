from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class HCP(Base):
    __tablename__ = "hcps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    speciality = Column(String)
    hospital = Column(String)
    city = Column(String)
    phone = Column(String)
    email = Column(String)
    preferred_contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_date = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # in minutes
    location = Column(String)
    discussion_summary = Column(Text)
    raw_chat = Column(Text)
    sentiment = Column(String)
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    hcp = relationship("HCP", back_populates="interactions")
    tasks = relationship("Task", back_populates="interaction")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    title = Column(String)
    due_date = Column(DateTime)
    status = Column(String, default="pending")
    
    interaction = relationship("Interaction", back_populates="tasks")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    description = Column(Text)
    url = Column(String)
