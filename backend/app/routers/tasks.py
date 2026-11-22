from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Task).where(Task.owner_id == current_user.id)
    
    if status is not None:
        query = query.where(Task.status == status)
    if priority is not None:
        query = query.where(Task.priority == priority)
        
    query = query.order_by(Task.due_date.asc())
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        owner_id=current_user.id,
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date,
        status=False
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
        
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.owner_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
        
    await db.delete(task)
    await db.commit()
    return None
