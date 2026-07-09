from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class HCPBase(BaseModel):
    name: str
    speciality: str
    hospital: str
    city: str
    phone: str
    email: str
    preferred_contact: str

class HCP(HCPBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class InteractionBase(BaseModel):
    hcp_id: int
    duration: int = Field(gt=0, description="Duration in minutes must be positive")
    location: str
    discussion_summary: str
    sentiment: str
    status: str = "completed"

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    interaction_date: datetime
    created_at: datetime
    raw_chat: Optional[str] = None
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    due_date: datetime
    status: str = "pending"

class TaskCreate(TaskBase):
    interaction_id: int

class Task(TaskBase):
    id: int
    interaction_id: int
    class Config:
        from_attributes = True

class MaterialBase(BaseModel):
    title: str
    category: str
    description: str
    url: str

class Material(MaterialBase):
    id: int
    class Config:
        from_attributes = True
        
# For Chat Interface
class ChatRequest(BaseModel):
    message: str
    session_id: str
