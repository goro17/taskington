"""API router for managing tasks."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from taskington.database.config import get_session
from taskington.models.task import Task, TaskCreate, TaskRead

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    """Create a new task.

    - **title**: Required. The title of the task.
    - **description**: Optional. Detailed description of the task.
    - **priority**: Optional. Priority level (1-5), defaults to 1.
    - **completed**: Optional. Task completion status, defaults to False.
    """
    # Convert TaskCreate model to Task model
    # Using model_validate(...) as from_orm(...) was deprecated
    db_task = Task.model_validate(task)

    # Add to database
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskRead])
def read_tasks(*, session: Session = Depends(get_session), offset: int = 0, limit: int = 100, completed: bool = None):
    """Retrieve a list of tasks with optional filtering.

    - **offset**: Number of tasks to skip (for pagination).
    - **limit**: Maximum number of tasks to return (for pagination).
    - **completed**: Filter by completion status.
    """
    query = select(Task)

    # Apply completion status filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Apply pagination
    tasks = session.exec(query.offset(offset).limit(limit)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
def read_task(*, session: Session = Depends(get_session), task_id: str):
    """Retrieve a specific task by ID.

    - **task_id**: The unique identifier of the task.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

    return task
