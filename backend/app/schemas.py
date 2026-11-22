from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    priority: Literal["low", "medium", "high"]
    due_date: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    priority: Optional[Literal["low", "medium", "high"]] = None
    due_date: Optional[datetime] = None
    status: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    priority: str
    due_date: datetime
    status: bool
    created_at: datetime

    class Config:
        from_attributes = True
