from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import Task, User
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str = Field(..., max_length=255)
    priority: str = Field(..., pattern="^(low|medium|high)$")
    due_date: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
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

@router.get("", response_model=List[TaskResponse])
async def list_tasks(status: Optional[bool] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = select(Task).where(Task.owner_id == current_user.id)
    if status is not None:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_task = Task(
        owner_id=current_user.id,
        title=task_in.title,
        priority=task_in.priority,
        due_date=task_in.due_date,
        status=False
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.patch("/{id}", response_model=TaskResponse)
async def update_task(id: int, task_in: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == id, Task.owner_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
    return None
