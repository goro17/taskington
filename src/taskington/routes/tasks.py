"""API router for managing tasks."""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

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
